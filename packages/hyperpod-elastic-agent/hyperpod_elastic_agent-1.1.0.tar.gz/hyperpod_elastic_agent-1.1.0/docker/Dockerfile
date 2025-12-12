FROM 763104351884.dkr.ecr.us-west-2.amazonaws.com/pytorch-training:2.2.0-cpu-py310-ubuntu20.04-ec2

WORKDIR /workspace
COPY test_train.py /workspace/test_train.py
COPY echo.sh /workspace/echo.sh

ARG HP_ELASTIC_AGENT_WHL_FILE_NAME="hyperpod_elastic_agent-*-py3-none-any.whl"

COPY ${HP_ELASTIC_AGENT_WHL_FILE_NAME} /workspace

ENV TEST_CASE=happy
ENV TEST_SLEEP_TIME=10
ENV FAIL_RANKS=2,
ENV LOGLEVEL=INFO
# Use :: for ipv6
ENV AGENT_HOST=0.0.0.0
ENV NPROC_PER_NODE=1

RUN pip install --no-cache-dir /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && rm /workspace/${HP_ELASTIC_AGENT_WHL_FILE_NAME} \
    && pip cache purge

ENTRYPOINT exec hyperpodrun \
    --server-host=${AGENT_HOST} --server-port=8080 \
    --nnodes=1 --nproc-per-node=$NPROC_PER_NODE --redirect=3 --tee=3 --log_dir=/tmp/hyperpod \
    --pre-train-script=/workspace/echo.sh --pre-train-args='pre-train-arg1 pre-train-arg2' \
    --post-train-script=/workspace/echo.sh --post-train-args='post-train-arg1 post-train-arg2' \
    /workspace/test_train.py
