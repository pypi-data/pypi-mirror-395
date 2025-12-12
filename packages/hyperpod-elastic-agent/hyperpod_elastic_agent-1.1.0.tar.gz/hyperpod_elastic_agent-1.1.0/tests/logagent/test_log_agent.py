import time
import os
import tempfile
import pytest
import random
import uuid

from hyperpod_elastic_agent.util import retry
from hyperpod_elastic_agent.logagent.log_agent import LogAgent, LogState, LogEvaluator


class TestLogEvaluator(object):

    def test_without_threshold(self):
        # Match case 1
        rule = {
            'name': 'testRule',
            'logPattern': '.*',
        }
        input_cases = [
            "this is any log", "another random log that should be match"
        ]
        evaluator = LogEvaluator(rule)
        for log in input_cases:
            log_state, log_line = evaluator.evaluate(log)
            assert log_state == LogState.HEALTHY
            assert log_line == log

        # Match case 2
        rule = {
            'name': 'testRule',
            'logPattern': '.+ (.+) TFLOPs.*',
        }
        input_cases = [
            "current throughput 12.5 TFLOPs",
            "training speed: 22.1 TFLOPs, 1.8 seconds per iteration"
        ]
        evaluator = LogEvaluator(rule)
        for log in input_cases:
            log_state, log_line = evaluator.evaluate(log)
            assert log_state == LogState.HEALTHY
            assert log_line == log

        # Not match case 1
        rule = {
            'name': 'testRule',
            'logPattern': '.+ (.+) TFLOPs.*',
            'expectedStartCutOffInSeconds': 1,
        }
        input_cases = [
            "doing rendezvous...", "training speed: 1.8 seconds per iteration"
        ]

        evaluator = LogEvaluator(rule)
        time.sleep(rule["expectedStartCutOffInSeconds"] + 1)
        for log in input_cases:
            log_state, log_line = evaluator.evaluate(log)
            assert log_state == LogState.HANGING
            assert log_line == None

        # Not match case 2
        rule = {
            'name': 'testRule',
            'logPattern': '.+ (.+) TFLOPs.*',
            'expectedRecurringFrequencyInSeconds': 1,
        }
        input_cases = ["doing rendezvous...", "current throughput 12.5 TFLOPs"]

        evaluator = LogEvaluator(rule)
        log_state, log_line = evaluator.evaluate(input_cases[0])
        assert log_state == LogState.WAITING
        assert log_line == None
        log_state, log_line = evaluator.evaluate(input_cases[1])
        assert log_state == LogState.HEALTHY
        assert log_line == input_cases[1]

        time.sleep(rule["expectedRecurringFrequencyInSeconds"] + 1)

        log_state, log_line = evaluator.evaluate(input_cases[0])
        assert log_state == LogState.HANGING
        assert log_line == input_cases[1]
        log_state, log_line = evaluator.evaluate(input_cases[1])
        assert log_state == LogState.HEALTHY
        assert log_line == input_cases[1]

    def test_with_threshold(self):
        # Match case 1
        threshold = 10
        rule = {
            "name": "TFLOPs",
            'logPattern': '.+ (.+) TFLOPs.*',
            'metricThreshold': threshold,
            "operator": "lt"
        }
        evaluator = LogEvaluator(rule)
        for _ in range(100):
            random_tflops = random.gauss(rule["metricThreshold"], 2)
            random_tflops = round(random_tflops, 2)
            log = f"training speed: {random_tflops:.2f} TFLOPs"

            is_slow = random_tflops < rule["metricThreshold"]
            log_state, log_line = evaluator.evaluate(log)
            assert log_state == LogState.SLOW if is_slow else log_state == LogState.HEALTHY, f"{random_tflops=}, {threshold=}, {is_slow=}, {log_state=}"
            assert log_line == log

    def test_with_fault_on_match(self):
        # Test immediate fault on match
        rule = {
            "name": "OutOfMemoryError",
            'logPattern': '.*OutOfMemoryError.*',
            'faultOnMatch': True
        }
        evaluator = LogEvaluator(rule)

        # Test with non-matching log
        log_state, log_line = evaluator.evaluate(
            "Training is proceeding normally")
        assert log_state == LogState.WAITING
        assert log_line == None

        # Test with matching log
        log_state, log_line = evaluator.evaluate(
            "OutOfMemoryError: Unable to allocate memory")
        assert log_state == LogState.FAULTED
        assert log_line == "OutOfMemoryError: Unable to allocate memory"

        # Test with another non-matching log after fault
        log_state, log_line = evaluator.evaluate(
            "Training is proceeding normally")
        assert log_state == LogState.FAULTED, "State should remain FAULTED after match"
        assert log_line == "OutOfMemoryError: Unable to allocate memory"

        # Test with rule that has both faultOnMatch and other parameters
        rule = {
            "name": "OutOfMemoryError",
            'logPattern': '.*OutOfMemoryError.*',
            'faultOnMatch': True,
            'metricThreshold': 10,
            'operator': 'lt',
            'expectedRecurringFrequencyInSeconds': 5
        }
        evaluator = LogEvaluator(rule)

        # Test with matching log - should fault immediately regardless of other parameters
        log_state, log_line = evaluator.evaluate(
            "OutOfMemoryError: Unable to allocate memory")
        assert log_state == LogState.FAULTED
        assert log_line == "OutOfMemoryError: Unable to allocate memory"

    def test_log_evaluator_suspend_resume_timing(self):
        """Test LogEvaluator suspend/resume timing calculations directly"""
        hanging_threshold = 2
        rule = {
            'name': 'testRule',
            'logPattern': '.* (.+) TFLOPs.*',
            'expectedStartCutOffInSeconds': hanging_threshold,
            'expectedRecurringFrequencyInSeconds': hanging_threshold,
        }

        evaluator = LogEvaluator(rule)

        # Initially should be waiting
        log_state, log_line = evaluator.evaluate()
        assert log_state == LogState.WAITING
        assert log_line is None

        # Provide a matching log
        log_state, log_line = evaluator.evaluate("training speed: 120 TFLOPs")
        assert log_state == LogState.HEALTHY
        assert log_line == "training speed: 120 TFLOPs"

        # Suspend the evaluator
        evaluator.suspend()

        # Wait longer than hanging threshold while suspended
        time.sleep(hanging_threshold + 0.5)

        # Resume the evaluator
        evaluator.resume()

        # Should still be healthy because suspended time doesn't count
        log_state, log_line = evaluator.evaluate("some other log")
        assert log_state == LogState.HEALTHY
        assert log_line == "training speed: 120 TFLOPs"

        # Now wait for hanging threshold after resume
        time.sleep(hanging_threshold + 0.5)

        # Should now detect hanging
        log_state, log_line = evaluator.evaluate("some other log")
        assert log_state == LogState.HANGING
        assert log_line == "training speed: 120 TFLOPs"

    def test_log_evaluator_multiple_suspend_resume_cycles(self):
        """Test multiple suspend/resume cycles accumulate idle time correctly"""
        hanging_threshold = 1
        rule = {
            'name': 'testRule',
            'logPattern': '.* (.+) TFLOPs.*',
            'expectedRecurringFrequencyInSeconds': hanging_threshold,
        }

        evaluator = LogEvaluator(rule)

        # Provide initial matching log
        log_state, log_line = evaluator.evaluate("training speed: 120 TFLOPs")
        assert log_state == LogState.HEALTHY

        # Multiple suspend/resume cycles
        for i in range(3):
            evaluator.suspend()
            suspend_duration = 0.5
            time.sleep(suspend_duration)
            evaluator.resume()

            # Should still be healthy after each resume
            log_state, _ = evaluator.evaluate("some other log")
            assert log_state == LogState.HEALTHY

        # Now wait for the actual hanging threshold
        time.sleep(hanging_threshold + 0.1)

        # Should detect hanging now
        log_state, _ = evaluator.evaluate("some other log")
        assert log_state == LogState.HANGING

    def test_log_evaluator_suspend_resume_with_start_cutoff(self):
        """Test suspend/resume with expectedStartCutOffInSeconds"""
        start_cutoff = 2
        rule = {
            'name': 'testRule',
            'logPattern': '.* (.+) TFLOPs.*',
            'expectedStartCutOffInSeconds': start_cutoff,
        }

        evaluator = LogEvaluator(rule)

        # Suspend immediately after creation
        evaluator.suspend()

        # Wait longer than start cutoff while suspended
        time.sleep(start_cutoff + 0.5)

        # Resume
        evaluator.resume()

        # Should still be waiting, not hanging, because suspended time doesn't count
        log_state, log_line = evaluator.evaluate()
        assert log_state == LogState.WAITING
        assert log_line is None

        # Now wait for the actual start cutoff after resume
        time.sleep(start_cutoff + 0.1)

        # Should detect hanging now
        log_state, log_line = evaluator.evaluate()
        assert log_state == LogState.HANGING
        assert log_line is None

    def test_log_evaluator_nested_suspend_resume(self):
        """Test nested suspend/resume calls"""
        rule = {
            'name': 'testRule',
            'logPattern': '.* (.+) TFLOPs.*',
            'expectedRecurringFrequencyInSeconds': 2,
        }

        evaluator = LogEvaluator(rule)

        # Provide initial matching log
        log_state, log_line = evaluator.evaluate("training speed: 120 TFLOPs")
        assert log_state == LogState.HEALTHY

        # Multiple suspend calls
        evaluator.suspend()
        evaluator.suspend()  # Second suspend should not cause issues

        time.sleep(1.2)

        # Single resume should handle multiple suspends
        evaluator.resume()

        # Should still be healthy because suspended time doesn't count
        log_state, log_line = evaluator.evaluate("some other log")
        assert log_state == LogState.HEALTHY

        # Multiple resume calls should not cause issues
        evaluator.resume()
        evaluator.resume()

        # Should still work normally
        log_state, log_line = evaluator.evaluate("training speed: 130 TFLOPs")
        assert log_state == LogState.HEALTHY


