"""Indexing models for user-provided resources."""

import secrets
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class ResourceType(str, Enum):
    """Type of indexed resource."""

    REPOSITORY = "repository"
    DOCUMENTATION = "documentation"
    DOCUMENT = "document"
    URL = "url"


class ResourceStatus(str, Enum):
    """Status of indexing resource."""

    PENDING = "pending"
    INDEXING = "indexing"
    COMPLETED = "completed"
    FAILED = "failed"
    DELETED = "deleted"
    CANCELLED = "cancelled"


class IndexedResource(BaseModel):
    """Model for tracking user-indexed resources."""

    resource_id: str = Field(
        ...,
        description="Unique resource identifier (e.g., 'res_abc123')",
        min_length=10,
        max_length=100,
    )
    user_id: str = Field(..., description="User ID who owns this resource")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID (if resource is shared within org)",
    )
    resource_type: ResourceType = Field(..., description="Type of resource")
    status: ResourceStatus = Field(
        default=ResourceStatus.PENDING,
        description="Current indexing status",
    )
    progress: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Indexing progress percentage (0-100)",
    )

    name: str = Field(..., description="Resource name", min_length=1, max_length=200)
    description: Optional[str] = Field(
        default=None,
        description="Resource description",
        max_length=1000,
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Tags for categorization",
        max_items=20,
    )

    repo_url: Optional[str] = Field(
        default=None,
        description="GitHub repository URL (for repository type)",
    )
    normalized_repo_url: Optional[str] = Field(
        default=None,
        description="Normalized repository URL for deduplication",
    )
    branch: Optional[str] = Field(
        default=None,
        description="GitHub branch name (default: main)",
    )
    last_commit_sha: Optional[str] = Field(
        default=None,
        description="Last commit SHA indexed (for change detection)",
    )
    documentation_url: Optional[str] = Field(
        default=None,
        description="Documentation website URL (for documentation type)",
    )
    include_patterns: Optional[list[str]] = Field(
        default=None,
        description="File path patterns to include (glob patterns for repositories, URL patterns for documentation)",
    )
    exclude_patterns: Optional[list[str]] = Field(
        default=None,
        description="File path patterns to exclude (glob patterns for repositories, URL patterns for documentation)",
    )
    max_pages: int = Field(
        default=100,
        ge=1,
        le=500,
        description="Maximum pages to crawl for documentation (1-500)",
    )
    max_depth: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum link depth to follow for documentation (1-10)",
    )
    incremental_update: bool = Field(
        default=True,
        description="Skip unchanged pages on re-index",
    )
    document_url: Optional[str] = Field(
        default=None,
        description="Document URL or file path (for document type)",
    )
    document_type: Optional[str] = Field(
        default=None,
        description="Document type (pdf, docx, markdown, xml, excel, csv, etc.)",
    )
    file_storage_id: Optional[str] = Field(
        default=None,
        description="GridFS file ID for stored original file",
    )
    file_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 hash of file content for change detection",
    )
    version: int = Field(
        default=1,
        ge=1,
        description="Document version number",
    )
    versions: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Version history metadata",
    )

    articles_indexed: int = Field(
        default=0,
        ge=0,
        description="Number of knowledge articles created from this resource",
    )
    files_processed: int = Field(
        default=0,
        ge=0,
        description="Number of files processed",
    )
    total_files: Optional[int] = Field(
        default=None,
        description="Total number of files to process (if known)",
    )
    storage_mb: float = Field(
        default=0.0,
        ge=0.0,
        description="Storage used by this resource in MB",
    )

    error_message: Optional[str] = Field(
        default=None,
        description="Error message if indexing failed",
    )
    error_details: Optional[dict[str, Any]] = Field(
        default=None,
        description="Detailed error information",
    )

    github_token_encrypted: Optional[str] = Field(
        default=None,
        description="Encrypted GitHub token (for private repos)",
    )
    compliance_standards: Optional[list[str]] = Field(
        default=None,
        description="Compliance standards to check (PCI-DSS, HIPAA, SOC2, etc.)",
    )
    environment_name: Optional[str] = Field(
        default=None,
        description="Environment name (dev, stage, prod, etc.)",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )
    indexed_at: Optional[datetime] = Field(
        default=None,
        description="Completion timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"resource_id"})
        data["_id"] = self.resource_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        
        if "versions" in data and isinstance(data["versions"], list):
            for version in data["versions"]:
                if isinstance(version, dict) and "indexed_at" in version:
                    if isinstance(version["indexed_at"], str):
                        try:
                            from datetime import datetime
                            version["indexed_at"] = datetime.fromisoformat(version["indexed_at"])
                        except (ValueError, TypeError):
                            pass
        
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IndexedResource":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            IndexedResource instance
        """
        if "_id" in data:
            data["resource_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        if "organization_id" in data and isinstance(data["organization_id"], ObjectId):
            data["organization_id"] = str(data["organization_id"])
        
        if "versions" in data and isinstance(data["versions"], list):
            for version in data["versions"]:
                if isinstance(version, dict) and "indexed_at" in version:
                    if isinstance(version["indexed_at"], datetime):
                        version["indexed_at"] = version["indexed_at"].isoformat()
        
        if "version" not in data:
            data["version"] = 1
        if "versions" not in data:
            data["versions"] = []
        if "file_storage_id" not in data:
            data["file_storage_id"] = None
        if "file_hash" not in data:
            data["file_hash"] = None
        
        return cls(**data)


class JobStatus(str, Enum):
    """Status of indexing job."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class IndexingJob(BaseModel):
    """Model for indexing job queue."""

    job_id: str = Field(
        ...,
        description="Unique job identifier (e.g., 'job_abc123')",
        min_length=10,
        max_length=100,
    )
    resource_id: str = Field(..., description="Resource ID being indexed")
    user_id: str = Field(..., description="User ID who owns this job")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID (if job is for org resource)",
    )
    status: JobStatus = Field(
        default=JobStatus.PENDING,
        description="Current job status",
    )
    priority: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Job priority (higher = more important, based on plan)",
    )
    job_type: str = Field(..., description="Type of job (repository, documentation, document)")
    plan: str = Field(default="professional", description="User's plan (affects priority)")

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Job creation timestamp",
    )
    started_at: Optional[datetime] = Field(
        default=None,
        description="Job start timestamp",
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Job completion timestamp",
    )

    retry_count: int = Field(
        default=0,
        ge=0,
        description="Number of retry attempts",
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        description="Maximum retry attempts",
    )

    progress: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Job progress percentage (0-100)",
    )

    error_message: Optional[str] = Field(
        default=None,
        description="Error message if job failed",
    )
    error_details: Optional[dict[str, Any]] = Field(
        default=None,
        description="Detailed error information",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"job_id"})
        data["_id"] = self.job_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IndexingJob":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            IndexingJob instance
        """
        if "_id" in data:
            data["job_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        if "organization_id" in data and isinstance(data["organization_id"], ObjectId):
            data["organization_id"] = str(data["organization_id"])
        return cls(**data)


def generate_resource_id() -> str:
    """Generate unique resource ID.

    Returns:
        Resource ID string (e.g., 'res_abc123def456')
    """
    return f"res_{secrets.token_hex(12)}"


def generate_job_id() -> str:
    """Generate unique job ID.

    Returns:
        Job ID string (e.g., 'job_abc123def456')
    """
    return f"job_{secrets.token_hex(12)}"


class ActivityType(str, Enum):
    """Type of indexing activity event."""

    # Lifecycle events
    INDEXING_STARTED = "indexing_started"
    INDEXING_COMPLETED = "indexing_completed"
    INDEXING_FAILED = "indexing_failed"
    INDEXING_PROGRESS = "indexing_progress"

    # Discovery events
    REPO_CLONED = "repo_cloned"
    FILES_DISCOVERED = "files_discovered"
    FILE_DISCOVERED = "file_discovered"

    # Processing events
    FILE_PROCESSING = "file_processing"
    FILE_PROCESSED = "file_processed"
    FILE_SKIPPED = "file_skipped"
    FILE_FAILED = "file_failed"

    # Article events
    ARTICLE_CREATED = "article_created"
    ARTICLES_BATCH_STORED = "articles_batch_stored"

    # Checkpoint events
    CHECKPOINT_SAVED = "checkpoint_saved"

    # Document events
    DOCUMENT_DOWNLOADED = "document_downloaded"
    DOCUMENT_PARSED = "document_parsed"
    DOCUMENT_PROCESSING = "document_processing"
    DOCUMENT_UNCHANGED = "document_unchanged"

    # Documentation events
    URL_CRAWLED = "url_crawled"
    PAGE_PROCESSED = "page_processed"
    PAGE_UNCHANGED = "page_unchanged"
    PAGE_CHANGED = "page_changed"
    CRAWL_STARTED = "crawl_started"
    SITEMAP_FOUND = "sitemap_found"

    # Analysis events
    ANALYSIS_STARTED = "analysis_started"
    ANALYSIS_COMPLETED = "analysis_completed"


class IndexingActivity(BaseModel):
    """Model for tracking indexing activity events."""

    activity_id: str = Field(
        default_factory=lambda: f"act_{secrets.token_hex(8)}",
        description="Unique activity identifier",
    )
    resource_id: str = Field(..., description="Resource ID this activity belongs to")
    activity_type: ActivityType = Field(..., description="Type of activity")
    message: str = Field(..., description="Human-readable activity message")

    # Optional details
    file_path: Optional[str] = Field(
        default=None,
        description="File path being processed (if applicable)",
    )
    details: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional activity details",
    )

    # Progress info
    progress: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Progress at time of activity",
    )
    files_processed: Optional[int] = Field(
        default=None,
        description="Files processed at time of activity",
    )
    total_files: Optional[int] = Field(
        default=None,
        description="Total files at time of activity",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Activity timestamp",
    )
    elapsed_seconds: Optional[float] = Field(
        default=None,
        description="Seconds since indexing started",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"activity_id"})
        data["_id"] = self.activity_id
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IndexingActivity":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            IndexingActivity instance
        """
        if "_id" in data:
            data["activity_id"] = str(data["_id"])
        return cls(**data)


def generate_activity_id() -> str:
    """Generate unique activity ID.

    Returns:
        Activity ID string (e.g., 'act_abc123de')
    """
    return f"act_{secrets.token_hex(8)}"

