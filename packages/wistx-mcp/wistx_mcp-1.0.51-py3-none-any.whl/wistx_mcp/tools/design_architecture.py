"""Design architecture tool - project initialization and architecture design with intelligent context."""

import json
import logging
from pathlib import Path
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.architecture_templates import ArchitectureTemplates
from wistx_mcp.tools.lib.template_validator import TemplateValidator
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.context_builder import ContextBuilder
from wistx_mcp.tools.lib.github_tree_fetcher import GitHubTreeFetcher
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota
from wistx_mcp.tools import mcp_tools, web_search
from wistx_mcp.tools import visualize_infra_flow
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def design_architecture(
    action: str,
    project_type: str | None = None,
    project_name: str | None = None,
    architecture_type: str | None = None,
    cloud_provider: str | None = None,
    compliance_standards: list[str] | None = None,
    requirements: dict[str, Any] | None = None,
    existing_architecture: str | None = None,
    output_directory: str = ".",
    template_id: str | None = None,
    github_url: str | None = None,
    user_template: dict[str, Any] | None = None,
    include_compliance: bool = True,
    include_security: bool = True,
    include_best_practices: bool = True,
    api_key: str = "",
) -> dict[str, Any]:
    """Design and initialize DevOps/infrastructure/SRE/platform engineering projects with intelligent context.

    This function gathers context from multiple knowledge sources:
    - Templates (project structure)
    - Compliance requirements (standards)
    - Security knowledge (best practices)
    - Knowledge articles (patterns)
    - Code examples (implementations)

    Args:
        action: Action to perform (initialize, design, review, optimize)
        project_type: Type of project (terraform, kubernetes, devops, platform)
        project_name: Name of the project (for initialize)
        architecture_type: Architecture pattern (microservices, serverless, monolith)
        cloud_provider: Cloud provider (aws, gcp, azure, multi-cloud)
        compliance_standards: Compliance standards to include
        requirements: Project requirements
        existing_architecture: Existing architecture code/documentation
        output_directory: Directory to create project
        template_id: Template ID from MongoDB registry
        github_url: GitHub repository URL for template
        user_template: User-provided template dictionary
        include_compliance: Include compliance requirements context
        include_security: Include security knowledge context
        include_best_practices: Include best practices from knowledge base

    Returns:
        Dictionary with architecture results and intelligent context

    Raises:
        ValueError: If invalid parameters
        Exception: If operation fails
    """
    if action not in ["initialize", "design", "review", "optimize"]:
        raise ValueError(f"Invalid action: {action}")

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id
    from wistx_mcp.tools.lib.input_sanitizer import validate_infrastructure_code_input

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    if existing_architecture:
        validate_infrastructure_code_input(existing_architecture)

    logger.info(
        "Design architecture: action=%s, type=%s, name=%s",
        action,
        project_type,
        project_name,
    )

    try:
        user_info = await api_client.get_current_user(api_key=api_key)
        user_id = user_info.get("user_id")
        organization_id = user_info.get("organization_id")

        api_response = await api_client.design_architecture(
            action=action,
            project_type=project_type,
            project_name=project_name,
            architecture_type=architecture_type,
            cloud_provider=cloud_provider,
            compliance_standards=compliance_standards,
            requirements=requirements,
            existing_architecture=existing_architecture,
            output_directory=output_directory,
            template_id=template_id,
            github_url=github_url,
            user_template=user_template,
            include_compliance=include_compliance,
            include_security=include_security,
            include_best_practices=include_best_practices,
            api_key=api_key,
            user_id=user_id,
            organization_id=organization_id,
            use_cache=True,
        )

        if api_response.get("data"):
            result = api_response["data"]
            if result.get("cached"):
                logger.info("Returned cached architecture design")
            return result
        return api_response

    except Exception as e:
        logger.error("Error in design_architecture: %s", e, exc_info=True)
        raise


