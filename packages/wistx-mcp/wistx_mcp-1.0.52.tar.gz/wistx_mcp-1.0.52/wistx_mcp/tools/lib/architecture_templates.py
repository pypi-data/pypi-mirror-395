"""Architecture templates for project initialization."""

import json
import logging
import re
from pathlib import Path
from typing import Any

from wistx_mcp.models.template import TemplateSource
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.template_repository import TemplateRepositoryManager

logger = logging.getLogger(__name__)


ALLOWED_PROJECT_TYPES = {
    "terraform",
    "kubernetes",
    "devops",
    "platform",
}

ALLOWED_ARCHITECTURE_TYPES = {
    "microservices",
    "serverless",
    "monolith",
    "event-driven",
    "api-gateway",
    "service-mesh",
}

ALLOWED_CLOUD_PROVIDERS = {
    "aws",
    "gcp",
    "azure",
    "multi-cloud",
}


class ArchitectureTemplates:
    """Template system for architecture and project initialization."""

    def __init__(self, mongodb_client: MongoDBClient | None = None):
        """Initialize template system.

        Args:
            mongodb_client: MongoDB client for template repository (optional)
        """
        templates_base = Path(__file__).parent.parent.parent
        self.templates_dir = templates_base / "templates"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.mongodb_client = mongodb_client
        self.repository_manager = (
            TemplateRepositoryManager(mongodb_client) if mongodb_client else None
        )

    async def get_template(
        self,
        project_type: str,
        architecture_type: str | None = None,
        cloud_provider: str | None = None,
        template_id: str | None = None,
        github_url: str | None = None,
        user_template: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Get project template.

        Args:
            project_type: Type of project (terraform, kubernetes, devops, platform)
            architecture_type: Architecture pattern (microservices, serverless, etc.)
            cloud_provider: Cloud provider (aws, gcp, azure)
            template_id: Template ID from repository (optional)
            github_url: GitHub repository URL (optional)
            user_template: User-provided template dictionary (optional)

        Returns:
            Template dictionary with structure and files
        """
        if user_template:
            return user_template

        if github_url:
            try:
                from wistx_mcp.tools.lib.github_tree_fetcher import GitHubTreeFetcher

                fetcher = GitHubTreeFetcher()
                tree = await fetcher.fetch_tree(
                    repo_url=github_url,
                    include_patterns=["**/*.tf", "**/*.yaml", "**/*.yml", "**/Dockerfile", "**/*.json"],
                    exclude_patterns=["**/node_modules/**", "**/.git/**"],
                    max_depth=10,
                    include_content=False,
                )

                structure = tree.get("structure", {})
                metadata = tree.get("metadata", {})

                template = {
                    "structure": structure,
                    "metadata": metadata,
                    "source": "github",
                    "github_url": github_url,
                }

                logger.info("Fetched template from GitHub using GitHubTreeFetcher: %s", github_url)
                return template
            except Exception as e:
                logger.warning("Failed to fetch template from GitHub %s: %s", github_url, e)
                if self.repository_manager:
                    try:
                        template = await self.repository_manager.fetch_from_github(github_url)
                        return template
                    except Exception as fallback_error:
                        logger.warning("Fallback GitHub fetch also failed: %s", fallback_error)

        if template_id and self.repository_manager:
            try:
                template = await self.repository_manager.fetch_template(template_id)
                return template.get("structure", {})
            except Exception as e:
                logger.warning("Failed to fetch template %s: %s", template_id, e)

        template_name = self._build_template_name(
            project_type=project_type,
            architecture_type=architecture_type,
            cloud_provider=cloud_provider,
        )

        if not template_name:
            return self._get_default_template(project_type, cloud_provider)

        template_path = self.templates_dir / f"{template_name}.json"

        try:
            validated_path = self._validate_template_path(template_path)
            with open(validated_path, encoding="utf-8") as f:
                template = json.load(f)
            return template
        except (ValueError, FileNotFoundError) as e:
            logger.warning("Failed to load template %s: %s", template_path, e)
            return self._get_default_template(project_type, cloud_provider)
        except Exception as e:
            logger.warning("Unexpected error loading template %s: %s", template_path, e)
            return self._get_default_template(project_type, cloud_provider)

    def _build_template_name(
        self,
        project_type: str,
        architecture_type: str | None = None,
        cloud_provider: str | None = None,
    ) -> str | None:
        """Build template name from validated components.

        Args:
            project_type: Type of project
            architecture_type: Architecture pattern (optional)
            cloud_provider: Cloud provider (optional, handles multi-cloud by using default template)

        Returns:
            Template name string or None if invalid
        """
        if cloud_provider and cloud_provider.lower() in ["multi-cloud", "multi_cloud", "multicloud"]:
            logger.info("Multi-cloud project detected, using default template selection")
            cloud_provider = None
        if not project_type or project_type not in ALLOWED_PROJECT_TYPES:
            return None

        template_name = project_type

        if architecture_type:
            if architecture_type not in ALLOWED_ARCHITECTURE_TYPES:
                logger.warning("Invalid architecture_type: %s", architecture_type)
                return None
            template_name = f"{template_name}_{architecture_type}"

        if cloud_provider:
            if cloud_provider not in ALLOWED_CLOUD_PROVIDERS:
                logger.warning("Invalid cloud_provider: %s", cloud_provider)
                return None
            template_name = f"{template_name}_{cloud_provider}"

        if not re.match(r"^[a-z0-9_-]+$", template_name):
            logger.warning("Invalid template name format: %s", template_name)
            return None

        return template_name

    def _validate_template_path(self, template_path: Path) -> Path:
        """Validate template path is safe and within templates directory.

        Args:
            template_path: Path to template file

        Returns:
            Validated absolute path

        Raises:
            ValueError: If path is invalid or outside allowed directory
            FileNotFoundError: If template file doesn't exist
        """
        if not isinstance(template_path, Path):
            template_path = Path(template_path)

        if ".." in template_path.parts:
            raise ValueError("Path traversal detected in template path")

        resolved_base = self.templates_dir.resolve()
        resolved_path = (resolved_base / template_path.name).resolve()

        try:
            resolved_path.relative_to(resolved_base)
        except ValueError:
            raise ValueError(
                f"Template path outside allowed directory: {resolved_path} not in {resolved_base}"
            ) from None

        if not resolved_path.exists():
            raise FileNotFoundError(f"Template file not found: {resolved_path}")

        if not resolved_path.is_file():
            raise ValueError(f"Template path is not a file: {resolved_path}")

        if resolved_path.suffix != ".json":
            raise ValueError(f"Template file must have .json extension: {resolved_path}")

        return resolved_path

    def _get_default_template(
        self,
        project_type: str,
        cloud_provider: str | None = None,
    ) -> dict[str, Any]:
        """Get default template for project type.

        Args:
            project_type: Type of project
            cloud_provider: Cloud provider

        Returns:
            Default template dictionary
        """
        if project_type == "terraform":
            return {
                "structure": {
                    "main.tf": "# Main infrastructure code\n\nprovider \"aws\" {\n  region = var.aws_region\n}\n",
                    "variables.tf": "# Variables\n\nvariable \"aws_region\" {\n  description = \"AWS region\"\n  type        = string\n  default     = \"us-east-1\"\n}\n",
                    "outputs.tf": "# Outputs\n",
                    "terraform.tfvars.example": "# Example variables\n# aws_region = \"us-east-1\"\n",
                    "modules": {},
                    "environments": {
                        "dev": {},
                        "staging": {},
                        "prod": {},
                    },
                    "compliance": {},
                    "security": {},
                    "monitoring": {},
                    ".github": {
                        "workflows": {
                            "terraform.yml": "# CI/CD workflow\n",
                        },
                    },
                    "README.md": "# Project documentation\n",
                    ".gitignore": "# Git ignore rules\n*.tfstate\n*.tfstate.backup\n.terraform/\n",
                },
            }

        if project_type == "kubernetes":
            return {
                "structure": {
                    "deployments": {
                        "app-deployment.yaml": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
      - name: app
        image: app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
""",
                    },
                    "services": {
                        "app-service.yaml": """apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: app
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
""",
                    },
                    "configmaps": {},
                    "secrets": {},
                    "ingress": {},
                    "rbac": {},
                    "network-policies": {},
                    "monitoring": {},
                    "compliance": {},
                    "namespace.yaml": """apiVersion: v1
kind: Namespace
metadata:
  name: default
""",
                    "kustomization.yaml": """apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - namespace.yaml
  - deployments/
  - services/
""",
                    "README.md": """# Kubernetes Project

## Overview
Production-ready Kubernetes project structure with best practices.

## Structure
- `deployments/` - Deployment manifests
- `services/` - Service definitions
- `configmaps/` - Configuration maps
- `secrets/` - Secrets (not committed)
- `ingress/` - Ingress configurations
- `rbac/` - Role-based access control
- `network-policies/` - Network policies
- `monitoring/` - Monitoring configurations
- `compliance/` - Compliance configurations

## Deployment

```bash
kubectl apply -f namespace.yaml
kubectl apply -f deployments/
kubectl apply -f services/
```
""",
                },
            }

        if project_type == "devops":
            return {
                "structure": {
                    "Dockerfile": "# Dockerfile\n",
                    "docker-compose.yml": "# Docker Compose configuration\n",
                    ".github": {
                        "workflows": {
                            "ci.yml": "# CI/CD workflow\n",
                        },
                    },
                    "README.md": "# DevOps project documentation\n",
                },
            }

        if project_type == "platform":
            return {
                "structure": {
                    "platform": {},
                    "apis": {},
                    "services": {},
                    "README.md": "# Platform engineering project\n",
                },
            }

        return {
            "structure": {
                "README.md": "# Project documentation\n",
            },
        }

