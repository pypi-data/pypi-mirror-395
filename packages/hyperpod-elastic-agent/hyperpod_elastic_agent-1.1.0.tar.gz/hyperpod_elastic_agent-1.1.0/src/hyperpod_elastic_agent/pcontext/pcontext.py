import os
import psutil
import signal
import sys
import subprocess
import time

from concurrent.futures import ThreadPoolExecutor, wait
from torch.distributed.elastic.multiprocessing import start_processes as og_start_process
from torch.distributed.elastic.multiprocessing.api import (
    LogsSpecs,
    PContext,
    RunProcsResult,
    SubprocessContext,
)
from torch.distributed.elastic.multiprocessing.errors import ProcessFailure
from torch.distributed.elastic.multiprocessing.subprocess_handler import SubprocessHandler
from typing import Any, Callable, Optional, Union
from ..logging import get_logger

logger = get_logger(__name__)


def _validate_full_rank(d: dict[int, Any], nprocs: int, what: str):
    actual_keys = set(d.keys())
    expected_keys = set(range(nprocs))

    if actual_keys != expected_keys:
        raise RuntimeError(
            f"{what}, local rank mapping mismatch,"
            f" expected: {expected_keys}, actual: {actual_keys}")


def _get_kill_signal() -> signal.Signals:
    """Get the kill signal. SIGKILL for unix, CTRL_C_EVENT for windows."""
    if sys.platform == "win32":
        return signal.CTRL_C_EVENT  # type: ignore[attr-defined] # noqa: F821
    else:
        return signal.SIGKILL


def start_processes(
    name: str,
    entrypoint: Union[Callable, str],
    args: dict[int, tuple],
    envs: dict[int, dict[str, str]],
    logs_specs: LogsSpecs,
    death_sig: signal.Signals,
    signal_timeout: int,
    log_line_prefixes: Optional[dict[int, str]] = None,
    start_method: str = "spawn",
) -> PContext:
    """
    Overrides torchelastic's SubprocessContext to customize it for HyperPod
    """
    if not isinstance(entrypoint, str):
        return og_start_process(
            name=name,
            entrypoint=entrypoint,
            args=args,
            envs=envs,
            logs_specs=logs_specs,
            log_line_prefixes=log_line_prefixes,
            start_method=start_method,
        )

    nprocs = len(args)
    _validate_full_rank(args, nprocs, "args")
    _validate_full_rank(envs, nprocs, "envs")

    context: PContext
    context = HyperpodSubprocessContext(
        name=name,
        entrypoint=entrypoint,
        args=args,
        envs=envs,
        logs_specs=logs_specs,
        death_sig=death_sig,
        signal_timeout=signal_timeout,
        log_line_prefixes=log_line_prefixes,
    )

    try:
        context.start()
        return context
    except Exception:
        context.close()
        raise


