FROM 763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-training:2.4.0-gpu-py311-cu124-ubuntu22.04-ec2

ARG HP_ELASTIC_AGENT_WHL_FILE_NAME="hyperpod_elastic_agent-*-py3-none-any.whl"
ARG TRAIN_USE_GPU=false

ENV LOGLEVEL=INFO
ENV TRAIN_USE_GPU=$TRAIN_USE_GPU
# Use :: for ipv6
ENV AGENT_HOST=0.0.0.0
ENV AGENT_PORT=8080
ENV NNODES=1
ENV NPROC_PER_NODE=auto
ENV MASTER_ADDR=0.0.0.0

ENV TORCHELASTIC_MAX_RESTARTS=1

WORKDIR /workspace
COPY ${HP_ELASTIC_AGENT_WHL_FILE_NAME} /workspace
COPY echo.sh /workspace/echo.sh

RUN pip install -U --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu124 \
        pip pytorch_lightning torchvision kubernetes /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && rm /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && pip cache purge

COPY entrypoint-lightning-cd.sh /usr/local/bin/entrypoint-lightning-cd.sh
RUN chmod +x /usr/local/bin/entrypoint-lightning-cd.sh
COPY mnist_lightning_cd.py /workspace/mnist_lightning_cd.py

ENTRYPOINT ["/usr/local/bin/entrypoint-lightning-cd.sh"]
