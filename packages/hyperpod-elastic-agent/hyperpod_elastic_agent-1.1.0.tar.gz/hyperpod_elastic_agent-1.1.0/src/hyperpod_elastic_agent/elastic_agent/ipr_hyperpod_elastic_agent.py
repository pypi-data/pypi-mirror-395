import threading
import time

from .hyperpod_elastic_agent import HyperPodElasticAgent
from ..config import PrePostTrainConfig, ShutdownConfig
from ..ipc import (
    HyperPodPLRException,
    HyperPodIPCException,
    InProcessRestartSocketServer,
    RestartMode,
)
from ..logging import get_logger
from ..rendezvous import HyperPodRendezvousBackend
from ..server import AgentInfo, AgentState, IPR_VALID_TRANSITIONS
from datetime import datetime, timezone
from torch.distributed.elastic.agent.server.api import (
    RunResult,
    WorkerGroup,
    WorkerSpec,
    WorkerState,
    DEFAULT_ROLE,
)
from torch.distributed.elastic.metrics import put_metric
from torch.distributed.elastic.multiprocessing import LogsSpecs
from typing import Any, Callable, Optional

logger = get_logger(__name__)
agent_state_lock = threading.Lock()


class IPRHyperPodElasticAgent(HyperPodElasticAgent):
    """
    A specialized HyperPodElasticAgent that supports in-process restart capabilities.

    This agent manages worker processes with the ability to pause and resume training
    without killing the processes, enabling faster recovery and state preservation
    during restarts. It handles different training stages (pre-training, training,
    post-training) and manages worker state transitions.

    Key features:
    - Supports immediate worker startup when in INIT state (Agent start up)
    - Manages barrier synchronization for coordinated training
    - Implements pause/resume functionality for worker processes
    - Handles graceful stopping based on training stage

    There are a few changes from PLRHyperPodElasticAgent to IPRHyperPodElasticAgent:
        * We immediately start the workers as soon as Agent starts up
        * Only set AgentState to READY after pre-training is finished and the training worker
          group is started (and waiting at barrier)
        * When agent receives a /start signal, we notify the processes to start the RCB
          (Requires framework APIs)
        * When job agent is in AgentState.STOPPING state we do not kill processes on healthy nodes
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

        # Internal state variable marking whether or not the training process has passed the barrier and started RCB execution
        self._ipc_server = InProcessRestartSocketServer(
            local_world_size=spec.local_world_size)
        self._socket_server_path = self._ipc_server.socket_server.server_address
        self._process_level_start = False
        self.aggregate_worker_data: dict[str, Any] = {}
        self.inprocess_timeout = kwargs.get("inprocess_timeout", None)

    def __repr__(self):
        return f"IPRHyperPodElasticAgent({self._worker_group.spec!r})"

    def _stop_workers(self,
                      worker_group: WorkerGroup,
                      is_restart: bool = False) -> None:
        # Override _stop_workers method so AgentState goes back to AgentState.INIT
        # TODO: look into refactoring to avoid duplicate code
        logger.info("Stopping workers...")
        self._ipc_server.clear_clients()
        self._shutdown(
            death_sig=self._shutdown_config.shutdown_signal,
            is_restart=is_restart,
        )
        self.stop_log_monitoring(clear_log_monitoring_configuration=True)
        worker_group.state = WorkerState.INIT
        self.set_agent_state(AgentState.INIT)
        self.priority = False
        # Reset the generator
        self._training_stages_gen = self._training_stages_generator()
        self._ipc_server.reset_worker_state(clear_data=True)
        assert isinstance(self._rdzv_handler, HyperPodRendezvousBackend)
        self._rdzv_handler.ip_version = None

    def get_agent_state_info(self) -> AgentInfo:
        agent_info = super().get_agent_state_info()
        agent_info.ipc_worker_group = self._ipc_server.ipc_wg
        return agent_info

    def get_agent_state_valid_transitions(self):
        return IPR_VALID_TRANSITIONS

    def set_agent_state_running(self):
        self.set_agent_state(AgentState.RUNNING, reason="RunningStarted")

    def set_agent_state_fault(self):
        if self._ipc_server.is_failed:
            failed_ranks = self._ipc_server.ipc_wg.get_failed_ranks()

            # Try using reason and message from IPC
            for failed_rank in failed_ranks:
                if failed_rank.reason is not None and failed_rank.reason != '':
                    reason = failed_rank.reason
                    message = failed_rank.message
                    self.set_agent_state(
                        AgentState.FAULTED,
                        reason=reason,
                        message=message,
                    )
                    return

            # Default ipc failure reason and message
            str_failed_ranks = ", ".join(
                str(failed.rank) for failed in failed_ranks)
            reason = "WorkerReportedFault"
            message = f"The processes reported a failure on ranks {str_failed_ranks}"
            self.set_agent_state(
                AgentState.FAULTED,
                reason=reason,
                message=message,
            )
            return

        # Fallback to standard PLR fault cases
        return super().set_agent_state_fault()

    def _pause_workers(self, worker_group: WorkerGroup):
        """
        Helper method used to pause worker processes but not kill them
        """
        logger.info("Send stop signal to framework")
        restart_count = worker_group.spec.max_restarts - self._remaining_restarts
        self.priority = True
        self._ipc_server.send_fault(restart_count)
        self.stop_log_monitoring(clear_log_monitoring_configuration=True)
        self._ipc_server.get_ranks_at_barrier(timeout=self.inprocess_timeout)
        # Reset AgentState to READY
        self.set_agent_state(AgentState.READY)

    def _pause_or_stop_workers(self, worker_group: WorkerGroup):
        """
        Helper method used to pause or stop worker processes depending on the training stage
        If at training stage, pause. If at post training, stop. If at pretraining, no op
        """
        # TODO: check expected behavior for pre / post training
        if self._post_train_wg and worker_group is self._post_train_wg:
            self._stop_workers(worker_group)
        elif worker_group is self._train_wg:
            self._pause_workers(worker_group)

    def update_rendezvous_info(
        self,
        rank: int,
        nnodes: int,
        fault_count: int,
        master_addr: str,
        master_port: int,
        ip_version: str,
        rank_ips: list[dict[str, str | int]],
        aggregate_worker_data: Optional[dict[str, Any]] = None,
    ):
        self.aggregate_worker_data = {
            "rank_ips": rank_ips,
            "aggregate_worker_data": aggregate_worker_data,
        }
        super().update_rendezvous_info(
            rank,
            nnodes,
            fault_count,
            master_addr,
            master_port,
            ip_version,
            rank_ips,
            aggregate_worker_data,
        )

    def get_rank_info(self) -> dict[int, dict[str, str]]:
        """
        Calls _rendezvous to update the worker group and returns a dict with
        the latest ranking info for each local rank
        """
        if any(worker.id is None for worker in self._worker_group.workers):
            raise HyperPodIPCException(
                "Workers not initialized yet, cannot apply updates from operator."
            )
        # Keep track of the current pids since rendezvous will reset them
        worker_pids = [(worker.local_rank, worker.id)
                       for worker in self._worker_group.workers]
        # Rendezvous to update worker group with latest info
        self._rendezvous(self._worker_group)
        # Assign the worker pids
        for local_rank, w_id in worker_pids:
            worker = self._worker_group.workers[local_rank]
            worker.id = w_id

        spec = self._worker_group.spec
        restart_count = spec.max_restarts - self._remaining_restarts
        worker_envs: dict[int, dict[str, str]] = {}
        for worker in self._worker_group.workers:
            worker_envs[worker.local_rank] = {
                "RANK": str(worker.global_rank),
                "GROUP_RANK": str(self._worker_group.group_rank),
                "ROLE_RANK": str(worker.role_rank),
                "WORLD_SIZE": str(worker.world_size),
                "GROUP_WORLD_SIZE": str(self._worker_group.group_world_size),
                "ROLE_WORLD_SIZE": str(worker.role_world_size),
                "MASTER_ADDR": str(self._worker_group.master_addr),
                "MASTER_PORT": str(self._worker_group.master_port),
                "JOB_RESTART_COUNT": str(restart_count),
                "TORCHELASTIC_RESTART_COUNT": str(restart_count),
                "SPARE": str(self.spare),
            }
        return worker_envs

    def send_rank_info(self, rank: int):
        """
        Called by the server API thread. Gets the latest ranking info and sends it to each local rank via IPC
        """
        try:
            worker_envs = self.get_rank_info()
            self._ipc_server.send_rank_info(worker_envs,
                                            self.aggregate_worker_data)
        except HyperPodIPCException as ex:
            logger.debug(f"Failed to send rank info to clients: {ex}")
            assert isinstance(self._rdzv_handler, HyperPodRendezvousBackend)
            # Update the in-memory copy of ip_version to None so that /update is called again
            # which will over-write the inconsistent ip_tables file with the correct value
            self._rdzv_handler.ip_version = None
        else:
            self.set_assigned_rank(rank)

    def handle_spare_update(self, spare: bool, fault_count: int):
        """
        Called by the server API thread. If the transition is from "non-spare -> spare"
        it will set the `_process_level_start` flag so that next iteration of `_invoke_run` does a PLR.
        The processes could be pre-barrier or at-barrier when they are re-started.
        """
        if not spare and fault_count == 0 and self._agent_state == AgentState.INIT:
            self.priority = True
        if self.spare == spare:
            return
        if not self.spare:
            logger.info(
                f"Transitioning from spare={self.spare} to spare={spare}, will trigger a process level restart"
            )
            self._process_level_start = True
        self.spare = spare

    def set_restart_mode(self, restart_mode: str):
        """
        Called by the server API thread to enable a process_level_restart
        """
        logger.debug(f"Requested {restart_mode}")
        restart_mode_enum = RestartMode.IN_PROCESS_RESTART
        try:
            restart_mode_enum = RestartMode[restart_mode.upper()]
        except KeyError:
            logger.error(f"Unexpected {restart_mode=}, will use default")
        if restart_mode_enum == RestartMode.PROCESS_LEVEL_RESTART:
            logger.info(
                f"{restart_mode_enum} requested from operator, will trigger a process level restart"
            )
            self._process_level_start = True

    def get_restart_mode(self) -> str:
        """
        Returns the agent's restart mode capability.
        IPR agent returns in_process_restart.
        """
        return RestartMode.IN_PROCESS_RESTART.value

    def _invoke_run(self, role: str = DEFAULT_ROLE) -> RunResult:
        """
        This loop is invoked in the main thread and manages the Agent state machine.
        There are a few changes from PLRHyperPodElasticAgent to IPRHyperPodElasticAgent:
        * We immediately start the workers as soon as Agent starts up
        * Only set AgentState to READY after pre-training is finished and the training worker
          group is started (and waiting at barrier)
        * When agent receives a /start signal, we notify the processes to start the RCB
          (Requires framework APIs)
        * When job agent is in AgentState.STOPPING state we do not kill processes on healthy nodes
        """
        spec = self._worker_group.spec
        role = spec.role
        monitor_interval = spec.monitor_interval
        self._state_handler: dict[
            WorkerState,
            Callable[[str, WorkerSpec], None],
        ] = {
            WorkerState.INIT: self._handle_init_state,
            WorkerState.HEALTHY: self._handle_healthy_state,
            WorkerState.UNHEALTHY: self._handle_failed_state,
            WorkerState.STOPPED: self._handle_noop,
            WorkerState.SUCCEEDED: self._handle_succeeded_state,
            WorkerState.FAILED: self._handle_failed_state,
        }

        while self._agent_state != AgentState.SHUTDOWN:
            time.sleep(monitor_interval)
            self._run_result = self._monitor_workers(self._worker_group)
            state = self._run_result.state
            self._worker_group.state = state
            if self._process_level_start:
                logger.info(f"[{role}] Triggering a process level restart...")
                self._stop_workers(self._worker_group)
                self._process_level_start = False

            put_metric(
                f"workers.{role}.{self._worker_group.state.name.lower()}", 1)
            try:
                self._state_handler.get(
                    self._worker_group.state,
                    self._handle_noop,
                )(role, spec)
            except HyperPodPLRException:
                # Do PLR
                self._stop_workers(self._worker_group)
        logger.info(f"[{role}] Shutting down agent...")
        return self._run_result

    def _handle_init_state(self, role: str, spec: WorkerSpec):
        logger.debug(f"[{role}] worker group ready to start.")
        logger.info(
            f"[{role}] Agent starting workers for entrypoint: {spec.get_entrypoint_name()}."
        )
        # Execute pretraining step
        next(self._training_stages_gen)

    def _handle_succeeded_state(self, role: str, spec: WorkerSpec):
        if self._agent_state == AgentState.INIT:
            # AgentState is not READY so start training stage
            next(self._training_stages_gen)
            self.stop_log_monitoring(clear_log_monitoring_configuration=False)
            self._ipc_server.get_ranks_at_barrier(
                init=True, timeout=self.inprocess_timeout)
            self.set_agent_state(AgentState.READY)
            logger.info(
                f"[{role}] All clients reporting to be at RCB barrier.")
        elif self._agent_state == AgentState.RUNNING:
            try:
                next(self._training_stages_gen)
                self.start_log_monitoring()
            except StopIteration:
                logger.info(f"[{role}] worker group successfully finished.")
                self.set_agent_state(AgentState.COMPLETED)
                self.stop_log_monitoring(clear_log_monitoring_configuration=True)
        elif self._agent_state == AgentState.STOPPING:
            self._pause_or_stop_workers(self._worker_group)

    def _handle_failed_state(self, role: str, spec: WorkerSpec):
        self._worker_group.state = WorkerState.FAILED
        if self._agent_state in {
                AgentState.RUNNING, AgentState.INIT, AgentState.READY
        }:
            logger.error(
                f"[{role}] worker group changed to {self._worker_group.state} state."
            )
            self.set_agent_state_fault()
        elif self._agent_state == AgentState.STOPPING:
            # Need to stop workers since one or more processes are bad on this node
            self._stop_workers(self._worker_group)

    def _handle_healthy_state(self, role: str, spec: WorkerSpec):
        logger.debug(f"[{role}] worker group running.")
        if self._agent_state == AgentState.RUNNING:
            if self._ipc_server.at_barrier() and self.can_start:
                try:
                    worker_envs = self.get_rank_info()
                    logger.info(
                        "Send start signal to framework to kick off RCB")
                    assert None not in self.get_job_ip_tables(
                    ), "Operator hasn't supplied the complete IP table"
                    self._ipc_server.send_start(
                        worker_envs=worker_envs,
                        aggregate_worker_data=self.aggregate_worker_data,
                    )
                    self._agent_reason = "Running"
                    self.priority = False
                    self.start_log_monitoring()
                except HyperPodIPCException:
                    self.set_agent_state_fault()
            elif self._ipc_server.is_failed:
                self._process_level_start = self._ipc_server.trigger_local_plr(
                )
                self.set_agent_state_fault()
        elif self._agent_state == AgentState.INIT:
            # Best effort to start log monitoring as soon as config is sent via the first Update API call from pod manager
            # Pre-train script may have started before the first Update API call arrives
            if self._log_monitoring_configuration and not self._log_agent.is_running():
                self.start_log_monitoring()
        elif self._agent_state == AgentState.STOPPING:
            self._pause_or_stop_workers(self._worker_group)

    def _handle_noop(self, role: str, spec: WorkerSpec):
        pass
