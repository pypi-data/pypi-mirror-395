"""Pricing data models."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class PricingTier(BaseModel):
    """Pricing for a specific tier."""

    hourly: float = Field(..., description="Hourly price")
    monthly: float = Field(..., description="Monthly price")
    annual: float = Field(..., description="Annual price")


class PricingData(BaseModel):
    """Normalized pricing data."""

    cloud: str = Field(..., description="Cloud provider (aws, gcp, azure)")
    service: str = Field(..., description="Service name (rds, ec2, s3)")
    resource_type: str = Field(..., description="Resource type (e.g., db.t3.medium)")
    region: str = Field(..., description="Region identifier")
    pricing: dict[str, PricingTier] = Field(
        ..., description="Pricing tiers (on_demand, reserved_1yr, etc.)"
    )
    specifications: dict[str, Any] = Field(
        default_factory=dict, description="Resource specifications (vcpu, memory_gb, etc.)"
    )
    lookup_key: str = Field(..., description="Unique lookup key")
    embedding: Optional[list[float]] = Field(
        default=None, description="Vector embedding (added in Stage 3)"
    )
