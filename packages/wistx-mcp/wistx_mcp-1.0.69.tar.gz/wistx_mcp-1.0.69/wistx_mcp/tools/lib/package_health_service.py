"""Package health metrics service - calculate and track package health."""

import logging
from datetime import datetime, timedelta
from typing import Any

try:
    from data_pipelines.models.package_health import (
        MaintenanceStatus,
        PackageHealthMetrics,
        SecurityStatus,
    )
except ImportError:
    from wistx_mcp.models.package_health import (
        MaintenanceStatus,
        PackageHealthMetrics,
        SecurityStatus,
    )

logger = logging.getLogger(__name__)


class PackageHealthService:
    """Service for calculating and tracking package health metrics."""

    def __init__(self):
        """Initialize package health service."""
        pass

    async def calculate_health_metrics(
        self,
        package_metadata: dict[str, Any],
        registry: str,
        package_name: str,
    ) -> PackageHealthMetrics:
        """Calculate health metrics for a package.

        Args:
            package_metadata: Package metadata dictionary
            registry: Registry name
            package_name: Package name

        Returns:
            Package health metrics
        """
        package_id = f"{registry}:{package_name}"

        maintenance_status = self._determine_maintenance_status(package_metadata)
        last_updated = self._extract_last_updated(package_metadata)
        days_since_update = self._calculate_days_since_update(last_updated)

        security_status, vulnerability_count, critical_count = self._determine_security_status(
            package_metadata
        )

        popularity_score, downloads, stars = self._calculate_popularity(package_metadata)

        documentation_score, has_readme, has_docs = self._assess_documentation(
            package_metadata
        )

        license_score, license_name = self._assess_license(package_metadata)

        metrics = PackageHealthMetrics(
            package_id=package_id,
            registry=registry,
            package_name=package_name,
            maintenance_status=maintenance_status,
            last_updated=last_updated,
            days_since_update=days_since_update,
            security_status=security_status,
            vulnerability_count=vulnerability_count,
            critical_vulnerability_count=critical_count,
            popularity_score=popularity_score,
            downloads=downloads,
            stars=stars,
            documentation_score=documentation_score,
            has_readme=has_readme,
            has_docs=has_docs,
            license_score=license_score,
            license=license_name,
        )

        metrics.health_score = metrics.calculate_health_score()

        return metrics

    def _determine_maintenance_status(
        self,
        package_metadata: dict[str, Any],
    ) -> MaintenanceStatus:
        """Determine maintenance status from metadata.

        Args:
            package_metadata: Package metadata

        Returns:
            Maintenance status
        """
        if package_metadata.get("deprecated"):
            return MaintenanceStatus.DEPRECATED

        last_updated = self._extract_last_updated(package_metadata)
        if last_updated:
            days_since = self._calculate_days_since_update(last_updated)
            if days_since and days_since > 365:
                return MaintenanceStatus.SLOW
            elif days_since and days_since > 180:
                return MaintenanceStatus.SLOW
            else:
                return MaintenanceStatus.ACTIVE

        return MaintenanceStatus.UNKNOWN

    def _extract_last_updated(self, package_metadata: dict[str, Any]) -> datetime | None:
        """Extract last updated timestamp.

        Args:
            package_metadata: Package metadata

        Returns:
            Last updated datetime or None
        """
        for key in ["created_at", "published_at", "updated_at", "last_modified"]:
            value = package_metadata.get(key)
            if value:
                if isinstance(value, datetime):
                    return value
                elif isinstance(value, str):
                    try:
                        return datetime.fromisoformat(value.replace("Z", "+00:00"))
                    except Exception:
                        pass

        return None

    def _calculate_days_since_update(self, last_updated: datetime | None) -> int | None:
        """Calculate days since last update.

        Args:
            last_updated: Last updated datetime

        Returns:
            Days since update or None
        """
        if not last_updated:
            return None

        delta = datetime.utcnow() - last_updated.replace(tzinfo=None)
        return delta.days

    def _determine_security_status(
        self,
        package_metadata: dict[str, Any],
    ) -> tuple[SecurityStatus, int, int]:
        """Determine security status from metadata.

        Args:
            package_metadata: Package metadata

        Returns:
            Tuple of (security_status, vulnerability_count, critical_count)
        """
        vulnerabilities = package_metadata.get("vulnerabilities", [])
        if not vulnerabilities:
            return (SecurityStatus.SECURE, 0, 0)

        critical_count = sum(
            1
            for v in vulnerabilities
            if v.get("severity", "").lower() in ["critical", "high"]
        )

        if critical_count > 0:
            return (SecurityStatus.CRITICAL, len(vulnerabilities), critical_count)
        else:
            return (SecurityStatus.VULNERABILITIES, len(vulnerabilities), 0)

    def _calculate_popularity(
        self,
        package_metadata: dict[str, Any],
    ) -> tuple[float, int, int | None]:
        """Calculate popularity score.

        Args:
            package_metadata: Package metadata

        Returns:
            Tuple of (popularity_score, downloads, stars)
        """
        downloads = package_metadata.get("downloads", 0) or 0
        stars = package_metadata.get("stars") or package_metadata.get("github_stars")

        if downloads > 10000000:
            popularity_score = 100.0
        elif downloads > 1000000:
            popularity_score = 90.0
        elif downloads > 100000:
            popularity_score = 75.0
        elif downloads > 10000:
            popularity_score = 60.0
        elif downloads > 1000:
            popularity_score = 40.0
        elif downloads > 100:
            popularity_score = 20.0
        else:
            popularity_score = 10.0

        if stars:
            if stars > 10000:
                popularity_score = max(popularity_score, 100.0)
            elif stars > 1000:
                popularity_score = max(popularity_score, 80.0)
            elif stars > 100:
                popularity_score = max(popularity_score, 60.0)

        return (popularity_score, downloads, stars)

    def _assess_documentation(
        self,
        package_metadata: dict[str, Any],
    ) -> tuple[float, bool, bool]:
        """Assess documentation quality.

        Args:
            package_metadata: Package metadata

        Returns:
            Tuple of (documentation_score, has_readme, has_docs)
        """
        has_readme = bool(
            package_metadata.get("readme") or package_metadata.get("readme_url")
        )
        has_docs = bool(
            package_metadata.get("documentation_url")
            or package_metadata.get("docs_url")
            or package_metadata.get("homepage")
        )

        score = 0.0
        if has_readme:
            score += 40.0
        if has_docs:
            score += 60.0

        return (score, has_readme, has_docs)

    def _assess_license(
        self,
        package_metadata: dict[str, Any],
    ) -> tuple[float, str | None]:
        """Assess license compatibility.

        Args:
            package_metadata: Package metadata

        Returns:
            Tuple of (license_score, license_name)
        """
        license_name = package_metadata.get("license")
        if not license_name:
            return (0.0, None)

        license_lower = str(license_name).lower()

        permissive_licenses = [
            "mit",
            "apache-2.0",
            "apache",
            "bsd-3-clause",
            "bsd-2-clause",
            "bsd",
            "isc",
        ]

        copyleft_licenses = [
            "gpl-3.0",
            "gpl-2.0",
            "gpl",
            "lgpl",
            "agpl",
        ]

        if any(perm in license_lower for perm in permissive_licenses):
            return (100.0, license_name)
        elif any(copy in license_lower for copy in copyleft_licenses):
            return (50.0, license_name)
        else:
            return (75.0, license_name)

