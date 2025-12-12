"""Budget status aggregation models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class BudgetStatusAggregate(BaseModel):
    """Aggregated budget status model."""

    budget_id: str = Field(..., description="Budget ID")
    period: str = Field(
        ...,
        description="Period in YYYY-MM format",
        pattern=r"^\d{4}-\d{2}$",
    )

    total_spent_usd: float = Field(
        ...,
        description="Total spending in USD",
        ge=0,
    )
    budget_limit_usd: float = Field(
        ...,
        description="Budget limit in USD",
        gt=0,
    )
    remaining_usd: float = Field(
        ...,
        description="Remaining budget in USD",
    )
    utilization_percent: float = Field(
        ...,
        description="Budget utilization percentage",
        ge=0,
    )

    status: str = Field(
        ...,
        description="Budget status: on_track, warning, critical, exceeded",
    )
    alert_sent: dict[str, bool] = Field(
        default_factory=lambda: {"warning": False, "critical": False, "exceeded": False},
        description="Alert flags for each threshold",
    )
    last_alert_at: datetime | None = Field(
        default=None,
        description="Last alert timestamp",
    )
    daily_digest_sent: bool = Field(
        default=False,
        description="Daily digest sent flag",
    )
    last_digest_at: datetime | None = Field(
        default=None,
        description="Last daily digest timestamp",
    )

    by_cloud_provider: dict[str, float] = Field(
        default_factory=dict,
        description="Spending breakdown by cloud provider",
    )
    by_service: dict[str, float] = Field(
        default_factory=dict,
        description="Spending breakdown by service",
    )
    by_resource_type: dict[str, float] = Field(
        default_factory=dict,
        description="Spending breakdown by resource type",
    )

    projected_monthly_spend: float | None = Field(
        default=None,
        description="Projected monthly spending based on current rate",
    )
    projected_exceed: bool = Field(
        default=False,
        description="Whether budget is projected to be exceeded",
    )
    days_until_exceed: int | None = Field(
        default=None,
        description="Days until budget is exceeded (if projected)",
    )

    last_updated: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump()
        data["_id"] = f"{self.budget_id}_{self.period}"
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BudgetStatusAggregate":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            BudgetStatusAggregate instance
        """
        if "_id" in data:
            del data["_id"]
        return cls(**data)

