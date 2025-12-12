"""Admin system models."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class SystemHealthResponse(BaseModel):
    """System health response."""

    status: str = Field(..., description="Overall system status")
    api: dict[str, Any] = Field(..., description="API service status")
    database: dict[str, Any] = Field(..., description="Database service status")
    redis: dict[str, Any] = Field(..., description="Redis/Memorystore service status")
    vector_search: dict[str, Any] = Field(..., description="Vector search service status")
    uptime_seconds: Optional[float] = Field(None, description="System uptime in seconds")


class RedisMetricsResponse(BaseModel):
    """Redis metrics response."""

    healthy: bool = Field(..., description="Whether Redis is healthy")
    circuit_state: str = Field(..., description="Circuit breaker state")
    failure_count: int = Field(..., description="Current failure count")
    success_count: int = Field(..., description="Current success count")
    last_failure_time: Optional[float] = Field(None, description="Timestamp of last failure")
    last_health_check: Optional[float] = Field(None, description="Timestamp of last health check")
    client_initialized: bool = Field(..., description="Whether Redis client is initialized")
    metrics: dict[str, Any] = Field(..., description="Operation metrics")
    configuration: dict[str, Any] = Field(..., description="Redis configuration")


class RateLimitConfig(BaseModel):
    """Rate limit configuration."""

    plan: str = Field(..., description="Plan name")
    requests_per_minute: int = Field(..., description="Requests per minute limit")


class RateLimitConfigResponse(BaseModel):
    """Rate limit configuration response."""

    plans: list[RateLimitConfig] = Field(..., description="Rate limit configurations by plan")


class RateLimitUpdateRequest(BaseModel):
    """Request model for updating rate limits."""

    user_id: Optional[str] = Field(None, description="User ID (for user-specific override)")
    organization_id: Optional[str] = Field(None, description="Organization ID (for org-specific override)")
    requests_per_minute: int = Field(..., ge=1, description="Requests per minute limit")


class SystemStatsResponse(BaseModel):
    """System statistics response."""

    total_users: int = Field(..., description="Total users")
    total_api_keys: int = Field(..., description="Total API keys")
    active_api_keys: int = Field(..., description="Active API keys")
    total_organizations: int = Field(..., description="Total organizations")
    total_indexed_resources: int = Field(..., description="Total indexed resources")
    total_storage_mb: float = Field(..., description="Total storage used in MB")
    database_size_mb: Optional[float] = Field(None, description="Database size in MB")
    collections_count: int = Field(..., description="Number of collections")

