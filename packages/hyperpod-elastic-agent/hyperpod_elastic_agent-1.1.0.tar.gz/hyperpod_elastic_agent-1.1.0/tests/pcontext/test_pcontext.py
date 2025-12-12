import importlib
import os
import psutil
import pytest
import signal

from hyperpod_elastic_agent.pcontext.pcontext import (
    HyperpodSubprocessContext,
    _validate_full_rank,
)
from concurrent.futures import ThreadPoolExecutor
from torch.distributed.elastic.multiprocessing.api import DefaultLogsSpecs
from torch.distributed.elastic.multiprocessing.subprocess_handler import SubprocessHandler
from unittest.mock import Mock, call, patch


class TestHyperpodSubprocessContext:

    @classmethod
    def setup_class(cls):
        # Mock dependencies and create a sample instance
        cls.name = "test_subprocess"
        cls.entrypoint = "/path/to/entrypoint"
        cls.args = {0: ("arg1", "arg2")}
        cls.envs = {0: {"ENV_VAR": "value"}}
        cls.logs_specs = DefaultLogsSpecs()
        cls.death_sig = signal.SIGTERM
        cls.signal_timeout = 10
        cls.log_line_prefixes = {0: "prefix"}

    @pytest.fixture
    def context_with_env_variable(self):

        def _create(sigchld_handler_enabled="True"):
            with patch.dict(
                    os.environ, {
                        "HYPERPOD_ELASTICAGENT_ENABLE_SIGCHLD_HANDLER":
                        sigchld_handler_enabled
                    }):
                from hyperpod_elastic_agent.pcontext import pcontext
                importlib.reload(pcontext)
                return pcontext.HyperpodSubprocessContext(
                    name=self.name,
                    entrypoint=self.entrypoint,
                    args=self.args,
                    envs=self.envs,
                    logs_specs=self.logs_specs,
                    death_sig=self.death_sig,
                    signal_timeout=self.signal_timeout,
                    log_line_prefixes=self.log_line_prefixes,
                )

        return _create

    def test_init_without_sigchld(self, context_with_env_variable):
        """Test that the initialization sets the correct attributes"""
        context = context_with_env_variable("False")
        assert context.name == self.name
        assert context.entrypoint == self.entrypoint
        assert context._death_sig == self.death_sig
        assert not context.ENABLE_SIGCHLD_HANDLER
        assert context.SIGNAL_TIMEOUT == 30
        assert signal.getsignal(signalnum=signal.SIGCHLD) in {
            signal.SIG_DFL, signal.SIG_IGN, None
        }

    def test_init_with_sigchld(self, context_with_env_variable):
        context = context_with_env_variable()
        assert context.name == self.name
        assert context.entrypoint == self.entrypoint
        assert context._death_sig == self.death_sig
        assert context.ENABLE_SIGCHLD_HANDLER
        assert context.SIGNAL_TIMEOUT == 15
        assert signal.getsignal(
            signalnum=signal.SIGCHLD) == context._reap_zombies

    @patch('psutil.Process')
    def test_close_single_method_sigchld(
        self,
        mock_psutil_process,
        context_with_env_variable,
    ):
        context = context_with_env_variable("T")
        assert context.ENABLE_SIGCHLD_HANDLER
        mock_proc = Mock()
        # Process is still running
        mock_proc.poll.return_value = None
        mock_proc.pid = 1234

        # Mock psutil.Process instance
        mock_psutil_proc = Mock()
        mock_psutil_proc.status.side_effect = [
            psutil.STATUS_RUNNING,  # First check
            psutil.STATUS_RUNNING,  # Second check
            psutil.STATUS_ZOMBIE,  # Finally becomes zombie
        ]
        mock_psutil_process.return_value = mock_psutil_proc

        mock_handler = Mock(spec=SubprocessHandler)
        mock_handler.proc = mock_proc

        with patch(
                'hyperpod_elastic_agent.pcontext.pcontext.wait') as mock_wait:
            mock_wait.return_value = (set(), set())
            HyperpodSubprocessContext._close_single(
                mock_handler,
                signal.SIGTERM,
                HyperpodSubprocessContext.SIGNAL_TIMEOUT,
            )

        # Verify method calls
        mock_handler.close.assert_has_calls([call(death_sig=signal.SIGTERM)])
        assert mock_psutil_process.call_count == 3
        assert mock_proc.wait.call_count == 0

    @patch('psutil.Process')
    def test_close_single_method_no_sigchld(
        self,
        mock_psutil_process,
        context_with_env_variable,
    ):
        context = context_with_env_variable("F")
        assert not context.ENABLE_SIGCHLD_HANDLER
        mock_proc = Mock()
        # Process is still running
        mock_proc.poll.return_value = None
        mock_proc.pid = 1234
        mock_psutil_proc = Mock()
        mock_psutil_process.return_value = mock_psutil_proc

        mock_handler = Mock(spec=SubprocessHandler)
        mock_handler.proc = mock_proc

        with patch(
                'hyperpod_elastic_agent.pcontext.pcontext.wait') as mock_wait:
            mock_wait.return_value = (set(), set())
            HyperpodSubprocessContext._close_single(
                mock_handler,
                signal.SIGTERM,
                HyperpodSubprocessContext.SIGNAL_TIMEOUT,
            )

        # Verify method calls
        mock_handler.close.assert_has_calls([call(death_sig=signal.SIGTERM)])
        assert mock_psutil_process.call_count == 0
        assert mock_proc.wait.call_count == 2

    @patch('psutil.Process')
    def test_close_single_method_terminate(
        self,
        mock_psutil_process,
        context_with_env_variable,
    ):
        context = context_with_env_variable()
        assert context.ENABLE_SIGCHLD_HANDLER
        mock_proc = Mock()
        # Process is still running
        mock_proc.poll.return_value = None
        mock_proc.pid = 1234

        # Mock psutil.Process instance
        mock_psutil_proc = Mock()
        mock_psutil_proc.status.return_value = psutil.STATUS_RUNNING
        mock_psutil_process.return_value = mock_psutil_proc

        mock_handler = Mock(spec=SubprocessHandler)
        mock_handler.proc = mock_proc

        with patch(
                'hyperpod_elastic_agent.pcontext.pcontext.wait') as mock_wait:
            mock_wait.return_value = (set(), set())
            HyperpodSubprocessContext._close_single(
                handler=mock_handler,
                death_sig=signal.SIGTERM,
                timeout=1,
            )

        # Verify method calls
        mock_handler.close.assert_has_calls(
            [call(death_sig=signal.SIGTERM),
             call(death_sig=signal.SIGKILL)])
        mock_proc.wait.assert_has_calls([call()])

    def test_close_method(self, context_with_env_variable):
        context = context_with_env_variable()
        assert context.ENABLE_SIGCHLD_HANDLER
        # Create mock subprocess handlers
        mock_handlers = {
            0: Mock(spec=SubprocessHandler),
            1: Mock(spec=SubprocessHandler)
        }
        context.subprocess_handlers = mock_handlers

        # Mock the executor and futures
        mock_future1 = Mock()
        mock_future2 = Mock()
        mock_executor_instance = Mock()
        mock_executor_instance.submit.side_effect = [
            mock_future1, mock_future2
        ]

        # Patch the ThreadPoolExecutor to return our mock
        with patch.object(
                ThreadPoolExecutor,
                '__enter__',
                return_value=mock_executor_instance,
        ), patch('hyperpod_elastic_agent.pcontext.pcontext.wait') as mock_wait:
            mock_wait.return_value = (set(), set())
            context.close(timeout=30)
            mock_wait.assert_called_once()
        assert mock_executor_instance.submit.call_count == 2

    def test_close_method_process_exited(self, context_with_env_variable):
        context = context_with_env_variable()
        assert context.ENABLE_SIGCHLD_HANDLER
        mock_handlers = {0: Mock(spec=SubprocessHandler)}
        context.subprocess_handlers = mock_handlers

        mock_proc = Mock()
        # Process is still running
        mock_proc.poll.return_value = 0
        mock_proc.pid = 1234

        mock_handler = Mock(spec=SubprocessHandler)
        mock_handler.proc = mock_proc

        mock_future = Mock()
        mock_executor_instance = Mock()
        mock_executor_instance.submit.side_effect = [mock_future]

        # Call the method
        with patch.object(
                ThreadPoolExecutor,
                '__enter__',
                return_value=mock_executor_instance,
        ), patch('hyperpod_elastic_agent.pcontext.pcontext.wait') as mock_wait:
            mock_wait.return_value = (set(), set())
            context.close()

        # Verify method calls
        mock_handler.close.assert_not_called()
        mock_proc.wait.assert_not_called()

    def test_close_with_no_handlers(self, context_with_env_variable):
        context = context_with_env_variable()
        context.subprocess_handlers = {}
        context.close()

    def test_close_with_custom_death_signal(self, context_with_env_variable):
        context = context_with_env_variable()
        mock_handlers = {0: Mock(spec=SubprocessHandler)}
        context.subprocess_handlers = mock_handlers

        custom_sig = signal.SIGKILL
        with patch.object(context, '_close') as mock_close:
            context.close(death_sig=custom_sig)
            mock_close.assert_called_once_with(
                death_sig=custom_sig,
                timeout=self.signal_timeout,
            )

    def test_validate_full_rank_success(self):
        _validate_full_rank({
            0: ("bar0", ),
            1: ("bar1", ),
        }, 2, "")

    def test_validate_full_rank_fail(self):
        with pytest.raises(RuntimeError):
            _validate_full_rank({}, 10, "")

    def test_reap_zombies(self, context_with_env_variable):
        """Test the zombie process reaping functionality"""
        context = context_with_env_variable("1")
        with patch('os.waitpid') as mock_waitpid:
            # Simulate three child processes
            mock_waitpid.side_effect = [
                (1001, 0),  # Normal exit
                (1002, 256),  # Exit with status 1 (256 >> 8 = 1)
                (1003, 9),  # Terminated by SIGKILL
                (0, 0),  # No more children
            ]

            # Call _reap_zombies directly
            context._reap_zombies(signal.SIGCHLD, None)

            # Check that waitpid was called 4 times
            assert mock_waitpid.call_count == 4

            # Check that _process_exit_signals contains only non-zero exits
            assert context._process_exit_signals == {1002: 256, 1003: 9}
            context._process_exit_signals.clear()

    def test_reap_zombies_no_children(self, context_with_env_variable):
        """Test reaping behavior when no child processes exists"""
        context = context_with_env_variable("1")
        with patch('os.waitpid') as mock_waitpid:
            mock_waitpid.side_effect = ChildProcessError()

            # Call _reap_zombies directly
            context._reap_zombies(signal.SIGCHLD, None)

            # Check that waitpid was called once
            mock_waitpid.assert_called_once()

            # Check that _process_exit_signals is empty
            assert not context._process_exit_signals
