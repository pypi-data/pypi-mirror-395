"""Cross-Framework Control Mapping for WISTX.

This module provides intelligent mapping between compliance frameworks, enabling:
- Single control implementations to satisfy multiple framework requirements
- Reduced audit redundancy for multi-framework compliance
- Gap analysis for framework expansion
- Unified control catalog with canonical IDs

Mappings are based on authoritative sources:
- NIST Cybersecurity Framework mappings
- Cloud Security Alliance (CSA) CCM to SOC 2 mappings
- PCI DSS to ISO 27001 mappings from PCI Security Standards Council
- HIPAA to NIST 800-53 mappings from HHS
"""

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ControlMapping:
    """Represents a mapping between control frameworks."""
    source_framework: str
    source_control_id: str
    target_framework: str
    target_control_ids: list[str]
    mapping_type: str  # "equivalent", "partial", "related"
    confidence: float  # 0.0 to 1.0
    notes: str = ""


@dataclass
class UnifiedControl:
    """Canonical representation of a control across frameworks."""
    canonical_id: str
    title: str
    description: str
    category: str
    framework_mappings: dict[str, list[str]] = field(default_factory=dict)
    severity: str = "MEDIUM"
    implementation_guidance: str = ""


class CrossFrameworkMapper:
    """Maps controls across compliance frameworks.
    
    This mapper enables organizations to:
    1. Identify which controls satisfy multiple frameworks
    2. Prioritize high-value controls that cover multiple requirements
    3. Reduce audit evidence collection by reusing across frameworks
    4. Plan framework expansions based on existing coverage
    """

    # Core control categories that map across all frameworks
    UNIVERSAL_CATEGORIES = {
        "access_control": "Access Management & Authentication",
        "data_protection": "Data Protection & Encryption",
        "network_security": "Network Security & Segmentation",
        "logging_monitoring": "Logging, Monitoring & Audit Trails",
        "incident_response": "Incident Response & Recovery",
        "vulnerability_management": "Vulnerability & Patch Management",
        "change_management": "Change Management & Configuration",
        "asset_management": "Asset Inventory & Classification",
        "risk_management": "Risk Assessment & Treatment",
        "security_awareness": "Security Awareness & Training",
    }

    # Cross-framework mappings based on authoritative sources
    # Format: {category: {framework: [control_ids]}}
    FRAMEWORK_MAPPINGS: dict[str, dict[str, list[str]]] = {
        "access_control": {
            "SOC2": ["CC6.1", "CC6.2", "CC6.3"],
            "PCI-DSS": ["7.1", "7.2", "8.1", "8.2", "8.3"],
            "HIPAA": ["164.312(a)(1)", "164.312(d)"],
            "ISO-27001": ["A.9.1", "A.9.2", "A.9.4"],
            "NIST-800-53": ["AC-1", "AC-2", "AC-3", "AC-6", "IA-1", "IA-2"],
            "CIS-AWS": ["1.1", "1.2", "1.3", "1.4", "1.5"],
            "GDPR": ["Article 32(1)(b)"],
            "FedRAMP": ["AC-1", "AC-2", "AC-3", "AC-6", "IA-1", "IA-2"],
            "CCPA": ["1798.100(d)", "1798.150"],
            "SOX": ["SOX-302", "SOX-404"],
            "GLBA": ["314.4(b)(1)", "314.4(c)"],
        },
        "data_protection": {
            "SOC2": ["CC6.7", "CC9.1"],
            "PCI-DSS": ["3.1", "3.2", "3.4", "3.5", "4.1"],
            "HIPAA": ["164.312(a)(2)(iv)", "164.312(e)(1)", "164.312(e)(2)"],
            "ISO-27001": ["A.8.2", "A.10.1", "A.13.2"],
            "NIST-800-53": ["SC-8", "SC-12", "SC-13", "SC-28"],
            "CIS-AWS": ["2.1", "2.2", "2.3"],
            "GDPR": ["Article 32(1)(a)", "Article 25"],
            "FedRAMP": ["SC-8", "SC-12", "SC-13", "SC-28"],
            "CCPA": ["1798.100(e)", "1798.130"],
            "SOX": ["SOX-404-ITGC"],
            "GLBA": ["314.4(b)(3)", "314.4(c)(1)"],
        },
        "network_security": {
            "SOC2": ["CC6.6", "CC7.1"],
            "PCI-DSS": ["1.1", "1.2", "1.3", "1.4", "2.1"],
            "HIPAA": ["164.312(e)(1)"],
            "ISO-27001": ["A.13.1", "A.13.2"],
            "NIST-800-53": ["SC-7", "SC-8", "AC-4"],
            "CIS-AWS": ["4.1", "4.2", "4.3", "5.1", "5.2"],
            "GDPR": ["Article 32(1)(a)"],
            "FedRAMP": ["SC-7", "SC-8", "AC-4"],
            "SOX": ["SOX-404-ITGC"],
            "GLBA": ["314.4(b)(2)"],
        },
        "logging_monitoring": {
            "SOC2": ["CC4.1", "CC4.2", "CC7.2", "CC7.3"],
            "PCI-DSS": ["10.1", "10.2", "10.3", "10.5", "10.6", "10.7"],
            "HIPAA": ["164.312(b)"],
            "ISO-27001": ["A.12.4", "A.16.1"],
            "NIST-800-53": ["AU-1", "AU-2", "AU-3", "AU-6", "AU-12"],
            "CIS-AWS": ["3.1", "3.2", "3.3", "3.4", "3.5"],
            "GDPR": ["Article 30", "Article 33"],
            "FedRAMP": ["AU-1", "AU-2", "AU-3", "AU-6", "AU-12"],
            "SOX": ["SOX-404-ITGC", "SOX-302"],
            "GLBA": ["314.4(b)(3)"],
        },
        "incident_response": {
            "SOC2": ["CC7.4", "CC7.5", "CC9.2"],
            "PCI-DSS": ["12.10"],
            "HIPAA": ["164.308(a)(6)"],
            "ISO-27001": ["A.16.1", "A.17.1"],
            "NIST-800-53": ["IR-1", "IR-2", "IR-4", "IR-5", "IR-6", "IR-8"],
            "CIS-AWS": ["3.14"],
            "GDPR": ["Article 33", "Article 34"],
            "FedRAMP": ["IR-1", "IR-2", "IR-4", "IR-5", "IR-6", "IR-8"],
            "CCPA": ["1798.150"],
            "GLBA": ["314.4(b)(3)", "314.4(e)"],
        },
        "vulnerability_management": {
            "SOC2": ["CC7.1", "CC8.1"],
            "PCI-DSS": ["5.1", "5.2", "6.1", "6.2", "11.2", "11.3"],
            "HIPAA": ["164.308(a)(1)(ii)(B)"],
            "ISO-27001": ["A.12.6", "A.14.2"],
            "NIST-800-53": ["RA-5", "SI-2", "SI-5"],
            "CIS-AWS": ["2.4", "2.5"],
            "GDPR": ["Article 32(1)(d)"],
            "FedRAMP": ["RA-5", "SI-2", "SI-5"],
            "SOX": ["SOX-404-ITGC"],
            "GLBA": ["314.4(b)(2)"],
        },
        "change_management": {
            "SOC2": ["CC8.1"],
            "PCI-DSS": ["6.4", "6.5"],
            "HIPAA": ["164.308(a)(8)"],
            "ISO-27001": ["A.12.1", "A.14.2"],
            "NIST-800-53": ["CM-1", "CM-2", "CM-3", "CM-4"],
            "CIS-AWS": ["1.20", "1.21"],
            "GDPR": ["Article 32(1)(d)"],
            "FedRAMP": ["CM-1", "CM-2", "CM-3", "CM-4"],
            "SOX": ["SOX-404-ITGC"],
            "GLBA": ["314.4(b)(1)"],
        },
        "privacy_rights": {
            "GDPR": ["Article 15", "Article 16", "Article 17", "Article 18", "Article 20", "Article 21"],
            "CCPA": ["1798.100", "1798.105", "1798.110", "1798.115", "1798.120", "1798.125"],
            "HIPAA": ["164.524", "164.526", "164.528"],
            "GLBA": ["314.4(d)"],
        },
        "data_retention": {
            "SOC2": ["CC6.5"],
            "PCI-DSS": ["3.1", "9.8"],
            "HIPAA": ["164.530(j)"],
            "ISO-27001": ["A.8.3"],
            "NIST-800-53": ["SI-12"],
            "GDPR": ["Article 5(1)(e)", "Article 17"],
            "CCPA": ["1798.100(d)"],
            "SOX": ["SOX-802"],
            "GLBA": ["314.4(b)(3)"],
        },
        "third_party_risk": {
            "SOC2": ["CC9.2"],
            "PCI-DSS": ["12.8", "12.9"],
            "HIPAA": ["164.308(b)(1)", "164.314"],
            "ISO-27001": ["A.15.1", "A.15.2"],
            "NIST-800-53": ["SA-9", "SA-12"],
            "GDPR": ["Article 28", "Article 29"],
            "FedRAMP": ["SA-9", "SA-12"],
            "SOX": ["SOX-404"],
            "GLBA": ["314.4(d)"],
        },
    }

    @classmethod
    def get_mapped_frameworks(cls, control_id: str, source_framework: str) -> list[ControlMapping]:
        """Find all frameworks that a control maps to.

        Args:
            control_id: The control ID in the source framework
            source_framework: The source framework name

        Returns:
            List of ControlMapping objects showing equivalent controls
        """
        mappings: list[ControlMapping] = []
        
        # Normalize framework name
        source_framework_normalized = cls._normalize_framework_name(source_framework)
        
        # Find the category this control belongs to
        for category, framework_controls in cls.FRAMEWORK_MAPPINGS.items():
            source_controls = framework_controls.get(source_framework_normalized, [])
            
            # Check if control_id matches (partial match for flexibility)
            control_matched = False
            for src_ctrl in source_controls:
                if control_id.upper().startswith(src_ctrl.upper()) or src_ctrl.upper() in control_id.upper():
                    control_matched = True
                    break
            
            if control_matched:
                # Map to all other frameworks in this category
                for target_framework, target_controls in framework_controls.items():
                    if target_framework != source_framework_normalized:
                        mappings.append(ControlMapping(
                            source_framework=source_framework_normalized,
                            source_control_id=control_id,
                            target_framework=target_framework,
                            target_control_ids=target_controls,
                            mapping_type="equivalent",
                            confidence=0.85,
                            notes=f"Mapped via {cls.UNIVERSAL_CATEGORIES[category]} category",
                        ))

        return mappings

    @classmethod
    def get_cross_framework_coverage(
        cls,
        controls: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Analyze cross-framework coverage for a set of controls.

        Args:
            controls: List of compliance controls

        Returns:
            Dictionary with coverage analysis
        """
        framework_coverage: dict[str, set[str]] = {}
        category_coverage: dict[str, set[str]] = {}
        high_value_controls: list[dict[str, Any]] = []

        for control in controls:
            standard = control.get("standard", "Unknown")
            control_id = control.get("control_id", "")

            if standard not in framework_coverage:
                framework_coverage[standard] = set()
            framework_coverage[standard].add(control_id)

            # Find mappings for this control
            mappings = cls.get_mapped_frameworks(control_id, standard)

            if len(mappings) >= 3:  # Maps to 3+ other frameworks
                high_value_controls.append({
                    "control_id": control_id,
                    "standard": standard,
                    "title": control.get("title", ""),
                    "maps_to_frameworks": len(mappings),
                    "framework_list": [m.target_framework for m in mappings],
                })

            # Track category coverage
            for category, framework_controls in cls.FRAMEWORK_MAPPINGS.items():
                normalized_standard = cls._normalize_framework_name(standard)
                if normalized_standard in framework_controls:
                    if category not in category_coverage:
                        category_coverage[category] = set()
                    category_coverage[category].add(standard)

        # Calculate coverage metrics
        total_frameworks = len(framework_coverage)
        categories_covered = len(category_coverage)

        return {
            "frameworks_assessed": list(framework_coverage.keys()),
            "total_frameworks": total_frameworks,
            "categories_covered": categories_covered,
            "total_categories": len(cls.UNIVERSAL_CATEGORIES),
            "category_coverage_pct": (categories_covered / len(cls.UNIVERSAL_CATEGORIES)) * 100,
            "high_value_controls": sorted(
                high_value_controls,
                key=lambda x: x["maps_to_frameworks"],
                reverse=True
            )[:10],  # Top 10 high-value controls
            "coverage_by_category": {
                cat: {
                    "name": cls.UNIVERSAL_CATEGORIES[cat],
                    "frameworks_covered": list(frameworks),
                }
                for cat, frameworks in category_coverage.items()
            },
        }

    @classmethod
    def generate_cross_framework_markdown(
        cls,
        controls: list[dict[str, Any]],
    ) -> str:
        """Generate markdown showing cross-framework coverage.

        Returns:
            Markdown string with cross-framework analysis
        """
        coverage = cls.get_cross_framework_coverage(controls)

        md = []
        md.append("## Cross-Framework Control Mapping\n\n")
        md.append("This analysis shows how controls map across multiple compliance frameworks, ")
        md.append("enabling efficient multi-framework compliance.\n\n")

        # Coverage summary
        md.append("### Coverage Summary\n\n")
        md.append(f"| Metric | Value |\n")
        md.append(f"|--------|-------|\n")
        md.append(f"| Frameworks Assessed | {coverage['total_frameworks']} |\n")
        md.append(f"| Control Categories Covered | {coverage['categories_covered']}/{coverage['total_categories']} |\n")
        md.append(f"| Category Coverage | {coverage['category_coverage_pct']:.1f}% |\n\n")

        # High-value controls
        if coverage["high_value_controls"]:
            md.append("### High-Value Controls (Multi-Framework Coverage)\n\n")
            md.append("These controls satisfy requirements across multiple frameworks:\n\n")
            md.append("| Control | Framework | Title | Maps To |\n")
            md.append("|---------|-----------|-------|--------|\n")
            for ctrl in coverage["high_value_controls"][:5]:
                frameworks = ", ".join(ctrl["framework_list"][:3])
                if len(ctrl["framework_list"]) > 3:
                    frameworks += f" +{len(ctrl['framework_list']) - 3} more"
                md.append(f"| {ctrl['control_id']} | {ctrl['standard']} | {ctrl['title'][:40]}... | {frameworks} |\n")
            md.append("\n")

        # Category coverage
        md.append("### Coverage by Control Category\n\n")
        for category, data in coverage["coverage_by_category"].items():
            md.append(f"**{data['name']}**: {', '.join(data['frameworks_covered'])}\n\n")

        return "".join(md)

    @classmethod
    def _normalize_framework_name(cls, framework: str) -> str:
        """Normalize framework name for consistent matching."""
        mappings = {
            "soc2": "SOC2",
            "soc-2": "SOC2",
            "soc 2": "SOC2",
            "pci-dss": "PCI-DSS",
            "pci_dss": "PCI-DSS",
            "pci dss": "PCI-DSS",
            "hipaa": "HIPAA",
            "iso-27001": "ISO-27001",
            "iso27001": "ISO-27001",
            "iso 27001": "ISO-27001",
            "nist-800-53": "NIST-800-53",
            "nist800-53": "NIST-800-53",
            "nist 800-53": "NIST-800-53",
            "cis-aws": "CIS-AWS",
            "cis aws": "CIS-AWS",
            "cis": "CIS-AWS",
            "gdpr": "GDPR",
            "fedramp": "FedRAMP",
            "fed-ramp": "FedRAMP",
            "fed ramp": "FedRAMP",
            "ccpa": "CCPA",
            "cpra": "CCPA",
            "sox": "SOX",
            "sarbanes-oxley": "SOX",
            "glba": "GLBA",
            "gramm-leach-bliley": "GLBA",
        }
        return mappings.get(framework.lower(), framework.upper())

