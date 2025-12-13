"""Spending models for infrastructure spending tracking."""

import secrets
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class InfrastructureSpending(BaseModel):
    """Infrastructure spending record model."""

    spending_id: str = Field(
        ...,
        description="Unique spending identifier (e.g., 'spend_abc123')",
        min_length=10,
        max_length=100,
    )
    budget_id: str = Field(
        ...,
        description="Budget ID this spending applies to",
    )
    user_id: str = Field(..., description="User ID")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID (if spending is for org)",
    )

    source_type: str = Field(
        ...,
        description="Source type: repository-analysis, manual_entry, cloud_billing_api",
    )
    source_id: Optional[str] = Field(
        default=None,
        description="Source ID (resource_id if from repository)",
    )
    component_id: Optional[str] = Field(
        default=None,
        description="Component article_id if from analysis",
    )

    amount_usd: float = Field(
        ...,
        description="Spending amount in USD",
        gt=0,
    )
    period: str = Field(
        ...,
        description="Period in YYYY-MM format",
        pattern=r"^\d{4}-\d{2}$",
    )
    date: datetime = Field(..., description="Spending date")

    cloud_provider: Optional[str] = Field(
        default=None,
        description="Cloud provider (aws, gcp, azure, etc.)",
    )
    environment_name: Optional[str] = Field(
        default=None,
        description="Environment name (dev, stage, prod, etc.)",
    )
    service: Optional[str] = Field(
        default=None,
        description="Service name (ec2, rds, s3, etc.)",
    )
    resource_type: Optional[str] = Field(
        default=None,
        description="Resource type (compute, storage, network, etc.)",
    )
    resource_spec: Optional[dict[str, Any]] = Field(
        default=None,
        description="Resource specification details",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"spending_id"})
        data["_id"] = self.spending_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InfrastructureSpending":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            InfrastructureSpending instance
        """
        if "_id" in data:
            data["spending_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        if "organization_id" in data and isinstance(data["organization_id"], ObjectId):
            data["organization_id"] = str(data["organization_id"])
        return cls(**data)


def generate_spending_id() -> str:
    """Generate unique spending ID.

    Returns:
        Spending ID string (e.g., 'spend_abc123def456')
    """
    return f"spend_{secrets.token_hex(12)}"

