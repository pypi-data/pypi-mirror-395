import queue
import uuid

from abc import ABC
from typing import Callable, Optional
from .common import (
    BaseIPC,
    CheckpointDiscoverySocketMessageType,
    CommonSocketMessageType,
    HyperPodIPCException,
    InProcessRestartSocketMessageType,
    RestartMode,
    SocketMessageType,
)
from .socket import HyperPodElasticAgentSocketClient
from ..checkpoint_discovery import CheckpointType
from ..logging import get_logger

logger = get_logger(__name__)


class BaseIPCSocketClient(BaseIPC, ABC):
    socket_client = HyperPodElasticAgentSocketClient()

    def __init__(self):
        self.client_id = str(uuid.uuid4())

    def connect(self):
        self.socket_client.connect()
        # Identify the current clients rank to the server
        if not self.sendall(
                CommonSocketMessageType.INIT, {
                    "local_rank": self.socket_client.local_rank,
                    "client_id": self.client_id,
                }):
            raise ValueError("Failed to send INIT to server")

    def register_message_callback(
        self,
        message_type: str,
        callback: Callable[[dict], None],
    ):
        self.socket_client.register_message_callback(
            message_type,
            callback,
            self.client_id,
        )

    def register_message_queue(
        self,
        message_type: str,
        message_queue: queue.Queue,
    ) -> None:
        self.socket_client.register_message_queue(
            message_type,
            message_queue,
            self.client_id,
        )

    def drain_message_queue(
        self,
        message_queue: queue.Queue,
    ) -> list[tuple[SocketMessageType, Optional[dict]]]:
        return self.socket_client.drain_message_queue(message_queue)

    def sendall(
        self,
        message_type: str,
        message: dict,
    ):
        return self.socket_client.sendall(
            message_type,
            message,
            self.client_id,
        )


class CheckpointDiscoverySocketClient(BaseIPCSocketClient):
    """
    Provides an API for the training processes to be able to communicate checkpoint info
    to and from the HyperPodElasticAgent
    """

    def __init__(
        self,
        prefix: str,
        num_model_checkpoints: int = 0,
        num_data_checkpoints: int = 0,
    ):
        super().__init__()
        self.prefix = prefix
        self.num_model_checkpoints = num_model_checkpoints
        self.num_data_checkpoints = num_data_checkpoints
        self._get_latest_queue: queue.Queue = queue.Queue()
        self.register_message_queue(
            CheckpointDiscoverySocketMessageType.CKPT_INFO_GET,
            self._get_latest_queue)

        self.connect()
        if not self.sendall(
                CheckpointDiscoverySocketMessageType.CKPT_INIT,
            {
                "prefix": prefix,
                "checkpoint_types": {
                    CheckpointType.MODEL_CHECKPOINT:
                    self.num_model_checkpoints,
                    CheckpointType.DATA_CHECKPOINT: self.num_data_checkpoints,
                },
            }):
            raise ValueError(
                f"Failed to register checkpoint client with {prefix=} with the HyperPodElasticAgent"
            )
        logger.info(
            f"{self} connected to {self.socket_client.server_socket_path}")

    def __repr__(self):
        return f"CheckpointDiscoverySocketClient({self.prefix=}, {self.num_model_checkpoints=}, {self.num_data_checkpoints=})"

    def update(
        self,
        step: int,
        path: str,
        checkpoint_type: CheckpointType,
    ):
        """
        Communicates the checkpoint version that the training processes is operating on, to the HyperPodElasticAgent.
        This would be used by the HyperPodElasticAgent and the operator to reconcile the checkpoint to restart from
        in case of a failure.
        """
        if not self.sendall(
                CheckpointDiscoverySocketMessageType.CKPT_INFO_UPDATE, {
                    "step": step,
                    "path": path,
                    "checkpoint_type": checkpoint_type
                }):
            raise HyperPodIPCException(
                f"Failed to update HyperPodElasticAgent with the latest {step=}, {path=}, {checkpoint_type=} info."
            )

    def get_latest_checkpoint_path(self) -> Optional[str]:
        """
        Gets the latest checkpoint info from the HyperPodElasticAgent. In case of a restart this is the checkpoint
        that all training worker processes will restart from.
        """
        self.drain_message_queue(self._get_latest_queue)
        if not self.sendall(CheckpointDiscoverySocketMessageType.CKPT_INFO_GET,
                            {}):
            raise HyperPodIPCException(
                f"Failed to request latest checkpoint from agent.")
        try:
            _, msg = self._get_latest_queue.get(block=True)
            return msg.get("path")
        except queue.Empty:
            raise HyperPodIPCException("Failed to read data from server.")


