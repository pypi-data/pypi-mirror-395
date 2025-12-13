"""Evidence Collector for WISTX Compliance Reporting.

This module provides evidence collection from Infrastructure-as-Code (IaC) with:
- SHA-256 hash-based integrity verification
- Structured evidence artifacts for audit trails
- Control-to-evidence mapping
- Timestamp and metadata tracking

Evidence artifacts are designed to meet SOC 2 Type II and ISO 27001 audit requirements.
"""

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class EvidenceType(Enum):
    """Types of evidence artifacts."""
    IAC_CONFIGURATION = "iac_configuration"       # Terraform, CloudFormation, etc.
    SECURITY_POLICY = "security_policy"           # Security group rules, IAM policies
    ENCRYPTION_CONFIG = "encryption_config"       # Encryption settings, KMS configs
    NETWORK_CONFIG = "network_config"             # VPC, subnet, firewall rules
    LOGGING_CONFIG = "logging_config"             # CloudTrail, VPC Flow Logs configs
    ACCESS_CONTROL = "access_control"             # IAM roles, policies, MFA settings
    BACKUP_CONFIG = "backup_config"               # Backup policies, retention settings
    MONITORING_CONFIG = "monitoring_config"       # CloudWatch, alerting configurations
    COMPLIANCE_TAG = "compliance_tag"             # Resource tags for compliance


class EvidenceStatus(Enum):
    """Evidence verification status."""
    VERIFIED = "verified"         # Evidence matches expected configuration
    PARTIAL = "partial"           # Evidence partially matches requirements
    MISSING = "missing"           # Evidence not found
    OUTDATED = "outdated"         # Evidence timestamp is stale
    TAMPERED = "tampered"         # Hash mismatch detected


@dataclass
class EvidenceArtifact:
    """Individual evidence artifact with integrity tracking."""
    artifact_id: str
    evidence_type: EvidenceType
    control_ids: list[str]                    # Controls this evidence supports
    source: str                               # Source file or API
    content_hash: str                         # SHA-256 hash of content
    content_preview: str                      # First 500 chars of content
    collected_at: datetime
    status: EvidenceStatus = EvidenceStatus.VERIFIED
    metadata: dict[str, Any] = field(default_factory=dict)
    
    # Audit trail
    collected_by: str | None = None
    verified_by: str | None = None
    verified_at: datetime | None = None


@dataclass 
class EvidenceCollection:
    """Collection of evidence artifacts for an assessment."""
    assessment_id: str
    subject: str
    collected_at: datetime
    artifacts: list[EvidenceArtifact]
    master_hash: str                          # Hash of all artifact hashes
    total_controls_covered: int
    evidence_coverage_pct: float


