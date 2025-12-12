"""Retry and timeout utilities for external API calls."""

import asyncio
import logging
from functools import wraps
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


async def with_timeout(
    coro: Callable[..., Any],
    timeout_seconds: float = 30.0,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Execute coroutine with timeout.

    Args:
        coro: Coroutine function to execute
        timeout_seconds: Timeout in seconds
        *args: Positional arguments for coroutine
        **kwargs: Keyword arguments for coroutine

    Returns:
        Result from coroutine

    Raises:
        asyncio.TimeoutError: If operation exceeds timeout
        Exception: If coroutine raises an exception
    """
    try:
        return await asyncio.wait_for(
            coro(*args, **kwargs),
            timeout=timeout_seconds,
        )
    except asyncio.TimeoutError:
        logger.error(
            "Operation timed out after %.1f seconds: %s",
            timeout_seconds,
            coro.__name__ if hasattr(coro, "__name__") else str(coro),
        )
        raise RuntimeError(f"Operation timed out after {timeout_seconds} seconds") from None


async def with_retry(
    coro: Callable[..., Any],
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    backoff_multiplier: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Execute coroutine with retry logic and exponential backoff.

    Args:
        coro: Coroutine function to execute
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds before first retry
        max_delay: Maximum delay between retries
        backoff_multiplier: Multiplier for exponential backoff
        retryable_exceptions: Tuple of exception types to retry on
        *args: Positional arguments for coroutine
        **kwargs: Keyword arguments for coroutine

    Returns:
        Result from coroutine

    Raises:
        Exception: If all retry attempts fail
    """
    last_exception = None
    delay = initial_delay

    for attempt in range(max_attempts):
        try:
            return await coro(*args, **kwargs)
        except retryable_exceptions as e:
            last_exception = e
            if attempt < max_attempts - 1:
                logger.warning(
                    "Attempt %d/%d failed for %s: %s. Retrying in %.1f seconds...",
                    attempt + 1,
                    max_attempts,
                    coro.__name__ if hasattr(coro, "__name__") else str(coro),
                    str(e),
                    delay,
                )
                await asyncio.sleep(delay)
                delay = min(delay * backoff_multiplier, max_delay)
            else:
                logger.error(
                    "All %d attempts failed for %s: %s",
                    max_attempts,
                    coro.__name__ if hasattr(coro, "__name__") else str(coro),
                    str(e),
                )

    if last_exception:
        raise RuntimeError(
            f"Operation failed after {max_attempts} attempts: {last_exception}",
        ) from last_exception

    raise RuntimeError(f"Operation failed after {max_attempts} attempts")


async def with_timeout_and_retry(
    coro: Callable[..., Any],
    timeout_seconds: float = 30.0,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    backoff_multiplier: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Execute coroutine with both timeout and retry logic.

    Args:
        coro: Coroutine function to execute
        timeout_seconds: Timeout in seconds per attempt
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds before first retry
        max_delay: Maximum delay between retries
        backoff_multiplier: Multiplier for exponential backoff
        retryable_exceptions: Tuple of exception types to retry on
        *args: Positional arguments for coroutine
        **kwargs: Keyword arguments for coroutine

    Returns:
        Result from coroutine

    Raises:
        RuntimeError: If operation fails after all retries or times out
    """
    async def attempt_with_timeout() -> Any:
        return await with_timeout(coro, timeout_seconds, *args, **kwargs)

    return await with_retry(
        attempt_with_timeout,
        max_attempts=max_attempts,
        initial_delay=initial_delay,
        max_delay=max_delay,
        backoff_multiplier=backoff_multiplier,
        retryable_exceptions=retryable_exceptions,
    )


def retry_on_failure(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    backoff_multiplier: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,),
):
    """Decorator for retry logic with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts
        initial_delay: Initial delay in seconds before first retry
        max_delay: Maximum delay between retries
        backoff_multiplier: Multiplier for exponential backoff
        retryable_exceptions: Tuple of exception types to retry on

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            retry_param_names = {
                "max_attempts",
                "initial_delay",
                "max_delay",
                "backoff_multiplier",
                "retryable_exceptions",
            }
            func_kwargs = {k: v for k, v in kwargs.items() if k not in retry_param_names}
            
            async def wrapped_func() -> Any:
                return await func(*args, **func_kwargs)
            
            return await with_retry(
                wrapped_func,
                max_attempts=max_attempts,
                initial_delay=initial_delay,
                max_delay=max_delay,
                backoff_multiplier=backoff_multiplier,
                retryable_exceptions=retryable_exceptions,
            )

        return wrapper

    return decorator


def timeout(
    timeout_seconds: float = 30.0,
):
    """Decorator for timeout handling.

    Args:
        timeout_seconds: Timeout in seconds

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await with_timeout(
                func,
                timeout_seconds=timeout_seconds,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator

