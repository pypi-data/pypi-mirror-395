"""Backstage component parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class BackstageParser(ToolParser):
    """Parser for Backstage component definitions."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Backstage component types.
        
        Args:
            code: Backstage component YAML content
            
        Returns:
            List of component/system names
        """
        resources = []
        try:
            manifest = yaml.safe_load(code)
            
            kind = manifest.get("kind", "")
            metadata = manifest.get("metadata", {})
            name = metadata.get("name", "")
            
            if name:
                resources.append(f"{kind}:{name}")
            
            spec = manifest.get("spec", {})
            
            if kind == "Component":
                system = spec.get("system", "")
                if system:
                    resources.append(f"system:{system}")
                
                domain = spec.get("domain", "")
                if domain:
                    resources.append(f"domain:{domain}")
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Backstage component.
        
        Args:
            code: Backstage component YAML content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower:
            return "gcp"
        if "azure" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract services/components.
        
        Args:
            code: Backstage component YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "docker" in code_lower:
            services.append("docker")
        if "postgres" in code_lower:
            services.append("postgres")
        if "redis" in code_lower:
            services.append("redis")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Backstage metadata.
        
        Args:
            code: Backstage component YAML content
            
        Returns:
            Dictionary with Backstage metadata
        """
        metadata = {}
        try:
            manifest = yaml.safe_load(code)
            
            metadata["kind"] = manifest.get("kind")
            metadata["apiVersion"] = manifest.get("apiVersion")
            metadata["name"] = manifest.get("metadata", {}).get("name")
            metadata["namespace"] = manifest.get("metadata", {}).get("namespace")
            
            spec = manifest.get("spec", {})
            metadata["type"] = spec.get("type")
            metadata["lifecycle"] = spec.get("lifecycle")
            metadata["system"] = spec.get("system")
            metadata["domain"] = spec.get("domain")
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Backstage component syntax.
        
        Args:
            code: Backstage component YAML content
            
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
            
            valid_kinds = ["Component", "System", "Domain", "API", "Location"]
            return "backstage.io" in api_version and kind in valid_kinds
        except yaml.YAMLError:
            return False

