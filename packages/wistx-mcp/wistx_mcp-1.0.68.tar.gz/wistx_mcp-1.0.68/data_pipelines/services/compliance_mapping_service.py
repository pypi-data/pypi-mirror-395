"""Compliance mapping service - generates mappings between code examples and compliance controls."""

import logging
from typing import Any

from data_pipelines.models.compliance_mapping import ComplianceMapping

logger = logging.getLogger(__name__)


class ComplianceMappingService:
    """Service for generating compliance mappings from code examples."""

    def __init__(self):
        """Initialize compliance mapping service."""
        pass

    async def generate_mappings(
        self,
        example_id: str,
        resources: list[str],
        code: str,
        code_type: str,
        cloud_provider: str,
    ) -> list[ComplianceMapping]:
        """Generate compliance mappings for a code example.
        
        Args:
            example_id: Code example ID
            resources: List of resource types extracted from code
            code: Code content
            code_type: Code type (terraform, kubernetes, etc.)
            cloud_provider: Cloud provider (aws, gcp, azure)
            
        Returns:
            List of compliance mappings
        """
        if not resources:
            logger.debug("No resources found for example %s, skipping mapping", example_id)
            return []
        
        try:
            from api.services.compliance_service import ComplianceService
            
            compliance_service = ComplianceService()
            
            all_standards = ["PCI-DSS", "HIPAA", "SOC2", "CIS", "NIST-800-53", "ISO-27001"]
            
            mappings = []
            
            for standard in all_standards:
                try:
                    from api.models.v1_requests import ComplianceRequirementsRequest
                    
                    request = ComplianceRequirementsRequest(
                        resource_types=resources,
                        standards=[standard],
                        include_remediation=True,
                        include_verification=False,
                    )
                    
                    response = await compliance_service.get_compliance_requirements(
                        request=request,
                        request_id=None,
                    )
                    
                    controls = response.controls or []
                    
                    for control in controls:
                        control_id = control.control_id
                        if not control_id:
                            continue
                        
                        implementation_status = self._analyze_implementation_status(
                            code=code,
                            control=control.model_dump(),
                            code_type=code_type,
                        )
                        
                        if implementation_status == "not_applicable":
                            continue
                        
                        relevance_score = self._calculate_relevance_score(
                            resources=resources,
                            control=control_dict,
                            cloud_provider=cloud_provider,
                        )
                        
                        if relevance_score < 0.3:
                            continue
                        
                        applies_to = control_dict.get("applies_to", [])
                        applies_to_resources = [
                            r for r in resources if r in applies_to or self._resource_matches(r, applies_to)
                        ]
                        
                        if not applies_to_resources:
                            applies_to_resources = resources[:1]
                        
                        mapping_id = ComplianceMapping.generate_mapping_id(
                            example_id=example_id,
                            control_id=control_id,
                            standard=standard,
                        )
                        
                        mapping = ComplianceMapping(
                            mapping_id=mapping_id,
                            example_id=example_id,
                            control_id=control_id,
                            standard=standard,
                            severity=control_dict.get("severity", "MEDIUM"),
                            relevance_score=relevance_score,
                            applies_to_resources=applies_to_resources,
                            implementation_status=implementation_status,
                            notes=self._generate_notes(
                                control=control_dict,
                                resources=applies_to_resources,
                                implementation_status=implementation_status,
                            ),
                        )
                        
                        mappings.append(mapping)
                
                except Exception as e:
                    logger.debug("Error generating mappings for standard %s: %s", standard, e)
                    continue
            
            logger.info(
                "Generated %d compliance mappings for example %s",
                len(mappings),
                example_id,
            )
            
            return mappings
        
        except Exception as e:
            logger.warning("Error generating compliance mappings: %s", e)
            return []

    def _analyze_implementation_status(
        self,
        code: str,
        control: dict[str, Any],
        code_type: str,
    ) -> str:
        """Analyze if compliance control is implemented in code.
        
        Args:
            code: Code content
            control: Compliance control dictionary
            code_type: Code type
            
        Returns:
            Implementation status: implemented, partial, missing, not_applicable
        """
        code_lower = code.lower()
        
        remediation = control.get("remediation", {})
        code_snippets = remediation.get("code_snippets", [])
        
        if code_snippets:
            matching_snippets = 0
            for snippet in code_snippets:
                snippet_code = snippet.get("code", "")
                snippet_infra_type = snippet.get("infrastructure_type", "")
                
                if snippet_infra_type and snippet_infra_type != code_type:
                    continue
                
                if snippet_code:
                    snippet_lower = snippet_code.lower()
                    if len(snippet_lower) > 50:
                        if snippet_lower[:100] in code_lower:
                            matching_snippets += 1
                    elif snippet_lower in code_lower:
                        matching_snippets += 1
            
            if matching_snippets > 0:
                if matching_snippets == len(code_snippets):
                    return "implemented"
                else:
                    return "partial"
        
        control_title = control.get("title", "").lower()
        control_description = control.get("description", "").lower()
        
        keywords = []
        if control_title:
            keywords.extend(control_title.split()[:5])
        if control_description:
            keywords.extend(control_description.split()[:10])
        
        if keywords:
            found_keywords = sum(1 for kw in keywords if len(kw) > 3 and kw in code_lower)
            keyword_ratio = found_keywords / len(keywords)
            
            if keyword_ratio > 0.7:
                return "implemented"
            elif keyword_ratio > 0.4:
                return "partial"
            else:
                return "missing"
        
        return "missing"

    def _calculate_relevance_score(
        self,
        resources: list[str],
        control: dict[str, Any],
        cloud_provider: str,
    ) -> float:
        """Calculate relevance score between resources and control.
        
        Args:
            resources: List of resource types
            control: Compliance control dictionary
            cloud_provider: Cloud provider
            
        Returns:
            Relevance score (0.0-1.0)
        """
        applies_to = control.get("applies_to", [])
        
        if not applies_to:
            return 0.5
        
        matching_resources = 0
        for resource in resources:
            if resource in applies_to:
                matching_resources += 1
            elif self._resource_matches(resource, applies_to):
                matching_resources += 1
        
        if matching_resources == 0:
            return 0.3
        
        base_score = matching_resources / len(resources)
        
        cloud_match_bonus = 0.0
        for resource_type in applies_to:
            if cloud_provider == "aws" and resource_type.startswith("AWS::"):
                cloud_match_bonus = 0.2
                break
            elif cloud_provider == "gcp" and resource_type.startswith("GCP::"):
                cloud_match_bonus = 0.2
                break
            elif cloud_provider == "azure" and resource_type.startswith("Azure::"):
                cloud_match_bonus = 0.2
                break
        
        return min(1.0, base_score + cloud_match_bonus)

    def _resource_matches(self, resource: str, applies_to: list[str]) -> bool:
        """Check if resource matches any applies_to pattern.
        
        Args:
            resource: Resource type string
            applies_to: List of resource type patterns
            
        Returns:
            True if resource matches
        """
        resource_lower = resource.lower()
        
        for pattern in applies_to:
            pattern_lower = pattern.lower()
            
            if "::" in pattern_lower:
                parts = pattern_lower.split("::")
                if len(parts) >= 2:
                    service = parts[1].lower()
                    if service in resource_lower:
                        return True
            
            if pattern_lower in resource_lower or resource_lower in pattern_lower:
                return True
        
        return False

    def _generate_notes(
        self,
        control: dict[str, Any],
        resources: list[str],
        implementation_status: str,
    ) -> str:
        """Generate notes for mapping.
        
        Args:
            control: Compliance control dictionary
            resources: List of resources this applies to
            implementation_status: Implementation status
            
        Returns:
            Notes string
        """
        control_title = control.get("title", "")
        
        if implementation_status == "implemented":
            status_text = "fully implemented"
        elif implementation_status == "partial":
            status_text = "partially implemented"
        else:
            status_text = "not implemented"
        
        resources_text = ", ".join(resources[:3])
        if len(resources) > 3:
            resources_text += f" (+{len(resources) - 3} more)"
        
        return f"Control '{control_title}' {status_text} for resources: {resources_text}"

