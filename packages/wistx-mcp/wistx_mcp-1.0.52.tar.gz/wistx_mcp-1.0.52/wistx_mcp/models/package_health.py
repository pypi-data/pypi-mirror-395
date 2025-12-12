"""Package health metrics data model (local copy for MCP server)."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MaintenanceStatus(str, Enum):
    """Package maintenance status."""

    ACTIVE = "active"
    SLOW = "slow"
    DEPRECATED = "deprecated"
    UNKNOWN = "unknown"


class SecurityStatus(str, Enum):
    """Package security status."""

    SECURE = "secure"
    VULNERABILITIES = "vulnerabilities"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class PackageHealthMetrics(BaseModel):
    """Package health metrics model."""

    package_id: str = Field(..., description="Package identifier (registry:name)")
    registry: str = Field(..., description="Registry name (pypi, npm, terraform)")
    package_name: str = Field(..., description="Package name")

    health_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Overall health score (0-100)",
    )

    maintenance_status: MaintenanceStatus = Field(
        default=MaintenanceStatus.UNKNOWN,
        description="Maintenance status",
    )
    last_updated: datetime | None = Field(
        default=None,
        description="Last package update timestamp",
    )
    days_since_update: int | None = Field(
        default=None,
        description="Days since last update",
    )

    security_status: SecurityStatus = Field(
        default=SecurityStatus.UNKNOWN,
        description="Security status",
    )
    vulnerability_count: int = Field(
        default=0,
        ge=0,
        description="Number of known vulnerabilities",
    )
    critical_vulnerability_count: int = Field(
        default=0,
        ge=0,
        description="Number of critical vulnerabilities",
    )

    popularity_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Popularity score based on downloads/stars (0-100)",
    )
    downloads: int = Field(
        default=0,
        ge=0,
        description="Total downloads (or stars for GitHub)",
    )
    stars: int | None = Field(
        default=None,
        ge=0,
        description="GitHub stars count",
    )

    documentation_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Documentation quality score (0-100)",
    )
    has_readme: bool = Field(
        default=False,
        description="Has README file",
    )
    has_docs: bool = Field(
        default=False,
        description="Has documentation website",
    )

    license_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="License compatibility score (0-100)",
    )
    license: str | None = Field(
        default=None,
        description="Package license",
    )

    calculated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When metrics were calculated",
    )
    calculated_version: str = Field(
        default="1.0",
        description="Version of health calculation logic",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )

    def calculate_health_score(self) -> float:
        """Calculate overall health score.

        Returns:
            Health score (0-100)
        """
        maintenance_weight = 0.3
        security_weight = 0.3
        popularity_weight = 0.2
        documentation_weight = 0.1
        license_weight = 0.1

        maintenance_score = self._calculate_maintenance_score()
        security_score = self._calculate_security_score()
        popularity_score = self.popularity_score
        documentation_score = self.documentation_score
        license_score = self.license_score

        total_score = (
            maintenance_score * maintenance_weight +
            security_score * security_weight +
            popularity_score * popularity_weight +
            documentation_score * documentation_weight +
            license_score * license_weight
        )

        return round(total_score, 2)

    def _calculate_maintenance_score(self) -> float:
        """Calculate maintenance score.

        Returns:
            Maintenance score (0-100)
        """
        if self.maintenance_status == MaintenanceStatus.ACTIVE:
            if self.days_since_update is not None:
                if self.days_since_update <= 30:
                    return 100.0
                elif self.days_since_update <= 90:
                    return 80.0
                elif self.days_since_update <= 180:
                    return 60.0
                else:
                    return 40.0
            return 80.0
        elif self.maintenance_status == MaintenanceStatus.SLOW:
            return 40.0
        elif self.maintenance_status == MaintenanceStatus.DEPRECATED:
            return 10.0
        else:
            return 50.0

    def _calculate_security_score(self) -> float:
        """Calculate security score.

        Returns:
            Security score (0-100)
        """
        if self.security_status == SecurityStatus.SECURE:
            return 100.0
        elif self.security_status == SecurityStatus.VULNERABILITIES:
            if self.critical_vulnerability_count > 0:
                return max(0, 100 - (self.critical_vulnerability_count * 30))
            else:
                return max(0, 100 - (self.vulnerability_count * 10))
        elif self.security_status == SecurityStatus.CRITICAL:
            return 0.0
        else:
            return 50.0



















