"""Compliance Evidence and Assessment Persistence for WISTX.

This module provides MongoDB persistence for:
- Compliance assessment history (for trend tracking)
- Evidence artifacts (with integrity verification)
- Audit trails (immutable log of all compliance activities)

Designed for SOC 2 Type II and ISO 27001 audit requirements.
"""

import logging
from datetime import datetime
from typing import Any
from enum import Enum

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# Collection names
COLLECTION_COMPLIANCE_ASSESSMENTS = "compliance_assessments"
COLLECTION_EVIDENCE_ARTIFACTS = "evidence_artifacts"
COLLECTION_COMPLIANCE_AUDIT_TRAIL = "compliance_audit_trail"


class AssessmentStatus(str, Enum):
    """Status of a compliance assessment."""
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"


class AuditAction(str, Enum):
    """Types of audit trail actions."""
    ASSESSMENT_CREATED = "assessment_created"
    ASSESSMENT_UPDATED = "assessment_updated"
    EVIDENCE_COLLECTED = "evidence_collected"
    EVIDENCE_VERIFIED = "evidence_verified"
    EVIDENCE_TAMPERED = "evidence_tampered"
    REPORT_GENERATED = "report_generated"
    SCORECARD_CALCULATED = "scorecard_calculated"


class ComplianceAssessmentDocument(BaseModel):
    """MongoDB document for compliance assessment history."""
    assessment_id: str = Field(..., description="Unique assessment ID (SHA-256 hash)")
    user_id: str = Field(..., description="User who initiated assessment")
    subject: str = Field(..., description="Subject of assessment (project, resource, etc.)")
    
    # Scoring data
    overall_score: float = Field(..., ge=0, le=100, description="Overall compliance score")
    risk_adjusted_score: float = Field(..., ge=0, le=100, description="Risk-adjusted score")
    framework_scores: dict[str, float] = Field(default_factory=dict, description="Per-framework scores")
    
    # Assessment details
    frameworks_assessed: list[str] = Field(default_factory=list, description="Compliance frameworks")
    total_controls: int = Field(default=0, description="Total controls evaluated")
    compliant_controls: int = Field(default=0, description="Number of compliant controls")
    non_compliant_controls: int = Field(default=0, description="Number of non-compliant controls")
    
    # Severity breakdown
    severity_breakdown: dict[str, dict[str, int]] = Field(
        default_factory=dict, 
        description="Breakdown by severity: {CRITICAL: {compliant: X, non_compliant: Y}, ...}"
    )
    
    # Evidence reference
    evidence_collection_id: str | None = Field(None, description="Reference to evidence collection")
    evidence_hash: str = Field(..., description="SHA-256 hash for integrity verification")
    
    # Metadata
    status: AssessmentStatus = Field(default=AssessmentStatus.COMPLETED)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Context
    source: str = Field(default="mcp_tool", description="Source: mcp_tool, api, ci_cd")
    git_commit: str | None = Field(None, description="Git commit SHA if from CI/CD")
    git_branch: str | None = Field(None, description="Git branch if from CI/CD")
    infrastructure_hash: str | None = Field(None, description="Hash of IaC content")


class EvidenceArtifactDocument(BaseModel):
    """MongoDB document for evidence artifacts."""
    artifact_id: str = Field(..., description="Unique artifact ID")
    assessment_id: str = Field(..., description="Parent assessment ID")
    user_id: str = Field(..., description="User ID")
    
    evidence_type: str = Field(..., description="Type: iac_configuration, security_policy, etc.")
    control_ids: list[str] = Field(default_factory=list, description="Controls this supports")
    
    # Integrity
    content_hash: str = Field(..., description="SHA-256 hash of content")
    content_preview: str = Field(..., max_length=1000, description="Preview (first 500 chars)")
    
    # Source
    source: str = Field(..., description="Source file or API")
    source_type: str = Field(default="terraform", description="terraform, cloudformation, k8s, api")
    
    # Status
    status: str = Field(default="verified", description="verified, partial, missing, tampered")
    verified_at: datetime | None = Field(None, description="When artifact was verified")
    verified_by: str | None = Field(None, description="Who verified (user or system)")
    
    # Metadata
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ComplianceAuditTrailDocument(BaseModel):
    """Immutable audit trail entry for compliance activities."""
    trail_id: str = Field(..., description="Unique trail entry ID")
    user_id: str = Field(..., description="User ID")
    action: AuditAction = Field(..., description="Type of action")
    
    # References
    assessment_id: str | None = Field(None, description="Related assessment")
    artifact_id: str | None = Field(None, description="Related artifact")
    
    # Action details
    details: dict[str, Any] = Field(default_factory=dict, description="Action-specific details")
    
    # Integrity
    previous_hash: str | None = Field(None, description="Hash of previous entry (blockchain-style)")
    entry_hash: str = Field(..., description="Hash of this entry")
    
    # Timestamp (immutable)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Source
    ip_address: str | None = Field(None)
    user_agent: str | None = Field(None)