class TestLogAgent(object):

    @pytest.fixture
    def hanging_threshold(self):
        return 5

    @pytest.fixture
    def tflops_threshold(self):
        return 100

    @pytest.fixture
    def iterations_threshold(self):
        return 5

    @pytest.fixture
    def log_agent_config(self, hanging_threshold, tflops_threshold,
                         iterations_threshold):
        return [{
            "name": "TFLOPs",
            "logPattern": ".* (.+) TFLOPs.*",
            "expectedStartCutOffInSeconds": hanging_threshold,
            "expectedRecurringFrequencyInSeconds": hanging_threshold,
            "metricThreshold": tflops_threshold,
            "operator": "lt"
        }, {
            "name": "iterations/s",
            "logPattern": ".* (.+) iterations/s.*",
            "metricThreshold": iterations_threshold,
            "operator": "lt"
        }]

    @pytest.fixture
    def local_world_size(self):
        return 8

    def test_log_agent_no_config(self, local_world_size):
        log_agent = LogAgent(local_world_size)
        assert not log_agent.is_running()

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

    def test_log_agent_log_file_does_not_exist(self, local_world_size,
                                               log_agent_config,
                                               hanging_threshold):

        log_path = str(uuid.uuid4())
        log_agent = LogAgent(local_world_size)

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        log_agent.start(log_path,
                        log_monitoring_configuration=log_agent_config)
        validate_agent_running(log_agent)

        validate_agent_log_state(log_agent,
                                 [LogState.HANGING] * local_world_size)

        log_agent.stop()
        assert not log_agent.is_running()

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

    def test_log_agent_slow_job(self, local_world_size, log_agent_config):

        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size=local_world_size)
        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        log_agent.start(attempt_dir.name,
                        log_monitoring_configuration=log_agent_config)
        validate_agent_running(log_agent)

        for rank in range(local_world_size):
            fds[rank].write("Start training process...\n")
            fds[rank].write("training speed: 50 TFLOPs...\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent, [LogState.SLOW] * local_world_size)

        log_agent.stop()
        assert not log_agent.is_running()

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_hanging_job(self, local_world_size, log_agent_config,
                                   hanging_threshold):
        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        log_agent.start(attempt_dir.name,
                        log_monitoring_configuration=log_agent_config)
        validate_agent_running(log_agent)

        for rank in range(local_world_size):
            fds[rank].write("Start training process...\n")
            fds[rank].write("training speed: 50 TFLOPs...\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent,
                                 [LogState.HANGING] * local_world_size)

        log_agent.stop()
        assert not log_agent.is_running()

        validate_agent_log_state(log_agent,
                                 [LogState.WAITING] * local_world_size)

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_healthy_job(self, local_world_size, log_agent_config,
                                   tflops_threshold):
        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)
        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        log_agent.start(attempt_dir.name,
                        log_monitoring_configuration=log_agent_config)
        validate_agent_running(log_agent)

        for rank in range(local_world_size):
            fds[rank].write("Start training process...\n")
            fds[rank].write(
                f"training speed: {tflops_threshold + 1} TFLOPs...\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent,
                                 [LogState.HEALTHY] * local_world_size)

        log_agent.stop()
        assert not log_agent.is_running()

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_change_attempt_directory(self, local_world_size):
        log_monitoring_configuration = [
            {
                "name": "pretrain",
                "logPattern": ".*Start data loading.*",
                "stopPattern": ".*Start training.*",
                "expectedStartCutOffInSeconds": 60,
            },
            {
                "name": "train",
                "logPattern": ".* (.+) TFLOPs.*",
                "stopPattern": ".*Training complete.*",
                "expectedStartCutOffInSeconds": 120,
                "expectedRecurringFrequencyInSeconds": 30,
                "metricThreshold": 100,
                "operator": "lt",
                "metricEvaluationDataPoints": 1
            },
            {
                "name": "posttrain",
                "logPattern": ".*Saving data*",
                "expectedStartCutOffInSeconds": 180
            },
        ]

        log_agent = LogAgent(local_world_size)
        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        # Pretrain script logs monitoring
        pretrain_attempt_dir = tempfile.TemporaryDirectory(prefix="pretrain")
        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(pretrain_attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent.start(pretrain_attempt_dir.name, {0},
                        log_monitoring_configuration)
        validate_agent_running(log_agent)

        fds[0].write("Start data loading...\n")
        fds[0].flush()

        validate_agent_log_state(log_agent, [LogState.HEALTHY] +
                                 [LogState.WAITING] * (local_world_size - 1))

        for fd in fds:
            fd.close()

        # Training script logs monitoring
        train_attempt_dir = tempfile.TemporaryDirectory(prefix="train")
        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(train_attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent.start(train_attempt_dir.name, {0},
                        log_monitoring_configuration)
        validate_agent_running(log_agent)
        validate_agent_log_state(log_agent, [LogState.HEALTHY] +
                                 [LogState.WAITING] * (local_world_size - 1))

        fds[0].write("Start training...\n")
        fds[0].write("training speed: 120 TFLOPs...\n")
        fds[0].flush()

        validate_agent_log_state(log_agent, [LogState.HEALTHY] +
                                 [LogState.WAITING] * (local_world_size - 1))

        fds[0].write("training speed: 80 TFLOPs...\n")
        fds[0].flush()

        validate_agent_log_state(log_agent, [LogState.SLOW] +
                                 [LogState.WAITING] * (local_world_size - 1))

        fds[0].write("Training complete\n")
        fds[0].flush()

        validate_agent_log_state(log_agent, [LogState.HEALTHY] +
                                 [LogState.WAITING] * (local_world_size - 1))

        for fd in fds:
            fd.close()

        # Posttrain script logs monitoring
        posttrain_attempt_dir = tempfile.TemporaryDirectory(prefix="posttrain")
        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(posttrain_attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent.start(posttrain_attempt_dir.name, {0},
                        log_monitoring_configuration)
        validate_agent_log_state(log_agent, [LogState.HEALTHY] +
                                 [LogState.WAITING] * (local_world_size - 1))

        fds[0].write("Saving data\n")
        fds[0].flush()

        validate_agent_log_state(log_agent, [LogState.HEALTHY] +
                                 [LogState.WAITING] * (local_world_size - 1))

        log_agent.stop(clear_log_monitoring_configuration=True)
        assert not log_agent.is_running()

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        # Cleanup
        pretrain_attempt_dir.cleanup()
        train_attempt_dir.cleanup()
        posttrain_attempt_dir.cleanup()

    def test_log_agent_faulted_job(self, local_world_size, log_agent_config,
                                   tflops_threshold):
        # Create a configuration with faultOnMatch rule
        log_monitoring_configuration = [{
            "name": "OutOfMemoryError",
            "logPattern": ".*OutOfMemoryError.*",
            "faultOnMatch": True
        }]

        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)
        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        for rank in range(local_world_size):
            fds[rank].write("Start training process...\n")
            fds[rank].write(
                f"training speed: {tflops_threshold + 1} TFLOPs...\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent,
                                 [LogState.WAITING] * local_world_size)

        # Write error log to rank 0 only
        fds[0].write("OutOfMemoryError: Unable to allocate memory\n")
        fds[0].flush()

        # Verify rank 0 is in FAULTED state, others remain HEALTHY
        expected_states = [LogState.FAULTED
                           ] + [LogState.WAITING] * (local_world_size - 1)
        validate_agent_log_state(log_agent, expected_states)

        # Verify the rule name is correctly recorded
        assert list(
            log_agent.log_eval_results[0].rule_name_log_line.keys()) == [
                "OutOfMemoryError"
            ]

        # Write more normal logs to verify state doesn't change
        for rank in range(local_world_size):
            fds[rank].write("Epoch 2: Loss = 0.3\n")
            fds[rank].flush()

        # Verify states remain the same
        validate_agent_log_state(log_agent, expected_states)

        log_agent.stop()
        assert not log_agent.is_running()

        for i in range(local_world_size):
            assert log_agent.log_state[i] == LogState.WAITING

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_suspend_resume_functionality(self, local_world_size):
        """Test that suspend and resume functionality works correctly with timing calculations"""
        hanging_threshold = 3
        log_monitoring_configuration = [{
            "name":
            "TFLOPs",
            "logPattern":
            ".* (.+) TFLOPs.*",
            "expectedStartCutOffInSeconds":
            hanging_threshold,
            "expectedRecurringFrequencyInSeconds":
            hanging_threshold,
        }]

        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)

        # Start the agent
        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        # Write initial logs to establish pattern
        for rank in range(local_world_size):
            fds[rank].write("training speed: 120 TFLOPs...\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent,
                                 [LogState.HEALTHY] * local_world_size)

        # Stop the agent (this should suspend evaluators)
        log_agent.stop()
        assert not log_agent.is_running()

        # Wait for longer than the hanging threshold while suspended
        time.sleep(hanging_threshold + 1)

        # Restart the agent (this should resume evaluators)
        log_agent.start(attempt_dir.name)
        validate_agent_running(log_agent)

        # The job should still be healthy because the idle time during suspension
        # should not count towards hanging detection
        validate_agent_log_state(log_agent,
                                 [LogState.HEALTHY] * local_world_size)

        # Write more logs immediately after resume
        for rank in range(local_world_size):
            fds[rank].write("training speed: 125 TFLOPs...\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent,
                                 [LogState.HEALTHY] * local_world_size)

        log_agent.stop()

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_suspend_resume_with_hanging_detection(
            self, local_world_size):
        """Test that hanging detection works correctly after suspend/resume cycles"""
        hanging_threshold = 3
        log_monitoring_configuration = [{
            "name":
            "TFLOPs",
            "logPattern":
            ".* (.+) TFLOPs.*",
            "expectedRecurringFrequencyInSeconds":
            hanging_threshold,
        }]

        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)

        # Start the agent and write initial logs
        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        for rank in range(local_world_size):
            fds[rank].write("training speed: 120 TFLOPs...\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent,
                                 [LogState.HEALTHY] * local_world_size)

        # Stop and resume multiple times
        for _ in range(3):
            log_agent.stop()
            time.sleep(0.5)  # Short suspension
            log_agent.start(attempt_dir.name)
            validate_agent_running(log_agent)

        # Now wait for longer than hanging threshold without writing logs
        time.sleep(hanging_threshold + 1)

        # Should detect hanging since no matching pattern was found within threshold
        validate_agent_log_state(log_agent,
                                 [LogState.HANGING] * local_world_size)

        log_agent.stop()

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_clear_configuration_vs_suspend(self, local_world_size):
        """Test the difference between stopping with clear_log_monitoring_configuration=True vs False"""
        hanging_threshold = 3
        log_monitoring_configuration = [{
            "name":
            "TFLOPs",
            "logPattern":
            ".* (.+) TFLOPs.*",
            "expectedStartCutOffInSeconds":
            hanging_threshold,
        }]

        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)

        # Test 1: Stop without clearing configuration (should suspend)
        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        log_agent.stop(clear_log_monitoring_configuration=False)
        assert not log_agent.is_running()

        # Should be able to restart without providing configuration again
        log_agent.start(attempt_dir.name)
        validate_agent_running(log_agent)

        log_agent.stop()

        # Test 2: Stop with clearing configuration
        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        log_agent.stop(clear_log_monitoring_configuration=True)
        assert not log_agent.is_running()

        # Should not start without providing configuration again
        log_agent.start(attempt_dir.name)
        assert not log_agent.is_running(
        )  # Should not start because config was cleared

        # Should start again when configuration is provided
        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        log_agent.stop()

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_suspend_resume_preserves_evaluator_state(
            self, local_world_size):
        """Test that suspend/resume preserves evaluator internal state correctly"""
        log_monitoring_configuration = [{
            "name": "TFLOPs",
            "logPattern": ".* (.+) TFLOPs.*",
            "metricThreshold": 100,
            "operator": "lt",
            "metricEvaluationDataPoints":
            3  # Need 3 consecutive slow evaluations
        }]

        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)

        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        # Write 2 slow logs (below threshold)
        for rank in range(local_world_size):
            fds[rank].write(
                "training speed: 50 TFLOPs...\n")  # Below threshold
            fds[rank].flush()

        validate_agent_log_state(log_agent, [LogState.HEALTHY] *
                                 local_world_size)  # Not slow yet, need 3

        for rank in range(local_world_size):
            fds[rank].write(
                "training speed: 60 TFLOPs...\n")  # Below threshold
            fds[rank].flush()

        validate_agent_log_state(
            log_agent, [LogState.HEALTHY] *
            local_world_size)  # Still not slow, need 1 more

        # Suspend and resume
        log_agent.stop()
        time.sleep(0.1)
        log_agent.start(attempt_dir.name)
        validate_agent_running(log_agent)

        # Write the third slow log - should trigger SLOW state
        for rank in range(local_world_size):
            fds[rank].write(
                "training speed: 70 TFLOPs...\n")  # Below threshold
            fds[rank].flush()

        validate_agent_log_state(log_agent, [LogState.SLOW] *
                                 local_world_size)  # Now should be slow

        log_agent.stop()

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()

    def test_log_agent_suspend_resume_with_fault_on_match(
            self, local_world_size):
        """Test suspend/resume functionality with faultOnMatch rules"""
        log_monitoring_configuration = [{
            "name": "OutOfMemoryError",
            "logPattern": ".*OutOfMemoryError.*",
            "faultOnMatch": True
        }]

        attempt_dir = tempfile.TemporaryDirectory()

        fds = []
        for rank in range(local_world_size):
            rank_dir = os.path.join(attempt_dir.name, str(rank))
            os.makedirs(rank_dir)
            fds.append(open(os.path.join(rank_dir, f"stdout.log"), 'w'))

        log_agent = LogAgent(local_world_size)

        log_agent.start(
            attempt_dir.name,
            log_monitoring_configuration=log_monitoring_configuration)
        validate_agent_running(log_agent)

        # Write normal logs first
        for rank in range(local_world_size):
            fds[rank].write("Training proceeding normally\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent,
                                 [LogState.WAITING] * local_world_size)

        # Suspend and resume
        log_agent.stop()
        time.sleep(0.1)
        log_agent.start(attempt_dir.name)
        validate_agent_running(log_agent)

        # Write fault log to rank 0
        fds[0].write("OutOfMemoryError: Unable to allocate memory\n")
        fds[0].flush()

        # Should immediately fault
        expected_states = [LogState.FAULTED
                           ] + [LogState.WAITING] * (local_world_size - 1)
        validate_agent_log_state(log_agent, expected_states)

        # Suspend and resume again - fault state should persist
        log_agent.stop()
        time.sleep(0.1)
        log_agent.start(attempt_dir.name)
        validate_agent_running(log_agent)

        # Write more logs - fault state should remain
        for rank in range(local_world_size):
            fds[rank].write("More training logs\n")
            fds[rank].flush()

        validate_agent_log_state(log_agent, expected_states)

        log_agent.stop()

        for fd in fds:
            fd.close()
        attempt_dir.cleanup()


@retry(exceptions=(AssertionError, ), max_retries=60, delay=1, backoff=1)
def validate_agent_running(log_agent):
    assert log_agent.is_running()


@retry(exceptions=(AssertionError, ), max_retries=10, delay=1, backoff=1)
def validate_agent_log_state(log_agent, expected_log_state):
    assert log_agent.log_state == expected_log_state
