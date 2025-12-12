"""Per-domain circuit breaker for URL fetching.

Prevents repeatedly trying domains that are consistently failing.
"""

import logging
from collections import defaultdict
from urllib.parse import urlparse

from .circuit_breaker import CircuitBreaker, CircuitBreakerOpenError

logger = logging.getLogger(__name__)


class DomainCircuitBreakerManager:
    """Manages circuit breakers per domain for URL fetching.
    
    Tracks failures per domain and skips domains that are consistently failing.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 3600.0,
        success_threshold: int = 2,
    ):
        """Initialize domain circuit breaker manager.
        
        Args:
            failure_threshold: Number of failures before opening circuit (default: 3)
            recovery_timeout: Seconds to wait before attempting recovery (default: 3600s = 1 hour)
            success_threshold: Number of successes needed to close circuit (default: 2)
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.breakers: dict[str, CircuitBreaker] = defaultdict(
            lambda: CircuitBreaker(
                failure_threshold=failure_threshold,
                recovery_timeout=recovery_timeout,
                success_threshold=success_threshold,
            )
        )

    def get_domain(self, url: str) -> str:
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

    def get_breaker(self, url: str) -> CircuitBreaker:
        """Get circuit breaker for a domain.
        
        Args:
            url: Full URL
            
        Returns:
            Circuit breaker instance for the domain
        """
        domain = self.get_domain(url)
        return self.breakers[domain]

    def is_open(self, url: str) -> bool:
        """Check if circuit breaker is open for a domain.
        
        Args:
            url: Full URL
            
        Returns:
            True if circuit breaker is open (should skip this domain)
        """
        breaker = self.get_breaker(url)
        return breaker.state.value == "open"

    def record_success(self, url: str) -> None:
        """Record successful fetch for a domain.
        
        Args:
            url: Full URL that succeeded
        """
        breaker = self.get_breaker(url)
        try:
            breaker.record_success()
            domain = self.get_domain(url)
            if breaker.state.value == "closed":
                logger.debug("Domain %s circuit breaker CLOSED - service recovered", domain)
        except Exception as e:
            logger.warning("Error recording success for %s: %s", url, e)

    def record_failure(self, url: str) -> None:
        """Record failed fetch for a domain.
        
        Args:
            url: Full URL that failed
        """
        breaker = self.get_breaker(url)
        try:
            breaker.record_failure()
            domain = self.get_domain(url)
            if breaker.state.value == "open":
                logger.warning(
                    "Domain %s circuit breaker OPEN - skipping domain for %d seconds",
                    domain,
                    self.recovery_timeout,
                )
        except Exception as e:
            logger.warning("Error recording failure for %s: %s", url, e)

    def get_stats(self) -> dict[str, dict[str, any]]:
        """Get statistics for all circuit breakers.
        
        Returns:
            Dictionary mapping domain to circuit breaker stats
        """
        stats = {}
        for domain, breaker in self.breakers.items():
            stats[domain] = {
                "state": breaker.state.value,
                "failure_count": breaker.failure_count,
                "success_count": breaker.success_count,
                "last_failure_time": breaker.last_failure_time,
            }
        return stats

