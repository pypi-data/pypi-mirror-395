"""PowerShell script parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class PowerShellParser(ToolParser):
    """Parser for PowerShell scripts (Azure/infrastructure automation)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract infrastructure cmdlets/commands used.
        
        Args:
            code: PowerShell script content
            
        Returns:
            List of cmdlets/commands (e.g., ["New-AzResourceGroup", "terraform"])
        """
        resources = []
        
        azure_cmdlets = [
            "New-Az", "Get-Az", "Set-Az", "Remove-Az", "Connect-Az",
            "New-AzureRm", "Get-AzureRm", "Set-AzureRm",
        ]
        
        code_lower = code.lower()
        for cmdlet_pattern in azure_cmdlets:
            pattern = cmdlet_pattern.replace("-Az", r"-[Aa]z").replace("-AzureRm", r"-[Aa]zure[Rr]m")
            matches = re.findall(pattern, code, re.IGNORECASE)
            resources.extend(matches)
        
        infrastructure_tools = ["terraform", "kubectl", "helm", "docker", "aws"]
        for tool in infrastructure_tools:
            if tool in code_lower:
                if tool not in resources:
                    resources.append(tool)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from PowerShell script.
        
        Args:
            code: PowerShell script content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "az" in code_lower or "azure" in code_lower or "new-az" in code_lower:
            return "azure"
        if "aws" in code_lower or "amazon" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower:
            return "gcp"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract services deployed/managed.
        
        Args:
            code: PowerShell script content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        azure_services = {
            "compute": ["virtualmachine", "vm", "compute"],
            "storage": ["storageaccount", "storage"],
            "sql": ["sqldatabase", "sql"],
            "aks": ["aks", "managedcluster", "containerservice"],
            "keyvault": ["keyvault", "vault"],
        }
        
        for service, patterns in azure_services.items():
            if any(pattern in code_lower for pattern in patterns):
                if service not in services:
                    services.append(service)
        
        if "eks" in code_lower or "kubernetes" in code_lower:
            services.append("eks")
        if "s3" in code_lower:
            services.append("s3")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract PowerShell script metadata.
        
        Args:
            code: PowerShell script content
            
        Returns:
            Dictionary with script metadata
        """
        metadata = {
            "functions": self._extract_functions(code),
            "cmdlets": self._extract_cmdlets(code),
            "variables": self._extract_variables(code),
        }
        return metadata

    def _extract_functions(self, code: str) -> list[str]:
        """Extract function names."""
        functions = []
        pattern = r'function\s+([A-Za-z-]+)'
        matches = re.findall(pattern, code)
        functions.extend(matches)
        return list(set(functions))

    def _extract_cmdlets(self, code: str) -> list[str]:
        """Extract PowerShell cmdlets."""
        cmdlets = []
        pattern = r'([A-Za-z]+-[A-Za-z]+)'
        matches = re.findall(pattern, code)
        azure_cmdlets = [m for m in matches if m.startswith(("New-", "Get-", "Set-", "Remove-", "Connect-"))]
        cmdlets.extend(azure_cmdlets)
        return list(set(cmdlets))

    def _extract_variables(self, code: str) -> list[str]:
        """Extract variable names."""
        variables = []
        pattern = r'\$([A-Za-z_][A-Za-z0-9_]*)'
        matches = re.findall(pattern, code)
        variables.extend(matches)
        return list(set(variables))

    def validate_syntax(self, code: str) -> bool:
        """Validate PowerShell script syntax.
        
        Args:
            code: PowerShell script content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        
        has_shebang = code.strip().startswith("#!") and "pwsh" in code_lower
        has_powershell = "powershell" in code_lower or "pwsh" in code_lower
        has_cmdlets = bool(re.search(r'[A-Za-z]+-[A-Za-z]+', code))
        has_infrastructure = any(tool in code_lower for tool in ["az", "azure", "terraform", "aws", "kubectl"])
        
        return (has_shebang or has_powershell) and (has_cmdlets or has_infrastructure)

