"""Response models for indexing endpoints."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from api.models.indexing import ResourceStatus, ResourceType


class SectionSummary(BaseModel):
    """Section summary for resource responses."""

    section_id: str = Field(..., description="Section ID")
    title: str = Field(..., description="Section title")
    summary: str = Field(..., description="Section summary")
    section_type: str = Field(..., description="Section type")
    component_count: int = Field(..., ge=0, description="Number of components in section")


class IndexResourceResponse(BaseModel):
    """Response model for indexing operations."""

    resource_id: str = Field(..., description="Resource ID")
    status: ResourceStatus = Field(..., description="Current status")
    progress: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")
    message: str = Field(..., description="Status message")


class ResourceDetailResponse(BaseModel):
    """Response model for resource details."""

    resource_id: str = Field(..., description="Resource ID")
    user_id: str = Field(..., description="User ID")
    organization_id: Optional[str] = Field(default=None, description="Organization ID")
    resource_type: ResourceType = Field(..., description="Resource type")
    status: ResourceStatus = Field(..., description="Current status")
    progress: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")

    name: str = Field(..., description="Resource name")
    description: Optional[str] = Field(default=None, description="Resource description")
    tags: list[str] = Field(default_factory=list, description="Tags")

    repo_url: Optional[str] = Field(default=None, description="Repository URL")
    branch: Optional[str] = Field(default=None, description="Branch name")
    documentation_url: Optional[str] = Field(default=None, description="Documentation URL")
    document_url: Optional[str] = Field(default=None, description="Document URL")

    articles_indexed: int = Field(default=0, ge=0, description="Number of articles indexed")
    files_processed: int = Field(default=0, ge=0, description="Number of files processed")
    total_files: Optional[int] = Field(default=None, description="Total files")
    storage_mb: float = Field(default=0.0, ge=0.0, description="Storage used in MB")

    error_message: Optional[str] = Field(default=None, description="Error message if failed")
    error_details: Optional[dict[str, Any]] = Field(default=None, description="Error details")

    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    indexed_at: Optional[datetime] = Field(default=None, description="Indexing completion timestamp")
    deletion_hint: Optional[str] = Field(default=None, description="Hint for deleting this resource")

    sections: Optional[list[SectionSummary]] = Field(
        default=None,
        description="Documentation sections (if available)",
    )
    section_count: Optional[int] = Field(
        default=None,
        ge=0,
        description="Total number of sections",
    )


class ResourceListResponse(BaseModel):
    """Response model for resource list."""

    resources: list[ResourceDetailResponse] = Field(..., description="List of resources")
    total: int = Field(..., ge=0, description="Total number of resources")
    summary: Optional[dict[str, Any]] = Field(default=None, description="Summary statistics and deletion info")
    ai_analysis: Optional[dict[str, Any]] = Field(default=None, description="AI-analyzed insights")


class ActivityResponse(BaseModel):
    """Response model for a single indexing activity."""

    activity_id: str = Field(..., description="Unique activity ID")
    activity_type: str = Field(..., description="Type of activity (e.g., file_processed, repo_cloned)")
    message: str = Field(..., description="Human-readable activity message")
    file_path: Optional[str] = Field(default=None, description="File path if applicable")
    details: Optional[dict[str, Any]] = Field(default=None, description="Additional activity details")
    progress: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Progress at time of activity")
    files_processed: Optional[int] = Field(default=None, ge=0, description="Files processed at time of activity")
    total_files: Optional[int] = Field(default=None, ge=0, description="Total files to process")
    elapsed_seconds: Optional[float] = Field(default=None, ge=0.0, description="Seconds elapsed since indexing started")
    created_at: datetime = Field(..., description="Activity timestamp")


class ActivitiesListResponse(BaseModel):
    """Response model for list of indexing activities."""

    resource_id: str = Field(..., description="Resource ID")
    activities: list[ActivityResponse] = Field(..., description="List of activities")
    total: int = Field(..., ge=0, description="Total number of activities")
    has_more: bool = Field(default=False, description="Whether there are more activities to fetch")
