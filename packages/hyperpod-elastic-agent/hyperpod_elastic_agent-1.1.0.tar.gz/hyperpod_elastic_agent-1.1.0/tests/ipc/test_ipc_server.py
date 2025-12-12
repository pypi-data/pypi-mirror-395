import pytest
import queue

from hyperpod_elastic_agent.checkpoint_discovery import CheckpointType
from hyperpod_elastic_agent.ipc.common import (
    HyperPodPLRException,
    HyperPodIPCException,
    InProcessRestartSocketMessageType,
    RestartMode,
)
from hyperpod_elastic_agent.ipc.server import (
    CheckpointDiscoverySocketServer,
    InProcessRestartSocketServer,
)
from hyperpod_elastic_agent.ipc.socket import HyperPodElasticAgentSocketServer
from unittest.mock import ANY, Mock, call, patch


class TestCheckpointDiscoverySocketServer:

    @classmethod
    def setup_class(cls):
        cls.local_world_size = 4
        cls.local_ranks = set(range(cls.local_world_size))

    @pytest.fixture
    def mock_backing_socket(self):
        with patch(
                "hyperpod_elastic_agent.ipc.socket.HyperPodElasticAgentSocketServer"
        ) as mock:
            mock_instance = Mock()
            mock_instance.client_ranks = self.local_ranks
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def server(self, mock_backing_socket):
        CheckpointDiscoverySocketServer.socket_server = mock_backing_socket
        server = CheckpointDiscoverySocketServer()
        return server

    def test_init(self, server, mock_backing_socket):
        assert server is not None
        assert server.socket_server is not None
        mock_backing_socket.start.assert_called_once()
        assert mock_backing_socket.register_message_callback.call_count == 3

    def test_init_callback(self, server):
        ckpt_types = {
            CheckpointType.MODEL_CHECKPOINT: 8,
            CheckpointType.DATA_CHECKPOINT: 0,
        }
        assert server.tracker.checkpoint_datas == {}
        server._init_callback({
            "prefix": "test_prefix",
            "checkpoint_types": ckpt_types,
        })
        assert server.tracker.checkpoint_path_metadata.prefix == "test_prefix"
        assert server.tracker.checkpoint_path_metadata.checkpoint_types == ckpt_types
        # parameters are overridden
        server._init_callback({
            "prefix": "duplicate",
            "checkpoint_types": {
                CheckpointType.MODEL_CHECKPOINT: 4,
                CheckpointType.DATA_CHECKPOINT: 0,
            },
        })
        assert server.tracker.checkpoint_path_metadata.prefix == "duplicate"
        assert server.tracker.checkpoint_path_metadata.checkpoint_types[
            CheckpointType.MODEL_CHECKPOINT] == 4

    def test_update_callback(self, server):
        server._init_callback({
            "prefix": "test_prefix",
            "checkpoint_types": {
                CheckpointType.MODEL_CHECKPOINT: 8,
                CheckpointType.DATA_CHECKPOINT: 0,
            },
        })
        server._update_callback({
            "step":
            5,
            "local_rank":
            1,
            "path":
            "test",
            "checkpoint_type":
            CheckpointType.MODEL_CHECKPOINT
        })
        assert 5 in server.tracker.checkpoint_datas["test_prefix"]

    def test_get_latest_callback(self, server):
        data = {
            "prefix": "test_prefix",
            "checkpoint_types": {
                CheckpointType.MODEL_CHECKPOINT: 1,
                CheckpointType.DATA_CHECKPOINT: 0,
            },
        }
        server._init_callback(data)
        server._update_callback({
            "step":
            5,
            "local_rank":
            0,
            "path":
            "test",
            "checkpoint_type":
            CheckpointType.MODEL_CHECKPOINT
        })
        assert server._get_latest_callback({}) == {"path": "test"}


