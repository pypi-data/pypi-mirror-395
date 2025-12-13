"""Unified infrastructure lifecycle management tool - design, integration, and operations."""

import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.integration_analyzer import IntegrationAnalyzer
from wistx_mcp.tools.lib.integration_generator import IntegrationPatternAdvisor
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota
from wistx_mcp.tools.lib.constants import (
    COMPLIANCE_FETCH_TIMEOUT_SECONDS,
    COMPLIANCE_FETCH_MAX_ATTEMPTS,
    VISUALIZATION_GENERATION_TIMEOUT_SECONDS,
)
from wistx_mcp.tools import visualize_infra_flow

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def manage_infrastructure_lifecycle(
    action: str,
    infrastructure_type: str | None = None,
    resource_name: str | None = None,
    infrastructure_code: str | None = None,
    components: list[dict[str, Any]] | None = None,
    integration_type: str | None = None,
    cloud_provider: str | list[str] | None = None,
    configuration: dict[str, Any] | None = None,
    compliance_standards: list[str] | None = None,
    pattern_name: str | None = None,
    current_version: str | None = None,
    target_version: str | None = None,
    backup_type: str = "full",
    repository_url: str | None = None,
    api_key: str = "",
) -> dict[str, Any]:
    """Unified infrastructure lifecycle management - design, integration, and operations.

    This tool provides end-to-end infrastructure management capabilities:
    - Design & Analysis: Analyze existing infrastructure, design new infrastructure
    - Integration Management: Recommend integration patterns, validate integrations
    - Lifecycle Operations: Create, update, upgrade, backup, restore, monitor, optimize

    NOTE: This tool does NOT generate code. It provides analysis, recommendations, patterns,
    and guidance. Use an LLM to generate code based on these recommendations.

    Args:
        action: Action to perform:
            Design & Analysis:
                - "analyze": Analyze existing infrastructure code for issues
                - "design": Design new infrastructure with integration recommendations
                - "validate": Validate infrastructure design or integration
            Integration Management:
                - "integrate": Recommend integration patterns for components
                - "analyze_integration": Analyze integration patterns in existing code
            Lifecycle Operations:
                - "create": Create infrastructure resources
                - "update": Update infrastructure configuration
                - "upgrade": Upgrade infrastructure versions
                - "backup": Backup infrastructure state
                - "restore": Restore from backup
                - "monitor": Monitor infrastructure health
                - "optimize": Optimize infrastructure performance
        infrastructure_type: Type of infrastructure (kubernetes, multi_cloud, hybrid_cloud)
            Required for lifecycle operations (create, update, upgrade, etc.)
        resource_name: Name of the resource/cluster
            Required for lifecycle operations
        infrastructure_code: Infrastructure code to analyze (for analyze/design actions)
        components: List of components to integrate (for integrate action)
            Example: [
                {"type": "ec2", "id": "web-server"},
                {"type": "rds", "id": "database"}
            ]
        integration_type: Type of integration (networking, security, monitoring, service)
            Required for integrate action
        cloud_provider: Cloud provider(s) - single string or list for multi-cloud
        configuration: Infrastructure configuration (for lifecycle operations)
        compliance_standards: Compliance standards to consider
        pattern_name: Specific integration pattern to use (optional)
        current_version: Current version (for upgrade action)
        target_version: Target version (for upgrade action)
        backup_type: Type of backup (for backup action)
        repository_url: Repository URL for context-aware operations (optional)

    Returns:
        Dictionary with results based on action:
        - Design & Analysis: missing_connections, dependency_issues, recommendations, visualization
        - Integration: recommended_patterns, dependencies, security_rules, monitoring, implementation_guidance
        - Lifecycle: resource_id, status, endpoints, compliance_status, cost_summary, recommendations

    Raises:
        ValueError: If invalid action or parameters
        Exception: If operation fails
    """
    design_actions = ["analyze", "design", "validate"]
    integration_actions = ["integrate", "analyze_integration"]
    lifecycle_actions = ["create", "update", "upgrade", "backup", "restore", "monitor", "optimize"]
    
    valid_actions = design_actions + integration_actions + lifecycle_actions
    if action not in valid_actions:
        raise ValueError(
            f"Invalid action: {action}. Must be one of {valid_actions}. "
            f"Design: {design_actions}, Integration: {integration_actions}, Lifecycle: {lifecycle_actions}"
        )

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id
    from wistx_mcp.tools.lib.input_sanitizer import validate_infrastructure_code_input

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    if infrastructure_code:
        validate_infrastructure_code_input(infrastructure_code)

    logger.info(
        "Managing infrastructure lifecycle: action=%s, type=%s, resource=%s, provider=%s",
        action,
        infrastructure_type,
        resource_name,
        cloud_provider,
    )

    try:
        async with MongoDBClient() as mongodb_client:
            analyzer = IntegrationAnalyzer()
            from wistx_mcp.tools.lib.vector_search import VectorSearch
            from wistx_mcp.config import settings
            vector_search = VectorSearch(
                mongodb_client,
                gemini_api_key=settings.gemini_api_key,
                pinecone_api_key=settings.pinecone_api_key,
                pinecone_index_name=settings.pinecone_index_name,
            )
            advisor = IntegrationPatternAdvisor(mongodb_client=mongodb_client, vector_search=vector_search)

            if action in design_actions:
                return await _handle_design_actions(
                    action=action,
                    infrastructure_code=infrastructure_code,
                    components=components,
                    integration_type=integration_type,
                    cloud_provider=cloud_provider,
                    compliance_standards=compliance_standards,
                    api_key=api_key,
                    analyzer=analyzer,
                )

            elif action in integration_actions:
                return await _handle_integration_actions(
                    action=action,
                    infrastructure_code=infrastructure_code,
                    components=components,
                    integration_type=integration_type,
                    cloud_provider=cloud_provider,
                    pattern_name=pattern_name,
                    repository_url=repository_url,
                    api_key=api_key,
                    analyzer=analyzer,
                    advisor=advisor,
                )

            elif action in lifecycle_actions:
                missing_params = []
                if not infrastructure_type:
                    missing_params.append("infrastructure_type")
                if not resource_name:
                    missing_params.append("resource_name")
                
                if missing_params:
                    error_msg = (
                        f"Missing required parameters for '{action}' action: {', '.join(missing_params)}. "
                    )
                    if action == "upgrade":
                        error_msg += (
                            "For upgrade action, also provide: current_version, target_version. "
                        )
                    elif action == "backup":
                        error_msg += (
                            "For backup action, backup_type is optional (default: 'full'). "
                        )
                    error_msg += (
                        f"Valid infrastructure_type values: kubernetes, multi_cloud, hybrid_cloud. "
                        f"Example: manage_infrastructure_lifecycle("
                        f"action='{action}', "
                        f"infrastructure_type='kubernetes', "
                        f"resource_name='my-cluster', "
                        f"api_key='YOUR_API_KEY'"
                        f")"
                    )
                    raise ValueError(error_msg)

                return await _handle_lifecycle_actions(
                    action=action,
                    infrastructure_type=infrastructure_type,
                    resource_name=resource_name,
                    cloud_provider=cloud_provider,
                    configuration=configuration,
                    compliance_standards=compliance_standards,
                    current_version=current_version,
                    target_version=target_version,
                    backup_type=backup_type,
                    api_key=api_key,
                )

            else:
                raise ValueError(f"Unknown action: {action}")

    except Exception as e:
        logger.error("Error in manage_infrastructure_lifecycle: %s", e, exc_info=True)
        raise


