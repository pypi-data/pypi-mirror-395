#!/bin/bash

if [ "$TRAIN_USE_GPU" = "false" ]; then
    export AGENT_CMD="--no-cuda --accelerator cpu"
else
    export NCCL_SOCKET_IFNAME="eth0"
fi

exec hyperpodrun --server-host=${AGENT_HOST} --server-port=${AGENT_PORT} \
    --tee=3 --log_dir=/tmp/hyperpod \
    --nnodes=${NNODES} --nproc-per-node=${NPROC_PER_NODE} \
    --pre-train-script=/workspace/echo.sh --pre-train-args='Pre-training script' \
    --post-train-script=/workspace/echo.sh --post-train-args='Post-training script' \
    /workspace/mnist_lightning_cd.py ${AGENT_CMD} --num_nodes=${NNODES} --devices=${NPROC_PER_NODE}