class CompliancePersistenceService:
    """Service for persisting compliance data to MongoDB."""

    def __init__(self, mongodb_client: Any):
        """Initialize with MongoDB client.

        Args:
            mongodb_client: MongoDBClient instance (from wistx_mcp.tools.lib.mongodb_client)
        """
        self.mongodb_client = mongodb_client
        self._last_audit_hash: str | None = None

    async def _ensure_connected(self) -> None:
        """Ensure MongoDB is connected."""
        if self.mongodb_client.database is None:
            await self.mongodb_client.connect()

    async def save_assessment(
        self,
        assessment: ComplianceAssessmentDocument,
    ) -> str:
        """Save a compliance assessment to MongoDB.

        Args:
            assessment: Assessment document to save

        Returns:
            Assessment ID
        """
        await self._ensure_connected()
        db = self.mongodb_client.database
        if db is None:
            raise RuntimeError("MongoDB not available")

        collection = db[COLLECTION_COMPLIANCE_ASSESSMENTS]
        assessment_dict = assessment.model_dump()
        assessment_dict["updated_at"] = datetime.utcnow()

        await collection.update_one(
            {"assessment_id": assessment.assessment_id},
            {"$set": assessment_dict},
            upsert=True,
        )

        # Create audit trail entry
        await self._create_audit_entry(
            user_id=assessment.user_id,
            action=AuditAction.ASSESSMENT_CREATED,
            assessment_id=assessment.assessment_id,
            details={
                "subject": assessment.subject,
                "overall_score": assessment.overall_score,
                "frameworks": assessment.frameworks_assessed,
            },
        )

        logger.info(
            "Saved assessment %s for user %s (score: %.1f%%)",
            assessment.assessment_id[:16],
            assessment.user_id,
            assessment.overall_score,
        )
        return assessment.assessment_id

    async def save_evidence_artifacts(
        self,
        artifacts: list[EvidenceArtifactDocument],
    ) -> int:
        """Save evidence artifacts to MongoDB.

        Args:
            artifacts: List of evidence artifact documents

        Returns:
            Number of artifacts saved
        """
        if not artifacts:
            return 0

        await self._ensure_connected()
        db = self.mongodb_client.database
        if db is None:
            raise RuntimeError("MongoDB not available")

        collection = db[COLLECTION_EVIDENCE_ARTIFACTS]

        for artifact in artifacts:
            artifact_dict = artifact.model_dump()
            await collection.update_one(
                {"artifact_id": artifact.artifact_id, "assessment_id": artifact.assessment_id},
                {"$set": artifact_dict},
                upsert=True,
            )

        # Create audit trail entry
        if artifacts:
            await self._create_audit_entry(
                user_id=artifacts[0].user_id,
                action=AuditAction.EVIDENCE_COLLECTED,
                assessment_id=artifacts[0].assessment_id,
                details={
                    "artifact_count": len(artifacts),
                    "evidence_types": list(set(a.evidence_type for a in artifacts)),
                },
            )

        logger.info("Saved %d evidence artifacts", len(artifacts))
        return len(artifacts)

    async def get_assessment_history(
        self,
        user_id: str,
        subject: str | None = None,
        frameworks: list[str] | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get assessment history for trend analysis.

        Args:
            user_id: User ID
            subject: Optional subject filter
            frameworks: Optional framework filter
            limit: Maximum results

        Returns:
            List of assessment documents (newest first)
        """
        await self._ensure_connected()
        db = self.mongodb_client.database
        if db is None:
            return []

        collection = db[COLLECTION_COMPLIANCE_ASSESSMENTS]

        query: dict[str, Any] = {"user_id": user_id}
        if subject:
            query["subject"] = subject
        if frameworks:
            query["frameworks_assessed"] = {"$in": frameworks}

        cursor = collection.find(query).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_trend_data(
        self,
        user_id: str,
        subject: str,
        days: int = 90,
    ) -> dict[str, Any]:
        """Get trend data for compliance scores over time.

        Args:
            user_id: User ID
            subject: Subject to track
            days: Number of days to look back

        Returns:
            Trend analysis with scores over time
        """
        from datetime import timedelta

        await self._ensure_connected()
        db = self.mongodb_client.database
        if db is None:
            return {"error": "MongoDB not available"}

        collection = db[COLLECTION_COMPLIANCE_ASSESSMENTS]
        cutoff = datetime.utcnow() - timedelta(days=days)

        cursor = collection.find({
            "user_id": user_id,
            "subject": subject,
            "created_at": {"$gte": cutoff},
        }).sort("created_at", 1)

        assessments = await cursor.to_list(length=1000)

        if not assessments:
            return {
                "subject": subject,
                "period_days": days,
                "data_points": 0,
                "trend": "no_data",
                "scores": [],
            }

        scores = [
            {
                "date": a["created_at"].isoformat() if isinstance(a["created_at"], datetime) else a["created_at"],
                "overall_score": a["overall_score"],
                "risk_adjusted_score": a["risk_adjusted_score"],
                "frameworks": a.get("frameworks_assessed", []),
            }
            for a in assessments
        ]

        # Calculate trend
        if len(scores) >= 2:
            first_score = scores[0]["overall_score"]
            last_score = scores[-1]["overall_score"]
            delta = last_score - first_score

            if delta > 5:
                trend = "improving"
            elif delta < -5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "subject": subject,
            "period_days": days,
            "data_points": len(scores),
            "trend": trend,
            "first_score": scores[0]["overall_score"] if scores else None,
            "latest_score": scores[-1]["overall_score"] if scores else None,
            "score_delta": scores[-1]["overall_score"] - scores[0]["overall_score"] if len(scores) >= 2 else 0,
            "scores": scores,
        }

    async def _create_audit_entry(
        self,
        user_id: str,
        action: AuditAction,
        assessment_id: str | None = None,
        artifact_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> str:
        """Create an immutable audit trail entry.

        Args:
            user_id: User ID
            action: Type of action
            assessment_id: Related assessment
            artifact_id: Related artifact
            details: Action-specific details

        Returns:
            Trail entry ID
        """
        import hashlib
        import uuid

        await self._ensure_connected()
        db = self.mongodb_client.database
        if db is None:
            logger.warning("MongoDB not available for audit trail")
            return ""

        collection = db[COLLECTION_COMPLIANCE_AUDIT_TRAIL]

        # Create entry hash (blockchain-style)
        trail_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        hash_content = f"{trail_id}|{user_id}|{action.value}|{timestamp.isoformat()}|{self._last_audit_hash or 'genesis'}"
        entry_hash = hashlib.sha256(hash_content.encode()).hexdigest()

        entry = ComplianceAuditTrailDocument(
            trail_id=trail_id,
            user_id=user_id,
            action=action,
            assessment_id=assessment_id,
            artifact_id=artifact_id,
            details=details or {},
            previous_hash=self._last_audit_hash,
            entry_hash=entry_hash,
            timestamp=timestamp,
        )

        await collection.insert_one(entry.model_dump())
        self._last_audit_hash = entry_hash

        return trail_id

    async def get_audit_trail(
        self,
        user_id: str,
        assessment_id: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get audit trail entries.

        Args:
            user_id: User ID
            assessment_id: Optional assessment filter
            limit: Maximum results

        Returns:
            List of audit trail entries (newest first)
        """
        await self._ensure_connected()
        db = self.mongodb_client.database
        if db is None:
            return []

        collection = db[COLLECTION_COMPLIANCE_AUDIT_TRAIL]

        query: dict[str, Any] = {"user_id": user_id}
        if assessment_id:
            query["assessment_id"] = assessment_id

        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def verify_audit_chain(
        self,
        user_id: str,
        limit: int = 100,
    ) -> dict[str, Any]:
        """Verify integrity of audit trail chain.

        Checks that no entries have been tampered with by verifying
        the hash chain (blockchain-style integrity).

        Args:
            user_id: User ID
            limit: Number of entries to verify

        Returns:
            Verification result with any integrity issues
        """
        import hashlib

        await self._ensure_connected()
        db = self.mongodb_client.database
        if db is None:
            return {"verified": False, "error": "MongoDB not available"}

        collection = db[COLLECTION_COMPLIANCE_AUDIT_TRAIL]

        # Get entries in chronological order
        cursor = collection.find({"user_id": user_id}).sort("timestamp", 1).limit(limit)
        entries = await cursor.to_list(length=limit)

        if not entries:
            return {"verified": True, "entries_checked": 0, "message": "No entries to verify"}

        issues = []
        previous_hash = None

        for i, entry in enumerate(entries):
            # Verify previous_hash matches
            if entry.get("previous_hash") != previous_hash:
                if i > 0:  # Skip first entry (genesis)
                    issues.append({
                        "entry": i,
                        "trail_id": entry.get("trail_id"),
                        "issue": "previous_hash mismatch - possible tampering",
                    })

            previous_hash = entry.get("entry_hash")

        return {
            "verified": len(issues) == 0,
            "entries_checked": len(entries),
            "issues": issues,
            "message": "Audit chain verified successfully" if not issues else f"Found {len(issues)} integrity issues",
        }

