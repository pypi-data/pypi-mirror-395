"""Helm chart parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class HelmParser(ToolParser):
    """Parser for Helm charts (Chart.yaml and values.yaml)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Helm chart components.
        
        Args:
            code: Helm YAML content (Chart.yaml or values.yaml)
            
        Returns:
            List of chart/dependency names
        """
        resources = []
        config = self._parse_config(code)
        
        if not config:
            return resources
        
        if "name" in config:
            resources.append(config["name"])
        
        if "dependencies" in config:
            for dep in config["dependencies"]:
                if isinstance(dep, dict):
                    dep_name = dep.get("name", "")
                    if dep_name:
                        resources.append(f"dep:{dep_name}")
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Helm chart.
        
        Args:
            code: Helm YAML content
            
        Returns:
            Cloud provider name or None (Helm is cloud-agnostic)
        """
        code_lower = code.lower()
        
        if "eks" in code_lower or "aws" in code_lower:
            return "aws"
        if "gke" in code_lower or "gcp" in code_lower:
            return "gcp"
        if "aks" in code_lower or "azure" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract Kubernetes services/components.
        
        Args:
            code: Helm YAML content
            
        Returns:
            List of service names
        """
        services = ["kubernetes", "helm"]
        
        code_lower = code.lower()
        if "postgres" in code_lower or "postgresql" in code_lower:
            services.append("postgres")
        if "redis" in code_lower:
            services.append("redis")
        if "mongodb" in code_lower:
            services.append("mongodb")
        if "nginx" in code_lower:
            services.append("nginx")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Helm chart metadata.
        
        Args:
            code: Helm YAML content
            
        Returns:
            Dictionary with Helm metadata
        """
        metadata = {}
        try:
            config = self._parse_config(code)
            
            if config:
                metadata["name"] = config.get("name")
                metadata["version"] = config.get("version")
                metadata["apiVersion"] = config.get("apiVersion")
                metadata["description"] = config.get("description")
                metadata["appVersion"] = config.get("appVersion")
                metadata["dependencies_count"] = len(config.get("dependencies", []))
        except (AttributeError, TypeError):
            pass
        
        return metadata

    def _parse_config(self, code: str) -> dict[str, Any] | None:
        """Parse Helm YAML config.
        
        Args:
            code: Config content
            
        Returns:
            Parsed config dictionary or None
        """
        try:
            return yaml.safe_load(code)
        except yaml.YAMLError:
            return None

    def validate_syntax(self, code: str) -> bool:
        """Validate Helm chart syntax.
        
        Args:
            code: Helm YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        config = self._parse_config(code)
        if not config:
            return False
        
        has_name = "name" in config
        has_version = "version" in config
        has_api_version = "apiVersion" in config
        
        return has_name and (has_version or has_api_version)

