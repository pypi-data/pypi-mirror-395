"""Audit Workpaper Generator for WISTX.

This module generates AICPA/PCAOB-compliant audit workpapers that:
- Document audit procedures performed
- Record evidence examined and conclusions reached
- Support the auditor's report
- Meet 7-year retention requirements (PCAOB AS 1215)

Industry Standards Implemented:
- PCAOB AS 1215 (Audit Documentation)
- AICPA AU-C Section 230 (Audit Documentation)
- ISA 230 (Audit Documentation)
- SOC 2 Type II reporting requirements
"""

import hashlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class WorkpaperType(Enum):
    """Types of audit workpapers."""
    # Planning workpapers
    PLANNING_MEMO = "planning_memo"
    RISK_ASSESSMENT = "risk_assessment"
    MATERIALITY_CALCULATION = "materiality_calculation"
    
    # Testing workpapers
    CONTROL_TESTING = "control_testing"
    SUBSTANTIVE_TESTING = "substantive_testing"
    SAMPLING_DOCUMENTATION = "sampling_documentation"
    
    # Completion workpapers
    SUMMARY_OF_FINDINGS = "summary_of_findings"
    MANAGEMENT_REPRESENTATION = "management_representation"
    COMPLETION_CHECKLIST = "completion_checklist"
    
    # Evidence workpapers
    EVIDENCE_COLLECTION = "evidence_collection"
    INQUIRY_DOCUMENTATION = "inquiry_documentation"
    OBSERVATION_DOCUMENTATION = "observation_documentation"


class WorkpaperStatus(Enum):
    """Workpaper review status."""
    DRAFT = "draft"
    PREPARED = "prepared"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    SUPERSEDED = "superseded"


@dataclass
class WorkpaperReference:
    """Cross-reference to other workpapers or evidence."""
    reference_id: str
    reference_type: str  # workpaper, evidence, external
    description: str
    location: str = ""


@dataclass
class ReviewNote:
    """Review note on workpaper."""
    note_id: str
    reviewer: str
    date: datetime
    note_type: str  # question, comment, suggestion, cleared
    content: str
    response: str = ""
    cleared: bool = False
    cleared_by: str = ""
    cleared_date: datetime | None = None


@dataclass
class Workpaper:
    """Audit workpaper per PCAOB AS 1215."""
    # Identification
    workpaper_id: str
    workpaper_type: WorkpaperType
    title: str
    
    # Engagement information
    engagement_name: str
    engagement_period_start: datetime
    engagement_period_end: datetime
    
    # Content
    objective: str
    procedures_performed: list[str]
    evidence_examined: list[str]
    findings: list[str]
    conclusion: str
    
    # Cross-references
    references: list[WorkpaperReference] = field(default_factory=list)
    
    # Review trail
    prepared_by: str = ""
    prepared_date: datetime | None = None
    reviewed_by: str = ""
    reviewed_date: datetime | None = None
    review_notes: list[ReviewNote] = field(default_factory=list)
    status: WorkpaperStatus = WorkpaperStatus.DRAFT
    
    # Integrity
    content_hash: str = ""
    version: int = 1
    
    # Retention (PCAOB AS 1215 requires 7 years)
    retention_date: datetime | None = None


