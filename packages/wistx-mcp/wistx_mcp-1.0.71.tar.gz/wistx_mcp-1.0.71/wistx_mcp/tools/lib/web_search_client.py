"""Web search client using Tavily API."""

import logging
from datetime import datetime, timedelta
from typing import Any

import httpx

from wistx_mcp.config import settings
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry

logger = logging.getLogger(__name__)


class WebSearchClient:
    """Client for web search using Tavily API."""

    def __init__(self, api_key: str | None = None):
        """Initialize web search client.

        Args:
            api_key: Tavily API key (defaults to TAVILY_API_KEY env var)
        """
        self.api_key = api_key or settings.tavily_api_key
        self.base_url = "https://api.tavily.com"
        self.http_client = httpx.AsyncClient(timeout=30.0)

        if not self.api_key:
            logger.warning("Tavily API key not provided - web search will be disabled")

    async def close(self) -> None:
        """Close HTTP client connection."""
        await self.http_client.aclose()

    async def search(
        self,
        query: str,
        search_depth: str = "basic",
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_answer: bool = True,
        include_raw_content: bool = False,
        max_results: int = 5,
        max_age_days: int | None = None,
        time_range: str | None = None,
    ) -> dict[str, Any]:
        """Search the web using Tavily API with freshness controls.

        Args:
            query: Search query
            search_depth: Search depth (basic, advanced)
            include_domains: Domains to include in search
            exclude_domains: Domains to exclude from search
            include_answer: Include AI-generated answer
            include_raw_content: Include raw HTML content
            max_results: Maximum number of results
            max_age_days: Maximum age of results in days (overrides time_range)
            time_range: Predefined time range (day, week, month, year)

        Returns:
            Dictionary with search results:
            - query: Original query
            - answer: AI-generated answer (if include_answer=True)
            - results: List of search results (filtered by freshness)
            - response_time: API response time
            - freshness_info: Information about result freshness

        Raises:
            ValueError: If API key is not provided
            httpx.HTTPError: If API request fails
        """
        if not self.api_key:
            raise ValueError("Tavily API key is required for web search")

        url = f"{self.base_url}/search"
        headers = {
            "Content-Type": "application/json",
        }

        if max_age_days is None:
            max_age_days = settings.tavily_max_age_days

        if time_range is None and max_age_days:
            if max_age_days <= 1:
                time_range = "day"
            elif max_age_days <= 7:
                time_range = "week"
            elif max_age_days <= 30:
                time_range = "month"
            elif max_age_days <= 365:
                time_range = "year"
            else:
                time_range = None

        payload: dict[str, Any] = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": search_depth,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "max_results": max_results * 2,
        }

        if time_range:
            payload["time_range"] = time_range
        elif max_age_days:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=max_age_days)
            payload["start_date"] = start_date.strftime("%Y-%m-%d")
            payload["end_date"] = end_date.strftime("%Y-%m-%d")

        if include_domains:
            payload["include_domains"] = include_domains

        if exclude_domains:
            payload["exclude_domains"] = exclude_domains

        try:
            from wistx_mcp.tools.lib.constants import WEB_SEARCH_TIMEOUT_SECONDS

            response = await with_timeout_and_retry(
                self.http_client.post,
                timeout_seconds=WEB_SEARCH_TIMEOUT_SECONDS,
                max_attempts=3,
                retryable_exceptions=(httpx.HTTPError, httpx.TimeoutException, httpx.NetworkError),
                url=url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            result = response.json()

            all_results = result.get("results", [])
            original_count = len(all_results)
            
            if max_age_days:
                filtered_results = []
                cutoff_date = datetime.now() - timedelta(days=max_age_days)
                
                for item in all_results:
                    published_date_str = item.get("published_date")
                    if published_date_str:
                        try:
                            published_date = datetime.fromisoformat(published_date_str.replace("Z", "+00:00"))
                            if published_date.replace(tzinfo=None) >= cutoff_date:
                                filtered_results.append(item)
                        except (ValueError, AttributeError):
                            filtered_results.append(item)
                    else:
                        filtered_results.append(item)
                
                results = filtered_results[:max_results]
            else:
                results = all_results[:max_results]

            result["results"] = results
            result["freshness_info"] = {
                "max_age_days": max_age_days,
                "time_range": time_range,
                "results_count": len(results),
                "original_count": original_count,
                "filtered_out": original_count - len(results),
            }

            logger.info(
                "Tavily search completed: query='%s', results=%d, max_age=%d days",
                query[:100],
                len(results),
                max_age_days or 0,
            )

            return result

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("Tavily API authentication failed - check API key")
                raise ValueError("Invalid Tavily API key") from e
            elif e.response.status_code == 429:
                logger.warning("Tavily API rate limit exceeded")
                raise ValueError("Tavily API rate limit exceeded") from e
            else:
                logger.error("Tavily API error: %s", e.response.text)
                raise
        except httpx.HTTPError as e:
            logger.error("Tavily API request failed: %s", e)
            raise

    async def search_devops(
        self,
        query: str,
        max_results: int = 10,
        max_age_days: int = 90,
    ) -> dict[str, Any]:
        """Search for DevOps/infrastructure/compliance content with freshness control.

        Args:
            query: Search query
            max_results: Maximum number of results
            max_age_days: Maximum age of results in days (default: 90 days)

        Returns:
            Dictionary with search results
        """
        devops_domains = [
            "github.com",
            "docs.aws.amazon.com",
            "cloud.google.com",
            "learn.microsoft.com",
            "kubernetes.io",
            "terraform.io",
            "ansible.com",
            "pulumi.com",
            "hashicorp.com",
            "cncf.io",
        ]

        return await self.search(
            query=query,
            search_depth="advanced",
            include_domains=devops_domains,
            include_answer=True,
            max_results=max_results,
            max_age_days=max_age_days,
        )

    async def search_by_domain(
        self,
        query: str,
        domains: list[str] | None = None,
        max_results: int = 10,
        max_age_days: int | None = None,
    ) -> dict[str, Any]:
        """Search web content filtered by domain types with freshness control.

        Args:
            query: Search query
            domains: Domain types (compliance, finops, devops, infrastructure, security, sre, platform)
            max_results: Maximum number of results
            max_age_days: Maximum age of results in days (domain-specific defaults if None)

        Returns:
            Dictionary with search results
        """
        include_domains = []

        if not domains:
            domains = ["devops", "infrastructure"]

        domain_freshness = {
            "compliance": 365,
            "finops": 90,
            "devops": 90,
            "infrastructure": 90,
            "security": 30,
            "sre": 90,
            "platform": 90,
        }

        if max_age_days is None:
            max_age_days = min(
                domain_freshness.get(domain.lower(), 90) for domain in domains
            )

        domain_mapping = {
            "compliance": [
                "pci.com",
                "hipaaguide.net",
                "nist.gov",
                "iso.org",
                "soc2.org",
                "gdpr.eu",
            ],
            "finops": [
                "finops.org",
                "cloudability.com",
                "cloudhealthtech.com",
                "apptio.com",
                "docs.aws.amazon.com/cost-management",
                "cloud.google.com/billing",
            ],
            "devops": [
                "github.com",
                "gitlab.com",
                "jenkins.io",
                "circleci.com",
                "gitlab.com",
                "atlassian.com",
            ],
            "infrastructure": [
                "docs.aws.amazon.com",
                "cloud.google.com",
                "learn.microsoft.com",
                "terraform.io",
                "pulumi.com",
                "ansible.com",
            ],
            "security": [
                "owasp.org",
                "cve.mitre.org",
                "nvd.nist.gov",
                "security.aws.amazon.com",
                "cloud.google.com/security",
            ],
            "sre": [
                "sre.google",
                "sre.work",
                "prometheus.io",
                "grafana.com",
                "datadoghq.com",
            ],
            "platform": [
                "kubernetes.io",
                "cncf.io",
                "istio.io",
                "linkerd.io",
                "helm.sh",
            ],
        }

        for domain in domains:
            if domain.lower() in domain_mapping:
                include_domains.extend(domain_mapping[domain.lower()])

        if not include_domains:
            include_domains = domain_mapping["devops"]

        return await self.search(
            query=query,
            search_depth="advanced",
            include_domains=list(set(include_domains)),
            include_answer=True,
            max_results=max_results,
            max_age_days=max_age_days,
        )