class InProcessRestartSocketClient(BaseIPCSocketClient):
    """
    Provides an API for the training processes to be able to communicate info
    related to in process restarts to and from the HyperPodElasticAgent
    API Spec: https://quip-amazon.com/kBWEAPSd9KNd/Faraday-API-Spec-Between-InfraFramework
    """

    def __init__(self):
        super().__init__()
        self._hyperpod_barrier_queue = queue.Queue()
        self._hyperpod_wait_fault_queue = queue.Queue()
        self._hyperpod_wait_rank_queue = queue.Queue()

        self.register_message_queue(
            InProcessRestartSocketMessageType.JOB_START,
            self._hyperpod_barrier_queue,
        )
        self.register_message_queue(
            InProcessRestartSocketMessageType.JOB_FAULT,
            self._hyperpod_wait_fault_queue,
        )
        self.register_message_queue(
            InProcessRestartSocketMessageType.JOB_RANK_INFO,
            self._hyperpod_wait_rank_queue,
        )

        self.connect()
        logger.info(
            f"{self.__class__.__name__} connected to {self.socket_client.server_socket_path}"
        )

    def hyperpod_barrier(
        self,
        timeout: Optional[int] = None
    ) -> tuple[SocketMessageType, Optional[dict]]:
        """
        This is the `hp_barrier`
        from https://quip-amazon.com/IZBOAoVCwlvK/Faraday-Framework-fault-controller-design#temp:C:OKVd1dbec5522bc44c7956a33c01
        1. Notifies the agent that this rank is at the RCB barrier and ready to proceed.
        2. Then blocks on the Agent to issue a JOB_START notification. The job start notification will have data of
           the following format which is what this method returns
        (InProcessRestartSocketMessageType.JOB_START, {
            'worker_envs': {
                'RANK': '4',
                'GROUP_RANK': '1',
                'ROLE_RANK': '4',
                'WORLD_SIZE': '8',
                'GROUP_WORLD_SIZE': '8',
                'ROLE_WORLD_SIZE': '8',
                'MASTER_ADDR': '10.1.1.210',
                'MASTER_PORT': '1234',
                'JOB_RESTART_COUNT': '1',
                'TORCHELASTIC_RESTART_COUNT': '1',
                'SPARE': 'False'
            },
            'aggregate_worker_data':
                {
                    'rank_ips': [{'rank': 0, 'ip': '10.1.217.143'}],
                    'aggregate_worker_data': [{'group_rank': 1, 'rank': 4, 'local_rank': 0, 'failed': False, 'data': '{"step_restart_count=1_i=1": "1"}'}]
                }
            }
        ),
        """

        # 1: Let the server (and in turn the controller) know that the local_rank has reached the RCB_BARRIER
        if not self.sendall(InProcessRestartSocketMessageType.AT_RCB_BARRIER,
                            {}):
            raise HyperPodIPCException(
                "Failed to communicate barrier to server")

        # 2: Blocks until the Agent gets a `/start` call from the controller
        try:
            # Possible race condition here if the operator notifies start to clients before this client calls this
            self.drain_message_queue(self._hyperpod_barrier_queue)
            response = self._hyperpod_barrier_queue.get(block=True,
                                                        timeout=timeout)
        except queue.Empty:
            raise HyperPodIPCException(
                f"Timed out reading data from server after {timeout} seconds")
        else:
            logger.info("Barrier cleared")
            return response

    def hyperpod_wait_fault(
        self,
        timeout: Optional[int] = None
    ) -> tuple[SocketMessageType, Optional[dict]]:
        """
        Block until the next FAULT message from the socket server. The response will be of the following format
        (InProcessRestartSocketMessageType.FAULT, {"restart_count": 1})
        """
        try:
            self.drain_message_queue(self._hyperpod_wait_fault_queue)
            return self._hyperpod_wait_fault_queue.get(block=True,
                                                       timeout=timeout)
        except queue.Empty:
            raise HyperPodIPCException(
                f"Timed out reading data from server after {timeout} seconds")

    def hyperpod_wait_rank_info(
        self,
        timeout: Optional[int] = None
    ) -> tuple[SocketMessageType, Optional[dict]]:
        """
        Gets the latest or block until the next JOB_RANK_INFO message from the socket server. This is incremental
        information that the operator sends to the agent/workers as the state of the job changes.
        The response will be of the following format:
        (InProcessRestartSocketMessageType.JOB_RANK_INFO, {
            'worker_envs': {
                'RANK': '4',
                'GROUP_RANK': '1',
                'ROLE_RANK': '4',
                'WORLD_SIZE': '8',
                'GROUP_WORLD_SIZE': '8',
                'ROLE_WORLD_SIZE': '8',
                'MASTER_ADDR': '10.1.1.210',
                'MASTER_PORT': '1234',
                'JOB_RESTART_COUNT': '1',
                'TORCHELASTIC_RESTART_COUNT': '1',
                'SPARE': 'False'
            },
            'aggregate_worker_data':
                {
                    'rank_ips': [{'rank': 0, 'ip': '10.1.217.143'}],
                    'aggregate_worker_data': [{'group_rank': 1, 'rank': 4, 'local_rank': 0, 'failed': False, 'data': '{"step_restart_count=1_i=1": "1"}'}]
                }
            }
        ),
        """
        try:
            messages = self.drain_message_queue(self._hyperpod_wait_rank_queue)
            if len(messages) > 0:
                return messages[-1]
            return self._hyperpod_wait_rank_queue.get(block=True,
                                                      timeout=timeout)
        except queue.Empty:
            raise HyperPodIPCException(
                f"Timed out reading data from server after {timeout} seconds")

    def hyperpod_send_data(
        self,
        rank: int,
        data: str,
    ) -> None:
        """
        Notifies the Agent to associate data with this rank. This data is sent to the operator through the /status call.
        The operator then aggregates this data across all workers/agents and sends the aggregate data back to
        workers/agents via 2 APIs.
        * hyperpod_wait_rank_info: which gets incremental updates as the state of the job changes in preparation for a
                                   start/re-start
        * hyperpod_barrier: which gets the final aggregated information necessary for a new run to begin

        The data is cleared in 2 cases:
        * when a process level restart is triggered and the workers are terminated
        * after a new run has started following an in-process restart
        """
        if not self.sendall(InProcessRestartSocketMessageType.JOB_DATA, {
                "rank": rank,
                "data": data
        }):
            raise HyperPodIPCException("Failed to send data to Agent")

    def hyperpod_send_fault(
        self,
        rank: int,
        restart_mode: RestartMode = RestartMode.IN_PROCESS_RESTART,
        reason: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:
        """
        Sends a message notifying the Agent about a recoverable failure on this rank along with the restart mode that
        should be triggered
        """
        if not self.sendall(InProcessRestartSocketMessageType.JOB_FAULT, {
                "rank": rank,
                "restart_mode": restart_mode,
                "reason": reason,
                "message": message,
        }):
            raise HyperPodIPCException("Failed to send job_fault to Agent")

    def hyperpod_past_rcb_barrier(self) -> None:
        """
        Notifies the Agent that the barrier has been cleared successfully and we can transition to Agent.READY state
        """
        if not self.sendall(InProcessRestartSocketMessageType.PAST_RCB_BARRIER,
                            {}):
            raise HyperPodIPCException(
                "Failed to notify Agent of passing the RCB barrier")

    def hyperpod_notify_labels(
        self,
        labels: dict[str, str],
    ) -> None:
        """
        Lets the training jobs notify the agent about any dynamic labels e.g. PPRank.
        Currently, this is set per worker group i.e. whichever worker makes the most recent call will set this value
        and only used for setting PP labels. This is not intended to be used for per worker labels
        """
        if not self.sendall(InProcessRestartSocketMessageType.RANK_LABELS, {
                "labels": labels
        }):
            raise HyperPodIPCException(
                "Failed to notify Agent of current labels")


class TrainingManager:
    """
    Encapsulates capabilities for the training processes to wait on messages from the Agent and communicate
    its state to the Agent
    """

    def __init__(self):
        self.InProcessRestart = InProcessRestartSocketClient()

    @staticmethod
    def get_checkpoint_discovery_client(
        prefix: str,
        num_model_checkpoints: int = 0,
        num_data_checkpoints: int = 0,
    ):
        return CheckpointDiscoverySocketClient(
            prefix,
            num_model_checkpoints,
            num_data_checkpoints,
        )
