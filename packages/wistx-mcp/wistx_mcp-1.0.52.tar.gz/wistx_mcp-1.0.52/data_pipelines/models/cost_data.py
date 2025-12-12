"""FOCUS-compliant cost data models."""

from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator


class CostAllocationDimension(BaseModel):
    """Cost allocation dimension following FinOps best practices."""

    business_unit: str | None = Field(default=None, description="Business unit")
    department: str | None = Field(default=None, description="Department")
    team: str | None = Field(default=None, description="Team")
    project: str | None = Field(default=None, description="Project")
    environment: str | None = Field(default=None, description="Environment (prod/staging/dev)")
    application: str | None = Field(default=None, description="Application name")
    service: str | None = Field(default=None, description="Service name")
    component: str | None = Field(default=None, description="Component name")
    cost_center: str | None = Field(default=None, description="Cost center")
    owner_email: str | None = Field(default=None, description="Owner email")
    owner_team: str | None = Field(default=None, description="Owner team")
    custom_tags: dict[str, str] = Field(default_factory=dict, description="Custom tags")


class FOCUSCostData(BaseModel):
    """FOCUS-compliant cost data model.

    Follows FinOps Open Cost and Usage Specification (FOCUS) v1.0.
    Reference: https://focus.finops.org/
    """

    billing_account_id: str = Field(..., description="Billing account identifier")
    billing_account_name: str = Field(..., description="Billing account name")
    billing_currency: str = Field(default="USD", description="Billing currency (ISO 4217)")
    billing_period_start: datetime = Field(..., description="Billing period start (ISO 8601)")
    billing_period_end: datetime = Field(..., description="Billing period end (ISO 8601)")

    provider: str = Field(..., description="Cloud provider (aws/gcp/azure/oracle/alibaba)")
    invoice_issuer: str = Field(..., description="Invoice issuer name")
    publisher: str | None = Field(default=None, description="Marketplace publisher")

    region_id: str = Field(..., description="Region identifier")
    region_name: str = Field(..., description="Region name")
    availability_zone: str | None = Field(default=None, description="Availability zone")

    resource_id: str = Field(..., description="Resource identifier")
    resource_name: str = Field(..., description="Resource name")
    resource_type: str = Field(..., description="Resource type")

    service_category: str = Field(..., description="Service category")
    service_name: str = Field(..., description="Service name")
    service_subcategory: str | None = Field(default=None, description="Service subcategory")

    sku_id: str = Field(..., description="SKU identifier")
    sku_description: str = Field(..., description="SKU description")
    sku_price_id: str = Field(..., description="SKU price identifier")

    pricing_category: str = Field(..., description="Pricing category")
    pricing_quantity: float = Field(..., description="Pricing quantity")
    pricing_unit: str = Field(..., description="Pricing unit")

    list_cost: Decimal = Field(..., description="List cost")
    list_unit_price: Decimal = Field(..., description="List unit price")
    effective_cost: Decimal = Field(..., description="Effective cost")
    billed_cost: Decimal = Field(..., description="Billed cost")
    contracted_cost: Decimal | None = Field(default=None, description="Contracted cost")

    consumed_quantity: float = Field(..., description="Consumed quantity")
    consumed_unit: str = Field(..., description="Consumed unit")

    charge_category: str = Field(default="Usage", description="Charge category")
    charge_description: str = Field(..., description="Charge description")
    charge_frequency: str = Field(..., description="Charge frequency")
    charge_period_start: datetime = Field(..., description="Charge period start")
    charge_period_end: datetime = Field(..., description="Charge period end")

    tags: dict[str, str] = Field(default_factory=dict, description="Cost allocation tags")

    sub_account_id: str | None = Field(default=None, description="Sub account ID")
    sub_account_name: str | None = Field(default=None, description="Sub account name")

    contextual_description: str | None = Field(default=None, description="Contextual description for retrieval")
    embedding: list[float] | None = Field(default=None, description="Vector embedding")
    source_hash: str = Field(..., description="Source data hash for change detection")
    last_updated: datetime = Field(default_factory=lambda: datetime.utcnow(), description="Last update timestamp")

    lookup_key: str = Field(..., description="Unique lookup key")

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Validate provider."""
        valid_providers = {"aws", "gcp", "azure", "oracle", "alibaba"}
        if v.lower() not in valid_providers:
            raise ValueError(f"Provider must be one of {valid_providers}")
        return v.lower()

    @field_validator("service_category")
    @classmethod
    def validate_service_category(cls, v: str) -> str:
        """Validate service category."""
        valid_categories = {
            "Compute",
            "Storage",
            "Network",
            "Database",
            "Analytics",
            "Security",
            "Management",
            "Integration",
        }
        if v not in valid_categories:
            raise ValueError(f"Service category must be one of {valid_categories}")
        return v

    @field_validator("charge_category")
    @classmethod
    def validate_charge_category(cls, v: str) -> str:
        """Validate charge category."""
        valid_categories = {"Usage", "Tax", "Discount", "Credit", "Refund"}
        if v not in valid_categories:
            raise ValueError(f"Charge category must be one of {valid_categories}")
        return v

    @field_validator("pricing_category")
    @classmethod
    def validate_pricing_category(cls, v: str) -> str:
        """Validate pricing category."""
        valid_categories = {"OnDemand", "Reserved", "Spot", "Committed", "SavingsPlan"}
        if v not in valid_categories:
            raise ValueError(f"Pricing category must be one of {valid_categories}")
        return v

    def to_searchable_text(self) -> str:
        """Generate searchable text for embedding.

        Returns:
            Searchable text combining contextual description and base fields
        """
        parts = []

        if self.contextual_description:
            parts.append(self.contextual_description)

        parts.append(f"{self.provider} {self.service_name} {self.resource_type}")
        parts.append(f"in {self.region_name}")
        parts.append(f"costs {self.list_unit_price} per {self.pricing_unit}")

        if self.sku_description:
            parts.append(self.sku_description)

        if self.charge_description:
            parts.append(self.charge_description)

        return " ".join(parts)

    def model_dump_for_mongodb(self) -> dict[str, Any]:
        """Convert to MongoDB-compatible dictionary.

        Returns:
            Dictionary with MongoDB-compatible types
        """
        data = self.model_dump()
        data["list_cost"] = float(self.list_cost)
        data["list_unit_price"] = float(self.list_unit_price)
        data["effective_cost"] = float(self.effective_cost)
        data["billed_cost"] = float(self.billed_cost)
        if self.contracted_cost:
            data["contracted_cost"] = float(self.contracted_cost)
        return data

    def model_dump_for_pinecone(self) -> dict[str, Any]:
        """Convert to Pinecone-compatible dictionary.

        Returns:
            Dictionary with Pinecone metadata and vector
        """
        last_updated_dt: datetime = getattr(self, "last_updated", datetime.utcnow())
        last_updated_str = last_updated_dt.isoformat() if isinstance(last_updated_dt, datetime) else datetime.utcnow().isoformat()

        metadata = {
            "collection": "cost_data_focus",
            "provider": self.provider,
            "service_category": self.service_category,
            "service_name": self.service_name,
            "region_id": self.region_id,
            "pricing_category": self.pricing_category,
            "resource_type": self.resource_type,
            "list_unit_price": float(self.list_unit_price),
            "billing_currency": self.billing_currency,
            "lookup_key": self.lookup_key,
            "last_updated": last_updated_str,
        }

        if self.service_subcategory:
            metadata["service_subcategory"] = self.service_subcategory

        if self.tags:
            metadata["tags"] = self.tags

        return {
            "id": f"cost_{self.provider}_{self.lookup_key}",
            "values": self.embedding or [],
            "metadata": metadata,
        }

