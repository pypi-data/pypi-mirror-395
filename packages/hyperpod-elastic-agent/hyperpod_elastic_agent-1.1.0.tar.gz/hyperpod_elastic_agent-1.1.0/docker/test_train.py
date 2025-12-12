import logging
import os
import sys
import time
from typing import List

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.INFO,
                    stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

HEALTHY_LOG = "Training model, speed: 1000 TFLOPs..."
SLOW_LOG = "Training model, speed: 1 TFLOPs..."


def get_ranks_to_fail() -> List[int]:
    # Fail for rank 2 by default
    fail_ranks_str = os.environ.get("FAIL_RANKS", "2,")
    fail_ranks = [int(rank) for rank in fail_ranks_str.split(',') if rank]
    return fail_ranks


def dummy_train():
    rank = int(os.environ["RANK"])
    logger.info(f"[Rank={rank}] Training script started")
    fail_ranks = get_ranks_to_fail()
    test_case = os.environ.get("TEST_CASE", "sad")
    sleep_time = int(os.environ.get("TEST_SLEEP_TIME", "10"))
    failure_count = int(os.environ.get("FAILURE_COUNT", 1))
    current_retry_count = int(os.environ.get("TORCHELASTIC_RESTART_COUNT",
                                             "1"))
    error_message = os.environ.get("ERROR_MESSAGE")
    num_logs = 10
    log_interval = sleep_time / num_logs

    if rank in fail_ranks and test_case == "log_faultOnMatch" :
        logger.info(error_message)

    if rank in fail_ranks and test_case == "slow" and current_retry_count < failure_count:
        logger.info(
            f"[Rank={rank}] Current Retry count {current_retry_count}/{failure_count}"
        )

        event_time = max(num_logs // 2, 2)
        for _ in range(event_time):
            logger.info(HEALTHY_LOG)
            time.sleep(log_interval)

        for _ in range(num_logs - event_time):
            logger.info(SLOW_LOG)
            time.sleep(log_interval)

    else:
        logger.info(f"[Rank={rank}] Setting sleep time to {sleep_time}s")
        for _ in range(num_logs):
            logger.info(HEALTHY_LOG)
            time.sleep(log_interval)

    # Default value of test_case is "sad" and fail_ranks = [2]
    if rank in fail_ranks and test_case == "sad" and current_retry_count < failure_count:
        logger.info(
            f"[Rank={rank}] Current Retry count {current_retry_count}/{failure_count}"
        )
        logger.error(f"[Rank={rank}] Failing dummy training script")
        raise ValueError("Failing dummy training script")
    else:
        logger.info(f"[Rank={rank}] Training script successful")


if __name__ == "__main__":
    dummy_train()
