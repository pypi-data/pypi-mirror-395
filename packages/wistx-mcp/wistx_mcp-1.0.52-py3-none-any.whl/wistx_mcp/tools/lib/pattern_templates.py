"""Pre-built regex pattern templates for common use cases."""

from typing import Any


class PatternTemplates:
    """Pre-built regex pattern templates."""

    TEMPLATES: dict[str, dict[str, Any]] = {
        "api_key": {
            "pattern": r"api[_-]?key\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find API key assignments",
            "category": "security",
        },
        "password": {
            "pattern": r"password\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find password assignments",
            "category": "security",
        },
        "secret_key": {
            "pattern": r"secret[_-]?key\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find secret key assignments",
            "category": "security",
        },
        "aws_access_key": {
            "pattern": r"AKIA[0-9A-Z]{16}",
            "description": "Find AWS access key IDs",
            "category": "security",
        },
        "aws_secret_key": {
            "pattern": r"aws[_-]?secret[_-]?access[_-]?key\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find AWS secret access keys",
            "category": "security",
        },
        "ip_address": {
            "pattern": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
            "description": "Find IP addresses",
            "category": "security",
        },
        "email": {
            "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "description": "Find email addresses",
            "category": "security",
        },
        "unencrypted_storage": {
            "pattern": r"storage_encrypted\s*=\s*(?:false|0|null)",
            "description": "Find unencrypted storage configurations",
            "category": "compliance",
        },
        "public_access": {
            "pattern": r"public[_-]?access\s*=\s*(?:true|1)",
            "description": "Find publicly accessible resources",
            "category": "compliance",
        },
        "missing_backup": {
            "pattern": r"backup_retention_period\s*=\s*(?:0|null)",
            "description": "Find resources without backup retention",
            "category": "compliance",
        },
        "function_definition": {
            "pattern": r"def\s+(\w+)\s*\(",
            "description": "Find function definitions",
            "category": "code_analysis",
        },
        "class_definition": {
            "pattern": r"class\s+(\w+)",
            "description": "Find class definitions",
            "category": "code_analysis",
        },
        "terraform_resource": {
            "pattern": r"resource\s+[\"'](\w+)[\"']\s+[\"'](\w+)[\"']",
            "description": "Find Terraform resource definitions",
            "category": "code_analysis",
        },
        "token": {
            "pattern": r"token\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find token assignments",
            "category": "security",
        },
        "credential": {
            "pattern": r"credential[s]?\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find credential assignments",
            "category": "security",
        },
        "private_key": {
            "pattern": r"private[_-]?key\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find private key assignments",
            "category": "security",
        },
        "ssh_key": {
            "pattern": r"ssh[_-]?key\s*=\s*['\"]([^'\"]+)['\"]",
            "description": "Find SSH key assignments",
            "category": "security",
        },
        "jwt_token": {
            "pattern": r"eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*",
            "description": "Find JWT tokens",
            "category": "security",
        },
        "github_token": {
            "pattern": r"ghp_[A-Za-z0-9]{36}",
            "description": "Find GitHub personal access tokens",
            "category": "security",
        },
        "slack_token": {
            "pattern": r"xox[baprs]-[0-9A-Za-z-]{10,}",
            "description": "Find Slack tokens",
            "category": "security",
        },
        "credit_card": {
            "pattern": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            "description": "Find credit card numbers",
            "category": "security",
        },
        "ssn": {
            "pattern": r"\b\d{3}-\d{2}-\d{4}\b",
            "description": "Find Social Security Numbers",
            "category": "security",
        },
        "publicly_accessible": {
            "pattern": r"publicly_accessible\s*=\s*(?:true|1)",
            "description": "Find publicly accessible resources",
            "category": "compliance",
        },
        "no_encryption": {
            "pattern": r"encrypt[ed]?\s*=\s*(?:false|0|null)",
            "description": "Find resources without encryption",
            "category": "compliance",
        },
        "no_versioning": {
            "pattern": r"versioning\s*=\s*(?:false|0|null)",
            "description": "Find resources without versioning",
            "category": "compliance",
        },
        "no_logging": {
            "pattern": r"logging\s*=\s*(?:false|0|null)",
            "description": "Find resources without logging",
            "category": "compliance",
        },
        "no_mfa": {
            "pattern": r"mfa[_-]?enabled\s*=\s*(?:false|0|null)",
            "description": "Find resources without MFA",
            "category": "compliance",
        },
        "insecure_protocol": {
            "pattern": r"(?:http://|ftp://)",
            "description": "Find insecure protocols (HTTP, FTP)",
            "category": "security",
        },
        "latest_tag": {
            "pattern": r":latest\b",
            "description": "Find Docker images using 'latest' tag",
            "category": "code_quality",
        },
        "no_resource_limits": {
            "pattern": r"resources:\s*\{\s*\}",
            "description": "Find Kubernetes resources without limits",
            "category": "code_quality",
        },
        "hardcoded_port": {
            "pattern": r"port\s*=\s*(\d{1,5})",
            "description": "Find hardcoded port numbers",
            "category": "code_quality",
        },
        "hardcoded_url": {
            "pattern": r"url\s*=\s*['\"](https?://[^'\"]+)['\"]",
            "description": "Find hardcoded URLs",
            "category": "code_quality",
        },
        "terraform_data_source": {
            "pattern": r"data\s+[\"'](\w+)[\"']\s+[\"'](\w+)[\"']",
            "description": "Find Terraform data source definitions",
            "category": "code_analysis",
        },
        "terraform_variable": {
            "pattern": r"variable\s+[\"'](\w+)[\"']",
            "description": "Find Terraform variable definitions",
            "category": "code_analysis",
        },
        "kubernetes_secret": {
            "pattern": r"kind:\s*Secret",
            "description": "Find Kubernetes Secret resources",
            "category": "code_analysis",
        },
        "kubernetes_configmap": {
            "pattern": r"kind:\s*ConfigMap",
            "description": "Find Kubernetes ConfigMap resources",
            "category": "code_analysis",
        },
        "dockerfile_from": {
            "pattern": r"FROM\s+(\S+)",
            "description": "Find Dockerfile FROM statements",
            "category": "code_analysis",
        },
        "import_statement": {
            "pattern": r"import\s+['\"]([^'\"]+)['\"]",
            "description": "Find import statements",
            "category": "code_analysis",
        },
    }

    @classmethod
    def get_template(cls, template_name: str) -> str | None:
        """Get pattern template by name.

        Args:
            template_name: Template name

        Returns:
            Regex pattern or None if not found
        """
        template = cls.TEMPLATES.get(template_name)
        if template:
            return template["pattern"]
        return None

    @classmethod
    def list_templates(cls, category: str | None = None) -> list[dict[str, Any]]:
        """List available templates.

        Args:
            category: Filter by category (security, compliance, code_analysis, code_quality)

        Returns:
            List of template dictionaries
        """
        templates = []
        for name, template in cls.TEMPLATES.items():
            if category is None or template["category"] == category:
                templates.append({
                    "name": name,
                    "pattern": template["pattern"],
                    "description": template["description"],
                    "category": template["category"],
                })
        return templates