async def _handle_design_actions(
    action: str,
    infrastructure_code: str | None,
    components: list[dict[str, Any]] | None,
    integration_type: str | None,
    cloud_provider: str | None,
    compliance_standards: list[str] | None,
    api_key: str,
    analyzer: IntegrationAnalyzer,
) -> dict[str, Any]:
    """Handle design and analysis actions."""
    if action == "analyze":
        if not infrastructure_code:
            raise ValueError("infrastructure_code required for analyze action")

        analysis = await analyzer.analyze(
            infrastructure_code=infrastructure_code,
            cloud_provider=cloud_provider,
            api_key=api_key,
        )

        if compliance_standards:
            try:
                from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
                
                resource_types = _extract_resource_types(infrastructure_code)
                compliance_results = await with_timeout_and_retry(
                    api_client.get_compliance_requirements,
                    timeout_seconds=COMPLIANCE_FETCH_TIMEOUT_SECONDS,
                    max_attempts=COMPLIANCE_FETCH_MAX_ATTEMPTS,
                    retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                    resource_types=resource_types,
                    standards=compliance_standards,
                )
                analysis["compliance_status"] = compliance_results.get("controls", [])
            except (RuntimeError, ConnectionError, TimeoutError) as e:
                logger.warning("Failed to fetch compliance requirements: %s", e)

        result = {
            "action": "analyze",
            "missing_connections": analysis.get("missing_connections", []),
            "dependency_issues": analysis.get("dependency_issues", []),
            "security_gaps": analysis.get("security_gaps", []),
            "recommendations": analysis.get("recommendations", []),
            "compliance_status": analysis.get("compliance_status"),
        }

        try:
            import asyncio
            from wistx_mcp.tools.lib.retry_utils import with_timeout
            
            visualization_result = await with_timeout(
                visualize_infra_flow.visualize_infra_flow,
                timeout_seconds=VISUALIZATION_GENERATION_TIMEOUT_SECONDS,
                infrastructure_code=infrastructure_code,
                infrastructure_type=None,
                visualization_type="dependencies",
                format="mermaid",
                include_resources=True,
                include_networking=True,
                depth=3,
            )
            result["visualization"] = visualization_result.get("visualization", "")
            result["components"] = visualization_result.get("components", [])
        except asyncio.TimeoutError:
            logger.warning("Visualization generation timed out")
        except Exception as e:
            logger.warning("Failed to generate visualization: %s", e)

        return result

    elif action == "design":
        if not components:
            raise ValueError("components required for design action")
        if not cloud_provider:
            detected_provider = _detect_cloud_provider_from_components(components)
            if detected_provider:
                cloud_provider = detected_provider
                logger.info("Auto-detected cloud_provider '%s' from components for design action", cloud_provider)
            else:
                cloud_provider = "multi-cloud"
                logger.info("Could not detect cloud_provider from components, defaulting to 'multi-cloud' for design action")

        design_recommendations = {
            "action": "design",
            "components": components,
            "cloud_provider": cloud_provider,
            "recommendations": [],
        }

        if integration_type:
            async with MongoDBClient() as mongodb_client:
                from wistx_mcp.tools.lib.vector_search import VectorSearch
                from wistx_mcp.config import settings
                vector_search = VectorSearch(
                    mongodb_client,
                    gemini_api_key=settings.gemini_api_key,
                    pinecone_api_key=settings.pinecone_api_key,
                    pinecone_index_name=settings.pinecone_index_name,
                )
                advisor = IntegrationPatternAdvisor(mongodb_client=mongodb_client, vector_search=vector_search)
                integration_recommendations = await advisor.recommend_patterns(
                    components=components,
                    integration_type=integration_type,
                    cloud_provider=cloud_provider,
                    repository_url=repository_url,
                )
            design_recommendations["integration_recommendations"] = integration_recommendations

        if compliance_standards:
            try:
                resource_types = []
                for comp in components:
                    comp_type = comp.get("type", "")
                    if comp_type:
                        resource_types.append(comp_type.upper())
                    services = comp.get("services", [])
                    if isinstance(services, list):
                        for service in services:
                            if isinstance(service, str) and service.upper() not in resource_types:
                                resource_types.append(service.upper())
                
                if resource_types:
                    compliance_results = await api_client.get_compliance_requirements(
                        resource_types=resource_types,
                        standards=compliance_standards,
                        api_key=api_key,
                    )
                    design_recommendations["compliance_requirements"] = compliance_results.get("controls", [])
            except Exception as e:
                logger.warning("Failed to fetch compliance requirements: %s", e)

        design_recommendations["recommendations"].append(
            "Use an LLM to generate infrastructure code based on these recommendations"
        )

        return design_recommendations

    elif action == "validate":
        if not components:
            raise ValueError("components required for validate action")
        if not integration_type:
            raise ValueError("integration_type required for validate action")

        validation = analyzer.validate_integration(
            components=components,
            integration_type=integration_type,
        )

        return {
            "action": "validate",
            "valid": validation.get("valid", False),
            "issues": validation.get("issues", []),
            "fixes": validation.get("fixes", []),
        }