async def _gather_intelligent_context(
    mongodb_client: MongoDBClient,
    project_type: str | None,
    architecture_type: str | None,
    cloud_provider: str | None,
    compliance_standards: list[str] | None,
    include_compliance: bool,
    include_security: bool,
    include_best_practices: bool,
) -> dict[str, Any]:
    """Gather intelligent context from all knowledge sources in parallel.

    Args:
        mongodb_client: MongoDB client instance
        project_type: Project type
        architecture_type: Architecture type
        cloud_provider: Cloud provider
        compliance_standards: Compliance standards
        include_compliance: Include compliance context
        include_security: Include security context
        include_best_practices: Include best practices context

    Returns:
        Dictionary with gathered context
    """
    import asyncio
    from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry

    context: dict[str, Any] = {}

    async def gather_compliance() -> dict[str, Any] | None:
        """Gather compliance context."""
        if not include_compliance or not compliance_standards:
            return None
        try:
            resource_types = [project_type] if project_type else []
            if cloud_provider:
                resource_types.append(cloud_provider)

            result = await with_timeout_and_retry(
                mcp_tools.get_compliance_requirements,
                timeout_seconds=30.0,
                max_attempts=3,
                resource_types=resource_types,
                standards=compliance_standards,
                include_remediation=True,
                include_verification=True,
            )
            logger.info("Gathered compliance context: %d controls", len(result.get("controls", [])))
            return result
        except Exception as e:
            logger.warning("Failed to gather compliance context: %s", e)
            return None

    async def gather_security() -> dict[str, Any] | None:
        """Gather security context."""
        if not include_security:
            return None
        try:
            security_query = f"{project_type} security best practices"
            if cloud_provider:
                security_query += f" {cloud_provider}"
            if architecture_type:
                security_query += f" {architecture_type}"

            result = await with_timeout_and_retry(
                web_search.web_search,
                timeout_seconds=30.0,
                max_attempts=3,
                query=security_query,
                search_type="security",
                limit=10,
            )
            security_results = result.get("security", {}).get("results", []) or result.get("web", {}).get("results", [])
            logger.info("Gathered security context: %d results", len(security_results))
            return result
        except Exception as e:
            logger.warning("Failed to gather security context: %s", e)
            return None

    async def gather_best_practices() -> dict[str, Any] | None:
        """Gather best practices context."""
        if not include_best_practices:
            return None
        try:
            best_practices_query = f"{architecture_type} {project_type}"
            if cloud_provider:
                best_practices_query += f" {cloud_provider}"
            best_practices_query += " production best practices"

            result = await with_timeout_and_retry(
                mcp_tools.research_knowledge_base,
                timeout_seconds=30.0,
                max_attempts=3,
                query=best_practices_query,
                domains=["architecture", "devops"],
                include_cross_domain=True,
                include_web_search=True,
                max_results=15,
            )
            logger.info(
                "Gathered best practices context: %d articles",
                len(result.get("results", [])),
            )
            return result
        except Exception as e:
            logger.warning("Failed to gather best practices context: %s", e)
            return None

    results = await asyncio.gather(
        gather_compliance(),
        gather_security(),
        gather_best_practices(),
        return_exceptions=True,
    )

    compliance_result, security_result, best_practices_result = results

    if compliance_result and not isinstance(compliance_result, Exception):
        context["compliance"] = compliance_result

    if security_result and not isinstance(security_result, Exception):
        context["security"] = security_result

    if best_practices_result and not isinstance(best_practices_result, Exception):
        context["best_practices"] = best_practices_result

    return context


async def _enhance_template_with_context(
    template: dict[str, Any],
    context: dict[str, Any],
    project_type: str,
    compliance_standards: list[str] | None,
) -> dict[str, Any]:
    """Enhance template with intelligent context.

    Args:
        template: Original template dictionary
        context: Intelligent context dictionary
        project_type: Project type
        compliance_standards: Compliance standards

    Returns:
        Enhanced template dictionary
    """
    enhanced_template = template.copy()
    structure = enhanced_template.get("structure", {}).copy()

    compliance_controls = context.get("compliance", {}).get("controls", [])
    if compliance_controls and project_type == "kubernetes":
        if "rbac" not in structure:
            structure["rbac"] = {}

        rbac_content = _generate_rbac_from_compliance(compliance_controls)
        if rbac_content:
            structure["rbac"]["service-account.yaml"] = rbac_content

        if "network-policies" not in structure:
            structure["network-policies"] = {}

        network_policy_content = _generate_network_policy_from_compliance(compliance_controls)
        if network_policy_content:
            structure["network-policies"]["network-policy.yaml"] = network_policy_content

    if compliance_standards and "compliance" not in structure:
        structure["compliance"] = {}

    for standard in compliance_standards or []:
        compliance_file = f"{standard.lower().replace('-', '_')}.yaml"
        compliance_content = _generate_compliance_config(standard, compliance_controls)
        structure["compliance"][compliance_file] = compliance_content

    enhanced_template["structure"] = structure
    enhanced_template["context_applied"] = {
        "compliance": bool(context.get("compliance")),
        "security": bool(context.get("security")),
        "best_practices": bool(context.get("best_practices")),
    }

    return enhanced_template


