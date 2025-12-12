"""GitHub Actions workflow parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class GitHubActionsParser(ToolParser):
    """Parser for GitHub Actions workflows."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract pipeline jobs/stages.
        
        Args:
            code: GitHub Actions workflow YAML
            
        Returns:
            List of job names
        """
        try:
            workflow = yaml.safe_load(code)
            jobs = workflow.get("jobs", {})
            return list(jobs.keys())
        except (yaml.YAMLError, AttributeError, TypeError):
            return []

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from workflow.
        
        Args:
            code: GitHub Actions workflow YAML
            
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
            code: GitHub Actions workflow YAML
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "eks" in code_lower or "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("eks")
        if "ec2" in code_lower:
            services.append("ec2")
        if "lambda" in code_lower:
            services.append("lambda")
        if "s3" in code_lower:
            services.append("s3")
        if "rds" in code_lower:
            services.append("rds")
        if "gke" in code_lower:
            services.append("gke")
        if "aks" in code_lower:
            services.append("aks")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract GitHub Actions metadata.
        
        Args:
            code: GitHub Actions workflow YAML
            
        Returns:
            Dictionary with workflow metadata
        """
        try:
            workflow = yaml.safe_load(code)
            return {
                "name": workflow.get("name"),
                "on": workflow.get("on", {}),
                "jobs": list(workflow.get("jobs", {}).keys()),
                "triggers": self._extract_triggers(workflow),
                "environments": self._extract_environments(workflow),
            }
        except (yaml.YAMLError, AttributeError, TypeError):
            return {}

    def _extract_triggers(self, workflow: dict[str, Any]) -> list[str]:
        """Extract workflow triggers."""
        triggers = []
        on = workflow.get("on", {})
        
        if isinstance(on, dict):
            triggers.extend([key for key in on.keys() if key != "workflow_dispatch"])
        elif isinstance(on, list):
            triggers.extend(on)
        elif isinstance(on, str):
            triggers.append(on)
        
        return triggers

    def _extract_environments(self, workflow: dict[str, Any]) -> list[str]:
        """Extract deployment environments."""
        environments = []
        jobs = workflow.get("jobs", {})
        
        for job_name, job_config in jobs.items():
            env = job_config.get("environment")
            if env:
                if isinstance(env, str):
                    environments.append(env)
                elif isinstance(env, dict):
                    env_name = env.get("name")
                    if env_name:
                        environments.append(env_name)
        
        return list(set(environments))

    def validate_syntax(self, code: str) -> bool:
        """Validate GitHub Actions syntax.
        
        Args:
            code: GitHub Actions workflow YAML
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            workflow = yaml.safe_load(code)
            if not isinstance(workflow, dict):
                return False
            
            has_jobs = "jobs" in workflow
            has_on = "on" in workflow
            
            return has_jobs or has_on
        except yaml.YAMLError:
            return False

