import pytest

from hyperpod_elastic_agent.ipc import RestartMode
from hyperpod_elastic_agent.ipc.util import (
    LengthPrefixMessageFramer,
    IPCWorkerGroup,
)


class TestLengthPrefixMessageFramer:

    @pytest.fixture
    def framer(self):
        return LengthPrefixMessageFramer()

    def test_frame_message(self):
        # Test framing a simple message
        message = b"Hello, World!"
        framed = LengthPrefixMessageFramer.frame_message(message)

        # First 4 bytes should be the length (13 in this case)
        # The length should be in network byte order (big-endian)
        assert len(framed) == len(message) + 4
        assert framed[4:] == message

    def test_process_data_single_message(self, framer):
        # Test processing a single complete message
        original_message = b"Test message"
        framed_message = LengthPrefixMessageFramer.frame_message(
            original_message)

        messages = framer.process_data(framed_message)
        assert len(messages) == 1
        assert messages[0] == original_message

    def test_process_data_multiple_messages(self, framer):
        # Test processing multiple messages in one data chunk
        messages = [b"First message", b"Second message", b"Third message"]
        framed_messages = b"".join(
            LengthPrefixMessageFramer.frame_message(msg) for msg in messages)

        received_messages = framer.process_data(framed_messages)
        assert len(received_messages) == 3
        assert received_messages == messages

    def test_process_data_incomplete_message(self, framer):
        # Test handling incomplete message
        original_message = b"Test message"
        framed_message = LengthPrefixMessageFramer.frame_message(
            original_message)

        # Send only part of the message
        partial_data = framed_message[:6]
        messages = framer.process_data(partial_data)
        assert len(messages) == 0

        # Send the rest of the message
        remaining_data = framed_message[6:]
        messages = framer.process_data(remaining_data)
        assert len(messages) == 1
        assert messages[0] == original_message

    def test_process_data_incomplete_length_prefix(self, framer):
        # Test handling incomplete length prefix
        original_message = b"Test message"
        framed_message = LengthPrefixMessageFramer.frame_message(
            original_message)

        # Send only part of the length prefix
        messages = framer.process_data(framed_message[:2])
        assert len(messages) == 0

        # Send the rest
        messages = framer.process_data(framed_message[2:])
        assert len(messages) == 1
        assert messages[0] == original_message

    def test_empty_message(self):
        # Test framing and processing an empty message
        empty_message = b""
        framed = LengthPrefixMessageFramer.frame_message(empty_message)

        framer = LengthPrefixMessageFramer()
        messages = framer.process_data(framed)
        assert len(messages) == 1
        assert messages[0] == empty_message

    def test_large_message(self):
        # Test with a larger message
        large_message = b"x" * 1024 * 1024  # 1MB message
        framed = LengthPrefixMessageFramer.frame_message(large_message)

        framer = LengthPrefixMessageFramer()
        messages = framer.process_data(framed)
        assert len(messages) == 1
        assert messages[0] == large_message


