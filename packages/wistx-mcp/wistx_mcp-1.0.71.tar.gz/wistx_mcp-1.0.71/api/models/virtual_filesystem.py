"""Virtual filesystem models for infrastructure-aware file navigation."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class FilesystemEntryType(str, Enum):
    """Type of filesystem entry."""

    FILE = "file"
    DIRECTORY = "directory"
    INFRASTRUCTURE_GROUP = "infrastructure_group"
    TERRAFORM_MODULE = "terraform_module"
    KUBERNETES_NAMESPACE = "kubernetes_namespace"
    COMPLIANCE_CONTROL = "compliance_control"
    COST_COMPONENT = "cost_component"
    SECURITY_ISSUE = "security_issue"


class InfrastructureMetadata(BaseModel):
    """Infrastructure-specific metadata for filesystem entries."""

    resource_type: Optional[str] = Field(
        default=None,
        description="Infrastructure resource type (aws_rds_instance, kubernetes_deployment, etc.)",
    )
    cloud_provider: Optional[str] = Field(
        default=None,
        description="Cloud provider (aws, gcp, azure)",
    )
    service: Optional[str] = Field(
        default=None,
        description="Service name (rds, ec2, s3, eks, gke, etc.)",
    )
    environment: Optional[str] = Field(
        default=None,
        description="Environment name (dev, stage, prod)",
    )
    region: Optional[str] = Field(
        default=None,
        description="Cloud region (us-east-1, us-central1, etc.)",
    )
    compliance_standards: Optional[list[str]] = Field(
        default_factory=list,
        description="Compliance standards (PCI-DSS, HIPAA, SOC2, etc.)",
    )
    estimated_monthly_cost_usd: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Estimated monthly cost in USD",
    )
    security_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Security score (0-100)",
    )
    dependencies: Optional[list[str]] = Field(
        default_factory=list,
        description="List of dependent file paths or resource IDs",
    )
    dependents: Optional[list[str]] = Field(
        default_factory=list,
        description="List of files or resources that depend on this entry",
    )


class VirtualFilesystemEntry(BaseModel):
    """Model for virtual filesystem entries."""

    entry_id: str = Field(
        ...,
        description="Unique entry identifier (e.g., 'fs_abc123')",
        min_length=10,
        max_length=100,
    )
    resource_id: str = Field(
        ...,
        description="Resource ID this entry belongs to",
    )
    user_id: str = Field(..., description="User ID who owns this entry")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID (if entry is shared within org)",
    )

    entry_type: FilesystemEntryType = Field(
        ...,
        description="Type of filesystem entry",
    )
    path: str = Field(
        ...,
        description="Virtual filesystem path (e.g., '/infrastructure/terraform/modules/vpc/main.tf')",
    )
    name: str = Field(..., description="Entry name (file or directory name)")

    parent_path: Optional[str] = Field(
        default=None,
        description="Parent directory path",
    )

    original_file_path: Optional[str] = Field(
        default=None,
        description="Original file path in repository (for files)",
    )
    article_id: Optional[str] = Field(
        default=None,
        description="Knowledge article ID (if entry is linked to article)",
    )
    indexed_file_id: Optional[str] = Field(
        default=None,
        description="Indexed file ID (if entry is linked to indexed file)",
    )

    infrastructure_metadata: Optional[InfrastructureMetadata] = Field(
        default=None,
        description="Infrastructure-specific metadata",
    )

    file_size_bytes: Optional[int] = Field(
        default=None,
        ge=0,
        description="File size in bytes (for files)",
    )
    line_count: Optional[int] = Field(
        default=None,
        ge=0,
        description="Number of lines (for files)",
    )
    language: Optional[str] = Field(
        default=None,
        description="Programming language (python, terraform, yaml, etc.)",
    )
    code_type: Optional[str] = Field(
        default=None,
        description="Code type (terraform, kubernetes, docker, etc.)",
    )

    children_count: int = Field(
        default=0,
        ge=0,
        description="Number of child entries (for directories)",
    )
    children: Optional[list[str]] = Field(
        default_factory=list,
        description="List of child entry IDs (for directories)",
    )

    tags: list[str] = Field(
        default_factory=list,
        description="Tags for categorization",
        max_items=20,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"entry_id"})
        data["_id"] = self.entry_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VirtualFilesystemEntry":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            VirtualFilesystemEntry instance
        """
        if "_id" in data:
            data["entry_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        if "organization_id" in data and isinstance(data["organization_id"], ObjectId):
            data["organization_id"] = str(data["organization_id"])
        return cls(**data)

