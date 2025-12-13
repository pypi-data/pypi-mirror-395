"""Template storage models for quality-scored templates."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class QualityTemplate(BaseModel):
    """Quality template model for MongoDB storage."""

    template_id: str = Field(..., description="Unique template ID (UUID)")
    type: str = Field(..., description="Template type: repository_tree or infrastructure_visualization")
    source_repo_url: str | None = Field(None, description="Original repository URL")
    quality_score: float = Field(..., ge=0.0, le=100.0, description="Overall quality score")
    score_breakdown: dict[str, float] = Field(default_factory=dict, description="Detailed score breakdown")
    content: dict[str, Any] = Field(..., description="Template content (tree structure or visualization)")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Original metadata")
    tags: list[str] = Field(default_factory=list, description="Tags for filtering (project_type, cloud_provider, etc.)")
    categories: list[str] = Field(default_factory=list, description="Categories (terraform, kubernetes, devops, etc.)")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    last_used_at: datetime | None = Field(None, description="Last usage timestamp")
    usage_count: int = Field(default=0, description="Usage count")
    user_id: str | None = Field(None, description="User ID for user-specific templates")
    organization_id: str | None = Field(None, description="Organization ID for org-specific templates")
    visibility: str = Field(default="global", description="Visibility: global, user, or organization")

    model_config = {"extra": "forbid"}


class TemplateFilter(BaseModel):
    """Template filter model for querying."""

    type: str | None = None
    min_quality_score: float | None = None
    tags: list[str] | None = None
    categories: list[str] | None = None
    visibility: list[str] | None = None
    user_id: str | None = None
    organization_id: str | None = None
    limit: int = Field(default=10, ge=1, le=100)

    model_config = {"extra": "forbid"}

