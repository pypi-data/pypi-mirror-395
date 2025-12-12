"""Integration pattern advisor - provides integration patterns, recommendations, and guidance.

Uses dynamic pattern retrieval from knowledge base via vector search instead of hardcoded patterns.
Implements Phase 3 (Pattern Discovery) and Phase 4 (Quality Assurance) for industry-leading pattern management.
"""

import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.services.pattern_quality_scorer import PatternQualityScorer
from wistx_mcp.services.pattern_validation_service import PatternValidationService
from wistx_mcp.services.pattern_discovery_service import PatternDiscoveryService
from wistx_mcp.services.pattern_quality_assurance import PatternQualityAssurance
from wistx_mcp.config import settings
from data_pipelines.models.knowledge_article import ContentType, Domain

logger = logging.getLogger(__name__)


class IntegrationPatternAdvisor:
    """Advisor for integration patterns, recommendations, and best practices.

    Uses dynamic pattern retrieval from knowledge base with:
    - Vector search for semantic pattern matching
    - Pattern discovery from quality templates (Phase 3)
    - Quality assurance with template comparison (Phase 4)
    - Quality scoring and validation
    """

    def __init__(self, mongodb_client: MongoDBClient | None = None, vector_search: VectorSearch | None = None):
        """Initialize integration pattern advisor.

        Args:
            mongodb_client: MongoDB client (optional, creates new if not provided)
            vector_search: Vector search instance (optional, creates new if not provided)
        """
        self.mongodb_client = mongodb_client or MongoDBClient()
        self.vector_search = vector_search or VectorSearch(
            self.mongodb_client,
            gemini_api_key=settings.gemini_api_key,
            pinecone_api_key=settings.pinecone_api_key,
            pinecone_index_name=settings.pinecone_index_name,
        )
        self.quality_scorer = PatternQualityScorer()
        self.validation_service = PatternValidationService()
        self.discovery_service = PatternDiscoveryService(self.mongodb_client, self.vector_search)
        self.quality_assurance = PatternQualityAssurance(self.mongodb_client, self.vector_search)

    async def recommend_patterns(
        self,
        components: list[dict[str, Any]],
        integration_type: str,
        cloud_provider: str,
        pattern_name: str | None = None,
        repository_url: str | None = None,
    ) -> dict[str, Any]:
        """Recommend integration patterns and provide guidance for components.

        Uses dynamic pattern retrieval from knowledge base via vector search.
        Implements Phase 3 (Pattern Discovery) and Phase 4 (Quality Assurance).

        Args:
            components: List of components to integrate
            integration_type: Type of integration (networking, security, service, monitoring)
            cloud_provider: Cloud provider (aws, gcp, azure, kubernetes)
            pattern_name: Specific pattern to use (optional)
            repository_url: Repository URL for context-aware pattern discovery (optional)

        Returns:
            Dictionary with pattern recommendations:
            - recommended_patterns: List of recommended patterns with descriptions
            - pattern_details: Details about selected pattern (if pattern_name provided)
            - dependencies: List of dependencies required
            - security_rules: Security rules and best practices
            - monitoring: Monitoring configuration recommendations
            - implementation_guidance: Step-by-step implementation guidance
            - compliance_considerations: Compliance considerations
            - discovered_patterns: Patterns discovered from quality templates (Phase 3)
            - quality_assurance: Quality assurance results (Phase 4)
        """
        component_names = [comp.get("id", comp.get("type", "component")) for comp in components]
        
        query_parts = [integration_type]
        query_parts.extend(component_names)
        if cloud_provider:
            query_parts.append(cloud_provider)
        search_query = " ".join(query_parts)

        if pattern_name:
            pattern_articles = await self.vector_search.search_knowledge_articles(
                query=f"{pattern_name} {integration_type}",
                domains=[Domain.INFRASTRUCTURE.value],
                content_types=[ContentType.PATTERN.value],
                limit=10,
            )
            
            pattern_article = None
            for article in pattern_articles:
                structured_data = article.get("structured_data", {})
                if structured_data.get("pattern_name") == pattern_name and structured_data.get("integration_type") == integration_type:
                    pattern_article = article
                    break
            
            if not pattern_article:
                raise ValueError(f"Pattern {pattern_name} not found for {integration_type}")

            pattern = self._article_to_pattern_dict(pattern_article)
            quality_score_result = self.quality_scorer.score_pattern(pattern)
            validation_result = await self.validation_service.validate_pattern(pattern)
            
            quality_assurance_result = await self.quality_assurance.assess_pattern(
                pattern_article,
                components,
                cloud_provider,
            )
            
            discovered_patterns_info = []
            if repository_url:
                discovered_patterns_info = await self.discovery_service.get_discovery_summary(
                    repository_url,
                    integration_type,
                )
            
            pattern_details = {
                "name": pattern_name,
                "description": pattern.get("description", ""),
                "providers": pattern.get("providers", []),
                "components": pattern.get("components", []),
                "example_reference": pattern.get("terraform_example") or pattern.get("kubernetes_example", ""),
                "quality_score": quality_score_result.overall_score,
                "quality_breakdown": quality_score_result.score_breakdown,
                "meets_quality_threshold": quality_score_result.meets_threshold,
                "quality_recommendations": quality_score_result.recommendations,
                "validation_score": validation_result["score"],
                "validation_checks": validation_result["checks"],
                "meets_validation_threshold": validation_result["valid"],
                "validation_recommendations": validation_result["recommendations"],
                "quality_assurance": quality_assurance_result,
            }
        else:
            pattern_articles = await self.vector_search.search_knowledge_articles(
                query=search_query,
                domains=[Domain.INFRASTRUCTURE.value],
                content_types=[ContentType.PATTERN.value],
                limit=20,
            )
            
            if not pattern_articles:
                logger.warning(
                    "No patterns found in knowledge base for %s/%s, attempting pattern discovery",
                    integration_type,
                    cloud_provider,
                )
                
                if repository_url:
                    logger.info(
                        "No patterns found in knowledge base, attempting pattern discovery from repository: %s",
                        repository_url,
                    )
                    discovered_patterns = await self.discovery_service.discover_patterns_from_repository(
                        repository_url,
                        integration_type,
                        cloud_provider,
                    )
                    if discovered_patterns:
                        pattern_articles = discovered_patterns
                        stored_count = sum(1 for p in discovered_patterns if p.get("article_id"))
                        logger.info(
                            "Discovered %d patterns from repository %s (%d stored in knowledge base)",
                            len(discovered_patterns),
                            repository_url,
                            stored_count,
                        )
                    else:
                        logger.warning(
                            "Pattern discovery from repository %s found no patterns or patterns did not meet quality threshold",
                            repository_url,
                        )

            if not pattern_articles:
                raise ValueError(f"No patterns found for {integration_type} on {cloud_provider}")

            pattern_details = None
            recommended_patterns = []
            
            for article in pattern_articles:
                structured_data = article.get("structured_data", {})
                article_integration_type = structured_data.get("integration_type", "")
                article_providers = structured_data.get("providers", [])
                
                if article_integration_type != integration_type:
                    continue
                
                if cloud_provider and cloud_provider not in article_providers and "multi-cloud" not in article_providers:
                    continue
                
                pattern_data = self._article_to_pattern_dict(article)
                suitability = self._assess_pattern_suitability(pattern_data, components)
                
                quality_score_result = self.quality_scorer.score_pattern(pattern_data)
                quality_score = quality_score_result.overall_score
                
                validation_result = await self.validation_service.validate_pattern(pattern_data)
                validation_score = validation_result["score"]
                
                quality_assurance_result = await self.quality_assurance.assess_pattern(
                    article,
                    components,
                    cloud_provider,
                )
                
                recommended_patterns.append({
                    "name": structured_data.get("pattern_name", article.get("title", "")),
                    "description": pattern_data.get("description", ""),
                    "providers": pattern_data.get("providers", []),
                    "components": pattern_data.get("components", []),
                    "suitability": suitability,
                    "quality_score": quality_score,
                    "quality_breakdown": quality_score_result.score_breakdown,
                    "meets_quality_threshold": quality_score_result.meets_threshold,
                    "quality_recommendations": quality_score_result.recommendations,
                    "validation_score": validation_score,
                    "validation_checks": validation_result["checks"],
                    "meets_validation_threshold": validation_result["valid"],
                    "validation_recommendations": validation_result["recommendations"],
                    "quality_assurance": quality_assurance_result,
                    "article_id": article.get("article_id"),
                    "relevance_score": article.get("relevance_score", 0.0),
                })

            recommended_patterns.sort(
                key=lambda x: (
                    x.get("quality_score", 0) * 0.25 +
                    x.get("validation_score", 0) * 0.25 +
                    x.get("suitability", 0) * 0.30 +
                    x.get("relevance_score", 0) * 0.20
                ),
                reverse=True
            )
            
            discovered_patterns_info = []
            if repository_url:
                discovered_patterns_info = await self.discovery_service.get_discovery_summary(
                    repository_url,
                    integration_type,
                )
                if discovered_patterns_info:
                    logger.info(
                        "Found %d previously discovered patterns from repository %s",
                        len(discovered_patterns_info),
                        repository_url,
                    )

        dependencies = self._identify_dependencies(components, integration_type, cloud_provider)
        security_rules = self._generate_security_rules(integration_type, cloud_provider)
        monitoring = self._generate_monitoring_config(integration_type, cloud_provider)
        implementation_guidance = self._generate_implementation_guidance(
            components,
            integration_type,
            cloud_provider,
            pattern_name,
        )
        compliance_considerations = self._generate_compliance_considerations(
            integration_type,
            cloud_provider,
        )

        result = {
            "dependencies": dependencies,
            "security_rules": security_rules,
            "monitoring": monitoring,
            "implementation_guidance": implementation_guidance,
            "compliance_considerations": compliance_considerations,
        }

        if pattern_details:
            result["pattern_details"] = pattern_details
            if discovered_patterns_info:
                result["discovered_patterns"] = discovered_patterns_info
        else:
            result["recommended_patterns"] = recommended_patterns
            if discovered_patterns_info:
                result["discovered_patterns"] = discovered_patterns_info

        return result
    
    def _article_to_pattern_dict(self, article: dict[str, Any]) -> dict[str, Any]:
        """Convert knowledge article to pattern dictionary format.

        Args:
            article: Knowledge article dictionary

        Returns:
            Pattern dictionary compatible with quality scorer and validator
        """
        structured_data = article.get("structured_data", {})
        
        return {
            "description": article.get("summary", "") + "\n\n" + article.get("content", ""),
            "providers": structured_data.get("providers", []),
            "components": structured_data.get("components", []),
            "terraform_example": structured_data.get("terraform_example", ""),
            "kubernetes_example": structured_data.get("kubernetes_example", ""),
            "dependencies": structured_data.get("dependencies", []),
            "security_rules": structured_data.get("security_rules", []),
            "monitoring_config": structured_data.get("monitoring_config", {}),
            "implementation_guidance": structured_data.get("implementation_guidance", []),
            "compliance_considerations": structured_data.get("compliance_considerations", []),
        }

    def _assess_pattern_suitability(
        self,
        pattern: dict[str, Any],
        components: list[dict[str, Any]],
    ) -> int:
        """Assess how suitable a pattern is for given components.

        Args:
            pattern: Pattern dictionary
            components: List of components

        Returns:
            Suitability score (0-100)
        """
        pattern_components = pattern.get("components", [])
        component_types = [comp.get("type", "").lower() for comp in components]

        matches = sum(1 for pc in pattern_components if any(pc.lower() in ct or ct in pc.lower() for ct in component_types))
        return int((matches / max(len(pattern_components), 1)) * 100)

    def _identify_dependencies(
        self,
        components: list[dict[str, Any]],
        integration_type: str,
        cloud_provider: str,
    ) -> list[str]:
        """Identify dependencies required for integration.

        Args:
            components: List of components
            integration_type: Type of integration
            cloud_provider: Cloud provider

        Returns:
            List of dependency descriptions
        """
        dependencies = []

        if integration_type == "networking":
            dependencies.append("Network connectivity between components")
            if cloud_provider == "aws":
                dependencies.append("VPC configuration")
                dependencies.append("Security groups or network ACLs")
            elif cloud_provider == "kubernetes":
                dependencies.append("Network policies")
                dependencies.append("Service mesh (optional)")

        if integration_type == "security":
            dependencies.append("IAM roles/service accounts")
            dependencies.append("Secrets management")
            dependencies.append("Encryption keys")

        if integration_type == "service":
            dependencies.append("Service discovery mechanism")
            dependencies.append("Load balancing configuration")
            dependencies.append("Health check endpoints")

        if integration_type == "monitoring":
            dependencies.append("Monitoring agent/service")
            dependencies.append("Metrics collection endpoint")
            dependencies.append("Log aggregation system")

        return dependencies

    def _generate_security_rules(
        self,
        integration_type: str,
        cloud_provider: str,
    ) -> list[str]:
        """Generate security rules and best practices for integration.

        Args:
            integration_type: Type of integration
            cloud_provider: Cloud provider

        Returns:
            List of security rules
        """
        rules = []

        if integration_type == "networking":
            rules.append("Restrict network access to necessary ports only")
            rules.append("Use security groups/network policies for access control")
            rules.append("Enable encryption in transit (TLS/SSL)")
            rules.append("Implement network segmentation")
            rules.append("Use private endpoints where possible")

        if integration_type == "security":
            rules.append("Implement least privilege access")
            rules.append("Use IAM roles/service accounts (avoid hardcoded credentials)")
            rules.append("Enable audit logging for all access")
            rules.append("Rotate credentials regularly")
            rules.append("Use secrets management service")

        if integration_type == "service":
            rules.append("Use secure communication protocols (HTTPS, gRPC with TLS)")
            rules.append("Implement authentication and authorization")
            rules.append("Enable request validation and rate limiting")
            rules.append("Use API keys or OAuth tokens")
            rules.append("Implement circuit breakers for resilience")

        if integration_type == "monitoring":
            rules.append("Sanitize logs to remove sensitive data")
            rules.append("Encrypt monitoring data in transit")
            rules.append("Restrict access to monitoring dashboards")
            rules.append("Implement alerting for security events")

        return rules

    def _generate_monitoring_config(
        self,
        integration_type: str,
        cloud_provider: str,
    ) -> dict[str, Any]:
        """Generate monitoring configuration recommendations.

        Args:
            integration_type: Type of integration
            cloud_provider: Cloud provider

        Returns:
            Monitoring configuration dictionary
        """
        config = {
            "metrics": [],
            "alarms": [],
            "logs": [],
            "recommendations": [],
        }

        if cloud_provider == "aws":
            config["metrics"].append("Integration latency (p50, p95, p99)")
            config["metrics"].append("Error rate (4xx, 5xx)")
            config["metrics"].append("Request throughput")
            config["metrics"].append("Connection pool utilization")
            config["alarms"].append("High error rate alarm (> 1% for 5 minutes)")
            config["alarms"].append("Latency alarm (p95 > 1 second)")
            config["logs"].append("CloudWatch Logs with structured logging")
            config["recommendations"].append("Use CloudWatch Insights for log analysis")
            config["recommendations"].append("Set up X-Ray for distributed tracing")

        if cloud_provider == "kubernetes":
            config["metrics"].append("Request rate (requests/second)")
            config["metrics"].append("Response time (p50, p95, p99)")
            config["metrics"].append("Pod restart count")
            config["metrics"].append("Resource utilization (CPU, memory)")
            config["alarms"].append("Pod restart alarm (> 3 restarts in 5 minutes)")
            config["alarms"].append("High error rate alarm")
            config["logs"].append("Kubernetes logs via fluentd/fluent-bit")
            config["recommendations"].append("Use Prometheus for metrics collection")
            config["recommendations"].append("Use Grafana for visualization")

        if cloud_provider in ["gcp", "azure"]:
            config["metrics"].append("Integration latency")
            config["metrics"].append("Error rate")
            config["metrics"].append("Request throughput")
            config["alarms"].append("High error rate alarm")
            config["logs"].append("Cloud logging (GCP) or Application Insights (Azure)")
            config["recommendations"].append("Use cloud-native monitoring services")

        return config

    def _generate_implementation_guidance(
        self,
        components: list[dict[str, Any]],
        integration_type: str,
        cloud_provider: str,
        pattern_name: str | None,
    ) -> list[str]:
        """Generate step-by-step implementation guidance.

        Args:
            components: List of components
            integration_type: Type of integration
            cloud_provider: Cloud provider
            pattern_name: Optional pattern name

        Returns:
            List of implementation steps
        """
        component_names = [comp.get("id", comp.get("type", "component")) for comp in components]
        guidance = []

        if integration_type == "networking":
            guidance.append(f"1. Identify network requirements between {', '.join(component_names)}")
            if cloud_provider == "aws":
                guidance.append("2. Create or configure VPC and subnets")
                guidance.append("3. Configure security groups with least privilege rules")
                guidance.append("4. Set up route tables and network ACLs")
                guidance.append("5. Test connectivity between components")
            elif cloud_provider == "kubernetes":
                guidance.append("2. Configure network policies for pod-to-pod communication")
                guidance.append("3. Set up service mesh (Istio/Linkerd) if needed")
                guidance.append("4. Configure ingress/egress rules")
                guidance.append("5. Verify network connectivity")

        if integration_type == "security":
            guidance.append(f"1. Create IAM roles/service accounts for {', '.join(component_names)}")
            guidance.append("2. Configure least privilege access policies")
            guidance.append("3. Set up secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)")
            guidance.append("4. Enable encryption at rest and in transit")
            guidance.append("5. Configure audit logging")
            guidance.append("6. Test access controls")

        if integration_type == "service":
            guidance.append(f"1. Configure service discovery for {', '.join(component_names)}")
            guidance.append("2. Set up load balancing")
            guidance.append("3. Implement health check endpoints")
            guidance.append("4. Configure retry logic and circuit breakers")
            guidance.append("5. Set up API gateway if needed")
            guidance.append("6. Test service communication")

        if integration_type == "monitoring":
            guidance.append(f"1. Install monitoring agents on {', '.join(component_names)}")
            guidance.append("2. Configure metrics collection")
            guidance.append("3. Set up log aggregation")
            guidance.append("4. Create dashboards for visualization")
            guidance.append("5. Configure alerting rules")
            guidance.append("6. Test monitoring pipeline")

        if pattern_name:
            guidance.append(f"\nNote: Consider using the '{pattern_name}' pattern for this integration type.")

        return guidance

    def _generate_compliance_considerations(
        self,
        integration_type: str,
        cloud_provider: str,
    ) -> list[str]:
        """Generate compliance considerations for integration.

        Args:
            integration_type: Type of integration
            cloud_provider: Cloud provider

        Returns:
            List of compliance considerations
        """
        considerations = []

        if integration_type == "networking":
            considerations.append("PCI-DSS: Ensure network segmentation for cardholder data")
            considerations.append("HIPAA: Encrypt all PHI in transit")
            considerations.append("SOC2: Document network access controls")
            considerations.append("GDPR: Ensure data transfer mechanisms comply with regulations")

        if integration_type == "security":
            considerations.append("PCI-DSS: Implement strong access controls")
            considerations.append("HIPAA: Use role-based access control (RBAC)")
            considerations.append("SOC2: Enable audit logging for all access")
            considerations.append("NIST: Follow least privilege principle")

        if integration_type == "service":
            considerations.append("PCI-DSS: Secure API endpoints")
            considerations.append("HIPAA: Encrypt service-to-service communication")
            considerations.append("SOC2: Implement authentication and authorization")
            considerations.append("GDPR: Ensure data processing agreements are in place")

        return considerations

