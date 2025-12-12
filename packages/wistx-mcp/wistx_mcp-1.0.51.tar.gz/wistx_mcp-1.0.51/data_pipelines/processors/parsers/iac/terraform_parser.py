"""Terraform code parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class TerraformParser(ToolParser):
    """Parser for Terraform code."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Terraform resource types.
        
        Args:
            code: Terraform code content
            
        Returns:
            List of resource types (e.g., ["aws.rds.db_instance", "aws.s3.bucket"])
        """
        resources = []
        pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"'
        matches = re.findall(pattern, code)
        
        for provider, resource_type in matches:
            resource_id = f"{provider}.{resource_type}"
            normalized = resource_id.replace("_", ".").lower()
            resources.append(normalized)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Terraform.
        
        Args:
            code: Terraform code content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if 'provider "aws"' in code_lower or 'aws_' in code_lower:
            return "aws"
        if 'provider "google"' in code_lower or 'google_' in code_lower or 'gcp_' in code_lower:
            return "gcp"
        if 'provider "azurerm"' in code_lower or 'azurerm_' in code_lower:
            return "azure"
        if 'provider "oci"' in code_lower or 'oci_' in code_lower:
            return "oracle"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract AWS services from Terraform.
        
        Args:
            code: Terraform code content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        aws_services = {
            "aws_db_instance": "rds",
            "aws_rds": "rds",
            "aws_s3_bucket": "s3",
            "aws_instance": "ec2",
            "aws_eks_cluster": "eks",
            "aws_lambda_function": "lambda",
            "aws_ecs": "ecs",
            "aws_cloudfront": "cloudfront",
            "aws_route53": "route53",
            "aws_iam": "iam",
            "aws_vpc": "vpc",
            "aws_security_group": "ec2",
        }
        
        for tf_resource, service in aws_services.items():
            if tf_resource in code_lower:
                if service not in services:
                    services.append(service)
        
        gcp_services = {
            "google_compute_instance": "compute",
            "google_sql_database_instance": "sql",
            "google_storage_bucket": "storage",
            "google_container_cluster": "gke",
        }
        
        for tf_resource, service in gcp_services.items():
            if tf_resource in code_lower:
                if service not in services:
                    services.append(service)
        
        azure_services = {
            "azurerm_virtual_machine": "compute",
            "azurerm_sql_database": "sql",
            "azurerm_storage_account": "storage",
            "azurerm_kubernetes_cluster": "aks",
        }
        
        for tf_resource, service in azure_services.items():
            if tf_resource in code_lower:
                if service not in services:
                    services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Terraform-specific metadata.
        
        Args:
            code: Terraform code content
            
        Returns:
            Dictionary with Terraform metadata
        """
        metadata = {
            "modules": self._extract_modules(code),
            "variables": self._extract_variables(code),
            "outputs": self._extract_outputs(code),
            "data_sources": self._extract_data_sources(code),
        }
        return metadata

    def _extract_modules(self, code: str) -> list[str]:
        """Extract module references."""
        modules = []
        pattern = r'module\s+"([^"]+)"'
        matches = re.findall(pattern, code)
        return matches

    def _extract_variables(self, code: str) -> list[str]:
        """Extract variable declarations."""
        variables = []
        pattern = r'variable\s+"([^"]+)"'
        matches = re.findall(pattern, code)
        return matches

    def _extract_outputs(self, code: str) -> list[str]:
        """Extract output declarations."""
        outputs = []
        pattern = r'output\s+"([^"]+)"'
        matches = re.findall(pattern, code)
        return matches

    def _extract_data_sources(self, code: str) -> list[str]:
        """Extract data source references."""
        data_sources = []
        pattern = r'data\s+"([^"]+)"\s+"([^"]+)"'
        matches = re.findall(pattern, code)
        return [f"{provider}.{resource}" for provider, resource in matches]

    def validate_syntax(self, code: str) -> bool:
        """Basic Terraform syntax validation.
        
        Args:
            code: Terraform code content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        has_resource = 'resource' in code_lower
        has_data = 'data' in code_lower
        has_module = 'module' in code_lower
        has_provider = 'provider' in code_lower
        
        return has_resource or has_data or has_module or has_provider

