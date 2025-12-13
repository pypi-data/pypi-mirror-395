"""Quality score models for repository trees and infrastructure visualizations."""

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field


@dataclass
class QualityScoreBreakdown:
    """Detailed quality score breakdown."""

    structure_completeness: float = 0.0
    infrastructure_quality: float = 0.0
    devops_maturity: float = 0.0
    documentation_quality: float = 0.0
    compliance_security: float = 0.0
    code_organization: float = 0.0
    diagram_completeness: float = 0.0
    visualization_accuracy: float = 0.0
    diagram_quality: float = 0.0
    infrastructure_complexity: float = 0.0
    best_practices: float = 0.0


class QualityScoreResult(BaseModel):
    """Quality score result model."""

    overall_score: float = Field(..., ge=0.0, le=100.0, description="Overall quality score (0-100)")
    score_breakdown: dict[str, float] = Field(default_factory=dict, description="Detailed score breakdown")
    recommendations: list[str] = Field(default_factory=list, description="Improvement recommendations")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    meets_threshold: bool = Field(default=False, description="Whether score meets storage threshold (80%)")

    model_config = {"extra": "forbid"}

