"""Budget models for infrastructure budget management."""

import secrets
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class BudgetScopeType(str, Enum):
    """Budget scope types."""

    OVERALL = "overall"
    CLOUD_PROVIDER = "cloud_provider"
    ENVIRONMENT = "environment"


class BudgetStatus(str, Enum):
    """Budget status."""

    ACTIVE = "active"
    PAUSED = "paused"
    EXCEEDED = "exceeded"


class EnforcementMode(str, Enum):
    """Budget enforcement mode."""

    ALERT = "alert"
    WARN = "warn"
    BLOCK = "block"


class BudgetScope(BaseModel):
    """Budget scope definition."""

    type: BudgetScopeType = Field(..., description="Budget scope type")
    cloud_provider: Optional[str] = Field(
        default=None,
        description="Cloud provider (required if type is cloud_provider)",
    )
    environment_name: Optional[str] = Field(
        default=None,
        description="Environment name (dev, stage, prod, etc.) - required if type is environment and cloud_provider is not set",
    )

    def model_validate_scope(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validate scope based on type.
        
        Allows cloud_provider and environment_name to be set together for combined scoping.
        """
        scope_type = values.get("type")
        cloud_provider = values.get("cloud_provider")
        environment_name = values.get("environment_name")
        
        if scope_type == BudgetScopeType.CLOUD_PROVIDER:
            if not cloud_provider and not environment_name:
                raise ValueError("cloud_provider is required for cloud_provider scope")
        
        if scope_type == BudgetScopeType.ENVIRONMENT:
            if not environment_name and not cloud_provider:
                raise ValueError("environment_name is required for environment scope")
        
        return values


class InfrastructureBudget(BaseModel):
    """Infrastructure budget model."""

    budget_id: str = Field(
        ...,
        description="Unique budget identifier (e.g., 'bud_abc123')",
        min_length=10,
        max_length=100,
    )
    user_id: str = Field(..., description="User ID who owns this budget")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID (if budget is shared within org)",
    )
    name: str = Field(..., description="Budget name", min_length=1, max_length=200)
    description: Optional[str] = Field(
        default=None,
        description="Budget description",
        max_length=1000,
    )

    scope: BudgetScope = Field(..., description="Budget scope")

    monthly_limit_usd: float = Field(
        ...,
        description="Monthly budget limit in USD",
        gt=0,
    )
    alert_threshold_percent: float = Field(
        default=80.0,
        description="Alert threshold percentage (default: 80%)",
        ge=0,
        le=100,
    )
    critical_threshold_percent: float = Field(
        default=95.0,
        description="Critical alert threshold percentage (default: 95%)",
        ge=0,
        le=100,
    )

    period: str = Field(
        default="monthly",
        description="Budget period (always monthly, with quarterly/annual rollup)",
    )
    current_period_start: datetime = Field(
        ...,
        description="Current period start date",
    )
    current_period_end: datetime = Field(
        ...,
        description="Current period end date",
    )

    quarterly_rollup: bool = Field(
        default=True,
        description="Enable quarterly rollup for reporting",
    )
    annual_rollup: bool = Field(
        default=True,
        description="Enable annual rollup for reporting",
    )

    status: BudgetStatus = Field(
        default=BudgetStatus.ACTIVE,
        description="Budget status",
    )
    enforcement_mode: EnforcementMode = Field(
        default=EnforcementMode.ALERT,
        description="Budget enforcement mode",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )
    created_by: str = Field(..., description="User ID who created this budget")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"budget_id"})
        data["_id"] = self.budget_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InfrastructureBudget":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            InfrastructureBudget instance
        """
        if "_id" in data:
            data["budget_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        if "organization_id" in data and isinstance(data["organization_id"], ObjectId):
            data["organization_id"] = str(data["organization_id"])
        return cls(**data)

    def is_current_period(self, date: Optional[datetime] = None) -> bool:
        """Check if date falls within current period.

        Args:
            date: Date to check (defaults to now)

        Returns:
            True if date is in current period
        """
        if date is None:
            date = datetime.utcnow()
        return self.current_period_start <= date <= self.current_period_end

    def get_period_string(self) -> str:
        """Get period string in YYYY-MM format.

        Returns:
            Period string
        """
        return self.current_period_start.strftime("%Y-%m")


def generate_budget_id() -> str:
    """Generate unique budget ID.

    Returns:
        Budget ID string (e.g., 'bud_abc123def456')
    """
    return f"bud_{secrets.token_hex(12)}"


def get_month_period(date: Optional[datetime] = None) -> tuple[datetime, datetime]:
    """Get current month period start and end.

    Args:
        date: Reference date (defaults to now)

    Returns:
        Tuple of (period_start, period_end)
    """
    if date is None:
        date = datetime.utcnow()
    
    period_start = datetime(date.year, date.month, 1)
    
    if date.month == 12:
        period_end = datetime(date.year + 1, 1, 1) - timedelta(seconds=1)
    else:
        period_end = datetime(date.year, date.month + 1, 1) - timedelta(seconds=1)
    
    return period_start, period_end

