import queue
import time

from abc import ABC
from typing import Any, Callable, Optional
from .common import (
    BaseIPC,
    CheckpointDiscoverySocketMessageType,
    HyperPodPLRException,
    HyperPodIPCException,
    InProcessRestartSocketMessageType,
    RestartMode,
    SocketMessageType,
)
from .socket import HyperPodElasticAgentSocketServer
from .util import IPCWorkerGroup
from ..checkpoint_discovery import CheckpointTracker
from ..logging import get_logger

logger = get_logger(__name__)


class BaseIPCSocketServer(BaseIPC, ABC):
    socket_server = HyperPodElasticAgentSocketServer()

    def __init__(self):
        self.socket_server.start()

    def register_message_callback(
        self,
        message_type: str,
        callback: Callable[[dict], Optional[dict]],
    ):
        self.socket_server.register_message_callback(message_type, callback)

    def register_message_queue(
        self,
        message_type: str,
        message_queue: queue.Queue,
    ) -> None:
        self.socket_server.register_message_queue(message_type, message_queue)

    def drain_message_queue(
        self,
        message_queue: queue.Queue,
    ) -> list[tuple[SocketMessageType, Optional[dict]]]:
        return self.socket_server.drain_message_queue(message_queue)

    @property
    def num_clients(self):
        return len(self.socket_server.client_ranks)

    @property
    def client_ranks(self):
        return self.socket_server.client_ranks


class CheckpointDiscoverySocketServer(BaseIPCSocketServer):
    """
    Provides an API for the agent to be able to communicate checkpoint info to and from the training processes.
    ASSUMPTION: Multiple socket clients per local_rank, e.g. model checkpoints, data checkpoints
    """

    def __init__(self):
        super().__init__()
        logger.info(
            f"Started {self.__class__.__name__} over {self.socket_server.server_address}"
        )
        self.register_message_callback(
            CheckpointDiscoverySocketMessageType.CKPT_INIT,
            self._init_callback,
        )
        self.register_message_callback(
            CheckpointDiscoverySocketMessageType.CKPT_INFO_UPDATE,
            self._update_callback,
        )
        self.register_message_callback(
            CheckpointDiscoverySocketMessageType.CKPT_INFO_GET,
            self._get_latest_callback,
        )
        # TODO: Make it self.tracker as its accessed outside this class
        self.tracker = CheckpointTracker()

    def _init_callback(self, msg: dict) -> None:
        """
        We're operating under the assumption that all local ranks would be reporting the same
        prefix, rank, num_expected_ranks. So we can set these as soon as the first one reports.
        If this changes in the future, this logic would need to be updated.
        """
        prefix = msg.get("prefix")
        checkpoint_types = msg.get("checkpoint_types")
        self.tracker.update_checkpoint_info(
            prefix=prefix,
            checkpoint_types=checkpoint_types,
        )

    def _update_callback(self, msg: dict) -> None:
        step = msg.get("step")
        path = msg.get("path")
        local_rank = msg.get("local_rank")
        checkpoint_type = msg.get("checkpoint_type")
        logger.debug(
            f"Checkpoint update received from {local_rank=} with version {step=}"
        )
        self.tracker.update_checkpoint_data(
            rank=local_rank,
            step=step,
            path=path,
            checkpoint_type=checkpoint_type,
        )

    def _get_latest_callback(self, msg: dict) -> dict:
        """
        Returns the current checkpoint info.
        NOTE: If called before CKPT_INIT it will return None
        """
        logger.debug(
            f"Got request for latest checkpoint from local_rank={msg.get('local_rank')}"
        )
        return {"path": self.tracker.get_latest_checkpoint_path()}

    def update_progress(self, progress: dict):
        self.tracker.progress = progress


