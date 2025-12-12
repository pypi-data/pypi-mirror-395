"""Alibaba Cloud cost data collector with FOCUS mapping."""

import base64
import hashlib
import hmac
import json
from datetime import datetime
from decimal import Decimal
from typing import Any
from urllib.parse import quote, urlencode

import httpx

from .base_cost_collector import BaseCostCollector
from ..models.provider_mappings import ServiceCategoryMapper
from ..utils.config import PipelineSettings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
settings = PipelineSettings()


class AlibabaCostCollector(BaseCostCollector):
    """Collect Alibaba Cloud pricing data and map to FOCUS format.

    Uses Alibaba Cloud OpenAPI:
    - Billing API: https://bssopenapi.aliyun.com
    - Product API: QueryProductList, DescribeProductList, DescribePricingModule
    
    Reference: https://next.api.alibabacloud.com/
    """

    BILLING_API_BASE = "https://bssopenapi.aliyun.com"
    ECS_API_BASE = "https://ecs.aliyuncs.com"

    ALIBABA_SERVICES = [
        "ECS",
        "OSS",
        "RDS",
        "Function Compute",
        "SLB",
        "CDN",
        "WAF",
    ]

    ALIBABA_REGIONS = [
        "cn-hangzhou",
        "cn-shanghai",
        "cn-beijing",
        "us-east-1",
        "us-west-1",
        "ap-southeast-1",
    ]

    def __init__(self):
        """Initialize Alibaba Cloud cost collector."""
        super().__init__(provider="alibaba", rate_limit=(50, 60))
        self.service_mapper = ServiceCategoryMapper()
        self.access_key_id = settings.alibaba_access_key_id
        self.access_key_secret = settings.alibaba_access_key_secret

    async def collect_pricing_data(
        self, region: str | None = None, service: str | None = None
    ) -> list[dict[str, Any]]:
        """Collect Alibaba Cloud pricing data.

        Args:
            region: Optional region filter
            service: Optional service filter

        Returns:
            List of raw pricing data dictionaries
        """
        if not self.access_key_id or not self.access_key_secret:
            logger.warning("Alibaba Cloud credentials not configured. Skipping Alibaba collection.")
            return []

        regions = [region] if region else self.ALIBABA_REGIONS
        services = [service] if service else self.ALIBABA_SERVICES

        all_data = []

        async with httpx.AsyncClient(timeout=60.0) as client:
            for alibaba_service in services:
                for alibaba_region in regions:
                    try:
                        data = await self._fetch_service_pricing(client, alibaba_service, alibaba_region)
                        all_data.extend(data)
                    except Exception as e:
                        logger.warning(
                            "Failed to fetch pricing for %s in %s: %s",
                            alibaba_service,
                            alibaba_region,
                            e,
                        )
                        continue

        return all_data

    def _sign_request(self, params: dict[str, Any]) -> str:
        """Sign Alibaba Cloud API request using HMAC-SHA1.

        Args:
            params: Request parameters

        Returns:
            Signature string
        """
        sorted_params = sorted(params.items())
        canonical_query_string = "&".join(
            [f"{quote(str(k), safe='')}={quote(str(v), safe='')}" for k, v in sorted_params]
        )

        string_to_sign = f"GET&%2F&{quote(canonical_query_string, safe='')}"

        signature = base64.b64encode(
            hmac.new(
                f"{self.access_key_secret}&".encode(),
                string_to_sign.encode(),
                hashlib.sha1,
            ).digest()
        ).decode()

        return signature

    async def _fetch_service_pricing(
        self, client: httpx.AsyncClient, service: str, region: str
    ) -> list[dict[str, Any]]:
        """Fetch pricing for a specific service and region using Alibaba OpenAPI.

        Args:
            client: HTTP client
            service: Alibaba service name
            region: Alibaba region

        Returns:
            List of pricing data dictionaries
        """
        pricing_data = []

        try:
            product_code = self._get_product_code(service)
            
            params = {
                "Format": "JSON",
                "Version": "2017-12-14",
                "AccessKeyId": self.access_key_id,
                "SignatureMethod": "HMAC-SHA1",
                "Timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "SignatureVersion": "1.0",
                "SignatureNonce": str(int(datetime.utcnow().timestamp() * 1000)),
                "Action": "QueryProductList",
                "ProductCode": product_code,
                "RegionId": region,
            }

            signature = self._sign_request(params)
            params["Signature"] = signature

            url = f"{self.BILLING_API_BASE}/"
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("Code") == "Success":
                products = data.get("Data", {}).get("ProductList", [])
                for product in products:
                    raw_data = {
                        "service": service,
                        "region": region,
                        "product_code": product.get("ProductCode", ""),
                        "product_name": product.get("ProductName", ""),
                        "price": product.get("Price", 0),
                        "currency": product.get("Currency", "CNY"),
                        "unit": product.get("ChargeType", "hour"),
                        "product": product,
                    }
                    pricing_data.append(raw_data)
            else:
                logger.warning(
                    "Alibaba API returned error: %s - %s",
                    data.get("Code"),
                    data.get("Message"),
                )

            pricing_module = await self._fetch_pricing_module(client, product_code, region)
            pricing_data.extend(pricing_module)

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error fetching Alibaba pricing: %s", e)
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
        except Exception as e:
            logger.error("Unexpected error fetching Alibaba pricing: %s", e)

        return pricing_data

    async def _fetch_pricing_module(
        self, client: httpx.AsyncClient, product_code: str, region: str
    ) -> list[dict[str, Any]]:
        """Fetch pricing module details for a product.

        Args:
            client: HTTP client
            product_code: Product code
            region: Alibaba region

        Returns:
            List of pricing module data dictionaries
        """
        pricing_data = []

        try:
            params = {
                "Format": "JSON",
                "Version": "2017-12-14",
                "AccessKeyId": self.access_key_id,
                "SignatureMethod": "HMAC-SHA1",
                "Timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "SignatureVersion": "1.0",
                "SignatureNonce": str(int(datetime.utcnow().timestamp() * 1000)),
                "Action": "DescribePricingModule",
                "ProductCode": product_code,
                "RegionId": region,
            }

            signature = self._sign_request(params)
            params["Signature"] = signature

            url = f"{self.BILLING_API_BASE}/"
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("Code") == "Success":
                modules = data.get("Data", {}).get("ModuleList", {}).get("Module", [])
                for module in modules:
                    raw_data = {
                        "service": product_code,
                        "region": region,
                        "product_code": product_code,
                        "module_code": module.get("ModuleCode", ""),
                        "module_name": module.get("ModuleName", ""),
                        "price": module.get("Price", {}).get("Value", 0),
                        "currency": module.get("Price", {}).get("Currency", "CNY"),
                        "unit": module.get("Unit", "hour"),
                        "module": module,
                    }
                    pricing_data.append(raw_data)

        except Exception as e:
            logger.debug("Error fetching pricing module: %s", e)

        return pricing_data

    def _get_product_code(self, service: str) -> str:
        """Get Alibaba product code for service.

        Args:
            service: Service name

        Returns:
            Product code
        """
        product_codes = {
            "ECS": "ecs",
            "OSS": "oss",
            "RDS": "rds",
            "Function Compute": "fc",
            "SLB": "slb",
            "CDN": "cdn",
            "WAF": "waf",
        }
        return product_codes.get(service, service.lower().replace(" ", "-"))


    def map_to_focus(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Map Alibaba raw data to FOCUS format.

        Args:
            raw_data: Alibaba raw pricing data

        Returns:
            FOCUS-compliant data dictionary
        """
        service = raw_data.get("service", "")
        region = raw_data.get("region", "")
        product_code = raw_data.get("product_code", "")
        product_name = raw_data.get("product_name", "")
        price = Decimal(str(raw_data.get("price", 0)))
        currency = raw_data.get("currency", "CNY")
        unit = raw_data.get("unit", "hour")

        service_description = product_name or product_code or ""
        service_category = self.service_mapper.get_service_category("alibaba", service, service_description)

        billing_period_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        billing_period_end = datetime.utcnow()

        focus_data = {
            "billing_account_id": "alibaba-default",
            "billing_account_name": "Alibaba Cloud Default Account",
            "billing_currency": currency,
            "billing_period_start": billing_period_start,
            "billing_period_end": billing_period_end,
            "provider": "alibaba",
            "invoice_issuer": "Alibaba Cloud",
            "publisher": None,
            "region_id": region,
            "region_name": self._get_region_name(region),
            "availability_zone": None,
            "resource_id": product_code,
            "resource_name": product_name or f"{service} in {region}",
            "resource_type": service.lower().replace(" ", "-"),
            "service_category": service_category,
            "service_name": service,
            "service_subcategory": None,
            "sku_id": product_code,
            "sku_description": product_name or f"{service} service",
            "sku_price_id": product_code,
            "pricing_category": "OnDemand",
            "pricing_quantity": 1.0,
            "pricing_unit": unit,
            "list_cost": price,
            "list_unit_price": price,
            "effective_cost": price,
            "billed_cost": price,
            "contracted_cost": None,
            "consumed_quantity": 1.0,
            "consumed_unit": unit,
            "charge_category": "Usage",
            "charge_description": f"{service} {product_name} in {region}",
            "charge_frequency": "Hourly" if "hour" in unit.lower() else "Monthly",
            "charge_period_start": billing_period_start,
            "charge_period_end": billing_period_end,
            "tags": {},
            "sub_account_id": None,
            "sub_account_name": None,
        }

        return focus_data

    def _get_region_name(self, region_id: str) -> str:
        """Get human-readable region name.

        Args:
            region_id: Alibaba region ID

        Returns:
            Region name
        """
        region_names = {
            "cn-hangzhou": "China (Hangzhou)",
            "cn-shanghai": "China (Shanghai)",
            "cn-beijing": "China (Beijing)",
            "us-east-1": "US East",
            "us-west-1": "US West",
            "ap-southeast-1": "Asia Pacific (Southeast)",
        }
        return region_names.get(region_id, region_id)

