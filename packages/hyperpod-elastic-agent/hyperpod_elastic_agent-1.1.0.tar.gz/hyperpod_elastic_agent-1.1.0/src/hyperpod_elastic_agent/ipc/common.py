from abc import ABC, abstractmethod
from enum import Enum
from queue import Queue


class BaseIPC(ABC):
    """
    Base class for defining capabilities that are supported for the IPC between Agent and Training Processes.
    """

    @abstractmethod
    def register_message_queue(
        self,
        message_type: str,
        message_queue: Queue,
    ) -> None:
        """
        Register queues for message_types. When the agent/training_process receives a message of `message_type`
        it puts the accompanying payload along with the type name on this queue

        Args:
            message_type: type of message received from the socketserver
            message_queue: queue on which to put the optional accompanying payload
        """

    @abstractmethod
    def drain_message_queue(
        self,
        message_queue: Queue,
    ):
        """
        Clears the message queue in prep for waiting for a message from the agent/training_process

        Args:
            message_queue: queue on which to put the optional accompanying payload
        """


class HyperPodIPCException(RuntimeError):
    """Raised when a Hyperpod IPC communication fails within the timeout"""


class HyperPodPLRException(RuntimeError):
    """Raised from IPR state machine when a PLR needs to be triggered"""


class SocketMessageType(str, Enum):
    pass


class CommonSocketMessageType(SocketMessageType):
    INIT = "init"
    INVALID_RESPONSE = "invalid_response"


class InProcessRestartSocketMessageType(SocketMessageType):
    AT_RCB_BARRIER = "at_rcb_barrier"
    JOB_DATA = "job_data"
    JOB_FAILED_RANKS = "job_failed_ranks"
    JOB_FAULT = "job_fault"
    JOB_RANK_INFO = "job_rank_info"
    JOB_START = "job_start"
    PAST_RCB_BARRIER = "past_rcb_barrier"
    RANK_LABELS = "rank_labels"


class CheckpointDiscoverySocketMessageType(SocketMessageType):
    CKPT_INFO_GET = "ckpt_info_get"
    CKPT_INFO_UPDATE = "ckpt_info_update"
    CKPT_INIT = "ckpt_init"


class RestartMode(str, Enum):
    """
    PLR (Process Level Restart): This represents a global PLR. Framework communicates this to Operator via Agent,
                                 Operator triggers PLR across ALL Agents via a `/stop` command with "plr" flag
    IPR (In Process Restart): Default mode, if Operator doesn't send any special flags with a `/stop`
    JLR (Job Level Restart): Handled by Operator as a last resort restart strategy.
                             This is just in case we need a JLR triggered from the framework in the future.
    LOCAL_PRL: Framework communicates this to the Agent, Agent triggers a PLR across all workers in this node.
               This signal is not propagated to the Operator and handled locally.
    """
    IN_PROCESS_RESTART = "in_process_restart"
    JOB_LEVEL_RESTART = "job_level_restart"
    LOCAL_PRL = "local_process_level_restart"
    PROCESS_LEVEL_RESTART = "process_level_restart"
