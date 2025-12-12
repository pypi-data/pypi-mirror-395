import json
import os
import pytest
import queue
import random
import re
import selectors

from hyperpod_elastic_agent.ipc.common import InProcessRestartSocketMessageType
from hyperpod_elastic_agent.ipc.socket import (
    ClientData,
    HyperPodElasticAgentSocketClient,
    HyperPodElasticAgentSocketServer,
)
from hyperpod_elastic_agent.ipc.util import LengthPrefixMessageFramer
from collections import defaultdict
from unittest.mock import ANY, Mock, call, patch

DEFAULT = "DEFAULT"


class TestHyperPodElasticAgentSocketServer:

    @pytest.fixture
    def mock_socket(self):
        with patch('socket.socket') as mock:
            mock_instance = Mock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def mock_select(self):
        with patch('selectors.DefaultSelector') as mock:
            mock_instance = Mock()
            mock_instance.register.return_value = Mock()
            mock_instance.unregister.return_value = Mock()
            mock.return_value = mock_instance
            yield mock

    @pytest.fixture
    def mock_os(self):
        with patch('os.unlink') as mock:
            yield mock

    @pytest.fixture
    def mock_thread(self):
        with patch('threading.Thread') as mock:
            mock_instance = Mock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def server(self, mock_socket, mock_select, mock_thread):
        server = HyperPodElasticAgentSocketServer()
        server._selectors = mock_select
        server.start()
        return server

    def test_init(self):
        server = HyperPodElasticAgentSocketServer()
        assert server._message_queues == {}
        assert not server.running
        assert server.server_address is not None

    def test_already_running(self, server, mock_socket):
        server.start()
        server.start()
        assert mock_socket.bind.call_count == 1

    @patch("os.path.exists", return_value=True)
    def test_path_exist(self, mock_socket, mock_os):
        server = HyperPodElasticAgentSocketServer()
        mock_os.assert_called_once_with(server.server_address)

    def test_singleton(self, server):
        server1 = HyperPodElasticAgentSocketServer()
        assert server1 == server

    def test_client_ranks(self, server):
        for i in range(2):
            server._rank_to_client_ids[i].add(Mock())
        assert server.client_ranks == {0, 1}

    def test_num_client(self, server):
        total_clients = 0
        for i in range(2):
            client_per_curr_rank = random.randint(1, 5)
            total_clients += client_per_curr_rank
            [
                server._rank_to_client_ids[i].add(Mock())
                for _ in range(client_per_curr_rank)
            ]
        assert server.client_ranks == {0, 1}
        assert server.num_clients == total_clients

    def test_server_address_property(self, server):
        assert isinstance(server.server_address, str)
        assert re.search(r"hyperpod_elastic_agent_\d+.sock$",
                         server.server_address)

    def test_start(self, server, mock_thread, mock_socket):
        assert server.running
        mock_socket.assert_has_calls([
            call.bind(ANY),
            call.listen(),
            call.setblocking(False),
        ])
        mock_thread.start.assert_called_once()

    def test_shutdown(self, server, mock_socket, mock_os, mock_thread):
        server.shutdown()
        assert not server.running
        mock_socket.close.assert_called_once()
        mock_thread.join.assert_called_once()
        mock_os.assert_called_once_with(server.server_address)

    def test_shutdown_thread_dead(self, server, mock_socket, mock_os,
                                  mock_thread):
        mock_thread.is_alive.return_value = False
        server.shutdown()
        assert not server.running
        mock_socket.close.assert_called_once()
        mock_thread.join.assert_not_called()
        mock_os.assert_called_once_with(server.server_address)

    def test_register_message_callback(self, server):
        test_callback = lambda x: x
        message_type = "TEST_MESSAGE"
        server.register_message_callback(message_type, test_callback)
        assert server._message_callbacks[(message_type,
                                          DEFAULT)] == [test_callback]

    def test_register_message_queue(self, server):
        test_queue = queue.Queue()
        message_type = "TEST_MESSAGE"
        server.register_message_queue(message_type, test_queue)
        assert server._message_queues[(message_type, DEFAULT)] == [test_queue]

    def test_drain_message_queue(self, server, mock_socket):
        test_queue = queue.Queue()
        message_type = "TEST_MESSAGE"
        test_queue.put(InProcessRestartSocketMessageType.JOB_FAULT)
        server.drain_message_queue(test_queue)
        assert len(server._message_queues[(message_type, DEFAULT)]) == 0

    def test_run_accept_connection(self, server, mock_socket, mock_select):
        mock_client_socket = Mock()
        mock_socket.accept.return_value = (mock_client_socket, 'mock_address')
        server._accept_connection(mock_socket)
        mock_socket.accept.assert_called_once()
        mock_client_socket.setblocking.assert_called_once_with(True)
        assert len(server._client_framers) == 1
        assert mock_client_socket in server._client_framers
        mock_select.register.assert_any_call(
            fileobj=mock_client_socket,
            events=selectors.EVENT_READ,
            data=ANY,
        )

    def test_cleanup_socket(self, server, mock_socket, mock_select):
        mock_client_socket1 = Mock()
        client_data1 = ClientData("111", mock_client_socket1, 0)
        mock_client_socket2 = Mock()
        client_data2 = ClientData("222", mock_client_socket2, 0)
        mock_socket.accept.side_effect = [
            (mock_client_socket1, 'mock_address1'),
            (mock_client_socket2, 'mock_address2')
        ]
        server._accept_connection(mock_socket)
        server._client_data["111"] = client_data1
        server._rank_to_client_ids[0].add("111")
        server._accept_connection(mock_socket)
        server._client_data["222"] = client_data2
        server._rank_to_client_ids[0].add("222")
        assert mock_select.register.call_count == 3
        assert mock_client_socket1 in server._client_framers
        assert mock_client_socket2 in server._client_framers
        server._cleanup_connection(mock_client_socket1)
        assert mock_select.unregister.call_count == 1
        assert len(server._client_framers) == 1
        assert len(server._rank_to_client_ids[0]) == 1
        server._cleanup_connection(mock_client_socket2)
        assert mock_select.unregister.call_count == 2
        assert len(server._client_framers) == 0
        assert 0 not in server._rank_to_client_ids

    def test_clear_clients(self, server, mock_socket, mock_select):
        mock_client_socket1 = Mock()
        client_data1 = ClientData("111", mock_client_socket1, 0)
        mock_client_socket2 = Mock()
        client_data2 = ClientData("222", mock_client_socket2, 0)
        mock_socket.accept.side_effect = [
            (mock_client_socket1, 'mock_address1'),
            (mock_client_socket2, 'mock_address2')
        ]
        server._accept_connection(mock_socket)
        server._client_data["111"] = client_data1
        server._rank_to_client_ids[0].add("111")
        server._accept_connection(mock_socket)
        server._client_data["222"] = client_data2
        server._rank_to_client_ids[0].add("222")
        server.clear_clients()
        assert server._client_data == {}
        assert server._client_framers == {}
        assert server._rank_to_client_ids == defaultdict(set)
        assert mock_select.unregister.call_count == 2

    def test_cleanup_unregistered_socket_no_error(
        self,
        server,
        mock_socket,
        mock_select,
    ):
        mock_unregistered_socket = Mock()
        mock_client_socket = Mock()
        server._client_data["111"] = ClientData("111", mock_client_socket, 0)
        server._rank_to_client_ids[0].add("111")
        server._cleanup_connection(mock_unregistered_socket)
        assert isinstance(server._rank_to_client_ids, defaultdict)
        # Make a second call to make sure there is no error for already unregistered socket
        mock_select.unregister.side_effect = KeyError
        server._cleanup_connection(mock_unregistered_socket)

    def test_recv_disconnect(self, mock_select, server, mock_socket):
        mock_client_socket = Mock()
        mock_client_socket.recv.return_value = None
        server._client_data["111"] = ClientData("111", mock_client_socket, 0)
        server._rank_to_client_ids[0].add("111")
        server._client_framers[mock_client_socket] = Mock()
        server._recv(mock_client_socket)
        assert mock_select.unregister.call_count == 1

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_recv_ignore_missing_msg_type(self, mock_logger, server):
        mock_client_socket = Mock()
        msg = LengthPrefixMessageFramer.frame_message(
            json.dumps({
                "dummy": "message"
            }).encode("utf-8"))
        mock_client_socket.recv.return_value = msg
        server._client_data["111"] = ClientData("111", mock_client_socket, 0)
        server._rank_to_client_ids[0].add("111")
        server._client_framers[mock_client_socket] = LengthPrefixMessageFramer(
        )
        server._recv(mock_client_socket)
        mock_logger.warning.assert_called_once_with(
            "Invalid message with type=None, local_rank=None or client_id=None. Ignoring."
        )
        # No new client has been added
        assert len(server._rank_to_client_ids) == len(server._client_data) == 1

    def test_recv_init(self, server):
        mock_client_socket = Mock()
        msg = LengthPrefixMessageFramer.frame_message(
            json.dumps({
                "type": "init",
                "local_rank": 0,
                "client_id": "123",
            }).encode("utf-8"))
        mock_client_socket.recv.return_value = msg
        assert len(server._rank_to_client_ids) == len(server._client_data) == 0
        server._client_framers[mock_client_socket] = LengthPrefixMessageFramer(
        )
        server._recv(mock_client_socket)
        # New client has been added
        assert len(server._rank_to_client_ids) == len(server._client_data) == 1
        assert {"123"} in server._rank_to_client_ids.values()
        assert "123" in server._client_data
        assert server._client_data["123"].socket == mock_client_socket
        assert server._client_data["123"].local_rank == 0
        assert len(server._client_framers) == 1

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_recv_ignore_init_missing_local_rank(self, mock_logger, server):
        mock_client_socket = Mock()
        msg = LengthPrefixMessageFramer.frame_message(
            json.dumps({
                "type": "init",
                "client_id": "123",
            }).encode("utf-8"))
        mock_client_socket.recv.return_value = msg
        assert len(server._rank_to_client_ids) == 0
        server._client_framers[mock_client_socket] = LengthPrefixMessageFramer(
        )
        server._recv(mock_client_socket)
        # No new client has been added
        mock_logger.warning.assert_called_once_with(
            "Invalid message with type=init, local_rank=None or client_id='123'. Ignoring."
        )
        assert len(server._rank_to_client_ids) == len(server._client_data) == 0

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_recv_ignore_invalid_json(self, mock_logger, server):
        mock_client_socket = Mock()
        msg = LengthPrefixMessageFramer.frame_message(
            "invalid_json".encode("utf-8"))
        mock_client_socket.recv.return_value = msg
        server._client_data["111"] = ClientData("111", mock_client_socket, 0)
        server._rank_to_client_ids[0].add("111")
        server._client_framers[mock_client_socket] = LengthPrefixMessageFramer(
        )
        server._recv(mock_client_socket)
        mock_logger.error.assert_called_once_with(
            "Unexpected response format from server.")
        # No new client has been added
        assert len(server._rank_to_client_ids) == len(server._client_data) == 1

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_recv_socket_error(
        self,
        mock_logger,
        mock_select,
        server,
    ):
        mock_client_socket1, mock_client_socket2 = Mock(), Mock()
        server._client_data["111"] = ClientData("111", mock_client_socket1, 0)
        server._client_data["222"] = ClientData("222", mock_client_socket2, 0)
        server._rank_to_client_ids[0] = {"111", "222"}
        mock_client_socket1.recv.side_effect = ConnectionResetError(
            "client socket connection error")
        server._client_framers[
            mock_client_socket1] = LengthPrefixMessageFramer()
        server._recv(mock_client_socket1)
        mock_logger.error.assert_called_once_with(
            f"{mock_client_socket1} error: client socket connection error")
        assert mock_select.unregister.call_count == 1
        assert len(server._client_framers) == 0
        assert len(server._rank_to_client_ids) == len(server._client_data) == 1

    def test_recv_valid_message(self, server):
        test_q = queue.Queue()
        server.register_message_queue("test", test_q)
        test_var = None

        def test_callback_1(echo_msg: dict) -> dict:
            nonlocal test_var
            test_var = echo_msg
            return {"foo": "bar"}

        def test_callback_2(echo_msg: dict) -> None:
            pass

        def test_callback_3(echo_msg: dict) -> None:
            raise RuntimeError("Callback failure")

        server.register_message_callback("test", test_callback_1)
        server.register_message_callback("test", test_callback_2)
        server.register_message_callback("test", test_callback_3)

        init = LengthPrefixMessageFramer.frame_message(
            json.dumps({
                "type": "init",
                "local_rank": 5,
                "client_id": "111",
            }).encode("utf-8"))
        msg = LengthPrefixMessageFramer.frame_message(
            json.dumps({
                "type": "test",
                "local_rank": 5,
                "client_id": "111",
                "envs": {
                    "GROUP_RANK": 5
                }
            }).encode("utf-8"))
        mock_client_socket = Mock()
        mock_client_socket.recv.return_value = init + msg
        server._client_framers[mock_client_socket] = LengthPrefixMessageFramer(
        )
        server._recv(mock_client_socket)
        assert len(server._client_framers) == 1
        assert len(server._rank_to_client_ids) == len(server._client_data) == 1
        payload = {
            "local_rank": 5,
            "client_id": "111",
            "envs": {
                "GROUP_RANK": 5
            }
        }
        msg_type, msg = test_q.get()
        assert (msg_type, msg) == ("test", payload)
        msg["envs"] = {}
        assert test_var == payload

    def test_run_server_success(
        self,
        server,
        mock_select,
    ):
        mock_callback = Mock()
        # Setup mock selector events
        mock_event1 = Mock()
        mock_event1.fileobj = server._server_socket  # Server socket
        mock_event1.data = mock_callback

        mock_client_socket = Mock()
        mock_event2 = Mock()
        mock_event2.fileobj = mock_client_socket  # Client socket
        mock_event2.data = mock_callback

        mock_select.select.side_effect = [
            [(mock_event1, selectors.EVENT_READ)],
            [(mock_event2, selectors.EVENT_READ)],
            KeyboardInterrupt,
        ]

        try:
            server._run_server()
        except KeyboardInterrupt:
            pass

        assert mock_callback.call_count == 2

    def test_run_server_not_running(
        self,
        server,
        mock_select,
    ):
        server.running = False
        server._run_server()
        mock_select.select.assert_not_called()
        server.running = True

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_run_server_client_disconnect(
        self,
        mock_logger,
        server,
        mock_socket,
        mock_select,
    ):
        mock_event1 = Mock()
        mock_event1.fileobj = mock_socket
        mock_event1.data = Mock()

        mock_select.select.side_effect = [
            [(mock_event1, selectors.EVENT_READ)],
            OSError(111, "Test error"),
            KeyboardInterrupt,
        ]

        try:
            server._run_server()
        except KeyboardInterrupt:
            pass
        mock_logger.error.assert_called_once_with(
            "Error in server loop: Test error")

    def test_sendall_to_rank_success(self, server):
        mock_client_socket = Mock()
        server._client_data["111"] = ClientData("111", mock_client_socket, 0)
        server._rank_to_client_ids[0] = {"111"}
        server._client_framers[mock_client_socket] = LengthPrefixMessageFramer(
        )
        assert server.sendall_to_rank(
            0, InProcessRestartSocketMessageType.JOB_START, {})

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_sendall_to_rank_client_not_connected(
        self,
        mock_logger,
        server,
    ):
        assert not server.sendall_to_rank(
            0, InProcessRestartSocketMessageType.JOB_START, {})
        mock_logger.error.assert_called_once_with(
            "Cannot send message to local_rank=0 as there is no registered client."
        )

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_sendall_to_rank_failure(
        self,
        mock_logger,
        server,
    ):
        mock_client_socket1, mock_client_socket2 = Mock(), Mock()
        server._client_data["111"] = ClientData("111", mock_client_socket1, 0)
        server._client_data["222"] = ClientData("111", mock_client_socket2, 0)
        mock_client_socket1.sendall.side_effect = OSError("Socket send failed")
        server._rank_to_client_ids[0] = {"111", "222"}
        server._client_framers[
            mock_client_socket1] = LengthPrefixMessageFramer()
        server._client_framers[
            mock_client_socket2] = LengthPrefixMessageFramer()
        assert not server.sendall_to_rank(
            0, InProcessRestartSocketMessageType.JOB_START, {})
        mock_logger.error.assert_called_once_with(
            "Failed to send message={'type': <InProcessRestartSocketMessageType.JOB_START: 'job_start'>, "
            "'client_id': '111'} with client_id='111': Socket send failed")

    def test_broadcast(self, server):
        mock_client_sock1, mock_client_sock2, mock_client_sock3 = Mock(), Mock(
        ), Mock()
        server._client_data["111"] = ClientData("111", mock_client_sock1, 0)
        server._client_data["222"] = ClientData("222", mock_client_sock2, 1)
        server._client_data["333"] = ClientData("333", mock_client_sock3, 1)
        server._rank_to_client_ids = defaultdict(set, {
            0: {"111"},
            1: {"222", "333"}
        })
        server._client_framers = {
            mock_client_sock1: LengthPrefixMessageFramer(),
            mock_client_sock2: LengthPrefixMessageFramer(),
            mock_client_sock3: LengthPrefixMessageFramer(),
        }
        server.broadcast(InProcessRestartSocketMessageType.JOB_START, {})
        assert mock_client_sock1.sendall.call_count == 1
        assert mock_client_sock2.sendall.call_count == 1
        assert mock_client_sock3.sendall.call_count == 1

    def test_start_timeout_setting(self, mock_socket, mock_select,
                                   mock_thread):
        """Test that socket timeout is properly set during server start"""
        server = HyperPodElasticAgentSocketServer()
        server._selectors = mock_select
        server.start(timeout=30)

        mock_socket.assert_has_calls([
            call.bind(ANY),
            call.listen(),
            call.setblocking(False),
            call.settimeout(30),
        ])
        assert server.running

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_sendall_to_rank_timeout(self, mock_logger, server):
        """Test sendall_to_rank behavior when socket times out"""
        mock_client_socket = Mock()
        server._client_data["111"] = ClientData("111", mock_client_socket, 0)
        server._rank_to_client_ids[0] = {"111"}

        from socket import timeout
        mock_client_socket.sendall.side_effect = timeout(
            "Socket operation timed out")

        assert not server.sendall_to_rank(0, "test_message", {"data": "test"})
        mock_logger.error.assert_called_once()
        error_msg = mock_logger.error.call_args[0][0]

        assert "Failed to send message=" in error_msg
        assert "'type': 'test_message'" in error_msg
        assert "'data': 'test'" in error_msg
        assert "with client_id='111'" in error_msg
        assert "timed out" in error_msg


