#!/bin/bash
# Launch the socket server
# $ cd test_scripts
# $ python test_sock_server.py
# Note the socket address in the console logs
# `Server started on /tmp/hyperpod_elastic_agent_21063.sock`
# Launch the clients with this socket path
# $ SOCK_PATH="/tmp/hyperpod_elastic_agent_21063.sock" sh launch_clients.sh


HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH="$SOCK_PATH" LOCAL_RANK=0 python test_sock_client.py &
HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH="$SOCK_PATH" LOCAL_RANK=1 python test_sock_client.py &
HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH="$SOCK_PATH" LOCAL_RANK=2 python test_sock_client.py &
HYPERPOD_ELASTICAGENT_SOCKET_SERVER_PATH="$SOCK_PATH" LOCAL_RANK=3 python test_sock_client.py &
