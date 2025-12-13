"""Crossplane composition parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class CrossplaneParser(ToolParser):
    """Parser for Crossplane compositions and XRD definitions."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Crossplane resource types.
        
        Args:
            code: Crossplane YAML manifest
            
        Returns:
            List of resource types
        """
        resources = []
        try:
            manifest = yaml.safe_load(code)
            kind = manifest.get("kind", "")
            
            if kind == "Composition":
                composition_resources = manifest.get("spec", {}).get("resources", [])
                for resource in composition_resources:
                    base = resource.get("base", {})
                    resource_kind = base.get("kind", "")
                    if resource_kind:
                        resources.append(resource_kind)
            elif kind in ["CompositeResourceDefinition", "XRD"]:
                spec = manifest.get("spec", {})
                group = spec.get("group", "")
                names = spec.get("names", {})
                kind_name = names.get("kind", "")
                if group and kind_name:
                    resources.append(f"{group}/{kind_name}")
            else:
                if kind:
                    resources.append(kind)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Crossplane.
        
        Args:
            code: Crossplane YAML manifest
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "ec2" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower:
            return "gcp"
        if "azure" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract cloud services from Crossplane.
        
        Args:
            code: Crossplane YAML manifest
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "rds" in code_lower or "database" in code_lower:
            services.append("rds")
        if "s3" in code_lower or "bucket" in code_lower:
            services.append("s3")
        if "eks" in code_lower or "cluster" in code_lower:
            services.append("eks")
        if "gke" in code_lower:
            services.append("gke")
        if "aks" in code_lower:
            services.append("aks")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Crossplane metadata.
        
        Args:
            code: Crossplane YAML manifest
            
        Returns:
            Dictionary with Crossplane metadata
        """
        metadata = {}
        try:
            manifest = yaml.safe_load(code)
            
            metadata["kind"] = manifest.get("kind")
            metadata["apiVersion"] = manifest.get("apiVersion")
            metadata["name"] = manifest.get("metadata", {}).get("name")
            
            if manifest.get("kind") == "Composition":
                spec = manifest.get("spec", {})
                metadata["composite_type"] = spec.get("compositeTypeRef", {}).get("name")
                metadata["resources_count"] = len(spec.get("resources", []))
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Crossplane syntax.
        
        Args:
            code: Crossplane YAML manifest
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            manifest = yaml.safe_load(code)
            if not isinstance(manifest, dict):
                return False
            
            valid_kinds = ["Composition", "CompositeResourceDefinition", "XRD", "Provider"]
            kind = manifest.get("kind", "")
            
            return kind in valid_kinds
        except yaml.YAMLError:
            return False

