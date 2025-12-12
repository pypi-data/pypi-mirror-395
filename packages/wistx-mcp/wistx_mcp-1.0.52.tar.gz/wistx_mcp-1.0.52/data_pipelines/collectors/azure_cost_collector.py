"""Azure cost data collector with FOCUS mapping."""

import json
from datetime import datetime
from decimal import Decimal
from typing import Any

import httpx

from .base_cost_collector import BaseCostCollector
from ..models.provider_mappings import ServiceCategoryMapper
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class AzureCostCollector(BaseCostCollector):
    """Collect Azure pricing data and map to FOCUS format.

    Uses Azure Retail Prices API:
    - Endpoint: prices.azure.com/api/retail/prices
    - No authentication required for public pricing
    """

    PRICING_API_BASE = "https://prices.azure.com/api/retail/prices"

    AZURE_SERVICES = [
        "Virtual Machines",
        "Storage",
        "SQL Database",
        "Cosmos DB",
        "Azure Functions",
        "Container Instances",
    ]

    AZURE_REGIONS = [
        "eastus",
        "eastus2",
        "westus",
        "westus2",
        "westeurope",
        "northeurope",
        "southeastasia",
    ]

    def __init__(self):
        """Initialize Azure cost collector."""
        super().__init__(provider="azure", rate_limit=(100, 60))
        self.service_mapper = ServiceCategoryMapper()

    async def collect_pricing_data(
        self, region: str | None = None, service: str | None = None
    ) -> list[dict[str, Any]]:
        """Collect Azure pricing data.

        Args:
            region: Optional region filter
            service: Optional service filter

        Returns:
            List of raw pricing data dictionaries
        """
        regions = [region] if region else self.AZURE_REGIONS
        services = [service] if service else self.AZURE_SERVICES

        all_data = []

        async with httpx.AsyncClient(timeout=60.0) as client:
            for azure_service in services:
                for azure_region in regions:
                    try:
                        data = await self._fetch_service_pricing(client, azure_service, azure_region)
                        all_data.extend(data)
                    except Exception as e:
                        logger.warning(
                            "Failed to fetch pricing for %s in %s: %s",
                            azure_service,
                            azure_region,
                            e,
                        )
                        continue

        return all_data

    async def _fetch_service_pricing(
        self, client: httpx.AsyncClient, service: str, region: str
    ) -> list[dict[str, Any]]:
        """Fetch pricing for a specific service and region.

        Args:
            client: HTTP client
            service: Azure service name
            region: Azure region

        Returns:
            List of pricing data dictionaries
        """
        all_items = []
        next_page_url = None

        while True:
            if next_page_url:
                url = next_page_url
                params = {}
            else:
                url = self.PRICING_API_BASE
                params = {
                    "$filter": f"serviceName eq '{service}' and armRegionName eq '{region}'",
                }

            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                items = data.get("Items", [])
                all_items.extend(items)

                next_page_url = data.get("NextPageLink")
                if not next_page_url:
                    break

            except httpx.HTTPStatusError as e:
                logger.error("HTTP error fetching Azure pricing: %s", e)
                break
            except json.JSONDecodeError as e:
                logger.error("JSON decode error: %s", e)
                break

        pricing_data = []
        for item in all_items:
            raw_data = {
                "service": service,
                "region": region,
                "meter_name": item.get("meterName", ""),
                "meter_category": item.get("meterCategory", ""),
                "meter_subcategory": item.get("meterSubCategory", ""),
                "unit_of_measure": item.get("unitOfMeasure", ""),
                "retail_price": item.get("retailPrice", 0),
                "currency_code": item.get("currencyCode", "USD"),
                "arm_region_name": item.get("armRegionName", ""),
                "sku_id": item.get("skuId", ""),
                "product_name": item.get("productName", ""),
                "item": item,
            }
            pricing_data.append(raw_data)

        return pricing_data

    def map_to_focus(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Map Azure raw data to FOCUS format.

        Args:
            raw_data: Azure raw pricing data

        Returns:
            FOCUS-compliant data dictionary
        """
        service = raw_data.get("service", "")
        region = raw_data.get("region", "")
        meter_name = raw_data.get("meter_name", "")
        meter_category = raw_data.get("meter_category", "")
        meter_subcategory = raw_data.get("meter_subcategory", "")
        unit_of_measure = raw_data.get("unit_of_measure", "")
        retail_price = Decimal(str(raw_data.get("retail_price", 0)))
        currency_code = raw_data.get("currency_code", "USD")
        sku_id = raw_data.get("sku_id", "")
        product_name = raw_data.get("product_name", "")

        service_description = product_name or meter_category or meter_subcategory or ""
        service_category = self.service_mapper.get_service_category("azure", service, service_description)

        billing_period_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        billing_period_end = datetime.utcnow()

        focus_data = {
            "billing_account_id": "azure-default",
            "billing_account_name": "Azure Default Subscription",
            "billing_currency": currency_code,
            "billing_period_start": billing_period_start,
            "billing_period_end": billing_period_end,
            "provider": "azure",
            "invoice_issuer": "Microsoft Corporation",
            "publisher": None,
            "region_id": region,
            "region_name": self._get_region_name(region),
            "availability_zone": None,
            "resource_id": sku_id or product_name,
            "resource_name": product_name or meter_name,
            "resource_type": meter_subcategory or meter_category,
            "service_category": service_category,
            "service_name": service,
            "service_subcategory": meter_subcategory,
            "sku_id": sku_id or meter_name,
            "sku_description": meter_name,
            "sku_price_id": sku_id or meter_name,
            "pricing_category": "OnDemand",
            "pricing_quantity": 1.0,
            "pricing_unit": unit_of_measure,
            "list_cost": retail_price,
            "list_unit_price": retail_price,
            "effective_cost": retail_price,
            "billed_cost": retail_price,
            "contracted_cost": None,
            "consumed_quantity": 1.0,
            "consumed_unit": unit_of_measure,
            "charge_category": "Usage",
            "charge_description": f"{service} {meter_name} in {region}",
            "charge_frequency": "Hourly" if "hour" in unit_of_measure.lower() else "Monthly",
            "charge_period_start": billing_period_start,
            "charge_period_end": billing_period_end,
            "tags": {
                "meter_category": meter_category,
                "meter_subcategory": meter_subcategory,
            },
            "sub_account_id": None,
            "sub_account_name": None,
        }

        return focus_data

    def _get_region_name(self, region_id: str) -> str:
        """Get human-readable region name.

        Args:
            region_id: Azure region ID

        Returns:
            Region name
        """
        region_names = {
            "eastus": "East US",
            "eastus2": "East US 2",
            "westus": "West US",
            "westus2": "West US 2",
            "westeurope": "West Europe",
            "northeurope": "North Europe",
            "southeastasia": "Southeast Asia",
        }
        return region_names.get(region_id, region_id)

