"""Task tracking models for agent improvement measurement."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskMetrics(BaseModel):
    """Metrics for a task."""

    compliance_score: Optional[float] = Field(
        default=None, ge=0.0, le=100.0, description="Compliance adherence score (0-100)"
    )
    cost_accuracy: Optional[float] = Field(
        default=None, ge=0.0, le=100.0, description="Cost estimation accuracy (0-100)"
    )
    code_correctness: Optional[bool] = Field(
        default=None, description="Whether generated code is syntactically correct"
    )
    hallucinations_detected: int = Field(
        default=0, ge=0, description="Number of hallucinations detected"
    )
    validation_passed: bool = Field(
        default=False, description="Whether validation checks passed"
    )
    estimated_cost: Optional[float] = Field(
        default=None, ge=0.0, description="Estimated infrastructure cost"
    )
    actual_cost: Optional[float] = Field(
        default=None, ge=0.0, description="Actual infrastructure cost"
    )


class ValidationResults(BaseModel):
    """Validation results for a task."""

    terraform_validate: Optional[bool] = Field(
        default=None, description="Terraform validation result"
    )
    kubernetes_validate: Optional[bool] = Field(
        default=None, description="Kubernetes validation result"
    )
    compliance_check: Optional[bool] = Field(
        default=None, description="Compliance check result"
    )
    cost_estimate: Optional[bool] = Field(
        default=None, description="Cost estimate validation result"
    )
    errors: list[str] = Field(default_factory=list, description="Validation errors")


class TaskRecord(BaseModel):
    """Task tracking record."""

    task_id: str = Field(..., description="Unique task ID")
    user_id: str = Field(..., description="User ID")
    task_type: str = Field(
        ..., description="Task type: compliance, pricing, code_generation, best_practices"
    )
    task_description: str = Field(..., description="Task description")
    wistx_enabled: bool = Field(..., description="Whether WISTX was enabled")
    start_time: datetime = Field(..., description="Task start time")
    end_time: Optional[datetime] = Field(default=None, description="Task end time")
    duration_seconds: Optional[float] = Field(
        default=None, ge=0.0, description="Task duration in seconds"
    )
    status: str = Field(
        ..., description="Task status: completed, failed, in_progress, cancelled"
    )
    attempts: int = Field(default=1, ge=1, description="Number of attempts")
    wistx_tools_used: list[str] = Field(
        default_factory=list, description="WISTX tools used during task"
    )
    metrics: TaskMetrics = Field(default_factory=TaskMetrics, description="Task metrics")
    generated_code: Optional[str] = Field(
        default=None, description="Generated code (if applicable)"
    )
    validation_results: Optional[ValidationResults] = Field(
        default=None, description="Validation results"
    )
    user_feedback: Optional[dict] = Field(
        default=None, description="User feedback (rating, comments)"
    )


class TaskComparison(BaseModel):
    """Comparison between tasks with and without WISTX."""

    metric_name: str = Field(..., description="Metric name")
    without_wistx: float = Field(..., description="Value without WISTX")
    with_wistx: float = Field(..., description="Value with WISTX")
    improvement_percentage: float = Field(..., description="Improvement percentage")
    improvement_absolute: float = Field(..., description="Absolute improvement")
    statistical_significance: Optional[float] = Field(
        default=None, description="P-value for statistical significance"
    )


class AgentImprovementReport(BaseModel):
    """Agent improvement measurement report."""

    period_start: datetime = Field(..., description="Report period start")
    period_end: datetime = Field(..., description="Report period end")
    sample_size_without: int = Field(..., ge=0, description="Sample size without WISTX")
    sample_size_with: int = Field(..., ge=0, description="Sample size with WISTX")
    overall_improvement: float = Field(..., description="Overall improvement percentage")
    metrics: list[TaskComparison] = Field(
        default_factory=list, description="Individual metric comparisons"
    )
    task_type_breakdown: dict[str, TaskComparison] = Field(
        default_factory=dict, description="Breakdown by task type"
    )

