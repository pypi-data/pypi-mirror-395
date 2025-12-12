"""Request models for indexing endpoints."""

from typing import Optional

from pydantic import BaseModel, Field


class IndexRepositoryRequest(BaseModel):
    """Request model for indexing a GitHub repository."""

    repo_url: str = Field(..., description="GitHub repository URL")
    branch: Optional[str] = Field(default=None, description="Branch name (default: main)")
    name: Optional[str] = Field(default=None, description="Custom name for the resource")
    description: Optional[str] = Field(default=None, description="Resource description")
    tags: list[str] = Field(default_factory=list, max_items=20, description="Tags for categorization")
    include_patterns: Optional[list[str]] = Field(
        default=None,
        description="File path patterns to include (glob patterns)",
    )
    exclude_patterns: Optional[list[str]] = Field(
        default=None,
        description="File path patterns to exclude (glob patterns)",
    )
    github_token: Optional[str] = Field(default=None, description="GitHub token (if not using OAuth)")
    compliance_standards: Optional[list[str]] = Field(
        default=None,
        description="Compliance standards to check (PCI-DSS, HIPAA, SOC2, etc.)",
    )
    environment_name: Optional[str] = Field(
        default=None,
        description="Environment name (dev, stage, prod, etc.)",
    )


class IndexDocumentationRequest(BaseModel):
    """Request model for indexing a documentation website."""

    documentation_url: str = Field(..., description="Documentation website URL")
    name: Optional[str] = Field(default=None, description="Custom name for the resource")
    description: Optional[str] = Field(default=None, description="Resource description")
    tags: list[str] = Field(default_factory=list, max_items=20, description="Tags for categorization")
    include_patterns: Optional[list[str]] = Field(
        default=None,
        description="URL patterns to include",
    )
    exclude_patterns: Optional[list[str]] = Field(
        default=None,
        description="URL patterns to exclude",
    )
    max_pages: int = Field(
        default=100,
        ge=1,
        le=500,
        description="Maximum number of pages to crawl (1-500)",
    )
    max_depth: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum link depth to follow (1-10)",
    )
    incremental_update: bool = Field(
        default=True,
        description="Skip unchanged pages on re-index",
    )
    compliance_standards: Optional[list[str]] = Field(
        default=None,
        description="Compliance standards to check (PCI-DSS, HIPAA, SOC2, etc.)",
    )
    environment_name: Optional[str] = Field(
        default=None,
        description="Environment name (dev, stage, prod, etc.)",
    )


class IndexDocumentRequest(BaseModel):
    """Request model for indexing a document."""

    document_type: str = Field(..., description="Document type: pdf, docx, markdown, txt, xml, excel, csv")
    name: Optional[str] = Field(default=None, description="Custom name for the resource")
    description: Optional[str] = Field(default=None, description="Resource description")
    tags: list[str] = Field(default_factory=list, max_items=20, description="Tags for categorization")


class UpdateDocumentRequest(BaseModel):
    """Request model for updating document metadata."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Updated name")
    description: Optional[str] = Field(default=None, max_length=1000, description="Updated description")
    tags: Optional[list[str]] = Field(default=None, max_items=20, description="Updated tags")


class ReplaceDocumentContentRequest(BaseModel):
    """Request model for replacing document content."""

    document_url: Optional[str] = Field(default=None, description="New document URL")
    re_index: bool = Field(default=True, description="Whether to re-index after replacement")


class ReindexDocumentRequest(BaseModel):
    """Request model for re-indexing a document."""

    force: bool = Field(default=False, description="Force re-index even if content unchanged")
