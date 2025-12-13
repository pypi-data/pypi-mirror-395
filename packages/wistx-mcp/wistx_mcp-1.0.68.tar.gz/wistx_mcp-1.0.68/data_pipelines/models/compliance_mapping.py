"""Compliance mapping data models.

Maps code examples to compliance controls without directly tagging examples as compliant.
This allows multiple standards to map to the same example independently.
"""

import hashlib
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ComplianceMapping(BaseModel):
    """Mapping between code example and compliance control."""

    mapping_id: str = Field(..., description="Unique mapping identifier")
    example_id: str = Field(..., description="Reference to code_examples collection")
    control_id: str = Field(..., description="Reference to compliance_controls collection")
    standard: str = Field(..., description="Compliance standard (PCI-DSS, HIPAA, etc.)")
    severity: str = Field(..., description="Control severity (HIGH, MEDIUM, LOW, CRITICAL)")
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How relevant this control is to this example (0.0-1.0)",
    )
    applies_to_resources: list[str] = Field(
        default_factory=list,
        description="Which resources in example this control applies to",
    )
    implementation_status: str = Field(
        ...,
        description="Implementation status: implemented, partial, missing, not_applicable",
    )
    notes: str = Field(
        default="",
        description="Why this mapping exists, implementation details, etc.",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Mapping creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    @classmethod
    def generate_mapping_id(
        cls,
        example_id: str,
        control_id: str,
        standard: str,
    ) -> str:
        """Generate unique mapping ID.
        
        Args:
            example_id: Code example ID
            control_id: Compliance control ID
            standard: Compliance standard
            
        Returns:
            Unique mapping ID
        """
        unique_string = f"{example_id}:{control_id}:{standard}"
        hash_obj = hashlib.sha256(unique_string.encode("utf-8"))
        return hash_obj.hexdigest()[:24]

