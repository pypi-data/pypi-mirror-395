FROM 763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-training:2.4.0-gpu-py311-cu124-ubuntu22.04-ec2

ARG HP_ELASTIC_AGENT_WHL_FILE_NAME="hyperpod_elastic_agent-*-py3-none-any.whl"
ARG TRAIN_USE_GPU=false

ENV TEST_CASE=happy
ENV TEST_SLEEP_TIME=10
ENV FAIL_RANKS=2,
ENV LOGLEVEL=INFO
ENV TRAIN_USE_GPU=$TRAIN_USE_GPU
# Use :: for ipv6
ENV AGENT_HOST=0.0.0.0
ENV AGENT_PORT=8080
ENV NNODES=1
ENV NPROC_PER_NODE=auto
ENV TEST_FAIL_AFTER_EPOCH=1
ENV TORCHELASTIC_ERROR_FILE=error.json

WORKDIR /workspace
COPY mnist.py /workspace/mnist.py
COPY echo.sh /workspace/echo.sh
COPY ${HP_ELASTIC_AGENT_WHL_FILE_NAME} /workspace
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh \
    && pip install torchvision tensorboardX==2.6.2 \
    && pip install --no-cache-dir /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && rm /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && pip cache purge \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