class InProcessRestartSocketServer(BaseIPCSocketServer):
    """
    Provides an API for the HyperPodElasticAgent to be able to communicate info
    related to in process restarts to and from the training processes
    """

    def __init__(self, local_world_size):
        super().__init__()
        logger.info(
            f"Started {self.__class__.__name__} over {self.socket_server.server_address}"
        )
        if local_world_size < 1:
            raise HyperPodIPCException(f"Invalid {local_world_size=}")
        self._local_world_size = local_world_size
        self._local_ranks = set(range(local_world_size))
        self.ipc_wg = IPCWorkerGroup(local_world_size)

        self._clients_ready_queue = queue.Queue()
        self.register_message_queue(
            InProcessRestartSocketMessageType.AT_RCB_BARRIER,
            self._clients_ready_queue,
        )
        self.register_message_callback(
            InProcessRestartSocketMessageType.JOB_FAULT,
            self._job_fault_callback,
        )
        self.register_message_callback(
            InProcessRestartSocketMessageType.JOB_DATA,
            self._job_data_callback,
        )
        self.register_message_callback(
            InProcessRestartSocketMessageType.PAST_RCB_BARRIER,
            self._past_rcb_barrier_callback,
        )
        self.register_message_callback(
            InProcessRestartSocketMessageType.RANK_LABELS,
            self._notify_labels_callback,
        )

    def send_start(
        self,
        worker_envs: dict[int, dict[str, str]],
        aggregate_worker_data: dict[str, Any],
    ) -> None:
        """
        Sends a start signal to the training processes along with the updated rank info.
        In case of a restart, fault_data will be set to notify workers about previous runs fault info
        """
        self.reset_worker_state()
        self._send_rank_info_helper(
            worker_envs=worker_envs,
            message_type=InProcessRestartSocketMessageType.JOB_START,
            aggregate_worker_data=aggregate_worker_data,
        )

    def send_rank_info(
        self,
        worker_envs: dict[int, dict[str, str]],
        aggregate_worker_data: dict[str, Any],
    ) -> None:
        """
        Sends the updated rank info to the training processes.
        """
        self._send_rank_info_helper(
            worker_envs=worker_envs,
            message_type=InProcessRestartSocketMessageType.JOB_RANK_INFO,
            aggregate_worker_data=aggregate_worker_data,
        )

    def _send_rank_info_helper(
        self,
        worker_envs: dict[int, dict[str, str]],
        message_type: InProcessRestartSocketMessageType,
        aggregate_worker_data: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        `worker_envs` is usually set at _start_workers after the rendezvous when the training info has been updated.
        But in this case (InProcRestart), this would not be available at process start and needs to be sent before RCB.
        `worker_envs` should contain the following keys and value for every rank computed based on info from operator
        and which can possibly change between restarts:
            "RANK"
            "GROUP_RANK"
            "ROLE_RANK"
            "WORLD_SIZE"
            "GROUP_WORLD_SIZE"
            "ROLE_WORLD_SIZE"
            "MASTER_ADDR"
            "MASTER_PORT"
            "JOB_RESTART_COUNT"
            "TORCHELASTIC_RESTART_COUNT"
        """
        if set(worker_envs.keys()) != self.socket_server.client_ranks:
            raise HyperPodIPCException(
                f"Missing client connections from ranks={set(worker_envs.keys()) - self.socket_server.client_ranks}"
            )
        # In the current state this could be a broadcast. Keeping it per local_rank
        # in case we have rank specific variables in the future
        for local_rank, envs in worker_envs.items():
            if not self.socket_server.sendall_to_rank(
                    local_rank=local_rank,
                    message_type=message_type,
                    message={
                        "worker_envs": envs,
                        "aggregate_worker_data": aggregate_worker_data
                    },
            ):
                raise HyperPodIPCException(
                    f"Failed to send {message_type.value} signal to {local_rank=}"
                )
            self.ipc_wg.update_rank_info(
                local_rank=local_rank,
                global_rank=int(envs.get("RANK", "-1")),
                group_rank=int(envs.get("GROUP_RANK", "-1")),
            )

    def send_fault(self, restart_count: int) -> None:
        """
        Broadcasts to all local_rank that there has been a FAULT in the training job.
        All clients receiving this message are expected to clean up and get back to RCB barrier.
        """
        if not self.socket_server.broadcast(
                message_type=InProcessRestartSocketMessageType.JOB_FAULT,
                message={"restart_count": restart_count},
        ):
            raise HyperPodIPCException(
                f"Failed to send FAULT signal to training processes")

    def get_ranks_at_barrier(self, timeout=None, init=False):
        """
        Checks if all ranks are at the pre RCB barrier. This call is expected to be called from the monitor loop.
        ASSUMPTION: Only 1 socket client per local_rank
        """
        # TODO(mohaan): To make sure updates from the controller are being applied this shouldn't block indefinitely.
        ready_ranks, end = set(), 0
        if timeout:
            end = time.monotonic() + timeout
        while ready_ranks != self._local_ranks:
            if not init and self._local_ranks.difference(
                    self.client_ranks) != set():
                raise HyperPodPLRException(
                    f"Client connections dropped for ranks: {self._local_ranks - self.client_ranks}"
                )
            if timeout and end - time.monotonic() <= 0:
                raise HyperPodPLRException(
                    f"Timed out ({timeout}s) waiting for workers to report to barrier."
                )
            logger.info(
                f"Waiting for ranks={self._local_ranks-ready_ranks} to report ready status"
            )
            try:
                _, msg = self._clients_ready_queue.get(block=True, timeout=1)
                ready_ranks.add(msg["local_rank"])
                self.ipc_wg.notify_rank_at_barrier(msg["local_rank"])
            except queue.Empty:
                # No rank reported, try again
                pass
            except KeyError:
                raise HyperPodIPCException(
                    "Expected `local_rank` to be present in message from client"
                )
        return True

    def _job_fault_callback(self, msg: dict):
        local_rank = msg.get("local_rank")
        global_rank = msg.get("rank")
        group_rank = global_rank // self._local_world_size
        reason = msg.get("reason")
        message = msg.get("message")
        restart_mode = msg.get("restart_mode")
        logger.debug(
            f"Process with {global_rank=}, {local_rank=} reported failure")
        self.ipc_wg.fail_rank(
            group_rank,
            global_rank,
            local_rank,
            reason,
            message,
            restart_mode,
        )

    def _job_data_callback(self, msg: dict):
        local_rank = msg.get("local_rank")
        global_rank = msg.get("rank")
        group_rank = global_rank // self._local_world_size
        data = msg.get("data")
        logger.debug(
            f"Process with {global_rank=}, {local_rank=} reported data")
        self.ipc_wg.set_data(
            group_rank,
            global_rank,
            local_rank,
            data,
        )

    def _past_rcb_barrier_callback(self, msg):
        local_rank = msg.get("local_rank")
        logger.info(f"{local_rank=} has successfully passed RCB barrier")
        self.ipc_wg.notify_rank_past_barrier(local_rank)

    def _notify_labels_callback(self, msg):
        local_rank = msg.get("local_rank")
        labels = msg.get("labels")
        logger.debug(f"{local_rank=} received {labels=}")
        self.ipc_wg.assign_labels(
            labels=labels,
        )

    def passed_barrier(self):
        return self.ipc_wg.passed_barrier()

    def at_barrier(self):
        return self.ipc_wg.at_barrier()

    @property
    def is_failed(self) -> bool:
        return self.ipc_wg.is_failed

    def reset_worker_state(self, clear_data=False):
        self.ipc_wg.reset(clear_data)
        self.drain_message_queue(self._clients_ready_queue)

    def clear_clients(self):
        self.socket_server.clear_clients()

    def trigger_local_plr(self) -> bool:
        return any(w.restart_mode == RestartMode.LOCAL_PRL
                   for w in self.ipc_wg.workers.values())
