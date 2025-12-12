"""Pulumi code parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class PulumiParser(ToolParser):
    """Parser for Pulumi code (Python, TypeScript, Go, C#, Java)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Pulumi resource types.
        
        Args:
            code: Pulumi code content
            
        Returns:
            List of resource types
        """
        resources = []
        
        patterns = [
            r'pulumi\.([a-zA-Z]+)\.([a-zA-Z]+)\(',  # Python: pulumi.aws.s3.Bucket
            r'new\s+([a-zA-Z]+)\.([a-zA-Z]+)\(',  # TypeScript: new aws.s3.Bucket
            r'@pulumi/([a-zA-Z]+)',  # TypeScript imports
            r'pulumi\.([a-zA-Z]+)',  # Python imports
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                if isinstance(match, tuple):
                    provider = match[0] if len(match) > 0 else ""
                    resource = match[1] if len(match) > 1 else ""
                    if provider and resource:
                        resources.append(f"{provider}.{resource}")
                elif isinstance(match, str):
                    resources.append(match)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Pulumi code.
        
        Args:
            code: Pulumi code content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "pulumi.aws" in code_lower or "@pulumi/aws" in code_lower or "pulumi_aws" in code_lower:
            return "aws"
        if "pulumi.gcp" in code_lower or "@pulumi/gcp" in code_lower or "pulumi_gcp" in code_lower:
            return "gcp"
        if "pulumi.azure" in code_lower or "@pulumi/azure" in code_lower or "pulumi_azure" in code_lower:
            return "azure"
        if "pulumi.kubernetes" in code_lower or "@pulumi/kubernetes" in code_lower:
            return "kubernetes"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract cloud services from Pulumi code.
        
        Args:
            code: Pulumi code content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        service_patterns = {
            "rds": ["rds", "dbinstance", "database"],
            "s3": ["s3", "bucket"],
            "ec2": ["ec2", "instance"],
            "eks": ["eks", "cluster"],
            "lambda": ["lambda", "function"],
            "ecs": ["ecs", "service"],
            "gke": ["gke", "container.cluster"],
            "aks": ["aks", "containerservice"],
        }
        
        for service, patterns in service_patterns.items():
            if any(pattern in code_lower for pattern in patterns):
                if service not in services:
                    services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Pulumi-specific metadata.
        
        Args:
            code: Pulumi code content
            
        Returns:
            Dictionary with Pulumi metadata
        """
        metadata = {
            "language": self._detect_language(code),
            "exports": self._extract_exports(code),
            "config": self._extract_config(code),
        }
        return metadata

    def _detect_language(self, code: str) -> str | None:
        """Detect programming language."""
        if "import pulumi" in code or "from pulumi" in code:
            return "python"
        if "import * as pulumi" in code or "import { pulumi }" in code:
            return "typescript"
        if "package main" in code:
            return "go"
        if "using Pulumi" in code:
            return "csharp"
        return None

    def _extract_exports(self, code: str) -> list[str]:
        """Extract exported values."""
        exports = []
        patterns = [
            r'export\s+(?:const\s+)?(\w+)',  # TypeScript/JavaScript
            r'pulumi\.export\(["\'](\w+)["\']',  # Python
        ]
        for pattern in patterns:
            matches = re.findall(pattern, code)
            exports.extend(matches)
        return list(set(exports))

    def _extract_config(self, code: str) -> dict[str, Any]:
        """Extract Pulumi config."""
        config = {}
        pattern = r'config\.(?:get|require)\(["\']([^"\']+)["\']'
        matches = re.findall(pattern, code)
        if matches:
            config["keys"] = list(set(matches))
        return config

    def validate_syntax(self, code: str) -> bool:
        """Basic Pulumi syntax validation.
        
        Args:
            code: Pulumi code content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        has_pulumi = "pulumi" in code_lower
        has_resource = any(keyword in code_lower for keyword in ["bucket", "instance", "cluster", "function", "service"])
        
        return has_pulumi and has_resource

