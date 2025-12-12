"""Code enrichment service - enriches code examples with metadata and relationships."""

import logging
from datetime import datetime
from typing import Any

try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    AsyncAnthropic = None

from api.config import settings
from data_pipelines.models.code_example import CodeExample

logger = logging.getLogger(__name__)


class CodeEnrichmentService:
    """Enrich code examples with metadata, relationships, and analysis."""

    def __init__(self):
        """Initialize code enrichment service."""
        if not ANTHROPIC_AVAILABLE:
            self.anthropic_client = None
            logger.warning("anthropic package not installed. Contextual description generation disabled.")
        else:
            anthropic_api_key = getattr(settings, "anthropic_api_key", None)
            if anthropic_api_key:
                self.anthropic_client = AsyncAnthropic(api_key=anthropic_api_key)
            else:
                self.anthropic_client = None
                logger.warning("ANTHROPIC_API_KEY not set. Contextual description generation disabled.")

    async def enrich_code_example(
        self,
        processed: dict[str, Any],
        generate_mappings: bool = True,
    ) -> dict[str, Any]:
        """Enrich a processed code example.
        
        Args:
            processed: Processed code example dictionary
            generate_mappings: Whether to generate compliance mappings (default: True)
            
        Returns:
            Enriched code example dictionary with mappings in relationships
        """
        enriched = processed.copy()
        
        enriched["compliance_analysis"] = await self._analyze_compliance(enriched)
        enriched["cost_analysis"] = await self._analyze_cost(enriched)
        enriched["best_practices"] = await self._extract_best_practices(enriched)
        enriched["relationships"] = await self._discover_relationships(enriched)
        enriched["contextual_description"] = await self._generate_contextual_description(enriched)
        
        if generate_mappings:
            enriched["compliance_mappings"] = await self._generate_compliance_mappings(enriched)
        else:
            enriched["compliance_mappings"] = []
        
        enriched["enriched_at"] = datetime.utcnow()
        
        return enriched

    async def _generate_compliance_mappings(
        self,
        enriched: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Generate compliance mappings for enriched code example.
        
        Args:
            enriched: Enriched code example dictionary
            
        Returns:
            List of compliance mapping dictionaries
        """
        try:
            from data_pipelines.services.compliance_mapping_service import ComplianceMappingService
            
            mapping_service = ComplianceMappingService()
            
            example_id = enriched.get("example_id", "")
            resources = enriched.get("resources", [])
            code = enriched.get("code", "")
            code_type = enriched.get("code_type", "")
            cloud_provider = enriched.get("cloud_provider", "unknown")
            
            if not example_id or not resources:
                return []
            
            mappings = await mapping_service.generate_mappings(
                example_id=example_id,
                resources=resources,
                code=code,
                code_type=code_type,
                cloud_provider=cloud_provider,
            )
            
            return [mapping.model_dump() for mapping in mappings]
        
        except Exception as e:
            logger.warning("Error generating compliance mappings: %s", e)
            return []

    async def _analyze_compliance(self, processed: dict[str, Any]) -> dict[str, Any]:
        """Analyze compliance for code example.
        
        Args:
            processed: Processed code example
            
        Returns:
            Compliance analysis dictionary
        """
        try:
            from api.services.compliance_service import ComplianceService
            
            compliance_service = ComplianceService()
            resources = processed.get("resources", [])
            
            if not resources:
                return {
                    "applicable_standards": [],
                    "resource_types": [],
                    "compliance_score": {},
                    "missing_controls": {},
                    "implemented_controls": {},
                    "analysis_timestamp": datetime.utcnow(),
                }
            
            all_standards = ["PCI-DSS", "HIPAA", "SOC2", "CIS", "NIST-800-53", "ISO-27001"]
            
            applicable_standards = []
            compliance_scores = {}
            missing_controls = {}
            implemented_controls = {}
            
            for standard in all_standards:
                try:
                    from api.models.v1_requests import ComplianceRequirementsRequest
                    
                    request = ComplianceRequirementsRequest(
                        resource_types=resources,
                        standards=[standard],
                        include_remediation=True,
                        include_verification=True,
                    )
                    
                    response = await compliance_service.get_compliance_requirements(request)
                    
                    if response and response.controls:
                        applicable_standards.append(standard)
                        
                        controls = response.controls
                        implemented = []
                        missing = []
                        
                        for control in controls:
                            control_id = control.control_id
                            if self._is_control_implemented(processed["code"], control.model_dump()):
                                implemented.append(control_id)
                            else:
                                missing.append(control_id)
                        
                        implemented_controls[standard] = implemented
                        missing_controls[standard] = missing
                        
                        if controls:
                            score = len(implemented) / len(controls)
                            compliance_scores[standard] = score
                except Exception as e:
                    logger.debug("Error analyzing compliance for standard %s: %s", standard, e)
                    continue
            
            return {
                "applicable_standards": applicable_standards,
                "resource_types": resources,
                "compliance_score": compliance_scores,
                "missing_controls": missing_controls,
                "implemented_controls": implemented_controls,
                "analysis_timestamp": datetime.utcnow(),
            }
        except Exception as e:
            logger.warning("Error in compliance analysis: %s", e)
            return {
                "applicable_standards": [],
                "resource_types": [],
                "compliance_score": {},
                "missing_controls": {},
                "implemented_controls": {},
                "analysis_timestamp": datetime.utcnow(),
                "error": str(e),
            }

    def _is_control_implemented(self, code: str, control: dict[str, Any]) -> bool:
        """Check if compliance control is implemented in code.
        
        Args:
            code: Code content
            control: Compliance control dictionary
            
        Returns:
            True if control appears to be implemented
        """
        code_lower = code.lower()
        
        remediation = control.get("remediation", {})
        code_snippets = remediation.get("code_snippets", [])
        
        if code_snippets:
            for snippet in code_snippets:
                snippet_code = snippet.get("code", "")
                if snippet_code and snippet_code.lower() in code_lower:
                    return True
        
        control_title = control.get("title", "").lower()
        control_description = control.get("description", "").lower()
        
        keywords = []
        if control_title:
            keywords.extend(control_title.split())
        if control_description:
            keywords.extend(control_description.split()[:10])
        
        if keywords:
            found_keywords = sum(1 for kw in keywords if kw in code_lower)
            if found_keywords / len(keywords) > 0.5:
                return True
        
        return False

    async def _analyze_cost(self, processed: dict[str, Any]) -> dict[str, Any]:
        """Analyze cost for code example.
        
        Args:
            processed: Processed code example
            
        Returns:
            Cost analysis dictionary
        """
        try:
            from wistx_mcp.tools.pricing import calculate_infrastructure_cost
            
            resources = processed.get("resources", [])
            cloud_provider = processed.get("cloud_provider", "unknown")
            
            if not resources or cloud_provider == "unknown":
                return {
                    "estimated_monthly": 0.0,
                    "estimated_annual": 0.0,
                    "resource_costs": [],
                    "analysis_timestamp": datetime.utcnow(),
                }
            
            resource_specs = []
            for resource in resources[:10]:
                resource_specs.append({
                    "cloud": cloud_provider,
                    "service": self._extract_service_from_resource(resource),
                    "instance_type": self._extract_instance_type_from_resource(resource),
                    "quantity": 1,
                })
            
            if resource_specs:
                try:
                    result = await calculate_infrastructure_cost(
                        resources=resource_specs,
                        user_id=None,
                        check_budgets=False,
                    )
                    
                    return {
                        "estimated_monthly": result.get("total_monthly", 0.0),
                        "estimated_annual": result.get("total_annual", 0.0),
                        "resource_costs": result.get("breakdown", []),
                        "analysis_timestamp": datetime.utcnow(),
                    }
                except Exception as e:
                    logger.debug("Error calculating cost: %s", e)
            
            return {
                "estimated_monthly": 0.0,
                "estimated_annual": 0.0,
                "resource_costs": [],
                "analysis_timestamp": datetime.utcnow(),
            }
        except Exception as e:
            logger.warning("Error in cost analysis: %s", e)
            return {
                "estimated_monthly": 0.0,
                "estimated_annual": 0.0,
                "resource_costs": [],
                "analysis_timestamp": datetime.utcnow(),
                "error": str(e),
            }

    def _extract_service_from_resource(self, resource: str) -> str:
        """Extract service name from resource type.
        
        Args:
            resource: Resource type string
            
        Returns:
            Service name
        """
        resource_lower = resource.lower()
        
        if "rds" in resource_lower or "database" in resource_lower:
            return "rds"
        if "s3" in resource_lower or "bucket" in resource_lower:
            return "s3"
        if "ec2" in resource_lower or "instance" in resource_lower:
            return "ec2"
        if "lambda" in resource_lower:
            return "lambda"
        if "eks" in resource_lower or "kubernetes" in resource_lower:
            return "eks"
        
        return "unknown"

    def _extract_instance_type_from_resource(self, resource: str) -> str:
        """Extract instance type from resource type.
        
        Args:
            resource: Resource type string
            
        Returns:
            Instance type
        """
        return "default"

    async def _extract_best_practices(self, processed: dict[str, Any]) -> list[str]:
        """Extract best practices from code example.
        
        Args:
            processed: Processed code example
            
        Returns:
            List of best practice identifiers
        """
        best_practices = []
        code = processed.get("code", "")
        code_type = processed.get("code_type", "")
        
        code_lower = code.lower()
        
        if code_type == "terraform":
            if "variable" in code_lower:
                best_practices.append("uses-variables")
            if "module" in code_lower:
                best_practices.append("uses-modules")
            if "output" in code_lower:
                best_practices.append("has-outputs")
            if "backend" in code_lower:
                best_practices.append("uses-backend")
        
        if code_type in ["kubernetes", "docker"]:
            if "resource" in code_lower and "limits" in code_lower:
                best_practices.append("has-resource-limits")
            if "securitycontext" in code_lower or "security" in code_lower:
                best_practices.append("has-security-context")
        
        if "encryption" in code_lower or "encrypt" in code_lower:
            best_practices.append("uses-encryption")
        
        if "monitoring" in code_lower or "metrics" in code_lower:
            best_practices.append("has-monitoring")
        
        if "backup" in code_lower or "snapshot" in code_lower:
            best_practices.append("has-backup")
        
        return best_practices

    async def _discover_relationships(self, processed: dict[str, Any]) -> dict[str, Any]:
        """Discover relationships with other code examples and knowledge articles.
        
        Args:
            processed: Processed code example
            
        Returns:
            Relationships dictionary
        """
        return {
            "related_code_examples": [],
            "related_knowledge_articles": [],
            "related_compliance_controls": processed.get("compliance_analysis", {}).get("implemented_controls", {}),
            "discovered_at": datetime.utcnow(),
        }

    async def _generate_contextual_description(self, processed: dict[str, Any]) -> str:
        """Generate contextual description using Anthropic LLM.
        
        Uses Anthropic's contextual retrieval approach: generates a description
        that will be prepended before embedding to improve semantic search accuracy.
        
        Args:
            processed: Processed code example
            
        Returns:
            Contextual description string (max 2000 chars)
        """
        if not self.anthropic_client:
            logger.debug("Anthropic client not available, using fallback description")
            return self._generate_fallback_description(processed)
        
        try:
            code = processed.get("code", "")[:3000]
            code_type = processed.get("code_type", "")
            cloud_provider = processed.get("cloud_provider", "")
            services = processed.get("services", [])
            resources = processed.get("resources", [])
            
            prompt = f"""Generate a concise contextual description for this {code_type} infrastructure code example. This description will be used to improve semantic search accuracy.

Code Type: {code_type}
Cloud Provider: {cloud_provider}
Services: {', '.join(services[:5])}
Resources: {', '.join(resources[:5]) if resources else 'N/A'}

Code:
{code}

Generate a 2-4 sentence contextual description that:
1. Explains what infrastructure this code creates/manages
2. Highlights key features, patterns, or best practices demonstrated
3. Describes use cases or scenarios where this would be applicable
4. Mentions any compliance, security, or cost considerations if evident

The description should be informative and help with semantic search retrieval. Be specific about the infrastructure components and their purpose.

Description:"""

            response = await self.anthropic_client.messages.create(
                model="claude-opus-4-1",
                max_tokens=300,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}],
            )
            
            description = response.content[0].text.strip()
            
            if len(description) > 2000:
                description = description[:1997] + "..."
            
            logger.debug("Generated contextual description (%d chars) for example %s", len(description), processed.get("example_id", "unknown"))
            
            return description
        except Exception as e:
            logger.warning("Error generating contextual description: %s", e)
            return self._generate_fallback_description(processed)

    def _generate_fallback_description(self, processed: dict[str, Any]) -> str:
        """Generate fallback description when Anthropic is unavailable.
        
        Args:
            processed: Processed code example
            
        Returns:
            Fallback description string
        """
        code_type = processed.get("code_type", "")
        cloud_provider = processed.get("cloud_provider", "")
        services = processed.get("services", [])
        resources = processed.get("resources", [])
        
        parts = []
        
        if code_type:
            parts.append(f"{code_type.title()} code example")
        
        if cloud_provider and cloud_provider != "unknown":
            parts.append(f"for {cloud_provider.upper()}")
        
        if services:
            parts.append(f"using {', '.join(services[:3])}")
        
        if resources:
            parts.append(f"managing {', '.join(resources[:3])}")
        
        description = " ".join(parts) if parts else processed.get("description", "")
        
        return description

