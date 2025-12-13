"""Rate limiting utilities for API calls."""

import asyncio
import threading
import time
from collections import deque
from typing import Callable, TypeVar

T = TypeVar("T")


class RateLimiter:
    """Token bucket rate limiter for API calls.

    Thread-safe implementation using locks.
    Ensures API calls don't exceed specified rate limits.
    """

    def __init__(self, max_calls: int, period: float):
        """Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: deque[float] = deque()
        self.lock = threading.Lock()

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator to rate limit a function.

        Args:
            func: Function to rate limit

        Returns:
            Wrapped function with rate limiting
        """

        def wrapper(*args, **kwargs) -> T:
            with self.lock:
                now = time.time()

                while self.calls and self.calls[0] < now - self.period:
                    self.calls.popleft()

                if len(self.calls) >= self.max_calls:
                    sleep_time = self.period - (now - self.calls[0])
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                        return wrapper(*args, **kwargs)

                self.calls.append(time.time())

            return func(*args, **kwargs)

        return wrapper

    def reset(self) -> None:
        """Reset the rate limiter."""
        with self.lock:
            self.calls.clear()

    async def acquire(self) -> None:
        """Acquire rate limit permission asynchronously.

        Waits if necessary until rate limit allows the call.
        Uses asyncio.sleep() for non-blocking waits.
        """
        while True:
            with self.lock:
                now = time.time()

                while self.calls and self.calls[0] < now - self.period:
                    self.calls.popleft()

                if len(self.calls) < self.max_calls:
                    self.calls.append(now)
                    return

                sleep_time = self.period - (now - self.calls[0])

            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
