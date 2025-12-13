"""Architecture service - business logic for architecture design operations."""

import hashlib
import json
import logging
import re
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
from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer
from wistx_mcp.services.template_storage_service import TemplateStorageService
from wistx_mcp.services.repository_discovery import RepositoryDiscoveryService
from wistx_mcp.services.quality_scorer import QualityScorer
from wistx_mcp.models.template_storage import TemplateFilter
from api.config import settings
from api.exceptions import ValidationError, ExternalServiceError

logger = logging.getLogger(__name__)


class ArchitectureService:
    """Service for architecture design operations."""

    # Quality threshold for stored templates
    TEMPLATE_QUALITY_THRESHOLD = 80.0

    def __init__(self):
        """Initialize architecture service."""
        self.mongodb_adapter = None
        self.api_client = WISTXAPIClient()
        self._template_storage: TemplateStorageService | None = None
        self._repository_discovery: RepositoryDiscoveryService | None = None
        self._quality_scorer: QualityScorer | None = None
        self._ai_analyzer: AIAnalyzer | None = None

    async def _get_template_storage(self) -> TemplateStorageService:
        """Get or initialize template storage service."""
        if self._template_storage is None:
            mongodb_client = MongoDBClient()
            await mongodb_client.connect()
            self._template_storage = TemplateStorageService(mongodb_client)
        return self._template_storage

    async def _get_repository_discovery(self) -> RepositoryDiscoveryService:
        """Get or initialize repository discovery service."""
        if self._repository_discovery is None:
            github_token = getattr(settings, "GITHUB_TOKEN", None)
            self._repository_discovery = RepositoryDiscoveryService(github_token=github_token)
        return self._repository_discovery

    def _get_ai_analyzer(self) -> AIAnalyzer:
        """Get or initialize AI analyzer for LLM-powered generation."""
        if self._ai_analyzer is None:
            self._ai_analyzer = AIAnalyzer()
        return self._ai_analyzer

    def _get_quality_scorer(self) -> QualityScorer:
        """Get or initialize quality scorer."""
        if self._quality_scorer is None:
            self._quality_scorer = QualityScorer()
        return self._quality_scorer

    async def _search_stored_templates(
        self,
        project_type: str | None,
        cloud_provider: str | None,
        resources: list[str] | None,
        user_id: str | None = None,
        organization_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Search for high-quality stored templates matching requirements.

        Args:
            project_type: Project type (terraform, kubernetes, etc.)
            cloud_provider: Cloud provider (aws, gcp, azure)
            resources: List of resource names
            user_id: User ID for user-specific templates
            organization_id: Organization ID for org-specific templates

        Returns:
            Best matching template or None if no good match found
        """
        try:
            template_storage = await self._get_template_storage()

            # Build tags from resources
            tags = []
            if resources:
                tags = [r.lower() for r in resources]
            if project_type:
                tags.append(project_type.lower())
            if cloud_provider and cloud_provider != "multi-cloud":
                tags.append(cloud_provider.lower())

            # Build categories
            categories = []
            if project_type:
                categories.append(project_type.lower())

            # Create filter with high quality threshold
            template_filter = TemplateFilter(
                type="repository_tree",
                min_quality_score=self.TEMPLATE_QUALITY_THRESHOLD,
                tags=tags if tags else None,
                categories=categories if categories else None,
                visibility=["global", "user", "organization"],
                user_id=user_id,
                organization_id=organization_id,
                limit=5,
            )

            templates = await template_storage.find_templates(template_filter)

            if templates:
                # Return the highest scoring template
                best_template = templates[0]
                logger.info(
                    "Found stored template: id=%s, score=%.2f",
                    best_template.get("template_id"),
                    best_template.get("quality_score", 0),
                )

                # Increment usage count
                await template_storage.increment_usage(best_template.get("template_id", ""))

                return best_template

            logger.debug("No stored templates found matching criteria")
            return None

        except Exception as e:
            logger.warning("Failed to search stored templates: %s", e)
            return None

    async def _search_github_templates(
        self,
        project_type: str | None,
        cloud_provider: str | None,
        resources: list[str] | None,
    ) -> dict[str, Any] | None:
        """Search GitHub for high-quality templates and store if found.

        Args:
            project_type: Project type (terraform, kubernetes, etc.)
            cloud_provider: Cloud provider (aws, gcp, azure)
            resources: List of resource names

        Returns:
            Best matching template or None if no good match found
        """
        try:
            discovery = await self._get_repository_discovery()

            # Build search queries
            queries = []

            if project_type == "terraform" and cloud_provider:
                provider_name = cloud_provider.lower() if cloud_provider != "multi-cloud" else "aws"
                queries.append(f"terraform {provider_name} production")
                queries.append(f"terraform {provider_name} modules")

                if resources:
                    # Add resource-specific queries
                    for resource in resources[:3]:  # Limit to avoid rate limits
                        queries.append(f"terraform {provider_name} {resource.lower()}")

            elif project_type == "kubernetes":
                queries.append("kubernetes production helm")
                queries.append("kubernetes kustomize production")

            if not queries:
                queries = [f"{project_type or 'infrastructure'} production best-practices"]

            # Discover repositories
            repos = await discovery.discover_repositories(
                queries=queries,
                min_stars=100,  # Lower threshold for broader search
                min_quality_score=70.0,
                max_results=5,
            )

            if repos:
                best_repo = repos[0]
                logger.info(
                    "Found GitHub repository: %s, score=%.2f",
                    best_repo.get("full_name"),
                    best_repo.get("quality_score", 0),
                )

                # Store high-quality repos for future use
                if best_repo.get("quality_score", 0) >= self.TEMPLATE_QUALITY_THRESHOLD:
                    await self._store_discovered_template(
                        best_repo,
                        project_type=project_type,
                        cloud_provider=cloud_provider,
                        resources=resources,
                    )

                return {
                    "source": "github",
                    "repo_url": best_repo.get("html_url"),
                    "repo_name": best_repo.get("full_name"),
                    "quality_score": best_repo.get("quality_score", 0),
                    "description": best_repo.get("description", ""),
                    "stars": best_repo.get("stargazers_count", 0),
                }

            logger.debug("No GitHub repositories found matching criteria")
            return None

        except Exception as e:
            logger.warning("Failed to search GitHub templates: %s", e)
            return None

    async def _store_discovered_template(
        self,
        repo: dict[str, Any],
        project_type: str | None,
        cloud_provider: str | None,
        resources: list[str] | None,
    ) -> str | None:
        """Store a discovered GitHub repo as a template.

        Args:
            repo: Repository data from GitHub API
            project_type: Project type
            cloud_provider: Cloud provider
            resources: List of resources

        Returns:
            Template ID or None if storage failed
        """
        try:
            template_storage = await self._get_template_storage()

            # Build tags
            tags = []
            if resources:
                tags.extend([r.lower() for r in resources])
            if project_type:
                tags.append(project_type.lower())
            if cloud_provider and cloud_provider != "multi-cloud":
                tags.append(cloud_provider.lower())
            tags.append("github-discovered")

            # Build categories
            categories = [project_type.lower()] if project_type else ["infrastructure"]

            template_id = await template_storage.store_template(
                template_type="repository_tree",
                content={
                    "repo_url": repo.get("html_url"),
                    "repo_name": repo.get("full_name"),
                    "description": repo.get("description"),
                    "default_branch": repo.get("default_branch", "main"),
                    "stars": repo.get("stargazers_count", 0),
                    "language": repo.get("language"),
                    "topics": repo.get("topics", []),
                },
                quality_score=repo.get("quality_score", 0),
                score_breakdown={
                    "stars": min(repo.get("stargazers_count", 0) / 1000 * 30, 30),
                    "activity": 20.0,  # Approximate
                    "documentation": 15.0,  # Approximate
                    "structure": 15.0,  # Approximate
                },
                metadata={
                    "source": "github_discovery",
                    "discovered_at": repo.get("updated_at"),
                    "project_type": project_type,
                    "cloud_provider": cloud_provider,
                },
                source_repo_url=repo.get("html_url"),
                tags=tags,
                categories=categories,
                visibility="global",
            )

            logger.info("Stored discovered template: %s", template_id)
            return template_id

        except Exception as e:
            logger.warning("Failed to store discovered template: %s", e)
            return None

    # === PHASE 5: LLM-Powered Intelligent Generation ===

    async def _generate_with_llm(
        self,
        project_type: str | None,
        cloud_provider: str | None,
        resources: list[str] | None,
        architecture_type: str | None,
        compliance_context: dict[str, Any] | None,
        discovered_templates: list[dict[str, Any]] | None,
    ) -> dict[str, Any] | None:
        """Generate intelligent architecture recommendations using LLM.

        Args:
            project_type: Project type (terraform, kubernetes, etc.)
            cloud_provider: Cloud provider (aws, gcp, azure)
            resources: List of resource names
            architecture_type: Architecture type (microservices, monolith, etc.)
            compliance_context: Compliance controls from existing compliance tool
            discovered_templates: Templates discovered from storage/GitHub

        Returns:
            LLM-generated insights or None if LLM unavailable
        """
        analyzer = self._get_ai_analyzer()
        if not analyzer.client:
            logger.debug("LLM not available for intelligent generation")
            return None

        try:
            # Build context from discovered templates
            template_context = ""
            if discovered_templates:
                template_context = "\n**Reference Templates:**\n"
                for t in discovered_templates[:2]:
                    source = t.get("source", "unknown")
                    score = t.get("quality_score", 0)
                    template_context += f"- {source} (quality: {score:.1f}): "
                    if source == "github":
                        template_context += f"{t.get('repo_name', 'unknown')}\n"
                    else:
                        template_context += f"{t.get('template_id', 'stored')}\n"

            # Build compliance context
            compliance_info = ""
            if compliance_context and compliance_context.get("controls"):
                controls = compliance_context["controls"][:5]
                compliance_info = f"\n**Compliance Controls ({len(compliance_context['controls'])} total):**\n"
                for c in controls:
                    compliance_info += f"- {c.get('control_id', 'N/A')}: {c.get('title', 'N/A')}\n"

            prompt = f"""You are a world-class cloud architect designing production infrastructure.

**Request:**
- Project Type: {project_type or 'infrastructure'}
- Cloud Provider: {cloud_provider or 'aws'}
- Architecture Type: {architecture_type or 'microservices'}
- Resources: {', '.join(resources) if resources else 'general infrastructure'}
{template_context}
{compliance_info}

Generate a JSON response with:
1. "architecture_insights": Brief expert analysis of this architecture (2-3 sentences)
2. "resource_relationships": Array of {{from, to, relationship_type}} describing how resources connect
3. "critical_considerations": Array of 3-5 critical items for production deployment
4. "terraform_best_practices": Array of 3-5 terraform-specific best practices for these resources
5. "estimated_complexity": "low", "medium", or "high" with brief justification

Focus on actionable, production-grade recommendations. Be specific to the requested resources."""

            response = await analyzer._call_llm(prompt)
            if not response:
                return None

            # Parse JSON from response
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())

            return {"architecture_insights": response}

        except Exception as e:
            logger.warning("LLM generation failed: %s", e)
            return None

    # === PHASE 7: Dynamic Recommendations Generation ===

    async def _generate_dynamic_recommendations(
        self,
        project_type: str | None,
        cloud_provider: str | None,
        resources: list[str] | None,
        compliance_context: dict[str, Any] | None,
        security_context: dict[str, Any] | None,
        llm_insights: dict[str, Any] | None,
        include_compliance: bool = False,
        include_security: bool = True,
    ) -> list[str]:
        """Generate dynamic, resource-specific recommendations.

        Uses existing compliance tool data and LLM insights to generate
        categorized, actionable recommendations.

        Args:
            project_type: Project type
            cloud_provider: Cloud provider
            resources: List of resources
            compliance_context: Compliance controls from get_compliance_requirements tool
            security_context: Security context from vector search
            llm_insights: LLM-generated insights from Phase 5
            include_compliance: Whether compliance was requested
            include_security: Whether security was requested

        Returns:
            List of categorized recommendations
        """
        recommendations = []

        # === Resource-Specific Recommendations ===
        if resources:
            resource_recs = self._get_resource_specific_recommendations(
                resources, cloud_provider
            )
            recommendations.extend(resource_recs)

        # === Compliance Recommendations (from existing compliance tool) ===
        if include_compliance and compliance_context:
            controls = compliance_context.get("controls", [])
            if controls:
                # Group by severity
                critical_controls = [c for c in controls if c.get("severity") == "CRITICAL"]
                high_controls = [c for c in controls if c.get("severity") == "HIGH"]

                if critical_controls:
                    recommendations.append(
                        f"🔴 CRITICAL: Address {len(critical_controls)} critical compliance controls immediately"
                    )
                    for c in critical_controls[:2]:
                        recommendations.append(f"   - {c.get('control_id')}: {c.get('title', 'N/A')}")

                if high_controls:
                    recommendations.append(
                        f"🟠 HIGH: Review {len(high_controls)} high-priority compliance controls"
                    )

                recommendations.append(
                    f"📋 Total: {len(controls)} compliance controls to implement"
                )
                recommendations.append("Set up automated compliance scanning in CI/CD pipeline")

        # === Security Recommendations ===
        if include_security:
            security_recs = self._get_security_recommendations(
                resources, cloud_provider, security_context
            )
            recommendations.extend(security_recs)

        # === LLM-Generated Recommendations ===
        if llm_insights:
            if llm_insights.get("critical_considerations"):
                recommendations.append("⚡ Critical Considerations:")
                for item in llm_insights["critical_considerations"][:3]:
                    recommendations.append(f"   - {item}")

            if llm_insights.get("terraform_best_practices"):
                recommendations.append("📘 Terraform Best Practices:")
                for item in llm_insights["terraform_best_practices"][:3]:
                    recommendations.append(f"   - {item}")

        # === Project Structure Recommendations ===
        if project_type == "terraform":
            recommendations.extend([
                "Use terraform-docs for automated documentation",
                "Implement Terratest for infrastructure testing",
                "Configure pre-commit hooks with tflint and terraform fmt",
            ])
        elif project_type == "kubernetes":
            recommendations.extend([
                "Use Helm or Kustomize for templating",
                "Implement GitOps with ArgoCD or Flux",
                "Configure pod security policies/standards",
            ])

        return recommendations

    def _get_resource_specific_recommendations(
        self,
        resources: list[str],
        cloud_provider: str | None,
    ) -> list[str]:
        """Get recommendations specific to requested resources."""
        recommendations = []
        resource_set = {r.lower() for r in resources}

        # Database recommendations
        if any(db in resource_set for db in ["rds", "aurora", "dynamodb", "database"]):
            recommendations.append("🗄️ Database: Enable automated backups with appropriate retention")
            recommendations.append("🗄️ Database: Configure Multi-AZ for production high availability")
            if "rds" in resource_set:
                recommendations.append("🗄️ RDS: Enable Performance Insights for query analysis")

        # Compute recommendations
        if any(c in resource_set for c in ["ec2", "ecs", "eks", "lambda"]):
            recommendations.append("💻 Compute: Implement auto-scaling based on actual metrics")
            if "ec2" in resource_set:
                recommendations.append("💻 EC2: Use launch templates for consistent deployments")
            if "eks" in resource_set:
                recommendations.append("💻 EKS: Configure cluster autoscaler and Karpenter")

        # Storage recommendations
        if any(s in resource_set for s in ["s3", "efs", "ebs"]):
            recommendations.append("📦 Storage: Enable versioning and lifecycle policies")
            if "s3" in resource_set:
                recommendations.append("📦 S3: Configure bucket policies and block public access")

        # Network recommendations
        if any(n in resource_set for n in ["vpc", "subnet", "security_group", "alb", "nlb"]):
            recommendations.append("🌐 Network: Implement proper subnet segmentation (public/private)")
            recommendations.append("🌐 Network: Use VPC flow logs for network monitoring")

        return recommendations

    def _get_security_recommendations(
        self,
        resources: list[str] | None,
        cloud_provider: str | None,
        security_context: dict[str, Any] | None,
    ) -> list[str]:
        """Get security recommendations based on resources and context."""
        recommendations = []
        resource_set = {r.lower() for r in (resources or [])}

        # Core security recommendations
        recommendations.append("🔒 Security: Enable encryption at rest and in transit")
        recommendations.append("🔒 Security: Implement least-privilege IAM policies")

        # Resource-specific security
        if "rds" in resource_set or "aurora" in resource_set:
            recommendations.append("🔒 Database Security: Enable IAM database authentication")
            recommendations.append("🔒 Database Security: Use Secrets Manager for credentials")

        if "s3" in resource_set:
            recommendations.append("🔒 S3 Security: Enable server-side encryption (SSE-S3 or SSE-KMS)")
            recommendations.append("🔒 S3 Security: Block public access at account level")

        if "ec2" in resource_set or "eks" in resource_set:
            recommendations.append("🔒 Compute Security: Use IMDSv2 for instance metadata")

        # Add insights from security context if available
        if security_context and security_context.get("results"):
            results = security_context["results"][:2]
            for r in results:
                if r.get("title"):
                    recommendations.append(f"🔒 {r['title']}")

        return recommendations

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

                # === PRIORITY 2: Template Discovery ===
                # Extract resources from requirements
                resources = None
                if request.requirements and isinstance(request.requirements, dict):
                    resources = request.requirements.get("resources", [])

                # Step 1: Search stored high-quality templates
                stored_template = await self._search_stored_templates(
                    project_type=request.project_type,
                    cloud_provider=request.cloud_provider,
                    resources=resources,
                    user_id=user_id,
                    organization_id=organization_id,
                )

                # Step 2: If no stored template, search GitHub
                github_template = None
                if not stored_template and resources:
                    github_template = await self._search_github_templates(
                        project_type=request.project_type,
                        cloud_provider=request.cloud_provider,
                        resources=resources,
                    )

                # Enrich template with discovered content
                discovered_templates = []
                if stored_template:
                    discovered_templates.append({
                        "source": "stored",
                        "template_id": stored_template.get("template_id"),
                        "quality_score": stored_template.get("quality_score"),
                        "content": stored_template.get("content", {}),
                    })
                    # Merge stored template structure if available
                    if stored_template.get("content", {}).get("structure"):
                        template["discovered_structure"] = stored_template["content"]["structure"]

                if github_template:
                    discovered_templates.append({
                        "source": "github",
                        "repo_url": github_template.get("repo_url"),
                        "repo_name": github_template.get("repo_name"),
                        "quality_score": github_template.get("quality_score"),
                        "stars": github_template.get("stars"),
                    })

                # Add discovered templates to template metadata
                if discovered_templates:
                    template["discovered_templates"] = discovered_templates
                    logger.info(
                        "Enriched template with %d discovered sources",
                        len(discovered_templates),
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

                # Generate dynamic recommendations based on project context
                # === PHASE 5: LLM-Powered Generation ===
                llm_insights = None
                if resources:
                    llm_insights = await self._generate_with_llm(
                        project_type=request.project_type,
                        cloud_provider=request.cloud_provider,
                        resources=resources,
                        architecture_type=request.architecture_type,
                        compliance_context=compliance_context,
                        discovered_templates=discovered_templates,
                    )
                    if llm_insights:
                        logger.info("LLM insights generated for initialize action")
                        # Add LLM insights to template for downstream use
                        template["llm_insights"] = llm_insights

                # === PHASE 7: Dynamic Recommendations ===
                init_recommendations = await self._generate_dynamic_recommendations(
                    project_type=request.project_type,
                    cloud_provider=request.cloud_provider,
                    resources=resources,
                    compliance_context=compliance_context,
                    security_context=None,  # Will be populated later if needed
                    llm_insights=llm_insights,
                    include_compliance=request.include_compliance,
                    include_security=request.include_security,
                )

                # Add project type specific getting-started recommendations
                if request.project_type == "terraform":
                    init_recommendations.insert(0, "🚀 Run 'terraform init' to initialize the working directory")
                    init_recommendations.insert(1, "🚀 Run 'terraform plan' to preview infrastructure changes")
                elif request.project_type == "kubernetes":
                    init_recommendations.insert(0, "🚀 Apply namespace configuration first: kubectl apply -f namespaces/")
                    init_recommendations.insert(1, "🚀 Configure RBAC policies before deploying workloads")

                # Build architecture dict with components and diagram
                architecture_type = request.architecture_type or "microservices"
                components = self._get_architecture_components(
                    architecture_type,
                    requirements=request.requirements,
                    cloud_provider=request.cloud_provider,
                )
                diagram = self._generate_architecture_diagram(
                    architecture_type,
                    request.cloud_provider,
                    requirements=request.requirements,
                )

                # Generate dynamic structure if requirements.resources provided
                structure = template.get("structure", {})
                if request.requirements and request.requirements.get("resources"):
                    dynamic_structure = self._generate_project_structure(
                        project_type=request.project_type,
                        requirements=request.requirements,
                        cloud_provider=request.cloud_provider,
                    )
                    if dynamic_structure:
                        structure = dynamic_structure

                response = ArchitectureDesignResponse(
                    action=request.action,
                    project_name=request.project_name,
                    architecture={
                        "template": template,
                        "structure": structure,
                        "architecture_type": architecture_type,
                        "cloud_provider": request.cloud_provider or "multi-cloud",
                        "components": components,
                        "diagram": diagram,
                    },
                    templates=[{"template_id": request.template_id}] if request.template_id else [],
                    compliance_context=compliance_context,
                    security_context={"enabled": request.include_security} if request.include_security else None,
                    best_practices=best_practices,
                    recommendations=init_recommendations,
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

                # === PRIORITY 2: Template Discovery for Design Action ===
                # Extract resources from requirements
                resources = None
                if request.requirements and isinstance(request.requirements, dict):
                    resources = request.requirements.get("resources", [])

                # Step 1: Search stored high-quality templates
                stored_template = await self._search_stored_templates(
                    project_type=project_type,
                    cloud_provider=request.cloud_provider,
                    resources=resources,
                    user_id=user_id,
                    organization_id=organization_id,
                )

                # Step 2: If no stored template, search GitHub
                github_template = None
                if not stored_template and resources:
                    github_template = await self._search_github_templates(
                        project_type=project_type,
                        cloud_provider=request.cloud_provider,
                        resources=resources,
                    )

                # Enrich template with discovered content
                discovered_templates = []
                if stored_template:
                    discovered_templates.append({
                        "source": "stored",
                        "template_id": stored_template.get("template_id"),
                        "quality_score": stored_template.get("quality_score"),
                        "content": stored_template.get("content", {}),
                    })
                    # Use discovered structure if available and no dynamic generation needed
                    if stored_template.get("content", {}).get("structure"):
                        template["discovered_structure"] = stored_template["content"]["structure"]

                if github_template:
                    discovered_templates.append({
                        "source": "github",
                        "repo_url": github_template.get("repo_url"),
                        "repo_name": github_template.get("repo_name"),
                        "quality_score": github_template.get("quality_score"),
                        "stars": github_template.get("stars"),
                    })

                # Add discovered templates to template metadata
                if discovered_templates:
                    template["discovered_templates"] = discovered_templates
                    logger.info(
                        "Design action enriched with %d discovered sources",
                        len(discovered_templates),
                    )

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

                # === PHASE 5: LLM-Powered Generation for Design Action ===
                llm_insights = None
                if resources:
                    llm_insights = await self._generate_with_llm(
                        project_type=project_type,
                        cloud_provider=request.cloud_provider,
                        resources=resources,
                        architecture_type=request.architecture_type,
                        compliance_context=compliance_context,
                        discovered_templates=discovered_templates,
                    )
                    if llm_insights:
                        logger.info("LLM insights generated for design action")
                        template["llm_insights"] = llm_insights

                # === PHASE 7: Dynamic Recommendations for Design Action ===
                recommendations = await self._generate_dynamic_recommendations(
                    project_type=project_type,
                    cloud_provider=request.cloud_provider,
                    resources=resources,
                    compliance_context=compliance_context,
                    security_context=security_context,
                    llm_insights=llm_insights,
                    include_compliance=request.include_compliance,
                    include_security=request.include_security,
                )

                # Add architecture type specific recommendations
                if request.architecture_type == "microservices":
                    recommendations.insert(0, "🏗️ Microservices: Use service mesh for inter-service communication")
                    recommendations.insert(1, "🏗️ Microservices: Implement centralized logging and monitoring")

                try:
                    components = self._get_architecture_components(
                        request.architecture_type,
                        requirements=request.requirements,
                        cloud_provider=request.cloud_provider,
                    )
                except Exception as e:
                    logger.warning("Failed to get architecture components: %s", e)
                    components = []

                try:
                    diagram = self._generate_architecture_diagram(
                        request.architecture_type,
                        request.cloud_provider,
                        requirements=request.requirements,
                    )
                except Exception as e:
                    logger.warning("Failed to generate architecture diagram: %s", e)
                    diagram = "Architecture diagram"

                template_dict = template if isinstance(template, dict) else {}
                template_structure = template_dict.get("structure", {}) if isinstance(template_dict.get("structure"), dict) else {}

                # Generate dynamic structure if requirements.resources provided
                if request.requirements and request.requirements.get("resources"):
                    dynamic_structure = self._generate_project_structure(
                        project_type=request.project_type,
                        requirements=request.requirements,
                        cloud_provider=request.cloud_provider,
                    )
                    if dynamic_structure:
                        template_structure = dynamic_structure

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

    # AWS Resource component definitions for dynamic generation
    AWS_RESOURCE_COMPONENTS: dict[str, dict[str, Any]] = {
        "ec2": {
            "name": "EC2 Module",
            "type": "compute",
            "description": "EC2 instances with Auto Scaling Groups, Launch Templates, and security groups",
            "purpose": "Application tier hosting and compute capacity",
            "terraform_resources": ["aws_instance", "aws_launch_template", "aws_autoscaling_group", "aws_security_group"],
            "dependencies": ["vpc"],
        },
        "rds": {
            "name": "RDS Module",
            "type": "database",
            "description": "RDS database instances with Multi-AZ, automated backups, and encryption",
            "purpose": "Relational database for persistent data storage",
            "terraform_resources": ["aws_db_instance", "aws_db_subnet_group", "aws_db_parameter_group", "aws_security_group"],
            "dependencies": ["vpc"],
        },
        "s3": {
            "name": "S3 Module",
            "type": "storage",
            "description": "S3 buckets with versioning, lifecycle policies, and encryption",
            "purpose": "Object storage for assets, backups, and static content",
            "terraform_resources": ["aws_s3_bucket", "aws_s3_bucket_versioning", "aws_s3_bucket_lifecycle_configuration", "aws_s3_bucket_server_side_encryption_configuration"],
            "dependencies": [],
        },
        "vpc": {
            "name": "VPC Module",
            "type": "networking",
            "description": "VPC with public/private subnets, NAT Gateways, route tables, and NACLs",
            "purpose": "Network isolation, security, and connectivity",
            "terraform_resources": ["aws_vpc", "aws_subnet", "aws_nat_gateway", "aws_internet_gateway", "aws_route_table", "aws_network_acl"],
            "dependencies": [],
        },
        "route53": {
            "name": "Route53 Module",
            "type": "dns",
            "description": "Route53 hosted zones, DNS records, health checks, and routing policies",
            "purpose": "DNS management, traffic routing, and failover",
            "terraform_resources": ["aws_route53_zone", "aws_route53_record", "aws_route53_health_check"],
            "dependencies": [],
        },
        "alb": {
            "name": "ALB Module",
            "type": "load_balancer",
            "description": "Application Load Balancer with target groups, listeners, and SSL certificates",
            "purpose": "Layer 7 load balancing and SSL termination",
            "terraform_resources": ["aws_lb", "aws_lb_target_group", "aws_lb_listener", "aws_acm_certificate"],
            "dependencies": ["vpc"],
        },
        "iam": {
            "name": "IAM Module",
            "type": "security",
            "description": "IAM roles, policies, and instance profiles with least-privilege access",
            "purpose": "Identity and access management",
            "terraform_resources": ["aws_iam_role", "aws_iam_policy", "aws_iam_instance_profile", "aws_iam_role_policy_attachment"],
            "dependencies": [],
        },
        "cloudwatch": {
            "name": "CloudWatch Module",
            "type": "monitoring",
            "description": "CloudWatch alarms, dashboards, log groups, and metrics",
            "purpose": "Monitoring, alerting, and observability",
            "terraform_resources": ["aws_cloudwatch_metric_alarm", "aws_cloudwatch_dashboard", "aws_cloudwatch_log_group"],
            "dependencies": [],
        },
        "eks": {
            "name": "EKS Module",
            "type": "container_orchestration",
            "description": "EKS cluster with managed node groups, OIDC provider, and addons",
            "purpose": "Kubernetes container orchestration",
            "terraform_resources": ["aws_eks_cluster", "aws_eks_node_group", "aws_eks_addon", "aws_iam_openid_connect_provider"],
            "dependencies": ["vpc", "iam"],
        },
        "lambda": {
            "name": "Lambda Module",
            "type": "serverless",
            "description": "Lambda functions with layers, triggers, and environment configuration",
            "purpose": "Serverless compute for event-driven workloads",
            "terraform_resources": ["aws_lambda_function", "aws_lambda_layer_version", "aws_lambda_permission", "aws_cloudwatch_log_group"],
            "dependencies": ["iam"],
        },
        "dynamodb": {
            "name": "DynamoDB Module",
            "type": "database",
            "description": "DynamoDB tables with GSIs, auto-scaling, and point-in-time recovery",
            "purpose": "NoSQL database for high-performance workloads",
            "terraform_resources": ["aws_dynamodb_table", "aws_appautoscaling_target", "aws_appautoscaling_policy"],
            "dependencies": [],
        },
        "elasticache": {
            "name": "ElastiCache Module",
            "type": "cache",
            "description": "ElastiCache Redis/Memcached clusters with replication and failover",
            "purpose": "In-memory caching for performance optimization",
            "terraform_resources": ["aws_elasticache_cluster", "aws_elasticache_replication_group", "aws_elasticache_subnet_group"],
            "dependencies": ["vpc"],
        },
        "sns": {
            "name": "SNS Module",
            "type": "messaging",
            "description": "SNS topics and subscriptions for pub/sub messaging",
            "purpose": "Event notification and fan-out messaging",
            "terraform_resources": ["aws_sns_topic", "aws_sns_topic_subscription", "aws_sns_topic_policy"],
            "dependencies": [],
        },
        "sqs": {
            "name": "SQS Module",
            "type": "messaging",
            "description": "SQS queues with dead-letter queues and visibility timeout",
            "purpose": "Message queuing for decoupled architectures",
            "terraform_resources": ["aws_sqs_queue", "aws_sqs_queue_policy"],
            "dependencies": [],
        },
        "kms": {
            "name": "KMS Module",
            "type": "security",
            "description": "KMS keys with key policies and aliases for encryption",
            "purpose": "Encryption key management",
            "terraform_resources": ["aws_kms_key", "aws_kms_alias", "aws_kms_key_policy"],
            "dependencies": [],
        },
        "secrets_manager": {
            "name": "Secrets Manager Module",
            "type": "security",
            "description": "Secrets Manager secrets with rotation configuration",
            "purpose": "Secure secrets and credentials management",
            "terraform_resources": ["aws_secretsmanager_secret", "aws_secretsmanager_secret_version", "aws_secretsmanager_secret_rotation"],
            "dependencies": ["kms"],
        },
        "waf": {
            "name": "WAF Module",
            "type": "security",
            "description": "WAF web ACLs with managed rules and custom rules",
            "purpose": "Web application firewall protection",
            "terraform_resources": ["aws_wafv2_web_acl", "aws_wafv2_rule_group", "aws_wafv2_ip_set"],
            "dependencies": ["alb"],
        },
        "cloudfront": {
            "name": "CloudFront Module",
            "type": "cdn",
            "description": "CloudFront distributions with origins, behaviors, and cache policies",
            "purpose": "Content delivery and edge caching",
            "terraform_resources": ["aws_cloudfront_distribution", "aws_cloudfront_origin_access_identity", "aws_cloudfront_cache_policy"],
            "dependencies": ["s3"],
        },
    }

    def _get_architecture_components(
        self,
        architecture_type: str | None,
        requirements: dict[str, Any] | None = None,
        cloud_provider: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get architecture components based on requirements and architecture type.

        Args:
            architecture_type: Architecture pattern
            requirements: Project requirements including resources list
            cloud_provider: Cloud provider (aws, gcp, azure)

        Returns:
            List of component dictionaries
        """
        # First, try to generate dynamic components from requirements.resources
        if requirements and isinstance(requirements, dict):
            resources = requirements.get("resources", [])
            if resources and isinstance(resources, list) and len(resources) > 0:
                return self._generate_dynamic_components(resources, cloud_provider)

        # No resources specified - return empty list
        # Better to return no data than hardcoded placeholder data that could mislead coding agents
        return []

    def _generate_dynamic_components(
        self,
        resources: list[str],
        cloud_provider: str | None = None,
    ) -> list[dict[str, Any]]:
        """Generate dynamic components based on requested resources.

        Args:
            resources: List of resource names (EC2, RDS, S3, VPC, etc.)
            cloud_provider: Cloud provider

        Returns:
            List of component dictionaries with detailed information
        """
        components: list[dict[str, Any]] = []
        added_resources: set[str] = set()

        # Normalize resource names to lowercase for matching
        normalized_resources = [r.lower().replace("-", "_").replace(" ", "_") for r in resources]

        # Add dependencies first (e.g., VPC before EC2)
        resources_with_deps: list[str] = []
        for resource in normalized_resources:
            if resource in self.AWS_RESOURCE_COMPONENTS:
                deps = self.AWS_RESOURCE_COMPONENTS[resource].get("dependencies", [])
                for dep in deps:
                    if dep not in resources_with_deps and dep not in normalized_resources:
                        resources_with_deps.append(dep)
        resources_with_deps.extend(normalized_resources)

        # Generate components in dependency order
        # VPC and IAM should come first
        priority_order = ["vpc", "iam", "kms"]
        sorted_resources = []
        for priority in priority_order:
            if priority in resources_with_deps:
                sorted_resources.append(priority)
        for resource in resources_with_deps:
            if resource not in sorted_resources:
                sorted_resources.append(resource)

        for resource in sorted_resources:
            if resource in added_resources:
                continue

            if resource in self.AWS_RESOURCE_COMPONENTS:
                component_def = self.AWS_RESOURCE_COMPONENTS[resource]
                components.append({
                    "name": component_def["name"],
                    "type": component_def["type"],
                    "description": component_def["description"],
                    "purpose": component_def.get("purpose", ""),
                    "terraform_resources": component_def.get("terraform_resources", []),
                    "dependencies": component_def.get("dependencies", []),
                })
                added_resources.add(resource)
            else:
                # Handle unknown resources with generic component
                components.append({
                    "name": f"{resource.upper()} Module",
                    "type": "custom",
                    "description": f"Custom module for {resource}",
                    "purpose": f"Manages {resource} resources",
                    "terraform_resources": [],
                    "dependencies": [],
                })
                added_resources.add(resource)

        return components

    # Resource relationship mappings for diagram generation
    RESOURCE_RELATIONSHIPS: dict[str, dict[str, Any]] = {
        "route53": {"connects_to": ["alb", "cloudfront", "ec2"], "layer": "edge"},
        "cloudfront": {"connects_to": ["s3", "alb"], "layer": "edge"},
        "waf": {"connects_to": ["alb", "cloudfront"], "layer": "edge"},
        "alb": {"connects_to": ["ec2", "eks", "lambda"], "layer": "load_balancer"},
        "ec2": {"connects_to": ["rds", "dynamodb", "elasticache", "s3", "sqs", "sns"], "layer": "compute"},
        "eks": {"connects_to": ["rds", "dynamodb", "elasticache", "s3", "sqs", "sns"], "layer": "compute"},
        "lambda": {"connects_to": ["rds", "dynamodb", "s3", "sqs", "sns", "secrets_manager"], "layer": "compute"},
        "rds": {"connects_to": [], "layer": "data"},
        "dynamodb": {"connects_to": [], "layer": "data"},
        "elasticache": {"connects_to": [], "layer": "data"},
        "s3": {"connects_to": [], "layer": "storage"},
        "sqs": {"connects_to": ["lambda"], "layer": "messaging"},
        "sns": {"connects_to": ["sqs", "lambda"], "layer": "messaging"},
        "vpc": {"contains": ["ec2", "rds", "elasticache", "eks", "alb", "lambda"], "layer": "network"},
        "iam": {"supports": ["ec2", "lambda", "eks", "rds", "s3"], "layer": "security"},
        "kms": {"supports": ["rds", "s3", "dynamodb", "secrets_manager"], "layer": "security"},
        "secrets_manager": {"supports": ["ec2", "lambda", "eks", "rds"], "layer": "security"},
        "cloudwatch": {"monitors": ["ec2", "rds", "lambda", "eks", "alb"], "layer": "monitoring"},
    }

    def _generate_architecture_diagram(
        self,
        architecture_type: str | None,
        cloud_provider: str | None,
        requirements: dict[str, Any] | None = None,
    ) -> str:
        """Generate architecture diagram based on requirements or architecture type.

        Args:
            architecture_type: Architecture pattern
            cloud_provider: Cloud provider
            requirements: Project requirements including resources list

        Returns:
            Architecture diagram as Mermaid flowchart
        """
        # First, try to generate dynamic diagram from requirements.resources
        if requirements and isinstance(requirements, dict):
            resources = requirements.get("resources", [])
            if resources and isinstance(resources, list) and len(resources) > 0:
                return self._generate_dynamic_diagram(resources, cloud_provider)

        # Fallback to architecture-type based diagrams (legacy behavior)
        return self._generate_legacy_diagram(architecture_type, cloud_provider)

    def _generate_dynamic_diagram(
        self,
        resources: list[str],
        cloud_provider: str | None = None,
    ) -> str:
        """Generate dynamic Mermaid diagram based on requested resources.

        Args:
            resources: List of resource names (EC2, RDS, S3, VPC, etc.)
            cloud_provider: Cloud provider

        Returns:
            Mermaid flowchart diagram
        """
        # Normalize resource names
        normalized = [r.lower().replace("-", "_").replace(" ", "_") for r in resources]

        # Categorize resources by layer
        layers: dict[str, list[str]] = {
            "edge": [],
            "load_balancer": [],
            "compute": [],
            "data": [],
            "storage": [],
            "messaging": [],
            "network": [],
            "security": [],
            "monitoring": [],
        }

        for resource in normalized:
            if resource in self.RESOURCE_RELATIONSHIPS:
                layer = self.RESOURCE_RELATIONSHIPS[resource].get("layer", "compute")
                if layer in layers:
                    layers[layer].append(resource)
            else:
                layers["compute"].append(resource)

        # Build Mermaid diagram
        lines = ["flowchart TB"]

        # Add subgraphs for each layer with resources
        subgraph_order = ["edge", "load_balancer", "compute", "data", "storage", "messaging"]
        layer_names = {
            "edge": "Edge Layer",
            "load_balancer": "Load Balancing",
            "compute": "Compute Layer",
            "data": "Data Layer",
            "storage": "Storage Layer",
            "messaging": "Messaging Layer",
        }

        # Check if VPC should wrap compute and data
        has_vpc = "vpc" in normalized

        if has_vpc:
            lines.append('    subgraph VPC["VPC - Network Isolation"]')

        for layer in subgraph_order:
            if layers[layer]:
                layer_resources = layers[layer]
                if layer == "network":
                    continue  # VPC handled separately

                indent = "        " if has_vpc and layer in ["compute", "data", "storage"] else "    "

                if len(layer_resources) > 1 or layer in ["compute", "data"]:
                    lines.append(f'{indent}subgraph {layer}["{layer_names.get(layer, layer.title())}"]')
                    for res in layer_resources:
                        node_id = res.upper()
                        node_label = self._get_resource_label(res)
                        lines.append(f'{indent}    {node_id}["{node_label}"]')
                    lines.append(f"{indent}end")
                else:
                    for res in layer_resources:
                        node_id = res.upper()
                        node_label = self._get_resource_label(res)
                        lines.append(f'{indent}{node_id}["{node_label}"]')

        if has_vpc:
            lines.append("    end")

        # Add connections based on relationships
        lines.append("")
        lines.append("    %% Resource Connections")

        added_connections: set[str] = set()
        for resource in normalized:
            if resource in self.RESOURCE_RELATIONSHIPS:
                connects_to = self.RESOURCE_RELATIONSHIPS[resource].get("connects_to", [])
                for target in connects_to:
                    if target in normalized:
                        conn_key = f"{resource.upper()}-->{target.upper()}"
                        if conn_key not in added_connections:
                            lines.append(f"    {resource.upper()} --> {target.upper()}")
                            added_connections.add(conn_key)

        # Add styling
        lines.append("")
        lines.append("    %% Styling")

        style_mappings = {
            "compute": "fill:#ff9900,stroke:#232f3e,color:#232f3e",
            "data": "fill:#3b48cc,stroke:#232f3e,color:#fff",
            "storage": "fill:#3f8624,stroke:#232f3e,color:#fff",
            "edge": "fill:#8c4fff,stroke:#232f3e,color:#fff",
            "load_balancer": "fill:#ff4f8b,stroke:#232f3e,color:#fff",
            "messaging": "fill:#ff9900,stroke:#232f3e,color:#232f3e",
        }

        for layer, style in style_mappings.items():
            for res in layers[layer]:
                lines.append(f"    style {res.upper()} {style}")

        # Add features section
        features = self._get_architecture_features(normalized, cloud_provider)
        if features:
            lines.append("")
            lines.append("```")
            lines.append("")
            lines.append("**Architecture Features:**")
            for feature in features:
                lines.append(f"- {feature}")

        return "\n".join(lines)

    def _get_resource_label(self, resource: str) -> str:
        """Get display label for a resource.

        Args:
            resource: Resource name (lowercase)

        Returns:
            Human-readable label
        """
        labels = {
            "ec2": "EC2\\nAuto Scaling",
            "rds": "RDS\\nPostgreSQL",
            "s3": "S3\\nBuckets",
            "vpc": "VPC",
            "route53": "Route53\\nDNS",
            "alb": "ALB\\nLoad Balancer",
            "cloudfront": "CloudFront\\nCDN",
            "lambda": "Lambda\\nFunctions",
            "eks": "EKS\\nKubernetes",
            "dynamodb": "DynamoDB\\nNoSQL",
            "elasticache": "ElastiCache\\nRedis",
            "sqs": "SQS\\nQueues",
            "sns": "SNS\\nTopics",
            "iam": "IAM\\nRoles",
            "kms": "KMS\\nEncryption",
            "secrets_manager": "Secrets\\nManager",
            "waf": "WAF\\nFirewall",
            "cloudwatch": "CloudWatch\\nMonitoring",
        }
        return labels.get(resource, resource.upper())

    def _get_architecture_features(
        self,
        resources: list[str],
        cloud_provider: str | None,
    ) -> list[str]:
        """Get architecture features based on resources.

        Args:
            resources: List of normalized resource names
            cloud_provider: Cloud provider

        Returns:
            List of feature descriptions
        """
        features = []

        if "vpc" in resources:
            features.append("Network isolation with public/private subnets")
        if "alb" in resources or "route53" in resources:
            features.append("High availability with load balancing")
        if "ec2" in resources:
            features.append("Auto-scaling compute capacity")
        if "rds" in resources:
            features.append("Managed database with Multi-AZ failover")
        if "s3" in resources:
            features.append("Durable object storage with versioning")
        if "elasticache" in resources:
            features.append("In-memory caching for performance")
        if "cloudfront" in resources:
            features.append("Global content delivery with edge caching")
        if "lambda" in resources:
            features.append("Serverless compute for event-driven workloads")
        if "eks" in resources:
            features.append("Container orchestration with Kubernetes")
        if "sqs" in resources or "sns" in resources:
            features.append("Decoupled architecture with messaging")
        if "kms" in resources or "secrets_manager" in resources:
            features.append("Encryption and secrets management")
        if "waf" in resources:
            features.append("Web application firewall protection")
        if "cloudwatch" in resources:
            features.append("Comprehensive monitoring and alerting")

        if cloud_provider == "multi-cloud":
            features.append("Multi-cloud deployment for vendor independence")

        return features

    def _generate_legacy_diagram(
        self,
        architecture_type: str | None,
        cloud_provider: str | None,
    ) -> str:
        """Generate legacy architecture diagram for backward compatibility.

        Args:
            architecture_type: Architecture pattern
            cloud_provider: Cloud provider

        Returns:
            Empty string - no hardcoded diagrams to avoid misleading coding agents
        """
        # Return empty string - better to return no data than hardcoded placeholder data
        # that could mislead coding agents into generating incorrect architecture
        return ""

    def _generate_project_structure(
        self,
        project_type: str | None,
        requirements: dict[str, Any] | None = None,
        cloud_provider: str | None = None,
    ) -> dict[str, Any]:
        """Generate dynamic project structure based on requirements.

        Args:
            project_type: Type of project (terraform, kubernetes, etc.)
            requirements: Project requirements including resources list
            cloud_provider: Cloud provider

        Returns:
            Nested dictionary representing project structure
        """
        if not requirements or not isinstance(requirements, dict):
            return {}

        resources = requirements.get("resources", [])
        if not resources or not isinstance(resources, list):
            return {}

        # Normalize resource names
        normalized = [r.lower().replace("-", "_").replace(" ", "_") for r in resources]

        if project_type == "terraform":
            return self._generate_terraform_structure(normalized, cloud_provider)
        elif project_type == "kubernetes":
            return self._generate_kubernetes_structure(normalized, cloud_provider)
        else:
            return self._generate_generic_structure(normalized, cloud_provider)

    def _generate_terraform_structure(
        self,
        resources: list[str],
        cloud_provider: str | None = None,
    ) -> dict[str, Any]:
        """Generate Terraform project structure.

        Only generates resource-specific module structure based on provided resources.
        Does not include hardcoded root-level placeholders.

        Args:
            resources: List of normalized resource names
            cloud_provider: Cloud provider

        Returns:
            Nested dictionary with only resource-specific modules
        """
        structure: dict[str, Any] = {}

        # Only generate modules for specified resources - no hardcoded root files
        modules: dict[str, Any] = {}

        for resource in resources:
            if resource in self.AWS_RESOURCE_COMPONENTS:
                component = self.AWS_RESOURCE_COMPONENTS[resource]
                module_name = resource

                # Generate module structure with resource-specific terraform resources
                terraform_resources = component.get("terraform_resources", [])
                modules[module_name] = {
                    "name": component["name"],
                    "description": component["description"],
                    "terraform_resources": terraform_resources,
                    "files": ["main.tf", "variables.tf", "outputs.tf"],
                }

                # Add data.tf for modules that need data sources
                if resource in ["ec2", "eks", "lambda", "rds"]:
                    modules[module_name]["files"].append("data.tf")

                # Add locals.tf for complex modules
                if resource in ["vpc", "eks", "ec2"]:
                    modules[module_name]["files"].append("locals.tf")

        if modules:
            structure["modules"] = modules

        # Only return resource-specific modules - no hardcoded environments/scripts/tests/CI
        # The coding agent should generate these based on project requirements
        return structure

    def _generate_kubernetes_structure(
        self,
        resources: list[str],
        cloud_provider: str | None = None,
    ) -> dict[str, Any]:
        """Generate Kubernetes project structure.

        Only generates resource-specific manifest structure based on provided resources.
        Does not include hardcoded base/overlay placeholders.

        Args:
            resources: List of normalized resource names
            cloud_provider: Cloud provider

        Returns:
            Nested dictionary with only resource-specific manifests
        """
        structure: dict[str, Any] = {}

        # Only generate manifests for specified Kubernetes resources
        manifests: dict[str, Any] = {}
        k8s_resources = ["deployment", "service", "ingress", "configmap", "secret", "statefulset", "daemonset", "job", "cronjob"]

        for resource in resources:
            resource_lower = resource.lower()
            if resource_lower in k8s_resources:
                manifests[resource_lower] = {
                    "name": f"{resource.title()} Manifest",
                    "description": f"Kubernetes {resource.title()} resource definition",
                    "api_version": self._get_k8s_api_version(resource_lower),
                    "files": [f"{resource_lower}.yaml"],
                }

        if manifests:
            structure["manifests"] = manifests

        return structure

    def _get_k8s_api_version(self, resource: str) -> str:
        """Get the Kubernetes API version for a resource type."""
        api_versions = {
            "deployment": "apps/v1",
            "service": "v1",
            "ingress": "networking.k8s.io/v1",
            "configmap": "v1",
            "secret": "v1",
            "statefulset": "apps/v1",
            "daemonset": "apps/v1",
            "job": "batch/v1",
            "cronjob": "batch/v1",
        }
        return api_versions.get(resource, "v1")

    def _generate_generic_structure(
        self,
        resources: list[str],
        cloud_provider: str | None = None,
    ) -> dict[str, Any]:
        """Generate generic project structure.

        Only generates resource-specific infrastructure based on provided resources.
        Does not include hardcoded src/docs/scripts placeholders.

        Args:
            resources: List of normalized resource names
            cloud_provider: Cloud provider

        Returns:
            Nested dictionary with only resource-specific infrastructure
        """
        structure: dict[str, Any] = {}

        # Only add infrastructure modules for specified resources
        infrastructure: dict[str, Any] = {}
        for resource in resources:
            if resource in self.AWS_RESOURCE_COMPONENTS:
                component = self.AWS_RESOURCE_COMPONENTS[resource]
                infrastructure[resource] = {
                    "name": component["name"],
                    "description": component["description"],
                    "terraform_resources": component.get("terraform_resources", []),
                }

        if infrastructure:
            structure["infrastructure"] = infrastructure

        return structure

