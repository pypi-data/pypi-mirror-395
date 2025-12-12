import copy
import json
import os
import selectors
import socket
import tempfile
import threading

from abc import ABC
from collections import defaultdict
from dataclasses import dataclass
from queue import Empty, Queue
from typing import Callable, Optional
from .common import CommonSocketMessageType, SocketMessageType
from .util import LengthPrefixMessageFramer
from ..logging import get_logger

logger = get_logger(__name__)
DEFAULT = "DEFAULT"


class HyperPodElasticAgentSocket(ABC):

    def __init__(self):
        self._event_loop_thread: threading.Thread
        self._message_queues: dict[tuple[str, str],
                                   list[Queue]] = defaultdict(list)
        self._message_callbacks: dict[tuple[str, str], list[Callable[
            [dict], Optional[dict]]]] = defaultdict(list)
        self._queue_lock = threading.Lock()
        self._selectors = selectors.DefaultSelector()
        self.running: bool = False

    def register_message_callback(
        self,
        message_type: str,
        callback: Callable[[dict], Optional[dict]],
        client_id: str = DEFAULT,
    ) -> None:
        """
        Register a callback for a (message_type, client_id) combo. When the socket receives a message of `message_type`
        it will invoke the callback with the deserialized message

        Args:
            message_type: type of message received from the socketserver
            callback: callable which handles the message and returns an optional response
            client_id: object identity if there are multiple sharing this socket connection
        """
        self._message_callbacks[(message_type, client_id)].append(callback)

    def register_message_queue(
        self,
        message_type: str,
        message_queue: Queue,
        client_id: str = DEFAULT,
    ) -> None:
        """
        Register queues for a (message_type, client_id) combo. When the socket receives a message of `message_type`
        it puts the accompanying payload along with the type name on this queue

        Args:
            message_type: type of message received from the socketserver
            message_queue: queue on which to put the optional accompanying payload
            client_id: object identity if there are multiple sharing this socket connection
        """
        self._message_queues[(message_type, client_id)].append(message_queue)

    def drain_message_queue(
        self,
        message_queue: Queue,
    ) -> list[tuple[SocketMessageType, Optional[dict]]]:
        """
        Clears the message queue in prep for waiting for a message from the socketserver

        Args:
            message_queue: queue on which to put the optional accompanying payload
        """
        messages = []
        with self._queue_lock:
            while not message_queue.empty():
                try:
                    message = message_queue.get_nowait()
                    messages.append(message)
                except Empty:
                    break
        return messages


@dataclass
class ClientData:
    client_id: str
    socket: socket.socket
    local_rank: int