def _generate_rbac_from_compliance(controls: list[dict[str, Any]]) -> str:
    """Generate RBAC configuration dynamically from compliance controls.

    Args:
        controls: List of compliance controls

    Returns:
        RBAC YAML content
    """
    rbac_parts = []

    rbac_controls = [
        c
        for c in controls
        if c.get("category", "").lower() in ["access_control", "access", "rbac", "iam"]
        or "rbac" in c.get("title", "").lower()
        or "role" in c.get("title", "").lower()
        or "permission" in c.get("title", "").lower()
        or "least privilege" in c.get("description", "").lower()
    ]

    if not rbac_controls:
        return ""

    rbac_parts.append("""apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-service-account
  namespace: default
  annotations:
    # Compliance: Least privilege access
""")

    for i, control in enumerate(rbac_controls[:5]):
        control_id = control.get("control_id", f"control-{i}").replace(".", "-").replace("_", "-")
        title = control.get("title", "")
        standard = control.get("standard", "")

        remediation = control.get("remediation", {})
        guidance = ""
        if isinstance(remediation, dict):
            guidance = remediation.get("guidance", "") or remediation.get("summary", "")

        rbac_parts.append(f"""---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: role-{control_id}
  namespace: default
  annotations:
    compliance.standard: "{standard}"
    compliance.control: "{control_id}"
rules:
- apiGroups: [""]
  resources: ["pods", "configmaps"]
  verbs: ["get", "list"]
  # Compliance: {title}
""")

        if guidance:
            rbac_parts[-1] += f"  # Guidance: {guidance[:100]}\n"

    rbac_parts.append("""---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-rolebinding
  namespace: default
subjects:
- kind: ServiceAccount
  name: app-service-account
  namespace: default
roleRef:
  kind: Role
  name: role-default
  apiGroup: rbac.authorization.k8s.io
""")

    return "\n".join(rbac_parts)


def _generate_network_policy_from_compliance(controls: list[dict[str, Any]]) -> str:
    """Generate network policy dynamically from compliance controls.

    Args:
        controls: List of compliance controls

    Returns:
        Network policy YAML content
    """
    network_controls = [
        c
        for c in controls
        if c.get("category", "").lower() in ["network_security", "network", "firewall"]
        or "network" in c.get("title", "").lower()
        or "firewall" in c.get("title", "").lower()
        or "isolation" in c.get("description", "").lower()
    ]

    if not network_controls:
        return ""

    ingress_rules = []
    egress_rules = []

    for control in network_controls[:3]:
        control_id = control.get("control_id", "")
        title = control.get("title", "")
        standard = control.get("standard", "")

        remediation = control.get("remediation", {})
        code_snippet = ""
        if isinstance(remediation, dict):
            code_snippets = remediation.get("code_snippets", [])
            if code_snippets:
                code_snippet = code_snippets[0]

        if "ingress" in title.lower() or "inbound" in title.lower():
            ingress_rules.append(f"""  # {standard} {control_id}: {title}
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
""")
        elif "egress" in title.lower() or "outbound" in title.lower():
            egress_rules.append(f"""  # {standard} {control_id}: {title}
  - to:
    - namespaceSelector: {{}}
    ports:
    - protocol: TCP
      port: 53
""")

    if not ingress_rules:
        ingress_rules = [
            """  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
"""
        ]

    if not egress_rules:
        egress_rules = [
            """  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 53
"""
        ]

    network_policy = f"""apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
  namespace: default
  annotations:
    compliance.applied: "true"
spec:
  podSelector:
    matchLabels:
      app: app
  policyTypes:
  - Ingress
  - Egress
  ingress:
{''.join(ingress_rules)}
  egress:
{''.join(egress_rules)}
"""

    return network_policy


def _generate_compliance_config(standard: str, controls: list[dict[str, Any]]) -> str:
    """Generate compliance configuration file.

    Args:
        standard: Compliance standard name
        controls: List of compliance controls

    Returns:
        Compliance configuration content
    """
    config = f"# {standard} Compliance Configuration\n\n"
    config += "## Applied Controls\n\n"

    for control in controls[:10]:
        control_id = control.get("control_id", "")
        title = control.get("title", "")
        config += f"### {control_id}: {title}\n\n"
        remediation = control.get("remediation", {})
        if remediation.get("guidance"):
            config += f"{remediation['guidance']}\n\n"

    return config


