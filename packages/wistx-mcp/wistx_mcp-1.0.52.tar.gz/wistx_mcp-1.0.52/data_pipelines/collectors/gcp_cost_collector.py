"""GCP cost data collector with FOCUS mapping.

Follows the pattern from GCP_API_IMPLEMENTATION.md:
- Service Account Authentication (JWT-based OAuth2) or API Key fallback
- Service Discovery & Intelligent Filtering (80+ Google Cloud patterns, 50+ marketplace exclusions)
- SKU Fetching & Pricing Extraction
- FOCUS Data Structure mapping
- MongoDB/Pinecone integration handled by pipeline orchestrator
"""

import json
import os
import re
import time
from datetime import datetime
from decimal import Decimal
from typing import Any

import httpx
import jwt

from .base_cost_collector import BaseCostCollector
from ..models.provider_mappings import ServiceCategoryMapper
from ..utils.config import PipelineSettings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
settings = PipelineSettings()


class GCPCostCollector(BaseCostCollector):
    """Collect GCP pricing data and map to FOCUS format.

    Uses GCP Cloud Billing Catalog API v1:
    - Endpoint: cloudbilling.googleapis.com/v1/services
    - Authentication: Service Account (JWT OAuth2) or API Key
    - Service Discovery: Lists all services, filters Google Cloud services
    - SKU Fetching: Fetches pricing SKUs for each service
    """

    BILLING_API_BASE = "https://cloudbilling.googleapis.com/v1"
    OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"

    GOOGLE_CLOUD_PATTERNS = [
        r"^Cloud\s+",
        r"^Compute Engine",
        r"^App Engine",
        r"^BigQuery",
        r"^Cloud Bigtable",
        r"^Cloud Datastore",
        r"^Cloud Firestore",
        r"^Dataflow",
        r"^Dataproc",
        r"^Pub/Sub",
        r"^Vertex",
        r"^AI Platform",
        r"^AutoML",
        r"^Vision API",
        r"^Speech",
        r"^Translation",
        r"^Natural Language",
        r"^Dialogflow",
        r"^Document AI",
        r"Kubernetes Engine",
        r"^GKE",
        r"^Anthos",
        r"^Container",
        r"^Cloud CDN",
        r"^Cloud DNS",
        r"^Cloud VPN",
        r"^Cloud NAT",
        r"^Cloud Load Balancing",
        r"^Cloud Armor",
        r"^Cloud KMS",
        r"^Cloud IAM",
        r"^Binary Authorization",
        r"^Certificate Manager",
        r"^Security Command",
        r"^Cloud Logging",
        r"^Cloud Monitoring",
        r"^Cloud Trace",
        r"^Cloud Debugger",
        r"^Cloud Profiler",
        r"^Error Reporting",
        r"^Cloud Build",
        r"^Cloud Deploy",
        r"^Cloud Source",
        r"^Persistent Disk",
        r"^Local SSD",
        r"^Cloud Filestore",
        r"^Cloud Memorystore",
        r"^Cloud Functions",
        r"^Cloud Tasks",
        r"^Cloud Workflows",
        r"^Eventarc",
        r"^Cloud Endpoints",
        r"^Cloud API Gateway",
        r"^Service Directory",
        r"^Firebase",
        r"^Google\s+",
        r"\bAPI$",
    ]

    MARKETPLACE_KEYWORDS = [
        "centos",
        "ubuntu",
        "windows",
        "linux",
        "redhat",
        "suse",
        "debian",
        "rhel",
        "bitnami",
        "cognosys",
        "f5",
        "fortinet",
        "cisco",
        "netapp",
        "vmware",
        "citrix",
        "oracle",
        "sap",
        "microsoft",
        "nvidia",
        "apache",
        "nginx",
        "elastic",
        "docker",
        "jenkins",
        "gitlab",
        "atlassian",
        "jfrog",
        "wordpress",
        "drupal",
        "joomla",
        "moodle",
        "magento",
        "prestashop",
        "mysql",
        "postgresql",
        "mongodb",
        "redis",
        "cassandra",
        "elasticsearch",
        "mariadb",
        "percona",
        "influxdb",
        "neo4j",
        "couchbase",
        "memcached",
        "lamp",
        "lemp",
        "wamp",
        "xampp",
        "mean",
        "mern",
        "phpmyadmin",
        "webmin",
        "cpanel",
        "plesk",
        "ispconfig",
        "zabbix",
        "nagios",
        "splunk",
        "suricata",
        "ossec",
        "wazuh",
        "inc.",
        "ltd.",
        "corp.",
        "llc.",
        "gmbh",
        "certified by",
        "powered by",
        "edition",
        "community",
        "enterprise",
    ]

    GCP_REGIONS = [
        "us-central1",
        "us-east1",
        "us-west1",
        "europe-west1",
        "asia-east1",
        "asia-southeast1",
    ]

    def __init__(self):
        """Initialize GCP cost collector."""
        super().__init__(provider="gcp", rate_limit=(100, 60))
        self.service_mapper = ServiceCategoryMapper()
        self.access_token: str | None = None
        self.token_expires_at: float = 0.0

        self.service_account_key_path = settings.gcp_service_account_key_path
        self.service_account_key_json = settings.gcp_service_account_key_json
        api_key_value = settings.gcp_api_key
        self.api_key = api_key_value.strip() if api_key_value and isinstance(api_key_value, str) else None

        if self.service_account_key_path or self.service_account_key_json:
            logger.info("GCP service account credentials configured")
        elif self.api_key:
            logger.info("GCP API key configured (fallback mode)")
        else:
            logger.warning(
                "GCP credentials not found. Set GCP_SERVICE_ACCOUNT_KEY_PATH, "
                "GCP_SERVICE_ACCOUNT_KEY_JSON, or GCP_API_KEY environment variable."
            )

    async def _get_access_token(self) -> str | None:
        """Get GCP access token using service account credentials.

        Returns:
            Access token string or None if authentication fails
        """
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token

        if not (self.service_account_key_path or self.service_account_key_json):
            return None

        try:
            if self.service_account_key_path and os.path.exists(self.service_account_key_path):
                with open(self.service_account_key_path, "r") as f:
                    service_account_info = json.load(f)
            elif self.service_account_key_json:
                service_account_info = json.loads(self.service_account_key_json)
            else:
                logger.error("GCP service account key not found")
                return None

            now = int(time.time())
            payload = {
                "iss": service_account_info["client_email"],
                "scope": "https://www.googleapis.com/auth/cloud-billing.readonly https://www.googleapis.com/auth/cloud-platform.read-only",
                "aud": self.OAUTH_TOKEN_URL,
                "iat": now,
                "exp": now + 3600,
            }

            token = jwt.encode(payload, service_account_info["private_key"], algorithm="RS256")

            async with httpx.AsyncClient(timeout=30.0) as client:
                data = {
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                    "assertion": token,
                }
                response = await client.post(self.OAUTH_TOKEN_URL, data=data)
                response.raise_for_status()
                result = response.json()
                access_token = result.get("access_token")
                expires_in = result.get("expires_in", 3600)

                self.access_token = access_token
                self.token_expires_at = time.time() + expires_in - 60

                logger.debug("GCP access token obtained successfully")
                return access_token

        except Exception as e:
            logger.error("Failed to obtain GCP access token: %s", e, exc_info=True)
            return None

    def _get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers for API requests.

        Returns:
            Dictionary with Authorization header or empty dict for API key
        """
        if self.access_token:
            return {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        return {}

    def _is_google_cloud_service(self, display_name: str) -> bool:
        """Check if service is a legitimate Google Cloud service.

        Args:
            display_name: Service display name

        Returns:
            True if service matches Google Cloud patterns
        """
        return any(re.search(pattern, display_name, re.IGNORECASE) for pattern in self.GOOGLE_CLOUD_PATTERNS)

    def _is_marketplace_service(self, display_name: str) -> bool:
        """Check if service is a marketplace/third-party offering.

        Args:
            display_name: Service display name

        Returns:
            True if service matches marketplace keywords
        """
        display_lower = display_name.lower()
        return any(keyword in display_lower for keyword in self.MARKETPLACE_KEYWORDS)

    def _filter_services(self, all_services: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Filter services to include only legitimate Google Cloud services.

        Args:
            all_services: List of all service dictionaries

        Returns:
            Filtered list of Google Cloud services
        """
        google_cloud_services = []
        marketplace_count = 0

        for service in all_services:
            display_name = service.get("displayName", "")

            if self._is_marketplace_service(display_name):
                marketplace_count += 1
                continue

            if self._is_google_cloud_service(display_name):
                google_cloud_services.append(service)

        logger.info(
            "Filtered GCP services: %d Google Cloud services, %d marketplace services excluded",
            len(google_cloud_services),
            marketplace_count,
        )

        return google_cloud_services

    async def _list_services(self, client: httpx.AsyncClient) -> list[dict[str, Any]]:
        """List all available GCP services.

        Handles pagination if the API returns nextPageToken.

        Args:
            client: HTTP client

        Returns:
            List of service dictionaries
        """
        url = f"{self.BILLING_API_BASE}/services"
        headers = self._get_auth_headers()
        params = {"key": self.api_key} if self.api_key and not headers else {}

        all_services = []
        page_token = None

        try:
            while True:
                if page_token:
                    params["pageToken"] = page_token

                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                services = data.get("services", [])
                all_services.extend(services)

                page_token = data.get("nextPageToken")
                if not page_token:
                    break

                params.pop("pageToken", None)

            logger.info("Discovered %d GCP services", len(all_services))
            return all_services
        except httpx.HTTPStatusError as e:
            logger.error("HTTP error listing GCP services: %s", e)
            if e.response.status_code == 401:
                logger.error("GCP authentication failed. Check service account credentials or API key.")
            elif e.response.status_code == 403:
                logger.error("GCP API access forbidden. Check API permissions and enablement.")
            elif e.response.status_code == 404:
                logger.error("GCP Cloud Billing API endpoint not found. Check API enablement.")
            return []
        except Exception as e:
            logger.error("Error listing GCP services: %s", e, exc_info=True)
            return []

    async def _get_service_skus(
        self, client: httpx.AsyncClient, service_id: str, region: str | None = None
    ) -> list[dict[str, Any]]:
        """Get SKUs for a service and optionally filter by region.

        Handles pagination if the API returns nextPageToken.

        Args:
            client: HTTP client
            service_id: GCP service ID
            region: Optional region filter

        Returns:
            List of SKU dictionaries
        """
        url = f"{self.BILLING_API_BASE}/services/{service_id}/skus"
        headers = self._get_auth_headers()
        params = {"key": self.api_key} if self.api_key and not headers else {}

        all_skus = []
        page_token = None

        try:
            while True:
                if page_token:
                    params["pageToken"] = page_token

                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                skus = data.get("skus", [])
                for sku in skus:
                    service_regions = sku.get("serviceRegions", [])
                    if region is None or region in service_regions or not service_regions:
                        all_skus.append(sku)

                page_token = data.get("nextPageToken")
                if not page_token:
                    break

                params.pop("pageToken", None)

            return all_skus

        except httpx.HTTPStatusError as e:
            logger.error("HTTP error fetching GCP SKUs for service %s: %s", service_id, e)
            return []
        except json.JSONDecodeError as e:
            logger.error("JSON decode error fetching GCP SKUs: %s", e)
            return []

    async def collect_pricing_data(
        self, region: str | None = None, service: str | None = None
    ) -> list[dict[str, Any]]:
        """Collect GCP pricing data following GCP_API_IMPLEMENTATION.md pattern.

        Flow:
        1. Authenticate (Service Account or API Key)
        2. List all services
        3. Filter Google Cloud services (exclude marketplace)
        4. Fetch SKUs for each filtered service
        5. Return raw pricing data

        Args:
            region: Optional region filter
            service: Optional service ID filter

        Returns:
            List of raw pricing data dictionaries
        """
        if not (self.service_account_key_path or self.service_account_key_json) and not self.api_key:
            logger.warning("GCP credentials not configured. Skipping GCP collection.")
            return []

        regions = [region] if region else self.GCP_REGIONS
        all_data = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            if self.service_account_key_path or self.service_account_key_json:
                access_token = await self._get_access_token()
                if not access_token:
                    logger.error("Failed to authenticate with GCP service account")
                    return []

            available_services = await self._list_services(client)

            if not available_services:
                logger.warning("No GCP services available. Check API key permissions and Cloud Billing API enablement.")
                return []

            google_cloud_services = self._filter_services(available_services)

            if not google_cloud_services:
                logger.warning("No legitimate Google Cloud services found after filtering")
                return []

            logger.info("Processing %d Google Cloud services", len(google_cloud_services))

            for service_info in google_cloud_services:
                service_id = service_info.get("serviceId", "")
                display_name = service_info.get("displayName", "")

                if service and service_id != service:
                    continue

                try:
                    await self.rate_limiter.acquire()
                    logger.debug("Fetching SKUs for: %s (%s)", display_name, service_id)

                    for gcp_region in regions:
                        skus = await self._get_service_skus(client, service_id, gcp_region)
                        logger.debug("Found %d SKUs for %s in region %s", len(skus), display_name, gcp_region)

                        for sku in skus:
                            raw_data = {
                                "service_id": service_id,
                                "service_name": display_name,
                                "region": gcp_region,
                                "sku": sku,
                            }
                            all_data.append(raw_data)

                except Exception as e:
                    logger.warning("Failed to fetch pricing for service %s: %s", display_name, e, exc_info=True)
                    continue

        logger.info("Collected %d GCP pricing records", len(all_data))
        return all_data

    async def collect_with_limits(
        self,
        regions: list[str] | None = None,
        services: list[str] | None = None,
        max_services: int | None = None,
        max_regions: int | None = None,
        max_records: int | None = None,
    ) -> "CollectionResult":
        """Collect GCP pricing data with limits enforced during collection.

        This method applies limits DURING collection to avoid unnecessary API calls:
        - max_services: Limits number of services processed
        - max_regions: Limits number of regions processed per service
        - max_records: Stops collection once limit is reached

        Args:
            regions: Optional list of regions to collect
            services: Optional list of service IDs to collect
            max_services: Maximum number of services to process
            max_regions: Maximum number of regions per service
            max_records: Maximum number of records to collect

        Returns:
            CollectionResult with collected data
        """
        from ..collectors.collection_result import CollectionResult

        result = CollectionResult(
            collector_name="gcp-cost",
            version="1.0",
            success=False,
        )
        result.metrics.start_time = datetime.utcnow()

        if not (self.service_account_key_path or self.service_account_key_json) and not self.api_key:
            logger.warning("GCP credentials not configured. Skipping GCP collection.")
            result.add_error("config", "MissingCredentials", "GCP credentials not configured")
            result.finalize()
            return result

        provider_regions = regions if regions else self.GCP_REGIONS
        if max_regions and len(provider_regions) > max_regions:
            provider_regions = provider_regions[:max_regions]
            logger.info("Limited to %d regions: %s", max_regions, provider_regions)

        all_data = []

        async with httpx.AsyncClient(timeout=30.0) as client:
            if self.service_account_key_path or self.service_account_key_json:
                access_token = await self._get_access_token()
                if not access_token:
                    logger.error("Failed to authenticate with GCP service account")
                    result.add_error("auth", "AuthenticationFailed", "Failed to obtain access token")
                    result.finalize()
                    return result

            available_services = await self._list_services(client)

            if not available_services:
                logger.warning("No GCP services available. Check API key permissions and Cloud Billing API enablement.")
                result.add_error("api", "NoServices", "No services available")
                result.finalize()
                return result

            google_cloud_services = self._filter_services(available_services)

            if not google_cloud_services:
                logger.warning("No legitimate Google Cloud services found after filtering")
                result.add_error("filter", "NoServices", "No Google Cloud services found after filtering")
                result.finalize()
                return result

            services_to_process = google_cloud_services
            if services:
                service_ids_set = set(services)
                services_to_process = [s for s in google_cloud_services if s.get("serviceId", "") in service_ids_set]
            elif max_services:
                services_to_process = google_cloud_services[:max_services]
                logger.info("Limited to %d services: %s", max_services, [s.get("displayName", "") for s in services_to_process])

            logger.info("Processing %d Google Cloud services", len(services_to_process))

            for service_info in services_to_process:
                if max_records and len(all_data) >= max_records:
                    logger.info("Reached max_records limit (%d), stopping collection", max_records)
                    break

                service_id = service_info.get("serviceId", "")
                display_name = service_info.get("displayName", "")

                try:
                    await self.rate_limiter.acquire()
                    logger.debug("Fetching SKUs for: %s (%s)", display_name, service_id)

                    for gcp_region in provider_regions:
                        if max_records and len(all_data) >= max_records:
                            break

                        skus = await self._get_service_skus(client, service_id, gcp_region)
                        logger.debug("Found %d SKUs for %s in region %s", len(skus), display_name, gcp_region)

                        for sku in skus:
                            if max_records and len(all_data) >= max_records:
                                break

                            raw_data = {
                                "service_id": service_id,
                                "service_name": display_name,
                                "region": gcp_region,
                                "sku": sku,
                            }
                            all_data.append(raw_data)

                except Exception as e:
                    logger.warning("Failed to fetch pricing for service %s: %s", display_name, e, exc_info=True)
                    continue

        result.items = all_data
        result.metrics.items_collected = len(all_data)
        result.metrics.successful_urls = 1
        result.success = True
        result.finalize()

        logger.info("Collected %d GCP pricing records (limit: %s)", len(all_data), max_records or "none")
        return result

    def map_to_focus(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Map GCP raw data to FOCUS format.

        Args:
            raw_data: GCP raw pricing data

        Returns:
            FOCUS-compliant data dictionary
        """
        service_id = raw_data.get("service_id", "")
        service_name = raw_data.get("service_name", "")
        region = raw_data.get("region", "")
        sku = raw_data.get("sku", {})

        sku_id = sku.get("skuId", "")
        description = sku.get("description", "")
        category = sku.get("category", {})
        pricing_info = sku.get("pricingInfo", [{}])[0] if sku.get("pricingInfo") else {}

        service_display_name = category.get("serviceDisplayName", service_name)
        resource_family = category.get("resourceFamily", "")
        resource_group = category.get("resourceGroup", "")
        usage_type = category.get("usageType", "OnDemand")

        pricing_expr = pricing_info.get("pricingExpression", {})
        tiered_rates = pricing_expr.get("tieredRates", [{}])
        unit_price = tiered_rates[0].get("unitPrice", {}) if tiered_rates else {}
        nanos = unit_price.get("nanos", 0)
        units = unit_price.get("units", "0")
        currency_code = unit_price.get("currencyCode", "USD")

        units_decimal = Decimal(units) if units else Decimal("0")
        nanos_decimal = Decimal(nanos) / Decimal("1000000000")
        price_decimal = units_decimal + nanos_decimal
        unit = pricing_expr.get("usageUnit", "hour")
        unit_description = pricing_expr.get("usageUnitDescription", unit)

        service_description = description or service_display_name or ""
        service_category = self.service_mapper.get_service_category("gcp", service_name, service_description)

        billing_period_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        billing_period_end = datetime.utcnow()

        focus_data = {
            "billing_account_id": "gcp-default",
            "billing_account_name": "GCP Default Billing Account",
            "billing_currency": currency_code,
            "billing_period_start": billing_period_start,
            "billing_period_end": billing_period_end,
            "provider": "gcp",
            "invoice_issuer": "Google Cloud Platform",
            "publisher": None,
            "region_id": region,
            "region_name": self._get_region_name(region),
            "availability_zone": None,
            "resource_id": sku_id,
            "resource_name": description,
            "resource_type": resource_group or resource_family or "default",
            "service_category": service_category,
            "service_name": service_name,
            "service_subcategory": service_display_name,
            "sku_id": sku_id,
            "sku_description": description,
            "sku_price_id": sku_id,
            "pricing_category": usage_type or "OnDemand",
            "pricing_quantity": 1.0,
            "pricing_unit": unit,
            "list_cost": price_decimal,
            "list_unit_price": price_decimal,
            "effective_cost": price_decimal,
            "billed_cost": price_decimal,
            "contracted_cost": None,
            "consumed_quantity": 1.0,
            "consumed_unit": unit,
            "charge_category": "Usage",
            "charge_description": f"{service_name} {description} in {region}",
            "charge_frequency": "Hourly" if "hour" in unit.lower() or "hour" in unit_description.lower() else "Monthly",
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
            region_id: GCP region ID

        Returns:
            Region name
        """
        region_names = {
            "us-central1": "Iowa",
            "us-east1": "South Carolina",
            "us-west1": "Oregon",
            "europe-west1": "Belgium",
            "asia-east1": "Taiwan",
            "asia-southeast1": "Singapore",
        }
        return region_names.get(region_id, region_id)
