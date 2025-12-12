"""Documentation section model for hierarchical organization."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field


class SectionType(str, Enum):
    """Section type enumeration."""

    API = "api"
    ARCHITECTURE = "architecture"
    COMPONENT_GROUP = "component_group"
    WORKFLOW = "workflow"
    CONFIGURATION = "configuration"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    FINOPS = "finops"
    PLATFORM = "platform"
    SRE = "sre"
    INFRASTRUCTURE = "infrastructure"
    AUTOMATION = "automation"
    CUSTOM = "custom"


class DocumentationSection(BaseModel):
    """Documentation section for hierarchical organization.

    Sections group related components into logical functional areas,
    similar to CodeWiki's structure.
    """

    section_id: str = Field(
        ...,
        description="Unique section identifier",
        min_length=5,
        max_length=200,
    )
    resource_id: str = Field(
        ...,
        description="Associated IndexedResource ID",
    )
    user_id: str = Field(
        ...,
        description="User ID who owns this section",
    )

    title: str = Field(
        ...,
        description="Section title (e.g., 'Kubernetes API Definition and Management')",
        min_length=10,
        max_length=200,
    )
    summary: str = Field(
        ...,
        description="Section-level summary/overview",
        min_length=100,
        max_length=2000,
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed section description",
    )

    section_type: SectionType = Field(
        ...,
        description="Type of section",
    )

    architecture_diagram: Optional[str] = Field(
        default=None,
        description="Architecture diagram (Mermaid format) for this section",
    )
    architecture_diagram_format: Optional[str] = Field(
        default=None,
        description="Diagram format (mermaid, plantuml)",
    )

    parent_section_id: Optional[str] = Field(
        default=None,
        description="Parent section ID (for nested sections)",
    )
    child_section_ids: list[str] = Field(
        default_factory=list,
        description="Child section IDs",
    )

    component_article_ids: list[str] = Field(
        default_factory=list,
        description="KnowledgeArticle IDs belonging to this section",
    )

    tags: list[str] = Field(
        default_factory=list,
        description="Tags for categorization",
        max_items=20,
    )
    categories: list[str] = Field(
        default_factory=list,
        description="Hierarchical categories",
    )

    quality_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Section quality score",
    )
    completeness_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Completeness score (based on component coverage)",
    )

    version: str = Field(
        default="1.0",
        description="Section version",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    commit_sha: Optional[str] = Field(
        default=None,
        description="Git commit SHA when section was created",
    )
    branch: Optional[str] = Field(
        default=None,
        description="Git branch",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage."""
        return self.model_dump(mode="json")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DocumentationSection":
        """Create from dictionary."""
        return cls(**data)

