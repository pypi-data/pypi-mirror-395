import signal
import threading
import time

from ..config import PrePostTrainConfig, ShutdownConfig
from ..logging import get_logger
from ..server import AgentState, PLR_VALID_TRANSITIONS
from torch.distributed.elastic.agent.server.api import (
    RunResult,
    WorkerGroup,
    WorkerSpec,
    WorkerState,
    DEFAULT_ROLE,
)
from torch.distributed.elastic.metrics import put_metric
from torch.distributed.elastic.multiprocessing import LogsSpecs
from typing import Optional
from .hyperpod_elastic_agent import HyperPodElasticAgent

logger = get_logger(__name__)
agent_state_lock = threading.Lock()


class PLRHyperPodElasticAgent(HyperPodElasticAgent):
    """
    A HyperPodElasticAgent implementation that supports process-level restart functionality.
    This class contains the original functionality of HyperPodElasticAgent.

    There are a few changes from LocalElasticAgent to PLRHyperPodElasticAgent:
        * The agent state transitions now depend both on the worker state
          and the Job Controller making API calls to the associated `self._server_thread`
        * We don't immediately start the workers, but wait in WorkerState.INIT state
          until we get a /start call from the controller, which updates the rdzv info
          before updating the AgentState
        * We don't shut down the agent on worker success, but wait for either an explicit
          /shutdown call or the controller to remove the pod that the agent is running inside
    """

    def __init__(
        self,
        spec: WorkerSpec,
        logs_specs: LogsSpecs,
        pre_post_train_config: PrePostTrainConfig,
        shutdown_config: ShutdownConfig,
        version: str,
        start_method="spawn",
        exit_barrier_timeout: float = 300,
        log_line_prefix_template: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            spec,
            logs_specs,
            pre_post_train_config,
            shutdown_config,
            version,
            start_method,
            exit_barrier_timeout,
            log_line_prefix_template,
            **kwargs,
        )
        # Start AgentState at READY
        self.set_agent_state(AgentState.READY)

    def __repr__(self):
        return f"PLRHyperPodElasticAgent({self._worker_group.spec!r})"

    def _stop_workers(self,
                      worker_group: WorkerGroup,
                      is_restart: bool = False) -> None:
        logger.info("Stopping workers...")
        # Get graceful shutdown parameters from agent instance
        is_graceful, timeout = self.get_graceful_shutdown_params()
        # Use SIGUSR1 if graceful shutdown is requested, otherwise use config default
        death_sig = signal.SIGUSR1 if is_graceful else self._shutdown_config.shutdown_signal
        # Pass timeout directly - no side effects
        self._shutdown(death_sig=death_sig, is_restart=is_restart, timeout=timeout)
        self.stop_log_monitoring(clear_log_monitoring_configuration=True)
        worker_group.state = WorkerState.INIT
        self.set_agent_state(AgentState.READY)
        # Reset the generator
        self._training_stages_gen = self._training_stages_generator()

    def get_agent_state_valid_transitions(self):
        return PLR_VALID_TRANSITIONS

    def set_agent_state_running(self):
        self.set_agent_state(AgentState.RUNNING, reason="Running")

    def send_rank_info(self, rank: int):
        pass

    def handle_spare_update(self, spare: bool, fault_count: int):
        pass

    def _invoke_run(self, role: str = DEFAULT_ROLE) -> RunResult:
        """
        There are a few changes from LocalElasticAgent to PLRHyperPodElasticAgent:
        * The agent state transitions now depend both on the worker state
          and the Job Controller making API calls to the associated `self._server_thread`
        * We don't immediately start the workers, but wait in WorkerState.INIT state
          until we get a /start call from the controller, which updates the rdzv info
          before updating the AgentState
        * We don't shut down the agent on worker success, but wait for either an explicit
          /shutdown call or the controller to remove the pod that the agent is running inside
        """
        spec = self._worker_group.spec
        role = spec.role
        monitor_interval = spec.monitor_interval

        while self._agent_state != AgentState.SHUTDOWN:
            time.sleep(monitor_interval)
            self._run_result = self._monitor_workers(self._worker_group)
            state = self._run_result.state
            self._worker_group.state = state

            put_metric(f"workers.{role}.{state.name.lower()}", 1)
            # TODO(mohaan): Encapsulate this into a FSM for better readability
            if state == WorkerState.INIT:
                logger.debug(f"[{role}] worker group ready to start.")
                if self._agent_state == AgentState.RUNNING:
                    logger.info(
                        f"[{role}] Agent starting workers for entrypoint: {spec.get_entrypoint_name()}."
                    )
                    next(self._training_stages_gen)
                    self.start_log_monitoring()
                elif self._agent_state == AgentState.STOPPING:
                    self._stop_workers(self._worker_group)
            elif state == WorkerState.SUCCEEDED:
                if self._agent_state == AgentState.RUNNING and self.can_start:
                    try:
                        next(self._training_stages_gen)
                        self.start_log_monitoring()
                    except StopIteration:
                        logger.info(
                            f"[{role}] worker group successfully finished.")
                        self.set_agent_state(AgentState.COMPLETED)
                        self.stop_log_monitoring(clear_log_monitoring_configuration=True)
                elif self._agent_state == AgentState.STOPPING:
                    self._stop_workers(self._worker_group)
                elif self._log_agent.is_running():
                    self.stop_log_monitoring(clear_log_monitoring_configuration=False)
            elif state in {WorkerState.UNHEALTHY, WorkerState.FAILED}:
                self._worker_group.state = WorkerState.FAILED
                if self._agent_state == AgentState.RUNNING:
                    logger.error(
                        f"[{role}] worker group changed to {state} state.")
                    self.set_agent_state_fault()
                elif self._agent_state == AgentState.STOPPING:
                    self._stop_workers(self._worker_group)
            elif state == WorkerState.HEALTHY:
                # No need to handle membership changes
                logger.debug(f"[{role}] worker group running.")
                if self._agent_state == AgentState.STOPPING:
                    self._stop_workers(self._worker_group)
            else:
                logger.error(
                    f"[{role}] Worker group in unrecoverable {state.name} state"
                )
        logger.info(f"[{role}] Shutting down agent...")
        return self._run_result
