"""Document generator for creating documentation and reports."""

import logging
import re
from datetime import datetime
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


class DocumentGenerator:
    """Generator for various types of documentation."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize document generator.

        Args:
            mongodb_client: MongoDB client for knowledge base access
        """
        self.mongodb_client = mongodb_client
        self.vector_search = VectorSearch(
            mongodb_client,
            gemini_api_key=settings.gemini_api_key,
        )

    async def generate_architecture_doc(
        self,
        subject: str,
        infrastructure_code: str | None = None,
        configuration: dict[str, Any] | None = None,
        include_compliance: bool = True,
        include_security: bool = True,
    ) -> str:
        """Generate architecture documentation.

        Args:
            subject: Subject name
            infrastructure_code: Infrastructure code
            configuration: Configuration dictionary
            include_compliance: Include compliance information
            include_security: Include security information

        Returns:
            Generated markdown documentation
        """
        markdown = f"# Architecture Documentation: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        markdown += "## Overview\n\n"
        markdown += f"This document describes the architecture for {subject}.\n\n"

        if infrastructure_code:
            markdown += "## Infrastructure Code\n\n"
            markdown += f"```hcl\n{infrastructure_code}\n```\n\n"

        if configuration:
            markdown += "## Configuration\n\n"
            for key, value in configuration.items():
                if isinstance(value, dict):
                    markdown += f"### {key}\n\n"
                    for sub_key, sub_value in value.items():
                        markdown += f"- **{sub_key}**: {sub_value}\n"
                    markdown += "\n"
                else:
                    markdown += f"- **{key}**: {value}\n"
            markdown += "\n"

        if include_security:
            markdown += "## Security Considerations\n\n"
            markdown += "### Security Best Practices\n\n"
            markdown += "- Implement least privilege access\n"
            markdown += "- Enable encryption at rest and in transit\n"
            markdown += "- Regular security audits\n"
            markdown += "- Monitor for security events\n"
            markdown += "- Keep dependencies updated\n\n"

        if include_compliance:
            markdown += "## Compliance\n\n"
            markdown += "### Compliance Standards\n\n"
            markdown += "- Review compliance requirements\n"
            markdown += "- Implement compliance controls\n"
            markdown += "- Regular compliance audits\n\n"

        markdown += "## Architecture Components\n\n"
        markdown += "### Components\n\n"
        markdown += "- Application layer\n"
        markdown += "- Data layer\n"
        markdown += "- Network layer\n"
        markdown += "- Security layer\n\n"

        return markdown

    async def generate_runbook(
        self,
        subject: str,
        operations: list[str] | None = None,
        troubleshooting: list[str] | None = None,
    ) -> str:
        """Generate operational runbook.

        Args:
            subject: Subject name
            operations: List of operations
            troubleshooting: List of troubleshooting steps

        Returns:
            Generated markdown runbook
        """
        markdown = f"# Runbook: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        markdown += "## Operations\n\n"
        if operations:
            for i, op in enumerate(operations, 1):
                markdown += f"### {i}. {op}\n\n"
                markdown += "**Steps**:\n"
                markdown += "1. Verify prerequisites\n"
                markdown += "2. Execute operation\n"
                markdown += "3. Verify success\n\n"
        else:
            markdown += "### Standard Operations\n\n"
            markdown += "1. Monitor system health\n"
            markdown += "2. Check logs for errors\n"
            markdown += "3. Verify resource status\n"
            markdown += "4. Review monitoring metrics\n\n"

        markdown += "## Troubleshooting\n\n"
        if troubleshooting:
            for i, step in enumerate(troubleshooting, 1):
                markdown += f"{i}. {step}\n"
        else:
            markdown += "1. Check error logs\n"
            markdown += "2. Verify configuration\n"
            markdown += "3. Check resource status\n"
            markdown += "4. Review monitoring metrics\n"
            markdown += "5. Check network connectivity\n\n"

        markdown += "## Emergency Procedures\n\n"
        markdown += "### Incident Response\n\n"
        markdown += "1. Identify the issue\n"
        markdown += "2. Assess impact\n"
        markdown += "3. Implement fix\n"
        markdown += "4. Verify resolution\n"
        markdown += "5. Document incident\n\n"

        return markdown

    async def _fetch_compliance_data(
        self,
        resource_types: list[str],
        standards: list[str] | None = None,
        resource_ids: list[str] | None = None,
        cloud_provider: str | list[str] | None = None,
    ) -> dict[str, Any]:
        """Fetch compliance data as structured dictionary.

        This method extracts the shared logic for fetching compliance data,
        ensuring consistency between template and non-template report generation.

        Args:
            resource_types: List of resource types (will be normalized)
            standards: List of compliance standards
            resource_ids: List of specific indexed resource IDs (optional)
            cloud_provider: Cloud provider for normalization

        Returns:
            Dictionary with 'controls' key containing list of ALL compliance controls
            and 'summary' key with summary information
        """
        from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_types

        normalized_resource_types = normalize_resource_types(resource_types or [], cloud_provider)

        try:
            compliance_results = await with_timeout_and_retry(
                api_client.get_compliance_requirements,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                resource_types=normalized_resource_types,
                standards=standards or [],
            )
        except ValueError as e:
            error_msg = str(e)
            if "Invalid resource types" in error_msg or "Invalid request parameters" in error_msg:
                logger.warning(
                    "Failed to fetch compliance requirements due to invalid resource types: %s. "
                    "Original resource types: %s, Normalized: %s. "
                    "Attempting to filter out invalid types and retry.",
                    error_msg,
                    resource_types,
                    normalized_resource_types,
                )
                invalid_types_match = re.search(r"Invalid resource types: \[(.*?)\]", error_msg)
                if invalid_types_match:
                    invalid_types_str = invalid_types_match.group(1)
                    invalid_types = [t.strip().strip("'\"") for t in invalid_types_str.split(",")]
                    filtered_types = [rt for rt in normalized_resource_types if rt not in invalid_types]
                    if filtered_types:
                        logger.info(
                            "Retrying with filtered resource types: %s (removed: %s)",
                            filtered_types,
                            invalid_types,
                        )
                        compliance_results = await with_timeout_and_retry(
                            api_client.get_compliance_requirements,
                            timeout_seconds=30.0,
                            max_attempts=2,
                            retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                            resource_types=filtered_types,
                            standards=standards or [],
                        )
                    else:
                        logger.error(
                            "All resource types were invalid. Cannot generate compliance report."
                        )
                        raise ValueError(
                            f"All resource types are invalid: {invalid_types}. "
                            "Please check resource type names."
                        ) from e
                else:
                    raise ValueError(
                        f"Invalid resource types in request: {error_msg}"
                    ) from e
            else:
                raise

        controls = []
        if "controls" in compliance_results:
            controls = compliance_results["controls"]
        elif "data" in compliance_results and isinstance(compliance_results["data"], dict):
            controls = compliance_results["data"].get("controls", [])

        if not isinstance(controls, list):
            logger.warning("Controls is not a list: %s", type(controls))
            controls = []

        return {
            "controls": controls,
            "summary": compliance_results.get("summary", {}),
        }

    async def _map_controls_to_resources(
        self,
        controls: list[dict[str, Any]],
        resource_ids: list[str] | None,
        resource_types: list[str] | None,
        cloud_provider: str | list[str] | None,
        selected_resources_info: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Map compliance controls to resources and create summaries.

        This is the shared resource-mapping logic used by both template and
        non-template compliance report paths. It ensures consistent, resource-aware
        reports regardless of which path is taken.

        Args:
            controls: List of compliance controls
            resource_ids: List of specific indexed resource IDs (optional)
            resource_types: List of resource types
            cloud_provider: Cloud provider name
            selected_resources_info: Pre-fetched resource information (optional)

        Returns:
            Dictionary containing:
            - resource_list: List of resources being assessed
            - resource_compliance_summary: Per-resource compliance stats
            - requirements_with_resources: Controls mapped to resources
        """
        from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_type

        def _normalize_resource_name(resource_name: str) -> str:
            """Normalize resource name for matching."""
            normalized = normalize_resource_type(resource_name, cloud_provider)
            return normalized

        def _resource_matches_control(resource_name: str, applies_to: list[str]) -> bool:
            """Check if resource matches control's applies_to list."""
            if not applies_to:
                return True

            normalized_resource = _normalize_resource_name(resource_name)
            normalized_resource_key = normalized_resource.upper().replace(" ", "").replace("_", "").replace("-", "")

            for pattern in applies_to:
                if not pattern or not isinstance(pattern, str):
                    continue

                normalized_pattern = _normalize_resource_name(pattern)
                normalized_pattern_key = normalized_pattern.upper().replace(" ", "").replace("_", "").replace("-", "")

                if normalized_pattern_key == "*" or normalized_pattern_key == "GENERIC":
                    return True

                if normalized_resource_key == normalized_pattern_key:
                    return True

                if normalized_resource_key in normalized_pattern_key or normalized_pattern_key in normalized_resource_key:
                    return True

                if normalized_resource == normalized_pattern:
                    return True

                if pattern.upper() in resource_name.upper() or resource_name.upper() in pattern.upper():
                    return True
            return False

        # Build resource list from selected resources or resource types
        resource_list = (
            [{"resource_id": r.get("resource_id"), "name": r.get("name"), "type": r.get("resource_type")} for r in selected_resources_info]
            if selected_resources_info
            else [{"type": rt, "name": rt} for rt in resource_types or []]
        )

        # Initialize resource-control mappings
        resource_control_mappings: dict[str, list[dict[str, Any]]] = {}
        for resource in resource_list:
            resource_name = resource.get("name") or resource.get("type", "")
            resource_key = f"{resource.get('type', '')}:{resource_name}"
            resource_control_mappings[resource_key] = []

        # Map controls to resources
        requirements_with_resources = []
        for i, control in enumerate(controls):
            applies_to = control.get("applies_to", [])
            if not isinstance(applies_to, list):
                applies_to = []

            applicable_resources = []
            for resource in resource_list:
                resource_name = resource.get("name") or resource.get("type", "")
                if _resource_matches_control(resource_name, applies_to):
                    applicable_resources.append({
                        "resource_id": resource.get("resource_id"),
                        "name": resource_name,
                        "type": resource.get("type", ""),
                        "status": "assessed",
                    })

            if not applicable_resources and resource_list:
                applicable_resources = [{
                    "name": resource.get("name") or resource.get("type", ""),
                    "type": resource.get("type", ""),
                    "status": "assessed",
                } for resource in resource_list[:1]]

            requirement = {
                "number": i + 1,
                "standard": control.get("standard", ""),
                "control_id": control.get("control_id", ""),
                "title": control.get("title", ""),
                "severity": control.get("severity", "MEDIUM"),
                "description": control.get("description", ""),
                "status": "assessed",
                "remediation": self._transform_remediation(control.get("remediation")),
                "findings": [],
                "applies_to_resources": applicable_resources,
            }
            requirements_with_resources.append(requirement)

            for resource in applicable_resources:
                resource_key = f"{resource.get('type', '')}:{resource.get('name', '')}"
                if resource_key not in resource_control_mappings:
                    resource_control_mappings[resource_key] = []
                resource_control_mappings[resource_key].append({
                    "control_id": control.get("control_id", ""),
                    "title": control.get("title", ""),
                    "severity": control.get("severity", "MEDIUM"),
                    "status": "assessed",
                    "standard": control.get("standard", ""),
                })

        # Create per-resource compliance summary
        resource_compliance_summary = []
        for resource in resource_list:
            resource_name = resource.get("name") or resource.get("type", "")
            resource_key = f"{resource.get('type', '')}:{resource_name}"
            controls_for_resource = resource_control_mappings.get(resource_key, [])
            resource_compliance_summary.append({
                "resource_id": resource.get("resource_id"),
                "name": resource_name,
                "type": resource.get("type", ""),
                "total_controls": len(controls_for_resource),
                "critical_controls": sum(1 for c in controls_for_resource if c.get("severity") == "CRITICAL"),
                "high_controls": sum(1 for c in controls_for_resource if c.get("severity") == "HIGH"),
                "medium_controls": sum(1 for c in controls_for_resource if c.get("severity") == "MEDIUM"),
                "low_controls": sum(1 for c in controls_for_resource if c.get("severity") == "LOW"),
                "controls": controls_for_resource,
            })

        return {
            "resource_list": resource_list,
            "resource_compliance_summary": resource_compliance_summary,
            "requirements_with_resources": requirements_with_resources,
        }

    def _transform_remediation(self, remediation: dict[str, Any] | None) -> str:
        """Transform remediation dict to string format.

        Args:
            remediation: Remediation dictionary or None

        Returns:
            Formatted remediation string
        """
        if not remediation:
            return ""
        if isinstance(remediation, str):
            return remediation

        guidance = remediation.get("guidance", "")
        steps = remediation.get("steps", [])

        if guidance and steps:
            steps_text = "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
            return f"{guidance}\n\nSteps:\n{steps_text}"
        elif guidance:
            return guidance
        elif steps:
            return "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
        else:
            return ""

    async def generate_compliance_report(
        self,
        subject: str,
        resource_types: list[str],
        standards: list[str] | None = None,
        resource_ids: list[str] | None = None,
        cloud_provider: str | list[str] | None = None,
    ) -> str:
        """Generate compliance report.

        Args:
            subject: Subject name
            resource_types: List of resource types
            standards: List of compliance standards
            resource_ids: List of specific indexed resource IDs (optional)

        Returns:
            Generated markdown compliance report
        """
        markdown = f"# Compliance Report: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        markdown += "## Executive Summary\n\n"
        markdown += f"This report assesses compliance for {subject}.\n\n"

        markdown += f"## Resources Assessed\n\n"
        if resource_ids:
            markdown += f"**Selected Resources**: {len(resource_ids)} indexed resource(s)\n\n"
        if resource_types:
            for resource_type in resource_types:
                markdown += f"- {resource_type}\n"
        markdown += "\n"

        markdown += f"## Compliance Standards\n\n"
        if standards:
            for standard in standards:
                markdown += f"- {standard}\n"
        else:
            markdown += "- Review applicable compliance standards\n"
        markdown += "\n"

        try:
            compliance_data = await self._fetch_compliance_data(
                resource_types=resource_types,
                standards=standards,
                resource_ids=resource_ids,
                cloud_provider=cloud_provider,
            )

            controls = compliance_data.get("controls", [])

            # Fetch selected resources from MongoDB if resource_ids provided
            selected_resources_info = None
            if resource_ids:
                try:
                    if self.mongodb_client.database is None:
                        await self.mongodb_client.connect()
                    db = self.mongodb_client.database
                    if db:
                        collection = db["indexed_resources"]
                        cursor = collection.find({"resource_id": {"$in": resource_ids}})
                        selected_resources_info = await cursor.to_list(length=None)
                except Exception as e:
                    logger.warning("Failed to fetch selected resources: %s", e)

            # Use shared resource-mapping logic
            mapping_data = await self._map_controls_to_resources(
                controls=controls,
                resource_ids=resource_ids,
                resource_types=resource_types,
                cloud_provider=cloud_provider,
                selected_resources_info=selected_resources_info,
            )

            resource_list = mapping_data["resource_list"]
            resource_compliance_summary = mapping_data["resource_compliance_summary"]
            requirements_with_resources = mapping_data["requirements_with_resources"]

            # Build resource-aware markdown report
            markdown += "## Resource Compliance Summary\n\n"
            for resource_summary in resource_compliance_summary:
                markdown += f"### {resource_summary['name']} ({resource_summary['type']})\n\n"
                markdown += f"**Total Controls**: {resource_summary['total_controls']}\n"
                markdown += f"- **CRITICAL**: {resource_summary['critical_controls']}\n"
                markdown += f"- **HIGH**: {resource_summary['high_controls']}\n"
                markdown += f"- **MEDIUM**: {resource_summary['medium_controls']}\n"
                markdown += f"- **LOW**: {resource_summary['low_controls']}\n\n"

                if resource_summary['controls']:
                    markdown += "**Applicable Controls**:\n"
                    for control in resource_summary['controls']:
                        markdown += f"- **{control['control_id']}** ({control['severity']}): {control['title']}\n"
                    markdown += "\n"
                markdown += "---\n\n"

            markdown += "## Compliance Controls\n\n"
            markdown += f"**Total Controls**: {len(controls)}\n\n"

            severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for control in controls:
                severity = control.get("severity", "MEDIUM")
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

            markdown += "### Severity Breakdown\n\n"
            for severity, count in severity_counts.items():
                if count > 0:
                    markdown += f"- **{severity}**: {count}\n"
            markdown += "\n"

            markdown += "### Controls by Resource\n\n"
            for requirement in requirements_with_resources[:20]:
                markdown += f"#### {requirement['standard']} {requirement['control_id']}: {requirement['title']}\n\n"
                markdown += f"**Severity**: {requirement['severity']}\n\n"
                markdown += f"{requirement['description']}\n\n"

                if requirement['applies_to_resources']:
                    markdown += "**Applies To Resources**:\n"
                    for resource in requirement['applies_to_resources']:
                        markdown += f"- **{resource['type']}**: {resource['name']} (Status: {resource['status']})\n"
                    markdown += "\n"

                if requirement['remediation']:
                    markdown += f"**Remediation**: {requirement['remediation']}\n\n"

                markdown += "---\n\n"

        except Exception as e:
            logger.warning("Failed to generate compliance report: %s", e)
            markdown += "## Compliance Assessment\n\n"
            markdown += "Unable to generate compliance report. Please check resource types and standards.\n\n"

        return markdown

    async def _map_security_findings_to_resources(
        self,
        findings: list[dict[str, Any]],
        resource_ids: list[str] | None,
        resource_types: list[str] | None,
        cloud_provider: str | list[str] | None,
        selected_resources_info: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Map security findings to resources and create summaries.

        This is the shared security-mapping logic used by both template and
        non-template security report paths. It ensures consistent, resource-aware
        security reports regardless of which path is taken.

        Args:
            findings: List of security findings/vulnerabilities
            resource_ids: List of specific indexed resource IDs (optional)
            resource_types: List of resource types
            cloud_provider: Cloud provider name
            selected_resources_info: Pre-fetched resource information (optional)

        Returns:
            Dictionary containing:
            - resource_list: List of resources being assessed
            - resource_security_summary: Per-resource security stats
            - findings_with_resources: Findings mapped to resources
        """
        from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_type

        def _normalize_resource_name(resource_name: str) -> str:
            """Normalize resource name for matching."""
            normalized = normalize_resource_type(resource_name, cloud_provider)
            return normalized

        def _finding_applies_to_resource(resource_name: str, finding: dict[str, Any]) -> bool:
            """Check if security finding applies to resource."""
            # Check if finding has resource_type field
            finding_resource_type = finding.get("resource_type")
            if not finding_resource_type:
                return True  # Generic finding applies to all resources

            normalized_resource = _normalize_resource_name(resource_name)
            normalized_resource_key = normalized_resource.upper().replace(" ", "").replace("_", "").replace("-", "")

            normalized_finding = _normalize_resource_name(finding_resource_type)
            normalized_finding_key = normalized_finding.upper().replace(" ", "").replace("_", "").replace("-", "")

            if normalized_finding_key == "*" or normalized_finding_key == "GENERIC":
                return True

            if normalized_resource_key == normalized_finding_key:
                return True

            if normalized_resource_key in normalized_finding_key or normalized_finding_key in normalized_resource_key:
                return True

            if normalized_resource == normalized_finding:
                return True

            if finding_resource_type.upper() in resource_name.upper() or resource_name.upper() in finding_resource_type.upper():
                return True

            return False

        # Build resource list
        resource_list = (
            [{"resource_id": r.get("resource_id"), "name": r.get("name"), "type": r.get("resource_type")} for r in selected_resources_info]
            if selected_resources_info
            else [{"type": rt, "name": rt} for rt in resource_types or []]
        )

        # Initialize resource-finding mappings
        resource_finding_mappings: dict[str, list[dict[str, Any]]] = {}
        for resource in resource_list:
            resource_name = resource.get("name") or resource.get("type", "")
            resource_key = f"{resource.get('type', '')}:{resource_name}"
            resource_finding_mappings[resource_key] = []

        # Map findings to resources
        findings_with_resources = []
        for i, finding in enumerate(findings):
            applicable_resources = []
            for resource in resource_list:
                resource_name = resource.get("name") or resource.get("type", "")
                if _finding_applies_to_resource(resource_name, finding):
                    applicable_resources.append({
                        "resource_id": resource.get("resource_id"),
                        "name": resource_name,
                        "type": resource.get("type", ""),
                        "status": "assessed",
                    })

            if not applicable_resources and resource_list:
                applicable_resources = [{
                    "name": resource.get("name") or resource.get("type", ""),
                    "type": resource.get("type", ""),
                    "status": "assessed",
                } for resource in resource_list[:1]]

            finding_record = {
                "number": i + 1,
                "finding_id": finding.get("cve_id") or finding.get("id", f"finding_{i}"),
                "title": finding.get("title", ""),
                "severity": finding.get("severity", "MEDIUM"),
                "description": finding.get("description", ""),
                "source": finding.get("source", "unknown"),
                "status": "identified",
                "applies_to_resources": applicable_resources,
                "references": finding.get("references", []),
                "published_date": finding.get("published_date", ""),
            }
            findings_with_resources.append(finding_record)

            for resource in applicable_resources:
                resource_key = f"{resource.get('type', '')}:{resource.get('name', '')}"
                if resource_key not in resource_finding_mappings:
                    resource_finding_mappings[resource_key] = []
                resource_finding_mappings[resource_key].append({
                    "finding_id": finding.get("cve_id") or finding.get("id", f"finding_{i}"),
                    "title": finding.get("title", ""),
                    "severity": finding.get("severity", "MEDIUM"),
                    "status": "identified",
                    "source": finding.get("source", "unknown"),
                })

        # Create per-resource security summary
        resource_security_summary = []
        for resource in resource_list:
            resource_name = resource.get("name") or resource.get("type", "")
            resource_key = f"{resource.get('type', '')}:{resource_name}"
            findings_for_resource = resource_finding_mappings.get(resource_key, [])
            resource_security_summary.append({
                "resource_id": resource.get("resource_id"),
                "name": resource_name,
                "type": resource.get("type", ""),
                "total_findings": len(findings_for_resource),
                "critical_findings": sum(1 for f in findings_for_resource if f.get("severity") == "CRITICAL"),
                "high_findings": sum(1 for f in findings_for_resource if f.get("severity") == "HIGH"),
                "medium_findings": sum(1 for f in findings_for_resource if f.get("severity") == "MEDIUM"),
                "low_findings": sum(1 for f in findings_for_resource if f.get("severity") == "LOW"),
                "findings": findings_for_resource,
            })

        return {
            "resource_list": resource_list,
            "resource_security_summary": resource_security_summary,
            "findings_with_resources": findings_with_resources,
        }

    async def generate_security_report(
        self,
        subject: str,
        resource_types: list[str] | None = None,
        cloud_provider: str | list[str] | None = None,
        resource_ids: list[str] | None = None,
    ) -> str:
        """Generate security report.

        Args:
            subject: Subject name
            resource_types: List of resource types
            cloud_provider: Cloud provider
            resource_ids: List of specific indexed resource IDs (optional)

        Returns:
            Generated markdown security report
        """
        markdown = f"# Security Report: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        markdown += "## Executive Summary\n\n"
        markdown += f"This report assesses security posture for {subject}.\n\n"

        try:
            # Fetch security findings from SecurityClient
            from wistx_mcp.tools.lib.security_client import SecurityClient

            security_client = SecurityClient(self.mongodb_client)
            findings = []

            # Search for CVEs related to resource types
            if resource_types:
                for resource_type in resource_types:
                    try:
                        cves = await security_client.search_cves(
                            query=resource_type,
                            resource_type=resource_type,
                            limit=10,
                        )
                        findings.extend(cves)
                    except Exception as e:
                        logger.warning("Failed to fetch CVEs for %s: %s", resource_type, e)

            # Search for advisories
            if cloud_provider:
                try:
                    advisories = await security_client.search_advisories(
                        query=f"{subject} security",
                        cloud_provider=str(cloud_provider) if isinstance(cloud_provider, str) else None,
                        limit=10,
                    )
                    findings.extend(advisories)
                except Exception as e:
                    logger.warning("Failed to fetch advisories: %s", e)

            # Fetch selected resources from MongoDB if resource_ids provided
            selected_resources_info = None
            if resource_ids:
                try:
                    if self.mongodb_client.database is None:
                        await self.mongodb_client.connect()
                    db = self.mongodb_client.database
                    if db:
                        collection = db["indexed_resources"]
                        cursor = collection.find({"resource_id": {"$in": resource_ids}})
                        selected_resources_info = await cursor.to_list(length=None)
                except Exception as e:
                    logger.warning("Failed to fetch selected resources: %s", e)

            # Use shared security-mapping logic
            if findings:
                mapping_data = await self._map_security_findings_to_resources(
                    findings=findings,
                    resource_ids=resource_ids,
                    resource_types=resource_types,
                    cloud_provider=cloud_provider,
                    selected_resources_info=selected_resources_info,
                )

                resource_list = mapping_data["resource_list"]
                resource_security_summary = mapping_data["resource_security_summary"]
                findings_with_resources = mapping_data["findings_with_resources"]

                # Build resource-aware security markdown report
                markdown += "## Resource Security Summary\n\n"
                for resource_summary in resource_security_summary:
                    markdown += f"### {resource_summary['name']} ({resource_summary['type']})\n\n"
                    markdown += f"**Total Findings**: {resource_summary['total_findings']}\n"
                    markdown += f"- **CRITICAL**: {resource_summary['critical_findings']}\n"
                    markdown += f"- **HIGH**: {resource_summary['high_findings']}\n"
                    markdown += f"- **MEDIUM**: {resource_summary['medium_findings']}\n"
                    markdown += f"- **LOW**: {resource_summary['low_findings']}\n\n"

                    if resource_summary['findings']:
                        markdown += "**Security Findings**:\n"
                        for finding in resource_summary['findings']:
                            markdown += f"- **{finding['finding_id']}** ({finding['severity']}): {finding['title']}\n"
                        markdown += "\n"
                    markdown += "---\n\n"

                markdown += "## Security Findings\n\n"
                markdown += f"**Total Findings**: {len(findings)}\n\n"

                severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
                for finding in findings:
                    severity = finding.get("severity", "MEDIUM")
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1

                markdown += "### Severity Breakdown\n\n"
                for severity, count in severity_counts.items():
                    if count > 0:
                        markdown += f"- **{severity}**: {count}\n"
                markdown += "\n"

                markdown += "### Findings by Resource\n\n"
                for finding in findings_with_resources[:20]:
                    markdown += f"#### {finding['finding_id']}: {finding['title']}\n\n"
                    markdown += f"**Severity**: {finding['severity']}\n"
                    markdown += f"**Source**: {finding['source']}\n\n"
                    markdown += f"{finding['description']}\n\n"

                    if finding['applies_to_resources']:
                        markdown += "**Affects Resources**:\n"
                        for resource in finding['applies_to_resources']:
                            markdown += f"- **{resource['type']}**: {resource['name']} (Status: {resource['status']})\n"
                        markdown += "\n"

                    if finding['references']:
                        markdown += "**References**:\n"
                        for ref in finding['references'][:3]:
                            markdown += f"- {ref}\n"
                        markdown += "\n"

                    markdown += "---\n\n"
            else:
                # Fallback to generic security report if no findings
                markdown += "## Security Assessment\n\n"
                markdown += "### Security Best Practices\n\n"
                markdown += "- Enable encryption at rest and in transit\n"
                markdown += "- Implement least privilege access\n"
                markdown += "- Regular security audits\n"
                markdown += "- Monitor for security events\n"
                markdown += "- Keep dependencies updated\n"
                markdown += "- Implement network segmentation\n"
                markdown += "- Use security groups and firewalls\n\n"

                if resource_types:
                    markdown += "## Resource-Specific Security\n\n"
                    for resource_type in resource_types:
                        markdown += f"### {resource_type}\n\n"
                        markdown += "- Review security configurations\n"
                        markdown += "- Check access controls\n"
                        markdown += "- Verify encryption settings\n"
                        markdown += "- Review audit logs\n\n"

        except Exception as e:
            logger.warning("Failed to generate resource-aware security report: %s", e)
            markdown += "## Security Assessment\n\n"
            markdown += "### Security Best Practices\n\n"
            markdown += "- Enable encryption at rest and in transit\n"
            markdown += "- Implement least privilege access\n"
            markdown += "- Regular security audits\n"
            markdown += "- Monitor for security events\n"
            markdown += "- Keep dependencies updated\n"
            markdown += "- Implement network segmentation\n"
            markdown += "- Use security groups and firewalls\n\n"

        if cloud_provider:
            markdown += f"## {str(cloud_provider).upper()} Security\n\n"
            markdown += f"- Review {cloud_provider} security best practices\n"
            markdown += f"- Check {cloud_provider} security groups\n"
            markdown += f"- Verify {cloud_provider} IAM policies\n\n"

        markdown += "## Recommendations\n\n"
        markdown += "1. Implement security monitoring\n"
        markdown += "2. Regular security audits\n"
        markdown += "3. Keep security configurations updated\n"
        markdown += "4. Review access controls regularly\n\n"

        return markdown

    async def _map_costs_to_resources(
        self,
        cost_breakdown: list[dict[str, Any]],
        resource_ids: list[str] | None,
        resource_types: list[str] | None,
        cloud_provider: str | list[str] | None,
        selected_resources_info: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Map cost breakdown to resources and create summaries.

        This is the shared cost-mapping logic used for resource-aware cost reports.
        It ensures consistent, resource-specific cost analysis.

        Args:
            cost_breakdown: List of cost breakdown items
            resource_ids: List of specific indexed resource IDs (optional)
            resource_types: List of resource types
            cloud_provider: Cloud provider name
            selected_resources_info: Pre-fetched resource information (optional)

        Returns:
            Dictionary containing:
            - resource_list: List of resources being assessed
            - resource_cost_summary: Per-resource cost stats
            - costs_with_resources: Costs mapped to resources
        """
        from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_type

        def _normalize_resource_name(resource_name: str) -> str:
            """Normalize resource name for matching."""
            normalized = normalize_resource_type(resource_name, cloud_provider)
            return normalized

        def _cost_applies_to_resource(resource_name: str, cost_item: dict[str, Any]) -> bool:
            """Check if cost item applies to resource."""
            # Parse resource identifier (format: cloud:service:instance_type)
            resource_identifier = cost_item.get("resource", "")
            if not resource_identifier:
                return True

            parts = resource_identifier.split(":")
            if len(parts) < 2:
                return True

            service = parts[1] if len(parts) > 1 else ""
            if not service:
                return True

            normalized_resource = _normalize_resource_name(resource_name)
            normalized_resource_key = normalized_resource.upper().replace(" ", "").replace("_", "").replace("-", "")

            normalized_service = _normalize_resource_name(service)
            normalized_service_key = normalized_service.upper().replace(" ", "").replace("_", "").replace("-", "")

            if normalized_service_key == "*" or normalized_service_key == "GENERIC":
                return True

            if normalized_resource_key == normalized_service_key:
                return True

            if normalized_resource_key in normalized_service_key or normalized_service_key in normalized_resource_key:
                return True

            if normalized_resource == normalized_service:
                return True

            if service.upper() in resource_name.upper() or resource_name.upper() in service.upper():
                return True

            return False

        # Build resource list
        resource_list = (
            [{"resource_id": r.get("resource_id"), "name": r.get("name"), "type": r.get("resource_type")} for r in selected_resources_info]
            if selected_resources_info
            else [{"type": rt, "name": rt} for rt in resource_types or []]
        )

        # Initialize resource-cost mappings
        resource_cost_mappings: dict[str, list[dict[str, Any]]] = {}
        for resource in resource_list:
            resource_name = resource.get("name") or resource.get("type", "")
            resource_key = f"{resource.get('type', '')}:{resource_name}"
            resource_cost_mappings[resource_key] = []

        # Map costs to resources
        costs_with_resources = []
        for i, cost_item in enumerate(cost_breakdown):
            applicable_resources = []
            for resource in resource_list:
                resource_name = resource.get("name") or resource.get("type", "")
                if _cost_applies_to_resource(resource_name, cost_item):
                    applicable_resources.append({
                        "resource_id": resource.get("resource_id"),
                        "name": resource_name,
                        "type": resource.get("type", ""),
                        "status": "active",
                    })

            if not applicable_resources and resource_list:
                applicable_resources = [{
                    "name": resource.get("name") or resource.get("type", ""),
                    "type": resource.get("type", ""),
                    "status": "active",
                } for resource in resource_list[:1]]

            cost_record = {
                "number": i + 1,
                "resource": cost_item.get("resource", ""),
                "quantity": cost_item.get("quantity", 1),
                "monthly": cost_item.get("monthly", 0.0),
                "annual": cost_item.get("annual", 0.0),
                "region": cost_item.get("region"),
                "pricing_category": cost_item.get("pricing_category", "OnDemand"),
                "applies_to_resources": applicable_resources,
            }
            costs_with_resources.append(cost_record)

            for resource in applicable_resources:
                resource_key = f"{resource.get('type', '')}:{resource.get('name', '')}"
                if resource_key not in resource_cost_mappings:
                    resource_cost_mappings[resource_key] = []
                resource_cost_mappings[resource_key].append({
                    "resource": cost_item.get("resource", ""),
                    "quantity": cost_item.get("quantity", 1),
                    "monthly": cost_item.get("monthly", 0.0),
                    "annual": cost_item.get("annual", 0.0),
                    "pricing_category": cost_item.get("pricing_category", "OnDemand"),
                })

        # Create per-resource cost summary
        resource_cost_summary = []
        for resource in resource_list:
            resource_name = resource.get("name") or resource.get("type", "")
            resource_key = f"{resource.get('type', '')}:{resource_name}"
            costs_for_resource = resource_cost_mappings.get(resource_key, [])

            total_monthly = sum(c.get("monthly", 0.0) for c in costs_for_resource)
            total_annual = sum(c.get("annual", 0.0) for c in costs_for_resource)

            resource_cost_summary.append({
                "resource_id": resource.get("resource_id"),
                "name": resource_name,
                "type": resource.get("type", ""),
                "total_monthly": round(total_monthly, 2),
                "total_annual": round(total_annual, 2),
                "item_count": len(costs_for_resource),
                "costs": costs_for_resource,
            })

        return {
            "resource_list": resource_list,
            "resource_cost_summary": resource_cost_summary,
            "costs_with_resources": costs_with_resources,
        }

    async def generate_cost_report(
        self,
        subject: str,
        resources: list[dict[str, Any]] | None = None,
        resource_ids: list[str] | None = None,
        cloud_provider: str | list[str] | None = None,
    ) -> str:
        """Generate cost report.

        Args:
            subject: Subject name
            resources: List of resource specifications
            resource_ids: List of specific indexed resource IDs (optional)
            cloud_provider: Cloud provider name

        Returns:
            Generated markdown cost report
        """
        markdown = f"# Cost Report: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        markdown += "## Executive Summary\n\n"
        markdown += f"This report provides cost analysis for {subject}.\n\n"

        if resources:
            try:
                from wistx_mcp.tools import pricing
                cost_results = await with_timeout_and_retry(
                    pricing.calculate_infrastructure_cost,
                    timeout_seconds=30.0,
                    max_attempts=3,
                    retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                    resources=resources,
                )

                total_monthly = cost_results.get("total_monthly", 0)
                total_annual = cost_results.get("total_annual", 0)

                markdown += f"## Cost Summary\n\n"
                markdown += f"**Monthly Cost**: ${total_monthly:.2f}\n\n"
                markdown += f"**Annual Cost**: ${total_annual:.2f}\n\n"

                breakdown = cost_results.get("breakdown", [])

                # Fetch selected resources from MongoDB if resource_ids provided
                selected_resources_info = None
                resource_types = None
                if resource_ids:
                    try:
                        if self.mongodb_client.database is None:
                            await self.mongodb_client.connect()
                        db = self.mongodb_client.database
                        if db:
                            collection = db["indexed_resources"]
                            cursor = collection.find({"resource_id": {"$in": resource_ids}})
                            selected_resources_info = await cursor.to_list(length=None)
                            # Extract resource types from selected resources
                            resource_types = list(set(r.get("resource_type") for r in selected_resources_info if r.get("resource_type")))
                    except Exception as e:
                        logger.warning("Failed to fetch selected resources: %s", e)

                # Use shared cost-mapping logic if we have resources
                if breakdown and (selected_resources_info or resource_types):
                    mapping_data = await self._map_costs_to_resources(
                        cost_breakdown=breakdown,
                        resource_ids=resource_ids,
                        resource_types=resource_types,
                        cloud_provider=cloud_provider,
                        selected_resources_info=selected_resources_info,
                    )

                    resource_cost_summary = mapping_data["resource_cost_summary"]

                    # Build resource-aware cost markdown report
                    markdown += "## Resource Cost Summary\n\n"
                    for resource_summary in resource_cost_summary:
                        markdown += f"### {resource_summary['name']} ({resource_summary['type']})\n\n"
                        markdown += f"**Monthly Cost**: ${resource_summary['total_monthly']:.2f}\n"
                        markdown += f"**Annual Cost**: ${resource_summary['total_annual']:.2f}\n"
                        markdown += f"**Items**: {resource_summary['item_count']}\n\n"

                        if resource_summary['costs']:
                            markdown += "**Cost Breakdown**:\n"
                            for cost in resource_summary['costs']:
                                markdown += f"- {cost['resource']}: ${cost['monthly']:.2f}/month (${cost['annual']:.2f}/year)\n"
                            markdown += "\n"
                        markdown += "---\n\n"

                if breakdown:
                    markdown += "## Detailed Cost Breakdown\n\n"
                    markdown += "| Resource | Quantity | Monthly | Annual | Category |\n"
                    markdown += "|----------|----------|---------|--------|----------|\n"
                    for item in breakdown:
                        category = item.get("pricing_category", "OnDemand")
                        markdown += f"| {item['resource']} | {item['quantity']} | "
                        markdown += f"${item['monthly']:.2f} | ${item['annual']:.2f} | {category} |\n"
                    markdown += "\n"

                optimizations = cost_results.get("optimizations", [])
                if optimizations:
                    markdown += "## Optimization Suggestions\n\n"
                    for opt in optimizations:
                        markdown += f"- {opt}\n"
                    markdown += "\n"

                # Add cost optimization recommendations
                markdown += "## Cost Optimization Recommendations\n\n"
                if total_monthly > 1000:
                    markdown += "- **Reserved Instances**: Consider purchasing 1-year or 3-year reserved instances for 30-40% savings\n"
                if total_monthly > 500:
                    markdown += "- **Spot Instances**: Use spot instances for non-critical workloads to reduce costs by 70-90%\n"
                markdown += "- **Right-sizing**: Review instance types and consider downsizing over-provisioned resources\n"
                markdown += "- **Auto-scaling**: Implement auto-scaling policies to match demand\n"
                markdown += "- **Storage Optimization**: Archive old data and use cheaper storage tiers\n\n"

            except Exception as e:
                logger.warning("Failed to generate cost report: %s", e)
                markdown += "## Cost Analysis\n\n"
                markdown += "Unable to generate cost report. Please provide resource specifications.\n\n"
        else:
            markdown += "## Cost Analysis\n\n"
            markdown += "No resource specifications provided.\n\n"
            markdown += "### Cost Estimation Guidelines\n\n"
            markdown += "1. Identify all resources\n"
            markdown += "2. Estimate usage patterns\n"
            markdown += "3. Calculate monthly costs\n"
            markdown += "4. Plan for scaling\n\n"

        return markdown

    async def generate_api_documentation(
        self,
        subject: str,
        api_spec: dict[str, Any] | None = None,
    ) -> str:
        """Generate API documentation.

        Args:
            subject: API name
            api_spec: API specification dictionary

        Returns:
            Generated markdown API documentation
        """
        markdown = f"# API Documentation: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        markdown += "## Overview\n\n"
        markdown += f"This document describes the API for {subject}.\n\n"

        if api_spec:
            markdown += "## Endpoints\n\n"
            endpoints = api_spec.get("endpoints", [])
            for endpoint in endpoints:
                method = endpoint.get("method", "GET")
                path = endpoint.get("path", "")
                markdown += f"### {method} {path}\n\n"
                markdown += f"{endpoint.get('description', '')}\n\n"
        else:
            markdown += "## API Endpoints\n\n"
            markdown += "### Endpoints\n\n"
            markdown += "- List endpoints\n"
            markdown += "- Document request/response formats\n"
            markdown += "- Include authentication requirements\n\n"

        markdown += "## Authentication\n\n"
        markdown += "API authentication requirements.\n\n"

        markdown += "## Examples\n\n"
        markdown += "### Request Example\n\n"
        markdown += "```json\n{}\n```\n\n"

        markdown += "### Response Example\n\n"
        markdown += "```json\n{}\n```\n\n"

        return markdown

    async def generate_deployment_guide(
        self,
        subject: str,
        infrastructure_type: str | None = None,
        cloud_provider: str | list[str] | None = None,
        include_compliance: bool = True,
        include_security: bool = True,
        include_cost: bool = True,
        include_best_practices: bool = True,
        api_key: str = "",
    ) -> str:
        """Generate comprehensive deployment guide with research-backed content.

        Args:
            subject: Subject name (e.g., "On-Premises to Multi-Cloud Migration")
            infrastructure_type: Infrastructure type (terraform, kubernetes, etc.)
            cloud_provider: Cloud provider(s) (aws, gcp, azure, etc.)
            include_compliance: Include compliance considerations
            include_security: Include security considerations
            include_cost: Include cost optimization guidance
            include_best_practices: Include best practices and patterns
            api_key: API key for research operations

        Returns:
            Generated markdown deployment guide with comprehensive content
        """
        markdown = f"# Deployment Guide: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        research_results = {}
        knowledge_articles = []

        try:
            research_queries = self._build_research_queries(subject, cloud_provider)
            
            for query_info in research_queries:
                try:
                    articles = await self.vector_search.search_knowledge_articles(
                        query=query_info["query"],
                        domains=query_info.get("domains"),
                        content_types=query_info.get("content_types", ["guide", "pattern", "best_practice", "strategy"]),
                        limit=20,
                    )
                    knowledge_articles.extend(articles)
                except Exception as e:
                    logger.warning("Failed to search knowledge articles for query '%s': %s", query_info["query"], e)

            if api_key:
                try:
                    from wistx_mcp.tools import mcp_tools
                    research_result = await mcp_tools.research_knowledge_base(
                        query=f"{subject} deployment migration strategies patterns best practices",
                        domains=["devops", "infrastructure", "architecture"],
                        include_web_search=True,
                        format="structured",
                        max_results=50,
                        api_key=api_key,
                    )
                    research_results = research_result
                except Exception as e:
                    logger.warning("Failed to research knowledge base: %s", e)

        except Exception as e:
            logger.warning("Error during knowledge research: %s", e)

        markdown += "## Executive Summary\n\n"
        research_summary = research_results.get("research_summary", "")
        if research_summary:
            markdown += f"{research_summary}\n\n"
        else:
            markdown += f"This guide provides comprehensive deployment instructions for {subject}.\n\n"
        
        if knowledge_articles:
            markdown += f"**Knowledge Base**: This guide incorporates insights from {len(knowledge_articles)} knowledge articles and best practices.\n\n"

        markdown += "## Prerequisites\n\n"
        markdown += self._generate_prerequisites_section(
            subject, infrastructure_type, cloud_provider, knowledge_articles
        )

        markdown += "## Migration Strategy and Patterns\n\n"
        markdown += self._generate_migration_strategies_section(
            subject, cloud_provider, research_results, knowledge_articles
        )

        markdown += "## Deployment Steps\n\n"
        markdown += self._generate_deployment_steps_section(
            subject, infrastructure_type, cloud_provider, knowledge_articles
        )

        if include_cost:
            markdown += "## Cost Optimization\n\n"
            markdown += self._generate_cost_optimization_section(
                subject, cloud_provider, research_results, knowledge_articles
            )

        if include_security:
            markdown += "## Security Considerations\n\n"
            markdown += self._generate_security_section(
                subject, cloud_provider, research_results, knowledge_articles
            )

        if include_compliance:
            markdown += "## Compliance Considerations\n\n"
            markdown += self._generate_compliance_section(
                subject, cloud_provider, research_results, knowledge_articles
            )

        markdown += "## Disaster Recovery Planning\n\n"
        markdown += self._generate_disaster_recovery_section(
            subject, cloud_provider, research_results, knowledge_articles
        )

        markdown += "## Monitoring and Observability\n\n"
        markdown += self._generate_monitoring_section(
            subject, cloud_provider, research_results, knowledge_articles
        )

        markdown += "## CI/CD Pipeline Modernization\n\n"
        markdown += self._generate_cicd_section(
            subject, cloud_provider, research_results, knowledge_articles
        )

        if include_best_practices:
            markdown += "## Best Practices and Common Pitfalls\n\n"
            markdown += self._generate_best_practices_section(
                subject, cloud_provider, research_results, knowledge_articles
            )

        markdown += "## Team Training and Change Management\n\n"
        markdown += self._generate_training_section(
            subject, research_results, knowledge_articles
        )

        markdown += "## Rollback Procedures\n\n"
        markdown += self._generate_rollback_section(
            subject, infrastructure_type, cloud_provider, knowledge_articles
        )

        markdown += "## References and Additional Resources\n\n"
        markdown += self._generate_references_section(knowledge_articles, research_results)

        return markdown

    def _build_research_queries(
        self, subject: str, cloud_provider: str | list[str] | None
    ) -> list[dict[str, Any]]:
        """Build research queries based on subject and cloud provider.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)

        Returns:
            List of query dictionaries with query, domains, and content_types
        """
        queries = []
        
        base_query = subject.lower()
        providers = []
        if cloud_provider:
            if isinstance(cloud_provider, list):
                providers = cloud_provider
            else:
                providers = [cloud_provider]
        
        provider_str = " ".join(providers) if providers else ""
        
        queries.append({
            "query": f"{base_query} migration strategies patterns",
            "domains": ["devops", "infrastructure", "architecture"],
            "content_types": ["guide", "pattern", "strategy"],
        })
        
        queries.append({
            "query": f"{base_query} cost optimization FinOps {provider_str}",
            "domains": ["finops", "infrastructure"],
            "content_types": ["guide", "best_practice"],
        })
        
        queries.append({
            "query": f"{base_query} security compliance {provider_str}",
            "domains": ["security", "compliance"],
            "content_types": ["guide", "best_practice", "reference"],
        })
        
        queries.append({
            "query": f"{base_query} disaster recovery backup failover {provider_str}",
            "domains": ["infrastructure", "devops"],
            "content_types": ["guide", "strategy", "pattern"],
        })
        
        queries.append({
            "query": f"{base_query} monitoring observability {provider_str}",
            "domains": ["devops", "infrastructure"],
            "content_types": ["guide", "best_practice"],
        })
        
        queries.append({
            "query": f"{base_query} CI/CD pipeline {provider_str}",
            "domains": ["devops"],
            "content_types": ["guide", "pattern", "best_practice"],
        })
        
        return queries

    def _generate_prerequisites_section(
        self,
        subject: str,
        infrastructure_type: str | None,
        cloud_provider: str | list[str] | None,
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate prerequisites section.

        Args:
            subject: Deployment guide subject
            infrastructure_type: Infrastructure type
            cloud_provider: Cloud provider(s)
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for prerequisites section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if "prerequisite" in a.get("title", "").lower() or "requirement" in a.get("title", "").lower()
        ]
        
        content += "### Required Tools and Access\n\n"
        content += "- Cloud provider accounts with appropriate permissions\n"
        if isinstance(cloud_provider, list):
            for provider in cloud_provider:
                content += f"- {provider.upper()} CLI and SDK installed\n"
        elif cloud_provider:
            content += f"- {cloud_provider.upper()} CLI and SDK installed\n"
        else:
            content += "- Cloud provider CLI tools installed\n"
        
        if infrastructure_type == "terraform":
            content += "- Terraform >= 1.0 installed\n"
            content += "- Terraform state backend configured\n"
        elif infrastructure_type == "kubernetes":
            content += "- kubectl configured\n"
            content += "- Helm (if using Helm charts)\n"
        
        content += "- Git for version control\n"
        content += "- CI/CD platform access (GitHub Actions, GitLab CI, etc.)\n\n"
        
        content += "### Configuration Files\n\n"
        content += "- Environment-specific configuration files\n"
        content += "- Secrets management system configured\n"
        content += "- Network configuration documented\n"
        content += "- Resource naming conventions defined\n\n"
        
        content += "### Credentials and Permissions\n\n"
        content += "- Service accounts with least privilege access\n"
        content += "- API keys securely stored\n"
        content += "- IAM roles and policies configured\n"
        content += "- Multi-factor authentication enabled\n\n"
        
        if relevant_articles:
            content += "### Additional Prerequisites\n\n"
            for article in relevant_articles[:3]:
                summary = article.get("summary", "")
                if summary:
                    content += f"- {summary[:200]}\n"
            content += "\n"
        
        return content

    def _generate_migration_strategies_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate migration strategies section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for migration strategies section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["migration", "strategy", "pattern"])
        ]
        
        research_summary = research_results.get("research_summary", "")
        if research_summary:
            content += f"{research_summary}\n\n"
        
        content += "### Migration Patterns\n\n"
        content += "1. **Lift and Shift (Rehost)**: Move applications as-is to cloud\n"
        content += "   - Fastest migration approach\n"
        content += "   - Minimal application changes required\n"
        content += "   - Best for: Legacy applications, time-constrained migrations\n\n"
        
        content += "2. **Replatform (Lift, Tinker, and Shift)**: Optimize applications for cloud\n"
        content += "   - Moderate changes to leverage cloud services\n"
        content += "   - Improved performance and cost efficiency\n"
        content += "   - Best for: Applications with cloud-native potential\n\n"
        
        content += "3. **Refactor (Re-architect)**: Redesign for cloud-native architecture\n"
        content += "   - Maximum cloud benefits\n"
        content += "   - Microservices, serverless, containers\n"
        content += "   - Best for: Strategic applications, long-term goals\n\n"
        
        content += "4. **Hybrid Approach**: Combination of patterns\n"
        content += "   - Phased migration strategy\n"
        content += "   - Risk mitigation through gradual transition\n"
        content += "   - Best for: Complex environments, multi-phase projects\n\n"
        
        if isinstance(cloud_provider, list) and len(cloud_provider) > 1:
            content += "### Multi-Cloud Considerations\n\n"
            content += "- **Vendor Lock-in Mitigation**: Distribute workloads across providers\n"
            content += "- **Resilience**: Avoid single points of failure\n"
            content += "- **Cost Optimization**: Leverage best pricing from each provider\n"
            content += "- **Compliance**: Meet region-specific requirements\n"
            content += "- **Network Architecture**: Plan for cross-cloud connectivity\n\n"
        
        if relevant_articles:
            content += "### Additional Strategies\n\n"
            for article in relevant_articles[:5]:
                title = article.get("title", "")
                summary = article.get("summary", "")
                if title and summary:
                    content += f"#### {title}\n\n"
                    content += f"{summary[:300]}\n\n"
        
        return content

    def _generate_deployment_steps_section(
        self,
        subject: str,
        infrastructure_type: str | None,
        cloud_provider: str | list[str] | None,
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate deployment steps section.

        Args:
            subject: Deployment guide subject
            infrastructure_type: Infrastructure type
            cloud_provider: Cloud provider(s)
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for deployment steps section
        """
        content = ""
        
        content += "### Phase 1: Assessment and Planning\n\n"
        content += "1. **Inventory Current Infrastructure**\n"
        content += "   - Document all applications and dependencies\n"
        content += "   - Map network topology and data flows\n"
        content += "   - Identify critical systems and SLAs\n\n"
        
        content += "2. **Define Migration Goals**\n"
        content += "   - Establish success criteria\n"
        content += "   - Set timelines and milestones\n"
        content += "   - Allocate resources and budget\n\n"
        
        content += "3. **Risk Assessment**\n"
        content += "   - Identify potential risks and mitigation strategies\n"
        content += "   - Plan for business continuity\n"
        content += "   - Establish rollback procedures\n\n"
        
        content += "### Phase 2: Infrastructure Setup\n\n"
        
        if infrastructure_type == "terraform":
            content += "```bash\n"
            content += "# Initialize Terraform\n"
            content += "terraform init\n\n"
            content += "# Review planned changes\n"
            content += "terraform plan -out=tfplan\n\n"
            content += "# Apply infrastructure changes\n"
            content += "terraform apply tfplan\n\n"
            content += "# Verify deployment\n"
            content += "terraform output\n"
            content += "```\n\n"
        elif infrastructure_type == "kubernetes":
            content += "```bash\n"
            content += "# Apply Kubernetes manifests\n"
            content += "kubectl apply -f manifests/\n\n"
            content += "# Verify pod status\n"
            content += "kubectl get pods --all-namespaces\n\n"
            content += "# Check service endpoints\n"
            content += "kubectl get svc\n"
            content += "```\n\n"
        else:
            content += "1. **Provision Cloud Resources**\n"
            content += "   - Create VPCs and networking\n"
            content += "   - Set up compute instances\n"
            content += "   - Configure storage and databases\n\n"
        
        content += "2. **Network Configuration**\n"
        if isinstance(cloud_provider, list):
            for provider in cloud_provider:
                if provider.lower() == "aws":
                    content += "   - AWS: Configure VPC, subnets, route tables, security groups\n"
                elif provider.lower() == "gcp":
                    content += "   - GCP: Configure VPC networks, firewall rules, Cloud Router\n"
                elif provider.lower() == "azure":
                    content += "   - Azure: Configure Virtual Networks, Network Security Groups\n"
        else:
            content += "   - Configure virtual networks and subnets\n"
            content += "   - Set up routing and firewall rules\n"
            content += "   - Configure DNS and load balancing\n\n"
        
        content += "### Phase 3: Application Migration\n\n"
        content += "1. **Data Migration**\n"
        content += "   - Plan data transfer strategy\n"
        content += "   - Execute data migration with validation\n"
        content += "   - Verify data integrity\n\n"
        
        content += "2. **Application Deployment**\n"
        content += "   - Deploy applications to target environment\n"
        content += "   - Configure application settings\n"
        content += "   - Update connection strings and endpoints\n\n"
        
        content += "3. **Service Configuration**\n"
        content += "   - Configure load balancers\n"
        content += "   - Set up auto-scaling policies\n"
        content += "   - Configure monitoring and alerting\n\n"
        
        content += "### Phase 4: Testing and Validation\n\n"
        content += "1. **Functional Testing**\n"
        content += "   - Verify application functionality\n"
        content += "   - Test integration points\n"
        content += "   - Validate data consistency\n\n"
        
        content += "2. **Performance Testing**\n"
        content += "   - Load testing\n"
        content += "   - Stress testing\n"
        content += "   - Performance benchmarking\n\n"
        
        content += "3. **Security Testing**\n"
        content += "   - Vulnerability scanning\n"
        content += "   - Penetration testing\n"
        content += "   - Security configuration review\n\n"
        
        content += "### Phase 5: Cutover and Go-Live\n\n"
        content += "1. **Pre-Cutover Checklist**\n"
        content += "   - All tests passed\n"
        content += "   - Monitoring in place\n"
        content += "   - Rollback plan ready\n"
        content += "   - Team briefed and ready\n\n"
        
        content += "2. **Execute Cutover**\n"
        content += "   - Update DNS records\n"
        content += "   - Switch traffic to new environment\n"
        content += "   - Monitor closely for issues\n\n"
        
        content += "3. **Post-Cutover Validation**\n"
        content += "   - Verify all systems operational\n"
        content += "   - Monitor performance metrics\n"
        content += "   - Address any immediate issues\n\n"
        
        return content

    def _generate_cost_optimization_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate cost optimization section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for cost optimization section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["cost", "finops", "optimization", "pricing"])
        ]
        
        content += "### Cost Optimization Strategies\n\n"
        content += "1. **Right-Sizing Resources**\n"
        content += "   - Analyze actual resource utilization\n"
        content += "   - Downsize over-provisioned instances\n"
        content += "   - Use auto-scaling to match demand\n\n"
        
        content += "2. **Reserved Instances and Savings Plans**\n"
        if isinstance(cloud_provider, list):
            for provider in cloud_provider:
                if provider.lower() == "aws":
                    content += "   - AWS: Purchase Reserved Instances (1-3 year terms) for 30-40% savings\n"
                    content += "   - AWS Savings Plans for flexible compute usage\n"
                elif provider.lower() == "gcp":
                    content += "   - GCP: Committed Use Discounts for predictable workloads\n"
                    content += "   - Sustained Use Discounts automatically applied\n"
        else:
            content += "   - Purchase reserved capacity for predictable workloads\n"
            content += "   - Commit to usage for significant discounts\n\n"
        
        content += "3. **Spot Instances and Preemptible VMs**\n"
        content += "   - Use spot/preemptible instances for fault-tolerant workloads\n"
        content += "   - Achieve 70-90% cost savings\n"
        content += "   - Implement proper instance interruption handling\n\n"
        
        content += "4. **Storage Optimization**\n"
        content += "   - Use appropriate storage tiers (hot, warm, cold, archive)\n"
        content += "   - Implement lifecycle policies\n"
        content += "   - Archive old data to cheaper storage\n\n"
        
        content += "5. **Network Cost Optimization**\n"
        content += "   - Minimize data transfer costs\n"
        content += "   - Use CDN for content delivery\n"
        content += "   - Optimize cross-region data transfer\n\n"
        
        if isinstance(cloud_provider, list) and len(cloud_provider) > 1:
            content += "### Multi-Cloud Cost Management\n\n"
            content += "- **Cost Visibility**: Use FinOps tools to track costs across providers\n"
            content += "- **Cost Allocation**: Tag resources for accurate cost attribution\n"
            content += "- **Provider Comparison**: Regularly compare pricing and optimize placement\n"
            content += "- **Cost Governance**: Implement budgets and alerts\n\n"
        
        if relevant_articles:
            content += "### Additional Cost Optimization Tips\n\n"
            for article in relevant_articles[:3]:
                summary = article.get("summary", "")
                if summary:
                    content += f"- {summary[:250]}\n"
            content += "\n"
        
        return content

    def _generate_security_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate security section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for security section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["security", "encryption", "iam", "access"])
        ]
        
        content += "### Security Best Practices\n\n"
        content += "1. **Identity and Access Management (IAM)**\n"
        content += "   - Implement least privilege access\n"
        content += "   - Use role-based access control (RBAC)\n"
        content += "   - Enable multi-factor authentication (MFA)\n"
        content += "   - Regular access reviews and audits\n\n"
        
        content += "2. **Network Security**\n"
        content += "   - Implement network segmentation\n"
        content += "   - Use security groups and firewalls\n"
        content += "   - Enable VPC flow logs\n"
        content += "   - Implement DDoS protection\n\n"
        
        content += "3. **Data Protection**\n"
        content += "   - Encrypt data at rest and in transit\n"
        content += "   - Use managed encryption keys\n"
        content += "   - Implement data classification\n"
        content += "   - Regular backups with encryption\n\n"
        
        content += "4. **Security Monitoring**\n"
        content += "   - Enable cloud provider security services\n"
        if isinstance(cloud_provider, list):
            for provider in cloud_provider:
                if provider.lower() == "aws":
                    content += "   - AWS: CloudTrail, GuardDuty, Security Hub\n"
                elif provider.lower() == "gcp":
                    content += "   - GCP: Cloud Security Command Center, Cloud Armor\n"
                elif provider.lower() == "azure":
                    content += "   - Azure: Security Center, Sentinel\n"
        else:
            content += "   - CloudTrail/audit logging\n"
            content += "   - Threat detection services\n"
            content += "   - Security information and event management (SIEM)\n\n"
        
        content += "5. **Compliance and Governance**\n"
        content += "   - Implement security policies\n"
        content += "   - Regular security assessments\n"
        content += "   - Vulnerability management\n"
        content += "   - Incident response planning\n\n"
        
        if relevant_articles:
            content += "### Additional Security Considerations\n\n"
            for article in relevant_articles[:3]:
                title = article.get("title", "")
                summary = article.get("summary", "")
                if title and summary:
                    content += f"#### {title}\n\n"
                    content += f"{summary[:300]}\n\n"
        
        return content

    def _generate_compliance_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate compliance section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for compliance section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["compliance", "hipaa", "soc2", "pci", "gdpr"])
        ]
        
        content += "### Compliance Standards\n\n"
        content += "Common compliance standards to consider:\n\n"
        content += "- **SOC 2**: Security, availability, processing integrity\n"
        content += "- **HIPAA**: Healthcare data protection\n"
        content += "- **PCI-DSS**: Payment card data security\n"
        content += "- **GDPR**: European data protection\n"
        content += "- **ISO 27001**: Information security management\n"
        content += "- **NIST**: Cybersecurity framework\n\n"
        
        content += "### Compliance Implementation\n\n"
        content += "1. **Data Classification**\n"
        content += "   - Classify data by sensitivity\n"
        content += "   - Apply appropriate controls\n"
        content += "   - Document data handling procedures\n\n"
        
        content += "2. **Access Controls**\n"
        content += "   - Implement role-based access\n"
        content += "   - Regular access reviews\n"
        content += "   - Audit logging and monitoring\n\n"
        
        content += "3. **Data Protection**\n"
        content += "   - Encryption requirements\n"
        content += "   - Data retention policies\n"
        content += "   - Secure data disposal\n\n"
        
        content += "4. **Audit and Monitoring**\n"
        content += "   - Continuous compliance monitoring\n"
        content += "   - Regular compliance assessments\n"
        content += "   - Documentation and reporting\n\n"
        
        if relevant_articles:
            content += "### Compliance Resources\n\n"
            for article in relevant_articles[:3]:
                title = article.get("title", "")
                summary = article.get("summary", "")
                if title and summary:
                    content += f"#### {title}\n\n"
                    content += f"{summary[:300]}\n\n"
        
        return content

    def _generate_disaster_recovery_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate disaster recovery section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for disaster recovery section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["disaster", "recovery", "backup", "failover"])
        ]
        
        content += "### Disaster Recovery Strategies\n\n"
        content += "1. **Backup Strategy**\n"
        content += "   - Regular automated backups\n"
        content += "   - Multi-region backup storage\n"
        content += "   - Test backup restoration procedures\n"
        content += "   - Document RPO (Recovery Point Objective) and RTO (Recovery Time Objective)\n\n"
        
        content += "2. **Replication Strategy**\n"
        if isinstance(cloud_provider, list):
            for provider in cloud_provider:
                if provider.lower() == "aws":
                    content += "   - AWS: Cross-region replication for S3, RDS Multi-AZ\n"
                elif provider.lower() == "gcp":
                    content += "   - GCP: Cross-region replication, Cloud SQL replicas\n"
        else:
            content += "   - Cross-region replication\n"
            content += "   - Database replication\n"
            content += "   - Application state replication\n\n"
        
        content += "3. **Failover Procedures**\n"
        content += "   - Automated failover for critical systems\n"
        content += "   - Manual failover procedures documented\n"
        content += "   - Failover testing schedule\n"
        content += "   - Communication plan for incidents\n\n"
        
        content += "4. **Multi-Cloud Disaster Recovery**\n"
        if isinstance(cloud_provider, list) and len(cloud_provider) > 1:
            content += "   - Distribute workloads across providers\n"
            content += "   - Cross-cloud backup and replication\n"
            content += "   - Provider-agnostic disaster recovery\n"
            content += "   - Test cross-cloud failover procedures\n\n"
        
        if relevant_articles:
            content += "### Additional Disaster Recovery Guidance\n\n"
            for article in relevant_articles[:3]:
                summary = article.get("summary", "")
                if summary:
                    content += f"- {summary[:250]}\n"
            content += "\n"
        
        return content

    def _generate_monitoring_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate monitoring section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for monitoring section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["monitoring", "observability", "logging", "metrics"])
        ]
        
        content += "### Monitoring Stack\n\n"
        if isinstance(cloud_provider, list):
            for provider in cloud_provider:
                if provider.lower() == "aws":
                    content += "**AWS Services**:\n"
                    content += "- CloudWatch for metrics and logs\n"
                    content += "- X-Ray for distributed tracing\n"
                    content += "- CloudTrail for API auditing\n\n"
                elif provider.lower() == "gcp":
                    content += "**GCP Services**:\n"
                    content += "- Cloud Monitoring (formerly Stackdriver)\n"
                    content += "- Cloud Logging\n"
                    content += "- Cloud Trace\n\n"
        else:
            content += "- Cloud provider native monitoring\n"
            content += "- Application performance monitoring (APM)\n"
            content += "- Log aggregation and analysis\n\n"
        
        content += "### Observability Best Practices\n\n"
        content += "1. **Metrics**\n"
        content += "   - Collect infrastructure metrics (CPU, memory, disk, network)\n"
        content += "   - Application metrics (request rate, latency, errors)\n"
        content += "   - Business metrics (user actions, conversions)\n"
        content += "   - Use Prometheus-compatible metrics where possible\n\n"
        
        content += "2. **Logging**\n"
        content += "   - Centralized log aggregation\n"
        content += "   - Structured logging (JSON format)\n"
        content += "   - Log retention policies\n"
        content += "   - Log analysis and alerting\n\n"
        
        content += "3. **Tracing**\n"
        content += "   - Distributed tracing for microservices\n"
        content += "   - Trace sampling strategies\n"
        content += "   - Performance bottleneck identification\n\n"
        
        content += "4. **Alerting**\n"
        content += "   - Define alert thresholds\n"
        content += "   - Set up alert channels (email, Slack, PagerDuty)\n"
        content += "   - Implement alert fatigue prevention\n"
        content += "   - Runbook integration with alerts\n\n"
        
        if relevant_articles:
            content += "### Additional Monitoring Resources\n\n"
            for article in relevant_articles[:3]:
                summary = article.get("summary", "")
                if summary:
                    content += f"- {summary[:250]}\n"
            content += "\n"
        
        return content

    def _generate_cicd_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate CI/CD section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for CI/CD section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["cicd", "pipeline", "deployment", "ci", "cd"])
        ]
        
        content += "### CI/CD Pipeline Modernization\n\n"
        content += "1. **Pipeline Architecture**\n"
        content += "   - Source control integration (Git)\n"
        content += "   - Automated testing (unit, integration, e2e)\n"
        content += "   - Build and artifact management\n"
        content += "   - Deployment automation\n\n"
        
        content += "2. **Multi-Cloud CI/CD**\n"
        if isinstance(cloud_provider, list):
            content += "   - Use provider-agnostic tools (GitHub Actions, GitLab CI)\n"
            content += "   - Terraform for infrastructure provisioning\n"
            content += "   - Cross-cloud deployment pipelines\n"
            content += "   - Unified deployment workflows\n\n"
        else:
            content += "   - Cloud-native CI/CD services\n"
            content += "   - Infrastructure as Code integration\n"
            content += "   - Automated deployment pipelines\n\n"
        
        content += "3. **Best Practices**\n"
        content += "   - Implement GitOps workflows\n"
        content += "   - Use infrastructure as code (IaC)\n"
        content += "   - Blue-green or canary deployments\n"
        content += "   - Automated rollback capabilities\n"
        content += "   - Security scanning in pipeline\n\n"
        
        content += "4. **Tools and Platforms**\n"
        content += "   - GitHub Actions for GitHub repositories\n"
        content += "   - GitLab CI/CD for GitLab projects\n"
        if isinstance(cloud_provider, list):
            for provider in cloud_provider:
                if provider.lower() == "aws":
                    content += "   - AWS CodePipeline, CodeBuild, CodeDeploy\n"
                elif provider.lower() == "gcp":
                    content += "   - GCP Cloud Build, Cloud Deploy\n"
        content += "   - Jenkins for self-hosted CI/CD\n"
        content += "   - ArgoCD for GitOps deployments\n\n"
        
        if relevant_articles:
            content += "### Additional CI/CD Resources\n\n"
            for article in relevant_articles[:3]:
                summary = article.get("summary", "")
                if summary:
                    content += f"- {summary[:250]}\n"
            content += "\n"
        
        return content

    def _generate_best_practices_section(
        self,
        subject: str,
        cloud_provider: str | list[str] | None,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate best practices section.

        Args:
            subject: Deployment guide subject
            cloud_provider: Cloud provider(s)
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for best practices section
        """
        content = ""
        
        relevant_articles = [
            a for a in knowledge_articles
            if any(keyword in a.get("title", "").lower() for keyword in ["best practice", "pattern", "pitfall", "anti-pattern"])
        ]
        
        content += "### Best Practices\n\n"
        content += "1. **Planning and Preparation**\n"
        content += "   - Thorough assessment before migration\n"
        content += "   - Phased migration approach\n"
        content += "   - Clear success criteria and milestones\n"
        content += "   - Comprehensive testing strategy\n\n"
        
        content += "2. **Infrastructure as Code**\n"
        content += "   - Version control all infrastructure\n"
        content += "   - Use Terraform, CloudFormation, or similar\n"
        content += "   - Review and test changes before applying\n"
        content += "   - Document infrastructure decisions\n\n"
        
        content += "3. **Security First**\n"
        content += "   - Implement security from the start\n"
        content += "   - Regular security assessments\n"
        content += "   - Automated security scanning\n"
        content += "   - Incident response plan ready\n\n"
        
        content += "4. **Cost Management**\n"
        content += "   - Monitor costs continuously\n"
        content += "   - Use cost allocation tags\n"
        content += "   - Set up budget alerts\n"
        content += "   - Regular cost optimization reviews\n\n"
        
        content += "### Common Pitfalls to Avoid\n\n"
        content += "1. **Insufficient Planning**\n"
        content += "   - Rushing migration without proper assessment\n"
        content += "   - Underestimating complexity\n"
        content += "   - Lack of rollback planning\n\n"
        
        content += "2. **Security Oversights**\n"
        content += "   - Default security configurations\n"
        content += "   - Overly permissive IAM policies\n"
        content += "   - Neglecting encryption\n"
        content += "   - Insufficient monitoring\n\n"
        
        content += "3. **Cost Overruns**\n"
        content += "   - Not monitoring costs from day one\n"
        content += "   - Over-provisioning resources\n"
        content += "   - Ignoring unused resources\n"
        content += "   - Missing cost optimization opportunities\n\n"
        
        content += "4. **Network and Connectivity Issues**\n"
        content += "   - Inadequate network planning\n"
        content += "   - Latency issues\n"
        content += "   - Bandwidth constraints\n"
        content += "   - DNS configuration errors\n\n"
        
        if relevant_articles:
            content += "### Additional Best Practices\n\n"
            for article in relevant_articles[:5]:
                title = article.get("title", "")
                summary = article.get("summary", "")
                if title and summary:
                    content += f"#### {title}\n\n"
                    content += f"{summary[:300]}\n\n"
        
        return content

    def _generate_training_section(
        self,
        subject: str,
        research_results: dict[str, Any],
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate training section.

        Args:
            subject: Deployment guide subject
            research_results: Research results from knowledge base
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for training section
        """
        content = ""
        
        content += "### Team Training Requirements\n\n"
        content += "1. **Cloud Platform Training**\n"
        content += "   - Provider-specific certifications\n"
        content += "   - Hands-on labs and workshops\n"
        content += "   - Architecture best practices\n"
        content += "   - Cost management training\n\n"
        
        content += "2. **Tooling and Processes**\n"
        content += "   - Infrastructure as Code tools\n"
        content += "   - CI/CD pipeline usage\n"
        content += "   - Monitoring and observability tools\n"
        content += "   - Incident response procedures\n\n"
        
        content += "3. **Security and Compliance**\n"
        content += "   - Security best practices\n"
        content += "   - Compliance requirements\n"
        content += "   - Security incident handling\n"
        content += "   - Access management procedures\n\n"
        
        content += "### Change Management\n\n"
        content += "1. **Communication Plan**\n"
        content += "   - Regular status updates\n"
        content += "   - Stakeholder engagement\n"
        content += "   - Documentation and knowledge sharing\n"
        content += "   - Feedback mechanisms\n\n"
        
        content += "2. **Training Schedule**\n"
        content += "   - Pre-migration training\n"
        content += "   - During migration support\n"
        content += "   - Post-migration optimization\n"
        content += "   - Ongoing education\n\n"
        
        content += "3. **Support Structure**\n"
        content += "   - Designated migration team\n"
        content += "   - Escalation procedures\n"
        content += "   - Knowledge base and documentation\n"
        content += "   - Regular team meetings\n\n"
        
        return content

    def _generate_rollback_section(
        self,
        subject: str,
        infrastructure_type: str | None,
        cloud_provider: str | list[str] | None,
        knowledge_articles: list[dict[str, Any]],
    ) -> str:
        """Generate rollback section.

        Args:
            subject: Deployment guide subject
            infrastructure_type: Infrastructure type
            cloud_provider: Cloud provider(s)
            knowledge_articles: Relevant knowledge articles

        Returns:
            Markdown content for rollback section
        """
        content = ""
        
        content += "### Rollback Procedures\n\n"
        content += "1. **Pre-Rollback Assessment**\n"
        content += "   - Identify rollback trigger conditions\n"
        content += "   - Assess impact of rollback\n"
        content += "   - Verify rollback point availability\n"
        content += "   - Notify stakeholders\n\n"
        
        content += "2. **Execute Rollback**\n"
        if infrastructure_type == "terraform":
            content += "   ```bash\n"
            content += "   # Revert to previous state\n"
            content += "   terraform state list\n"
            content += "   terraform apply -target=<resource> -auto-approve\n"
            content += "   ```\n\n"
        elif infrastructure_type == "kubernetes":
            content += "   ```bash\n"
            content += "   # Rollback deployment\n"
            content += "   kubectl rollout undo deployment/<name>\n"
            content += "   kubectl rollout status deployment/<name>\n"
            content += "   ```\n\n"
        else:
            content += "   - Restore from backup\n"
            content += "   - Revert configuration changes\n"
            content += "   - Switch traffic back to previous environment\n\n"
        
        content += "3. **Post-Rollback Validation**\n"
        content += "   - Verify system functionality\n"
        content += "   - Check data integrity\n"
        content += "   - Monitor system health\n"
        content += "   - Document rollback reason and lessons learned\n\n"
        
        content += "4. **Rollback Communication**\n"
        content += "   - Notify all stakeholders\n"
        content += "   - Document rollback in incident log\n"
        content += "   - Schedule post-mortem meeting\n"
        content += "   - Update runbook with learnings\n\n"
        
        return content

    def _generate_references_section(
        self,
        knowledge_articles: list[dict[str, Any]],
        research_results: dict[str, Any],
    ) -> str:
        """Generate references section.

        Args:
            knowledge_articles: Knowledge articles used
            research_results: Research results

        Returns:
            Markdown content for references section
        """
        content = ""
        
        if knowledge_articles:
            content += "### Knowledge Base Articles\n\n"
            seen_urls = set()
            for article in knowledge_articles[:10]:
                url = article.get("url")
                title = article.get("title", "Untitled")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    content += f"- [{title}]({url})\n"
            content += "\n"
        
        web_results = research_results.get("web_results")
        if web_results:
            content += "### Web Resources\n\n"
            seen_urls = set()
            
            if isinstance(web_results, dict):
                web_results_list = web_results.get("results", [])
            elif isinstance(web_results, list):
                web_results_list = web_results
            else:
                web_results_list = []
            
            for result in web_results_list[:10]:
                if isinstance(result, dict):
                    url = result.get("url")
                    title = result.get("title", "Untitled")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        content += f"- [{title}]({url})\n"
            content += "\n"
        
        return content

    async def generate_project_overview(
        self,
        subject: str,
        resource_ids: list[str] | None = None,
        include_compliance: bool = True,
        include_security: bool = True,
        include_cost: bool = True,
        include_toc: bool = True,
        api_key: str = "",
    ) -> str:
        """Generate a holistic project overview document (CodeWiki-style).

        Combines all sections and components into a comprehensive overview with:
        - Executive summary
        - Table of contents
        - Repository statistics
        - Section summaries with architecture diagrams
        - Aggregated compliance/cost/security analysis
        - Component index

        Args:
            subject: Project/repository name
            resource_ids: List of resource IDs to include
            include_compliance: Include compliance summary
            include_security: Include security summary
            include_cost: Include cost summary
            include_toc: Include table of contents
            api_key: API key for fetching data

        Returns:
            Generated markdown project overview
        """
        from datetime import datetime

        markdown = f"# Project Overview: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        sections_data = []
        cost_data = {}
        compliance_data = {}
        total_components = 0
        languages = set()
        resource_types = set()

        if resource_ids:
            try:
                from api.services.section_organizer import section_organizer
                from api.services.repository_analysis_service import repository_analysis_service

                for resource_id in resource_ids:
                    try:
                        user_id = None
                        from wistx_mcp.tools.lib.auth_context import get_auth_context
                        auth_ctx = get_auth_context()
                        if auth_ctx:
                            user_id = auth_ctx.get_user_id()

                        if user_id:
                            sections = await section_organizer.get_sections_for_resource(
                                resource_id=resource_id,
                                user_id=user_id,
                            )
                            sections_data.extend(sections)

                            if include_cost:
                                cost_result = await repository_analysis_service.get_cost_analysis(
                                    resource_id=resource_id,
                                    user_id=user_id,
                                )
                                if cost_result:
                                    cost_data[resource_id] = cost_result

                            if include_compliance:
                                compliance_result = await repository_analysis_service.get_compliance_analysis(
                                    resource_id=resource_id,
                                    user_id=user_id,
                                )
                                if compliance_result:
                                    compliance_data[resource_id] = compliance_result

                            db = self.mongodb_client.get_database()
                            articles = list(db.knowledge_articles.find({
                                "resource_id": resource_id,
                                "user_id": user_id,
                            }))
                            total_components += len(articles)

                            for article in articles:
                                tags = article.get("tags", [])
                                for tag in tags:
                                    tag_lower = tag.lower()
                                    if tag_lower in ["python", "javascript", "typescript", "go", "rust", "java", "terraform", "yaml", "json"]:
                                        languages.add(tag)
                                resource_type = article.get("resource_type")
                                if resource_type:
                                    resource_types.add(resource_type)
                    except Exception as e:
                        logger.warning("Failed to fetch data for resource %s: %s", resource_id, e)
            except ImportError as e:
                logger.warning("Could not import services for project overview: %s", e)

        toc_entries = []

        markdown += "---\n\n"
        markdown += "## Executive Summary\n\n"
        toc_entries.append(("Executive Summary", 2))

        markdown += f"This document provides a comprehensive overview of **{subject}**"
        if total_components > 0:
            markdown += f", containing **{total_components} components**"
        if sections_data:
            markdown += f" organized into **{len(sections_data)} functional sections**"
        markdown += ".\n\n"

        if languages:
            markdown += f"**Languages/Technologies**: {', '.join(sorted(languages))}\n\n"
        if resource_types:
            markdown += f"**Resource Types**: {', '.join(sorted(resource_types))}\n\n"

        if include_cost and cost_data:
            total_monthly = sum(c.get("total_monthly", 0) for c in cost_data.values())
            markdown += f"**Estimated Monthly Cost**: ${total_monthly:,.2f}\n\n"

        if include_compliance and compliance_data:
            statuses = [c.get("overall_status", "unknown") for c in compliance_data.values()]
            if "non_compliant" in statuses:
                overall = "⚠️ Non-Compliant"
            elif "partial" in statuses:
                overall = "⚡ Partial Compliance"
            elif "compliant" in statuses:
                overall = "✅ Compliant"
            else:
                overall = "❓ Unknown"
            markdown += f"**Compliance Status**: {overall}\n\n"

        markdown += "---\n\n"

        if sections_data:
            markdown += "## Sections Overview\n\n"
            toc_entries.append(("Sections Overview", 2))

            for section in sections_data:
                section_title = section.title if hasattr(section, 'title') else section.get("title", "Untitled")
                section_type = section.section_type.value if hasattr(section, 'section_type') else section.get("section_type", "general")
                section_summary = section.summary if hasattr(section, 'summary') else section.get("summary", "")
                component_count = len(section.component_article_ids) if hasattr(section, 'component_article_ids') else len(section.get("component_article_ids", []))

                markdown += f"### {section_title}\n\n"
                toc_entries.append((section_title, 3))

                markdown += f"**Type**: {section_type} | **Components**: {component_count}\n\n"

                if section_summary:
                    markdown += f"{section_summary}\n\n"

                diagram = section.architecture_diagram if hasattr(section, 'architecture_diagram') else section.get("architecture_diagram")
                if diagram:
                    markdown += "#### Architecture\n\n"
                    markdown += f"```mermaid\n{diagram}\n```\n\n"

            markdown += "---\n\n"

        markdown = await self._add_cost_summary(markdown, toc_entries, include_cost, cost_data)
        markdown = await self._add_compliance_summary(markdown, toc_entries, include_compliance, compliance_data)
        markdown = await self._add_security_overview(markdown, toc_entries, include_security)
        markdown = self._add_references(markdown, toc_entries)

        if include_toc:
            markdown = self._insert_toc(markdown, toc_entries)

        return markdown

    async def _add_cost_summary(
        self,
        markdown: str,
        toc_entries: list,
        include_cost: bool,
        cost_data: dict,
    ) -> str:
        """Add cost analysis summary to project overview."""
        if not include_cost or not cost_data:
            return markdown

        markdown += "## Cost Analysis Summary\n\n"
        toc_entries.append(("Cost Analysis Summary", 2))

        total_monthly = sum(c.get("total_monthly", 0) for c in cost_data.values())
        total_annual = total_monthly * 12

        markdown += "| Metric | Value |\n"
        markdown += "|--------|-------|\n"
        markdown += f"| Total Monthly Cost | ${total_monthly:,.2f} |\n"
        markdown += f"| Total Annual Cost | ${total_annual:,.2f} |\n\n"

        all_by_service = {}
        for cost in cost_data.values():
            for service, amount in cost.get("breakdown", {}).get("by_service", {}).items():
                all_by_service[service] = all_by_service.get(service, 0) + amount

        if all_by_service:
            markdown += "### Cost by Service\n\n"
            markdown += "| Service | Monthly Cost |\n"
            markdown += "|---------|-------------|\n"
            for service, amount in sorted(all_by_service.items(), key=lambda x: x[1], reverse=True)[:10]:
                markdown += f"| {service} | ${amount:,.2f} |\n"
            markdown += "\n"

        markdown += "---\n\n"
        return markdown

    async def _add_compliance_summary(
        self,
        markdown: str,
        toc_entries: list,
        include_compliance: bool,
        compliance_data: dict,
    ) -> str:
        """Add compliance summary to project overview."""
        if not include_compliance or not compliance_data:
            return markdown

        markdown += "## Compliance Summary\n\n"
        toc_entries.append(("Compliance Summary", 2))

        all_standards = {}
        for compliance in compliance_data.values():
            for standard, data in compliance.get("standards", {}).items():
                if standard not in all_standards:
                    all_standards[standard] = {"compliant": 0, "partial": 0, "non_compliant": 0}
                all_standards[standard]["compliant"] += data.get("compliant_count", 0)
                all_standards[standard]["partial"] += data.get("partial_count", 0)
                all_standards[standard]["non_compliant"] += data.get("non_compliant_count", 0)

        if all_standards:
            markdown += "| Standard | Compliant | Partial | Non-Compliant | Status |\n"
            markdown += "|----------|-----------|---------|---------------|--------|\n"
            for standard, counts in all_standards.items():
                total = counts["compliant"] + counts["partial"] + counts["non_compliant"]
                if total > 0:
                    rate = (counts["compliant"] / total) * 100
                    status = "✅" if rate >= 90 else "⚡" if rate >= 50 else "⚠️"
                else:
                    status = "❓"
                markdown += f"| {standard} | {counts['compliant']} | {counts['partial']} | {counts['non_compliant']} | {status} |\n"
            markdown += "\n"

        markdown += "---\n\n"
        return markdown

    async def _add_security_overview(
        self,
        markdown: str,
        toc_entries: list,
        include_security: bool,
    ) -> str:
        """Add security overview to project overview."""
        if not include_security:
            return markdown

        markdown += "## Security Overview\n\n"
        toc_entries.append(("Security Overview", 2))

        markdown += "### Security Best Practices\n\n"
        markdown += "- ✅ Implement least privilege access controls\n"
        markdown += "- ✅ Enable encryption at rest and in transit\n"
        markdown += "- ✅ Regular security audits and vulnerability scanning\n"
        markdown += "- ✅ Monitor for security events and anomalies\n"
        markdown += "- ✅ Keep dependencies and packages updated\n\n"

        markdown += "---\n\n"
        return markdown

    def _add_references(self, markdown: str, toc_entries: list) -> str:
        """Add references section to project overview."""
        markdown += "## References\n\n"
        toc_entries.append(("References", 2))

        markdown += "- [WISTX Documentation](https://wistx.dev/docs)\n"
        markdown += "- [Compliance Standards Reference](https://wistx.dev/compliance)\n"
        markdown += "- [Cost Optimization Guide](https://wistx.dev/cost-optimization)\n\n"

        return markdown

    def _insert_toc(self, markdown: str, toc_entries: list) -> str:
        """Insert table of contents into markdown."""
        toc_markdown = "## Table of Contents\n\n"
        for title, level in toc_entries:
            indent = "  " * (level - 2)
            anchor = title.lower().replace(" ", "-").replace("/", "").replace("(", "").replace(")", "")
            toc_markdown += f"{indent}- [{title}](#{anchor})\n"
        toc_markdown += "\n"

        insert_pos = markdown.find("---\n\n") + 5
        return markdown[:insert_pos] + toc_markdown + markdown[insert_pos:]

    async def generate_infrastructure_import_report(
        self,
        subject: str,
        discovery_data: dict[str, Any],
        include_compliance: bool = True,
        include_security: bool = True,
        include_diagram: bool = True,
        include_import_commands: bool = True,
        include_toc: bool = True,
        api_key: str = "",
    ) -> str:
        """Generate infrastructure import documentation from cloud discovery results.

        Args:
            subject: Project/infrastructure name
            discovery_data: Discovery results containing resources, dependencies, metrics
            include_compliance: Include compliance analysis
            include_security: Include security recommendations
            include_diagram: Include architecture diagram
            include_import_commands: Include Terraform import commands
            include_toc: Include table of contents

        Returns:
            Generated markdown documentation
        """
        toc_entries: list[tuple[str, int]] = []

        # Extract discovery data
        resources = discovery_data.get("resources", [])
        dependency_graph = discovery_data.get("dependency_graph", {})
        metrics = discovery_data.get("metrics", {})
        provider = discovery_data.get("provider", "aws")
        regions = discovery_data.get("regions", [])

        markdown = f"# Infrastructure Import Report: {subject}\n\n"
        markdown += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        markdown += f"**Cloud Provider**: {provider.upper()}\n"
        if regions:
            markdown += f"**Regions**: {', '.join(regions)}\n"
        markdown += "\n---\n\n"

        # Executive Summary
        markdown += "## Executive Summary\n\n"
        toc_entries.append(("Executive Summary", 2))

        total_resources = len(resources)
        resource_types = {}
        for r in resources:
            rt = r.get("resource_type", "unknown")
            resource_types[rt] = resource_types.get(rt, 0) + 1

        markdown += f"This report documents **{total_resources}** cloud resources discovered "
        markdown += f"across **{len(resource_types)}** resource types.\n\n"

        markdown += "### Discovery Metrics\n\n"
        markdown += "| Metric | Value |\n"
        markdown += "|--------|-------|\n"
        markdown += f"| Total Resources | {total_resources} |\n"
        markdown += f"| Resource Types | {len(resource_types)} |\n"
        markdown += f"| Regions Scanned | {len(regions)} |\n"
        if metrics:
            markdown += f"| Discovery Duration | {metrics.get('duration_seconds', 'N/A')}s |\n"
        markdown += "\n"

        # Resource Inventory
        markdown += "## Resource Inventory\n\n"
        toc_entries.append(("Resource Inventory", 2))

        markdown += "### Resources by Type\n\n"
        markdown += "| Resource Type | Count | Terraform Type |\n"
        markdown += "|---------------|-------|----------------|\n"
        for rt, count in sorted(resource_types.items(), key=lambda x: x[1], reverse=True):
            tf_type = self._get_terraform_type(rt, provider)
            markdown += f"| {rt} | {count} | `{tf_type}` |\n"
        markdown += "\n"

        # Group resources by import phase
        markdown += "### Resources by Import Phase\n\n"
        phases = self._group_by_import_phase(resources)
        for phase, phase_resources in phases.items():
            if phase_resources:
                markdown += f"#### {phase}\n\n"
                toc_entries.append((phase, 4))
                markdown += "| Resource Name | Resource ID | Region |\n"
                markdown += "|---------------|-------------|--------|\n"
                for r in phase_resources[:20]:  # Limit to 20 per phase
                    name = r.get("name", r.get("terraform_name", "unnamed"))
                    rid = r.get("resource_id", "N/A")
                    region = r.get("region", "N/A")
                    markdown += f"| {name} | `{rid}` | {region} |\n"
                if len(phase_resources) > 20:
                    markdown += f"| ... and {len(phase_resources) - 20} more | | |\n"
                markdown += "\n"

        # Architecture Diagram
        if include_diagram and dependency_graph:
            markdown += "## Architecture Diagram\n\n"
            toc_entries.append(("Architecture Diagram", 2))
            mermaid = self._generate_mermaid_from_dependencies(dependency_graph, resources)
            markdown += f"```mermaid\n{mermaid}\n```\n\n"

        # Dependency Analysis
        if dependency_graph:
            markdown += "## Dependency Analysis\n\n"
            toc_entries.append(("Dependency Analysis", 2))

            edges = dependency_graph.get("edges", [])
            nodes = dependency_graph.get("nodes", [])

            markdown += f"The infrastructure contains **{len(nodes)}** nodes "
            markdown += f"with **{len(edges)}** dependency relationships.\n\n"

            # Import order
            import_order = dependency_graph.get("topological_order", [])
            if import_order:
                markdown += "### Recommended Import Order\n\n"
                markdown += "Resources should be imported in this order to satisfy dependencies:\n\n"
                for i, resource_id in enumerate(import_order[:30], 1):
                    resource = next((r for r in resources if r.get("resource_id") == resource_id), None)
                    name = resource.get("terraform_name", resource_id) if resource else resource_id
                    markdown += f"{i}. `{name}`\n"
                if len(import_order) > 30:
                    markdown += f"... and {len(import_order) - 30} more\n"
                markdown += "\n"

        # Import Commands
        if include_import_commands:
            markdown += "## Terraform Import Commands\n\n"
            toc_entries.append(("Terraform Import Commands", 2))

            markdown += "Use these commands to import existing resources into Terraform state:\n\n"
            markdown += "```bash\n"
            for r in resources[:50]:  # Limit to 50 commands
                import_cmd = r.get("import_command")
                if import_cmd:
                    markdown += f"{import_cmd}\n"
            markdown += "```\n\n"
            if len(resources) > 50:
                markdown += f"*... and {len(resources) - 50} more import commands*\n\n"

        # Security Analysis
        if include_security:
            markdown += "## Security Recommendations\n\n"
            toc_entries.append(("Security Recommendations", 2))
            markdown += await self._generate_security_recommendations(resources, provider)

        # Compliance Status
        if include_compliance:
            markdown += "## Compliance Considerations\n\n"
            toc_entries.append(("Compliance Considerations", 2))
            markdown += await self._generate_compliance_considerations(resources, provider)

        # Next Steps
        markdown += "## Next Steps\n\n"
        toc_entries.append(("Next Steps", 2))
        markdown += "1. **Review Resources**: Verify the discovered resources match your infrastructure\n"
        markdown += "2. **Generate Terraform**: Use your AI coding assistant to generate Terraform code\n"
        markdown += "3. **Import State**: Run the import commands to import existing resources\n"
        markdown += "4. **Validate**: Run `terraform plan` to ensure no changes are detected\n"
        markdown += "5. **Iterate**: Address any drift and update configurations as needed\n\n"

        if include_toc:
            markdown = self._insert_toc(markdown, toc_entries)

        return markdown

    def _get_terraform_type(self, resource_type: str, provider: str) -> str:
        """Get Terraform resource type from cloud resource type."""
        # Common AWS mappings
        aws_mappings = {
            "AWS::EC2::Instance": "aws_instance",
            "AWS::EC2::VPC": "aws_vpc",
            "AWS::EC2::Subnet": "aws_subnet",
            "AWS::EC2::SecurityGroup": "aws_security_group",
            "AWS::S3::Bucket": "aws_s3_bucket",
            "AWS::RDS::DBInstance": "aws_db_instance",
            "AWS::Lambda::Function": "aws_lambda_function",
            "AWS::IAM::Role": "aws_iam_role",
            "AWS::DynamoDB::Table": "aws_dynamodb_table",
        }
        return aws_mappings.get(resource_type, resource_type.lower().replace("::", "_"))

    def _group_by_import_phase(self, resources: list[dict]) -> dict[str, list]:
        """Group resources by import phase."""
        phases = {
            "Foundation": [],
            "Networking": [],
            "Security": [],
            "Data Layer": [],
            "Compute": [],
            "Other": [],
        }

        phase_patterns = {
            "Foundation": ["VPC", "Subnet", "RouteTable", "InternetGateway", "NATGateway"],
            "Networking": ["LoadBalancer", "TargetGroup", "Listener", "NetworkInterface"],
            "Security": ["SecurityGroup", "IAM", "KMS", "Secret"],
            "Data Layer": ["RDS", "DynamoDB", "S3", "ElastiCache", "Elasticsearch"],
            "Compute": ["EC2", "Lambda", "ECS", "EKS", "AutoScaling"],
        }

        for resource in resources:
            rt = resource.get("resource_type", "")
            placed = False
            for phase, patterns in phase_patterns.items():
                if any(p in rt for p in patterns):
                    phases[phase].append(resource)
                    placed = True
                    break
            if not placed:
                phases["Other"].append(resource)

        return phases

    def _generate_mermaid_from_dependencies(
        self, dependency_graph: dict, resources: list[dict]
    ) -> str:
        """Generate Mermaid diagram from dependency graph."""
        mermaid = "graph TB\n"

        # Create node ID mapping for shorter IDs
        resource_map = {r.get("resource_id"): r for r in resources}
        node_ids = {}
        counter = 0

        for node in dependency_graph.get("nodes", [])[:50]:  # Limit nodes
            resource = resource_map.get(node)
            if resource:
                name = resource.get("terraform_name", node)[:30]
                rt = resource.get("resource_type", "").split("::")[-1]
                node_ids[node] = f"n{counter}"
                mermaid += f"    n{counter}[{rt}\\n{name}]\n"
                counter += 1

        for edge in dependency_graph.get("edges", [])[:100]:  # Limit edges
            from_id = node_ids.get(edge.get("from"))
            to_id = node_ids.get(edge.get("to"))
            if from_id and to_id:
                mermaid += f"    {from_id} --> {to_id}\n"

        return mermaid

    async def _generate_security_recommendations(
        self, resources: list[dict], provider: str
    ) -> str:
        """Generate security recommendations based on discovered resources."""
        md = ""

        # Check for common security concerns
        has_public_resources = any(
            r.get("configuration", {}).get("public", False) or
            "public" in str(r.get("configuration", {})).lower()
            for r in resources
        )

        has_encryption = any(
            r.get("configuration", {}).get("encrypted", False) or
            "kms" in str(r.get("configuration", {})).lower()
            for r in resources
        )

        md += "### Key Findings\n\n"
        md += "| Check | Status | Recommendation |\n"
        md += "|-------|--------|----------------|\n"

        if has_public_resources:
            md += "| Public Resources | ⚠️ Found | Review public access settings |\n"
        else:
            md += "| Public Resources | ✅ None Found | Good practice |\n"

        if has_encryption:
            md += "| Encryption | ✅ Enabled | Continue using encryption |\n"
        else:
            md += "| Encryption | ⚠️ Check | Enable encryption at rest |\n"

        md += "\n### Recommendations\n\n"
        md += "1. **Review Security Groups**: Ensure no overly permissive rules (0.0.0.0/0)\n"
        md += "2. **Enable Encryption**: Use KMS for encryption at rest\n"
        md += "3. **IAM Least Privilege**: Review IAM roles for minimal permissions\n"
        md += "4. **Enable Logging**: Enable CloudTrail and VPC Flow Logs\n\n"

        return md

    async def _generate_compliance_considerations(
        self, resources: list[dict], provider: str
    ) -> str:
        """Generate compliance considerations based on discovered resources."""
        md = ""

        resource_types = set(r.get("resource_type", "") for r in resources)

        md += "### Applicable Standards\n\n"
        md += "Based on the discovered resources, consider the following compliance standards:\n\n"

        # Check for data storage resources
        has_data_storage = any(
            "S3" in rt or "RDS" in rt or "DynamoDB" in rt
            for rt in resource_types
        )

        if has_data_storage:
            md += "- **SOC 2**: Data storage resources require access controls and encryption\n"
            md += "- **GDPR**: Ensure data residency and retention policies\n"
            md += "- **HIPAA**: If handling PHI, ensure BAA and encryption requirements\n"

        # Check for networking resources
        has_networking = any("VPC" in rt or "Subnet" in rt for rt in resource_types)
        if has_networking:
            md += "- **PCI DSS**: Network segmentation and firewall rules\n"

        md += "\n### Recommended Actions\n\n"
        md += "1. Enable AWS Config rules for compliance monitoring\n"
        md += "2. Implement resource tagging for cost allocation and compliance tracking\n"
        md += "3. Review and document data classification for all storage resources\n\n"

        return md

