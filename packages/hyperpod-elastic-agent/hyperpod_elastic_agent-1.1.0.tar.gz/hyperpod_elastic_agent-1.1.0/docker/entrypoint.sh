#!/bin/bash

if [ "$TRAIN_USE_GPU" = "false" ]; then
    export AGENT_CMD="--backend=gloo --no-cuda"
else
    export AGENT_CMD="--backend=nccl"
    export NCCL_SOCKET_IFNAME="eth0"
fi

exec hyperpodrun --server-host=${AGENT_HOST} --server-port=${AGENT_PORT} \
    --tee=3 --log_dir=/tmp/hyperpod \
    --nnodes=${NNODES} --nproc-per-node=${NPROC_PER_NODE} \
    --pre-train-script=/workspace/echo.sh --pre-train-args='Pre-training script' \
    --post-train-script=/workspace/echo.sh --post-train-args='Post-training script' \
    /workspace/mnist.py --epochs=2 ${AGENT_CMD}
