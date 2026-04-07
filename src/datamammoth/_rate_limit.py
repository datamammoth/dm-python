"""Rate limit handler with automatic retry logic."""

import time
from typing import Any, Callable, TypeVar

from datamammoth.exceptions import RateLimitError

T = TypeVar("T")

DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_BASE = 1.0  # seconds


def with_retry(
    fn: Callable[..., T],
    *args: Any,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_base: float = DEFAULT_BACKOFF_BASE,
    **kwargs: Any,
) -> T:
    """Execute a function with automatic retry on rate limit errors.

    Uses exponential backoff. If the server provides a Retry-After header,
    that value is used instead.

    Args:
        fn: The function to call.
        max_retries: Maximum number of retry attempts.
        backoff_base: Base seconds for exponential backoff.
        *args: Positional arguments to pass to fn.
        **kwargs: Keyword arguments to pass to fn.

    Returns:
        The return value of fn.

    Raises:
        RateLimitError: If all retries are exhausted.
    """
    last_error: RateLimitError
    for attempt in range(max_retries + 1):
        try:
            return fn(*args, **kwargs)
        except RateLimitError as e:
            last_error = e
            if attempt == max_retries:
                raise
            wait = e.retry_after if e.retry_after else backoff_base * (2 ** attempt)
            time.sleep(wait)
    raise last_error  # pragma: no cover


async def async_with_retry(
    fn: Callable[..., Any],
    *args: Any,
    max_retries: int = DEFAULT_MAX_RETRIES,
    backoff_base: float = DEFAULT_BACKOFF_BASE,
    **kwargs: Any,
) -> Any:
    """Async version of with_retry."""
    import asyncio

    last_error: RateLimitError
    for attempt in range(max_retries + 1):
        try:
            return await fn(*args, **kwargs)
        except RateLimitError as e:
            last_error = e
            if attempt == max_retries:
                raise
            wait = e.retry_after if e.retry_after else backoff_base * (2 ** attempt)
            await asyncio.sleep(wait)
    raise last_error  # pragma: no cover
