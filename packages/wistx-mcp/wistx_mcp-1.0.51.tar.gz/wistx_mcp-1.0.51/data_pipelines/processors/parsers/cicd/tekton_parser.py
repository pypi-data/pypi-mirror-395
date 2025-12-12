"""Tekton pipeline parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class TektonParser(ToolParser):
    """Parser for Tekton Pipeline and Task manifests."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Tekton tasks/steps.
        
        Args:
            code: Tekton YAML manifest content
            
        Returns:
            List of task/step names
        """
        resources = []
        try:
            manifest = yaml.safe_load(code)
            
            kind = manifest.get("kind", "")
            
            if kind == "Pipeline":
                tasks = manifest.get("spec", {}).get("tasks", [])
                for task in tasks:
                    task_ref = task.get("taskRef", {})
                    task_name = task_ref.get("name", "") or task.get("name", "")
                    if task_name:
                        resources.append(task_name)
            elif kind == "Task":
                steps = manifest.get("spec", {}).get("steps", [])
                for step in steps:
                    step_name = step.get("name", "")
                    if step_name:
                        resources.append(step_name)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Tekton pipeline.
        
        Args:
            code: Tekton YAML manifest content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "s3" in code_lower or "eks" in code_lower:
            return "aws"
        if "gcp" in code_lower or "gke" in code_lower:
            return "gcp"
        if "azure" in code_lower or "aks" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract services used in Tekton pipeline.
        
        Args:
            code: Tekton YAML manifest content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "docker" in code_lower:
            services.append("docker")
        if "s3" in code_lower:
            services.append("s3")
        if "gcr" in code_lower or "gcr.io" in code_lower:
            services.append("gcr")
        if "ecr" in code_lower:
            services.append("ecr")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Tekton metadata.
        
        Args:
            code: Tekton YAML manifest content
            
        Returns:
            Dictionary with Tekton metadata
        """
        metadata = {}
        try:
            manifest = yaml.safe_load(code)
            
            metadata["kind"] = manifest.get("kind")
            metadata["apiVersion"] = manifest.get("apiVersion")
            metadata["name"] = manifest.get("metadata", {}).get("name")
            
            spec = manifest.get("spec", {})
            
            if manifest.get("kind") == "Pipeline":
                metadata["tasks_count"] = len(spec.get("tasks", []))
                metadata["params"] = list(spec.get("params", []))
            elif manifest.get("kind") == "Task":
                metadata["steps_count"] = len(spec.get("steps", []))
                metadata["params"] = list(spec.get("params", []))
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Tekton manifest syntax.
        
        Args:
            code: Tekton YAML manifest content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            manifest = yaml.safe_load(code)
            if not isinstance(manifest, dict):
                return False
            
            api_version = manifest.get("apiVersion", "")
            kind = manifest.get("kind", "")
            
            return "tekton.dev" in api_version and kind in ["Pipeline", "Task", "PipelineRun", "TaskRun"]
        except yaml.YAMLError:
            return False