class HyperpodSubprocessContext(SubprocessContext):
    ENABLE_SIGCHLD_HANDLER = os.getenv(
        "HYPERPOD_ELASTICAGENT_ENABLE_SIGCHLD_HANDLER",
        "True").lower() in ("true", "1", "t")
    SIGNAL_TIMEOUT = 15 if ENABLE_SIGCHLD_HANDLER else 30

    def __init__(
        self,
        name: str,
        entrypoint: str,
        args: dict[int, tuple],
        envs: dict[int, dict[str, str]],
        logs_specs: LogsSpecs,
        death_sig: signal.Signals,
        signal_timeout: int,
        log_line_prefixes: Optional[dict[int, str]] = None,
    ):
        super().__init__(
            name,
            entrypoint,
            args,
            envs,
            logs_specs,
            log_line_prefixes,
        )
        self._death_sig = death_sig
        self._signal_timeout = signal_timeout
        self._process_exit_signals: dict[int, int] = {}
        if self.ENABLE_SIGCHLD_HANDLER:
            # Set up the signal handler
            logger.info("Setting up signal handler to reap zombie processes")
            signal.signal(signal.SIGCHLD, self._reap_zombies)

    def _reap_zombies(self, signum, frame):
        """Reap child processes when they terminate"""
        while True:
            try:
                # Wait for any child process to terminate
                pid, status = os.waitpid(-1, os.WNOHANG)
                # If no more children, exit the loop
                if pid == 0:
                    break
                logger.info(f"Reaped child process {pid} with status {status}")
                # Need to keep track of the exit signal since handler.proc.poll()
                # will return exitcode 0 even if the process was terminated by a signal
                if status != 0:
                    # Only store if status is non zero to save on memory
                    self._process_exit_signals[pid] = status
            except ChildProcessError:
                # No child processes left
                break

    def close(self,
              death_sig: Optional[signal.Signals] = None,
              timeout: Optional[int] = None) -> None:
        if not death_sig:
            death_sig = self._death_sig
        if not timeout:
            timeout = self._signal_timeout
        logger.debug(f"pcontext.close() called with death_sig={death_sig.name}, timeout={timeout}")
        super().close(death_sig, timeout)
        # Clear exit signals after close is finished
        self._process_exit_signals.clear()
        logger.debug(f"pcontext.close() completed for signal {death_sig.name}")

    @staticmethod
    def _close_single(
        handler: SubprocessHandler,
        death_sig: signal.Signals,
        timeout: int = SIGNAL_TIMEOUT,
    ):
        logger.debug(
            "Sending process %s closing signal %s",
            handler.proc.pid,
            death_sig.name,
        )
        handler.close(death_sig=death_sig)
        if HyperpodSubprocessContext.ENABLE_SIGCHLD_HANDLER:
            # Wait for zombie state
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    process = psutil.Process(handler.proc.pid)
                    status = process.status()
                    if status == psutil.STATUS_ZOMBIE:
                        logger.warning(
                            f"Process {handler.proc.pid} is now zombie, okay to proceed"
                        )
                        logger.info(f"Connections for process {handler.proc.pid}: {process.net_connections()}")
                        return
                    time.sleep(0.1)
                except psutil.NoSuchProcess:
                    logger.warning(
                        f"Process {handler.proc.pid} no longer exists")
                    return

        if not HyperpodSubprocessContext.ENABLE_SIGCHLD_HANDLER:
            try:
                handler.proc.wait(timeout)
            except subprocess.TimeoutExpired:
                # Ignore the timeout expired exception, since
                # the child process will be forcefully terminated via SIGKILL
                pass

        # Keep existing wait logic if process does not become zombie in time
        # TODO: Look into crashing the pod if timeout occurs
        if handler.proc.poll() is None:
            logger.warning(
                "Unable to shutdown process %s via %s, forcefully exiting via %s",
                handler.proc.pid,
                death_sig,
                _get_kill_signal(),
            )
            handler.close(death_sig=_get_kill_signal())
            handler.proc.wait()

    def _close(
        self,
        death_sig: signal.Signals,
        timeout: int = SIGNAL_TIMEOUT,
    ) -> None:
        if not self.subprocess_handlers:
            return
        with ThreadPoolExecutor() as executor:
            futures = []
            for handler in self.subprocess_handlers.values():
                futures.append(
                    executor.submit(
                        self._close_single,
                        handler,
                        death_sig,
                        timeout,
                    ))

            wait(futures)

    def _poll(self) -> Optional[RunProcsResult]:
        if not self.ENABLE_SIGCHLD_HANDLER:
            return super()._poll()

        done_local_ranks = set()
        for local_rank in self._running_local_ranks:
            handler = self.subprocess_handlers[local_rank]
            exitcode = handler.proc.poll()
            if exitcode is not None:
                pid = handler.proc.pid
                # Check if we have stored signal information for this pid
                # handler.proc.poll() will return exitcode 0 even if the
                # process was terminated by a different signal
                if pid in self._process_exit_signals:
                    exitcode = -self._process_exit_signals[pid]
                    logger.info(
                        "Process %s (local_rank: %s) was terminated by signal %s, setting exitcode to %s",
                        pid, local_rank, self._process_exit_signals[pid],
                        exitcode)
                    # Clean up stored signal info
                    del self._process_exit_signals[pid]

                done_local_ranks.add(local_rank)
                if exitcode != 0:  # failed or signaled
                    self._failures[local_rank] = ProcessFailure(
                        local_rank=local_rank,
                        pid=handler.proc.pid,
                        exitcode=exitcode,
                        error_file=self.error_files[local_rank],
                    )
                # else: --> succeeded; nothing to do

        self._running_local_ranks.difference_update(done_local_ranks)
        return super()._poll()
