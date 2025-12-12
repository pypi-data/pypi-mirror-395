"""Circuit breaker pattern for external API calls."""

import asyncio
import logging
import time
from enum import Enum
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""

    pass


class CircuitBreaker:
    """Circuit breaker for external API calls.

    Prevents cascading failures by stopping requests when external services are down.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exceptions: tuple[type[Exception], ...] = (RuntimeError, ConnectionError, TimeoutError),
        name: str = "api",
    ):
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exceptions: Exception types that trigger circuit breaker
            name: Name for logging purposes
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions
        self.name = name

        self.failure_count = 0
        self.last_failure_time: float | None = None
        self.state = CircuitState.CLOSED
        self.success_count = 0
        self.lock = asyncio.Lock()

    async def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute async function with circuit breaker protection.

        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerError: If circuit is open
        """
        async with self.lock:
            if self.state == CircuitState.OPEN:
                if self.last_failure_time and (
                    time.time() - self.last_failure_time > self.recovery_timeout
                ):
                    logger.info("Circuit breaker %s: Attempting recovery (HALF_OPEN)", self.name)
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitBreakerError(
                        f"Circuit breaker {self.name} is OPEN. "
                        f"Last failure: {self.last_failure_time}"
                    )

        try:
            if asyncio.iscoroutinefunction(func) or asyncio.iscoroutine(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            async with self.lock:
                if self.state == CircuitState.HALF_OPEN:
                    self.success_count += 1
                    if self.success_count >= 2:
                        logger.info("Circuit breaker %s: Recovered (CLOSED)", self.name)
                        self.state = CircuitState.CLOSED
                        self.failure_count = 0
                        self.success_count = 0
                elif self.state == CircuitState.CLOSED:
                    self.failure_count = 0

            return result

        except self.expected_exceptions as e:
            async with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()

                logger.warning(
                    "Circuit breaker %s: Failure %d/%d: %s",
                    self.name,
                    self.failure_count,
                    self.failure_threshold,
                    e,
                )

                if self.failure_count >= self.failure_threshold:
                    logger.error("Circuit breaker %s: Opening circuit (OPEN)", self.name)
                    self.state = CircuitState.OPEN

            raise

    def reset(self) -> None:
        """Manually reset circuit breaker to closed state."""
        logger.info("Circuit breaker %s: Manually reset", self.name)
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.success_count = 0

    def get_state(self) -> CircuitState:
        """Get current circuit breaker state."""
        return self.state

    def get_stats(self) -> dict[str, Any]:
        """Get circuit breaker statistics."""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
            "success_count": self.success_count,
        }