async def _handle_integration_actions(
    action: str,
    infrastructure_code: str | None,
    components: list[dict[str, Any]] | None,
    integration_type: str | None,
    cloud_provider: str | None,
    pattern_name: str | None,
    repository_url: str | None,
    api_key: str,
    analyzer: IntegrationAnalyzer,
    advisor: IntegrationPatternAdvisor,
) -> dict[str, Any]:
    """Handle integration management actions."""
    if action == "integrate":
        if not components:
            raise ValueError("components required for integrate action")
        if not integration_type:
            raise ValueError("integration_type required for integrate action")
        if not cloud_provider:
            detected_provider = _detect_cloud_provider_from_components(components)
            if detected_provider:
                cloud_provider = detected_provider
                logger.info("Auto-detected cloud_provider '%s' from components for integrate action", cloud_provider)
            else:
                cloud_provider = "multi-cloud"
                logger.info("Could not detect cloud_provider from components, defaulting to 'multi-cloud' for integrate action")

        recommendations = await advisor.recommend_patterns(
            components=components,
            integration_type=integration_type,
            cloud_provider=cloud_provider,
            pattern_name=pattern_name,
            repository_url=repository_url,
        )

        result = {
            "action": "integrate",
            "dependencies": recommendations.get("dependencies", []),
            "security_rules": recommendations.get("security_rules", []),
            "monitoring": recommendations.get("monitoring", {}),
            "implementation_guidance": recommendations.get("implementation_guidance", []),
            "compliance_considerations": recommendations.get("compliance_considerations", []),
        }

        if recommendations.get("pattern_details"):
            result["pattern_details"] = recommendations["pattern_details"]
        else:
            result["recommended_patterns"] = recommendations.get("recommended_patterns", [])

        return result

    elif action == "analyze_integration":
        if not infrastructure_code:
            raise ValueError("infrastructure_code required for analyze_integration action")

        analysis = await analyzer.analyze(
            infrastructure_code=infrastructure_code,
            cloud_provider=cloud_provider,
            api_key=api_key,
        )

        return {
            "action": "analyze_integration",
            "missing_connections": analysis.get("missing_connections", []),
            "dependency_issues": analysis.get("dependency_issues", []),
            "security_gaps": analysis.get("security_gaps", []),
            "recommendations": analysis.get("recommendations", []),
        }