async def _create_intelligent_project_structure(
    project_path: Path,
    template: dict[str, Any],
    context: dict[str, Any],
    compliance_standards: list[str] | None,
    cloud_provider: str | None,
    files_created: list[str],
    structure: list[str],
) -> None:
    """Create intelligent project structure with context-enhanced templates.

    Args:
        project_path: Path to project directory
        template: Enhanced template dictionary
        context: Intelligent context dictionary
        compliance_standards: Compliance standards
        cloud_provider: Cloud provider
        files_created: List to append created files
        structure: List to append structure items
    """
    structure_dict = template.get("structure", {})

    for item_path, content in structure_dict.items():
        full_path = project_path / item_path

        if isinstance(content, dict):
            full_path.mkdir(parents=True, exist_ok=True)
            structure.append(f"{item_path}/")
            await _create_intelligent_project_structure(
                project_path=full_path,
                template={"structure": content},
                context=context,
                compliance_standards=compliance_standards,
                cloud_provider=cloud_provider,
                files_created=files_created,
                structure=structure,
            )
        else:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(str(content), encoding="utf-8")
            files_created.append(str(full_path.relative_to(project_path)))
            structure.append(item_path)

    if compliance_standards and "compliance" not in structure_dict:
        compliance_dir = project_path / "compliance"
        compliance_dir.mkdir(exist_ok=True)

        for standard in compliance_standards:
            compliance_file = compliance_dir / f"{standard.lower().replace('-', '_')}.yaml"
            compliance_content = _generate_compliance_config(
                standard,
                context.get("compliance", {}).get("controls", []),
            )
            compliance_file.write_text(compliance_content, encoding="utf-8")
            files_created.append(str(compliance_file.relative_to(project_path)))


def _format_context_summary(context: dict[str, Any]) -> dict[str, Any]:
    """Format context summary for response.

    Args:
        context: Intelligent context dictionary

    Returns:
        Formatted context summary
    """
    security_data = context.get("security", {})
    security_results = security_data.get("security", {}).get("results", []) or security_data.get("web", {}).get("results", [])

    summary = {
        "compliance": {
            "enabled": bool(context.get("compliance")),
            "controls_count": len(context.get("compliance", {}).get("controls", [])),
        },
        "security": {
            "enabled": bool(context.get("security")),
            "results_count": len(security_results),
        },
        "best_practices": {
            "enabled": bool(context.get("best_practices")),
            "articles_count": len(context.get("best_practices", {}).get("results", [])),
        },
    }
    return summary


def _get_intelligent_recommendations(
    architecture_type: str | None,
    requirements: dict[str, Any] | None,
    context: dict[str, Any],
) -> list[str]:
    """Get intelligent recommendations based on context.

    Args:
        architecture_type: Architecture type
        requirements: Project requirements
        context: Intelligent context dictionary

    Returns:
        List of recommendations
    """
    recommendations = []

    if architecture_type == "microservices":
        recommendations.extend([
            "Use service mesh for inter-service communication",
            "Implement centralized logging",
            "Set up distributed tracing",
        ])

    if requirements and requirements.get("scalability") == "high":
        recommendations.append("Consider auto-scaling configuration")

    compliance_controls = context.get("compliance", {}).get("controls", [])
    if compliance_controls:
        recommendations.append(f"Applied {len(compliance_controls)} compliance controls")

    security_data = context.get("security", {})
    security_results = security_data.get("security", {}).get("results", []) or security_data.get("web", {}).get("results", [])
    if security_results:
        recommendations.append("Security best practices applied from latest knowledge")

    best_practices = context.get("best_practices", {}).get("results", [])
    if best_practices:
        recommendations.append(f"Applied {len(best_practices)} best practice patterns")

    return recommendations