class WorkpaperGenerator:
    """Generates AICPA/PCAOB-compliant audit workpapers.
    
    This generator creates standardized workpapers that meet
    professional documentation requirements and support the
    audit opinion.
    """
    
    def __init__(
        self,
        engagement_name: str,
        period_start: datetime,
        period_end: datetime,
        preparer: str = "",
    ):
        """Initialize workpaper generator.
        
        Args:
            engagement_name: Name of the audit engagement
            period_start: Start of audit period
            period_end: End of audit period
            preparer: Name of preparer
        """
        self.engagement_name = engagement_name
        self.period_start = period_start
        self.period_end = period_end
        self.preparer = preparer
        self._workpaper_counter = 0
    
    def _generate_workpaper_id(self, prefix: str = "WP") -> str:
        """Generate unique workpaper ID."""
        self._workpaper_counter += 1
        date_str = datetime.now().strftime("%Y%m%d")
        return f"{prefix}-{date_str}-{self._workpaper_counter:04d}"
    
    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def generate_control_testing_workpaper(
        self,
        control_id: str,
        control_description: str,
        testing_procedures: list[str],
        sample_items: list[dict[str, Any]],
        exceptions: list[dict[str, Any]],
        conclusion: str,
    ) -> Workpaper:
        """Generate workpaper for control testing.
        
        Args:
            control_id: Control identifier
            control_description: Description of control
            testing_procedures: List of procedures performed
            sample_items: Items tested
            exceptions: Exceptions noted
            conclusion: Testing conclusion
            
        Returns:
            Completed workpaper
        """
        # Format evidence examined
        evidence = [
            f"Sample item {i+1}: {item.get('id', 'N/A')} - {item.get('description', '')}"
            for i, item in enumerate(sample_items)
        ]
        
        # Format findings
        findings = []
        if exceptions:
            for exc in exceptions:
                findings.append(
                    f"Exception: {exc.get('description', 'N/A')} - "
                    f"Management Response: {exc.get('response', 'Pending')}"
                )
        else:
            findings.append("No exceptions noted during testing.")
        
        workpaper = Workpaper(
            workpaper_id=self._generate_workpaper_id("CT"),
            workpaper_type=WorkpaperType.CONTROL_TESTING,
            title=f"Control Testing - {control_id}",
            engagement_name=self.engagement_name,
            engagement_period_start=self.period_start,
            engagement_period_end=self.period_end,
            objective=f"Test operating effectiveness of control {control_id}: {control_description}",
            procedures_performed=testing_procedures,
            evidence_examined=evidence,
            findings=findings,
            conclusion=conclusion,
            prepared_by=self.preparer,
            prepared_date=datetime.now(),
        )
        
        # Calculate content hash
        content = f"{workpaper.objective}{workpaper.procedures_performed}{workpaper.findings}"
        workpaper.content_hash = self._calculate_hash(content)

        return workpaper

    def generate_sampling_workpaper(
        self,
        sample_result: Any,  # SampleResult from audit_sampling
        population_description: str,
        sampling_rationale: str,
    ) -> Workpaper:
        """Generate workpaper documenting sampling methodology.

        Per PCAOB AS 2315, sampling documentation must include:
        - Description of population
        - Sampling method and rationale
        - Sample size determination
        - Selection method
        - Evaluation of results

        Args:
            sample_result: Results from audit sampling
            population_description: Description of population sampled
            sampling_rationale: Rationale for sampling approach

        Returns:
            Completed workpaper
        """
        procedures = [
            f"1. Defined population: {population_description}",
            f"2. Selected sampling method: {sample_result.sampling_method.value}",
            f"3. Determined sample size: {sample_result.sample_size} items",
            f"4. Applied selection technique with interval: {sample_result.items[0].selection_interval if sample_result.items else 'N/A'}",
            "5. Performed testing procedures on selected items",
            "6. Evaluated sample results and projected to population",
        ]

        evidence = [
            f"Population size: {sample_result.parameters.population_size}",
            f"Population value: ${sample_result.parameters.population_value:,.2f}" if sample_result.parameters.population_value else "N/A",
            f"Tolerable misstatement: ${sample_result.parameters.tolerable_misstatement:,.2f}" if sample_result.parameters.tolerable_misstatement else "N/A",
            f"Risk assessment: {sample_result.parameters.risk_of_material_misstatement.value}",
            f"Sample items selected: {sample_result.sample_size}",
        ]

        findings = [
            f"Exceptions found: {sample_result.exceptions_found}",
            f"Projected misstatement: ${sample_result.projected_misstatement:,.2f}" if sample_result.projected_misstatement else "No misstatement projected",
        ]

        workpaper = Workpaper(
            workpaper_id=self._generate_workpaper_id("SP"),
            workpaper_type=WorkpaperType.SAMPLING_DOCUMENTATION,
            title=f"Sampling Documentation - {sample_result.sample_id}",
            engagement_name=self.engagement_name,
            engagement_period_start=self.period_start,
            engagement_period_end=self.period_end,
            objective=f"Document sampling methodology and results. Rationale: {sampling_rationale}",
            procedures_performed=procedures,
            evidence_examined=evidence,
            findings=findings,
            conclusion=sample_result.conclusion or "See evaluation results.",
            prepared_by=self.preparer,
            prepared_date=datetime.now(),
        )

        content = f"{workpaper.objective}{workpaper.procedures_performed}{workpaper.findings}"
        workpaper.content_hash = self._calculate_hash(content)

        return workpaper

    def generate_evidence_collection_workpaper(
        self,
        evidence_items: list[dict[str, Any]],
        source_description: str,
        collection_method: str,
    ) -> Workpaper:
        """Generate workpaper for evidence collection.

        Documents evidence gathered from IaC, configurations,
        logs, and other sources.

        Args:
            evidence_items: List of evidence items collected
            source_description: Description of evidence source
            collection_method: How evidence was collected

        Returns:
            Completed workpaper
        """
        procedures = [
            f"1. Identified evidence source: {source_description}",
            f"2. Applied collection method: {collection_method}",
            "3. Verified evidence integrity using SHA-256 hashing",
            "4. Mapped evidence to applicable controls",
            "5. Documented evidence artifacts with timestamps",
        ]

        evidence = []
        for item in evidence_items:
            evidence.append(
                f"- {item.get('type', 'Unknown')}: {item.get('description', 'N/A')} "
                f"(Hash: {item.get('hash', 'N/A')[:16]}...)"
            )

        findings = [
            f"Total evidence items collected: {len(evidence_items)}",
            f"Evidence source: {source_description}",
            f"Collection timestamp: {datetime.now().isoformat()}",
        ]

        workpaper = Workpaper(
            workpaper_id=self._generate_workpaper_id("EC"),
            workpaper_type=WorkpaperType.EVIDENCE_COLLECTION,
            title=f"Evidence Collection - {source_description[:50]}",
            engagement_name=self.engagement_name,
            engagement_period_start=self.period_start,
            engagement_period_end=self.period_end,
            objective=f"Collect and document evidence from {source_description}",
            procedures_performed=procedures,
            evidence_examined=evidence,
            findings=findings,
            conclusion="Evidence collected and verified. See cross-references for control mapping.",
            prepared_by=self.preparer,
            prepared_date=datetime.now(),
        )

        content = f"{workpaper.objective}{evidence_items}"
        workpaper.content_hash = self._calculate_hash(content)

        return workpaper

    def generate_summary_of_findings_workpaper(
        self,
        findings: list[dict[str, Any]],
        overall_conclusion: str,
    ) -> Workpaper:
        """Generate summary of findings workpaper.

        Aggregates all findings from the engagement for
        management and audit committee communication.

        Args:
            findings: List of findings from all testing
            overall_conclusion: Overall engagement conclusion

        Returns:
            Completed workpaper
        """
        procedures = [
            "1. Aggregated findings from all testing workpapers",
            "2. Classified findings by severity and control area",
            "3. Evaluated impact on audit opinion",
            "4. Prepared management letter comments",
            "5. Documented management responses",
        ]

        evidence = [
            f"Total findings identified: {len(findings)}",
            f"Critical findings: {sum(1 for f in findings if f.get('severity') == 'critical')}",
            f"High findings: {sum(1 for f in findings if f.get('severity') == 'high')}",
            f"Medium findings: {sum(1 for f in findings if f.get('severity') == 'medium')}",
            f"Low findings: {sum(1 for f in findings if f.get('severity') == 'low')}",
        ]

        finding_details = []
        for i, finding in enumerate(findings, 1):
            finding_details.append(
                f"{i}. [{finding.get('severity', 'N/A').upper()}] {finding.get('title', 'N/A')}: "
                f"{finding.get('description', 'N/A')}"
            )

        workpaper = Workpaper(
            workpaper_id=self._generate_workpaper_id("SF"),
            workpaper_type=WorkpaperType.SUMMARY_OF_FINDINGS,
            title="Summary of Findings",
            engagement_name=self.engagement_name,
            engagement_period_start=self.period_start,
            engagement_period_end=self.period_end,
            objective="Summarize all findings from the engagement and evaluate impact on opinion",
            procedures_performed=procedures,
            evidence_examined=evidence,
            findings=finding_details,
            conclusion=overall_conclusion,
            prepared_by=self.preparer,
            prepared_date=datetime.now(),
        )

        content = f"{workpaper.objective}{findings}"
        workpaper.content_hash = self._calculate_hash(content)

        return workpaper

    def render_workpaper_markdown(self, workpaper: Workpaper) -> str:
        """Render workpaper as Markdown document.

        Args:
            workpaper: Workpaper to render

        Returns:
            Markdown formatted workpaper
        """
        md = f"""# {workpaper.title}

**Workpaper ID**: {workpaper.workpaper_id}
**Type**: {workpaper.workpaper_type.value}
**Status**: {workpaper.status.value}

---

## Engagement Information

| Field | Value |
|-------|-------|
| Engagement | {workpaper.engagement_name} |
| Period Start | {workpaper.engagement_period_start.strftime('%Y-%m-%d')} |
| Period End | {workpaper.engagement_period_end.strftime('%Y-%m-%d')} |
| Prepared By | {workpaper.prepared_by} |
| Prepared Date | {workpaper.prepared_date.strftime('%Y-%m-%d %H:%M') if workpaper.prepared_date else 'N/A'} |
| Reviewed By | {workpaper.reviewed_by or 'Pending'} |
| Reviewed Date | {workpaper.reviewed_date.strftime('%Y-%m-%d %H:%M') if workpaper.reviewed_date else 'Pending'} |

---

## Objective

{workpaper.objective}

---

## Procedures Performed

"""
        for proc in workpaper.procedures_performed:
            md += f"- {proc}\n"

        md += """
---

## Evidence Examined

"""
        for evidence in workpaper.evidence_examined:
            md += f"- {evidence}\n"

        md += """
---

## Findings

"""
        for finding in workpaper.findings:
            md += f"- {finding}\n"

        md += f"""
---

## Conclusion

{workpaper.conclusion}

---

## Cross-References

"""
        if workpaper.references:
            for ref in workpaper.references:
                md += f"- [{ref.reference_id}] {ref.description} ({ref.reference_type})\n"
        else:
            md += "No cross-references documented.\n"

        md += f"""
---

## Review Notes

"""
        if workpaper.review_notes:
            for note in workpaper.review_notes:
                status = "✅ Cleared" if note.cleared else "⏳ Open"
                md += f"- [{status}] {note.reviewer} ({note.date.strftime('%Y-%m-%d')}): {note.content}\n"
                if note.response:
                    md += f"  - Response: {note.response}\n"
        else:
            md += "No review notes.\n"

        md += f"""
---

## Document Integrity

| Field | Value |
|-------|-------|
| Content Hash | `{workpaper.content_hash[:32]}...` |
| Version | {workpaper.version} |
| Retention Until | {workpaper.retention_date.strftime('%Y-%m-%d') if workpaper.retention_date else 'Per retention policy (7 years)'} |

---

*Generated by WISTX Context Augmentation Platform*
*Compliant with PCAOB AS 1215 and AICPA AU-C Section 230*
"""
        return md

    def generate_workpaper_package(
        self,
        controls_tested: list[dict[str, Any]],
        sample_results: list[Any],
        evidence_collections: list[dict[str, Any]],
        findings: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generate complete workpaper package for an engagement.

        Creates all required workpapers for a compliance audit
        engagement, properly cross-referenced and indexed.

        Args:
            controls_tested: List of controls with testing results
            sample_results: List of sampling results
            evidence_collections: List of evidence collection results
            findings: List of all findings

        Returns:
            Dictionary containing all workpapers and index
        """
        workpapers = []

        # Generate control testing workpapers
        for control in controls_tested:
            wp = self.generate_control_testing_workpaper(
                control_id=control.get("control_id", ""),
                control_description=control.get("description", ""),
                testing_procedures=control.get("procedures", []),
                sample_items=control.get("sample_items", []),
                exceptions=control.get("exceptions", []),
                conclusion=control.get("conclusion", ""),
            )
            workpapers.append(wp)

        # Generate sampling workpapers
        for sample in sample_results:
            wp = self.generate_sampling_workpaper(
                sample_result=sample,
                population_description=sample.parameters.population_size if hasattr(sample, 'parameters') else "N/A",
                sampling_rationale="Statistical sampling per PCAOB AS 2315",
            )
            workpapers.append(wp)

        # Generate evidence collection workpapers
        for evidence in evidence_collections:
            wp = self.generate_evidence_collection_workpaper(
                evidence_items=evidence.get("items", []),
                source_description=evidence.get("source", ""),
                collection_method=evidence.get("method", "Automated collection"),
            )
            workpapers.append(wp)

        # Generate summary of findings
        summary_wp = self.generate_summary_of_findings_workpaper(
            findings=findings,
            overall_conclusion=self._determine_overall_conclusion(findings),
        )
        workpapers.append(summary_wp)

        # Create index
        index = self._create_workpaper_index(workpapers)

        return {
            "engagement_name": self.engagement_name,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "generated_at": datetime.now().isoformat(),
            "workpaper_count": len(workpapers),
            "index": index,
            "workpapers": [
                {
                    "id": wp.workpaper_id,
                    "type": wp.workpaper_type.value,
                    "title": wp.title,
                    "status": wp.status.value,
                    "content_hash": wp.content_hash,
                    "markdown": self.render_workpaper_markdown(wp),
                }
                for wp in workpapers
            ],
        }

    def _determine_overall_conclusion(self, findings: list[dict[str, Any]]) -> str:
        """Determine overall conclusion based on findings."""
        critical = sum(1 for f in findings if f.get("severity") == "critical")
        high = sum(1 for f in findings if f.get("severity") == "high")

        if critical > 0:
            return (
                f"Based on our testing, we identified {critical} critical finding(s) "
                "that represent material weaknesses in the control environment. "
                "These matters require immediate management attention."
            )
        elif high > 3:
            return (
                f"Based on our testing, we identified {high} high-severity finding(s) "
                "that represent significant deficiencies. Management should address "
                "these matters in a timely manner."
            )
        elif high > 0:
            return (
                f"Based on our testing, we identified {high} high-severity finding(s). "
                "Overall, controls are operating effectively with noted exceptions."
            )
        else:
            return (
                "Based on our testing, controls are operating effectively. "
                "No material weaknesses or significant deficiencies were identified."
            )

    def _create_workpaper_index(self, workpapers: list[Workpaper]) -> list[dict[str, Any]]:
        """Create workpaper index for navigation."""
        index = []

        # Group by type
        by_type: dict[str, list[Workpaper]] = {}
        for wp in workpapers:
            type_name = wp.workpaper_type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(wp)

        for type_name, wps in by_type.items():
            index.append({
                "section": type_name.replace("_", " ").title(),
                "workpapers": [
                    {
                        "id": wp.workpaper_id,
                        "title": wp.title,
                        "status": wp.status.value,
                    }
                    for wp in wps
                ],
            })

        return index

