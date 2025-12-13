"""Security data client for fetching security information."""

import logging
from datetime import datetime, timedelta
from typing import Any

import httpx

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from wistx_mcp.tools.lib.constants import (
    NVD_API_MAX_RESULTS_PER_PAGE,
    NVD_API_TIMEOUT_SECONDS,
    NVD_API_MAX_RETRIES,
    SECURITY_CACHE_TTL_HOURS,
    SECURITY_QUERY_MIN_WORD_LENGTH,
    SECURITY_QUERY_MAX_IMPORTANT_WORDS,
    SECURITY_QUERY_FALLBACK_LENGTH,
    CVSS_V2_CRITICAL_THRESHOLD,
    CVSS_V2_HIGH_THRESHOLD,
    CVSS_V2_MEDIUM_THRESHOLD,
)

logger = logging.getLogger(__name__)


class SecurityClient:
    """Client for fetching security data from various sources."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize security client.

        Args:
            mongodb_client: MongoDB client for caching
        """
        self.mongodb_client = mongodb_client
        self.cache_ttl_hours = SECURITY_CACHE_TTL_HOURS
        self.http_client = httpx.AsyncClient(timeout=NVD_API_TIMEOUT_SECONDS)

    async def close(self) -> None:
        """Close HTTP client connection."""
        await self.http_client.aclose()

    def _simplify_query(self, query: str, resource_type: str | None = None) -> list[str]:
        """Simplify query for NVD API by extracting key terms.
        
        NVD API works better with simple, focused queries rather than verbose descriptions.
        This function extracts key terms and generates multiple query variations.
        
        Args:
            query: Original query string
            resource_type: Optional resource type to prioritize
            
        Returns:
            List of simplified query strings to try
        """
        import re
        
        query_lower = query.lower()
        
        if resource_type:
            queries = [resource_type]
        else:
            queries = []
        
        common_terms_to_remove = [
            "security", "vulnerability", "vulnerabilities", "cve", "cves", "advisory", "advisories",
            "2024", "2025", "recent", "latest", "issues", "problems", "exploits", "related", "our"
        ]
        
        cloud_terms_to_remove = ["gcp", "aws", "azure", "google", "cloud", "platform", "amazon", "microsoft"]
        
        words = re.findall(r'\b\w+\b', query_lower)
        important_words = [
            w for w in words 
            if w not in common_terms_to_remove 
            and w not in cloud_terms_to_remove
            and len(w) > SECURITY_QUERY_MIN_WORD_LENGTH
        ]
        
        if important_words:
            if len(important_words) <= SECURITY_QUERY_MAX_IMPORTANT_WORDS:
                queries.append(" ".join(important_words))
            else:
                queries.append(" ".join(important_words[:SECURITY_QUERY_MAX_IMPORTANT_WORDS]))
                if len(important_words) > SECURITY_QUERY_MAX_IMPORTANT_WORDS:
                    queries.append(" ".join(important_words[1:SECURITY_QUERY_MAX_IMPORTANT_WORDS + 1]))
        
        if not queries:
            simplified = query[:SECURITY_QUERY_FALLBACK_LENGTH].strip()
            for term in common_terms_to_remove + cloud_terms_to_remove:
                simplified = re.sub(rf'\b{re.escape(term)}\b', '', simplified, flags=re.IGNORECASE)
            simplified = re.sub(r'\s+', ' ', simplified).strip()
            if simplified:
                queries.append(simplified[:SECURITY_QUERY_FALLBACK_LENGTH])
            else:
                queries.append(query[:SECURITY_QUERY_FALLBACK_LENGTH])
        
        return list(dict.fromkeys(queries))

    async def search_cves(
        self,
        query: str,
        resource_type: str | None = None,
        severity: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search CVE database.

        Args:
            query: Search query
            resource_type: Filter by resource type
            severity: Filter by severity (CRITICAL, HIGH, MEDIUM, LOW)
            limit: Maximum results

        Returns:
            List of CVE dictionaries
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            logger.warning("MongoDB not connected, returning empty CVE results")
            return []

        collection = self.mongodb_client.database.security_knowledge

        cache_key = f"cve:{query}:{resource_type}:{severity}"
        cached_result = await collection.find_one(
            {"cache_key": cache_key, "cache_expires_at": {"$gt": datetime.utcnow()}}
        )

        if cached_result:
            logger.debug("Using cached CVE results for query: %s", query[:50])
            return cached_result.get("data", [])

        simplified_queries = self._simplify_query(query, resource_type)
        all_cves = []
        seen_cve_ids = set()

        for simplified_query in simplified_queries:
            if len(all_cves) >= limit:
                break
            
            remaining_needed = limit - len(all_cves)
            query_limit = min(remaining_needed, NVD_API_MAX_RESULTS_PER_PAGE)
            if query_limit <= 0:
                break
                
            try:
                nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
                params: dict[str, Any] = {
                    "keywordSearch": simplified_query,
                    "resultsPerPage": query_limit,
                }

                response = await with_timeout_and_retry(
                    self.http_client.get,
                    timeout_seconds=NVD_API_TIMEOUT_SECONDS,
                    max_attempts=NVD_API_MAX_RETRIES,
                    retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                    url=nvd_url,
                    params=params,
                )
                response.raise_for_status()

                nvd_data = response.json()
                
                for vuln in nvd_data.get("vulnerabilities", []):
                    if len(all_cves) >= limit:
                        break
                        
                    cve_item = vuln.get("cve", {})
                    cve_id = cve_item.get("id", "")
                    
                    if cve_id in seen_cve_ids:
                        continue
                    seen_cve_ids.add(cve_id)
                    
                    descriptions = cve_item.get("descriptions", [])
                    description = descriptions[0].get("value", "") if descriptions else ""

                    metrics = cve_item.get("metrics", {})
                    
                    base_severity = "MEDIUM"
                    cvss_score = 0.0
                    
                    cvss_v31 = metrics.get("cvssMetricV31", [{}])[0] if metrics.get("cvssMetricV31") else {}
                    cvss_v30 = metrics.get("cvssMetricV30", [{}])[0] if metrics.get("cvssMetricV30") else {}
                    cvss_v2 = metrics.get("cvssMetricV2", [{}])[0] if metrics.get("cvssMetricV2") else {}
                    
                    if cvss_v31:
                        cvss_data = cvss_v31.get("cvssData", {})
                        base_severity = cvss_data.get("baseSeverity", "MEDIUM")
                        cvss_score = cvss_data.get("baseScore", 0.0)
                    elif cvss_v30:
                        cvss_data = cvss_v30.get("cvssData", {})
                        base_severity = cvss_data.get("baseSeverity", "MEDIUM")
                        cvss_score = cvss_data.get("baseScore", 0.0)
                    elif cvss_v2:
                        cvss_data = cvss_v2.get("cvssData", {})
                        cvss_score = cvss_data.get("baseScore", 0.0)
                        
                        if cvss_score >= CVSS_V2_CRITICAL_THRESHOLD:
                            base_severity = "CRITICAL"
                        elif cvss_score >= CVSS_V2_HIGH_THRESHOLD:
                            base_severity = "HIGH"
                        elif cvss_score >= CVSS_V2_MEDIUM_THRESHOLD:
                            base_severity = "MEDIUM"
                        else:
                            base_severity = "LOW"

                    if severity:
                        severity_upper = severity.upper()
                        base_severity_upper = base_severity.upper()
                        
                        severity_map = {
                            "CRITICAL": ["CRITICAL"],
                            "HIGH": ["CRITICAL", "HIGH"],
                            "MEDIUM": ["CRITICAL", "HIGH", "MEDIUM"],
                            "LOW": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                        }
                        
                        allowed_severities = severity_map.get(severity_upper, [])
                        if base_severity_upper not in allowed_severities:
                            continue

                    cve_dict = {
                        "cve_id": cve_id,
                        "title": f"{cve_id}: {description[:100]}",
                        "description": description,
                        "severity": base_severity.upper(),
                        "cvss_score": cvss_score,
                        "resource_type": resource_type,
                        "source": "nvd",
                        "published_date": cve_item.get("published", ""),
                        "updated_date": cve_item.get("lastModified", ""),
                        "references": [ref.get("url", "") for ref in cve_item.get("references", [])],
                    }

                    all_cves.append(cve_dict)

            except httpx.HTTPError as e:
                logger.debug("Failed to fetch CVEs for query '%s': %s", simplified_query, e)
                continue
            except Exception as e:
                logger.debug("Error searching CVEs for query '%s': %s", simplified_query, e)
                continue

        if all_cves:
            all_cves.sort(key=lambda x: x.get("cvss_score", 0.0), reverse=True)
            cache_expires = datetime.utcnow() + timedelta(hours=self.cache_ttl_hours)
            await collection.insert_one({
                "cache_key": cache_key,
                "data": all_cves[:limit],
                "cached_at": datetime.utcnow(),
                "cache_expires_at": cache_expires,
            })

        logger.info("Found %d CVEs for query: %s", len(all_cves), query[:50])
        return all_cves[:limit]

    async def search_advisories(
        self,
        query: str,
        cloud_provider: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search security advisories.

        Args:
            query: Search query
            cloud_provider: Filter by cloud provider
            limit: Maximum results

        Returns:
            List of advisory dictionaries
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            logger.warning("MongoDB not connected, returning empty advisory results")
            return []

        simplified_queries = self._simplify_query(query)
        all_advisories = []
        seen_advisory_ids = set()

        for simplified_query in simplified_queries:
            if len(all_advisories) >= limit:
                break

            if cloud_provider == "aws" or not cloud_provider:
                try:
                    aws_advisories = await self._search_aws_advisories(simplified_query, limit)
                    for adv in aws_advisories:
                        adv_id = adv.get("id") or adv.get("title", "")
                        if adv_id and adv_id not in seen_advisory_ids:
                            seen_advisory_ids.add(adv_id)
                            all_advisories.append(adv)
                except Exception as e:
                    logger.debug("Failed to search AWS advisories: %s", e)

            if cloud_provider == "gcp" or not cloud_provider:
                try:
                    gcp_advisories = await self._search_gcp_advisories(simplified_query, limit)
                    for adv in gcp_advisories:
                        adv_id = adv.get("id") or adv.get("title", "")
                        if adv_id and adv_id not in seen_advisory_ids:
                            seen_advisory_ids.add(adv_id)
                            all_advisories.append(adv)
                except Exception as e:
                    logger.debug("Failed to search GCP advisories: %s", e)

            if cloud_provider == "azure" or not cloud_provider:
                try:
                    azure_advisories = await self._search_azure_advisories(simplified_query, limit)
                    for adv in azure_advisories:
                        adv_id = adv.get("id") or adv.get("title", "")
                        if adv_id and adv_id not in seen_advisory_ids:
                            seen_advisory_ids.add(adv_id)
                            all_advisories.append(adv)
                except Exception as e:
                    logger.debug("Failed to search Azure advisories: %s", e)

        logger.info("Found %d advisories for query: %s", len(all_advisories), query[:50])
        return all_advisories[:limit]

    async def _search_aws_advisories(
        self,
        query: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Search AWS security advisories.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of AWS advisory dictionaries
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return []

        collection = self.mongodb_client.database.security_knowledge

        from wistx_mcp.tools.lib.mongodb_utils import build_safe_mongodb_regex_query

        mongo_query: dict[str, Any] = {
            "source": "aws",
            **build_safe_mongodb_regex_query(
                query=query,
                fields=["title", "description"],
                case_insensitive=True,
            ),
        }

        cursor = collection.find(mongo_query).sort("published_date", -1).limit(limit)
        results = await cursor.to_list(length=limit)

        if results:
            return results

        return []

    async def _search_gcp_advisories(
        self,
        query: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Search GCP security advisories.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of GCP advisory dictionaries
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return []

        collection = self.mongodb_client.database.security_knowledge

        from wistx_mcp.tools.lib.mongodb_utils import build_safe_mongodb_regex_query

        mongo_query: dict[str, Any] = {
            "source": "gcp",
            **build_safe_mongodb_regex_query(
                query=query,
                fields=["title", "description"],
                case_insensitive=True,
            ),
        }

        cursor = collection.find(mongo_query).sort("published_date", -1).limit(limit)
        results = await cursor.to_list(length=limit)

        if results:
            return results

        return []

    async def _search_azure_advisories(
        self,
        query: str,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Search Azure security advisories.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of Azure advisory dictionaries
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            return []

        collection = self.mongodb_client.database.security_knowledge

        from wistx_mcp.tools.lib.mongodb_utils import build_safe_mongodb_regex_query

        mongo_query: dict[str, Any] = {
            "source": "azure",
            **build_safe_mongodb_regex_query(
                query=query,
                fields=["title", "description"],
                case_insensitive=True,
            ),
        }

        cursor = collection.find(mongo_query).sort("published_date", -1).limit(limit)
        results = await cursor.to_list(length=limit)

        if results:
            return results

        return []

    async def search_kubernetes_security(
        self,
        query: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """Search Kubernetes security information.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of Kubernetes security items
        """
        await self.mongodb_client.connect()

        if self.mongodb_client.database is None:
            logger.warning("MongoDB not connected, returning empty K8s security results")
            return []

        collection = self.mongodb_client.database.security_knowledge

        from wistx_mcp.tools.lib.mongodb_utils import build_safe_mongodb_regex_query

        mongo_query: dict[str, Any] = {
            "$or": [
                {"source": "kubernetes"},
                {"source": "cncf"},
                {"resource_type": {"$regex": "kubernetes|k8s|eks|gke|aks", "$options": "i"}},
            ],
            **build_safe_mongodb_regex_query(
                query=query,
                fields=["title", "description"],
                case_insensitive=True,
            ),
        }

        cursor = collection.find(mongo_query).sort("published_date", -1).limit(limit)
        results = await cursor.to_list(length=limit)

        logger.info("Found %d Kubernetes security items for query: %s", len(results), query[:50])
        return results

