"""Incident and solution models for troubleshooting."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class IncidentStatus(str, Enum):
    """Incident status."""

    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentSeverity(str, Enum):
    """Incident severity."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Incident(BaseModel):
    """Troubleshooting incident record."""

    incident_id: str = Field(..., description="Unique incident identifier")

    issue_description: str = Field(..., description="Issue description")
    infrastructure_type: Optional[str] = Field(default=None, description="Infrastructure type")
    cloud_provider: Optional[str] = Field(default=None, description="Cloud provider")
    resource_type: Optional[str] = Field(default=None, description="Resource type")

    error_messages: list[str] = Field(default_factory=list, description="Error messages")
    error_patterns: list[str] = Field(default_factory=list, description="Error patterns")
    logs: Optional[str] = Field(default=None, description="Log output")
    configuration_code: Optional[str] = Field(default=None, description="Configuration code")

    root_cause: Optional[str] = Field(default=None, description="Root cause")
    confidence: str = Field(default="medium", description="Confidence level")
    identified_issues: list[str] = Field(default_factory=list, description="Identified issues")

    status: IncidentStatus = Field(default=IncidentStatus.OPEN, description="Incident status")
    severity: IncidentSeverity = Field(default=IncidentSeverity.MEDIUM, description="Severity")

    solution_applied: Optional[str] = Field(default=None, description="Solution applied")
    solution_code: Optional[str] = Field(default=None, description="Solution code")
    solution_source: Optional[str] = Field(default=None, description="Solution source")
    solution_effective: Optional[bool] = Field(default=None, description="Was solution effective?")

    fixes_attempted: list[dict[str, Any]] = Field(default_factory=list, description="Fixes attempted")

    prevention_strategies: list[str] = Field(default_factory=list, description="Prevention strategies")

    related_knowledge: list[str] = Field(default_factory=list, description="Related knowledge article IDs")
    similar_incidents: list[str] = Field(default_factory=list, description="Similar incident IDs")

    resolution_time_minutes: Optional[int] = Field(default=None, description="Resolution time in minutes")
    attempts_count: int = Field(default=0, description="Number of fix attempts")

    user_id: Optional[str] = Field(default=None, description="User ID")
    organization_id: Optional[str] = Field(default=None, description="Organization ID")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = Field(default=None, description="Resolution timestamp")
    closed_at: Optional[datetime] = Field(default=None, description="Closure timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SolutionKnowledge(BaseModel):
    """Solution knowledge article from resolved incidents."""

    solution_id: str = Field(..., description="Unique solution identifier")

    problem_summary: str = Field(..., description="Problem summary")
    problem_pattern: str = Field(..., description="Problem pattern (normalized)")
    infrastructure_type: Optional[str] = Field(default=None, description="Infrastructure type")
    cloud_provider: Optional[str] = Field(default=None, description="Cloud provider")
    resource_type: Optional[str] = Field(default=None, description="Resource type")

    solution_description: str = Field(..., description="Solution description")
    solution_code: Optional[str] = Field(default=None, description="Solution code")
    solution_steps: list[str] = Field(default_factory=list, description="Solution steps")

    root_cause: str = Field(..., description="Root cause")

    prevention_strategies: list[str] = Field(default_factory=list, description="Prevention strategies")

    tags: list[str] = Field(default_factory=list, description="Tags")
    severity: IncidentSeverity = Field(..., description="Severity")

    source_incidents: list[str] = Field(default_factory=list, description="Source incident IDs")
    success_count: int = Field(default=1, ge=0, description="Number of successful applications")
    failure_count: int = Field(default=0, ge=0, description="Number of failed applications")
    success_rate: float = Field(default=1.0, ge=0.0, le=1.0, description="Success rate")

    quality_score: int = Field(default=0, ge=0, le=100, description="Quality score")
    verified: bool = Field(default=False, description="Verified solution")

    embedding: Optional[list[float]] = Field(default=None, description="Vector embedding")
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

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_used_at: Optional[datetime] = Field(default=None, description="Last usage timestamp")

    def to_searchable_text(self) -> str:
        """Convert solution to searchable text for embedding.
        
        Includes contextual description if available (for contextual retrieval).
        
        Returns:
            Searchable text string with contextual description prepended
        """
        text_parts = []
        
        if self.contextual_description:
            text_parts.append(self.contextual_description)
            text_parts.append("")
        
        text_parts.append(f"Problem: {self.problem_summary}\n")
        text_parts.append(f"Root Cause: {self.root_cause}\n")
        text_parts.append(f"Solution: {self.solution_description}\n")
        
        if self.solution_steps:
            text_parts.append("Steps: " + " ".join(self.solution_steps))
        
        if self.prevention_strategies:
            text_parts.append("Prevention: " + " ".join(self.prevention_strategies))
        
        if self.infrastructure_type:
            text_parts.append(f"Infrastructure: {self.infrastructure_type}")
        if self.cloud_provider:
            text_parts.append(f"Cloud: {self.cloud_provider}")
        if self.resource_type:
            text_parts.append(f"Resource: {self.resource_type}")
        
        return "\n".join(text_parts)

