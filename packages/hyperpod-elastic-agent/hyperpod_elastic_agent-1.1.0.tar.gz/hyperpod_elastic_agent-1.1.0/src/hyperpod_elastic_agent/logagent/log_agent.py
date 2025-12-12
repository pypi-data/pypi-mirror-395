import logging
import os
import re
import tempfile
import time

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class LogState(Enum):
    """
    Enum representing the different states of logging

    WAITING: Waiting for the log agent to start or first log line to be emitted
    HEALTHY: The logging is within expectation
    SLOW: The logging metrics are out of expectation, indicating a slow job
    HANGING: No log has been received for a long time, indicating a hanging job
    FAULTED: A critical error pattern was matched in the logs, indicating immediate fault
    """
    WAITING = "WAITING"
    HEALTHY = "HEALTHY"
    SLOW = "SLOW"
    HANGING = "HANGING"
    FAULTED = "FAULTED"


@dataclass
class LogEvalResult:
    log_state: LogState = LogState.WAITING
    rule_name_log_line: Optional[Dict[str, Optional[str]]] = None

    def __post_init__(self):
        if self.log_state in {LogState.HANGING, LogState.SLOW, LogState.FAULTED} and not self.rule_name_log_line:
            raise RuntimeError(f"LogEvalResult.rule_name_log_line must be set if LogEvalResult.log_state is SLOW, HANGING, or FAULTED")


LOGSTATE_TRANSITIONS = {
    LogState.WAITING: {LogState.HEALTHY, LogState.SLOW, LogState.HANGING, LogState.FAULTED},
    LogState.HEALTHY: {LogState.SLOW, LogState.HANGING, LogState.FAULTED},
    LogState.SLOW: {LogState.HEALTHY, LogState.HANGING, LogState.FAULTED},
    LogState.HANGING: {LogState.HEALTHY, LogState.SLOW, LogState.FAULTED}
}


class LogEvaluator(object):
    """ Rule for evaluating job status using logs """

    OPERATOR_SET = {"gt", "lt", "eq", "gteq", "lteq"}

    def __init__(self, rule: Dict[str, str]) -> None:
        """ Initialize from a configuration dict, the configuration should have the following fields:

            name [Required]: name of the rule 
            logPattern [Required]: Regex to identify log lines to apply the rule to and extract metric value
            expectedStartCutOffInSeconds [Optional]: Time to first match for LogPattern, beyond which the rule evaluates to HANGING
            expectedRecurringFrequencyInSeconds [Optional]: Time interval between two subsequent matches for LogPattern, beyond which the rule evaluates to HANGING
            stopPattern [Optional]: Regex to identify the log line at which to deactivate the rule
            metricThreshold [Optional]: Threshold for value extracted by logPattern
            operator [Optional]: Operator to compare the value extracted by LogPattern to metricThreshold
            metricEvaluationDataPoints [Optional]: The number of consecutive times that the rule must evaluate to SLOW in order to mark the job as SLOW
            faultOnMatch [Optional]: When true, the rule will evaluate to FAULTED as soon as the LogPattern is matched
        """
        self.name = rule["name"]
        self.log_pattern = re.compile(rule["logPattern"])
        self.start_cutoff = int(
            rule["expectedStartCutOffInSeconds"]) if "expectedStartCutOffInSeconds" in rule else None
        self.recurring_frequency = int(
            rule["expectedRecurringFrequencyInSeconds"]) if "expectedRecurringFrequencyInSeconds" in rule else None
        self.stop_pattern = re.compile(
            rule["stopPattern"]) if "stopPattern" in rule else None
        self.metric_threshold = int(
            rule["metricThreshold"]) if "metricThreshold" in rule else None
        self.operator = rule.get("operator")
        self.evaluation_count = int(rule.get("metricEvaluationDataPoints", 1))
        self.fault_on_match = rule.get("faultOnMatch", False)

        self._active = True
        self._start_timestamp = time.time()
        self._log_pattern_match_line: Optional[str] = None
        self._log_pattern_match_timestamp: Optional[float] = None
        self._slow_count = 0
        self._state = LogState.WAITING
        self._last_suspend_time: Optional[float] = None
        self._total_idle_time = 0.0

        assert self.name, "Rule name should be specified"
        assert self.log_pattern, "Log pattern should be specified"
        assert self.operator in self.OPERATOR_SET if self.operator else True, f"Invalid operator {self.operator}, should be one of {self.OPERATOR_SET}"

    def suspend(self) -> None:
        if self._last_suspend_time is None:
            self._last_suspend_time = time.time()

    def resume(self) -> None:
        if self._last_suspend_time is not None:
            self._total_idle_time += time.time() - self._last_suspend_time
            self._last_suspend_time = None

    def _get_effective_time(self, timestamp: float) -> float:
        return timestamp - self._total_idle_time

    def evaluate(self, line: Optional[str] = None) -> Tuple[LogState, Optional[str]]:
        """ Evaluate the log against the rule, return LogState """
        if not self._active:
            self._state = LogState.HEALTHY
            return self._state, self._log_pattern_match_line

        current_timestamp = self._get_effective_time(time.time())

        log_pattern_match = self.log_pattern.match(
            line) if line is not None else None
        if log_pattern_match:
            self._log_pattern_match_line = line
            self._log_pattern_match_timestamp = current_timestamp
            # Check for immediate fault condition
            if self.fault_on_match:
                self._state = LogState.FAULTED
                return self._state, self._log_pattern_match_line

        if (line is not None
                and self.stop_pattern
                and self.stop_pattern.match(line)):
            self._active = False
            self._state = LogState.HEALTHY
            return self._state, self._log_pattern_match_line

        if (self.start_cutoff is not None
                and not self._log_pattern_match_timestamp
                and current_timestamp - self._start_timestamp > self.start_cutoff):
            self._state = LogState.HANGING
            return self._state, self._log_pattern_match_line

        if (self.recurring_frequency is not None
                and self._log_pattern_match_timestamp
                and current_timestamp - self._log_pattern_match_timestamp > self.recurring_frequency):
            self._state = LogState.HANGING
            return self._state, self._log_pattern_match_line

        if log_pattern_match is None:
            return self._state, self._log_pattern_match_line

        if (not log_pattern_match.groups()
                or self.metric_threshold is None
                or self.operator is None):
            self._state = LogState.HEALTHY
            return self._state, self._log_pattern_match_line

        metric_value = float(log_pattern_match.group(1))
        if ((self.operator == "gt" and metric_value > self.metric_threshold)
                or (self.operator == "lt" and metric_value < self.metric_threshold)
                or (self.operator == "eq" and metric_value == self.metric_threshold)
                or (self.operator == "gteq" and metric_value >= self.metric_threshold)
                or (self.operator == "lteq" and metric_value <= self.metric_threshold)):
            self._slow_count = self._slow_count + \
                1 if self._slow_count < self.evaluation_count else self._slow_count
        else:
            self._slow_count = 0

        if self._slow_count >= self.evaluation_count:
            self._state = LogState.SLOW
            return self._state, self._log_pattern_match_line

        self._state = LogState.HEALTHY
        return self._state, self._log_pattern_match_line


