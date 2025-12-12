"""Resilience patterns for tool execution."""

import asyncio
import logging
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitBreaker:
    """Circuit breaker pattern for resilient tool execution."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 3,
    ):
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            half_open_max_calls: Max calls in half-open state
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.failure_count = 0
        self.last_failure_time: float | None = None
        self.state = "closed"
        self.half_open_calls = 0

    def record_success(self) -> None:
        """Record successful call."""
        self.failure_count = 0
        self.half_open_calls = 0
        self.state = "closed"

    def record_failure(self) -> None:
        """Record failed call."""
        import time

        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == "half_open":
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = "open"
                logger.warning("Circuit breaker opened after half-open failures")
        elif self.failure_count >= self.failure_threshold:
            self.state = "open"
            logger.warning("Circuit breaker opened after %d failures", self.failure_count)

    def can_execute(self) -> bool:
        """Check if execution is allowed.

        Returns:
            True if execution is allowed, False otherwise
        """
        import time

        if self.state == "closed":
            return True

        if self.state == "open":
            if self.last_failure_time is None:
                return False
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "half_open"
                self.half_open_calls = 0
                logger.info("Circuit breaker entering half-open state")
                return True
            return False

        if self.state == "half_open":
            return True

        return False


async def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    *args: Any,
    **kwargs: Any,
) -> T:
    """Retry function with exponential backoff.

    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        exceptions: Exception types to retry on
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        Function result

    Raises:
        Exception: Last exception if all retries fail
    """
    delay = initial_delay
    last_exception: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except exceptions as e:
            last_exception = e
            if attempt < max_retries:
                logger.warning(
                    "Retry attempt %d/%d failed: %s. Retrying in %.2f seconds...",
                    attempt + 1,
                    max_retries + 1,
                    str(e),
                    delay,
                )
                await asyncio.sleep(delay)
                delay = min(delay * exponential_base, max_delay)
            else:
                logger.error("All %d retry attempts failed", max_retries + 1)
                raise

    if last_exception:
        raise last_exception
    raise RuntimeError("Retry function failed without exception")


class TimeoutHandler:
    """Handle timeouts gracefully."""

    @staticmethod
    async def execute_with_timeout(
        coro: Callable[..., T],
        timeout_seconds: float,
        timeout_message: str = "Operation timed out",
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """Execute coroutine with timeout.

        Args:
            coro: Coroutine to execute
            timeout_seconds: Timeout in seconds
            timeout_message: Message for timeout error
            *args: Positional arguments for coro
            **kwargs: Keyword arguments for coro

        Returns:
            Coroutine result

        Raises:
            asyncio.TimeoutError: If operation times out
        """
        try:
            return await asyncio.wait_for(coro(*args, **kwargs), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            logger.error("%s after %.2f seconds", timeout_message, timeout_seconds)
            raise

