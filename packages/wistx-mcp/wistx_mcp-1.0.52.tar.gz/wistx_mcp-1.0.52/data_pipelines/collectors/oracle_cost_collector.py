"""Oracle Cloud cost data collector with FOCUS mapping."""

import base64
import json
from datetime import datetime
from decimal import Decimal
from typing import Any
from urllib.parse import urlencode

import httpx

from .base_cost_collector import BaseCostCollector
from ..models.provider_mappings import ServiceCategoryMapper
from ..utils.config import PipelineSettings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
settings = PipelineSettings()


class OracleCostCollector(BaseCostCollector):
    """Collect Oracle Cloud pricing data and map to FOCUS format.

    Uses Oracle Cloud Infrastructure (OCI) REST APIs:
    - Cost Management API: /20190111/usageCosts
    - Pricing API: /20181001/pricing
    
    Reference: https://docs.public.content.oci.oraclecloud.com/en-us/iaas/Content/Billing/Tasks/signingup_topic-Estimating_Costs.htm
    """

    OCI_API_BASE = "https://{region}.ociapis.oci.oraclecloud.com"
    COST_MANAGEMENT_API = "/20190111/usageCosts"
    PRICING_API = "/20181001/pricing"

    ORACLE_SERVICES = [
        "Compute",
        "Object Storage",
        "Autonomous Database",
        "Exadata",
        "Load Balancer",
        "WAF",
    ]

    ORACLE_REGIONS = [
        "us-ashburn-1",
        "us-phoenix-1",
        "eu-frankfurt-1",
        "uk-london-1",
        "ap-sydney-1",
        "ap-tokyo-1",
    ]

    def __init__(self):
        """Initialize Oracle Cloud cost collector."""
        super().__init__(provider="oracle", rate_limit=(50, 60))
        self.service_mapper = ServiceCategoryMapper()
        self.tenancy_ocid = settings.oracle_tenancy_ocid
        self.user_ocid = settings.oracle_user_ocid
        self.fingerprint = settings.oracle_fingerprint
        self.private_key_path = settings.oracle_private_key_path
        self.private_key_content = settings.oracle_private_key_content

    async def collect_pricing_data(
        self, region: str | None = None, service: str | None = None
    ) -> list[dict[str, Any]]:
        """Collect Oracle Cloud pricing data using OCI REST APIs.

        Args:
            region: Optional region filter
            service: Optional service filter

        Returns:
            List of raw pricing data dictionaries
        """
        if not self._has_credentials():
            logger.warning("Oracle Cloud credentials not configured. Skipping Oracle collection.")
            return []

        regions = [region] if region else self.ORACLE_REGIONS
        services = [service] if service else self.ORACLE_SERVICES

        all_data = []

        async with httpx.AsyncClient(timeout=60.0) as client:
            for oracle_region in regions:
                try:
                    usage_costs = await self._fetch_usage_costs(client, oracle_region)
                    all_data.extend(usage_costs)
                    
                    pricing_data = await self._fetch_pricing_data(client, oracle_region, services)
                    all_data.extend(pricing_data)
                except Exception as e:
                    logger.warning(
                        "Failed to fetch pricing for region %s: %s",
                        oracle_region,
                        e,
                    )
                    continue

        return all_data

    def _has_credentials(self) -> bool:
        """Check if OCI credentials are configured.

        Returns:
            True if credentials are available
        """
        return bool(
            self.tenancy_ocid
            and self.user_ocid
            and self.fingerprint
            and (self.private_key_content or self.private_key_path)
        )

    def _get_private_key(self) -> str:
        """Get private key content.

        Returns:
            Private key content as string
        """
        if self.private_key_content:
            return self.private_key_content
        if self.private_key_path:
            with open(self.private_key_path, "r") as f:
                return f.read()
        return ""

    def _sign_request(
        self, method: str, url: str, headers: dict[str, str], body: str = ""
    ) -> dict[str, str]:
        """Sign OCI API request using signature-based authentication.

        Args:
            method: HTTP method
            url: Request URL
            headers: Request headers
            body: Request body

        Returns:
            Updated headers with signature
        """
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.primitives import hashes
        except ImportError:
            logger.error("cryptography library required for OCI authentication")
            return headers

        private_key_pem = self._get_private_key()
        if not private_key_pem:
            return headers

        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(), password=None
            )

            key_id = f"{self.tenancy_ocid}/{self.user_ocid}/{self.fingerprint}"

            request_target = f"{method.lower()} {url.split('?')[0]}"

            signing_string_parts = [
                f"date: {headers.get('date', '')}",
                f"(request-target): {request_target}",
                f"host: {headers.get('host', '')}",
            ]

            signing_string = "\n".join(signing_string_parts)

            signature = private_key.sign(
                signing_string.encode(),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )

            signature_b64 = base64.b64encode(signature).decode()

            headers["Authorization"] = (
                f'Signature keyId="{key_id}",algorithm="rsa-sha256",'
                f'headers="date (request-target) host",signature="{signature_b64}"'
            )

        except Exception as e:
            logger.error("Failed to sign OCI request: %s", e)

        return headers

    async def _fetch_usage_costs(
        self, client: httpx.AsyncClient, region: str
    ) -> list[dict[str, Any]]:
        """Fetch usage costs from OCI Cost Management API.

        Args:
            client: HTTP client
            region: Oracle region

        Returns:
            List of usage cost data dictionaries
        """
        pricing_data = []

        try:
            api_base = self.OCI_API_BASE.format(region=region)
            url = f"{api_base}{self.COST_MANAGEMENT_API}"

            headers = {
                "date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "host": url.split("//")[1].split("/")[0],
                "content-type": "application/json",
            }

            params = {
                "compartmentId": self.tenancy_ocid,
                "timeUsageStarted": (datetime.utcnow().replace(day=1)).isoformat() + "Z",
                "timeUsageEnded": datetime.utcnow().isoformat() + "Z",
            }

            headers = self._sign_request("GET", url, headers)
            full_url = f"{url}?{urlencode(params)}"

            response = await client.get(full_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            items = data.get("items", [])
            for item in items:
                raw_data = {
                    "service": item.get("skuName", ""),
                    "region": region,
                    "sku": item.get("skuPartNumber", ""),
                    "description": item.get("skuName", ""),
                    "price": item.get("computedAmount", {}).get("value", 0),
                    "currency": item.get("currency", "USD"),
                    "unit": item.get("unit", "hour"),
                    "usage": item.get("quantity", 0),
                    "item": item,
                }
                pricing_data.append(raw_data)

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error fetching OCI usage costs: %s", e)
        except json.JSONDecodeError as e:
            logger.error("JSON decode error: %s", e)
        except Exception as e:
            logger.error("Unexpected error fetching OCI usage costs: %s", e)

        return pricing_data

    async def _fetch_pricing_data(
        self, client: httpx.AsyncClient, region: str, services: list[str]
    ) -> list[dict[str, Any]]:
        """Fetch pricing data from OCI Pricing API.

        Args:
            client: HTTP client
            region: Oracle region
            services: List of services to fetch

        Returns:
            List of pricing data dictionaries
        """
        pricing_data = []

        try:
            api_base = self.OCI_API_BASE.format(region=region)
            url = f"{api_base}{self.PRICING_API}"

            headers = {
                "date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "host": url.split("//")[1].split("/")[0],
                "content-type": "application/json",
            }

            headers = self._sign_request("GET", url, headers)

            for service in services:
                params = {
                    "compartmentId": self.tenancy_ocid,
                    "service": service,
                }

                full_url = f"{url}?{urlencode(params)}"
                response = await client.get(full_url, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    for item in items:
                        raw_data = {
                            "service": service,
                            "region": region,
                            "sku": item.get("partNumber", ""),
                            "description": item.get("displayName", ""),
                            "price": item.get("price", {}).get("value", 0),
                            "currency": item.get("currency", "USD"),
                            "unit": item.get("unit", "hour"),
                            "item": item,
                        }
                        pricing_data.append(raw_data)

        except httpx.HTTPStatusError as e:
            logger.debug("Pricing API endpoint returned: %s", e.response.status_code)
        except Exception as e:
            logger.debug("Error fetching pricing data: %s", e)

        return pricing_data

    def map_to_focus(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Map Oracle raw data to FOCUS format.

        Args:
            raw_data: Oracle raw pricing data

        Returns:
            FOCUS-compliant data dictionary
        """
        service = raw_data.get("service", "")
        region = raw_data.get("region", "")
        sku = raw_data.get("sku", "")
        description = raw_data.get("description", "")
        price = Decimal(str(raw_data.get("price", 0)))
        currency = raw_data.get("currency", "USD")
        unit = raw_data.get("unit", "hour")

        service_category = self.service_mapper.get_service_category("oracle", service, description)

        billing_period_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        billing_period_end = datetime.utcnow()

        focus_data = {
            "billing_account_id": "oracle-default",
            "billing_account_name": "Oracle Cloud Default Account",
            "billing_currency": currency,
            "billing_period_start": billing_period_start,
            "billing_period_end": billing_period_end,
            "provider": "oracle",
            "invoice_issuer": "Oracle Corporation",
            "publisher": None,
            "region_id": region,
            "region_name": self._get_region_name(region),
            "availability_zone": None,
            "resource_id": sku,
            "resource_name": description or f"{service} in {region}",
            "resource_type": service.lower().replace(" ", "-"),
            "service_category": service_category,
            "service_name": service,
            "service_subcategory": None,
            "sku_id": sku,
            "sku_description": description,
            "sku_price_id": sku,
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
            "charge_description": f"{service} {description} in {region}",
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
            region_id: Oracle region ID

        Returns:
            Region name
        """
        region_names = {
            "us-ashburn-1": "US East (Ashburn)",
            "us-phoenix-1": "US West (Phoenix)",
            "eu-frankfurt-1": "Europe (Frankfurt)",
            "uk-london-1": "UK (London)",
            "ap-sydney-1": "Asia Pacific (Sydney)",
            "ap-tokyo-1": "Asia Pacific (Tokyo)",
        }
        return region_names.get(region_id, region_id)

