import io
import os
import signal
import tempfile
import threading

from ..config import PrePostTrainConfig, ShutdownConfig
from ..ipc import CheckpointDiscoverySocketServer
from ..ipc.common import RestartMode
from ..logagent.log_agent import LogAgent, LogState
from ..logging import get_logger
from ..pcontext import start_processes
from ..rendezvous import HyperPodRendezvousBackend
from ..server.util import AgentInfo, AgentState, AGENT_STATE_EXPLANATIONS
from abc import abstractmethod
from datetime import datetime, timezone
from string import Template
from torch.distributed.elastic.agent.server.api import (
    RunResult,
    Worker,
    WorkerGroup,
    WorkerSpec,
    WorkerState,
    DEFAULT_ROLE,
)
from torch.distributed.elastic.agent.server.local_elastic_agent import LocalElasticAgent
from torch.distributed.elastic.metrics.api import prof
from torch.distributed.elastic.multiprocessing import LogsSpecs
from torch.distributed.elastic.utils import macros
from typing import Any, Optional

logger = get_logger(__name__)
agent_state_lock = threading.Lock()


class HyperPodElasticAgent(LocalElasticAgent):

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
            start_method,
            exit_barrier_timeout,
            log_line_prefix_template,
        )
        self._pre_post_train_config = pre_post_train_config
        self._shutdown_config = shutdown_config
        self._run_result = RunResult(state=self._worker_group.state)
        self._training_stages_gen = self._training_stages_generator()
        self._log_monitoring_configuration: Optional[list[dict[str, Any]]] = None
        self._log_agent = LogAgent(spec.local_world_size)
        # Setup worker groups and logging dirs
        self._pre_train_wg, self._train_wg, self._post_train_wg = None, self._worker_group, None
        self.train_log_dir, self.pre_train_log_dir, self.post_train_log_dir = os.devnull, os.devnull, os.devnull
        if self._logs_specs.root_log_dir != os.devnull:
            self.train_log_dir = tempfile.mkdtemp(
                prefix=f"{spec.rdzv_handler.get_run_id()}_",
                dir=self._logs_specs.root_log_dir,
            )
        if isinstance(self._pre_post_train_config.pre_train_script, str):
            if self._logs_specs.root_log_dir != os.devnull:
                self.pre_train_log_dir = tempfile.mkdtemp(
                    prefix=f"pre_train_{spec.rdzv_handler.get_run_id()}_",
                    dir=self._logs_specs.root_log_dir,
                )
            pre_train_spec = WorkerSpec(
                role=spec.role,
                local_world_size=1,
                entrypoint=self._pre_post_train_config.pre_train_script,
                args=tuple([self._pre_post_train_config.pre_train_args]),
                rdzv_handler=spec.rdzv_handler,
                monitor_interval=spec.monitor_interval,
                master_addr=spec.master_addr,
                master_port=spec.master_port,
                local_addr=spec.local_addr,
            )
            self._pre_train_wg = WorkerGroup(pre_train_spec)
        if isinstance(self._pre_post_train_config.post_train_script, str):
            if self._logs_specs.root_log_dir != os.devnull:
                self.post_train_log_dir = tempfile.mkdtemp(
                    prefix=f"post_train_{spec.rdzv_handler.get_run_id()}_",
                    dir=self._logs_specs.root_log_dir,
                )
            post_train_spec = WorkerSpec(
                role=spec.role,
                local_world_size=1,
                entrypoint=self._pre_post_train_config.post_train_script,
                args=tuple([self._pre_post_train_config.post_train_args]),
                rdzv_handler=spec.rdzv_handler,
                monitor_interval=spec.monitor_interval,
                master_addr=spec.master_addr,
                master_port=spec.master_port,
                local_addr=spec.local_addr,
            )
            self._post_train_wg = WorkerGroup(post_train_spec)
        self._ckpt_server = CheckpointDiscoverySocketServer()
        self._socket_server_path: str = self._ckpt_server.socket_server.server_address
        self._assigned_rank = -1
        self.can_start = False
        self.spare = True
        self.priority = False
        self.version = version
        # NOTE: All state must be initialized before the Agent is updated to READY state
        self._agent_state: AgentState = AgentState.INIT
        self._agent_reason: Optional[str] = None
        self._agent_message: Optional[str] = None
        self._agent_transitions: dict[AgentState, str] = {
            self._agent_state: datetime.now(timezone.utc).isoformat()
        }

    def __repr__(self):
        return f"HyperPodElasticAgent({self._worker_group.spec!r})"

    def _stop_workers(self,
                      worker_group: WorkerGroup,
                      is_restart: bool = False) -> None:
        raise NotImplementedError("Subclass must implement _stop_workers")

    def _training_stages_generator(self):
        if self._pre_train_wg:
            setattr(self._logs_specs, "_run_log_dir", self.pre_train_log_dir)
            self._worker_group = self._pre_train_wg
            super()._initialize_workers(self._worker_group)
        else:
            logger.debug(
                f"Skipping pre_train as script is either not specified "
                f"or not a string type: {self._pre_post_train_config.pre_train_script}"
            )
            self._worker_group.state = WorkerState.SUCCEEDED
        yield

        setattr(self._logs_specs, "_run_log_dir", self.train_log_dir)
        self._worker_group = self._train_wg
        super()._initialize_workers(self._worker_group)
        yield

        if self._post_train_wg:
            setattr(self._logs_specs, "_run_log_dir", self.post_train_log_dir)
            self._worker_group = self._post_train_wg
            super()._initialize_workers(self._worker_group)
        else:
            logger.debug(
                f"Skipping post_train as script is either not specified "
                f"or not a string: {self._pre_post_train_config.post_train_script}"
            )
            self._worker_group.state = WorkerState.SUCCEEDED
        yield

    @prof
    def _start_workers(self, worker_group: WorkerGroup) -> dict[int, Any]:
        """
        Overriding just to add a single new env variable
        """
        logger.info(
            f"Starting workers with worker spec {worker_group.spec=}...")
        assert not worker_group.spec.rdzv_handler.use_agent_store, "HyperPod Agent store cannot be re-used for training"
        spec = worker_group.spec
        store = worker_group.store
        assert store is not None
        restart_count = spec.max_restarts - self._remaining_restarts

        use_agent_store: bool = spec.rdzv_handler.use_agent_store

        args: dict[int, tuple] = {}
        envs: dict[int, dict[str, str]] = {}
        log_line_prefixes: Optional[dict[
            int, str]] = {} if self._log_line_prefix_template else None
        for worker in worker_group.workers:
            local_rank = worker.local_rank
            worker_env = {
                "LOCAL_RANK":
                str(local_rank),
                "RANK":
                str(worker.global_rank),
                "GROUP_RANK":
                str(worker_group.group_rank),
                "ROLE_RANK":
                str(worker.role_rank),
                "ROLE_NAME":
                spec.role,
                "LOCAL_WORLD_SIZE":
                str(spec.local_world_size),
                "WORLD_SIZE":
                str(worker.world_size),
                "GROUP_WORLD_SIZE":
                str(worker_group.group_world_size),
                "ROLE_WORLD_SIZE":
                str(worker.role_world_size),
                "MASTER_ADDR":
                worker_group.master_addr,
                "MASTER_PORT":
                str(worker_group.master_port),
                "JOB_RESTART_COUNT":
                str(restart_count),
                "TORCHELASTIC_RESTART_COUNT":
                str(restart_count),
                "TORCHELASTIC_MAX_RESTARTS":
                str(spec.max_restarts),
                "TORCHELASTIC_RUN_ID":
                spec.rdzv_handler.get_run_id(),
                "TORCHELASTIC_USE_AGENT_STORE":
                str(use_agent_store),
                "TORCH_NCCL_ASYNC_ERROR_HANDLING":
                os.getenv("TORCH_NCCL_ASYNC_ERROR_HANDLING", str(1)),
                "HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH":
                self._socket_server_path,
                "HYPERPOD_SIGNAL_COORDINATION":
                os.getenv("HYPERPOD_SIGNAL_COORDINATION", "disabled"),
            }
            if "OMP_NUM_THREADS" in os.environ:
                worker_env["OMP_NUM_THREADS"] = os.environ["OMP_NUM_THREADS"]

            # export TORCHELASTIC_LOG_LINE_PREFIX_TEMPLATE="[rank\$rank-group_rank\$group_rank-attempt\$restart_count]:"
            if self._log_line_prefix_template:
                log_line_prefix = Template(
                    self._log_line_prefix_template).safe_substitute(
                        role_name=spec.role,
                        rank=worker.global_rank,
                        local_rank=local_rank,
                        group_rank=worker_group.group_rank,
                        restart_count=restart_count,
                    )
                log_line_prefixes[local_rank] = log_line_prefix

            envs[local_rank] = worker_env
            worker_args = list(spec.args)
            worker_args = macros.substitute(worker_args, str(local_rank))
            args[local_rank] = tuple(worker_args)

        self._setup_local_watchdog(envs=envs)
        self._setup_healthcheck()

        assert spec.entrypoint is not None
        assert self._logs_specs is not None
        self._pcontext = start_processes(
            name=spec.role,
            entrypoint=spec.entrypoint,
            args=args,
            envs=envs,
            logs_specs=self._logs_specs,
            death_sig=self._shutdown_config.shutdown_signal,
            signal_timeout=self._shutdown_config.shutdown_timeout,
            log_line_prefixes=log_line_prefixes,
            start_method=self._start_method,
        )

        return self._pcontext.pids()

    def _shutdown(self,
                  death_sig: signal.Signals = signal.SIGTERM,
                  is_restart: bool = False,
                  timeout: Optional[int] = None) -> None:
        logger.debug(f"_shutdown called with death_sig={death_sig.name}, is_restart={is_restart}, timeout={timeout}")
        
        if self._worker_watchdog is not None:
            logger.debug("Stopping worker watchdog")
            self._worker_watchdog.stop()
            self._worker_watchdog = None
        if self._health_check_server is not None:
            logger.debug("Stopping health check server")
            self._health_check_server.stop()
            self._health_check_server = None
        if self._pcontext:
            # Explicit parameter precedence - much cleaner than side effects
            shutdown_timeout = timeout if timeout is not None else self._shutdown_config.shutdown_timeout
            logger.debug(f"Closing pcontext with death_sig={death_sig.name}, timeout={shutdown_timeout}")
            
            self._pcontext.close(
                death_sig=death_sig,
                timeout=shutdown_timeout,
            )
            logger.debug("pcontext.close() completed")
            self._pcontext = None
        else:
            logger.debug("No pcontext to shutdown")
            
        if not is_restart and self._rdzv_handler:
            logger.debug("Shutting down rendezvous handler")
            self._rdzv_handler.shutdown()
        
        logger.info(f"Shutdown completed for signal {death_sig.name}")

    def _monitor_workers(self, worker_group: WorkerGroup) -> RunResult:
        # self._pcontext is None if
        # 1. Workers have not been started yet, or
        # 2. Workers were stopped
        if self._pcontext is None:
            return RunResult(state=worker_group.state)
        run_result = super()._monitor_workers(worker_group)
        # Additionally, check LogAgent state
        # (Note: Setting the workerState UNHEALTHY for the monitor loop to pick up this change)
        for log_eval_result in self._log_agent.log_eval_results:
            if log_eval_result.log_state in {
                    LogState.SLOW, LogState.HANGING, LogState.FAULTED
            }:
                run_result.state = WorkerState.UNHEALTHY
                break
        return run_result

    def _get_worker_state(self, worker: Worker, result: RunResult) -> str:
        failure = result.failures.get(worker.global_rank)
        if not failure and result.state in {
                WorkerState.UNHEALTHY, WorkerState.FAILED
        }:
            # The worker got terminated by the torchelastic agent via SIGTERM signal
            return "TERMINATED"
        elif failure or worker.global_rank in result.return_values:
            return result.state.value
        elif self._agent_state == AgentState.SHUTDOWN:
            # For a graceful shutdown of the agent
            return "SHUTDOWN"
        else:
            raise ValueError(f"Unknown worker: {worker.global_rank}")

    def get_agent_state_valid_transitions(self):
        raise NotImplementedError("Subclass must implement get_agent_state_valid_transitions()")

    def set_agent_state(self,
                        agent_state: AgentState,
                        reason: Optional[str] = None,
                        message: Optional[str] = None) -> None:
        """
        Can be called during `_invoke_run` by the main thread OR a request handler in the server API thread
        """
        with agent_state_lock:
            if agent_state in self.get_agent_state_valid_transitions()[self._agent_state]:
                logger.info(
                    f"Transitioned from {self._agent_state} to {agent_state}")
                logger.info(AGENT_STATE_EXPLANATIONS[agent_state])
                self._agent_state = agent_state
                self._agent_reason = reason
                self._agent_message = message
                self._agent_transitions[agent_state] = datetime.now(
                    timezone.utc).isoformat()
            else:
                logger.error(
                    f"Invalid agent state transition from {self._agent_state} to {agent_state}."
                )

    def get_agent_state_info(self) -> AgentInfo:
        assert isinstance(self._rdzv_handler, HyperPodRendezvousBackend)
        return AgentInfo(
            state=self._agent_state,
            reason=self._agent_reason,
            message=self._agent_message,
            transitions=self._agent_transitions,
            ip_version=self._rdzv_handler.ip_version,
        )

    def set_assigned_rank(self, rank: int):
        self._assigned_rank = rank

    def get_assigned_rank(self) -> int:
        return self._assigned_rank

    def send_rank_info(self, rank: int):
        raise NotImplementedError("Subclass must implement send_rank_info()")

    def handle_spare_update(self, spare: bool, fault_count: int):
        raise NotImplementedError(
            "Subclass must implement handle_spare_update()")

    def set_restart_mode(self, restart_mode: str):
        pass

    def get_restart_mode(self) -> str:
        """
        Returns the agent's restart mode capability.
        Base class returns process_level_restart as default.
        """
        return RestartMode.PROCESS_LEVEL_RESTART.value

    def set_graceful_shutdown_params(self, is_graceful: Optional[bool], timeout: Optional[int]) -> None:
        """Set graceful shutdown parameters for stop operations"""
        self._is_graceful = is_graceful
        self._stop_timeout = timeout

    def get_graceful_shutdown_params(self) -> tuple[Optional[bool], Optional[int]]:
        """Get graceful shutdown parameters, returns (is_graceful, timeout)"""
        return getattr(self, '_is_graceful', None), getattr(self, '_stop_timeout', None)

    def set_agent_state_running(self):
        pass

    def set_agent_state_fault(self):
        run_result = self.get_run_result()
        log_state, rule_name_log_line = self.get_log_agent_state()
        reason, message = None, None

        if log_state in {LogState.HANGING, LogState.SLOW, LogState.FAULTED}:
            if log_state == LogState.HANGING:
                reason = f"LogHang_{list(rule_name_log_line.keys())[0]}"
                message = f"The job is hanging (not receiving required logs) on the following log monitoring rules and corresponding last matched log lines: {rule_name_log_line}"
            elif log_state == LogState.SLOW:
                reason = f"LogSlow_{list(rule_name_log_line.keys())[0]}"
                message = f"The job is slowed (logs outside of acceptable thresholds) on the following log monitoring rules and corresponding log lines: {rule_name_log_line}"
            elif log_state == LogState.FAULTED:
                reason = f"LogFault_{list(rule_name_log_line.keys())[0]}"
                message = f"The job detected a fault indicating log message for the following log monitoring rules and corresponding log lines: {rule_name_log_line}"
            self.set_agent_state(AgentState.FAULTED,
                                 reason=reason,
                                 message=message)
            return

        if run_result.state in {WorkerState.UNHEALTHY, WorkerState.FAILED}:
            message = io.StringIO()
            if run_result.state == WorkerState.UNHEALTHY:
                reason = f"WorkerUnhealthy"
                message.write(
                    "A training worker process entered into an unhealthy state:\n"
                )
            elif run_result.state == WorkerState.FAILED:
                reason = f"WorkerCrash"
                message.write(
                    "A training worker process has crashed:\n")
            for failure in run_result.failures.values():
                message.write(
                    f"    Local Rank {failure.local_rank} exited with code {failure.exitcode} due to: {failure.message}\n"
                )
            self.set_agent_state(AgentState.FAULTED,
                                 reason=reason,
                                 message=message.getvalue())
            return

        reason = "WorkerFault"
        message = "An unknown fault occurred resulting in the training worker processes becoming unhealthy"
        self.set_agent_state(AgentState.FAULTED,
                             reason=reason,
                             message=message)

    def update_rendezvous_info(
        self,
        rank: int,
        nnodes: int,
        fault_count: int,
        master_addr: str,
        master_port: int,
        ip_version: str,
        rank_ips: list[dict[str, Any]],
        aggregate_worker_data: Optional[dict[str, Any]] = None,
    ):
        """
        Called by the server API thread to do a rendezvous and update the ranking info
        """
        spec = self._worker_group.spec
        if isinstance(spec.rdzv_handler, HyperPodRendezvousBackend):
            spec.rdzv_handler.set_rdzv_info(rank, nnodes, master_addr,
                                            master_port, ip_version, rank_ips)
        else:
            raise RuntimeError(
                f"Unexpected rendezvous backend: {type(spec.rdzv_handler)}")
        # The API assigns `restart_count = spec.max_restarts - self._remaining_restarts`
        # updating `self._remaining_restarts` to avoid overriding torch.distributed.elastic.server.api._rendezvous
        # Currently `_remaining_restarts` is not being used anywhere else in torchelastic
        # except to calculate the `restart_count`
        self._remaining_restarts = spec.max_restarts - fault_count
        logger.update_run_info(rank, fault_count)

    def update_progress(self, progress: dict):
        self._ckpt_server.update_progress(progress)

    def get_job_ip_tables(self) -> list:
        assert isinstance(self._worker_group.spec.rdzv_handler,
                          HyperPodRendezvousBackend)
        rdzv_handler = self._worker_group.spec.rdzv_handler
        return rdzv_handler.get_job_ip_table()

    def get_run_result(self) -> RunResult:
        return self._run_result

    def set_log_monitoring_configuration(self, config: Optional[list[dict[str, Any]]]):
        self._log_monitoring_configuration = config

    def start_log_monitoring(self):
        if self._worker_group.state not in [WorkerState.INIT, WorkerState.HEALTHY]:
            logger.debug(f"Skip starting log monitoring since worker state is {self._worker_group.state}")
            return

        restart_count = self._worker_group.spec.max_restarts - self._remaining_restarts
        # Override restart_count from worker environment if they have already started running
        if getattr(self._pcontext, "envs", None) and 0 in self._pcontext.envs and "TORCHELASTIC_RESTART_COUNT" in self._pcontext.envs[0]:
            restart_count = int(self._pcontext.envs[0]["TORCHELASTIC_RESTART_COUNT"])
        attempt_dir = LogAgent.compute_attempt_dir(
            run_log_dir=getattr(self._logs_specs, "_run_log_dir", ""),
            attempt_num=restart_count)
        # Start log monitoring only for local rank 0 by default
        self._log_agent.start(attempt_dir, {0}, self._log_monitoring_configuration)

    def stop_log_monitoring(self, clear_log_monitoring_configuration=False):
        self._log_agent.stop(clear_log_monitoring_configuration)

    def get_agent_progress(self) -> Optional[dict[str, dict]]:
        max_valid_checkpoint = self._ckpt_server.tracker.max_valid_checkpoint
        if max_valid_checkpoint is None:
            return None
        response: dict[str, dict] = {
            max_valid_checkpoint.prefix: {
                "progressData": max_valid_checkpoint.path,
                "progressCount": max_valid_checkpoint.step
            }
        }
        return response

    def get_log_agent_state(self) -> tuple[LogState, Optional[dict[str, Optional[str]]]]:
        """
        Returns a common LogState and offending rule name and last matched log line
        based on the LogAgent state across all the local_ranks, similar to WorkerState.
        This is used for setting the `reason` and `message` field of the StatusResponse
        """
        for log_eval_result in self._log_agent.log_eval_results:
            if log_eval_result.log_state == LogState.FAULTED:
                logger.info(
                    f"LogState.FAULTED for rules={log_eval_result.rule_name_log_line}")
                return LogState.FAULTED, log_eval_result.rule_name_log_line
            if log_eval_result.log_state == LogState.HANGING:
                logger.info(
                    f"LogState.HANGING for rules={log_eval_result.rule_name_log_line}")
                return LogState.HANGING, log_eval_result.rule_name_log_line
            if log_eval_result.log_state == LogState.SLOW:
                logger.info(
                    f"LogState.SLOW for rules={log_eval_result.rule_name_log_line}")
                return LogState.SLOW, log_eval_result.rule_name_log_line
        if LogState.WAITING in self._log_agent.log_state:
            return LogState.WAITING, None
        return LogState.HEALTHY, None

    @abstractmethod
    def _invoke_run(self, role: str = DEFAULT_ROLE) -> RunResult:
        raise NotImplementedError("Subclass must implement _invoke_run()")
