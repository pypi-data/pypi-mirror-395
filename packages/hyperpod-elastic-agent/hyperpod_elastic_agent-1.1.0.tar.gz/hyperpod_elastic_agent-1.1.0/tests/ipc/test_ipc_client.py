import os
import pytest
import queue
import socket

from unittest.mock import Mock, patch
from hyperpod_elastic_agent.checkpoint_discovery import CheckpointType
from hyperpod_elastic_agent.ipc.common import (
    CheckpointDiscoverySocketMessageType,
    HyperPodIPCException,
    InProcessRestartSocketMessageType,
    RestartMode,
)
from hyperpod_elastic_agent.ipc.client import (
    BaseIPCSocketClient,
    InProcessRestartSocketClient,
    CheckpointDiscoverySocketClient,
    TrainingManager,
)
from hyperpod_elastic_agent.ipc.util import LengthPrefixMessageFramer

DUMMY_SOCKET = os.path.join(os.sep, "tmp", "test.sock")


class TestCheckpointDiscoveryClient:
    FRAMER = LengthPrefixMessageFramer()

    @pytest.fixture
    def mock_backing_socket(self):
        with patch(
                "hyperpod_elastic_agent.ipc.socket.HyperPodElasticAgentSocketClient"
        ) as mock:
            BaseIPCSocketClient.socket_client = mock
            yield mock

    @pytest.fixture
    def client(self, mock_backing_socket):
        with patch.dict(
                "os.environ",
            {"HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH": DUMMY_SOCKET}):
            client = CheckpointDiscoverySocketClient(
                prefix="test_prefix",
                num_model_checkpoints=4,
                num_data_checkpoints=0,
            )
            return client

    def test_init_success(self, client, mock_backing_socket):
        assert client is not None
        assert client.socket_client is not None
        mock_backing_socket.connect.assert_called_once()
        assert mock_backing_socket.sendall.call_count == 2

    def test_init_fail(self, mock_backing_socket):
        mock_backing_socket.sendall.return_value = False
        with pytest.raises(ValueError):
            CheckpointDiscoverySocketClient(
                prefix="test_prefix",
                num_model_checkpoints=4,
                num_data_checkpoints=0,
            )

    def test_repr(self, client):
        assert repr(client).startswith("CheckpointDiscoverySocketClient(")

    def test_update_success(self, client, mock_backing_socket):
        mock_backing_socket.sendall.return_value = True
        client.update(step=123,
                      path="/test_path",
                      checkpoint_type=CheckpointType.MODEL_CHECKPOINT)
        client.socket_client.sendall.assert_called_with(
            CheckpointDiscoverySocketMessageType.CKPT_INFO_UPDATE, {
                "step": 123,
                "path": "/test_path",
                "checkpoint_type": CheckpointType.MODEL_CHECKPOINT,
            }, client.client_id)

    def test_update_fail(self, client, mock_backing_socket):
        mock_backing_socket.reset_mock()
        mock_backing_socket.sendall.return_value = False
        with pytest.raises(HyperPodIPCException):
            client.update(step=123,
                          path="/test_path",
                          checkpoint_type=CheckpointType.MODEL_CHECKPOINT)

    def test_get_latest_checkpoint_path_success(
        self,
        client,
        mock_backing_socket,
    ):
        client._get_latest_queue.put(
            (CheckpointDiscoverySocketMessageType.CKPT_INFO_GET, {
                "path": "/path"
            }))
        mock_backing_socket.reset_mock()
        assert client.get_latest_checkpoint_path() == "/path"
        mock_backing_socket.drain_message_queue.assert_called_once()
        assert mock_backing_socket.sendall.call_count == 1

    def test_get_latest_checkpoint_path_send_fail(
        self,
        client,
        mock_backing_socket,
    ):
        client._get_latest_queue.put(
            (CheckpointDiscoverySocketMessageType.CKPT_INFO_GET, {
                "path": "/path"
            }))
        mock_backing_socket.reset_mock()
        mock_backing_socket.sendall.return_value = False
        with pytest.raises(HyperPodIPCException):
            client.get_latest_checkpoint_path()
        mock_backing_socket.drain_message_queue.assert_called_once()
        assert mock_backing_socket.sendall.call_count == 1

    def test_get_latest_checkpoint_path_recv_fail(
        self,
        client,
        mock_backing_socket,
    ):
        get_ckpt_queue = Mock()
        get_ckpt_queue.get.side_effect = queue.Empty()
        client._get_latest_queue = get_ckpt_queue

        with pytest.raises(HyperPodIPCException) as exc_info:
            client.get_latest_checkpoint_path()
            assert "Failed to read data from server" in str(exc_info.value)

        client.socket_client.sendall.assert_called_with(
            CheckpointDiscoverySocketMessageType.CKPT_INFO_GET,
            {},
            client.client_id,
        )


