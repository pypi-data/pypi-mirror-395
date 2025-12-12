"""Report template models for documentation generation."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class TemplateEngine(str, Enum):
    """Template engine type."""

    JINJA2 = "jinja2"
    MUSTACHE = "mustache"
    MARKDOWN = "markdown"


class OutputFormat(str, Enum):
    """Output format."""

    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    DOCX = "docx"
    JSON = "json"


class ReportTemplate(BaseModel):
    """Report template metadata."""

    template_id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    version: str = Field(..., description="Semantic version (e.g., '1.2.3')")

    template_engine: TemplateEngine = Field(default=TemplateEngine.JINJA2, description="Template engine")
    template_content: str = Field(..., description="Template content")
    output_formats: list[OutputFormat] = Field(default_factory=lambda: [OutputFormat.MARKDOWN], description="Supported output formats")

    document_type: str = Field(..., description="Document type (compliance_report, security_report, etc.)")
    compliance_standards: list[str] = Field(default_factory=list, description="Applicable compliance standards")
    resource_types: list[str] = Field(default_factory=list, description="Applicable resource types")

    variables: dict[str, Any] = Field(default_factory=dict, description="Template variables schema")
    sections: list[str] = Field(default_factory=list, description="Required sections")
    optional_sections: list[str] = Field(default_factory=list, description="Optional sections")

    branding: dict[str, Any] = Field(default_factory=dict, description="Branding configuration (logo, colors, etc.)")
    styles: dict[str, Any] = Field(default_factory=dict, description="CSS/styles for HTML/PDF output")

    author: Optional[str] = Field(default=None, description="Template author")
    tags: list[str] = Field(default_factory=list, description="Template tags")
    quality_score: int = Field(default=0, ge=0, le=100, description="Quality score")

    is_latest: bool = Field(default=True, description="Is latest version")
    previous_version: Optional[str] = Field(default=None, description="Previous version ID")
    changelog: list[str] = Field(default_factory=list, description="Changelog entries")

    visibility: str = Field(default="public", description="public, private, organization")
    user_id: Optional[str] = Field(default=None, description="Owner user ID")
    organization_id: Optional[str] = Field(default=None, description="Owner organization ID")

    usage_count: int = Field(default=0, ge=0, description="Usage count")
    last_used_at: Optional[datetime] = Field(default=None, description="Last usage timestamp")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = Field(default=None, description="Publication timestamp")