class EvidenceCollector:
    """Collects and verifies evidence from Infrastructure-as-Code.
    
    This collector parses IaC configurations to extract evidence artifacts
    that demonstrate compliance control implementation. Evidence is hashed
    for integrity verification and mapped to specific compliance controls.
    """

    # Patterns for extracting evidence from Terraform
    TERRAFORM_PATTERNS = {
        EvidenceType.ENCRYPTION_CONFIG: [
            r'encrypted\s*=\s*true',
            r'kms_key_id\s*=',
            r'server_side_encryption',
            r'encryption_configuration',
        ],
        EvidenceType.LOGGING_CONFIG: [
            r'logging\s*\{',
            r'enable_logging\s*=\s*true',
            r'cloudwatch_log_group',
            r'flow_log',
        ],
        EvidenceType.ACCESS_CONTROL: [
            r'aws_iam_policy',
            r'aws_iam_role',
            r'google_project_iam',
            r'azurerm_role_assignment',
        ],
        EvidenceType.NETWORK_CONFIG: [
            r'aws_security_group',
            r'aws_vpc',
            r'google_compute_firewall',
            r'azurerm_network_security_group',
        ],
        EvidenceType.BACKUP_CONFIG: [
            r'backup_retention',
            r'aws_backup',
            r'snapshot',
            r'point_in_time_recovery',
        ],
    }

    # Control mapping - which controls require which evidence types
    CONTROL_EVIDENCE_MAPPING = {
        # SOC2 Trust Services Criteria
        "CC6.1": [EvidenceType.ACCESS_CONTROL],
        "CC6.6": [EvidenceType.NETWORK_CONFIG],
        "CC6.7": [EvidenceType.ENCRYPTION_CONFIG],
        "CC7.2": [EvidenceType.LOGGING_CONFIG, EvidenceType.MONITORING_CONFIG],
        "CC9.1": [EvidenceType.BACKUP_CONFIG],
        # PCI-DSS
        "3.4": [EvidenceType.ENCRYPTION_CONFIG],
        "7.1": [EvidenceType.ACCESS_CONTROL],
        "10.1": [EvidenceType.LOGGING_CONFIG],
        "1.1": [EvidenceType.NETWORK_CONFIG],
        # HIPAA
        "164.312(a)(2)(iv)": [EvidenceType.ENCRYPTION_CONFIG],
        "164.312(b)": [EvidenceType.LOGGING_CONFIG],
        "164.312(d)": [EvidenceType.ACCESS_CONTROL],
    }

    @classmethod
    def generate_hash(cls, content: str) -> str:
        """Generate SHA-256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    @classmethod
    def collect_from_iac(
        cls,
        infrastructure_code: str,
        subject: str,
        controls: list[dict[str, Any]] | None = None,
    ) -> EvidenceCollection:
        """Collect evidence artifacts from Infrastructure-as-Code.

        Args:
            infrastructure_code: The IaC content (Terraform, CloudFormation, etc.)
            subject: Subject of the assessment
            controls: List of compliance controls to map evidence to

        Returns:
            EvidenceCollection with all found evidence artifacts
        """
        now = datetime.now()
        artifacts: list[EvidenceArtifact] = []
        controls_covered: set[str] = set()
        
        # Extract evidence by type
        for evidence_type, patterns in cls.TERRAFORM_PATTERNS.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, infrastructure_code, re.IGNORECASE))
                
                for i, match in enumerate(matches):
                    # Extract context around the match (up to 500 chars)
                    start = max(0, match.start() - 100)
                    end = min(len(infrastructure_code), match.end() + 400)
                    context = infrastructure_code[start:end]
                    
                    # Find controls this evidence supports
                    supported_controls = []
                    for control_id, required_types in cls.CONTROL_EVIDENCE_MAPPING.items():
                        if evidence_type in required_types:
                            supported_controls.append(control_id)
                            controls_covered.add(control_id)
                    
                    artifact = EvidenceArtifact(
                        artifact_id=f"{evidence_type.value}_{i+1}",
                        evidence_type=evidence_type,
                        control_ids=supported_controls,
                        source="infrastructure_code",
                        content_hash=cls.generate_hash(context),
                        content_preview=context[:500],
                        collected_at=now,
                        metadata={
                            "pattern_matched": pattern,
                            "match_position": match.start(),
                        }
                    )
                    artifacts.append(artifact)
        
        # Calculate master hash
        all_hashes = sorted([a.content_hash for a in artifacts])
        master_hash = cls.generate_hash("|".join(all_hashes)) if all_hashes else cls.generate_hash("")
        
        # Calculate coverage
        total_controls = len(cls.CONTROL_EVIDENCE_MAPPING)
        coverage_pct = (len(controls_covered) / total_controls * 100) if total_controls > 0 else 0
        
        return EvidenceCollection(
            assessment_id=cls.generate_hash(f"{subject}_{now.isoformat()}"),
            subject=subject,
            collected_at=now,
            artifacts=artifacts,
            master_hash=master_hash,
            total_controls_covered=len(controls_covered),
            evidence_coverage_pct=coverage_pct,
        )

    @classmethod
    def generate_evidence_markdown(cls, collection: EvidenceCollection) -> str:
        """Generate markdown representation of evidence collection.

        Returns:
            Markdown string with evidence summary and artifacts
        """
        md = []
        md.append("## Evidence Artifacts\n\n")
        md.append(f"**Assessment ID**: `{collection.assessment_id[:16]}...`\n")
        md.append(f"**Collected**: {collection.collected_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
        md.append(f"**Master Hash**: `{collection.master_hash[:16]}...`\n\n")

        # Summary
        md.append("### Evidence Summary\n\n")
        md.append(f"| Metric | Value |\n")
        md.append(f"|--------|-------|\n")
        md.append(f"| Total Artifacts | {len(collection.artifacts)} |\n")
        md.append(f"| Controls Covered | {collection.total_controls_covered} |\n")
        md.append(f"| Evidence Coverage | {collection.evidence_coverage_pct:.1f}% |\n\n")

        # Artifacts by type
        if collection.artifacts:
            md.append("### Artifacts by Type\n\n")
            md.append("| ID | Type | Controls | Hash | Status |\n")
            md.append("|----|------|----------|------|--------|\n")

            for artifact in collection.artifacts[:20]:  # Limit to 20
                controls_str = ", ".join(artifact.control_ids[:3])
                if len(artifact.control_ids) > 3:
                    controls_str += f" +{len(artifact.control_ids) - 3}"
                md.append(
                    f"| {artifact.artifact_id} | {artifact.evidence_type.value} | "
                    f"{controls_str} | `{artifact.content_hash[:8]}...` | "
                    f"{artifact.status.value} |\n"
                )

            if len(collection.artifacts) > 20:
                md.append(f"\n*...and {len(collection.artifacts) - 20} more artifacts*\n")
            md.append("\n")

        return "".join(md)

    @classmethod
    def collection_to_dict(cls, collection: EvidenceCollection) -> dict[str, Any]:
        """Convert evidence collection to dictionary for serialization."""
        return {
            "assessment_id": collection.assessment_id,
            "subject": collection.subject,
            "collected_at": collection.collected_at.isoformat(),
            "master_hash": collection.master_hash,
            "total_artifacts": len(collection.artifacts),
            "total_controls_covered": collection.total_controls_covered,
            "evidence_coverage_pct": collection.evidence_coverage_pct,
            "artifacts": [
                {
                    "artifact_id": a.artifact_id,
                    "evidence_type": a.evidence_type.value,
                    "control_ids": a.control_ids,
                    "source": a.source,
                    "content_hash": a.content_hash,
                    "collected_at": a.collected_at.isoformat(),
                    "status": a.status.value,
                }
                for a in collection.artifacts
            ],
        }

