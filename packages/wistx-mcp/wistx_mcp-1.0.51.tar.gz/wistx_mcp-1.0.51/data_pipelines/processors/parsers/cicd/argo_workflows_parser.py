"""Argo Workflows parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class ArgoWorkflowsParser(ToolParser):
    """Parser for Argo Workflows YAML manifests."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract workflow templates/steps.
        
        Args:
            code: Argo Workflows YAML content
            
        Returns:
            List of template/step names
        """
        resources = []
        try:
            manifest = yaml.safe_load(code)
            
            kind = manifest.get("kind", "")
            if kind == "Workflow":
                templates = manifest.get("spec", {}).get("templates", [])
                for template in templates:
                    name = template.get("name", "")
                    if name:
                        resources.append(name)
            elif kind == "WorkflowTemplate":
                templates = manifest.get("spec", {}).get("templates", [])
                for template in templates:
                    name = template.get("name", "")
                    if name:
                        resources.append(name)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Argo Workflows.
        
        Args:
            code: Argo Workflows YAML content
            
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
        """Extract services used in workflows.
        
        Args:
            code: Argo Workflows YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "s3" in code_lower:
            services.append("s3")
        if "eks" in code_lower:
            services.append("eks")
        if "gke" in code_lower:
            services.append("gke")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Argo Workflows metadata.
        
        Args:
            code: Argo Workflows YAML content
            
        Returns:
            Dictionary with Argo Workflows metadata
        """
        metadata = {}
        try:
            manifest = yaml.safe_load(code)
            
            metadata["kind"] = manifest.get("kind")
            metadata["apiVersion"] = manifest.get("apiVersion")
            metadata["name"] = manifest.get("metadata", {}).get("name")
            
            spec = manifest.get("spec", {})
            templates = spec.get("templates", [])
            metadata["templates_count"] = len(templates)
            metadata["entrypoint"] = spec.get("entrypoint")
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Argo Workflows syntax.
        
        Args:
            code: Argo Workflows YAML content
            
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
            
            return "argoproj.io" in api_version and kind in ["Workflow", "WorkflowTemplate"]
        except yaml.YAMLError:
            return False

