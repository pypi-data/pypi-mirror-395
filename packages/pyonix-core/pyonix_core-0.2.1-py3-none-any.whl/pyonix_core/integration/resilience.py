import time
import functools
from typing import Callable, Sequence, Type, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def with_onyx_retries(
    exceptions: Optional[Tuple[Type[BaseException], ...]] = None,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    fail_fast_exceptions: Optional[Tuple[Type[BaseException], ...]] = None,
):
    """
    Simple retry decorator with exponential backoff.

    - `exceptions`: tuple of exception classes to retry on. If None, defaults to `(Exception,)`.
    - `max_attempts`: maximum attempts (including first try).
    - `initial_delay`: delay before first retry in seconds.
    - `backoff_factor`: multiplier for successive delays.
    - `fail_fast_exceptions`: exceptions that should not be retried and are raised immediately.
    """

    if exceptions is None:
        exceptions = (Exception,)
    if fail_fast_exceptions is None:
        fail_fast_exceptions = ()

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = initial_delay
            last_exc = None
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except fail_fast_exceptions:
                    # Fail fast: re-raise
                    logger.debug("with_onyx_retries: fail-fast exception raised: %s", fail_fast_exceptions)
                    raise
                except exceptions as exc:
                    last_exc = exc
                    attempts += 1
                    logger.debug("with_onyx_retries caught %s (attempt %d/%d)", type(exc).__name__, attempts, max_attempts)
                    if attempts >= max_attempts:
                        logger.debug("with_onyx_retries: reached max attempts (%d)", max_attempts)
                        break
                    time.sleep(delay)
                    delay *= backoff_factor
            # Re-raise the last exception with context
            if last_exc is not None:
                raise last_exc
            # Shouldn't reach here, but raise a generic exception
            raise RuntimeError("with_onyx_retries: unexpected failure")

        return wrapper

    return decorator


__all__ = ["with_onyx_retries"]