async def _handle_lifecycle_actions(
    action: str,
    infrastructure_type: str,
    resource_name: str,
    cloud_provider: str | list[str] | None,
    configuration: dict[str, Any] | None,
    compliance_standards: list[str] | None,
    current_version: str | None,
    target_version: str | None,
    backup_type: str,
    api_key: str,
) -> dict[str, Any]:
    """Handle infrastructure lifecycle operations."""
    valid_types = ["kubernetes", "multi_cloud", "hybrid_cloud"]
    if infrastructure_type not in valid_types:
        raise ValueError(f"Invalid infrastructure_type: {infrastructure_type}. Must be one of {valid_types}")

    api_response = await api_client.manage_infrastructure(
        action=action,
        infrastructure_type=infrastructure_type,
        resource_name=resource_name,
        cloud_provider=cloud_provider,
        configuration=configuration,
        compliance_standards=compliance_standards,
        current_version=current_version,
        target_version=target_version,
        backup_type=backup_type,
        api_key=api_key,
    )

    if api_response.get("data"):
        return api_response["data"]
    return api_response


def _detect_cloud_provider_from_components(components: list[dict[str, Any]]) -> str | None:
    """Detect cloud provider from component types and services.
    
    Args:
        components: List of component dictionaries
        
    Returns:
        Detected cloud provider (aws, gcp, azure, kubernetes, multi-cloud) or None
    """
    detected_providers = set()
    
    for comp in components:
        comp_type = comp.get("type", "").lower()
        comp_name = comp.get("name", "").lower()
        services = comp.get("services", [])
        
        if isinstance(services, str):
            services = [services]
        if not isinstance(services, list):
            services = []
        
        if "multi-cloud" in comp_name or "multi_cloud" in comp_name or "multicloud" in comp_name:
            return "multi-cloud"
        
        text_to_check = f"{comp_type} {comp_name} {' '.join(str(s).lower() for s in services)}"
        
        if "eks" in text_to_check or ("aws" in text_to_check and "kubernetes" in text_to_check):
            detected_providers.add("aws")
        elif "gke" in text_to_check or ("gcp" in text_to_check and "kubernetes" in text_to_check):
            detected_providers.add("gcp")
        elif "aks" in text_to_check or ("azure" in text_to_check and "kubernetes" in text_to_check):
            detected_providers.add("azure")
        elif "kubernetes" in comp_type or "k8s" in comp_type:
            if "eks" in text_to_check:
                detected_providers.add("aws")
            elif "gke" in text_to_check:
                detected_providers.add("gcp")
            elif "aks" in text_to_check:
                detected_providers.add("azure")
            elif not services:
                detected_providers.add("kubernetes")
        
        for service in services:
            if isinstance(service, str):
                service_upper = service.upper()
                if service_upper in ["EKS", "EC2", "RDS", "S3", "LAMBDA", "VPC", "ELASTICACHE", "CLOUDFRONT"]:
                    detected_providers.add("aws")
                elif service_upper in ["GKE", "GCE", "CLOUD SQL", "CLOUD STORAGE", "CLOUD FUNCTIONS", "CLOUD MEMORYSTORE"]:
                    detected_providers.add("gcp")
                elif service_upper in ["AKS", "AZURE SQL", "BLOB STORAGE", "AZURE FUNCTIONS", "REDIS CACHE", "AZURE CACHE FOR REDIS"]:
                    detected_providers.add("azure")
    
    if len(detected_providers) > 1:
        return "multi-cloud"
    elif len(detected_providers) == 1:
        return list(detected_providers)[0]
    elif any("kubernetes" in str(comp.get("type", "")).lower() for comp in components):
        return "kubernetes"
    
    return None


def _extract_resource_types(infrastructure_code: str) -> list[str]:
    """Extract resource types from infrastructure code.

    Args:
        infrastructure_code: Infrastructure code

    Returns:
        List of resource types
    """
    resource_types = []

    aws_resources = [
        ("aws_instance", "EC2"),
        ("aws_rds_instance", "RDS"),
        ("aws_s3_bucket", "S3"),
        ("aws_lambda_function", "Lambda"),
        ("aws_eks_cluster", "EKS"),
        ("aws_ecs_service", "ECS"),
    ]

    for pattern, resource_type in aws_resources:
        if pattern in infrastructure_code:
            resource_types.append(resource_type)

    if "kubernetes" in infrastructure_code.lower() or "kind:" in infrastructure_code.lower():
        resource_types.append("EKS")
        resource_types.append("GKE")
        resource_types.append("AKS")

    return resource_types if resource_types else ["EC2"]

