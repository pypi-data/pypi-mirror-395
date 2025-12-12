import json
import logging
import os
import random
import sys
import threading
import time
from hyperpod_elastic_agent import (
    CheckpointDiscoverySocketClient,
    RestartMode,
    TrainingManager,
)
from hyperpod_elastic_agent.checkpoint_discovery import CheckpointType
from typing import List

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.INFO,
                    stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
restart_count = 0

SLEEP_TIME = int(os.environ.get("TEST_SLEEP_TIME", "5"))
LOCAL_RANK = int(os.environ["LOCAL_RANK"])
GLOBAL_RANK = int(os.environ["RANK"])
NUM_EPOCHS = int(os.environ.get("NUM_EPOCHS", "10"))
TEST_CASE = str(os.environ.get("TEST_CASE"))
FAILURE_COUNT = int(os.environ.get("FAILURE_COUNT", 1))

HEALTHY_LOG = "Training model, speed: 1000 TFLOPs..."
SLOW_LOG = "Training model, speed: 1 TFLOPs..."


def get_ranks_to_fail() -> List[int]:
    # Fail for rank 2,3, by default
    fail_ranks_str = os.environ.get("FAIL_RANKS", "2,3,")
    fail_ranks = [int(rank) for rank in fail_ranks_str.split(',') if rank]
    return fail_ranks


def sleep_with_jitter(fault_event, base_delay=SLEEP_TIME, jitter_range=1):
    delay = base_delay + random.uniform(-jitter_range, jitter_range)
    if delay < 0:
        delay = 1
    logger.debug(f"[{LOCAL_RANK=}] Sleeping for {delay} secs...")
    fault_event.wait(delay)


def dummy_get_step_from_path(ckpt_path: str):
    return int(ckpt_path[-1])


