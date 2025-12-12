"""Bash script parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class BashParser(ToolParser):
    """Parser for Bash scripts (infrastructure automation)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract infrastructure commands/tools used.
        
        Args:
            code: Bash script content
            
        Returns:
            List of tools/commands (e.g., ["terraform", "kubectl", "aws"])
        """
        resources = []
        
        infrastructure_tools = [
            "terraform", "pulumi", "ansible", "kubectl", "helm", "docker",
            "aws", "gcloud", "az", "kubectl", "kustomize", "terraform",
        ]
        
        code_lower = code.lower()
        for tool in infrastructure_tools:
            if tool in code_lower:
                if tool not in resources:
                    resources.append(tool)
        
        command_pattern = r'(terraform|kubectl|aws|gcloud|az|helm|docker)\s+\w+'
        matches = re.findall(command_pattern, code_lower)
        resources.extend(matches)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Bash script.
        
        Args:
            code: Bash script content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "amazon" in code_lower or "ec2" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower or "gcloud" in code_lower:
            return "gcp"
        if "azure" in code_lower or "az " in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract services deployed/managed.
        
        Args:
            code: Bash script content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "eks" in code_lower or "kubernetes" in code_lower or "kubectl" in code_lower:
            services.append("eks")
        if "ec2" in code_lower:
            services.append("ec2")
        if "s3" in code_lower:
            services.append("s3")
        if "rds" in code_lower:
            services.append("rds")
        if "lambda" in code_lower:
            services.append("lambda")
        if "docker" in code_lower:
            services.append("docker")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Bash script metadata.
        
        Args:
            code: Bash script content
            
        Returns:
            Dictionary with script metadata
        """
        metadata = {
            "functions": self._extract_functions(code),
            "commands": self._extract_commands(code),
            "variables": self._extract_variables(code),
        }
        return metadata

    def _extract_functions(self, code: str) -> list[str]:
        """Extract function names."""
        functions = []
        pattern = r'function\s+(\w+)|(\w+)\s*\(\)\s*\{'
        matches = re.findall(pattern, code)
        functions.extend([f[0] or f[1] for f in matches])
        return list(set(functions))

    def _extract_commands(self, code: str) -> list[str]:
        """Extract infrastructure commands."""
        commands = []
        pattern = r'(terraform|kubectl|aws|gcloud|az|helm|docker)\s+(\w+)'
        matches = re.findall(pattern, code, re.IGNORECASE)
        commands.extend([f"{tool} {cmd}" for tool, cmd in matches])
        return list(set(commands))

    def _extract_variables(self, code: str) -> list[str]:
        """Extract variable names."""
        variables = []
        pattern = r'\$(\w+)|\$\{(\w+)\}'
        matches = re.findall(pattern, code)
        variables.extend([v[0] or v[1] for v in matches])
        return list(set(variables))

    def validate_syntax(self, code: str) -> bool:
        """Validate Bash script syntax.
        
        Args:
            code: Bash script content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        
        has_shebang = code.strip().startswith("#!/") or "#!/bin/bash" in code_lower or "#!/usr/bin/env bash" in code_lower
        has_infrastructure = any(tool in code_lower for tool in ["terraform", "kubectl", "aws", "gcloud", "az", "helm", "docker"])
        
        return has_shebang or has_infrastructure