class TestHyperPodElasticAgentSocketClient:
    DUMMY_SOCK = os.path.join(os.sep, "tmp", "test.sock")

    @pytest.fixture
    def mock_socket(self):
        with patch('socket.socket') as mock:
            mock_instance = Mock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def mock_select(self):
        with patch('selectors.DefaultSelector') as mock:
            mock_instance = Mock()
            mock_instance.register.return_value = Mock()
            mock_instance.unregister.return_value = Mock()
            mock.return_value = mock_instance
            yield mock

    @pytest.fixture
    def mock_thread(self):
        with patch('threading.Thread') as mock:
            mock_instance = Mock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def client(self, mock_socket, mock_select, mock_thread):
        with patch.dict(
                "os.environ",
            {"HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH": self.DUMMY_SOCK}):
            client = HyperPodElasticAgentSocketClient()
            client._selectors = mock_select
            client.connect()
            return client

    def test_init(self):
        client = HyperPodElasticAgentSocketClient()
        assert client._message_queues == {}
        assert not client.running
        assert client.server_socket_path is not None

    def test_singleton(self, client):
        client1 = HyperPodElasticAgentSocketClient()
        assert client == client1

    def test_already_running(self, client, mock_socket):
        client.connect()
        client.connect()
        assert mock_socket.connect.call_count == 1

    def test_connect_success(
        self,
        client,
        mock_thread,
        mock_socket,
    ):
        assert client.running
        mock_socket.assert_has_calls([
            call.settimeout(60),
            call.connect(ANY),
            call.setblocking(False),
        ])
        mock_thread.start.assert_called_once()

    def test_connect_incorrect_socket_env(
        self,
        client,
        mock_socket,
    ):
        client.running = False
        with pytest.raises(ValueError), patch.dict(
                "os.environ",
            {"HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH": ""}):
            client.connect()

    def test_connect_failure(
        self,
        client,
        mock_thread,
        mock_socket,
    ):
        mock_socket.connect.side_effect = OSError("Test error")
        client.running = False
        with pytest.raises(OSError), patch.dict(
                "os.environ",
            {"HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH": self.DUMMY_SOCK}):
            client.connect()
        mock_socket.assert_has_calls([
            call.settimeout(60),
            call.connect(ANY),
        ])
        client.running = True

    def test_disconnect(
        self,
        client,
        mock_socket,
        mock_thread,
        mock_select,
    ):
        mock_select.unregister.side_effect = KeyError()
        client.disconnect()
        assert not client.running
        mock_socket.shutdown.assert_called_once_with(2)
        mock_socket.close.assert_called_once()
        mock_thread.is_alive.assert_called_once()
        mock_thread.join.assert_called_once()

    def test_disconnect_socket_not_init(
        self,
        client,
        mock_socket,
        mock_thread,
    ):
        client._sock, client._event_loop_thread = None, None
        client.disconnect()
        mock_socket.shutdown.assert_not_called()
        mock_socket.close.assert_not_called()
        mock_thread.is_alive.assert_not_called()

    def test_recv_disconnect(self, mock_select, client, mock_socket):
        mock_socket.recv.return_value = None
        client._recv(mock_socket)
        assert mock_select.unregister.call_count == 1

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_recv_ignore_missing_msg_type(self, mock_logger, client):
        mock_server_socket = Mock()
        msg = LengthPrefixMessageFramer.frame_message(
            json.dumps({
                "dummy": "message"
            }).encode("utf-8"))
        mock_server_socket.recv.return_value = msg
        client._recv(mock_server_socket)
        mock_logger.warning.assert_called_once_with(
            "Invalid message with type=None, client_id=None. Ignoring.")

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_recv_ignore_invalid_json(self, mock_logger, client):
        mock_server_socket = Mock()
        msg = LengthPrefixMessageFramer.frame_message(
            "invalid_json".encode("utf-8"))
        mock_server_socket.recv.return_value = msg
        client._recv(mock_server_socket)
        mock_logger.error.assert_called_once_with(
            "Unexpected response format from server.")

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_recv_socket_error(
        self,
        mock_logger,
        mock_select,
        client,
    ):
        mock_server_socket = Mock()
        mock_server_socket.recv.side_effect = ConnectionResetError(
            "server socket connection error")
        client._recv(mock_server_socket)
        mock_logger.error.assert_called_once_with(
            f"Socker error: server socket connection error")
        assert mock_select.unregister.call_count == 1

    def test_recv_valid_message(self, client):
        test_q = queue.Queue()
        client.register_message_queue("test", test_q, "123")
        test_var = None

        def test_callback_1(echo_msg: dict) -> dict:
            nonlocal test_var
            test_var = echo_msg
            return {"foo": "bar"}

        def test_callback_2(echo_msg: dict) -> None:
            raise RuntimeError("Callback failure")

        client.register_message_callback("test", test_callback_1, "123")
        client.register_message_callback("test", test_callback_2, "123")

        msg = LengthPrefixMessageFramer.frame_message(
            json.dumps({
                "type": "test",
                "local_rank": 5,
                "client_id": "123",
                "envs": {
                    "GROUP_RANK": 5
                }
            }).encode("utf-8"))
        mock_server_socket = Mock()
        mock_server_socket.recv.return_value = msg
        client._recv(mock_server_socket)
        payload = {"local_rank": 5, "envs": {"GROUP_RANK": 5}}
        msg_type, msg = test_q.get()
        assert (msg_type, msg) == ("test", payload)
        msg["envs"] = {}
        assert test_var == payload

    def test_run_client_success(
        self,
        client,
        mock_select,
    ):
        mock_callback = Mock()
        # Setup mock selector events
        mock_event = Mock()
        mock_event.fileobj = client._sock
        mock_event.data = mock_callback

        mock_select.select.side_effect = [
            [(mock_event, selectors.EVENT_READ)],
            KeyboardInterrupt,
        ]

        try:
            client._run_client()
        except KeyboardInterrupt:
            pass

        assert mock_callback.call_count == 1

    def test_run_client_not_running(
        self,
        client,
        mock_select,
    ):
        client.running = False
        client._run_client()
        mock_select.select.assert_not_called()
        mock_select.unregister.assert_not_called()

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_run_client_disconnect(
        self,
        mock_logger,
        client,
        mock_socket,
        mock_select,
    ):
        mock_event = Mock()
        mock_event.fileobj = mock_socket
        mock_event.data = Mock()

        mock_select.select.side_effect = [
            [(mock_event, selectors.EVENT_READ)],
            OSError(111, "Test error"),
            KeyboardInterrupt,
        ]

        try:
            client._run_client()
        except KeyboardInterrupt:
            pass
        mock_logger.error.assert_called_once_with(
            "Error in client loop: Test error")
        mock_select.unregister.assert_called_once()

    def test_sendall_to_rank_success(self, client, mock_socket):
        assert client.sendall(InProcessRestartSocketMessageType.JOB_START, {},
                              "123")
        assert mock_socket.sendall.call_count == 1

    @patch("hyperpod_elastic_agent.ipc.socket.logger")
    def test_sendall_to_rank_failure(
        self,
        mock_logger,
        client,
        mock_socket,
    ):
        mock_socket.sendall.side_effect = OSError("Socket send failed")
        assert not client.sendall(InProcessRestartSocketMessageType.JOB_START,
                                  {}, "123")
        mock_logger.error.assert_called_once_with(
            "Failed to send message={'type': <InProcessRestartSocketMessageType.JOB_START: 'job_start'>, "
            "'local_rank': 0, 'client_id': '123'} from self.local_rank=0: Socket send failed"
        )
