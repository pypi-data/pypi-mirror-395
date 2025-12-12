"""Admin pipeline request/response models."""

from typing import Optional

from pydantic import BaseModel, Field


class PipelineConfigResponse(BaseModel):
    """Pipeline configuration response."""

    max_concurrent_pipelines: int = Field(default=3, description="Maximum concurrent pipelines")
    max_batch_size: int = Field(default=1000, description="Maximum batch size")
    rate_limit_per_hour: int = Field(default=10, description="Rate limit per hour")
    pipeline_timeout_hours: int = Field(default=24, description="Pipeline timeout in hours")


class PipelineConfigUpdateRequest(BaseModel):
    """Pipeline configuration update request."""

    max_concurrent_pipelines: Optional[int] = Field(
        None, ge=1, le=10, description="Maximum concurrent pipelines"
    )
    max_batch_size: Optional[int] = Field(None, ge=100, le=10000, description="Maximum batch size")
    rate_limit_per_hour: Optional[int] = Field(
        None, ge=1, le=100, description="Rate limit per hour"
    )
    pipeline_timeout_hours: Optional[int] = Field(
        None, ge=1, le=48, description="Pipeline timeout in hours"
    )


class PipelineMetricsResponse(BaseModel):
    """Pipeline metrics response."""

    total_pipelines: int = Field(..., description="Total number of pipelines")
    success_rate: Optional[float] = Field(None, description="Success rate (0.0 - 1.0)")
    average_duration_seconds: Optional[float] = Field(
        None, description="Average duration in seconds"
    )
    running_count: int = Field(default=0, description="Currently running pipelines")
    pipelines_by_type: dict[str, int] = Field(
        default_factory=dict, description="Pipeline count by type"
    )
    recent_pipelines: list[dict] = Field(
        default_factory=list, description="Recent pipeline executions"
    )

