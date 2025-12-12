"""GitLab CI configuration parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class GitLabCIParser(ToolParser):
    """Parser for GitLab CI configuration files."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract pipeline stages/jobs.
        
        Args:
            code: GitLab CI YAML content
            
        Returns:
            List of job/stage names
        """
        resources = []
        try:
            config = yaml.safe_load(code)
            
            stages = config.get("stages", [])
            resources.extend(stages)
            
            jobs = {k: v for k, v in config.items() if isinstance(v, dict) and "script" in v}
            resources.extend(list(jobs.keys()))
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from GitLab CI config.
        
        Args:
            code: GitLab CI YAML content
            
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
            code: GitLab CI YAML content
            
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
        if "gke" in code_lower:
            services.append("gke")
        if "aks" in code_lower:
            services.append("aks")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract GitLab CI metadata.
        
        Args:
            code: GitLab CI YAML content
            
        Returns:
            Dictionary with GitLab CI metadata
        """
        metadata = {}
        try:
            config = yaml.safe_load(code)
            
            metadata["stages"] = config.get("stages", [])
            metadata["variables"] = list(config.get("variables", {}).keys()) if isinstance(config.get("variables"), dict) else []
            metadata["image"] = config.get("image")
            
            jobs = {k: v for k, v in config.items() if isinstance(v, dict) and "script" in v}
            metadata["jobs"] = list(jobs.keys())
            metadata["jobs_count"] = len(jobs)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate GitLab CI syntax.
        
        Args:
            code: GitLab CI YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            config = yaml.safe_load(code)
            if not isinstance(config, dict):
                return False
            
            has_stages = "stages" in config
            has_jobs = any(isinstance(v, dict) and "script" in v for v in config.values())
            
            return has_stages or has_jobs
        except yaml.YAMLError:
            return False