class TestInProcessRestartSocketServer:

    @classmethod
    def setup_class(cls):
        cls.local_world_size = 4
        cls.local_ranks = set(range(cls.local_world_size))

    @pytest.fixture
    def mock_backing_socket(self):
        with patch(
                "hyperpod_elastic_agent.ipc.socket.HyperPodElasticAgentSocketServer"
        ) as mock:
            mock_instance = Mock()
            mock_instance.client_ranks = self.local_ranks
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def server(self, mock_backing_socket):
        InProcessRestartSocketServer.socket_server = mock_backing_socket
        server = InProcessRestartSocketServer(
            local_world_size=self.local_world_size)
        return server

    def test_init_success(self, server, mock_backing_socket):
        assert server is not None
        assert server.socket_server is not None
        mock_backing_socket.start.assert_called_once()
        assert server._local_world_size == self.local_world_size
        assert server._local_ranks == self.local_ranks
        assert isinstance(server._clients_ready_queue, queue.Queue)
        mock_backing_socket.register_message_queue.assert_called_with(
            InProcessRestartSocketMessageType.AT_RCB_BARRIER, ANY)

    def test_init_failure(self, mock_backing_socket):
        with pytest.raises(HyperPodIPCException):
            InProcessRestartSocketServer(local_world_size=-1)

    def test_drain_clients_ready_queue(self, server, mock_backing_socket):
        server.drain_message_queue(server._clients_ready_queue)
        assert mock_backing_socket.drain_message_queue.call_count == 1

    def test_num_clients(self, server, mock_backing_socket):
        mock_backing_socket._clients = {}
        for i in range(self.local_world_size):
            mock_backing_socket._clients[i] = Mock()
        assert server.num_clients == self.local_world_size

    def test_send_start_success(self, server, mock_backing_socket):
        dummy_worker_data = {"rank": 1, "data": {"foo": "bar"}}
        server.send_start(
            worker_envs={
                0: {},
                1: {
                    "hello": "world"
                },
                2: {},
                3: {}
            },
            aggregate_worker_data=dummy_worker_data,
        )
        assert mock_backing_socket.sendall_to_rank.call_count == self.local_world_size
        mock_backing_socket.sendall_to_rank.assert_has_calls([
            call(local_rank=0,
                 message_type=InProcessRestartSocketMessageType.JOB_START,
                 message={
                     'aggregate_worker_data': dummy_worker_data,
                     'worker_envs': {},
                 }),
            call(local_rank=1,
                 message_type=InProcessRestartSocketMessageType.JOB_START,
                 message={
                     'aggregate_worker_data': dummy_worker_data,
                     'worker_envs': {
                         "hello": "world"
                     },
                 }),
            call(local_rank=2,
                 message_type=InProcessRestartSocketMessageType.JOB_START,
                 message={
                     'aggregate_worker_data': dummy_worker_data,
                     'worker_envs': {},
                 }),
            call(local_rank=3,
                 message_type=InProcessRestartSocketMessageType.JOB_START,
                 message={
                     'aggregate_worker_data': dummy_worker_data,
                     'worker_envs': {},
                 })
        ])

    def test_send_start_missing_clients(self, server, mock_backing_socket):
        mock_backing_socket.client_ranks = {0, 1, 2}
        with pytest.raises(HyperPodIPCException) as ex:
            server.send_start(
                worker_envs={
                    0: {},
                    1: {},
                    2: {},
                    3: {}
                },
                aggregate_worker_data={
                    "rank_ips": [],
                    "aggregate_worker_data": None,
                },
            )
        assert "Missing client connections from ranks={3}" in str(ex.value)

    def test_send_start_failed_send_to_clients(self, server,
                                               mock_backing_socket):
        mock_backing_socket.sendall_to_rank.return_value = False
        with pytest.raises(HyperPodIPCException) as ex:
            server.send_start(
                worker_envs={
                    0: {},
                    1: {},
                    2: {},
                    3: {}
                },
                aggregate_worker_data={
                    "rank_ips": [],
                    "aggregate_worker_data": None,
                },
            )
        assert "Failed to send job_start signal to local_rank=0" in str(
            ex.value)

    def test_send_rank_info_success(self, server, mock_backing_socket):
        worker_envs = {
            0: {
                "RANK": "0",
                "SPARE": "True"
            },
            1: {
                "RANK": "1",
                "SPARE": "True"
            },
            2: {
                "RANK": "2",
                "SPARE": "True"
            },
            3: {
                "RANK": "3",
                "SPARE": "True"
            }
        }
        aggregate_worker_data = {
            "rank_ips": [{
                "rank": 0,
                "ip": "10.1.1.210"
            }],
            "aggregate_worker_data": [{
                "group_rank": 1,
                "rank": 6,
                "local_rank": 2,
                "failed": False,
                "data": "foo=bar"
            }]
        }
        server.send_rank_info(
            worker_envs=worker_envs,
            aggregate_worker_data=aggregate_worker_data,
        )
        assert mock_backing_socket.sendall_to_rank.call_count == self.local_world_size
        mock_backing_socket.sendall_to_rank.assert_has_calls([
            call(local_rank=0,
                 message_type=InProcessRestartSocketMessageType.JOB_RANK_INFO,
                 message={
                     "worker_envs": {
                         "RANK": "0",
                         "SPARE": "True"
                     },
                     'aggregate_worker_data': aggregate_worker_data
                 }),
            call(local_rank=1,
                 message_type=InProcessRestartSocketMessageType.JOB_RANK_INFO,
                 message={
                     "worker_envs": {
                         "RANK": "1",
                         "SPARE": "True"
                     },
                     'aggregate_worker_data': aggregate_worker_data
                 }),
            call(local_rank=2,
                 message_type=InProcessRestartSocketMessageType.JOB_RANK_INFO,
                 message={
                     "worker_envs": {
                         "RANK": "2",
                         "SPARE": "True"
                     },
                     'aggregate_worker_data': aggregate_worker_data
                 }),
            call(local_rank=3,
                 message_type=InProcessRestartSocketMessageType.JOB_RANK_INFO,
                 message={
                     "worker_envs": {
                         "RANK": "3",
                         "SPARE": "True"
                     },
                     'aggregate_worker_data': aggregate_worker_data
                 })
        ])

    def test_send_rank_info_missing_clients(self, server, mock_backing_socket):
        mock_backing_socket.client_ranks = {0, 1, 2}
        with pytest.raises(HyperPodIPCException) as ex:
            server.send_rank_info({
                0: {},
                1: {},
                2: {},
                3: {}
            },
                                  aggregate_worker_data={})
        assert "Missing client connections from ranks={3}" in str(ex.value)

    def test_send_rank_info_failed_send_to_clients(self, server,
                                                   mock_backing_socket):
        mock_backing_socket.sendall_to_rank.return_value = False
        with pytest.raises(HyperPodIPCException) as ex:
            server.send_rank_info({
                0: {},
                1: {},
                2: {},
                3: {}
            },
                                  aggregate_worker_data={})
        assert "Failed to send job_rank_info signal to local_rank=0" in str(
            ex.value)

    def test_send_fault_success(self, server, mock_backing_socket):
        server.send_fault(restart_count=1)
        assert mock_backing_socket.broadcast.call_count == 1
        mock_backing_socket.broadcast.assert_called_once_with(
            message_type=InProcessRestartSocketMessageType.JOB_FAULT,
            message={"restart_count": 1},
        )

    def test_send_fault_failure(self, server, mock_backing_socket):
        mock_backing_socket.broadcast.return_value = False
        with pytest.raises(HyperPodIPCException) as ex:
            server.send_fault(restart_count=1)
        assert "Failed to send FAULT signal to training processes" in str(
            ex.value)

    def test_get_ranks_at_barrier_success(self, server, mock_backing_socket):
        for rank in self.local_ranks:
            ready_msg = (InProcessRestartSocketMessageType.AT_RCB_BARRIER, {
                "local_rank": rank
            })
            server._clients_ready_queue.put(ready_msg)
        assert server.get_ranks_at_barrier(timeout=60)

    def test_get_ranks_at_barrier_connection_dropped(
        self,
        server,
        mock_backing_socket,
    ):
        ready_queue = Mock()
        ready_queue.get.side_effect = queue.Empty()
        server._clients_ready_queue = ready_queue
        mock_backing_socket.client_ranks = self.local_ranks - {0}
        with pytest.raises(HyperPodPLRException) as ex:
            server.get_ranks_at_barrier(timeout=60)
        assert "Client connections dropped for ranks: {0}" in str(ex.value)

    def test_get_ranks_at_barrier_timeout(
        self,
        server,
        mock_backing_socket,
    ):
        ready_queue = Mock()
        ready_queue.get.side_effect = queue.Empty()
        server._clients_ready_queue = ready_queue
        timeout = 1
        with pytest.raises(HyperPodPLRException) as ex:
            server.get_ranks_at_barrier(timeout=timeout, init=True)
        assert f"Timed out ({timeout}s) waiting for workers to report to barrier." in str(
            ex.value)

    def test_get_ranks_at_barrier_missing_local_rank(
        self,
        server,
        mock_backing_socket,
    ):
        for rank in self.local_ranks:
            ready_msg = (InProcessRestartSocketMessageType.AT_RCB_BARRIER, {
                "global_rank": rank
            })
            server._clients_ready_queue.put(ready_msg)
        with pytest.raises(HyperPodIPCException) as ex:
            server.get_ranks_at_barrier(timeout=60)
        assert "Expected `local_rank` to be present in message from client" in str(
            ex.value)

    def test_job_fault_callback(self, server):
        server._job_fault_callback({"local_rank": 0, "rank": 4})
        assert server.ipc_wg.is_failed
        assert {f.rank for f in server.ipc_wg.get_failed_ranks()} == {4}

    def test_job_data_callback(self, server):
        server._job_data_callback({
            "local_rank": 0,
            "rank": 4,
            "data": "foo=bar"
        })
        assert not server.ipc_wg.is_failed
        assert server.ipc_wg.get_worker_data() == [
            {
                "rank": 4,
                "group_rank": 1,
                "local_rank": 0,
                "failed": False,
                "data": "foo=bar"
            },
        ]

    def test_past_rcb_barrier_callback(self, server):
        server._past_rcb_barrier_callback({"local_rank": 0, "rank": 4})
        assert not server.ipc_wg.passed_barrier()
        assert server.ipc_wg.passed_barrier() == server.passed_barrier()
        server._past_rcb_barrier_callback({"local_rank": 1, "rank": 5})
        server._past_rcb_barrier_callback({"local_rank": 2, "rank": 6})
        server._past_rcb_barrier_callback({"local_rank": 3, "rank": 7})
        assert server.ipc_wg.passed_barrier()

    def test_notify_labels_callback(self, server):
        labels = {"PP": "0", "TP": "1", "CP": "0", "EP": "3"}
        server._notify_labels_callback({
            "local_rank": 0,
            "rank": 4,
            "labels": labels
        })
        assert server.ipc_wg.get_rank_labels() == labels

    def test_at_barrier(self, server):
        server.ipc_wg.notify_rank_at_barrier(0)
        assert not server.ipc_wg.at_barrier()
        assert server.ipc_wg.at_barrier() == server.at_barrier()
        server.ipc_wg.notify_rank_at_barrier(1)
        server.ipc_wg.notify_rank_at_barrier(2)
        server.ipc_wg.notify_rank_at_barrier(3)
        assert server.ipc_wg.at_barrier()
        assert not server.ipc_wg.passed_barrier()

    def test_is_failed(self, server):
        assert not server.is_failed
        server.ipc_wg.set_data(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            data="foo=bar",
        )
        server.ipc_wg.fail_rank(
            local_rank=0,
            global_rank=0,
            group_rank=0,
        )
        assert server.is_failed
        server.reset_worker_state()
        assert not server.is_failed

    def test_clear_clients(self, server, mock_backing_socket):
        server.clear_clients()
        mock_backing_socket.clear_clients.assert_called_once()

    def test_reset_with_clear_data(self, server):
        server.socket_server = HyperPodElasticAgentSocketServer()
        server.ipc_wg.set_data(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            data="foo=bar",
        )
        server.ipc_wg.fail_rank(
            local_rank=0,
            global_rank=0,
            group_rank=0,
        )
        for rank in self.local_ranks:
            ready_msg = (InProcessRestartSocketMessageType.AT_RCB_BARRIER, {
                "global_rank": rank,
                "local_rank": rank,
            })
            server._clients_ready_queue.put(ready_msg)
        server.reset_worker_state(clear_data=True)
        assert server.ipc_wg.get_worker_data() == []
        # Message from previous run is cleared after reset
        with pytest.raises(
                HyperPodPLRException,
                match=
                r"Timed out \(1s\) waiting for workers to report to barrier.",
        ):
            server.get_ranks_at_barrier(timeout=1, init=True)

    def test_trigger_local_plr(self, server):
        assert not server.trigger_local_plr()
        server.ipc_wg.set_data(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            data="foo=bar",
        )
        server.ipc_wg.fail_rank(
            group_rank=0,
            global_rank=0,
            local_rank=0,
            restart_mode=RestartMode.LOCAL_PRL,
        )
        assert server.trigger_local_plr()
        server.ipc_wg.reset()
        assert not server.trigger_local_plr()