class LogAgent(object):
    """ 
    Log agent class to monitor logs from workers
    """

    READ_INTERVAL = 1

    def __init__(self, local_world_size: int) -> None:
        self._local_world_size = local_world_size
        self._monitor_thread_pool: Optional[ThreadPoolExecutor] = None
        self._futures: List[Future] = []
        self._stop_signaled = False
        self._evaluators: Dict[int, List[LogEvaluator]] = {}
        self._log_eval_results = [
            LogEvalResult() for _ in range(self._local_world_size)
        ]

        # Write log agent logs to a separate file
        self._logger = logging.getLogger("Log Agent")
        self._logger.setLevel(os.environ.get("LOGLEVEL", logging.INFO))

        with tempfile.NamedTemporaryFile(prefix="log_agent_",
                                         suffix=".log") as temp_file:
            self._log_agent_log_file = temp_file.name

        file_handler = logging.FileHandler(self._log_agent_log_file)
        file_handler.setLevel(os.environ.get("LOGLEVEL", logging.INFO))
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self._logger.addHandler(file_handler)

        self._logger.info(
            f"Log agent is ready, log agent logs will be saved to {self._log_agent_log_file}"
        )

    @property
    def log_state(self) -> List[LogState]:
        """ Return a list of size `local_world_size`, where index i store log state of local rank i """
        return [item.log_state for item in self._log_eval_results]

    @property
    def log_eval_results(self) -> List[LogEvalResult]:
        """ Return a list of size `local_world_size`, where index i store LogEvalResult of local rank i """
        return self._log_eval_results

    def is_running(self) -> bool:
        return self._monitor_thread_pool is not None and any(
            [f.running() for f in self._futures])

    def start(
        self,
        attempt_dir: str,
        local_ranks_filter: Optional[Set[int]] = None,
        log_monitoring_configuration: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        self.stop()
        self._stop_signaled = False

        # Log Agent currently does not support dynamic updates to log monitoring configuration
        if log_monitoring_configuration and not self._evaluators:
            try:
                self._evaluators = {
                    local_rank: [LogEvaluator(rule) for rule in log_monitoring_configuration]
                    for local_rank in range(self._local_world_size)
                }
            except Exception as e:
                self._logger.error(
                    f"Failed to load Log Monitoring Configuration: {e}",)

        if not self._evaluators:
            self._logger.info(
                "Not starting Log Agent since Log Monitoring Configuration is empty")
            return

        for local_rank in self._evaluators:
            for evaluator in self._evaluators[local_rank]:
                evaluator.resume()

        self._monitor_thread_pool = ThreadPoolExecutor(
            max_workers=self._local_world_size)
        self._futures = [
            self._monitor_thread_pool.submit(
                self._monitor_log_loop, local_rank, attempt_dir)
            for local_rank in range(self._local_world_size)
            if local_ranks_filter is None or local_rank in local_ranks_filter
        ]

        if self._futures:
            self._logger.info("Log agent started")
        else:
            self._logger.error(
                f"Log agent failed to start, see {self._log_agent_log_file} for running details"
            )

    def stop(self, clear_log_monitoring_configuration=False) -> None:
        self._stop_signaled = True

        if self._monitor_thread_pool:
            self._logger.info("Stopping log agent")
            self._monitor_thread_pool.shutdown(wait=True, cancel_futures=True)
            self._monitor_thread_pool = None
            self._futures = []

        for i in range(self._local_world_size):
            self._log_eval_results[i].log_state = LogState.WAITING
            self._log_eval_results[i].rule_name_log_line = None

        if self._evaluators:
            if clear_log_monitoring_configuration:
                self._logger.info("Clearing log monitoring configuration")
                self._evaluators = {}
            else:
                for local_rank in self._evaluators:
                    for evaluator in self._evaluators[local_rank]:
                        evaluator.suspend()

    def _set_log_state(
        self,
        new_state: LogState,
        local_rank: int,
        rule_name_log_line: Optional[Dict[str, Optional[str]]] = None,
    ) -> None:
        log_state = self.log_state[local_rank]
        if log_state == new_state:
            return

        if new_state not in LOGSTATE_TRANSITIONS[log_state]:
            raise ValueError(
                f"Invalid state transition from {log_state} to {new_state}")

        self._logger.info(
            f"Rank {local_rank}: Log agent state changed from {log_state} to {new_state} due to rules: {rule_name_log_line}"
        )
        self._log_eval_results[local_rank].log_state = new_state
        self._log_eval_results[local_rank].rule_name_log_line = rule_name_log_line

    def _monitor_log_loop(self, local_rank: int, attempt_dir: str) -> None:
        """ Continuously reading the log file and updating the states accordingly """
        log_path = os.path.join(attempt_dir, str(local_rank), "stdout.log")
        self._logger.info(f"Monitoring log file {log_path}")

        # Wait for the training process to create log file
        self._logger.debug(f"Waiting for rank {local_rank} log file to be created: {log_path}")
        while not self._stop_signaled and not os.path.exists(log_path):
            log_state_dict: dict[LogState, dict[str, Optional[str]]] = defaultdict(dict[str, Optional[str]])
            for rule in self._evaluators[local_rank]:
                evaluation_result, log_line = rule.evaluate()
                log_state_dict[evaluation_result][rule.name] = log_line
            if LogState.FAULTED in log_state_dict.keys():
                self._logger.info(
                    "Faulted job detected when waiting for log file to be created"
                )
                self._set_log_state(LogState.FAULTED, local_rank,
                                    log_state_dict[LogState.FAULTED])
            elif LogState.HANGING in log_state_dict.keys():
                self._logger.info(
                    "Hanging job detected when waiting for log file to be created"
                )
                self._set_log_state(LogState.HANGING, local_rank,
                                    log_state_dict[LogState.HANGING])
            time.sleep(self.READ_INTERVAL)
        self._logger.debug(f"Found rank {local_rank} log file: {log_path}")

        if self._stop_signaled:
            return

        with open(log_path, "r") as f:
            while not self._stop_signaled:
                line = f.readline()
                if line:
                    self._logger.debug(f"Read line from rank {local_rank} log: {line}")
                try:
                    log_state_dict = defaultdict(dict[str, Optional[str]])
                    for rule in self._evaluators[local_rank]:
                        evaluation_result, log_line = rule.evaluate(line)
                        log_state_dict[evaluation_result][rule.name] = log_line
                    if line:
                        self._logger.debug(f"Log evaluator status for rank {local_rank}: {log_state_dict}")
                except Exception as e:
                    self._logger.error(
                        f"Failed to evaluate log line: {line}, Error: {e}")
                    continue

                if LogState.FAULTED in log_state_dict.keys():
                    self._set_log_state(LogState.FAULTED, local_rank,
                                        log_state_dict[LogState.FAULTED])
                elif LogState.HANGING in log_state_dict.keys():
                    self._set_log_state(LogState.HANGING, local_rank,
                                        log_state_dict[LogState.HANGING])
                elif LogState.SLOW in log_state_dict.keys():
                    self._set_log_state(LogState.SLOW, local_rank,
                                        log_state_dict[LogState.SLOW])
                elif LogState.HEALTHY in log_state_dict.keys():
                    self._set_log_state(LogState.HEALTHY, local_rank,
                                        log_state_dict[LogState.HEALTHY])
                else:
                    self._set_log_state(LogState.WAITING, local_rank,
                                        log_state_dict[LogState.WAITING])

                if not line:
                    time.sleep(self.READ_INTERVAL)

    @staticmethod
    def compute_attempt_dir(run_log_dir, attempt_num):
        """ Compute the log file path from log directory and attempt number.
            The log path should have the following format

            <run_log_dir>/attempt_<attempt_num>/0/stdout.log

            The log_dir should be found in the LogsSpecs: log_specs._run_log_dir
        """

        attempt_dir = os.path.join(run_log_dir, f"attempt_{attempt_num}")

        return attempt_dir