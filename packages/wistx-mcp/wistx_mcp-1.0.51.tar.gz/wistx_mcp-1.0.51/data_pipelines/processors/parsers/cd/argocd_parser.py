"""ArgoCD Application parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class ArgoCDParser(ToolParser):
    """Parser for ArgoCD Application manifests."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract ArgoCD application components.
        
        Args:
            code: ArgoCD Application YAML content
            
        Returns:
            List of application/source names
        """
        resources = []
        try:
            manifest = yaml.safe_load(code)
            
            kind = manifest.get("kind", "")
            if kind == "Application":
                app_name = manifest.get("metadata", {}).get("name", "")
                if app_name:
                    resources.append(app_name)
                
                spec = manifest.get("spec", {})
                sources = spec.get("sources", [])
                if sources:
                    for source in sources:
                        repo_url = source.get("repoURL", "")
                        if repo_url:
                            resources.append(repo_url)
                else:
                    source = spec.get("source", {})
                    repo_url = source.get("repoURL", "")
                    if repo_url:
                        resources.append(repo_url)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from ArgoCD Application.
        
        Args:
            code: ArgoCD Application YAML content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "eks" in code_lower:
            return "aws"
        if "gcp" in code_lower or "gke" in code_lower:
            return "gcp"
        if "azure" in code_lower or "aks" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract services deployed.
        
        Args:
            code: ArgoCD Application YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "helm" in code_lower:
            services.append("helm")
        if "eks" in code_lower:
            services.append("eks")
        if "gke" in code_lower:
            services.append("gke")
        if "aks" in code_lower:
            services.append("aks")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract ArgoCD Application metadata.
        
        Args:
            code: ArgoCD Application YAML content
            
        Returns:
            Dictionary with ArgoCD metadata
        """
        metadata = {}
        try:
            manifest = yaml.safe_load(code)
            
            metadata["kind"] = manifest.get("kind")
            metadata["apiVersion"] = manifest.get("apiVersion")
            metadata["name"] = manifest.get("metadata", {}).get("name")
            metadata["namespace"] = manifest.get("metadata", {}).get("namespace")
            
            spec = manifest.get("spec", {})
            metadata["project"] = spec.get("project")
            metadata["sync_policy"] = spec.get("syncPolicy", {})
            
            destination = spec.get("destination", {})
            metadata["destination_server"] = destination.get("server")
            metadata["destination_namespace"] = destination.get("namespace")
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate ArgoCD Application syntax.
        
        Args:
            code: ArgoCD Application YAML content
            
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
            
            return "argoproj.io" in api_version and kind == "Application"
        except yaml.YAMLError:
            return False

