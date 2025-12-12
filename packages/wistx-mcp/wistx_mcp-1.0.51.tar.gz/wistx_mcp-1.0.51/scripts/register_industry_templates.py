"""Register industry-standard templates in MongoDB template registry."""

import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.template_repository import TemplateRepositoryManager
from wistx_mcp.models.template import TemplateSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CURATED_TEMPLATES = [
    {
        "name": "Kubernetes Microservices - AWS",
        "description": "Production-ready Kubernetes microservices template for AWS with security, monitoring, and compliance best practices",
        "github_url": "https://github.com/wistx-templates/kubernetes-microservices-aws",
        "project_type": "kubernetes",
        "architecture_type": "microservices",
        "cloud_provider": "aws",
        "tags": ["kubernetes", "microservices", "aws", "production", "best-practices", "security", "monitoring"],
        "compliance_standards": ["PCI-DSS", "SOC2"],
        "version": "1.0.0",
    },
    {
        "name": "Kubernetes Serverless - AWS",
        "description": "Production-ready Kubernetes serverless template for AWS with auto-scaling and event-driven architecture",
        "github_url": "https://github.com/wistx-templates/kubernetes-serverless-aws",
        "project_type": "kubernetes",
        "architecture_type": "serverless",
        "cloud_provider": "aws",
        "tags": ["kubernetes", "serverless", "aws", "production", "auto-scaling"],
        "compliance_standards": ["SOC2"],
        "version": "1.0.0",
    },
    {
        "name": "Terraform Multi-Tier - AWS",
        "description": "Production-ready Terraform template for multi-tier AWS infrastructure with VPC, RDS, EKS, and security groups",
        "github_url": "https://github.com/wistx-templates/terraform-multi-tier-aws",
        "project_type": "terraform",
        "architecture_type": "multi-tier",
        "cloud_provider": "aws",
        "tags": ["terraform", "aws", "multi-tier", "production", "vpc", "eks"],
        "compliance_standards": ["PCI-DSS", "HIPAA"],
        "version": "1.0.0",
    },
    {
        "name": "DevOps CI/CD - GitHub Actions",
        "description": "Complete DevOps CI/CD pipeline template with GitHub Actions, testing, security scanning, and deployment",
        "github_url": "https://github.com/wistx-templates/devops-cicd-github-actions",
        "project_type": "devops",
        "architecture_type": "ci-cd",
        "cloud_provider": None,
        "tags": ["devops", "ci-cd", "github-actions", "testing", "security"],
        "compliance_standards": [],
        "version": "1.0.0",
    },
]


async def register_templates():
    """Register all curated industry-standard templates."""
    mongodb_client = MongoDBClient()
    await mongodb_client.connect()

    template_manager = TemplateRepositoryManager(mongodb_client)

    registered_count = 0
    failed_count = 0

    for template_config in CURATED_TEMPLATES:
        try:
            logger.info("Registering template: %s", template_config["name"])

            try:
                template_structure = await template_manager.fetch_from_github(
                    template_config["github_url"],
                    path="template.json",
                )
            except Exception as e:
                logger.warning(
                    "Failed to fetch template from GitHub %s: %s. Using default structure.",
                    template_config["github_url"],
                    e,
                )
                template_structure = {
                    "structure": _get_default_structure_for_type(
                        template_config["project_type"],
                        template_config.get("architecture_type"),
                        template_config.get("cloud_provider"),
                    ),
                }

            template = await template_manager.register_template(
                name=template_config["name"],
                structure=template_structure.get("structure", {}),
                project_type=template_config["project_type"],
                architecture_type=template_config.get("architecture_type"),
                cloud_provider=template_config.get("cloud_provider"),
                source_type=TemplateSource.GITHUB,
                source_url=template_config["github_url"],
                version=template_config["version"],
                tags=template_config.get("tags", []),
                visibility="public",
                changelog=[
                    f"Initial release: {template_config['description']}",
                    "Includes production-ready configurations",
                    "Follows industry best practices",
                ],
            )

            logger.info("✅ Registered template: %s (ID: %s)", template.name, template.template_id)
            registered_count += 1

        except Exception as e:
            logger.error("❌ Failed to register %s: %s", template_config["name"], e, exc_info=True)
            failed_count += 1

    logger.info(
        "Template registration complete: %d registered, %d failed",
        registered_count,
        failed_count,
    )

    await mongodb_client.close()


def _get_default_structure_for_type(
    project_type: str,
    architecture_type: str | None = None,
    cloud_provider: str | None = None,
) -> dict[str, str]:
    """Get default structure for project type (fallback if GitHub fetch fails).

    Args:
        project_type: Project type
        architecture_type: Architecture type
        cloud_provider: Cloud provider

    Returns:
        Default structure dictionary
    """
    if project_type == "kubernetes":
        if architecture_type == "microservices":
            return {
                "deployments/": {},
                "services/": {},
                "configmaps/": {},
                "secrets/": {},
                "ingress/": {},
                "rbac/": {},
                "network-policies/": {},
                "monitoring/": {},
                "compliance/": {},
                "namespace.yaml": "# Namespace definition\n",
                "kustomization.yaml": "# Kustomize configuration\n",
                "README.md": "# Kubernetes Microservices Project\n",
            }
        return {
            "deployments/": {},
            "services/": {},
            "configmaps/": {},
            "secrets/": {},
            "ingress/": {},
            "namespace.yaml": "# Namespace definition\n",
            "kustomization.yaml": "# Kustomize configuration\n",
            "README.md": "# Kubernetes Project\n",
        }

    if project_type == "terraform":
        return {
            "main.tf": "# Main infrastructure code\n",
            "variables.tf": "# Variables\n",
            "outputs.tf": "# Outputs\n",
            "terraform.tfvars.example": "# Example variables\n",
            "modules/": {},
            "environments/": {
                "dev/": {},
                "staging/": {},
                "prod/": {},
            },
            "compliance/": {},
            "security/": {},
            "monitoring/": {},
            ".github/workflows/": {},
            "README.md": "# Terraform Project\n",
            ".gitignore": "# Git ignore rules\n",
        }

    if project_type == "devops":
        return {
            "Dockerfile": "# Dockerfile\n",
            "docker-compose.yml": "# Docker Compose configuration\n",
            ".github/workflows/": {},
            "scripts/": {},
            "tests/": {},
            "README.md": "# DevOps Project\n",
        }

    return {
        "README.md": "# Project\n",
    }


if __name__ == "__main__":
    asyncio.run(register_templates())

