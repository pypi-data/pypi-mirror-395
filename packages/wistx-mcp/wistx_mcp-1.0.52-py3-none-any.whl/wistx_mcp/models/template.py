"""Template metadata models."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class TemplateSource(str, Enum):
    """Template source type."""

    GITHUB = "github"
    USER = "user"


class TemplateMetadata(BaseModel):
    """Template metadata stored in MongoDB."""

    template_id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    version: str = Field(..., description="Semantic version (e.g., '1.2.3')")

    source_type: TemplateSource = Field(..., description="Source type")
    source_url: Optional[str] = Field(default=None, description="Source URL or path")
    source_ref: Optional[str] = Field(default=None, description="Git ref (branch/tag/commit)")

    project_type: str = Field(..., description="Project type (terraform, kubernetes, etc.)")
    architecture_type: Optional[str] = Field(default=None, description="Architecture pattern")
    cloud_provider: Optional[str] = Field(default=None, description="Cloud provider")

    structure: dict[str, Any] = Field(..., description="Template file structure")
    variables: dict[str, Any] = Field(default_factory=dict, description="Template variables")
    prompts: list[dict[str, str]] = Field(default_factory=list, description="User prompts")

    author: Optional[str] = Field(default=None, description="Template author")
    tags: list[str] = Field(default_factory=list, description="Template tags")
    quality_score: int = Field(default=0, ge=0, le=100, description="Quality score")

    usage_count: int = Field(default=0, ge=0, description="Usage count")
    last_used_at: Optional[datetime] = Field(default=None, description="Last usage timestamp")

    is_latest: bool = Field(default=True, description="Is latest version")
    previous_version: Optional[str] = Field(default=None, description="Previous version ID")
    changelog: list[str] = Field(default_factory=list, description="Changelog entries")

    visibility: str = Field(default="public", description="public, private, organization")
    user_id: Optional[str] = Field(default=None, description="Owner user ID")
    organization_id: Optional[str] = Field(default=None, description="Owner organization ID")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = Field(default=None, description="Publication timestamp")