def _validate_and_create_output_directory(
    output_directory: str,
    project_name: str,
) -> Path:
    """Validate and sanitize output directory path.

    Prevents path traversal attacks and ensures safe directory creation.

    Args:
        output_directory: Output directory path
        project_name: Project name (will be appended to output_directory)

    Returns:
        Validated Path object

    Raises:
        ValueError: If path is invalid or unsafe
    """
    if not output_directory:
        raise ValueError("output_directory cannot be empty")

    if not project_name:
        raise ValueError("project_name cannot be empty")

    if ".." in output_directory or ".." in project_name:
        raise ValueError("Path traversal not allowed in output_directory or project_name")

    if output_directory.startswith("/") and not output_directory.startswith("/tmp"):
        raise ValueError("Only /tmp directory allowed for absolute paths")

    if any(char in project_name for char in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]):
        raise ValueError(f"Invalid characters in project_name: {project_name}")

    base_path = Path(output_directory).resolve()

    if not base_path.exists():
        try:
            base_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create output directory: {e}") from e

    if not base_path.is_dir():
        raise ValueError(f"output_directory must be a directory: {output_directory}")

    project_path = base_path / project_name

    if project_path.exists() and not project_path.is_dir():
        raise ValueError(f"Project path exists but is not a directory: {project_path}")

    try:
        project_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise ValueError(f"Cannot create project directory: {e}") from e

    return project_path


def _get_next_steps(
    project_type: str,
    compliance_standards: list[str] | None,
) -> list[str]:
    """Get recommended next steps.

    Args:
        project_type: Type of project
        compliance_standards: Compliance standards

    Returns:
        List of next steps
    """
    steps = []

    if project_type == "terraform":
        steps.extend([
            f"Review generated {project_type} project structure",
            "Configure variables in terraform.tfvars",
            "Initialize Terraform: terraform init",
            "Plan changes: terraform plan",
            "Apply infrastructure: terraform apply",
        ])
    elif project_type == "kubernetes":
        steps.extend([
            "Review Kubernetes manifests",
            "Apply namespace: kubectl apply -f namespace.yaml",
            "Deploy resources: kubectl apply -f deployments/",
        ])

    if compliance_standards:
        steps.append(
            f"Review compliance configurations for {', '.join(compliance_standards)}"
        )

    return steps


