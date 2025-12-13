"""Unified retry handler with consistent strategies across components."""

import asyncio
import logging
import time
from dataclasses import dataclass
from functools import wraps
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class RetryConfig:
    """Retry configuration."""

    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    retryable_exceptions: tuple[type[Exception], ...] = (Exception,)


STANDARD_RETRY = RetryConfig(
    max_attempts=3,
    initial_delay=1.0,
    max_delay=10.0,
    exponential_base=2.0,
)

API_RETRY = RetryConfig(
    max_attempts=5,
    initial_delay=1.0,
    max_delay=60.0,
    exponential_base=2.0,
)

QUOTA_RETRY = RetryConfig(
    max_attempts=3,
    initial_delay=120.0,
    max_delay=480.0,
    exponential_base=2.0,
)


def retry_async(
    config: RetryConfig = STANDARD_RETRY,
    on_retry: Callable[[Exception, int], None] | None = None,
):
    """Async retry decorator with exponential backoff.

    Args:
        config: Retry configuration
        on_retry: Optional callback on retry (exception, attempt_number)
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = config.initial_delay
            last_exception: Exception | None = None

            for attempt in range(config.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e

                    if attempt < config.max_attempts - 1:
                        if on_retry:
                            on_retry(e, attempt + 1)
                        else:
                            logger.warning(
                                "Retry %d/%d for %s after %.1fs: %s",
                                attempt + 1,
                                config.max_attempts,
                                func.__name__,
                                delay,
                                e,
                            )

                        await asyncio.sleep(delay)
                        delay = min(delay * config.exponential_base, config.max_delay)
                    else:
                        logger.error(
                            "Failed after %d attempts for %s: %s",
                            config.max_attempts,
                            func.__name__,
                            e,
                        )
                        raise

            if last_exception:
                raise last_exception
            raise RuntimeError(f"Function {func.__name__} failed after {config.max_attempts} attempts")

        return wrapper

    return decorator


def retry_sync(
    config: RetryConfig = STANDARD_RETRY,
    on_retry: Callable[[Exception, int], None] | None = None,
):
    """Sync retry decorator with exponential backoff."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = config.initial_delay
            last_exception: Exception | None = None

            for attempt in range(config.max_attempts):
                try:
                    return func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e

                    if attempt < config.max_attempts - 1:
                        if on_retry:
                            on_retry(e, attempt + 1)
                        else:
                            logger.warning(
                                "Retry %d/%d for %s after %.1fs: %s",
                                attempt + 1,
                                config.max_attempts,
                                func.__name__,
                                delay,
                                e,
                            )

                        time.sleep(delay)
                        delay = min(delay * config.exponential_base, config.max_delay)
                    else:
                        logger.error(
                            "Failed after %d attempts for %s: %s",
                            config.max_attempts,
                            func.__name__,
                            e,
                        )
                        raise

            if last_exception:
                raise last_exception
            raise RuntimeError(f"Function {func.__name__} failed after {config.max_attempts} attempts")

        return wrapper

    return decorator