def step(
    training_manager: TrainingManager,
    fault_event: threading.Event,
    ckpt_clients: list[CheckpointDiscoverySocketClient],
):
    global GLOBAL_RANK
    logger.info(
        f"[{LOCAL_RANK=}] At RCB barrier. Waiting for server signal to proceed..."
    )
    _, payload = training_manager.InProcessRestart.hyperpod_barrier()
    envs, aggregate_worker_data = payload["worker_envs"], payload["aggregate_worker_data"]
    fault_event.clear()
    logger.info(
        f"[{LOCAL_RANK=}] Received start from Agent with {envs=}, {aggregate_worker_data=}"
    )
    GLOBAL_RANK = int(envs["RANK"])
    global restart_count
    restart_count = int(envs["TORCHELASTIC_RESTART_COUNT"])
    logging.info(
        "Sleeping to simulate delay for `at barrier` -> `past barrier`")
    sleep_with_jitter(fault_event, base_delay=3)
    training_manager.InProcessRestart.hyperpod_past_rcb_barrier()

    curr_step = 1
    # If this is a restart get the latest_checkpoint_path and parse it to get the step to restart from
    if restart_count > 0:
        latest_ckpt_path = ckpt_clients[0].get_latest_checkpoint_path()
        logger.info(
            f"[{LOCAL_RANK=}] Got latest checkpoint path from Agent: {latest_ckpt_path}"
        )
        if latest_ckpt_path is not None:
            # Checkpoint might not be available if the first checkpoint was not fully saved
            curr_step = dummy_get_step_from_path(latest_ckpt_path)

    logger.info(
        f"[{LOCAL_RANK=}] Cleared RCB barrier. Proceeding with training...")
    for i in range(NUM_EPOCHS):
        logger.info(
            f"[{LOCAL_RANK=}] Running epoch={i} with ckpt_step={curr_step}")
        # Simulate
        # 1. running training step
        # 2. writing ckpt file
        sleep_with_jitter(fault_event)
        # clients calls update
        for client in ckpt_clients:
            client.update(
                step=curr_step,
                path=f"test_path_{curr_step}",
                checkpoint_type=CheckpointType.MODEL_CHECKPOINT,
            )
        curr_step += 1
        if LOCAL_RANK in get_ranks_to_fail():
            if TEST_CASE == "log_faultOnMatch":
                logger.info(os.environ.get("ERROR_MESSAGE"))
            elif TEST_CASE == "slow":
                if restart_count < FAILURE_COUNT:
                    if curr_step < NUM_EPOCHS // 2:
                        logger.info(HEALTHY_LOG)
                    else:
                        logger.info(SLOW_LOG)
                else:
                    logger.info(HEALTHY_LOG)
            elif TEST_CASE == "happy":
                logger.info(HEALTHY_LOG)
            elif TEST_CASE == "sad" and restart_count == 0 and curr_step == 5:
                logger.error(f"[{LOCAL_RANK=}] Triggering IPR for {restart_count=}")
                dummy_trace = f"[{LOCAL_RANK=}] Recoverable failure"
                training_manager.InProcessRestart.hyperpod_send_data(
                    rank=GLOBAL_RANK,
                    data=json.dumps({
                        f"trace_{restart_count=}_{i=}": dummy_trace,
                        f"foo_{restart_count=}_{i=}": "bar",
                        f"step_{restart_count=}_{i=}": str(i),
                    })
                )
                training_manager.InProcessRestart.hyperpod_send_fault(rank=GLOBAL_RANK)
                raise RuntimeError(dummy_trace)
            elif TEST_CASE == "sad" and restart_count == 1 and curr_step == 6:
                logger.error(f"[{LOCAL_RANK=}] Triggering LOCAL_PLR for {restart_count=}")
                dummy_trace = f"[{LOCAL_RANK=}] Recoverable failure"
                training_manager.InProcessRestart.hyperpod_send_data(
                    rank=GLOBAL_RANK,
                    data=json.dumps({
                        f"trace_{restart_count=}_{i=}": dummy_trace,
                        f"foo_{restart_count=}_{i=}": "bar",
                        f"step_{restart_count=}_{i=}": str(i),
                    })
                )
                training_manager.InProcessRestart.hyperpod_send_fault(
                    rank=GLOBAL_RANK,
                    restart_mode=RestartMode.LOCAL_PRL,
                )
                raise RuntimeError(dummy_trace)
            elif TEST_CASE == "sad" and restart_count == 2 and curr_step == 7:
                logger.error(f"[{LOCAL_RANK=}] Triggering GLOBAL_PLR for {restart_count=}")
                dummy_trace = f"[{LOCAL_RANK=}] Recoverable failure"
                training_manager.InProcessRestart.hyperpod_send_data(
                    rank=GLOBAL_RANK,
                    data=json.dumps({
                        f"trace_{restart_count=}_{i=}": dummy_trace,
                        f"foo_{restart_count=}_{i=}": "bar",
                        f"step_{restart_count=}_{i=}": str(i),
                    })
                )
                training_manager.InProcessRestart.hyperpod_send_fault(
                    rank=GLOBAL_RANK,
                    restart_mode=RestartMode.PROCESS_LEVEL_RESTART,
                )
                raise RuntimeError(dummy_trace)
            elif TEST_CASE == "sad" and restart_count == 3 and curr_step == 8:
                # Simulated IPR failure t make sure previous mode is reset
                logger.error(f"[{LOCAL_RANK=}] Triggering IPR for {restart_count=}")
                dummy_trace = f"[{LOCAL_RANK=}] Recoverable failure"
                training_manager.InProcessRestart.hyperpod_send_data(
                    rank=GLOBAL_RANK,
                    data=json.dumps({
                        f"trace_{restart_count=}_{i=}": dummy_trace,
                        f"foo_{restart_count=}_{i=}": "bar",
                        f"step_{restart_count=}_{i=}": str(i),
                    })
                )
                training_manager.InProcessRestart.hyperpod_send_fault(
                    rank=GLOBAL_RANK,
                    restart_mode=RestartMode.IN_PROCESS_RESTART,
                )
                raise RuntimeError(dummy_trace)
        else:
            if TEST_CASE == "happy":
                logger.info(HEALTHY_LOG)

            training_manager.InProcessRestart.hyperpod_send_data(
                rank=GLOBAL_RANK,
                data=json.dumps({f"step_{restart_count=}_{i=}": str(i)})
            )
        if fault_event.is_set():
            logger.warning(
                f"[{LOCAL_RANK=}] Training failed on some other rank. Stopping..."
            )
            barrier_delay = int(os.environ.get("BARRIER_DELAY", 0))
            barrier_delay_ranks_str = os.environ.get("BARRIER_DELAY_RANKS")
            if barrier_delay_ranks_str is not None:
                barrier_delay_ranks = [
                    int(rank) for rank in barrier_delay_ranks_str.split(',')
                    if rank
                ]
                if GLOBAL_RANK not in barrier_delay_ranks:
                    barrier_delay = 0
            if barrier_delay > 0:
                logger.info(
                    f"[{LOCAL_RANK=}] Beginning barrier delay of {barrier_delay} sec..."
                )
                time.sleep(barrier_delay)
            return False
    return True