class TestInProcessRestartSocketClient:
    FRAMER = LengthPrefixMessageFramer()

    @pytest.fixture
    def mock_backing_socket(self):
        with patch(
                "hyperpod_elastic_agent.ipc.socket.HyperPodElasticAgentSocketClient"
        ) as mock:
            yield mock

    @pytest.fixture
    def client(self, mock_backing_socket):
        with patch.dict(
                "os.environ",
            {"HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH": DUMMY_SOCKET}):
            InProcessRestartSocketClient.socket_client = mock_backing_socket
            client = InProcessRestartSocketClient()
            return client

    def test_init(self, client, mock_backing_socket):
        assert client is not None
        assert client.socket_client is not None
        mock_backing_socket.connect.assert_called_once()

    def test_connect_failure(self, client, mock_backing_socket):
        mock_backing_socket.connect.side_effect = socket.error(
            "Connection refused")

        with pytest.raises(OSError) as exc_info:
            InProcessRestartSocketClient()
        assert "Connection refused" in str(exc_info.value)

    def test_register_queue(self, client, mock_backing_socket):
        mock_backing_socket.connect.return_value = True
        assert mock_backing_socket.register_message_queue.call_count == 3

    def test_drain_queue(self, client, mock_backing_socket):
        barrier_queue = Mock()
        client._hyperpod_barrier_queue = barrier_queue
        client.drain_message_queue(barrier_queue)
        assert mock_backing_socket.drain_message_queue.call_count == 1

    def test_hyperpod_barrier_success(self, client, mock_backing_socket):
        barrier_msg = (InProcessRestartSocketMessageType.JOB_START, {})
        mock_backing_socket.sendall.return_value = True
        barrier_queue = Mock()
        barrier_queue.get.return_value = barrier_msg
        client._hyperpod_barrier_queue = barrier_queue

        response = client.hyperpod_barrier()

        # Verify the barrier message was sent
        assert response == barrier_msg
        client.socket_client.sendall.assert_called_with(
            InProcessRestartSocketMessageType.AT_RCB_BARRIER, {},
            client.client_id)

    def test_hyperpod_barrier_sendall_exception(self, client,
                                                mock_backing_socket):
        mock_backing_socket.sendall.return_value = False

        with pytest.raises(HyperPodIPCException) as exc_info:
            client.hyperpod_barrier()
            assert "Failed to communicate barrier to server" in str(
                exc_info.value)

        client.socket_client.sendall.assert_called_with(
            InProcessRestartSocketMessageType.AT_RCB_BARRIER, {},
            client.client_id)

    def test_hyperpod_barrier_recv_exception(self, client,
                                             mock_backing_socket):
        mock_backing_socket.sendall.return_value = True
        barrier_queue = Mock()
        barrier_queue.get.side_effect = queue.Empty()
        client._hyperpod_barrier_queue = barrier_queue

        with pytest.raises(HyperPodIPCException) as exc_info:
            client.hyperpod_barrier()
            assert "Failed to read data from server" in str(exc_info.value)

        client.socket_client.sendall.assert_called_with(
            InProcessRestartSocketMessageType.AT_RCB_BARRIER, {},
            client.client_id)

    def test_hyperpod_wait_fault_success(self, client, mock_backing_socket):
        wait_queue = Mock()
        wait_queue.get.return_value = (
            InProcessRestartSocketMessageType.JOB_FAULT, {})
        client._hyperpod_wait_fault_queue = wait_queue

        response = client.hyperpod_wait_fault()
        assert response == (InProcessRestartSocketMessageType.JOB_FAULT, {})
        wait_queue.get.assert_called_once()
        mock_backing_socket.drain_message_queue.assert_called_once()

    def test_hyperpod_wait_fault_exception(self, client, mock_backing_socket):
        wait_fault_queue = Mock()
        wait_fault_queue.get.side_effect = queue.Empty()
        client._hyperpod_wait_fault_queue = wait_fault_queue

        with pytest.raises(HyperPodIPCException) as exc_info:
            client.hyperpod_wait_fault()
            assert "Failed to read data from server" in str(exc_info.value)
            mock_backing_socket.clear_message_queue.assert_called_once()

    def test_hyperpod_wait_rank_info_success(self, client,
                                             mock_backing_socket):
        wait_rank_info_queue = Mock()
        wait_rank_info_queue.get.return_value = (
            InProcessRestartSocketMessageType.JOB_RANK_INFO, {})
        client._hyperpod_wait_rank_queue = wait_rank_info_queue

        response = client.hyperpod_wait_rank_info()
        assert response == (InProcessRestartSocketMessageType.JOB_RANK_INFO,
                            {})
        wait_rank_info_queue.get.assert_called_once()
        mock_backing_socket.drain_message_queue.assert_called_once()

    def test_hyperpod_wait_rank_info_exception(self, client,
                                               mock_backing_socket):
        wait_rank_info_queue = Mock()
        wait_rank_info_queue.get.side_effect = queue.Empty()
        client._hyperpod_wait_rank_queue = wait_rank_info_queue

        with pytest.raises(HyperPodIPCException) as exc_info:
            client.hyperpod_wait_rank_info()
            assert "Failed to read data from server" in str(exc_info.value)
            mock_backing_socket.clear_message_queue.assert_called_once()

    def test_hyperpod_send_fault_success(self, client, mock_backing_socket):
        client.hyperpod_send_data(
            rank=0,
            data="foo=bar",
        )
        mock_backing_socket.sendall.assert_called_with(
            InProcessRestartSocketMessageType.JOB_DATA, {
                "rank": 0,
                "data": "foo=bar",
            }, client.client_id)
        client.hyperpod_send_fault(
            rank=0,
            restart_mode=RestartMode.PROCESS_LEVEL_RESTART,
        )
        mock_backing_socket.sendall.assert_called_with(
            InProcessRestartSocketMessageType.JOB_FAULT, {
                "rank": 0,
                "restart_mode": RestartMode.PROCESS_LEVEL_RESTART,
                "reason": None,
                "message": None,
            }, client.client_id)

    def test_hyperpod_send_fault_exception(self, client, mock_backing_socket):
        mock_backing_socket.sendall.return_value = False
        with pytest.raises(HyperPodIPCException) as exc_info:
            client.hyperpod_send_fault(rank=0)
        assert "Failed to send job_fault to Agent" in str(exc_info.value)
        mock_backing_socket.sendall.return_value = True

    def test_hyperpod_past_rcb_barrier_success(self, client,
                                               mock_backing_socket):
        client.hyperpod_past_rcb_barrier()
        mock_backing_socket.sendall.assert_called_with(
            InProcessRestartSocketMessageType.PAST_RCB_BARRIER, {},
            client.client_id)

    def test_hyperpod_past_rcb_barrier_exception(self, client,
                                                 mock_backing_socket):
        mock_backing_socket.sendall.return_value = False
        with pytest.raises(HyperPodIPCException) as exc_info:
            client.hyperpod_past_rcb_barrier()
        assert "Failed to notify Agent of passing the RCB barrier" in str(
            exc_info.value)
        mock_backing_socket.sendall.return_value = True

    def test_hyperpod_notify_labels_success(self, client, mock_backing_socket):
        client.hyperpod_notify_labels(labels={"foo": "bar"})
        mock_backing_socket.sendall.assert_called_with(
            InProcessRestartSocketMessageType.RANK_LABELS,
            {"labels": {
                "foo": "bar"
            }}, client.client_id)

    def test_hyperpod_notify_labels_exception(self, client,
                                              mock_backing_socket):
        mock_backing_socket.sendall.return_value = False
        with pytest.raises(HyperPodIPCException) as exc_info:
            client.hyperpod_notify_labels(labels={"foo": "bar"})
        assert "Failed to notify Agent of current labels" in str(
            exc_info.value)
        mock_backing_socket.sendall.return_value = True


class TestTrainingManager:

    @pytest.fixture
    def mock_backing_socket(self):
        with patch(
                "hyperpod_elastic_agent.ipc.socket.HyperPodElasticAgentSocketClient"
        ) as mock:
            yield mock

    @pytest.fixture
    def manager(self, mock_backing_socket):
        with patch.dict(
                "os.environ",
            {"HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH": DUMMY_SOCKET}):
            InProcessRestartSocketClient.socket_client = mock_backing_socket
            CheckpointDiscoverySocketClient.socket_client = mock_backing_socket
            manager = TrainingManager()
            return manager

    def test_capabilities(self, manager):
        assert isinstance(
            manager.InProcessRestart,
            InProcessRestartSocketClient,
        )

    def test_get_checkpoint_discovery_client_success(self, manager):
        client = manager.get_checkpoint_discovery_client(
            prefix="temp",
            num_model_checkpoints=4,
            num_data_checkpoints=4,
        )
        assert isinstance(client, CheckpointDiscoverySocketClient)
        assert client.prefix == "temp"
