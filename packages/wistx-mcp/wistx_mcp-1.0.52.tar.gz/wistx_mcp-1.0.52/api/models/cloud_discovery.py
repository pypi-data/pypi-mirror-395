"""Cloud Discovery API Models.

Pydantic models for cloud resource discovery API endpoints.
These are the API-layer models - the core models are in wistx_mcp/models/cloud_discovery.py
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CloudProviderEnum(str, Enum):
    """Supported cloud providers."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class DiscoveryStatusEnum(str, Enum):
    """Discovery status states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class CredentialStatusEnum(str, Enum):
    """Credential validation status."""
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"


# Request Models
class GenerateExternalIdRequest(BaseModel):
    """Request to generate a new External ID."""
    provider: CloudProviderEnum = CloudProviderEnum.AWS


class ValidateConnectionRequest(BaseModel):
    """Request to validate AWS connection."""
    provider: CloudProviderEnum = CloudProviderEnum.AWS
    role_arn: str = Field(..., description="AWS IAM Role ARN", pattern=r"^arn:aws:iam::\d{12}:role/.+$")
    external_id: str = Field(..., description="External ID for role assumption")


class StartDiscoveryRequest(BaseModel):
    """Request to start resource discovery."""
    provider: CloudProviderEnum = CloudProviderEnum.AWS
    role_arn: str | None = Field(default=None, description="AWS IAM Role ARN (optional if saved connection exists)")
    external_id: str | None = Field(default=None, description="External ID for role assumption (optional if saved connection exists)")
    regions: list[str] | None = Field(default=None, description="Specific regions to scan (default: all)")
    resource_types: list[str] | None = Field(default=None, description="Specific resource types to discover")
    tags_filter: dict[str, str] | None = Field(default=None, description="Filter resources by tags")


# Response Models
class ExternalIdResponse(BaseModel):
    """Response with generated External ID."""
    external_id: str
    created_at: datetime
    expires_at: datetime | None = None


class ConnectionSetupResponse(BaseModel):
    """Response with AWS connection setup instructions."""
    trust_policy: str
    permission_policy: str
    setup_instructions: list[str]
    wistx_account_id: str
    external_id_placeholder: str = "EXTERNAL_ID_PLACEHOLDER"


class ConnectionValidationResponse(BaseModel):
    """Response from connection validation."""
    is_valid: bool
    error_message: str | None = None
    permissions_missing: list[str] | None = None
    regions_accessible: list[str] = Field(default_factory=list)
    account_id: str | None = None
    account_alias: str | None = None


class DiscoveryMetricsResponse(BaseModel):
    """Discovery metrics summary."""
    total_resources: int
    resources_by_type: dict[str, int]
    resources_by_region: dict[str, int]
    resources_by_phase: dict[str, int]
    discovery_duration_seconds: float
    api_calls_made: int


class DiscoveryErrorResponse(BaseModel):
    """Discovery error details."""
    resource_type: str
    error_code: str
    error_message: str
    region: str | None = None
    timestamp: datetime


class DiscoveryListItem(BaseModel):
    """Summary of a discovery for list view."""
    discovery_id: str
    status: DiscoveryStatusEnum
    provider: CloudProviderEnum
    total_resources: int
    started_at: datetime
    completed_at: datetime | None = None
    errors_count: int = 0


class DiscoveryListResponse(BaseModel):
    """Response with list of discoveries."""
    discoveries: list[DiscoveryListItem]
    total: int
    page: int = 1
    per_page: int = 20


class TerraformMappingResponse(BaseModel):
    """Response with Terraform mappings for a provider."""
    provider: CloudProviderEnum
    total_mappings: int
    mappings: dict[str, Any]


# Database Models (for MongoDB storage)
class CloudConnectionDocument(BaseModel):
    """MongoDB document for storing cloud connections.

    Persists AWS connection credentials for reuse across sessions.
    """
    user_id: str
    provider: CloudProviderEnum
    role_arn: str
    external_id: str
    status: CredentialStatusEnum = CredentialStatusEnum.PENDING
    last_validated: datetime | None = None
    account_id: str | None = None
    account_alias: str | None = None
    regions_accessible: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class DiscoveryMetadataDocument(BaseModel):
    """MongoDB document for storing discovery metadata ONLY.

    IMPORTANT: We do NOT persist full resource data because:
    1. Cloud infrastructure changes constantly - stored data becomes stale quickly
    2. Full resource configs may contain sensitive data (IPs, security groups)
    3. The AI coding agent in the user's IDE has the full data locally
    4. Reduces database storage and improves query performance

    We only store:
    - Discovery metadata (id, status, timestamps)
    - Summary metrics (counts, duration)
    - Error information for debugging
    """
    discovery_id: str
    user_id: str
    provider: CloudProviderEnum
    status: DiscoveryStatusEnum = DiscoveryStatusEnum.PENDING

    # Request configuration (for audit/replay)
    regions_scanned: list[str] = Field(default_factory=list)
    resource_types_requested: list[str] | None = None
    tags_filter: dict[str, str] | None = None

    # Summary metrics only - NOT full resource data
    total_resources: int = 0
    resource_type_counts: dict[str, int] = Field(default_factory=dict)
    region_counts: dict[str, int] = Field(default_factory=dict)
    phase_counts: dict[str, int] = Field(default_factory=dict)
    total_dependencies: int = 0
    has_circular_dependencies: bool = False

    # Timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
    duration_seconds: float | None = None

    # Errors (for debugging, not full resource data)
    errors_count: int = 0
    error_summaries: list[str] = Field(default_factory=list)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Legacy model - kept for backward compatibility during migration
class DiscoveryDocument(BaseModel):
    """DEPRECATED: Use DiscoveryMetadataDocument instead.

    This model stored full resource data which is no longer recommended.
    Kept for backward compatibility with existing data.
    """
    discovery_id: str
    user_id: str
    provider: CloudProviderEnum
    role_arn: str
    status: DiscoveryStatusEnum = DiscoveryStatusEnum.PENDING
    request_config: dict[str, Any] = Field(default_factory=dict)
    resources: list[dict[str, Any]] = Field(default_factory=list)  # DEPRECATED
    dependency_graph: dict[str, Any] | None = None  # DEPRECATED
    metrics: dict[str, Any] | None = None
    errors: list[dict[str, Any]] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