class HyperPodElasticAgentSocketServer(HyperPodElasticAgentSocket):
    """
    Wrapper over a unix stream socket server. This server backs the InProcessRestart and CheckpointDiscovery
    servers for in process communication with the training processes
    """
    _singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super().__new__(cls)
        return cls._singleton_instance

    def __init__(self):
        super().__init__()
        socket_server_address = os.path.join(
            tempfile.gettempdir(),
            f"hyperpod_elastic_agent_{os.getpid()}.sock")
        if os.path.exists(socket_server_address):
            logger.debug(
                f"Unlinking pre-existing socket {socket_server_address}")
            os.unlink(socket_server_address)
        self.server_address = socket_server_address

        # Maps rank -> client sockets
        self._client_framers: dict[socket.socket,
                                   LengthPrefixMessageFramer] = {}
        self._client_data: dict[str, ClientData] = {}
        self._rank_to_client_ids: defaultdict[int, set[str]] = defaultdict(set)

    @property
    def client_ranks(self):
        """
        Set containing the ranks of the clients currently connected
        """
        return set(self._rank_to_client_ids.keys())

    @property
    def num_clients(self):
        """
        Number of clients currently connected. There can be multiple clients per rank
        """
        return sum(map(len, self._rank_to_client_ids.values()))

    def start(self, timeout: int = 60) -> None:
        """
        Start the socketserver

        Args:
            timeout: socket connection timeout
        """
        if self.running:
            return
        self._server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._server_socket.bind(self.server_address)
        self._server_socket.listen()
        self._server_socket.setblocking(False)
        self._server_socket.settimeout(timeout)
        self._selectors.register(
            fileobj=self._server_socket,
            events=selectors.EVENT_READ,
            data=self._accept_connection,
        )

        self._event_loop_thread = threading.Thread(
            target=self._run_server,
            daemon=True,
        )
        self.running = True
        self._event_loop_thread.start()
        logger.info(f"Server started on {self.server_address}")

    def shutdown(self) -> None:
        """
        Shuts down the socketserver
        """
        self._selectors.unregister(self._server_socket)
        self._server_socket.shutdown(socket.SHUT_RDWR)
        self._server_socket.close()

        self.running = False
        if self._event_loop_thread and self._event_loop_thread.is_alive():
            self._event_loop_thread.join()
        os.unlink(self.server_address)

    def clear_clients(self):
        """
        Cleans up all client connections. This can be used to force clear in case of process level restart.
        Instead of waiting for process termination to trigger a disconnect, we can pre-emptively do cleanup
        """
        sockets = [
            client_data.socket for client_data in self._client_data.values()
        ]
        for sock in sockets:
            self._cleanup_connection(sock)

    def _accept_connection(
        self,
        sock: socket.socket,
    ) -> None:
        """
        Accept a new client connection and register a callback with the selector for socket reads

        Args:
            sock: socket connection
        """
        client, addr = sock.accept()
        client.setblocking(True)

        # Create a message framer for this connection
        self._client_framers[client] = LengthPrefixMessageFramer()

        # Register the client for reading
        self._selectors.register(
            fileobj=client,
            events=selectors.EVENT_READ,
            data=self._recv,
        )
        logger.info(f"New connection accepted")

    def _cleanup_connection(
        self,
        sock: socket.socket,
    ):
        """
        * Unregister socket from selector to stop polling for events
        * Remove the socket specific message framer
        * Remove from the rank->sock map
        """
        logger.info(f"Cleaning socket: {sock}")
        try:
            self._selectors.unregister(sock)
        except (KeyError, ValueError):
            # socket already unregistered
            pass
        if sock in self._client_framers:
            del self._client_framers[sock]

        client_ids_to_remove = set()
        for client_id, client_data in self._client_data.items():
            if client_data.socket == sock:
                client_ids_to_remove.add(client_id)
                self._rank_to_client_ids[client_data.local_rank].discard(
                    client_id)

        self._rank_to_client_ids = defaultdict(
            set, {
                rank: client_ids
                for rank, client_ids in self._rank_to_client_ids.items()
                if client_ids
            })

        for client_id in client_ids_to_remove:
            del self._client_data[client_id]

    def _recv(
        self,
        sock: socket.socket,
    ) -> None:
        """
        Callback when receiving bytes from a client and decoding the data.
        The message_type is read from the payload and the optional accompanying data is
        put on the registered queues for this message_type
        """
        try:
            data = sock.recv(8192)
            if not data:
                logger.warning(f"{sock} connection closed")
                self._cleanup_connection(sock)
                return

            # Get the message framer for this socket
            framer = self._client_framers[sock]

            # Process received data and extract complete messages
            complete_messages = framer.process_data(data)

            for message_data in complete_messages:
                try:
                    # Decode and parse JSON message
                    msg = json.loads(message_data.decode("utf-8"))
                    logger.debug(f"Got data from client: {msg}")
                    msg_type = msg.pop("type", None)
                    local_rank = msg.get("local_rank")
                    client_id = msg.get("client_id")
                    if not msg_type or not client_id or local_rank is None:
                        logger.warning(
                            f"Invalid message with type={msg_type}, {local_rank=} or {client_id=}. Ignoring."
                        )
                        continue

                    # If this is an INIT message, register the sock for this rank
                    if msg_type == CommonSocketMessageType.INIT:
                        self._client_data[client_id] = ClientData(
                            client_id=client_id,
                            socket=sock,
                            local_rank=local_rank,
                        )
                        self._rank_to_client_ids[local_rank].add(client_id)
                        logger.info(f"Client identified with {local_rank=}")
                    else:
                        # Sending a copy of the payload to each consumer in case the consumer modifies it
                        with self._queue_lock:
                            for msg_q in self._message_queues.get(
                                (msg_type, DEFAULT), []):
                                msg_q.put((msg_type, copy.deepcopy(msg)))
                        for msg_callback in self._message_callbacks.get(
                            (msg_type, DEFAULT), []):
                            try:
                                response = msg_callback(copy.deepcopy(msg))
                                if response:
                                    HyperPodElasticAgentSocketServer._sendall_to_sock(
                                        sock,
                                        msg_type,
                                        client_id,
                                        response,
                                    )
                            except RuntimeError as ex:
                                logger.error(
                                    f"Exception in executing callback={msg_callback} for type={msg_type}: {str(ex)}"
                                )
                            except OSError as ex:
                                logger.error(
                                    f"Failed to send response to {client_id=} for callback={msg_callback}: {ex}"
                                )

                except json.JSONDecodeError:
                    logger.error("Unexpected response format from server.")
        except OSError as ex:
            logger.error(f"{sock} error: {ex}")
            self._cleanup_connection(sock)

    def _run_server(self) -> None:
        """Main server loop."""
        while self.running:
            try:
                events = self._selectors.select(timeout=1)
                for selector_key, _ in events:
                    callback = selector_key.data
                    callback(selector_key.fileobj)
            except OSError as e:
                logger.error(f"Error in server loop: {e.strerror}")

    @staticmethod
    def _sendall_to_sock(
        sock: socket.socket,
        message_type: str,
        client_id: str,
        message: Optional[dict] = None,
    ) -> bool:
        try:
            message = message or {}
            message["type"] = message_type
            message["client_id"] = client_id
            serialized_msg = json.dumps(message).encode("utf-8")
            framed_msg = LengthPrefixMessageFramer.frame_message(
                serialized_msg)
            sock.sendall(framed_msg)
            logger.debug(f"Sent {message=} to {client_id=}")
            return True
        except OSError as ex:
            logger.error(f"Failed to send {message=} with {client_id=}: {ex}")
            return False

    def sendall_to_rank(
        self,
        local_rank: int,
        message_type: str,
        message: Optional[dict] = None,
    ) -> bool:
        """
        Send a message (json serializable) to the socket server.
        Takes care of encoding the data before sending.

        Args:
            local_rank: the local_rank to which the payload will be sent
            message_type: type of message to send to the socketserver
            message: payload to send to the server

        Returns:
            bool: if the entire message was successfully sent
                  NOTE: Doesn't wait for an acknowledgment of receipt
        """
        if local_rank not in self._rank_to_client_ids:
            logger.error(
                f"Cannot send message to {local_rank=} as there is no registered client."
            )
            return False
        return all([
            HyperPodElasticAgentSocketServer._sendall_to_sock(
                self._client_data[client_id].socket,
                message_type,
                client_id,
                message,
            ) for client_id in self._rank_to_client_ids[local_rank]
        ])

    def broadcast(
        self,
        message_type: str,
        message: Optional[dict] = None,
    ) -> bool:
        """
        Send a message (json serializable) to all connected clients registered with this server.
        Takes care of encoding the data before sending.

        Args:
            message_type: type of message to send to the socketserver
            message: payload to send to the server

        Returns:
            bool: if the entire message was successfully sent
                  NOTE: Doesn't wait for an acknowledgment of receipt
        """
        return all([
            HyperPodElasticAgentSocketServer._sendall_to_sock(
                client.socket,
                message_type,
                client_id,
                message,
            ) for client_id, client in self._client_data.items()
        ])


