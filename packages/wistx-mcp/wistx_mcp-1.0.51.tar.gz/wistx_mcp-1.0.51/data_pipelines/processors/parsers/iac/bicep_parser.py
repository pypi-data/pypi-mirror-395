"""Azure Bicep parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class BicepParser(ToolParser):
    """Parser for Azure Bicep files."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Bicep resource types.
        
        Args:
            code: Bicep code content
            
        Returns:
            List of resource types (e.g., ["Microsoft.Storage/storageAccounts", "Microsoft.Compute/virtualMachines"])
        """
        resources = []
        
        pattern = r'resource\s+(\w+)\s+["\']([^"\']+)["\']'
        matches = re.findall(pattern, code)
        
        for resource_name, resource_type in matches:
            resources.append(resource_type)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Bicep.
        
        Args:
            code: Bicep code content
            
        Returns:
            Always returns "azure" for Bicep
        """
        return "azure"

    def extract_services(self, code: str) -> list[str]:
        """Extract Azure services from Bicep.
        
        Args:
            code: Bicep code content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        service_mapping = {
            "compute": ["microsoft.compute", "virtualmachine", "vm"],
            "storage": ["microsoft.storage", "storageaccount"],
            "sql": ["microsoft.sql", "sqldatabase"],
            "aks": ["microsoft.containerservice", "managedcluster"],
            "appservice": ["microsoft.web", "sites"],
            "keyvault": ["microsoft.keyvault", "vaults"],
        }
        
        for service, patterns in service_mapping.items():
            if any(pattern in code_lower for pattern in patterns):
                if service not in services:
                    services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Bicep-specific metadata.
        
        Args:
            code: Bicep code content
            
        Returns:
            Dictionary with Bicep metadata
        """
        metadata = {
            "parameters": self._extract_parameters(code),
            "outputs": self._extract_outputs(code),
            "modules": self._extract_modules(code),
            "variables": self._extract_variables(code),
        }
        return metadata

    def _extract_parameters(self, code: str) -> list[str]:
        """Extract parameter names."""
        parameters = []
        pattern = r'param\s+(\w+)'
        matches = re.findall(pattern, code)
        return matches

    def _extract_outputs(self, code: str) -> list[str]:
        """Extract output names."""
        outputs = []
        pattern = r'output\s+(\w+)'
        matches = re.findall(pattern, code)
        return matches

    def _extract_modules(self, code: str) -> list[str]:
        """Extract module references."""
        modules = []
        pattern = r'module\s+(\w+)\s+["\']([^"\']+)["\']'
        matches = re.findall(pattern, code)
        return [name for name, _ in matches]

    def _extract_variables(self, code: str) -> list[str]:
        """Extract variable names."""
        variables = []
        pattern = r'var\s+(\w+)'
        matches = re.findall(pattern, code)
        return matches

    def validate_syntax(self, code: str) -> bool:
        """Basic Bicep syntax validation.
        
        Args:
            code: Bicep code content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        has_resource = "resource" in code_lower
        has_microsoft = "microsoft" in code_lower
        
        return has_resource and has_microsoft

