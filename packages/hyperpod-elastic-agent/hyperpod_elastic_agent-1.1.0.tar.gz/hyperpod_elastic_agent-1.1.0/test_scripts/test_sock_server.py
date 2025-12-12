"""
Launch the socket server
$ cd test_scripts
$ python test_sock_server.py

Note the socket address in the console logs
`Server started on /tmp/hyperpod_elastic_agent_21063.sock`

Launch the clients with this socket path
$ SOCK_PATH="/tmp/hyperpod_elastic_agent_21063.sock" sh launch_clients.sh
"""

import time
from hyperpod_elastic_agent.ipc import (
    InProcessRestartSocketServer,
    CheckpointDiscoverySocketServer,
)

# Instantiate a CheckpointDiscoverySocketServer to make sure
# both are using the same backing socket connection
s, _ = InProcessRestartSocketServer(
    local_world_size=4), CheckpointDiscoverySocketServer()

print("WAITING for clients to get to barrier")
s.get_ranks_at_barrier(timeout=1800)
print("CLEARED barrier")

env = {
    "RANK": "0",
    "GROUP_RANK": "0",
    "ROLE_RANK": "0",
    "WORLD_SIZE": "4",
    "GROUP_WORLD_SIZE": "4",
    "ROLE_WORLD_SIZE": "4",
    "MASTER_ADDR": "192.168.1.1",
    "MASTER_PORT": "123456",
    "JOB_RESTART_COUNT": "2",
    "TORCHELASTIC_RESTART_COUNT": "2",
}
worker_envs = {}
for i in range(4):
    worker_envs[i] = env

print(f"SERVER accepted connection from {s.num_clients} clients, proceeding")
print("Simulating wait before /start...")
time.sleep(15)

# BARRIER_1
print(f"SENDING START signal to all workers")
s.send_start(worker_envs=worker_envs)
print("Simulating workload...")
time.sleep(15)

# WAIT
print(f"SENDING FAULT signal to all alive local_ranks")
s.send_fault()
## Send another FAULT to make sure it doesn't break anythings.send_fault()
print("SLEEPING...")
time.sleep(10)

# BARRIER_2
print(f"SENDING START signal to all workers")
s.send_start(worker_envs=worker_envs)
## Send another START to make sure it is a noop
s.send_start(worker_envs=worker_envs)
print("SLEEPING...")
time.sleep(15)

print("SLEEPING to allow clients to disconnect...")
while s.num_clients > 0:
    time.sleep(1)
