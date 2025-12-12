"""Karpenter NodePool parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class KarpenterParser(ToolParser):
    """Parser for Karpenter NodePool and EC2NodeClass manifests."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Karpenter resource types.
        
        Args:
            code: Karpenter YAML manifest content
            
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
            
            if kind == "NodePool":
                spec = manifest.get("spec", {})
                template = spec.get("template", {})
                metadata = template.get("metadata", {})
                labels = metadata.get("labels", {})
                if labels:
                    resources.append(f"labels:{len(labels)}")
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Karpenter manifest.
        
        Args:
            code: Karpenter YAML manifest content
            
        Returns:
            Always returns "aws" for Karpenter (AWS-specific)
        """
        return "aws"

    def extract_services(self, code: str) -> list[str]:
        """Extract cloud services from Karpenter.
        
        Args:
            code: Karpenter YAML manifest content
            
        Returns:
            List of service names
        """
        services = ["eks"]
        
        code_lower = code.lower()
        if "ec2" in code_lower:
            services.append("ec2")
        if "fargate" in code_lower:
            services.append("fargate")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Karpenter metadata.
        
        Args:
            code: Karpenter YAML manifest content
            
        Returns:
            Dictionary with Karpenter metadata
        """
        metadata = {}
        try:
            manifest = yaml.safe_load(code)
            
            metadata["kind"] = manifest.get("kind")
            metadata["apiVersion"] = manifest.get("apiVersion")
            metadata["name"] = manifest.get("metadata", {}).get("name")
            metadata["namespace"] = manifest.get("metadata", {}).get("namespace")
            
            spec = manifest.get("spec", {})
            
            if manifest.get("kind") == "NodePool":
                metadata["limits"] = spec.get("limits", {})
                metadata["disruption"] = spec.get("disruption", {})
                template = spec.get("template", {})
                spec_template = template.get("spec", {})
                requirements = spec_template.get("requirements", [])
                metadata["requirements_count"] = len(requirements)
            elif manifest.get("kind") == "EC2NodeClass":
                metadata["ami_family"] = spec.get("amiFamily")
                metadata["subnet_selector_terms"] = len(spec.get("subnetSelectorTerms", []))
                metadata["security_group_selector_terms"] = len(spec.get("securityGroupSelectorTerms", []))
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Karpenter manifest syntax.
        
        Args:
            code: Karpenter YAML manifest content
            
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
            
            return "karpenter.sh" in api_version and kind in ["NodePool", "EC2NodeClass"]
        except yaml.YAMLError:
            return False

