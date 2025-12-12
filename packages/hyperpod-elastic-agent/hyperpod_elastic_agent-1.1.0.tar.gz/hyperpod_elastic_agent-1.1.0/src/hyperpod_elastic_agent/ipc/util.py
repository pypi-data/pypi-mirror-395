from dataclasses import dataclass
from enum import Enum, auto
from struct import calcsize, pack, unpack
from typing import Any, Optional
from .common import RestartMode


class LengthPrefixMessageFramer:
    """
    Handles message framing for sending/receiving arbitrary length messages
    by length-prefixing them https://blog.stephencleary.com/2009/04/message-framing.html.
    """

    def __init__(self):
        """Initialize a message framer for receiving messages."""
        self.buffer = bytearray()
        self.message_length = None
        self.prefix_size = calcsize('!I')

    @staticmethod
    def frame_message(data: bytes) -> bytes:
        """Frame a message with its length prefix.

        Args:
            data: The raw message bytes to frame

        Returns:
            bytes: Length-prefixed framed message
        """
        # Use a 4-byte unsigned integer (network byte order) for the length prefix
        # https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment
        length_prefix = pack('!I', len(data))
        return length_prefix + data

    def process_data(self, data: bytes) -> list[bytes]:
        """Process incoming data and extract complete messages.

        Args:
            data: New data received from socket

        Returns:
            list[bytes]: List of complete messages extracted
        """
        self.buffer.extend(data)
        messages = []

        # Process buffer until we can't extract more complete messages
        while True:
            # If we don't know the current message length, try to extract it
            if self.message_length is None:
                if len(self.buffer) >= self.prefix_size:
                    self.message_length = unpack(
                        '>I', self.buffer[:self.prefix_size])[0]
                    self.buffer = self.buffer[self.prefix_size:]
                else:
                    # Not enough data to get length, wait for more
                    break

            # If we have the message length, check if the complete message is available
            if len(self.buffer) >= self.message_length:
                message_data = bytes(self.buffer[:self.message_length])
                messages.append(message_data)
                self.buffer = self.buffer[self.message_length:]
                self.message_length = None  # Reset for next message
            else:
                # Incomplete message, wait for more data
                break

        return messages


class IPCRankState(Enum):
    AT_BARRIER = auto()
    FAILED = auto()
    HEALTHY = auto()
    PAST_BARRIER = auto()


@dataclass
class IPCRankData:
    local_rank: int
    rank: int = -1
    group_rank: int = -1
    data: Optional[str] = None
    restart_mode: RestartMode = RestartMode.IN_PROCESS_RESTART
    reason: Optional[str] = None
    message: Optional[str] = None
    state: IPCRankState = IPCRankState.HEALTHY
    failed: bool = False


class IPCWorkerGroup:

    def __init__(self, local_world_size):
        self._local_world_size = local_world_size
        self.workers: dict[int, IPCRankData] = {
            local_rank: IPCRankData(local_rank=local_rank)
            for local_rank in range(local_world_size)
        }
        self._rank_labels: Optional[dict[str, str]] = {}

    @property
    def is_failed(self) -> bool:
        """
        Checks to see if there are ranks which have reported IPR failure
        """
        return any(w.state == IPCRankState.FAILED
                   for w in self.workers.values())

    def get_status(self) -> str:
        """
        Returns a string for the worker group status intended to be added to the status response for the Operator
        """
        if self.is_failed:
            return "Failure"
        return "Healthy"

    def get_rank_labels(self) -> Optional[dict[str, str]]:
        return self._rank_labels

    def get_worker_data(self) -> list[dict[str, Any]]:
        return [{
            "rank": w.rank,
            "group_rank": w.group_rank,
            "local_rank": local_rank,
            "failed": w.failed,
            "data": w.data,
        } for local_rank, w in self.workers.items() if w.data is not None]

    def reset(self, clear_data=False):
        # TODO(mohaan): Should we maintain rank_labels across restarts given the rank could change?
        self.workers = {
            local_rank:
            IPCRankData(
                local_rank=local_rank,
                data=None if clear_data else w.data,
                restart_mode=RestartMode.IN_PROCESS_RESTART,
            )
            for local_rank, w in self.workers.items()
        }

    def fail_rank(
        self,
        group_rank: int,
        global_rank: int,
        local_rank: int,
        reason: Optional[str] = None,
        message: Optional[str] = None,
        restart_mode: RestartMode = RestartMode.IN_PROCESS_RESTART,
    ):
        self.workers[local_rank].group_rank = group_rank
        self.workers[local_rank].rank = global_rank
        self.workers[local_rank].restart_mode = restart_mode
        self.workers[local_rank].state = IPCRankState.FAILED
        self.workers[local_rank].reason = reason
        self.workers[local_rank].message = message
        self.workers[local_rank].failed = True

    def set_data(
        self,
        group_rank: int,
        global_rank: int,
        local_rank: int,
        data: str,
    ):
        self.workers[local_rank].group_rank = group_rank
        self.workers[local_rank].rank = global_rank
        self.workers[local_rank].data = data

    def update_rank_info(
        self,
        local_rank: int,
        group_rank: int,
        global_rank: int,
    ):
        self.workers[local_rank].group_rank = group_rank
        self.workers[local_rank].rank = global_rank

    def notify_rank_at_barrier(self, local_rank):
        self.workers[local_rank].state = IPCRankState.AT_BARRIER

    def get_ranks_at_barrier(self) -> set[int]:
        return {
            w.local_rank
            for w in self.workers.values()
            if w.state == IPCRankState.AT_BARRIER
        }

    def notify_rank_past_barrier(self, local_rank):
        # Previous worker data is only cleared until after a new run has successfully started
        self.workers[local_rank].data = None
        self.workers[local_rank].state = IPCRankState.PAST_BARRIER
        self.workers[local_rank].restart_mode = RestartMode.IN_PROCESS_RESTART
        self.workers[local_rank].failed = False

    def get_ranks_past_barrier(self) -> set[int]:
        return {
            w.local_rank
            for w in self.workers.values()
            if w.state == IPCRankState.PAST_BARRIER
        }

    def get_failed_ranks(self) -> list[IPCRankData]:
        return [
            w
            for w in self.workers.values() if w.state == IPCRankState.FAILED
        ]

    def assign_labels(
        self,
        labels: dict[str, str],
    ):
        self._rank_labels = labels

    def passed_barrier(self) -> bool:
        return all(w.state == IPCRankState.PAST_BARRIER
                   for w in self.workers.values())

    def at_barrier(self) -> bool:
        return all(w.state == IPCRankState.AT_BARRIER
                   for w in self.workers.values())

    def get_operator_restart_mode(self) -> Optional[RestartMode]:
        """
        This is used to set the status data with a restart mode which needs to be handled by the operator
        """
        if any(w.restart_mode == RestartMode.JOB_LEVEL_RESTART
               for w in self.workers.values()):
            return RestartMode.JOB_LEVEL_RESTART
        if any(w.restart_mode == RestartMode.PROCESS_LEVEL_RESTART
               for w in self.workers.values()):
            return RestartMode.PROCESS_LEVEL_RESTART
        return None
