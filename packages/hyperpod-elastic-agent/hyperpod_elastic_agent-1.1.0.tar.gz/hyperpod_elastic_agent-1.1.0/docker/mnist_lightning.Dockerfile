FROM 763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-training:2.4.0-gpu-py311-cu124-ubuntu22.04-ec2

ARG HP_ELASTIC_AGENT_WHL_FILE_NAME="hyperpod_elastic_agent-1.0-py3-none-any.whl"
ARG TRAIN_USE_GPU=false

ENV LOGLEVEL=INFO
ENV TRAIN_USE_GPU=$TRAIN_USE_GPU
# Use :: for ipv6
ENV AGENT_HOST=0.0.0.0
ENV AGENT_PORT=8080
ENV NNODES=1
ENV NPROC_PER_NODE=auto

WORKDIR /workspace
COPY mnist_lightning.py /workspace/mnist_lightning.py
COPY ${HP_ELASTIC_AGENT_WHL_FILE_NAME} /workspace

RUN pip install -U --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu124 \
        pip pytorch_lightning torchvision /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && rm /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && pip cache purge

ENTRYPOINT exec hyperpodrun \
    --server-host=${AGENT_HOST} --server-port=8080 \
    --nnodes=${NNODES} --nproc-per-node=${NPROC_PER_NODE} --redirect=3 --tee=3 --log_dir=/tmp/hyperpod \
    /workspace/mnist_lightning.py
