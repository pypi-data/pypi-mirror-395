"""Intelligent context models for multi-resource context storage with automatic analysis."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class ContextType(str, Enum):
    """Type of context."""

    CONVERSATION = "conversation"
    ARCHITECTURE_DESIGN = "architecture_design"
    CODE_REVIEW = "code_review"
    TROUBLESHOOTING = "troubleshooting"
    DOCUMENTATION = "documentation"
    COMPLIANCE_AUDIT = "compliance_audit"
    COST_ANALYSIS = "cost_analysis"
    SECURITY_SCAN = "security_scan"
    INFRASTRUCTURE_CHANGE = "infrastructure_change"
    CUSTOM = "custom"


class ContextStatus(str, Enum):
    """Status of context."""

    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class InfrastructureResource(BaseModel):
    """Infrastructure resource reference in context."""

    resource_id: str = Field(..., description="Resource ID")
    resource_type: str = Field(..., description="Resource type (terraform, kubernetes, etc.)")
    path: str = Field(..., description="Virtual filesystem path")
    name: str = Field(..., description="Resource name")
    changes: Optional[list[dict[str, Any]]] = Field(
        default_factory=list,
        description="List of changes made to this resource",
    )


class ComplianceContext(BaseModel):
    """Compliance-related context."""

    standards: list[str] = Field(
        default_factory=list,
        description="Compliance standards (PCI-DSS, HIPAA, SOC2, etc.)",
    )
    controls: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Compliance controls referenced",
    )
    status: dict[str, str] = Field(
        default_factory=dict,
        description="Compliance status by standard",
    )
    violations: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Compliance violations found",
    )


class CostContext(BaseModel):
    """Cost-related context."""

    estimated_monthly: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Estimated monthly cost in USD",
    )
    estimated_annual: Optional[float] = Field(
        default=None,
        ge=0.0,
        description="Estimated annual cost in USD",
    )
    breakdown: dict[str, Any] = Field(
        default_factory=dict,
        description="Cost breakdown by service/provider",
    )
    changes: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Cost changes (e.g., +$200/month)",
    )


class SecurityContext(BaseModel):
    """Security-related context."""

    issues: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Security issues found",
    )
    vulnerabilities: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Vulnerabilities identified",
    )
    recommendations: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Security recommendations",
    )
    score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Security score (0-100)",
    )


class ContextAnalysis(BaseModel):
    """Automatic analysis results for context."""

    compliance: Optional[ComplianceContext] = Field(
        default=None,
        description="Compliance analysis",
    )
    costs: Optional[CostContext] = Field(
        default=None,
        description="Cost analysis",
    )
    security: Optional[SecurityContext] = Field(
        default=None,
        description="Security analysis",
    )
    infrastructure: Optional[dict[str, Any]] = Field(
        default=None,
        description="Infrastructure analysis",
    )
    analyzed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Analysis timestamp",
    )
    analysis_version: str = Field(
        default="1.0",
        description="Analysis version",
    )


class IntelligentContext(BaseModel):
    """Infrastructure-aware context storage with automatic analysis."""

    context_id: str = Field(
        ...,
        description="Unique context identifier (e.g., 'ctx_abc123')",
        min_length=10,
        max_length=100,
    )
    user_id: str = Field(..., description="User ID who owns this context")
    organization_id: Optional[str] = Field(
        default=None,
        description="Organization ID (if context is shared within org)",
    )

    context_type: ContextType = Field(..., description="Type of context")
    status: ContextStatus = Field(
        default=ContextStatus.ACTIVE,
        description="Context status",
    )

    title: str = Field(..., description="Context title", min_length=1, max_length=500)
    summary: str = Field(
        ...,
        description="Context summary",
        min_length=1,
        max_length=5000,
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed description",
        max_length=50000,
    )

    conversation_history: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Conversation history",
    )
    code_snippets: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Code snippets referenced",
    )
    plans: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Plans or workflows",
    )
    decisions: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Decisions made",
    )

    infrastructure_resources: list[InfrastructureResource] = Field(
        default_factory=list,
        description="Infrastructure resources referenced",
    )

    linked_resources: list[str] = Field(
        default_factory=list,
        description="Linked resource IDs",
    )
    linked_contexts: list[str] = Field(
        default_factory=list,
        description="Linked context IDs",
    )

    analysis: Optional[ContextAnalysis] = Field(
        default=None,
        description="Automatic analysis results",
    )

    tags: list[str] = Field(
        default_factory=list,
        description="Tags for categorization",
        max_items=20,
    )
    workspace: Optional[str] = Field(
        default=None,
        description="Workspace identifier",
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )
    accessed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last access timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"context_id"})
        data["_id"] = self.context_id
        data["user_id"] = ObjectId(self.user_id) if self.user_id else None
        data["organization_id"] = ObjectId(self.organization_id) if self.organization_id else None
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IntelligentContext":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            IntelligentContext instance
        """
        if "_id" in data:
            data["context_id"] = str(data["_id"])
        if "user_id" in data and isinstance(data["user_id"], ObjectId):
            data["user_id"] = str(data["user_id"])
        if "organization_id" in data and isinstance(data["organization_id"], ObjectId):
            data["organization_id"] = str(data["organization_id"])
        return cls(**data)


class ContextLink(BaseModel):
    """Link between contexts with semantic relationship."""

    link_id: str = Field(
        ...,
        description="Unique link identifier",
        min_length=10,
        max_length=100,
    )
    source_context_id: str = Field(..., description="Source context ID")
    target_context_id: str = Field(..., description="Target context ID")
    relationship_type: str = Field(
        ...,
        description="Relationship type (depends_on, related_to, supersedes, etc.)",
    )
    strength: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Relationship strength (0.0-1.0)",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp",
    )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for MongoDB storage.

        Returns:
            Dictionary representation
        """
        data = self.model_dump(exclude={"link_id"})
        data["_id"] = self.link_id
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextLink":
        """Create from MongoDB document.

        Args:
            data: MongoDB document

        Returns:
            ContextLink instance
        """
        if "_id" in data:
            data["link_id"] = str(data["_id"])
        return cls(**data)


class ContextSaveRequest(BaseModel):
    """Request model for saving context with analysis."""

    model_config = {"extra": "ignore"}

    context_type: str = Field(..., description="Type of context")
    title: str = Field(..., description="Context title", min_length=1, max_length=500)
    summary: str = Field(..., description="Context summary", min_length=1, max_length=5000)
    description: Optional[str] = Field(default=None, description="Detailed description", max_length=50000)
    conversation_history: Optional[list[dict[str, Any]]] = Field(default=None, description="Conversation history")
    code_snippets: Optional[list[dict[str, Any]]] = Field(default=None, description="Code snippets referenced")
    plans: Optional[list[dict[str, Any]]] = Field(default=None, description="Plans or workflows")
    decisions: Optional[list[dict[str, Any]]] = Field(default=None, description="Decisions made")
    infrastructure_resources: Optional[list[dict[str, Any]]] = Field(
        default=None, description="Infrastructure resources referenced"
    )
    linked_resources: Optional[list[str]] = Field(default=None, description="Linked resource IDs")
    tags: Optional[list[str]] = Field(default=None, description="Tags for categorization", max_items=20)
    workspace: Optional[str] = Field(default=None, description="Workspace identifier")
    auto_analyze: bool = Field(default=True, description="Automatically analyze infrastructure, compliance, costs, security")

