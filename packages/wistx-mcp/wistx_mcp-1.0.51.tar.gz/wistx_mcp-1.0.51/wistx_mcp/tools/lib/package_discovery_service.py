"""Package discovery service - discover and filter DevOps/infrastructure packages."""

import asyncio
import logging
from typing import Any

from wistx_mcp.tools.lib.package_domain_filter import PackageDomainFilter
from wistx_mcp.tools.lib.package_registry_integrator import (
    NPMIntegrator,
    PackageRegistryIntegrator,
    PyPIIntegrator,
    RegistryIntegratorFactory,
    TerraformRegistryIntegrator,
)

logger = logging.getLogger(__name__)


class PackageDiscoveryService:
    """Service for discovering DevOps/infrastructure packages."""

    def __init__(self):
        """Initialize package discovery service."""
        self.domain_filter = PackageDomainFilter()

    async def discover_packages(
        self,
        registry: str,
        query: str | None = None,
        domain: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Discover packages in registry.

        Args:
            registry: Registry name (pypi, npm, terraform)
            query: Optional search query
            domain: Optional domain filter (devops, infrastructure, compliance, finops, platform, sre)
            limit: Maximum results

        Returns:
            List of package metadata dictionaries
        """
        integrator = RegistryIntegratorFactory.create(registry)

        try:
            if query:
                packages = await integrator.search_packages(query, limit=limit * 2)
            else:
                packages = await self._discover_popular_packages(integrator, limit * 2)

            filtered_packages = []
            for package in packages:
                if self.domain_filter.is_devops_infrastructure_package(package):
                    domain_tags = self.domain_filter.get_domain_tags(package)
                    category = self.domain_filter.get_category(package)
                    relevance_score = self.domain_filter.calculate_relevance_score(package, domain)

                    package["domain_tags"] = domain_tags
                    package["category"] = category
                    package["relevance_score"] = relevance_score

                    if not domain or domain in domain_tags or domain == "all":
                        filtered_packages.append(package)

            filtered_packages.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            return filtered_packages[:limit]
        finally:
            await integrator.close()

    async def _discover_popular_packages(
        self,
        integrator: PackageRegistryIntegrator,
        limit: int,
    ) -> list[dict[str, Any]]:
        """Discover popular packages in registry."""
        if isinstance(integrator, PyPIIntegrator):
            queries = ["terraform", "kubernetes", "aws", "docker", "ansible"]
        elif isinstance(integrator, NPMIntegrator):
            queries = ["aws-sdk", "terraform", "kubernetes", "pulumi", "cdktf"]
        elif isinstance(integrator, TerraformRegistryIntegrator):
            queries = ["aws", "gcp", "azure", "kubernetes", "vpc"]
        else:
            queries = ["devops", "infrastructure", "cloud"]

        all_packages = []
        for query in queries:
            try:
                packages = await integrator.search_packages(query, limit=limit // len(queries))
                all_packages.extend(packages)
            except Exception as e:
                logger.warning("Failed to discover packages for query %s: %s", query, e)
                continue

        seen = set()
        unique_packages = []
        for package in all_packages:
            package_id = package.get("package_id") or package.get("name")
            if package_id and package_id not in seen:
                seen.add(package_id)
                unique_packages.append(package)

        return unique_packages[:limit]

    async def get_package(self, registry: str, package_name: str, version: str | None = None) -> dict[str, Any] | None:
        """Get specific package metadata.

        Args:
            registry: Registry name
            package_name: Package name
            version: Optional version

        Returns:
            Package metadata dictionary or None if not found
        """
        integrator = RegistryIntegratorFactory.create(registry)

        try:
            metadata = await integrator.get_package_metadata(package_name, version)

            if self.domain_filter.is_devops_infrastructure_package(metadata):
                domain_tags = self.domain_filter.get_domain_tags(metadata)
                category = self.domain_filter.get_category(metadata)
                relevance_score = self.domain_filter.calculate_relevance_score(metadata)

                metadata["domain_tags"] = domain_tags
                metadata["category"] = category
                metadata["relevance_score"] = relevance_score

                return metadata

            return None
        except Exception as e:
            logger.warning("Failed to get package %s from %s: %s", package_name, registry, e)
            return None
        finally:
            await integrator.close()