def monitor(
    training_manager: TrainingManager,
    fault_event: threading.Event,
):
    while True:
        logger.info(f"[{LOCAL_RANK=}] Waiting for fault messages...")
        _, restart_data = training_manager.InProcessRestart.hyperpod_wait_fault(
        )
        logger.info(
            f"[{LOCAL_RANK=}] Received fault for {restart_data=}. Stopping training..."
        )
        fault_event.set()


def ranking(training_manager: TrainingManager, ):
    global GLOBAL_RANK
    while True:
        logger.info(f"[{LOCAL_RANK=}] Waiting for rank info messages...")
        _, rank_info = training_manager.InProcessRestart.hyperpod_wait_rank_info(
        )
        logger.info(
            f"[{LOCAL_RANK=}] Received {rank_info=}. Updating process...")
        envs = rank_info["worker_envs"]
        GLOBAL_RANK = int(envs["RANK"])
        NUM_PP_GROUPS = int(os.environ.get("NUM_PP_GROUPS", 1))
        training_manager.InProcessRestart.hyperpod_notify_labels(
            labels={
                "PP": str(GLOBAL_RANK % NUM_PP_GROUPS),
                "TP": "2"
            },
        )


def dummy_train():
    logger.info(f"[{LOCAL_RANK=}] Training script started")
    training_manager = TrainingManager()

    fault_event = threading.Event()
    monitor_thread = threading.Thread(
        target=monitor,
        args=(
            training_manager,
            fault_event,
        ),
        daemon=True,
    )
    monitor_thread.start()
    ranking_thread = threading.Thread(
        target=ranking,
        args=(training_manager, ),
        daemon=True,
    )
    ranking_thread.start()

    retry_cnt, max_retry = 0, 5
    success = False

    # 2 checkpoint client to test multiple clients/rank
    ckpt_clients = []
    for i in range(2):
        ckpt_client = TrainingManager.get_checkpoint_discovery_client(
            prefix=f"test_prefix",
            num_model_checkpoints=4,
        )
        ckpt_clients.append(ckpt_client)

    while retry_cnt < max_retry:
        try:
            success = step(
                training_manager=training_manager,
                fault_event=fault_event,
                ckpt_clients=ckpt_clients,
            )
            fault_event.clear()
            if success:
                logger.info(f"[{LOCAL_RANK=}] Training succeeded. Exiting")
                return
            # else: Failure on another node
        except RuntimeError:
            logger.error(
                f"[{LOCAL_RANK=}] Recoverable failure on {GLOBAL_RANK=} for {restart_count=}. Returning to RCB barrier"
            )
        retry_cnt += 1
    if not success:
        # Failed after max retries
        raise RuntimeError(f"[{LOCAL_RANK=}] PLR failure after max_retries")


