"""Compliance control data models."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class CodeSnippet(BaseModel):
    """Code snippet for remediation.

    Flexible structure that supports any cloud provider, service, and infrastructure type.
    """

    cloud_provider: Optional[str] = Field(
        default=None,
        description="Cloud provider (aws, gcp, azure, or null for generic)",
    )
    service: Optional[str] = Field(
        default=None,
        description="Cloud service (rds, s3, ec2, cloudsql, etc.)",
    )
    infrastructure_type: str = Field(
        default="terraform",
        description="Infrastructure type (terraform, kubernetes, docker, cloudformation, etc.)",
    )
    code: str = Field(..., description="Code snippet")
    language: Optional[str] = Field(
        default=None, description="Language if applicable (hcl, yaml, json, etc.)"
    )
    description: Optional[str] = Field(
        default=None, description="Brief description of what this snippet does"
    )
    resource_type: Optional[str] = Field(
        default=None,
        description="Specific resource type (e.g., aws_db_instance, google_sql_database_instance)",
    )

    def get_key(self) -> str:
        """Generate a unique key for this snippet.

        Returns:
            Key string (e.g., "aws:rds:terraform" or "kubernetes:generic")
        """
        parts = []
        if self.cloud_provider:
            parts.append(self.cloud_provider)
        if self.service:
            parts.append(self.service)
        parts.append(self.infrastructure_type)
        return ":".join(parts)


class Remediation(BaseModel):
    """Remediation steps for a compliance control."""

    summary: str = Field(..., description="Summary of remediation steps")
    steps: list[str] = Field(default_factory=list, description="Detailed remediation steps")
    code_snippets: list[CodeSnippet] = Field(
        default_factory=list,
        description="Code snippets for remediation (supports terraform, cloudformation, pulumi, kubernetes, docker, etc.)",
    )

    def get_code_snippet(
        self,
        cloud_provider: Optional[str] = None,
        service: Optional[str] = None,
        infrastructure_type: str = "terraform",
    ) -> Optional[str]:
        """Get code snippet matching criteria.

        Args:
            cloud_provider: Cloud provider (aws, gcp, azure)
            service: Service name (rds, s3, etc.)
            infrastructure_type: Infrastructure type (terraform, kubernetes, etc.)

        Returns:
            Code snippet string or None if not found
        """
        for snippet in self.code_snippets:
            if snippet.infrastructure_type != infrastructure_type:
                continue
            if cloud_provider and snippet.cloud_provider != cloud_provider:
                continue
            if service and snippet.service != service:
                continue
            return snippet.code

        return None

    def get_all_for_cloud(self, cloud_provider: str) -> list[CodeSnippet]:
        """Get all code snippets for a specific cloud provider.

        Args:
            cloud_provider: Cloud provider (aws, gcp, azure)

        Returns:
            List of matching code snippets
        """
        return [
            snippet
            for snippet in self.code_snippets
            if snippet.cloud_provider == cloud_provider
        ]

    def get_all_by_infrastructure_type(self, infrastructure_type: str) -> list[CodeSnippet]:
        """Get all code snippets for a specific infrastructure type.

        Args:
            infrastructure_type: Infrastructure type (terraform, cloudformation, pulumi, kubernetes, docker, etc.)

        Returns:
            List of matching code snippets
        """
        return [
            snippet
            for snippet in self.code_snippets
            if snippet.infrastructure_type == infrastructure_type
        ]

    def get_by_service(self, service: str, cloud_provider: Optional[str] = None) -> list[CodeSnippet]:
        """Get all code snippets for a specific service.

        Args:
            service: Service name (rds, s3, ec2, etc.)
            cloud_provider: Optional cloud provider filter

        Returns:
            List of matching code snippets
        """
        return [
            snippet
            for snippet in self.code_snippets
            if snippet.service == service
            and (cloud_provider is None or snippet.cloud_provider == cloud_provider)
        ]


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


class DataQuality(BaseModel):
    """Data quality metrics."""

    completeness: float = Field(..., ge=0.0, le=1.0, description="Completeness score (0-1)")
    accuracy: float = Field(..., ge=0.0, le=1.0, description="Accuracy score (0-1)")
    last_verified: datetime = Field(..., description="Last verification timestamp")


class ComplianceControl(BaseModel):
    """Standardized compliance control."""

    control_id: str = Field(..., description="Unique control identifier")
    standard: str = Field(..., description="Compliance standard (e.g., PCI-DSS, CIS, HIPAA)")
    version: str = Field(..., description="Standard version")
    title: str = Field(..., description="Control title")
    description: str = Field(..., description="Control description")
    requirement: Optional[str] = Field(
        default=None, description="Detailed requirement text"
    )
    testing_procedures: list[str] = Field(
        default_factory=list, description="Testing procedures"
    )
    severity: str = Field(..., description="Severity level (HIGH, MEDIUM, LOW, CRITICAL)")
    category: Optional[str] = Field(
        default=None, description="Category (encryption, access, network, etc.)"
    )
    subcategory: Optional[str] = Field(
        default=None, description="Subcategory (data-at-rest, data-in-transit, etc.)"
    )
    applies_to: list[str] = Field(
        default_factory=list,
        description="List of cloud resources this applies to (e.g., AWS::RDS::DBInstance, GCP::SQL::Instance)",
    )
    remediation: Remediation = Field(..., description="Remediation information")
    verification: Optional[dict[str, Any]] = Field(
        default=None,
        description="Verification methods, tools, and queries",
    )
    references: list[Reference] = Field(
        default_factory=list, description="External references"
    )
    source_url: str = Field(..., description="Source URL for this control")
    embedding: Optional[list[float]] = Field(
        default=None, description="Vector embedding (1536 dimensions, added in Stage 3)"
    )
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, description="Last update timestamp"
    )
    version_history: list[VersionHistory] = Field(
        default_factory=list, description="Version history"
    )
    source: Optional[str] = Field(
        default=None, description="Source organization (e.g., PCI Security Standards Council)"
    )
    data_quality: Optional[DataQuality] = Field(
        default=None, description="Data quality metrics"
    )
    source_hash: Optional[str] = Field(
        default=None, description="SHA-256 hash of raw source data (for change detection)"
    )
    content_hash: Optional[str] = Field(
        default=None, description="SHA-256 hash of processed content (for change detection)"
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
    user_id: Optional[str] = Field(
        default=None,
        description="User ID for custom controls (null = public/WISTX control)",
    )
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID for org-specific controls",
    )
    visibility: str = Field(
        default="global",
        description="Visibility scope: global, organization, or user",
    )
    is_custom: bool = Field(
        default=False,
        description="True if this is a custom/enterprise control (not WISTX-provided)",
    )
    source_document_id: Optional[str] = Field(
        default=None,
        description="ID of uploaded document this control was extracted from",
    )
    source_document_name: Optional[str] = Field(
        default=None,
        description="Name of uploaded document",
    )
    extraction_method: Optional[str] = Field(
        default=None,
        description="Extraction method: llm, manual, structured",
    )
    extraction_confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score of extraction (0.0-1.0)",
    )
    reviewed: bool = Field(
        default=False,
        description="Whether control has been reviewed/approved by user",
    )
    reviewed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when control was reviewed",
    )
    reviewed_by: Optional[str] = Field(
        default=None,
        description="User ID who reviewed the control",
    )

    def to_searchable_text(self) -> str:
        """Convert control to searchable text for embedding.
        
        Includes contextual description if available (for contextual retrieval).
        
        Returns:
            Searchable text string with contextual description prepended
        """
        text_parts = []
        
        if self.contextual_description:
            text_parts.append(self.contextual_description)
            text_parts.append("")
        
        text_parts.append(f"{self.standard} {self.control_id}: {self.title}\n")
        text_parts.append(f"{self.description}\n")
        if self.requirement:
            text_parts.append(f"{self.requirement}\n")
        if isinstance(self.remediation, Remediation):
            text_parts.append(f"{self.remediation.summary}")
        
        return "\n".join(text_parts)

    def get_cloud_providers(self) -> list[str]:
        """Extract cloud providers from applies_to field.

        Returns:
            List of cloud provider names (aws, gcp, azure)
        """
        providers = set()
        for resource in self.applies_to:
            if resource.startswith("AWS::"):
                providers.add("aws")
            elif resource.startswith("GCP::"):
                providers.add("gcp")
            elif resource.startswith("Azure::"):
                providers.add("azure")
        return sorted(providers)

