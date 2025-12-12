"""Flux Kustomization parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class FluxParser(ToolParser):
    """Parser for Flux Kustomization and GitRepository manifests."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Flux resource types.
        
        Args:
            code: Flux YAML manifest content
            
        Returns:
            List of resource names/types
        """
        resources = []
        try:
            manifest = yaml.safe_load(code)
            
            kind = manifest.get("kind", "")
            name = manifest.get("metadata", {}).get("name", "")
            
            if name:
                resources.append(f"{kind}:{name}")
            
            if kind == "Kustomization":
                spec = manifest.get("spec", {})
                source_ref = spec.get("sourceRef", {})
                if source_ref:
                    resources.append(f"source:{source_ref.get('name', '')}")
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Flux manifest.
        
        Args:
            code: Flux YAML manifest content
            
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
            code: Flux YAML manifest content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "helm" in code_lower:
            services.append("helm")
        if "kustomize" in code_lower:
            services.append("kustomize")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Flux metadata.
        
        Args:
            code: Flux YAML manifest content
            
        Returns:
            Dictionary with Flux metadata
        """
        metadata = {}
        try:
            manifest = yaml.safe_load(code)
            
            metadata["kind"] = manifest.get("kind")
            metadata["apiVersion"] = manifest.get("apiVersion")
            metadata["name"] = manifest.get("metadata", {}).get("name")
            metadata["namespace"] = manifest.get("metadata", {}).get("namespace")
            
            spec = manifest.get("spec", {})
            
            if manifest.get("kind") == "Kustomization":
                metadata["path"] = spec.get("path")
                metadata["interval"] = spec.get("interval")
                metadata["prune"] = spec.get("prune", False)
            elif manifest.get("kind") == "GitRepository":
                metadata["url"] = spec.get("url")
                metadata["interval"] = spec.get("interval")
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Flux manifest syntax.
        
        Args:
            code: Flux YAML manifest content
            
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
            
            valid_kinds = ["Kustomization", "GitRepository", "HelmRelease", "OCIRepository"]
            return "fluxcd.io" in api_version or "kustomize.toolkit.fluxcd.io" in api_version and kind in valid_kinds
        except yaml.YAMLError:
            return False