def _generate_architecture_diagram(
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
        return """
Microservices Architecture:
- API Gateway → Multiple Services
- Each service: Independent deployment
- Service mesh for communication
- Centralized logging and monitoring
"""
    elif architecture_type == "serverless":
        return """
Serverless Architecture:
- API Gateway → Lambda Functions
- Event-driven architecture
- Managed services (RDS, DynamoDB)
- Auto-scaling
"""
    return "Architecture diagram"


def _get_architecture_components(
    architecture_type: str | None,
) -> list[dict[str, Any]]:
    """Get architecture components.

    Args:
        architecture_type: Architecture pattern

    Returns:
        List of component dictionaries
    """
    if architecture_type == "microservices":
        return [
            {"name": "API Gateway", "type": "gateway"},
            {"name": "Service A", "type": "service"},
            {"name": "Service B", "type": "service"},
            {"name": "Database", "type": "database"},
        ]
    return []


def _get_architecture_recommendations(
    architecture_type: str | None,
    requirements: dict[str, Any] | None,
) -> list[str]:
    """Get architecture recommendations.

    Args:
        architecture_type: Architecture pattern
        requirements: Project requirements

    Returns:
        List of recommendations
    """
    recommendations = []

    if architecture_type == "microservices":
        recommendations.extend([
            "Use service mesh for inter-service communication",
            "Implement centralized logging",
            "Set up distributed tracing",
        ])

    if requirements and requirements.get("scalability") == "high":
        recommendations.append("Consider auto-scaling configuration")

    return recommendations


async def _review_architecture(
    existing_architecture: str | None,
    compliance_standards: list[str] | None,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Review existing architecture with AI analysis.

    Args:
        existing_architecture: Existing architecture code/documentation
        compliance_standards: Compliance standards to check
        api_key: Optional API key for codebase-wide regex search

    Returns:
        Review results dictionary
    """
    if not existing_architecture:
        return {
            "issues": [],
            "recommendations": [],
            "compliance_status": "unknown",
            "security_status": "unknown",
        }

    regex_security_issues = []
    regex_compliance_violations = []

    if api_key:
        try:
            from wistx_mcp.tools import regex_search

            security_templates = ["api_key", "password", "secret_key", "token", "credential"]
            for template in security_templates:
                try:
                    regex_results = await regex_search.regex_search_codebase(
                        template=template,
                        api_key=api_key,
                        include_context=True,
                        limit=5,
                    )
                    matches = regex_results.get("matches", [])
                    if matches:
                        regex_security_issues.append({
                            "type": template,
                            "count": len(matches),
                            "matches": matches[:3],
                        })
                except Exception as e:
                    logger.warning("Regex search failed for template %s: %s", template, e)

            if compliance_standards:
                compliance_template_map = {
                    "PCI-DSS": ["unencrypted_storage", "public_access", "no_encryption"],
                    "HIPAA": ["missing_backup", "no_encryption", "no_logging"],
                    "SOC2": ["no_mfa", "no_logging", "public_access"],
                    "NIST": ["no_encryption", "public_access", "no_logging"],
                }

                for standard in compliance_standards:
                    templates = compliance_template_map.get(standard, [])
                    for template in templates:
                        try:
                            regex_results = await regex_search.regex_search_codebase(
                                template=template,
                                api_key=api_key,
                                include_context=True,
                                limit=5,
                            )
                            matches = regex_results.get("matches", [])
                            if matches:
                                regex_compliance_violations.append({
                                    "standard": standard,
                                    "type": template,
                                    "count": len(matches),
                                    "matches": matches[:3],
                                })
                        except Exception as e:
                            logger.warning("Regex search failed for template %s: %s", template, e)

        except ImportError:
            logger.warning("regex_search module not available, skipping regex security checks")
        except Exception as e:
            logger.warning("Regex search integration failed: %s", e, exc_info=True)

    try:
        from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer

        analyzer = AIAnalyzer()

        if analyzer.client:
            prompt = f"""
            Review this infrastructure architecture for issues and improvements:

            **Architecture Code/Documentation**:
            {existing_architecture[:3000]}

            **Compliance Standards**: {', '.join(compliance_standards or [])}

            Analyze and return JSON with:
            1. issues: Array of identified issues (security, compliance, best practices)
            2. recommendations: Array of specific recommendations
            3. compliance_status: "compliant", "partial", or "non_compliant"
            4. security_status: "secure", "needs_review", or "vulnerable"
            5. performance_issues: Array of performance concerns
            6. cost_opportunities: Array of cost optimization opportunities

            Be thorough and specific. Focus on actionable items.
            """

            ai_response = await analyzer._call_llm(prompt)

            if ai_response:
                import json
                import re

                json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)
                if json_match:
                    try:
                        ai_review = json.loads(json_match.group())
                        result = {
                            "issues": ai_review.get("issues", []),
                            "recommendations": ai_review.get("recommendations", []),
                            "compliance_status": ai_review.get("compliance_status", "unknown"),
                            "security_status": ai_review.get("security_status", "unknown"),
                            "performance_issues": ai_review.get("performance_issues", []),
                            "cost_opportunities": ai_review.get("cost_opportunities", []),
                        }

                        if regex_security_issues:
                            result["regex_security_issues"] = regex_security_issues
                            result["issues"].append(
                                f"Found {sum(issue['count'] for issue in regex_security_issues)} security issues via regex search"
                            )

                        if regex_compliance_violations:
                            result["regex_compliance_violations"] = regex_compliance_violations
                            result["issues"].append(
                                f"Found {sum(v['count'] for v in regex_compliance_violations)} compliance violations via regex search"
                            )

                        return result
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse AI review JSON, using fallback")
                        return await _review_architecture_fallback(
                            existing_architecture, compliance_standards, regex_security_issues, regex_compliance_violations
                        )
                else:
                    return await _review_architecture_fallback(
                        existing_architecture, compliance_standards, regex_security_issues, regex_compliance_violations
                    )
            else:
                return await _review_architecture_fallback(
                    existing_architecture, compliance_standards, regex_security_issues, regex_compliance_violations
                )
        else:
            return await _review_architecture_fallback(
                existing_architecture, compliance_standards, regex_security_issues, regex_compliance_violations
            )
    except Exception as e:
        logger.warning("AI architecture review failed, using fallback: %s", e)
        return await _review_architecture_fallback(
            existing_architecture, compliance_standards, regex_security_issues, regex_compliance_violations
        )


async def _review_architecture_fallback(
    existing_architecture: str,
    compliance_standards: list[str] | None,
    regex_security_issues: list[dict[str, Any]] | None = None,
    regex_compliance_violations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Fallback architecture review using basic analysis.

    Args:
        existing_architecture: Existing architecture code/documentation
        compliance_standards: Compliance standards to check
        regex_security_issues: Security issues found via regex search
        regex_compliance_violations: Compliance violations found via regex search

    Returns:
        Review results dictionary
    """
    issues = []
    recommendations = []

    if "encryption" not in existing_architecture.lower():
        issues.append("Missing encryption configuration")
        recommendations.append("Add encryption for data at rest and in transit")

    if compliance_standards:
        compliance_status = "partial"
        for standard in compliance_standards:
            if standard.lower() not in existing_architecture.lower():
                issues.append(f"Missing {standard} compliance configurations")
    else:
        compliance_status = "unknown"

    return {
        "issues": issues,
        "recommendations": recommendations,
        "compliance_status": compliance_status,
        "security_status": "review_needed",
        "performance_issues": [],
        "cost_opportunities": [],
    }


async def _optimize_architecture(
    existing_architecture: str | None,
    requirements: dict[str, Any] | None,
) -> dict[str, Any]:
    """Optimize architecture with AI analysis.

    Args:
        existing_architecture: Existing architecture code/documentation
        requirements: Optimization requirements

    Returns:
        Optimization results dictionary
    """
    if not existing_architecture:
        return {
            "optimizations": [],
            "cost_savings": [],
            "performance_improvements": [],
            "scalability_improvements": [],
        }

    try:
        from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer

        analyzer = AIAnalyzer()

        if analyzer.client:
            requirements_str = json.dumps(requirements, indent=2) if requirements else "None specified"

            prompt = f"""
            Analyze and optimize this infrastructure architecture:

            **Architecture Code/Documentation**:
            {existing_architecture[:3000]}

            **Optimization Requirements**:
            {requirements_str}

            Provide optimization recommendations in JSON format with:
            1. optimizations: Array of optimization recommendations
            2. cost_savings: Array of specific cost savings opportunities with estimated savings
            3. performance_improvements: Array of performance optimization suggestions
            4. scalability_improvements: Array of scalability enhancements
            5. resource_rightsizing: Array of resource sizing recommendations

            Be specific with:
            - Exact resource types and sizes to change
            - Estimated cost savings (percentage or dollar amount)
            - Performance impact estimates
            - Implementation complexity (low/medium/high)

            Focus on practical, actionable optimizations.
            """

            ai_response = await analyzer._call_llm(prompt)

            if ai_response:
                import json
                import re

                json_match = re.search(r"\{.*\}", ai_response, re.DOTALL)
                if json_match:
                    try:
                        ai_optimization = json.loads(json_match.group())
                        return {
                            "optimizations": ai_optimization.get("optimizations", []),
                            "cost_savings": ai_optimization.get("cost_savings", []),
                            "performance_improvements": ai_optimization.get("performance_improvements", []),
                            "scalability_improvements": ai_optimization.get("scalability_improvements", []),
                            "resource_rightsizing": ai_optimization.get("resource_rightsizing", []),
                        }
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse AI optimization JSON, using fallback")
                        return _optimize_architecture_fallback(existing_architecture, requirements)
                else:
                    return _optimize_architecture_fallback(existing_architecture, requirements)
            else:
                return _optimize_architecture_fallback(existing_architecture, requirements)
        else:
            return _optimize_architecture_fallback(existing_architecture, requirements)
    except Exception as e:
        logger.warning("AI architecture optimization failed, using fallback: %s", e)
        return _optimize_architecture_fallback(existing_architecture, requirements)


def _optimize_architecture_fallback(
    existing_architecture: str,
    requirements: dict[str, Any] | None,
) -> dict[str, Any]:
    """Fallback architecture optimization using basic analysis.

    Args:
        existing_architecture: Existing architecture code/documentation
        requirements: Optimization requirements

    Returns:
        Optimization results dictionary
    """
    optimizations = []
    cost_savings = []
    performance_improvements = []

    if existing_architecture:
        if "m5.2xlarge" in existing_architecture:
            optimizations.append("Consider using t3.medium for non-production workloads")
            cost_savings.append("Potential 60% cost reduction")

        if "single-az" not in existing_architecture.lower():
            optimizations.append("Consider single-AZ for non-critical workloads")
            cost_savings.append("Potential 50% cost reduction")

    return {
        "optimizations": optimizations,
        "cost_savings": cost_savings,
        "performance_improvements": performance_improvements,
        "scalability_improvements": [],
        "resource_rightsizing": [],
    }