class TestIPCWorkerGroup:

    @pytest.fixture
    def ipc_wg(self):
        return IPCWorkerGroup(local_world_size=4)

    def test_failure_followed_by_at_barrier(self, ipc_wg):
        assert not ipc_wg.is_failed
        ipc_wg.set_data(
            group_rank=1,
            local_rank=0,
            global_rank=4,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=1,
            local_rank=0,
            global_rank=4,
            restart_mode=RestartMode.PROCESS_LEVEL_RESTART,
        )
        assert ipc_wg.is_failed
        assert {f.rank for f in ipc_wg.get_failed_ranks()} == {4}
        # Should reset global ranks
        ipc_wg.reset()
        ipc_wg.notify_rank_at_barrier(0)
        assert ipc_wg.get_worker_data() == [{
            "rank": -1,
            "group_rank": -1,
            "local_rank": 0,
            "failed": False,
            "data": "foo=bar",
        }]
        assert not ipc_wg.is_failed
        ipc_wg.notify_rank_past_barrier(0)
        assert ipc_wg.get_worker_data() == []

    def test_get_status(self, ipc_wg):
        assert ipc_wg.get_status() == "Healthy"
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=0,
            local_rank=0,
            global_rank=0,
        )
        assert ipc_wg.get_status() == "Failure"

    def test_get_rank_labels_and_reset(self, ipc_wg):
        assert ipc_wg.get_rank_labels() == {}
        ipc_wg.assign_labels({"TP": "1"})
        assert ipc_wg.get_rank_labels() == {"TP": "1"}
        ipc_wg.reset()
        # rank_labels are preserved across restarts
        assert ipc_wg.get_rank_labels() == {"TP": "1"}
        ipc_wg.update_rank_info(1, 0, 1)
        assert ipc_wg.get_rank_labels() == {"TP": "1"}
        # rank_labels is updated based on the most recent update
        ipc_wg.assign_labels({"TP": "3"})
        assert ipc_wg.get_rank_labels() == {"TP": "3"}

    def test_get_fault_data(self, ipc_wg):
        assert not ipc_wg.is_failed
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=0,
            local_rank=0,
            global_rank=0,
        )
        assert ipc_wg.is_failed
        assert ipc_wg.get_worker_data() == [{
            "group_rank": 0,
            "local_rank": 0,
            "rank": 0,
            "failed": True,
            "data": "foo=bar",
        }]

    def test_reset(self, ipc_wg):
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=0,
            local_rank=0,
            global_rank=0,
        )
        ipc_wg.reset()
        assert not ipc_wg.is_failed
        ipc_wg.notify_rank_at_barrier(0)
        ipc_wg.reset()
        assert ipc_wg.get_ranks_at_barrier() == set()
        ipc_wg.notify_rank_past_barrier(0)
        ipc_wg.reset()
        assert ipc_wg.get_ranks_past_barrier() == set()

    def test_fault_at_barrier(self, ipc_wg):
        ipc_wg.notify_rank_at_barrier(0)
        assert not ipc_wg.at_barrier()
        ipc_wg.notify_rank_at_barrier(1)
        ipc_wg.notify_rank_at_barrier(2)
        ipc_wg.notify_rank_at_barrier(3)
        assert ipc_wg.at_barrier()
        assert not ipc_wg.workers[0].failed
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=0,
            local_rank=0,
            global_rank=0,
        )
        assert ipc_wg.workers[0].failed
        assert not ipc_wg.at_barrier()
        assert ipc_wg.get_worker_data() != []
        ipc_wg.notify_rank_at_barrier(0)
        # `failed` shouldn't get cleared until a new run has started
        assert ipc_wg.workers[0].failed
        assert ipc_wg.at_barrier()

    def test_fault_past_barrier(self, ipc_wg):
        ipc_wg.notify_rank_at_barrier(0)
        assert not ipc_wg.at_barrier()
        ipc_wg.notify_rank_at_barrier(1)
        ipc_wg.notify_rank_at_barrier(2)
        ipc_wg.notify_rank_at_barrier(3)
        assert ipc_wg.at_barrier()
        for i in range(ipc_wg._local_world_size):
            ipc_wg.notify_rank_past_barrier(i)
        assert not ipc_wg.at_barrier()
        assert ipc_wg.passed_barrier()
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=0,
            local_rank=0,
            global_rank=0,
        )
        assert not ipc_wg.at_barrier()
        assert ipc_wg.get_worker_data() != []
        ipc_wg.notify_rank_at_barrier(0)
        assert not ipc_wg.at_barrier()
        ipc_wg.notify_rank_past_barrier(0)
        assert ipc_wg.passed_barrier()
        assert ipc_wg.get_worker_data() == []

    def test_get_operator_restart_mode(self, ipc_wg):
        assert not ipc_wg.at_barrier()
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            restart_mode=RestartMode.LOCAL_PRL,
        )
        assert ipc_wg.get_operator_restart_mode() is None
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=1,
            local_rank=1,
            global_rank=1,
            restart_mode=RestartMode.PROCESS_LEVEL_RESTART,
        )
        assert ipc_wg.get_operator_restart_mode(
        ) == RestartMode.PROCESS_LEVEL_RESTART
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        ipc_wg.fail_rank(
            group_rank=2,
            local_rank=2,
            global_rank=2,
            restart_mode=RestartMode.JOB_LEVEL_RESTART,
        )
        assert ipc_wg.get_operator_restart_mode(
        ) == RestartMode.JOB_LEVEL_RESTART

    def test_data_persists_at_barrier(self, ipc_wg):
        worker_data = {
            "group_rank": 0,
            "local_rank": 0,
            "rank": 0,
            "failed": False,
            "data": "foo=bar",
        }
        assert ipc_wg.get_status() == "Healthy"
        ipc_wg.set_data(
            group_rank=0,
            local_rank=0,
            global_rank=0,
            data="foo=bar",
        )
        assert ipc_wg.get_status() == "Healthy"
        assert ipc_wg.get_worker_data() == [worker_data]
        ipc_wg.notify_rank_at_barrier(0)
        assert ipc_wg.get_worker_data() == [worker_data]
