"""Request and response models for custom compliance controls API."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class UploadComplianceDocumentRequest(BaseModel):
    """Request model for uploading compliance document."""

    standard: str = Field(..., description="Compliance standard name (e.g., PCI-DSS-CUSTOM)")
    version: str = Field(default="1.0", description="Standard version")
    visibility: str = Field(
        default="organization",
        description="Visibility: organization, user, or global",
        pattern="^(organization|user|global)$",
    )
    name: Optional[str] = Field(default=None, description="Document name")
    description: Optional[str] = Field(default=None, description="Document description")
    auto_approve: bool = Field(
        default=False,
        description="Auto-approve extracted controls (skip review)",
    )
    extraction_method: str = Field(
        default="llm",
        description="Extraction method: llm, structured, manual",
        pattern="^(llm|structured|manual)$",
    )


class UploadComplianceDocumentResponse(BaseModel):
    """Response model for compliance document upload."""

    upload_id: str = Field(..., description="Upload job ID")
    document_id: str = Field(..., description="Document ID")
    status: str = Field(..., description="Status: pending, processing, completed, failed")
    controls_extracted: int = Field(default=0, description="Number of controls extracted")
    controls_pending_review: int = Field(default=0, description="Number of controls pending review")
    message: str = Field(..., description="Status message")
    estimated_completion_time: Optional[datetime] = Field(
        default=None,
        description="Estimated completion time",
    )


class CustomComplianceControlResponse(BaseModel):
    """Response model for custom compliance control."""

    control_id: str = Field(..., description="Control ID")
    standard: str = Field(..., description="Compliance standard")
    version: str = Field(..., description="Standard version")
    title: str = Field(..., description="Control title")
    description: str = Field(..., description="Control description")
    requirement: Optional[str] = Field(default=None, description="Requirement text")
    severity: str = Field(..., description="Severity level")
    category: Optional[str] = Field(default=None, description="Category")
    subcategory: Optional[str] = Field(default=None, description="Subcategory")
    applies_to: list[str] = Field(default_factory=list, description="Applicable resources")
    remediation: dict[str, Any] = Field(..., description="Remediation guidance")
    verification: Optional[dict[str, Any]] = Field(default=None, description="Verification procedures")
    references: list[dict[str, Any]] = Field(default_factory=list, description="External references")
    visibility: str = Field(..., description="Visibility scope")
    is_custom: bool = Field(..., description="Is custom control")
    source: str = Field(..., description="Source")
    source_document_id: Optional[str] = Field(default=None, description="Source document ID")
    source_document_name: Optional[str] = Field(default=None, description="Source document name")
    extraction_method: Optional[str] = Field(default=None, description="Extraction method")
    extraction_confidence: Optional[float] = Field(default=None, description="Extraction confidence")
    reviewed: bool = Field(..., description="Reviewed status")
    reviewed_at: Optional[datetime] = Field(default=None, description="Review timestamp")
    reviewed_by: Optional[str] = Field(default=None, description="Reviewer user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")


class CustomControlsListResponse(BaseModel):
    """Response model for listing custom compliance controls."""

    controls: list[CustomComplianceControlResponse] = Field(default_factory=list, description="List of controls")
    total: int = Field(..., description="Total count")
    limit: int = Field(..., description="Limit")
    offset: int = Field(..., description="Offset")
    has_more: bool = Field(..., description="Has more results")


class UpdateCustomControlRequest(BaseModel):
    """Request model for updating custom compliance control."""

    title: Optional[str] = None
    description: Optional[str] = None
    requirement: Optional[str] = None
    severity: Optional[str] = Field(default=None, pattern="^(CRITICAL|HIGH|MEDIUM|LOW)$")
    category: Optional[str] = None
    subcategory: Optional[str] = None
    applies_to: Optional[list[str]] = None
    remediation: Optional[dict[str, Any]] = None
    verification: Optional[dict[str, Any]] = None
    references: Optional[list[dict[str, Any]]] = None
    visibility: Optional[str] = Field(default=None, pattern="^(organization|user|global)$")
    reviewed: Optional[bool] = None


class DeleteCustomControlResponse(BaseModel):
    """Response model for deleting custom compliance control."""

    control_id: str = Field(..., description="Control ID")
    deleted: bool = Field(..., description="Deleted status")
    message: str = Field(..., description="Message")


class ReviewCustomControlRequest(BaseModel):
    """Request model for reviewing custom compliance control."""

    approved: bool = Field(..., description="Whether control is approved")
    notes: Optional[str] = Field(default=None, description="Review notes")


class ReviewCustomControlResponse(BaseModel):
    """Response model for reviewing custom compliance control."""

    control_id: str = Field(..., description="Control ID")
    reviewed: bool = Field(..., description="Reviewed status")
    reviewed_at: datetime = Field(..., description="Review timestamp")
    reviewed_by: str = Field(..., description="Reviewer user ID")
    notes: Optional[str] = Field(default=None, description="Review notes")


class UploadStatusResponse(BaseModel):
    """Response model for upload status."""

    upload_id: str = Field(..., description="Upload ID")
    document_id: str = Field(..., description="Document ID")
    status: str = Field(..., description="Status")
    progress: float = Field(..., ge=0.0, le=100.0, description="Progress percentage")
    controls_extracted: int = Field(default=0, description="Controls extracted")
    controls_pending_review: int = Field(default=0, description="Controls pending review")
    controls_approved: int = Field(default=0, description="Controls approved")
    controls_rejected: int = Field(default=0, description="Controls rejected")
    error_message: Optional[str] = Field(default=None, description="Error message")
    started_at: datetime = Field(..., description="Start timestamp")
    completed_at: Optional[datetime] = Field(default=None, description="Completion timestamp")
    estimated_completion_time: Optional[datetime] = Field(
        default=None,
        description="Estimated completion time",
    )




