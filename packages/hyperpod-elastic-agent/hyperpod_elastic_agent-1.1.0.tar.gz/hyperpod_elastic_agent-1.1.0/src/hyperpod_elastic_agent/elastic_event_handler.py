import os
import signal
from .logging import get_logger

logger = get_logger(__name__)

# Global state for signal tracking
_signal_received = {}

# Valid signal coordination modes
_VALID_COORDINATION_MODES = {'disabled', 'distributed'}

# Signal coordination mode: 'disabled', 'distributed'
_raw_mode = os.getenv('HYPERPOD_SIGNAL_COORDINATION', 'disabled').lower()

if _raw_mode not in _VALID_COORDINATION_MODES:
    logger.warning(
        f'Invalid HYPERPOD_SIGNAL_COORDINATION value: "{_raw_mode}". '
        f'Valid values are: {", ".join(sorted(_VALID_COORDINATION_MODES))}. '
        f'Defaulting to "disabled".')
    _SIGNAL_COORDINATION_MODE = 'disabled'
else:
    _SIGNAL_COORDINATION_MODE = _raw_mode

logger.info(f'Signal coordination mode set to: {_SIGNAL_COORDINATION_MODE}')


def _signal_handler(signum, frame):
    """Signal handler - SIGUSR1 for elastic events"""
    global _signal_received
    _signal_received[signum] = True
    signal_desc = signal.strsignal(signum) or f'SIG{signum}'
    if signum == signal.SIGUSR1:
        logger.info(f'{signal_desc} received - elastic event detected')
    else:
        logger.info(f'{signal_desc} received')


# Register SIGUSR1 handler for elastic events (let PyTorch handle SIGTERM)
signal.signal(signal.SIGUSR1, _signal_handler)
_signal_received[signal.SIGUSR1] = False

logger.debug('Signal handler registered for SIGUSR1')


def elastic_event_detected(sig=signal.SIGUSR1):
    """Check if elastic scaling event signal (SIGUSR1) has been received
    
    This function is intended for use by training processes in their training loops,
    not by the agent process itself (to avoid collective communication issues).
    """
    logger.debug(f"elastic_event_detected called for signal {sig}")

    # Only handle SIGUSR1 for elastic events (let PyTorch handle SIGTERM)
    if sig != signal.SIGUSR1:
        logger.debug(f"Ignoring non-SIGUSR1 signal: {sig}")
        return False

    # Check coordination mode
    if _SIGNAL_COORDINATION_MODE == 'disabled':
        logger.debug(f"Event coordination disabled, returning False")
        return False  # Elastic events disabled

    local_signal = _signal_received.get(sig, False)
    logger.debug(f"Local event state for {sig}: {local_signal}")

    if _SIGNAL_COORDINATION_MODE == 'distributed':
        try:
            import torch
            import torch.distributed as dist

            if not dist.is_initialized():
                logger.debug(
                    f"Distributed not initialized, returning local event: {local_signal}"
                )
                return local_signal

            # Distributed coordination using all_reduce
            device = torch.device(
                f"cuda:{torch.cuda.current_device()}"
            ) if torch.cuda.is_available() else torch.device("cpu")
            signal_tensor = torch.tensor([1.0 if local_signal else 0.0],
                                         device=device)
            logger.debug(
                f"Performing distributed all_reduce for event coordination")
            dist.all_reduce(signal_tensor, op=dist.ReduceOp.MAX)
            result = signal_tensor.item() > 0
            logger.debug(f"Distributed event result: {result}")
            return result

        except (ImportError, Exception) as e:
            logger.warning(f'Error in distributed event check: {e}')
            return local_signal

    # Invalid coordination mode
    logger.warning(
        f'Invalid HYPERPOD_SIGNAL_COORDINATION mode: {_SIGNAL_COORDINATION_MODE}. Use "disabled" or "distributed"'
    )
    return False
