"""Architecture service - business logic for architecture design operations."""

import hashlib
import json
import logging
from typing import Any

from api.models.v1_requests import ArchitectureDesignRequest
from api.models.v1_responses import ArchitectureDesignResponse
from api.services.architecture_cache_service import architecture_cache_service
from api.models.architecture_cache import generate_cache_key
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.architecture_templates import ArchitectureTemplates
from wistx_mcp.tools.lib.template_validator import TemplateValidator
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from api.config import settings
from api.exceptions import ValidationError, ExternalServiceError

logger = logging.getLogger(__name__)


class ArchitectureService:
    """Service for architecture design operations."""

    def __init__(self):
        """Initialize architecture service."""
        self.mongodb_adapter = None
        self.api_client = WISTXAPIClient()

    async def design_architecture(
        self,
        request: ArchitectureDesignRequest,
        api_key: str,
        user_id: str | None = None,
        organization_id: str | None = None,
        use_cache: bool = True,
    ) -> ArchitectureDesignResponse:
        """Design architecture for DevOps/infrastructure projects.

        Args:
            request: Architecture design request
            api_key: API key for authentication
            user_id: User ID (optional, will be fetched if not provided)
            organization_id: Organization ID (optional)
            use_cache: Whether to use cache (default: True)

        Returns:
            Architecture design response

        Raises:
            ValueError: If invalid parameters
            RuntimeError: If operation fails
        """
        logger.info(
            "Designing architecture: action=%s, project_type=%s, project_name=%s",
            request.action,
            request.project_type,
            request.project_name,
        )

        if not user_id:
            try:
                user_info = await self.api_client.get_current_user(api_key=api_key)
                user_id = user_info.get("user_id")
                organization_id = organization_id or user_info.get("organization_id")
            except Exception as e:
                logger.warning("Could not fetch user_id from API key: %s", e)

        requirements_hash = None
        if request.requirements:
            requirements_str = json.dumps(request.requirements, sort_keys=True)
            requirements_hash = hashlib.sha256(requirements_str.encode()).hexdigest()[:16]

        cache_key = None
        if user_id and use_cache:
            cache_key = generate_cache_key(
                action=request.action,
                user_id=user_id,
                project_type=request.project_type,
                architecture_type=request.architecture_type,
                cloud_provider=request.cloud_provider,
                compliance_standards=request.compliance_standards,
                requirements=request.requirements,
            )

            cached_result = await architecture_cache_service.get_cached_design(
                cache_key=cache_key,
                user_id=user_id,
            )

            if cached_result:
                logger.info("Returning cached architecture design: key=%s", cache_key[:16])
                return ArchitectureDesignResponse(**cached_result)

        mongodb_client = MongoDBClient()
        await mongodb_client.connect()

        try:
            if request.action == "initialize":
                if not request.project_type or not request.project_name:
                    raise ValidationError(
                        message="project_type and project_name are required for initialize",
                        user_message="Project type and project name are required to initialize architecture",
                        error_code="MISSING_REQUIRED_FIELDS",
                        details={"action": request.action, "missing_fields": ["project_type", "project_name"]}
                    )

                templates = ArchitectureTemplates(mongodb_client)
                template = await templates.get_template(
                    project_type=request.project_type,
                    architecture_type=request.architecture_type,
                    cloud_provider=request.cloud_provider,
                    template_id=request.template_id,
                    github_url=request.github_url,
                    user_template=request.user_template,
                )

                validator = TemplateValidator()
                validation_result = validator.validate_template(template)

                if not validation_result["valid"]:
                    if validation_result["errors"]:
                        raise ValidationError(
                            message=f"Invalid template: {', '.join(validation_result['errors'])}",
                            user_message=f"Template validation failed: {', '.join(validation_result['errors'])}",
                            error_code="INVALID_TEMPLATE",
                            details={"errors": validation_result["errors"]}
                        )

                compliance_context = None
                if request.include_compliance and request.compliance_standards:
                    try:
                        compliance_results = await self.api_client.get_compliance_requirements(
                            resource_types=["RDS", "EC2", "S3"],
                            standards=request.compliance_standards,
                        )
                        compliance_context = {
                            "standards": request.compliance_standards,
                            "controls": compliance_results.get("controls", []),
                        }
                    except Exception as e:
                        logger.warning("Failed to fetch compliance requirements: %s", e)

                vector_search = VectorSearch(
                    mongodb_client,
                    gemini_api_key=settings.gemini_api_key,
                    pinecone_api_key=settings.pinecone_api_key,
                    pinecone_index_name=settings.pinecone_index_name,
                )

                best_practices = []
                if request.include_best_practices:
                    try:
                        practices = await vector_search.search_knowledge_articles(
                            query=f"{request.project_type} best practices",
                            domains=["devops", "infrastructure"],
                            limit=10,
                        )
                        best_practices = [
                            {
                                "title": p.get("title", ""),
                                "description": p.get("summary", ""),
                            }
                            for p in practices
                        ]
                    except Exception as e:
                        logger.warning("Failed to fetch best practices: %s", e)

                response = ArchitectureDesignResponse(
                    action=request.action,
                    project_name=request.project_name,
                    architecture={
                        "template": template,
                        "structure": template.get("structure", {}),
                    },
                    templates=[{"template_id": request.template_id}] if request.template_id else [],
                    compliance_context=compliance_context,
                    security_context={"enabled": request.include_security} if request.include_security else None,
                    best_practices=best_practices,
                    recommendations=["Review generated files", "Test infrastructure"],
                    output_files=[],
                )

                if cache_key and user_id and use_cache:
                    try:
                        await architecture_cache_service.cache_design(
                            cache_key=cache_key,
                            user_id=user_id,
                            organization_id=organization_id,
                            action=request.action,
                            project_type=request.project_type,
                            architecture_type=request.architecture_type,
                            cloud_provider=request.cloud_provider,
                            compliance_standards=request.compliance_standards,
                            requirements_hash=requirements_hash,
                            design_result=response.model_dump(),
                            metadata={
                                "project_name": request.project_name,
                                "template_id": request.template_id,
                            },
                        )
                    except Exception as e:
                        logger.warning("Failed to cache design result: %s", e, exc_info=True)

                return response

            elif request.action == "design":
                try:
                    templates = ArchitectureTemplates(mongodb_client)
                    project_type = request.project_type or "devops"
                    template = await templates.get_template(
                        project_type=project_type,
                        architecture_type=request.architecture_type,
                        cloud_provider=request.cloud_provider,
                        template_id=request.template_id,
                        github_url=request.github_url,
                        user_template=request.user_template,
                    )
                except Exception as e:
                    logger.error("Failed to get template: %s", e, exc_info=True)
                    raise ExternalServiceError(
                        message=f"Failed to get template: {e}",
                        user_message="Unable to retrieve architecture template. Please try again later.",
                        error_code="TEMPLATE_FETCH_ERROR",
                        details={"error": str(e)}
                    ) from e

                vector_search = None
                if request.include_security or request.include_best_practices:
                    try:
                        vector_search = VectorSearch(
                            mongodb_client,
                            gemini_api_key=settings.gemini_api_key,
                            pinecone_api_key=settings.pinecone_api_key,
                            pinecone_index_name=settings.pinecone_index_name,
                        )
                    except Exception as e:
                        logger.warning("Failed to initialize VectorSearch: %s", e)
                        vector_search = None

                compliance_context = None
                if request.include_compliance and request.compliance_standards:
                    try:
                        resource_types = []
                        if request.project_type:
                            resource_types.append(request.project_type.upper())
                        if request.cloud_provider and request.cloud_provider != "multi-cloud":
                            resource_types.append(request.cloud_provider.upper())

                        compliance_results = await self.api_client.get_compliance_requirements(
                            resource_types=resource_types if resource_types else ["EC2", "S3", "RDS"],
                            standards=request.compliance_standards,
                        )
                        if compliance_results and isinstance(compliance_results, dict):
                            compliance_context = {
                                "standards": request.compliance_standards,
                                "controls": compliance_results.get("controls", []),
                                "summary": compliance_results.get("summary", {}),
                            }
                        else:
                            logger.warning("Unexpected compliance results format: %s", type(compliance_results))
                            compliance_context = {
                                "standards": request.compliance_standards,
                                "controls": [],
                                "summary": {},
                            }
                    except Exception as e:
                        logger.warning("Failed to fetch compliance requirements: %s", e)

                security_context = None
                if request.include_security and vector_search:
                    try:
                        security_query = f"{request.project_type or 'infrastructure'} security best practices"
                        if request.cloud_provider and request.cloud_provider != "multi-cloud":
                            security_query += f" {request.cloud_provider}"
                        if request.architecture_type:
                            security_query += f" {request.architecture_type}"

                        security_articles = await vector_search.search_knowledge_articles(
                            query=security_query,
                            domains=["security", "devops"],
                            limit=10,
                        )
                        security_context = {
                            "enabled": True,
                            "results": [
                                {
                                    "title": article.get("title", ""),
                                    "summary": article.get("summary", ""),
                                    "domain": article.get("domain", ""),
                                }
                                for article in (security_articles or [])
                            ],
                        }
                    except Exception as e:
                        logger.warning("Failed to fetch security context: %s", e)
                        security_context = {"enabled": False}
                elif request.include_security:
                    security_context = {"enabled": False}

                best_practices = []
                if request.include_best_practices and vector_search:
                    try:
                        best_practices_query = f"{request.architecture_type or 'architecture'} {request.project_type or 'infrastructure'}"
                        if request.cloud_provider and request.cloud_provider != "multi-cloud":
                            best_practices_query += f" {request.cloud_provider}"
                        best_practices_query += " production best practices"

                        practices = await vector_search.search_knowledge_articles(
                            query=best_practices_query,
                            domains=["devops", "infrastructure", "architecture"],
                            limit=15,
                        )
                        best_practices = [
                            {
                                "title": p.get("title", ""),
                                "description": p.get("summary", ""),
                                "domain": p.get("domain", ""),
                            }
                            for p in (practices or [])
                        ]
                    except Exception as e:
                        logger.warning("Failed to fetch best practices: %s", e)

                recommendations = []
                if request.architecture_type == "microservices":
                    recommendations.extend([
                        "Use service mesh for inter-service communication",
                        "Implement centralized logging and monitoring",
                        "Set up distributed tracing",
                        "Configure auto-scaling for high availability",
                    ])
                if request.requirements:
                    if request.requirements.get("scalability") == "high":
                        recommendations.append("Consider horizontal scaling with load balancers")
                    if request.requirements.get("availability") and "99.9" in str(request.requirements.get("availability")):
                        recommendations.append("Implement multi-AZ deployment for high availability")
                    if request.requirements.get("security") == "high":
                        recommendations.append("Enable encryption at rest and in transit")
                        recommendations.append("Implement network segmentation and firewall rules")
                    if request.requirements.get("cost") == "optimized":
                        recommendations.append("Use reserved instances for predictable workloads")
                        recommendations.append("Implement auto-scaling to reduce costs during low traffic")

                if request.cloud_provider == "multi-cloud":
                    recommendations.extend([
                        "Implement cloud-agnostic abstractions for portability",
                        "Use multi-cloud management tools for unified operations",
                        "Design for cloud-specific optimizations where beneficial",
                    ])

                if compliance_context and compliance_context.get("controls"):
                    recommendations.append(f"Applied {len(compliance_context['controls'])} compliance controls")

                try:
                    components = self._get_architecture_components(request.architecture_type)
                except Exception as e:
                    logger.warning("Failed to get architecture components: %s", e)
                    components = []

                try:
                    diagram = self._generate_architecture_diagram(request.architecture_type, request.cloud_provider)
                except Exception as e:
                    logger.warning("Failed to generate architecture diagram: %s", e)
                    diagram = "Architecture diagram"

                template_dict = template if isinstance(template, dict) else {}
                template_structure = template_dict.get("structure", {}) if isinstance(template_dict.get("structure"), dict) else {}

                architecture_design = {
                    "template": template_dict,
                    "structure": template_structure,
                    "architecture_type": request.architecture_type or "microservices",
                    "cloud_provider": request.cloud_provider or "multi-cloud",
                    "components": components if isinstance(components, list) else [],
                    "diagram": diagram if isinstance(diagram, (str, dict)) else "Architecture diagram",
                }

                try:
                    response = ArchitectureDesignResponse(
                        action=request.action or "design",
                        project_name=request.project_name,
                        architecture=architecture_design,
                        templates=[{"template_id": request.template_id}] if request.template_id else [],
                        compliance_context=compliance_context if isinstance(compliance_context, dict) else None,
                        security_context=security_context if isinstance(security_context, dict) else None,
                        best_practices=best_practices if isinstance(best_practices, list) else [],
                        recommendations=recommendations if isinstance(recommendations, list) else [],
                        output_files=[],
                    )
                except Exception as e:
                    logger.error(
                        "Failed to create ArchitectureDesignResponse: %s | Template type: %s | Architecture design keys: %s",
                        e,
                        type(template),
                        list(architecture_design.keys()) if isinstance(architecture_design, dict) else "N/A",
                        exc_info=True,
                    )
                    raise ExternalServiceError(
                        message=f"Failed to create response: {e}",
                        user_message="Unable to generate architecture design. Please try again later.",
                        error_code="RESPONSE_CREATION_ERROR",
                        details={"error": str(e)}
                    ) from e

                if cache_key and user_id and use_cache:
                    try:
                        await architecture_cache_service.cache_design(
                            cache_key=cache_key,
                            user_id=user_id,
                            organization_id=organization_id,
                            action=request.action,
                            project_type=request.project_type,
                            architecture_type=request.architecture_type,
                            cloud_provider=request.cloud_provider,
                            compliance_standards=request.compliance_standards,
                            requirements_hash=requirements_hash,
                            design_result=response.model_dump(),
                            metadata={
                                "project_name": request.project_name,
                                "template_id": request.template_id,
                            },
                        )
                    except Exception as e:
                        logger.warning("Failed to cache design result: %s", e, exc_info=True)

                return response

            else:
                raise ValidationError(
                    message=f"Action {request.action} not yet implemented in service layer",
                    user_message=f"Action '{request.action}' is not yet supported",
                    error_code="ACTION_NOT_IMPLEMENTED",
                    details={"action": request.action}
                )

        finally:
            await mongodb_client.disconnect()

    def _get_architecture_components(self, architecture_type: str | None) -> list[dict[str, Any]]:
        """Get architecture components based on architecture type.

        Args:
            architecture_type: Architecture pattern

        Returns:
            List of component dictionaries
        """
        if architecture_type == "microservices":
            return [
                {"name": "API Gateway", "type": "gateway", "description": "Entry point for all client requests"},
                {"name": "Service A", "type": "service", "description": "Microservice A"},
                {"name": "Service B", "type": "service", "description": "Microservice B"},
                {"name": "Database", "type": "database", "description": "Persistent data storage"},
                {"name": "Service Mesh", "type": "mesh", "description": "Inter-service communication"},
            ]
        elif architecture_type == "serverless":
            return [
                {"name": "API Gateway", "type": "gateway", "description": "HTTP API endpoint"},
                {"name": "Lambda Functions", "type": "function", "description": "Serverless compute"},
                {"name": "Event Sources", "type": "event", "description": "Triggers for functions"},
                {"name": "Managed Services", "type": "service", "description": "RDS, DynamoDB, etc."},
            ]
        elif architecture_type == "monolith":
            return [
                {"name": "Application Server", "type": "server", "description": "Monolithic application"},
                {"name": "Database", "type": "database", "description": "Data storage"},
                {"name": "Load Balancer", "type": "balancer", "description": "Traffic distribution"},
            ]
        elif architecture_type == "event-driven":
            return [
                {"name": "Event Bus", "type": "bus", "description": "Central event routing"},
                {"name": "Event Producers", "type": "producer", "description": "Services that emit events"},
                {"name": "Event Consumers", "type": "consumer", "description": "Services that process events"},
                {"name": "Event Store", "type": "store", "description": "Event history storage"},
            ]
        return []

    def _generate_architecture_diagram(
        self,
        architecture_type: str | None,
        cloud_provider: str | None,
    ) -> str:
        """Generate architecture diagram text.

        Args:
            architecture_type: Architecture pattern
            cloud_provider: Cloud provider

        Returns:
            Architecture diagram as text
        """
        if architecture_type == "microservices":
            diagram = """
Microservices Architecture:
┌─────────────┐
│ API Gateway │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│ Svc │ │ Svc │
│  A  │ │  B  │
└──┬──┘ └──┬──┘
   │       │
   └───┬───┘
       │
┌──────▼──────┐
│  Database   │
└─────────────┘

Features:
- Independent service deployment
- Service mesh for communication
- Centralized logging and monitoring
- Auto-scaling per service
"""
            if cloud_provider == "multi-cloud":
                diagram += "\nMulti-Cloud Deployment:\n- AWS: Primary region\n- GCP: Secondary region\n- Azure: DR region"
            return diagram
        elif architecture_type == "serverless":
            diagram = """
Serverless Architecture:
┌─────────────┐
│ API Gateway │
└──────┬──────┘
       │
┌──────▼──────┐
│   Lambda    │
│  Functions  │
└──────┬──────┘
       │
┌──────▼──────┐
│   Managed   │
│   Services  │
└─────────────┘

Features:
- Event-driven execution
- Auto-scaling
- Pay-per-use pricing
- Managed infrastructure
"""
            return diagram
        elif architecture_type == "monolith":
            diagram = """
Monolithic Architecture:
┌─────────────┐
│Load Balancer│
└──────┬──────┘
       │
┌──────▼──────┐
│ Application │
│   Server    │
└──────┬──────┘
       │
┌──────▼──────┐
│  Database   │
└─────────────┘

Features:
- Single deployment unit
- Simplified operations
- Vertical scaling
"""
            return diagram
        elif architecture_type == "event-driven":
            diagram = """
Event-Driven Architecture:
┌──────────┐     ┌──────────┐
│Producer A│────▶│          │
└──────────┘     │  Event   │
                 │   Bus    │
┌──────────┐     │          │
│Producer B│────▶│          │
└──────────┘     └────┬─────┘
                       │
            ┌──────────┼──────────┐
            │          │          │
       ┌────▼───┐ ┌────▼───┐ ┌────▼───┐
       │Consumer│ │Consumer│ │Consumer│
       │   A    │ │   B    │ │   C    │
       └────────┘ └────────┘ └────────┘

Features:
- Loose coupling
- Asynchronous processing
- Scalable consumers
- Event sourcing support
"""
            return diagram
        return "Architecture diagram"

