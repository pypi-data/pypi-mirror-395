"""Knowledge article data models.

Unified model for all knowledge base content across domains:
compliance, FinOps, architecture, security, DevOps, infrastructure.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class Domain(str, Enum):
    """Knowledge domain enumeration."""

    COMPLIANCE = "compliance"
    FINOPS = "finops"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    DEVOPS = "devops"
    INFRASTRUCTURE = "infrastructure"
    CLOUD = "cloud"
    AUTOMATION = "automation"
    PLATFORM = "platform"
    SRE = "sre"


class ContentType(str, Enum):
    """Content type enumeration."""

    CONTROL = "control"
    GUIDE = "guide"
    PATTERN = "pattern"
    STRATEGY = "strategy"
    CHECKLIST = "checklist"
    REFERENCE = "reference"
    BEST_PRACTICE = "best_practice"


class Reference(BaseModel):
    """Reference to external documentation."""

    type: str = Field(..., description="Reference type (official, guide, blog, etc.)")
    url: str = Field(..., description="Reference URL")
    title: str = Field(..., description="Reference title")


class VersionHistory(BaseModel):
    """Version history entry."""

    version: str = Field(..., description="Version number")
    updated_at: datetime = Field(..., description="Update timestamp")
    changes: str = Field(..., description="Description of changes")


class KnowledgeArticle(BaseModel):
    """Unified knowledge article model for all domains.
    
    Supports compliance, FinOps, architecture, security, DevOps, and infrastructure
    knowledge with cross-domain relationships.
    """

    article_id: str = Field(
        ...,
        description="Unique article identifier (e.g., 'compliance-pci-dss-overview')",
        min_length=5,
        max_length=200,
    )
    domain: Domain = Field(..., description="Primary knowledge domain")
    subdomain: str = Field(
        ...,
        description="Subdomain (e.g., 'pci-dss', 'cost-optimization', 'microservices')",
        min_length=2,
        max_length=100,
    )
    content_type: ContentType = Field(..., description="Type of content")

    title: str = Field(..., description="Article title", min_length=10, max_length=200)
    summary: str = Field(
        ...,
        description="Brief summary (for search snippets)",
        min_length=50,
        max_length=500,
    )
    content: str = Field(
        ...,
        description="Full content (markdown supported)",
        min_length=100,
    )
    structured_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Domain-specific structured fields (flexible)",
    )

    tags: list[str] = Field(
        default_factory=list,
        description="Flexible tags for categorization",
        max_items=20,
    )
    categories: list[str] = Field(
        default_factory=list,
        description="Hierarchical categories",
    )
    industries: list[str] = Field(
        default_factory=list,
        description="Applicable industries (healthcare, finance, retail, etc.)",
    )
    cloud_providers: list[str] = Field(
        default_factory=list,
        description="Cloud providers (aws, gcp, azure, multi-cloud)",
    )
    services: list[str] = Field(
        default_factory=list,
        description="Cloud services (rds, s3, kubernetes, terraform, etc.)",
    )

    related_articles: list[str] = Field(
        default_factory=list,
        description="Related article IDs (cross-domain links)",
    )
    related_controls: list[str] = Field(
        default_factory=list,
        description="Related compliance control IDs",
    )
    related_code_examples: list[str] = Field(
        default_factory=list,
        description="Related code example IDs",
    )

    compliance_impact: Optional[dict[str, Any]] = Field(
        default=None,
        description="Compliance implications and requirements",
    )
    cost_impact: Optional[dict[str, Any]] = Field(
        default=None,
        description="FinOps/cost implications and optimization opportunities",
    )
    security_impact: Optional[dict[str, Any]] = Field(
        default=None,
        description="Security implications and considerations",
    )

    source_url: str = Field(..., description="Source URL for this article")
    references: list[Reference] = Field(
        default_factory=list,
        description="External references",
    )
    version: str = Field(
        default="1.0",
        description="Article version",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    quality_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Content quality score (0-100)",
    )
    source_credibility: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Source credibility score (0-100)",
    )
    freshness_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Content freshness score (0-100)",
    )

    version_history: list[VersionHistory] = Field(
        default_factory=list,
        description="Version history",
    )

    source_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 hash of raw source data (for change detection)",
    )
    content_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 hash of processed content (for change detection)",
    )
    contextual_description: Optional[str] = Field(
        default=None,
        description="Contextual description prepended before embedding (max 2000 chars)",
        max_length=2000,
    )
    context_generated_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when contextual description was generated",
    )
    context_version: Optional[str] = Field(
        default=None,
        description="Version of context generation logic",
    )

    source_urls: Optional[dict[str, str]] = Field(
        default=None,
        description="Multiple source URLs: snapshot (commit SHA), latest (branch), file",
    )
    commit_sha: Optional[str] = Field(
        default=None,
        description="Git commit SHA when analysis was performed",
    )
    branch: Optional[str] = Field(
        default=None,
        description="Git branch when analysis was performed",
    )
    analyzed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when analysis was performed",
    )

    embedding: Optional[list[float]] = Field(
        default=None,
        description="Vector embedding (1536 dimensions, stored in Pinecone)",
    )

    chunk_index: Optional[int] = Field(
        default=None,
        description="Chunk index (None = full file, 0+ = chunk number)",
    )
    parent_article_id: Optional[str] = Field(
        default=None,
        description="Parent article ID (for chunks, links to parent file)",
    )
    total_chunks: Optional[int] = Field(
        default=None,
        description="Total number of chunks in parent file",
    )
    start_line: Optional[int] = Field(
        default=None,
        description="Start line number (for chunks)",
    )
    end_line: Optional[int] = Field(
        default=None,
        description="End line number (for chunks)",
    )

    user_id: Optional[str] = Field(
        default=None,
        description="User ID for user-provided content (null = global/shared)",
    )
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID for org-shared content",
    )
    visibility: str = Field(
        default="global",
        description="Content visibility scope: global, user, or organization",
    )
    source_type: str = Field(
        default="automated",
        description="Source of the content: automated, user_upload, repository, documentation",
    )
    resource_id: Optional[str] = Field(
        default=None,
        description="Associated IndexedResource ID (for cleanup)",
    )

    def to_searchable_text(self) -> str:
        """Convert article to searchable text for embedding.
        
        Includes contextual description if available (for contextual retrieval).
        
        Returns:
            Searchable text string with contextual description prepended
        """
        text_parts = []
        
        if self.contextual_description:
            text_parts.append(self.contextual_description)
            text_parts.append("")
        
        text_parts.append(f"{self.title}\n{self.summary}\n{self.content}\n")
        text_parts.append(" ".join(self.tags))
        text_parts.append(" ".join(self.categories))
        
        if self.structured_data and isinstance(self.structured_data, dict):
            structured_values = [
                str(v) for v in self.structured_data.values() if isinstance(v, str)  # type: ignore[attr-defined]
            ]
            text_parts.append(" " + " ".join(structured_values))
        
        return "\n".join(text_parts)

    def get_cloud_providers(self) -> list[str]:
        """Extract cloud providers from cloud_providers field.
        
        Returns:
            List of cloud provider names
        """
        return sorted(set(self.cloud_providers))

    def get_industries(self) -> list[str]:
        """Get applicable industries.
        
        Returns:
            List of industry names
        """
        return sorted(set(self.industries))

    def model_dump_for_mongodb(self) -> dict[str, Any]:
        """Dump model for MongoDB storage (excludes embedding).
        
        Returns:
            Dictionary ready for MongoDB storage
        """
        data = self.model_dump(mode="json", exclude={"embedding"})
        return data

    def model_dump_for_pinecone(self) -> dict[str, Any]:
        """Dump model for Pinecone storage (embedding + minimal metadata).
        
        Returns:
            Dictionary ready for Pinecone storage
        """
        domain_str = self.domain.value if hasattr(self.domain, "value") else str(self.domain)
        content_type_str = self.content_type.value if hasattr(self.content_type, "value") else str(self.content_type)
        
        return {
            "id": f"knowledge_{self.article_id}",
            "values": self.embedding or [],
            "metadata": {
                "collection": "knowledge_articles",
                "article_id": self.article_id,
                "domain": domain_str,
                "subdomain": self.subdomain,
                "content_type": content_type_str,
                "title": self.title[:200],
                "summary": self.summary[:1000],
                "tags": ",".join(self.tags[:10]),
                "industries": ",".join(self.industries[:5]),
                "cloud_providers": ",".join(self.cloud_providers[:5]),
            },
        }

