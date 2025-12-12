import signal
from dataclasses import dataclass
from typing import Optional


@dataclass
class PrePostTrainConfig:
    pre_train_script: Optional[str] = None
    post_train_script: Optional[str] = None
    pre_train_args: Optional[str] = ""
    post_train_args: Optional[str] = ""


@dataclass
class ShutdownConfig:
    shutdown_timeout: int = 15
    shutdown_signal: signal.Signals = signal.SIGKILL

    def __post_init__(self):
        if isinstance(self.shutdown_signal, str):
            try:
                self.shutdown_signal = signal.Signals[self.shutdown_signal]
            except (KeyError, AttributeError):
                raise ValueError(
                    f"Invalid signal string: {self.shutdown_signal}")
