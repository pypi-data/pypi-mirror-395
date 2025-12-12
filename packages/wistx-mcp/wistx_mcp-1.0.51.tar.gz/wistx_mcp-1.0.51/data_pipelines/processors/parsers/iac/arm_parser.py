"""Azure ARM Template parser."""

import json
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class ARMParser(ToolParser):
    """Parser for Azure ARM Templates (JSON)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract ARM resource types.
        
        Args:
            code: ARM template JSON content
            
        Returns:
            List of resource types (e.g., ["Microsoft.Storage/storageAccounts"])
        """
        resources = []
        template = self._parse_template(code)
        
        if not template:
            return resources
        
        resources_section = template.get("resources", [])
        for resource in resources_section:
            if isinstance(resource, dict):
                resource_type = resource.get("type", "")
                if resource_type:
                    resources.append(resource_type)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from ARM template.
        
        Args:
            code: ARM template JSON content
            
        Returns:
            Always returns "azure" for ARM templates
        """
        return "azure"

    def extract_services(self, code: str) -> list[str]:
        """Extract Azure services from ARM template.
        
        Args:
            code: ARM template JSON content
            
        Returns:
            List of service names
        """
        services = []
        resources = self.extract_resources(code)
        
        service_mapping = {
            "Microsoft.Compute/virtualMachines": "compute",
            "Microsoft.Storage/storageAccounts": "storage",
            "Microsoft.Sql/servers": "sql",
            "Microsoft.ContainerService/managedClusters": "aks",
            "Microsoft.Web/sites": "appservice",
            "Microsoft.KeyVault/vaults": "keyvault",
        }
        
        for resource_type in resources:
            service = service_mapping.get(resource_type)
            if service and service not in services:
                services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract ARM template metadata.
        
        Args:
            code: ARM template JSON content
            
        Returns:
            Dictionary with ARM template metadata
        """
        metadata = {}
        template = self._parse_template(code)
        
        if template:
            metadata["$schema"] = template.get("$schema")
            metadata["contentVersion"] = template.get("contentVersion")
            metadata["parameters"] = list(template.get("parameters", {}).keys())
            metadata["outputs"] = list(template.get("outputs", {}).keys())
            metadata["resources_count"] = len(template.get("resources", []))
        
        return metadata

    def _parse_template(self, code: str) -> dict[str, Any] | None:
        """Parse ARM template JSON.
        
        Args:
            code: Template content
            
        Returns:
            Parsed template dictionary or None
        """
        try:
            return json.loads(code)
        except json.JSONDecodeError:
            return None

    def validate_syntax(self, code: str) -> bool:
        """Basic ARM template syntax validation.
        
        Args:
            code: ARM template JSON content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        template = self._parse_template(code)
        if not template:
            return False
        
        has_schema = "$schema" in template
        has_resources = "resources" in template
        
        return has_schema and has_resources

