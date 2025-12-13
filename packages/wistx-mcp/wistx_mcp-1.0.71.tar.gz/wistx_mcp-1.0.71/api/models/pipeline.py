"""Pipeline job models for data pipeline management."""

import secrets
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class PipelineStatus(str, Enum):
    """Status of pipeline execution."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PipelineType(str, Enum):
    """Type of data pipeline."""

    COMPLIANCE = "compliance"
    COST_DATA = "cost_data"
    CODE_EXAMPLES = "code_examples"
    KNOWLEDGE = "knowledge"


class StageStatus(str, Enum):
    """Status of pipeline stage."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class StageProgress(BaseModel):
    """Progress information for a pipeline stage."""

    stage_name: str = Field(..., description="Stage name")
    status: StageStatus = Field(default=StageStatus.PENDING, description="Stage status")
    items_processed: int = Field(default=0, description="Items processed")
    items_succeeded: int = Field(default=0, description="Items succeeded")
    items_failed: int = Field(default=0, description="Items failed")
    duration_seconds: Optional[float] = Field(default=None, description="Duration in seconds")
    progress_percentage: float = Field(default=0.0, ge=0.0, le=1.0, description="Progress percentage")
    started_at: Optional[datetime] = Field(default=None, description="Stage start time")
    completed_at: Optional[datetime] = Field(default=None, description="Stage completion time")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class PipelineStats(BaseModel):
    """Statistics for pipeline execution."""

    collected: int = Field(default=0, description="Items collected")
    processed: int = Field(default=0, description="Items processed")
    embedded: int = Field(default=0, description="Items embedded")
    loaded: int = Field(default=0, description="Items loaded")
    errors: list[dict[str, Any]] = Field(default_factory=list, description="List of errors")
    skipped_source_unchanged: int = Field(default=0, description="Items skipped (source unchanged)")
    skipped_content_unchanged: int = Field(default=0, description="Items skipped (content unchanged)")
    llm_calls_saved: int = Field(default=0, description="LLM calls saved via change detection")
    embedding_calls_saved: int = Field(default=0, description="Embedding calls saved")
    context_generated: int = Field(default=0, description="Context generated (cost_data pipeline)")
    loaded_mongodb: int = Field(default=0, description="Items loaded to MongoDB (cost_data pipeline)")
    loaded_pinecone: int = Field(default=0, description="Items loaded to Pinecone (cost_data pipeline)")
    allocated: int = Field(default=0, description="Items allocated (cost_data pipeline)")


class PipelineJob(BaseModel):
    """Model for pipeline execution job."""

    pipeline_id: str = Field(
        ...,
        description="Unique pipeline identifier (e.g., 'pipe_abc123')",
        min_length=10,
        max_length=100,
    )
    pipeline_type: PipelineType = Field(..., description="Type of pipeline")
    user_id: str = Field(..., description="User ID who triggered this pipeline")
    status: PipelineStatus = Field(
        default=PipelineStatus.PENDING,
        description="Current pipeline status",
    )
    priority: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Pipeline priority (higher = more important)",
    )

    request: dict[str, Any] = Field(..., description="Pipeline request parameters")
    correlation_id: str = Field(..., description="Correlation ID for tracing")

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Pipeline creation timestamp",
    )
    started_at: Optional[datetime] = Field(
        default=None,
        description="Pipeline start timestamp",
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Pipeline completion timestamp",
    )

    progress: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Overall progress (0.0 - 1.0)",
    )
    current_stage: Optional[str] = Field(
        default=None,
        description="Current stage name",
    )
    stages: dict[str, StageProgress] = Field(
        default_factory=dict,
        description="Stage progress information",
    )
    stats: PipelineStats = Field(
        default_factory=PipelineStats,
        description="Pipeline statistics",
    )

    error: Optional[str] = Field(
        default=None,
        description="Error message if pipeline failed",
    )
    error_details: Optional[dict[str, Any]] = Field(
        default=None,
        description="Detailed error information",
    )

    resource_acquired: bool = Field(
        default=False,
        description="Whether resource was acquired for execution",
    )
    max_retries: int = Field(
        default=0,
        ge=0,
        description="Maximum retry attempts",
    )
    retry_count: int = Field(
        default=0,
        ge=0,
        description="Current retry count",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"pipeline_id"})
        data["_id"] = self.pipeline_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value
            elif isinstance(value, dict) and "_id" in value:
                pass
        
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PipelineJob":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            PipelineJob instance
        """
        if "_id" in data:
            data["pipeline_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        
        if "stages" in data and isinstance(data["stages"], dict):
            for stage_name, stage_data in data["stages"].items():
                if isinstance(stage_data, dict):
                    stage_data_copy = stage_data.copy()
                    if "progress_percentage" in stage_data_copy:
                        progress = stage_data_copy["progress_percentage"]
                        if isinstance(progress, (int, float)) and progress > 1.0:
                            stage_data_copy["progress_percentage"] = progress / 100.0
                    data["stages"][stage_name] = StageProgress(**stage_data_copy)
        
        if "stats" in data and isinstance(data["stats"], dict):
            data["stats"] = PipelineStats(**data["stats"])
        
        return cls(**data)


def generate_pipeline_id() -> str:
    """Generate unique pipeline ID.

    Returns:
        Unique pipeline identifier
    """
    random_part = secrets.token_urlsafe(16)
    return f"pipe_{random_part}"

