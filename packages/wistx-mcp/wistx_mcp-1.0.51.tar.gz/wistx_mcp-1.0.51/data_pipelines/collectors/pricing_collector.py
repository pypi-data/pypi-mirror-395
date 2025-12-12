"""Cost data collector orchestrator for all cloud providers."""

from typing import Any

from .aws_cost_collector import AWSCostCollector
from .azure_cost_collector import AzureCostCollector
from .gcp_cost_collector import GCPCostCollector
from .oracle_cost_collector import OracleCostCollector
from .alibaba_cost_collector import AlibabaCostCollector
from ..collectors.collection_result import CollectionResult
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class CostDataCollector:
    """Main collector that orchestrates all cloud provider cost collectors."""

    def __init__(self):
        """Initialize cost data collector."""
        self.collectors = {
            "aws": AWSCostCollector(),
            "gcp": GCPCostCollector(),
            "azure": AzureCostCollector(),
            "oracle": OracleCostCollector(),
            "alibaba": AlibabaCostCollector(),
        }

    async def collect_all(
        self,
        providers: list[str] | None = None,
        regions: list[str] | None = None,
        services: list[str] | None = None,
        max_providers: int | None = None,
        max_regions: int | None = None,
        max_services: int | None = None,
        max_records: int | None = None,
    ) -> dict[str, CollectionResult]:
        """Collect cost data from all providers with limits enforced during collection.
        
        Limits are applied DURING collection to avoid unnecessary API calls:
        - max_services: Limits number of services processed per provider
        - max_regions: Limits number of regions processed per provider  
        - max_records: Stops collection once limit is reached (per provider)

        Args:
            providers: Optional list of providers to collect (default: all)
            regions: Optional list of regions to collect (default: all)
            services: Optional list of services to collect (default: all)
            max_providers: Maximum number of providers to process (None for all)
            max_regions: Maximum number of regions per provider (None for all)
            max_services: Maximum number of services per provider (None for all)
            max_records: Maximum number of cost records per provider (None for all)

        Returns:
            Dictionary mapping provider names to CollectionResult
        """
        if providers is None:
            providers = list(self.collectors.keys())

        if max_providers:
            providers = providers[:max_providers]
            logger.info("Limited to %d providers: %s", max_providers, providers)

        results = {}

        for provider in providers:
            if provider not in self.collectors:
                logger.warning("Unknown provider: %s", provider)
                continue

            try:
                logger.info("Collecting cost data from %s...", provider)

                collector = self.collectors[provider]
                
                if provider == "gcp":
                    has_service_account = (
                        hasattr(collector, "service_account_key_path")
                        and collector.service_account_key_path
                    ) or (
                        hasattr(collector, "service_account_key_json")
                        and collector.service_account_key_json
                    )
                    api_key = getattr(collector, "api_key", None)
                    has_api_key = api_key and isinstance(api_key, str) and api_key.strip()
                    
                    if not has_service_account and not has_api_key:
                        logger.warning(
                            "GCP credentials not configured. Skipping GCP collection. "
                            "Set GCP_SERVICE_ACCOUNT_KEY_PATH, GCP_SERVICE_ACCOUNT_KEY_JSON, "
                            "or GCP_API_KEY environment variable to enable GCP data collection."
                        )
                        results[provider] = CollectionResult(
                            provider=provider,
                            success=False,
                            items=[],
                        )
                        results[provider].add_error("config", "MissingCredentials", "GCP credentials not configured")
                        continue
                    else:
                        if has_service_account:
                            logger.debug("GCP service account credentials found, proceeding with collection")
                        else:
                            logger.debug("GCP API key found, proceeding with collection (fallback mode)")
                
                if regions is None:
                    default_regions = self._get_default_regions(provider, collector)
                    provider_regions = default_regions[:max_regions] if max_regions else default_regions
                else:
                    provider_regions = regions[:max_regions] if max_regions else regions
                
                if services is None:
                    default_services = self._get_default_services(provider, collector)
                    provider_services = default_services[:max_services] if max_services else default_services
                else:
                    provider_services = services[:max_services] if max_services else services

                if max_regions:
                    logger.info("Limited to %d regions for %s: %s", max_regions, provider, provider_regions)
                if max_services:
                    logger.info("Limited to %d services for %s: %s", max_services, provider, provider_services)
                if max_records:
                    logger.info("Limited to %d records for %s", max_records, provider)

                if provider == "gcp" and hasattr(collector, "collect_with_limits"):
                    result = await collector.collect_with_limits(
                        regions=provider_regions,
                        services=provider_services,
                        max_services=max_services,
                        max_regions=max_regions,
                        max_records=max_records,
                    )
                else:
                    result = await collector.collect(
                        regions=provider_regions,
                        services=provider_services,
                    )

                    if max_records and len(result.items) > max_records:
                        logger.info(
                            "Limiting %s to %d records (collected %d)",
                            provider,
                            max_records,
                            len(result.items),
                        )
                        result.items = result.items[:max_records]

                results[provider] = result
                
                if len(result.items) == 0:
                    logger.warning(
                        "No data collected from %s. Check logs for errors or missing configuration.",
                        provider,
                    )
                else:
                    logger.info(
                        "Collected %d items from %s",
                        len(result.items),
                        provider,
                    )

            except Exception as e:
                logger.error("Error collecting from %s: %s", provider, e, exc_info=True)
                results[provider] = CollectionResult(
                    collector_name=f"{provider}-cost",
                    version="1.0",
                    success=False,
                )

        return results

    def _get_default_regions(self, provider: str, collector: Any) -> list[str]:
        """Get default regions for a provider.
        
        Args:
            provider: Provider name
            collector: Collector instance
            
        Returns:
            List of default regions
        """
        if provider == "aws" and hasattr(collector, "AWS_REGIONS"):
            return collector.AWS_REGIONS
        elif provider == "gcp" and hasattr(collector, "GCP_REGIONS"):
            return collector.GCP_REGIONS
        elif provider == "azure" and hasattr(collector, "AZURE_REGIONS"):
            return collector.AZURE_REGIONS
        elif provider == "oracle" and hasattr(collector, "ORACLE_REGIONS"):
            return collector.ORACLE_REGIONS
        elif provider == "alibaba" and hasattr(collector, "ALIBABA_REGIONS"):
            return collector.ALIBABA_REGIONS
        return []

    def _get_default_services(self, provider: str, collector: Any) -> list[str]:
        """Get default services for a provider.
        
        Args:
            provider: Provider name
            collector: Collector instance
            
        Returns:
            List of default services
        """
        if provider == "aws" and hasattr(collector, "AWS_SERVICES"):
            return collector.AWS_SERVICES
        elif provider == "gcp":
            return []
        elif provider == "azure" and hasattr(collector, "AZURE_SERVICES"):
            return collector.AZURE_SERVICES
        elif provider == "oracle" and hasattr(collector, "ORACLE_SERVICES"):
            return collector.ORACLE_SERVICES
        elif provider == "alibaba" and hasattr(collector, "ALIBABA_SERVICES"):
            return collector.ALIBABA_SERVICES
        return []

    async def collect_provider(
        self,
        provider: str,
        regions: list[str] | None = None,
        services: list[str] | None = None,
    ) -> CollectionResult:
        """Collect cost data from a specific provider.

        Args:
            provider: Provider name (aws, gcp, azure)
            regions: Optional list of regions
            services: Optional list of services

        Returns:
            CollectionResult
        """
        if provider not in self.collectors:
            raise ValueError(f"Unknown provider: {provider}")

        collector = self.collectors[provider]
        return await collector.collect(regions=regions, services=services)
