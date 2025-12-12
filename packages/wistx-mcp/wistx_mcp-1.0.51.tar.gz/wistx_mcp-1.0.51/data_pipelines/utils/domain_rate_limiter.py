"""Per-domain rate limiter for URL fetching.

Prevents overwhelming individual domains with too many concurrent requests.
"""

import asyncio
import logging
from collections import defaultdict
from time import time
from urllib.parse import urlparse

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class DomainRateLimiter:
    """Rate limiter per domain for URL fetching.
    
    Limits the number of requests per domain to avoid overwhelming sites.
    """

    def __init__(
        self,
        max_calls_per_domain: int = 10,
        period_seconds: float = 60.0,
    ):
        """Initialize domain rate limiter.
        
        Args:
            max_calls_per_domain: Maximum calls per domain per period (default: 10)
            period_seconds: Time period in seconds (default: 60 seconds)
        """
        self.max_calls_per_domain = max_calls_per_domain
        self.period_seconds = period_seconds
        
        self._domain_calls: dict[str, list[float]] = defaultdict(list)
        self._domain_locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL.
        
        Args:
            url: Full URL
            
        Returns:
            Domain name (e.g., "example.com")
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split("/")[0]
            if domain.startswith("www."):
                domain = domain[4:]
            return domain.lower()
        except Exception as e:
            logger.warning("Failed to parse domain from URL %s: %s", url, e)
            return "unknown"

    async def acquire(self, url: str) -> None:
        """Acquire permission to fetch a URL (rate limiting).
        
        Blocks until rate limit allows the request.
        
        Args:
            url: URL to fetch
        """
        domain = self._get_domain(url)
        lock = self._domain_locks[domain]
        
        async with lock:
            now = time()
            cutoff = now - self.period_seconds
            
            calls = self._domain_calls[domain]
            calls[:] = [call_time for call_time in calls if call_time > cutoff]
            
            if len(calls) >= self.max_calls_per_domain:
                oldest_call = min(calls)
                wait_time = self.period_seconds - (now - oldest_call) + 0.1
                
                if wait_time > 0:
                    logger.debug(
                        "Rate limit reached for domain %s (%d/%d calls). Waiting %.1fs...",
                        domain,
                        len(calls),
                        self.max_calls_per_domain,
                        wait_time
                    )
                    await asyncio.sleep(wait_time)
                    now = time()
                    cutoff = now - self.period_seconds
                    calls[:] = [call_time for call_time in calls if call_time > cutoff]
            
            calls.append(now)
            logger.debug(
                "Rate limit acquired for domain %s (%d/%d calls)",
                domain,
                len(calls),
                self.max_calls_per_domain
            )

    def get_stats(self) -> dict[str, dict[str, any]]:
        """Get statistics for all domains.
        
        Returns:
            Dictionary mapping domain to rate limit stats
        """
        now = time()
        cutoff = now - self.period_seconds
        
        stats = {}
        for domain, calls in self._domain_calls.items():
            recent_calls = [call_time for call_time in calls if call_time > cutoff]
            stats[domain] = {
                "calls_in_period": len(recent_calls),
                "max_calls": self.max_calls_per_domain,
                "utilization": len(recent_calls) / self.max_calls_per_domain,
            }
        
        return stats

