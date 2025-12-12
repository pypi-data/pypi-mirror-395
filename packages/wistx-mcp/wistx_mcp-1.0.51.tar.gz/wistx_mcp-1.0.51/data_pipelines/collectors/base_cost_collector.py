"""Base cost data collector for cloud providers."""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

from ..collectors.collection_result import CollectionMetrics, CollectionResult
from ..utils.circuit_breaker import CircuitBreaker
from ..utils.logger import setup_logger
from ..utils.rate_limiter import RateLimiter
from ..utils.retry_handler import RetryHandler

logger = setup_logger(__name__)


class BaseCostCollector(ABC):
    """Base collector for cloud provider cost data.

    Provides shared functionality:
    - Rate limiting
    - Retry logic with exponential backoff
    - Circuit breaker pattern
    - Error handling
    - Metrics collection
    """

    def __init__(
        self,
        provider: str,
        rate_limit: tuple[int, float] = (100, 60),
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize base cost collector.

        Args:
            provider: Cloud provider name (aws, gcp, azure, oracle, alibaba)
            rate_limit: Rate limit tuple (max_calls, period_seconds)
            max_retries: Maximum retry attempts
            retry_delay: Base retry delay in seconds
        """
        self.provider = provider
        self.rate_limiter = RateLimiter(max_calls=rate_limit[0], period=rate_limit[1])
        self.retry_handler = RetryHandler(
            max_retries=max_retries,
            base_delay=retry_delay,
            exponential_base=2.0,
        )
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60.0,
            success_threshold=2,
        )

    @abstractmethod
    async def collect_pricing_data(
        self, region: str | None = None, service: str | None = None
    ) -> list[dict[str, Any]]:
        """Collect pricing data from provider.

        Args:
            region: Optional region filter
            service: Optional service filter

        Returns:
            List of raw pricing data dictionaries
        """
        pass

    @abstractmethod
    def map_to_focus(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Map provider-specific data to FOCUS format.

        Args:
            raw_data: Provider-specific raw data

        Returns:
            FOCUS-compliant data dictionary
        """
        pass

    async def collect(
        self,
        regions: list[str] | None = None,
        services: list[str] | None = None,
        billing_period_start: datetime | None = None,
        billing_period_end: datetime | None = None,
    ) -> CollectionResult:
        """Collect cost data from provider.

        Args:
            regions: Optional list of regions to collect
            services: Optional list of services to collect
            billing_period_start: Optional billing period start
            billing_period_end: Optional billing period end

        Returns:
            CollectionResult with collected data
        """
        result = CollectionResult(
            collector_name=f"{self.provider}-cost",
            version="1.0",
            success=False,
        )
        result.metrics.start_time = datetime.utcnow()

        if billing_period_start is None:
            billing_period_start = datetime.utcnow() - timedelta(days=30)
        if billing_period_end is None:
            billing_period_end = datetime.utcnow()

        try:
            all_data = []

            if regions:
                for region in regions:
                    if services:
                        for service in services:
                            data = await self._collect_with_retry(region, service)
                            all_data.extend(data)
                    else:
                        data = await self._collect_with_retry(region, None)
                        all_data.extend(data)
            else:
                data = await self._collect_with_retry(None, None)
                all_data.extend(data)

            result.items = all_data
            result.metrics.items_collected = len(all_data)
            result.metrics.successful_urls = 1
            result.success = True

        except Exception as e:
            logger.error("Error collecting cost data from %s: %s", self.provider, e, exc_info=True)
            result.add_error("api", type(e).__name__, str(e))
            result.metrics.failed_urls = 1

        finally:
            result.finalize()

        return result

    async def _collect_with_retry(
        self, region: str | None, service: str | None
    ) -> list[dict[str, Any]]:
        """Collect data with retry logic.

        Args:
            region: Optional region
            service: Optional service

        Returns:
            List of raw data dictionaries
        """
        async def _collect() -> list[dict[str, Any]]:
            await self.rate_limiter.acquire()
            return await self.collect_pricing_data(region=region, service=service)

        try:
            return await self.retry_handler.execute(_collect)
        except Exception as e:
            logger.error(
                "Failed to collect cost data from %s (region=%s, service=%s): %s",
                self.provider,
                region,
                service,
                e,
            )
            return []

