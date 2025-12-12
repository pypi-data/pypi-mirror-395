"""
Launch the socket server
$ cd test_scripts
$ python test_sock_server.py

Note the socket address in the console logs
`Server started on /tmp/hyperpod_elastic_agent_21063.sock`

Launch the clients with this socket path
$ SOCK_PATH="/tmp/hyperpod_elastic_agent_21063.sock" sh launch_clients.sh
"""

from hyperpod_elastic_agent import TrainingManager
import os

local_rank = int(os.environ.get("LOCAL_RANK", "0"))
c = TrainingManager()
print(f"CONNECTED client for {local_rank=}")

try:
    # BARRIER_1
    print(f"Client with {local_rank=} ENTERING barrier_1")
    response = c.InProcessRestart.hyperpod_barrier()
    print(
        f"Client with {local_rank=} EXITING barrier_1 with server message={response}"
    )

    # WAIT
    print(f"Client with {local_rank=} WAITING for server")
    response = c.InProcessRestart.hyperpod_wait()
    print(
        f"Client with {local_rank=} EXITED waiting for server with  with server message={response}"
    )

    # BARRIER_2
    print(f"Client with {local_rank=} ENTERING barrier_2")
    response = c.InProcessRestart.hyperpod_barrier()
    print(
        f"Client with {local_rank=} EXITING barrier_2 with  with server message={response}"
    )

    # SHUTDOWN
    print(f"Process with {local_rank=} completed")
except Exception as ex:
    print(f"Failed client: {ex}")
