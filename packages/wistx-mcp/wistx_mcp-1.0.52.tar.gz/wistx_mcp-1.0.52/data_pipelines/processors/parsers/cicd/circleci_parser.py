"""CircleCI configuration parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class CircleCIParser(ToolParser):
    """Parser for CircleCI configuration files."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract CircleCI jobs/workflows.
        
        Args:
            code: CircleCI config YAML content
            
        Returns:
            List of job/workflow names
        """
        resources = []
        try:
            config = yaml.safe_load(code)
            
            jobs = config.get("jobs", {})
            resources.extend(list(jobs.keys()))
            
            workflows = config.get("workflows", {})
            workflow_names = workflows.keys() if isinstance(workflows, dict) else []
            resources.extend(list(workflow_names))
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from CircleCI config.
        
        Args:
            code: CircleCI config YAML content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "amazon" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower:
            return "gcp"
        if "azure" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract services deployed/tested.
        
        Args:
            code: CircleCI config YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "eks" in code_lower or "kubernetes" in code_lower:
            services.append("eks")
        if "ec2" in code_lower:
            services.append("ec2")
        if "lambda" in code_lower:
            services.append("lambda")
        if "s3" in code_lower:
            services.append("s3")
        if "docker" in code_lower:
            services.append("docker")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract CircleCI metadata.
        
        Args:
            code: CircleCI config YAML content
            
        Returns:
            Dictionary with CircleCI metadata
        """
        metadata = {}
        try:
            config = yaml.safe_load(code)
            
            metadata["version"] = config.get("version")
            metadata["jobs"] = list(config.get("jobs", {}).keys())
            metadata["jobs_count"] = len(config.get("jobs", {}))
            
            workflows = config.get("workflows", {})
            if isinstance(workflows, dict):
                metadata["workflows"] = list(workflows.keys())
                metadata["workflows_count"] = len(workflows)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate CircleCI config syntax.
        
        Args:
            code: CircleCI config YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            config = yaml.safe_load(code)
            if not isinstance(config, dict):
                return False
            
            has_version = "version" in config
            has_jobs = "jobs" in config
            has_workflows = "workflows" in config
            
            return has_version and (has_jobs or has_workflows)
        except yaml.YAMLError:
            return False

