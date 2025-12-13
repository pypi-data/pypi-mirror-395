"""AWS cost data collector with FOCUS mapping."""

import json
from datetime import datetime
from decimal import Decimal
from typing import Any

import httpx

from .base_cost_collector import BaseCostCollector
from ..models.provider_mappings import ServiceCategoryMapper
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class AWSCostCollector(BaseCostCollector):
    """Collect AWS pricing data and map to FOCUS format.

    Uses AWS Pricing API:
    - Endpoint: pricing.us-east-1.amazonaws.com
    - Services: EC2, RDS, S3, Lambda, etc.
    """

    PRICING_API_BASE = "https://pricing.us-east-1.amazonaws.com"
    PRICING_API_VERSION = "1.0"

    AWS_SERVICES = [
        "AmazonEC2",
        "AmazonRDS",
        "AmazonS3",
        "AmazonEBS",
        "AWSLambda",
        "AmazonECS",
        "AmazonEKS",
        "AmazonRedshift",
        "AmazonCloudFront",
        "AmazonVPC",
    ]

    AWS_REGIONS = [
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "eu-west-1",
        "eu-central-1",
        "ap-southeast-1",
        "ap-southeast-2",
        "ap-northeast-1",
    ]

    def __init__(self):
        """Initialize AWS cost collector."""
        super().__init__(provider="aws", rate_limit=(100, 60))
        self.service_mapper = ServiceCategoryMapper()

    async def collect_pricing_data(
        self, region: str | None = None, service: str | None = None
    ) -> list[dict[str, Any]]:
        """Collect AWS pricing data.

        Args:
            region: Optional region filter
            service: Optional service filter

        Returns:
            List of raw pricing data dictionaries
        """
        regions = [region] if region else self.AWS_REGIONS
        services = [service] if service else self.AWS_SERVICES

        all_data = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            for aws_service in services:
                for aws_region in regions:
                    try:
                        data = await self._fetch_service_pricing(client, aws_service, aws_region)
                        all_data.extend(data)
                    except Exception as e:
                        logger.warning(
                            "Failed to fetch pricing for %s in %s: %s",
                            aws_service,
                            aws_region,
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
            service: AWS service name
            region: AWS region

        Returns:
            List of pricing data dictionaries
        """
        url = f"{self.PRICING_API_BASE}/offers/v1.0/aws/{service}/current/{region}/index.json"

        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            pricing_data = []

            products = data.get("products", {})
            terms = data.get("terms", {})

            for product_id, product in products.items():
                attributes = product.get("attributes", {})
                instance_type = attributes.get("instanceType", "")
                tenancy = attributes.get("tenancy", "Shared")
                operating_system = attributes.get("operatingSystem", "")
                location = attributes.get("location", "")

                on_demand_terms = terms.get("OnDemand", {}).get(product_id, {})
                pricing_dimensions = {}

                for term_key, term_value in on_demand_terms.items():
                    price_dimensions = term_value.get("priceDimensions", {})
                    for price_key, price_dim in price_dimensions.items():
                        price_per_unit = price_dim.get("pricePerUnit", {})
                        usd_price = price_per_unit.get("USD", "0")
                        unit = price_dim.get("unit", "Hrs")

                        pricing_dimensions[price_key] = {
                            "price": Decimal(usd_price),
                            "unit": unit,
                        }

                if pricing_dimensions:
                    raw_data = {
                        "service": service,
                        "region": region,
                        "product_id": product_id,
                        "instance_type": instance_type,
                        "tenancy": tenancy,
                        "operating_system": operating_system,
                        "location": location,
                        "attributes": attributes,
                        "pricing": pricing_dimensions,
                        "sku_id": product_id,
                    }

                    pricing_data.append(raw_data)

            return pricing_data

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error fetching AWS pricing: %s", e)
            return []
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
            return []
        except Exception as e:
            logger.error("Unexpected error fetching AWS pricing: %s", e)
            return []

    def map_to_focus(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Map AWS raw data to FOCUS format.

        Args:
            raw_data: AWS raw pricing data

        Returns:
            FOCUS-compliant data dictionary
        """
        service = raw_data.get("service", "")
        region = raw_data.get("region", "")
        instance_type = raw_data.get("instance_type", "")
        product_id = raw_data.get("product_id", "")
        attributes = raw_data.get("attributes", {})
        pricing = raw_data.get("pricing", {})

        service_description = attributes.get("servicecodeDescription") or attributes.get("description", "")
        service_category = self.service_mapper.get_service_category("aws", service, service_description)

        first_pricing = next(iter(pricing.values())) if pricing else {}
        list_unit_price = first_pricing.get("price", Decimal("0"))
        pricing_unit = first_pricing.get("unit", "Hrs")

        billing_period_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        billing_period_end = datetime.utcnow()

        focus_data = {
            "billing_account_id": "aws-default",
            "billing_account_name": "AWS Default Account",
            "billing_currency": "USD",
            "billing_period_start": billing_period_start,
            "billing_period_end": billing_period_end,
            "provider": "aws",
            "invoice_issuer": "Amazon Web Services",
            "publisher": None,
            "region_id": region,
            "region_name": self._get_region_name(region),
            "availability_zone": None,
            "resource_id": product_id,
            "resource_name": f"{service} {instance_type}",
            "resource_type": instance_type or "default",
            "service_category": service_category,
            "service_name": service,
            "service_subcategory": raw_data.get("tenancy", "Shared"),
            "sku_id": product_id,
            "sku_description": attributes.get("usagetype", ""),
            "sku_price_id": product_id,
            "pricing_category": "OnDemand",
            "pricing_quantity": 1.0,
            "pricing_unit": pricing_unit,
            "list_cost": list_unit_price,
            "list_unit_price": list_unit_price,
            "effective_cost": list_unit_price,
            "billed_cost": list_unit_price,
            "contracted_cost": None,
            "consumed_quantity": 1.0,
            "consumed_unit": pricing_unit,
            "charge_category": "Usage",
            "charge_description": f"{service} {instance_type} in {region}",
            "charge_frequency": "Hourly",
            "charge_period_start": billing_period_start,
            "charge_period_end": billing_period_end,
            "tags": {
                "operating_system": raw_data.get("operating_system", ""),
                "tenancy": raw_data.get("tenancy", ""),
            },
            "sub_account_id": None,
            "sub_account_name": None,
        }

        return focus_data

    def _get_region_name(self, region_id: str) -> str:
        """Get human-readable region name.

        Args:
            region_id: AWS region ID

        Returns:
            Region name
        """
        region_names = {
            "us-east-1": "US East (N. Virginia)",
            "us-east-2": "US East (Ohio)",
            "us-west-1": "US West (N. California)",
            "us-west-2": "US West (Oregon)",
            "eu-west-1": "Europe (Ireland)",
            "eu-central-1": "Europe (Frankfurt)",
            "ap-southeast-1": "Asia Pacific (Singapore)",
            "ap-southeast-2": "Asia Pacific (Sydney)",
            "ap-northeast-1": "Asia Pacific (Tokyo)",
        }
        return region_names.get(region_id, region_id)