if __name__ == "__main__":
    """
    Docker script to test IPR
    1. Create the wheel
    2. Copy whl to docker folder
    3. Build container
    4. Run the docker container
    5. You should see logs "At RCB barrier. Waiting for server signal to proceed..." from all 4 ranks.
       At this point the worker processes are at the RCB barrier. You can see the status is READY
    6. Signal the start using the following command
    7. The ranks should start running. Wait until we get step 6 is complete
    8. Send a stop signal to tell this agent that there was a failure on the cluster
    9. All the ranks should stop and go back to the RCB barrier waiting for a start signal
    10. Send a start with `{"checkpointVersion": 3}`, the logs should show "Starting training with ckpt_step 3"
    ```
    $ rm -rf build/hyperpod_elastic_agent-* && brazil-build build
    $ cd docker && rm -rf hyperpod_elastic_agent-*
    $ cp ../build/hyperpod_elastic_agent-*.whl .
    $ docker build -t ipr:latest -f ipr.Dockerfile .
    $ docker run --rm -it --network=host -e AGENT_HOST=:: ipr:latest
    $ curl -s \[::\]:8080/status | jq .
    {
      "status": "ready",
      "transitions": {
        "INIT": "2025-03-10T21:16:31.744344+00:00",
        "READY": "2025-03-10T21:16:34.204004+00:00"
      }
    }
    $ curl -X POST \
           -d '{"rank": 0, "nnodes": 1, "faultCount": 0, "master_addr": "::", "master_port": "23456", "rankIps": [{"rank": 0, "ip": "10.1.177.33"}], "ipVersion": "2025-01-10T13:00:00Z", "progress": {"checkpointProgress": {"progressCount": 1, "progressData": "test_path_1"}}}' \
           http://\[::\]:8080/start
    ### Wait until ranks 2 and 3 fail
    $ curl -X POST http://\[::\]:8080/stop
    ### There should be failures from rank 2 and 3
    $ curl -s \[::\]:8080/status | jq .
    {
      "status": "faulted",
      "transitions": {
        "INIT": "2025-04-10T19:02:24.370030+00:00",
        "READY": "2025-04-10T19:03:04.094517+00:00",
        "RUNNING": "2025-04-10T19:03:21.467508+00:00",
        "STOPPING": "2025-04-10T19:02:59.149696+00:00",
        "FAULTED": "2025-04-10T19:03:26.938813+00:00"
      },
      "reason": "ProcessStateFailure_Ranks2-3",
      "aggregate_worker_data": [
        {
          "rank": 2,
          "group_rank": 0,
          "local_rank": 2,
          "data": {
            "trace": "[LOCAL_RANK=2] Recoverable failure",
            "foo": "bar",
            "step": "0"
          }
        },
        {
          "rank": 3,
          "group_rank": 0,
          "local_rank": 3,
          "data": {
            "trace": "[LOCAL_RANK=3] Recoverable failure",
            "foo": "bar",
            "step": "0"
          }
        }
      ],
      "ipversion": "2025-01-10T13:00:00Z",
      "progress": {
        "checkpointProgress": {
          "progressData": "test_path_3",
          "progressCount": 3
        }
      },
      "agent_version": "1.1.20250410190153",
      "assigned_rank": "0",
      "spare": "False"
    }
    ```
    $ curl -X POST \
           -d '{"rank": 0, "nnodes": 1, "faultCount": 2, "master_addr": "::", "master_port": "23456", "rankIps": [{"rank": 0, "ip": "10.1.177.33"}], "ipVersion": "2025-01-10T13:00:00Z", "progress": {"checkpointProgress": {"progressCount": 3, "progressData": "test_path_3"}}, "aggregate_worker_data": [{"group_rank": 0, "rank": 0, "local_rank": 0, "data": {"trace": "failed0"}}, {"group_rank": 0, "rank": 1, "local_rank": 1, "data": {"trace": "failed1"}}]}' \
           http://\[::\]:8080/start
    ### Should log something like
    ### ... [LOCAL_RANK=3] Received start from Agent with envs={'RANK': '3', ... 'TORCHELASTIC_RESTART_COUNT': '2'}, aggregate_worker_data=[{'group_rank': 0, 'rank': 0, 'local_rank': 0, 'data': {'trace': 'failed0'}}, {'group_rank': 0, 'rank': 1, 'local_rank': 1, 'data': {'trace': 'failed1'}}]
    """
    dummy_train()