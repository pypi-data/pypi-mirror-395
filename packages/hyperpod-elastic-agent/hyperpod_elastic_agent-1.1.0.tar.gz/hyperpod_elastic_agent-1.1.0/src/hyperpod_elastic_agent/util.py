import functools
import time


def retry(exceptions, max_retries=3, delay=1, backoff=1):
    """
    Retry decorator with exponential backoff.

    Args:
        exceptions (tuple): Exceptions to catch and retry.
        max_retries (int): Maximum retry attempts.
        delay (float): Initial delay before retrying.
        backoff (float): Backoff multiplier (e.g., 2 doubles the delay each retry).
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Retry {attempt + 1}/{max_retries} due to {e}")
                    if attempt == max_retries - 1:
                        # Raise the last exception after max retries
                        raise
                    time.sleep(_delay)
                    # Increase delay exponentially
                    _delay *= backoff

        return wrapper

    return decorator