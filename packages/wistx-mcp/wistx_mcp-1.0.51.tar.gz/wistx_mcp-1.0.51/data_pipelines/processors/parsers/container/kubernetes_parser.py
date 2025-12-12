"""Kubernetes manifest parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class KubernetesParser(ToolParser):
    """Parser for Kubernetes YAML manifests."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Kubernetes resource kinds.
        
        Args:
            code: Kubernetes YAML manifest
            
        Returns:
            List of resource kinds (e.g., ["Deployment", "Service", "ConfigMap"])
        """
        resources = []
        
        try:
            if "---" in code:
                manifests = code.split("---")
            else:
                manifests = [code]
            
            for manifest_text in manifests:
                if not manifest_text.strip():
                    continue
                
                manifest = yaml.safe_load(manifest_text)
                if manifest and isinstance(manifest, dict):
                    kind = manifest.get("kind", "")
                    if kind:
                        resources.append(kind)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Kubernetes manifest.
        
        Args:
            code: Kubernetes YAML manifest
            
        Returns:
            Cloud provider name or None (Kubernetes is cloud-agnostic)
        """
        code_lower = code.lower()
        
        if "eks" in code_lower or "amazon" in code_lower:
            return "aws"
        if "gke" in code_lower or "google" in code_lower:
            return "gcp"
        if "aks" in code_lower or "azure" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract Kubernetes services/components.
        
        Args:
            code: Kubernetes YAML manifest
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "deployment" in code_lower:
            services.append("kubernetes")
        if "service" in code_lower:
            services.append("kubernetes")
        if "ingress" in code_lower:
            services.append("kubernetes")
        if "statefulset" in code_lower:
            services.append("kubernetes")
        if "daemonset" in code_lower:
            services.append("kubernetes")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Kubernetes-specific metadata.
        
        Args:
            code: Kubernetes YAML manifest
            
        Returns:
            Dictionary with Kubernetes metadata
        """
        metadata = {}
        
        try:
            if "---" in code:
                manifests = code.split("---")
            else:
                manifests = [code]
            
            resources = []
            namespaces = []
            
            for manifest_text in manifests:
                if not manifest_text.strip():
                    continue
                
                manifest = yaml.safe_load(manifest_text)
                if manifest and isinstance(manifest, dict):
                    kind = manifest.get("kind", "")
                    namespace = manifest.get("metadata", {}).get("namespace", "default")
                    
                    if kind:
                        resources.append(kind)
                    if namespace:
                        namespaces.append(namespace)
            
            metadata["resources"] = list(set(resources))
            metadata["namespaces"] = list(set(namespaces))
            metadata["manifests_count"] = len([m for m in manifests if m.strip()])
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Kubernetes manifest syntax.
        
        Args:
            code: Kubernetes YAML manifest
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            if "---" in code:
                manifests = code.split("---")
            else:
                manifests = [code]
            
            for manifest_text in manifests:
                if not manifest_text.strip():
                    continue
                
                manifest = yaml.safe_load(manifest_text)
                if not isinstance(manifest, dict):
                    return False
                
                has_api_version = "apiVersion" in manifest
                has_kind = "kind" in manifest
                has_metadata = "metadata" in manifest
                
                if has_api_version and has_kind and has_metadata:
                    return True
            
            return False
        except yaml.YAMLError:
            return False

