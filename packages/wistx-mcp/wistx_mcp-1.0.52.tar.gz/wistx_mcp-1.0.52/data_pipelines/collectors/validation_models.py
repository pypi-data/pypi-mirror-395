"""Pydantic models for raw data validation."""

from typing import Any

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


class RawComplianceControl(BaseModel):
    """Raw compliance control data model for validation."""

    control_id: str | None = Field(default=None, min_length=1, description="Control identifier")
    requirement: str | None = Field(default=None, min_length=1, description="Requirement text")
    title: str | None = Field(default=None, min_length=1, description="Control title")
    description: str | None = Field(default=None, min_length=1, description="Control description")
    testing_procedures: list[str] = Field(default_factory=list, description="Testing procedures")
    guidance: str | None = Field(default=None, description="Guidance text")
    source_url: HttpUrl | str = Field(..., description="Source URL")
    benchmark_id: str | None = Field(default=None, description="Benchmark ID (for CIS)")
    article_id: str | None = Field(default=None, description="Article ID (for GDPR)")
    requirement_id: str | None = Field(default=None, description="Requirement ID")
    content: str | None = Field(default=None, description="Content text")
    audit: str | None = Field(default=None, description="Audit information")
    remediation: str | None = Field(default=None, description="Remediation steps")
    level: str | None = Field(default=None, description="Level (for CIS)")
    cloud: str | None = Field(default=None, description="Cloud provider")
    criteria: str | None = Field(default=None, description="Criteria (for SOC2)")
    technical_safeguards: list[str] = Field(
        default_factory=list, description="Technical safeguards (for HIPAA)"
    )

    @model_validator(mode="after")
    def validate_at_least_one_id(self) -> "RawComplianceControl":
        """Ensure at least one ID field is provided."""
        ids = [
            self.control_id,
            self.benchmark_id,
            self.article_id,
            self.requirement_id,
        ]
        if not any(id_field and id_field.strip() for id_field in ids):
            raise ValueError(
                "At least one ID field (control_id, benchmark_id, article_id, requirement_id) must be provided"
            )
        return self

    @field_validator("control_id", "requirement", "title", "description", mode="before")
    @classmethod
    def validate_not_empty(cls, v: Any) -> Any:
        """Ensure string fields are not empty after stripping."""
        if isinstance(v, str):
            stripped = v.strip()
            if not stripped:
                return None
            return stripped
        return v

    @field_validator("source_url", mode="before")
    @classmethod
    def validate_url(cls, v: Any) -> str:
        """Validate and normalize URL."""
        if isinstance(v, str):
            return v.strip()
        return str(v)

    class Config:
        extra = "allow"
        str_strip_whitespace = True


class RawPricingData(BaseModel):
    """Raw pricing data model for validation."""

    cloud: str = Field(..., min_length=1, description="Cloud provider")
    service: str = Field(..., min_length=1, description="Service name")
    resource_type: str = Field(..., min_length=1, description="Resource type")
    region: str = Field(..., min_length=1, description="Region")
    pricing: dict[str, Any] = Field(..., description="Pricing information")
    sku: str | None = Field(default=None, description="SKU identifier")
    source_url: HttpUrl | str | None = Field(default=None, description="Source URL")

    @field_validator("cloud", "service", "region", mode="before")
    @classmethod
    def validate_lowercase(cls, v: Any) -> str:
        """Convert to lowercase."""
        if isinstance(v, str):
            return v.strip().lower()
        return str(v).lower()

    class Config:
        extra = "allow"
        str_strip_whitespace = True


class RawCodeExample(BaseModel):
    """Raw code example model for validation."""

    title: str = Field(..., min_length=1, description="Example title")
    description: str | None = Field(default=None, description="Description")
    code: str = Field(..., min_length=10, description="Code content")
    code_type: str = Field(..., description="Code type (terraform, kubernetes, etc.)")
    cloud_provider: str | None = Field(default=None, description="Cloud provider")
    github_url: HttpUrl | str | None = Field(default=None, description="GitHub URL")
    stars: int = Field(default=0, ge=0, description="GitHub stars")
    quality_score: int = Field(default=0, ge=0, le=100, description="Quality score")

    class Config:
        extra = "allow"
        str_strip_whitespace = True


class RawDocumentation(BaseModel):
    """Raw documentation model for validation."""

    title: str = Field(..., min_length=1, description="Document title")
    content: str = Field(..., min_length=100, description="Document content")
    source_url: HttpUrl | str = Field(..., description="Source URL")
    doc_type: str = Field(..., description="Document type")
    category: str | None = Field(default=None, description="Category")

    class Config:
        extra = "allow"
        str_strip_whitespace = True