class HyperPodElasticAgentSocketClient(HyperPodElasticAgentSocket):
    """
    Wraps a unix stream socket client. This client backs the InProcessRestart and CheckpointDiscovery
    servers for in process communication with the HyperPodElasticAgent.
    This will be instantiated only through implementations of BaseIPCSocketClient within a training worker process,
    launched by :py:class:`amzn_hyper_pod_elastic_agent.hyperpod_elastic_agent.HyperPodElasticAgent`
    as it depends on the environment variables set by the agent to function as expected.
    In case multiple InProcessRestart and CheckpointDiscovery clients are launched, they'll share the same backing
    socket client.
    """
    _singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super().__new__(cls)
        return cls._singleton_instance

    def __init__(self):
        super().__init__()
        self._sock: socket.socket
        self._message_framer: LengthPrefixMessageFramer
        self.server_socket_path: str = ""

    @property
    def local_rank(self):
        return int(os.getenv("LOCAL_RANK", "0"))

    def connect(self, timeout: int = 60) -> bool:
        """
        Connect to the socket server and send an Init message
        with the current rank of the training process

        Args:
            timeout: socket connection timeout

        Returns:
            bool: if the connection was successful
        """
        if self.running:
            return True
        self.server_socket_path = os.getenv(
            "HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH", "")
        if not self.server_socket_path:
            raise ValueError(
                "HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH not set. Can't initialize client"
            )
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)
        try:
            self._sock.connect(self.server_socket_path)
            self._sock.setblocking(False)
            self._message_framer = LengthPrefixMessageFramer()
            self._selectors.register(
                fileobj=self._sock,
                events=selectors.EVENT_READ,
                data=self._recv,
            )
            self._event_loop_thread = threading.Thread(
                target=self._run_client,
                daemon=True,
            )
            # Start the receiver thread
            self.running = True
            self._event_loop_thread.start()
        except OSError:
            self.disconnect()
            raise
        return self.running

    def disconnect(self) -> None:
        """
        Disconnect socket client
        """
        self.running = False

        if self._sock:
            try:
                self._selectors.unregister(self._sock)
            except (KeyError, ValueError):
                # socket already unregistered
                pass
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()

        if self._event_loop_thread not in {
                None, threading.current_thread()
        } and self._event_loop_thread.is_alive():
            self._event_loop_thread.join()

    def _recv(
        self,
        sock: socket.socket,
    ) -> None:
        """
        Callback when receiving bytes from the socketserver and decoding the data.
        The message_type is read from the payload and the optional accompanying data is
        put on the registered queues for this message_type
        """
        try:
            data = sock.recv(8192)
            if not data:
                logger.error("Server connection closed")
                self.disconnect()
                return

            complete_msgs = self._message_framer.process_data(data)

            for msg_data in complete_msgs:
                try:
                    msg = json.loads(msg_data.decode("utf-8"))
                    logger.debug(f"Got data from server: {msg}")
                    msg_type = msg.pop("type", None)
                    client_id = msg.pop("client_id", None)
                    if not msg_type or not client_id:
                        logger.warning(
                            f"Invalid message with type={msg_type}, {client_id=}. Ignoring."
                        )
                        continue
                    # Sending a copy of the payload to each consumer in case the consumer modifies it
                    with self._queue_lock:
                        for msg_q in self._message_queues.get(
                            (msg_type, client_id), []):
                            msg_q.put((msg_type, copy.deepcopy(msg)))
                    for msg_callback in self._message_callbacks.get(
                        (msg_type, client_id), []):
                        try:
                            msg_callback(copy.deepcopy(msg))
                        except RuntimeError as ex:
                            logger.error(
                                f"Exception in executing callback={msg_callback} for type={msg_type}: {str(ex)}"
                            )

                except json.JSONDecodeError:
                    logger.error("Unexpected response format from server.")
        except OSError as ex:
            logger.error(f"Socker error: {ex}")
            self.disconnect()

    def _run_client(self) -> None:
        """Main client receiver loop."""
        while self.running:
            try:
                # This will call the registered callbacks for ready ipc
                events = self._selectors.select(timeout=1)
                for key, _ in events:
                    callback = key.data
                    callback(key.fileobj)
            except OSError as e:
                logger.error(f"Error in client loop: {e.strerror}")
                self.disconnect()
                break

    def sendall(
        self,
        message_type: str,
        message: dict,
        client_id: str,
    ) -> bool:
        """
        Send a message (json serializable) to the socket server.
        Takes care of encoding the data before sending.

        Args:
            message_type: type of message to send to the socketserver
            message: payload to send to the server
            client_id: since multiple client objects could be using the same backing socket,
                    this id will be used to distinguish them for req-resp messages

        Returns:
            bool: if the entire message was successfully sent
                  NOTE: Doesn't wait for an acknowledgment of receipt
        """
        try:
            message["type"] = message_type
            message["local_rank"] = self.local_rank
            message["client_id"] = client_id
            serialized_msg = json.dumps(message).encode("utf-8")
            framed_msg = self._message_framer.frame_message(serialized_msg)
            self._sock.sendall(framed_msg)
            logger.debug(f"Sent {message=} to server")
            return True
        except OSError as ex:
            logger.error(
                f"Failed to send {message=} from {self.local_rank=}: {ex}")
            return False
