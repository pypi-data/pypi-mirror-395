"""Global rate limiter for external API calls (Gemini, Pinecone, etc.)."""

import asyncio
import time
from collections import deque
from typing import Any

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class GlobalRateLimiter:
    """Global async rate limiter for external API calls.
    
    Thread-safe and async-safe implementation using asyncio locks.
    Prevents exceeding rate limits for external APIs across all pipeline instances.
    """

    _instance: "GlobalRateLimiter | None" = None
    _lock = asyncio.Lock()

    def __init__(self, max_calls: int = 100, period: float = 60.0):
        """Initialize global rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed per period
            period: Time period in seconds (default: 60 seconds = 1 minute)
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: deque[float] = deque()
        self._async_lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls, max_calls: int = 100, period: float = 60.0) -> "GlobalRateLimiter":
        """Get singleton instance of global rate limiter.
        
        Args:
            max_calls: Maximum calls per period
            period: Time period in seconds
            
        Returns:
            GlobalRateLimiter instance
        """
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(max_calls=max_calls, period=period)
                    logger.info("Initialized global rate limiter: %d calls per %.1f seconds", max_calls, period)
        return cls._instance

    async def acquire(self) -> None:
        """Acquire rate limit permission asynchronously.
        
        Waits if necessary until rate limit allows the call.
        Uses asyncio.sleep() for non-blocking waits.
        """
        async with self._async_lock:
            now = time.time()

            while self.calls and self.calls[0] < now - self.period:
                self.calls.popleft()

            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return

            sleep_time = self.period - (now - self.calls[0])

        if sleep_time > 0:
            logger.debug("Rate limit: waiting %.2f seconds before next API call", sleep_time)
            await asyncio.sleep(sleep_time)
            await self.acquire()

    def reset(self) -> None:
        """Reset the rate limiter (for testing)."""
        self.calls.clear()

    def get_remaining_calls(self) -> int:
        """Get remaining calls in current period.
        
        Returns:
            Number of remaining calls
        """
        now = time.time()
        while self.calls and self.calls[0] < now - self.period:
            self.calls.popleft()
        return max(0, self.max_calls - len(self.calls))

    async def update_limits(self, max_calls: int | None = None, period: float | None = None) -> None:
        """Update rate limits dynamically (thread-safe).
        
        Allows runtime reconfiguration of rate limits without restarting the application.
        Useful for scaling up/down based on API tier or workload requirements.
        
        Args:
            max_calls: New maximum calls per period (None to keep current)
            period: New time period in seconds (None to keep current)
        """
        async with self._async_lock:
            old_max_calls = self.max_calls
            old_period = self.period
            
            if max_calls is not None:
                if max_calls < 1:
                    raise ValueError("max_calls must be at least 1")
                self.max_calls = max_calls
                logger.info("Rate limiter max_calls updated: %d -> %d", old_max_calls, max_calls)
            
            if period is not None:
                if period <= 0:
                    raise ValueError("period must be positive")
                self.period = period
                logger.info("Rate limiter period updated: %.1f -> %.1f seconds", old_period, period)
            
            if max_calls is not None or period is not None:
                logger.info(
                    "Rate limiter updated: %d calls per %.1f seconds",
                    self.max_calls,
                    self.period
                )


_global_rate_limiter: GlobalRateLimiter | None = None


async def get_global_rate_limiter(
    max_calls: int = 100, period: float = 60.0
) -> GlobalRateLimiter:
    """Get global rate limiter instance.
    
    Args:
        max_calls: Maximum calls per period
        period: Time period in seconds
        
    Returns:
        GlobalRateLimiter instance
    """
    return await GlobalRateLimiter.get_instance(max_calls=max_calls, period=period)

