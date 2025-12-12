FROM 763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-training:2.4.0-gpu-py311-cu124-ubuntu22.04-ec2

ARG HP_ELASTIC_AGENT_WHL_FILE_NAME="hyperpod_elastic_agent-*-py3-none-any.whl"
ARG TRAIN_USE_GPU=false

ENV TEST_CASE=happy
ENV TEST_SLEEP_TIME=5
ENV FAIL_RANKS=2,3,
ENV TEST_FAIL_AFTER_STEP=2
ENV LOGLEVEL=INFO
ENV TRAIN_USE_GPU=$TRAIN_USE_GPU
# Use :: for ipv6
ENV AGENT_HOST=0.0.0.0
ENV AGENT_PORT=8080
ENV NNODES=1
ENV NPROC_PER_NODE=4
ENV TORCHELASTIC_ERROR_FILE=error.json

WORKDIR /workspace
COPY ipr_test_train.py /workspace/ipr_test_train.py
COPY echo.sh /workspace/echo.sh
COPY ${HP_ELASTIC_AGENT_WHL_FILE_NAME} /workspace

RUN pip install --no-cache-dir /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && rm /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && pip cache purge \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

ENTRYPOINT exec hyperpodrun --inprocess-restart \
    --server-host=${AGENT_HOST} --server-port=${AGENT_PORT} \
    --nnodes=${NNODES} --nproc-per-node=${NPROC_PER_NODE} --redirect=3 --tee=3 --log_dir=/tmp/hyperpod \
    --pre-train-script=/workspace/echo.sh --pre-train-args='pre-train-arg1 pre-train-arg2' \
    --post-train-script=/workspace/echo.sh --post-train-args='post-train-arg1 post-train-arg2' \
    /workspace/ipr_test_train.py
