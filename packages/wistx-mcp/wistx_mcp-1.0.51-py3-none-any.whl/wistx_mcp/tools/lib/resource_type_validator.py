"""Provider-aware resource type validation utilities."""

import logging
from typing import Any

from wistx_mcp.tools.lib.resource_type_loader import get_resource_types

try:
    from api.utils.resource_types import (
        VALID_AWS_RESOURCE_TYPES,
        VALID_AZURE_RESOURCE_TYPES,
        VALID_GCP_RESOURCE_TYPES,
        VALID_RESOURCE_TYPES,
    )
except ImportError:
    VALID_AWS_RESOURCE_TYPES = set()
    VALID_GCP_RESOURCE_TYPES = set()
    VALID_AZURE_RESOURCE_TYPES = set()
    VALID_RESOURCE_TYPES = set()

logger = logging.getLogger(__name__)


def get_provider_resource_types(cloud_provider: str | None) -> set[str]:
    """Get valid resource types for a specific cloud provider.
    
    Loads from filesystem first, falls back to hardcoded lists.
    
    Args:
        cloud_provider: Cloud provider (aws, gcp, azure) or None for all
        
    Returns:
        Set of valid resource types for the provider
    """
    if cloud_provider:
        provider = cloud_provider.strip().lower()
        fs_types = get_resource_types(provider)
        if fs_types:
            return fs_types
        
        if provider == "aws":
            return VALID_AWS_RESOURCE_TYPES
        elif provider == "gcp":
            return VALID_GCP_RESOURCE_TYPES
        elif provider == "azure":
            return VALID_AZURE_RESOURCE_TYPES
    
    from wistx_mcp.tools.lib.resource_type_loader import get_all_resource_types
    fs_all = get_all_resource_types()
    if fs_all:
        return fs_all
    
    return VALID_RESOURCE_TYPES


def validate_provider_compatibility(
    resource_types: list[str],
    cloud_provider: str | None = None,
) -> tuple[list[str], list[str], dict[str, str]]:
    """Validate resource types are compatible with the specified cloud provider.
    
    Args:
        resource_types: List of resource types to validate
        cloud_provider: Cloud provider (aws, gcp, azure) or None for any
        
    Returns:
        Tuple of (valid_types, invalid_types, suggestions)
        where suggestions maps invalid types to suggested alternatives
    """
    valid_types = []
    invalid_types = []
    suggestions: dict[str, str] = {}
    
    if not cloud_provider:
        valid_types_upper = {rt.upper() for rt in VALID_RESOURCE_TYPES}
        for rt in resource_types:
            if rt and rt.strip():
                normalized = rt.strip().upper()
                if normalized in valid_types_upper:
                    valid_types.append(rt.strip())
                else:
                    invalid_types.append(rt.strip())
        return valid_types, invalid_types, suggestions
    
    provider = cloud_provider.strip().lower()
    provider_valid_types = get_provider_resource_types(provider)
    provider_valid_upper = {rt.upper() for rt in provider_valid_types}
    
    aws_valid_upper = {rt.upper() for rt in VALID_AWS_RESOURCE_TYPES}
    gcp_valid_upper = {rt.upper() for rt in VALID_GCP_RESOURCE_TYPES}
    azure_valid_upper = {rt.upper() for rt in VALID_AZURE_RESOURCE_TYPES}
    
    cross_provider_suggestions = {
        "aws": {
            "VPC": {"gcp": "Virtual Network", "azure": "Virtual Network"},
            "IAM": {"gcp": "Cloud IAM", "azure": "Active Directory"},
            "KMS": {"gcp": "Cloud KMS", "azure": "Key Vault"},
            "SecretsManager": {"gcp": "Cloud Secret Manager", "azure": "Key Vault"},
            "CloudWatch": {"gcp": "Cloud Monitoring", "azure": "Monitor"},
            "CloudWatch Logs": {"gcp": "Cloud Logging", "azure": "Log Analytics"},
            "ELB": {"gcp": "Cloud Load Balancing", "azure": "Load Balancer"},
            "ALB": {"gcp": "Cloud Load Balancing", "azure": "Load Balancer"},
            "NLB": {"gcp": "Cloud Load Balancing", "azure": "Load Balancer"},
            "WAF": {"gcp": "Cloud Armor", "azure": "Front Door"},
            "RDS": {"gcp": "Cloud SQL", "azure": "SQL Database"},
            "EC2": {"gcp": "GCE", "azure": "Virtual Machines"},
            "EKS": {"gcp": "GKE", "azure": "AKS"},
            "Lambda": {"gcp": "Cloud Functions", "azure": "Functions"},
            "S3": {"gcp": "Cloud Storage", "azure": "Storage Account"},
            "Route53": {"gcp": "Cloud DNS", "azure": "DNS"},
        },
        "gcp": {
            "Virtual Network": {"aws": "VPC", "azure": "Virtual Network"},
            "Cloud IAM": {"aws": "IAM", "azure": "Active Directory"},
            "Cloud KMS": {"aws": "KMS", "azure": "Key Vault"},
            "Cloud Secret Manager": {"aws": "SecretsManager", "azure": "Key Vault"},
            "Cloud Monitoring": {"aws": "CloudWatch", "azure": "Monitor"},
            "Cloud Logging": {"aws": "CloudWatch Logs", "azure": "Log Analytics"},
            "Cloud Load Balancing": {"aws": "ALB", "azure": "Load Balancer"},
            "Cloud Armor": {"aws": "WAF", "azure": "Front Door"},
            "Cloud SQL": {"aws": "RDS", "azure": "SQL Database"},
            "GCE": {"aws": "EC2", "azure": "Virtual Machines"},
            "GKE": {"aws": "EKS", "azure": "AKS"},
            "Cloud Functions": {"aws": "Lambda", "azure": "Functions"},
            "Cloud Storage": {"aws": "S3", "azure": "Storage Account"},
            "Cloud DNS": {"aws": "Route53", "azure": "DNS"},
        },
        "azure": {
            "Virtual Network": {"aws": "VPC", "gcp": "Virtual Network"},
            "Active Directory": {"aws": "IAM", "gcp": "Cloud IAM"},
            "Key Vault": {"aws": "KMS", "gcp": "Cloud KMS"},
            "Monitor": {"aws": "CloudWatch", "gcp": "Cloud Monitoring"},
            "Log Analytics": {"aws": "CloudWatch Logs", "gcp": "Cloud Logging"},
            "Load Balancer": {"aws": "ALB", "gcp": "Cloud Load Balancing"},
            "Front Door": {"aws": "WAF", "gcp": "Cloud Armor"},
            "SQL Database": {"aws": "RDS", "gcp": "Cloud SQL"},
            "Virtual Machines": {"aws": "EC2", "gcp": "GCE"},
            "AKS": {"aws": "EKS", "gcp": "GKE"},
            "Functions": {"aws": "Lambda", "gcp": "Cloud Functions"},
            "Storage Account": {"aws": "S3", "gcp": "Cloud Storage"},
            "DNS": {"aws": "Route53", "gcp": "Cloud DNS"},
        },
    }
    
    for rt in resource_types:
        if not rt or not rt.strip():
            continue
        
        rt_normalized = rt.strip()
        rt_upper = rt_normalized.upper()
        
        if rt_upper in provider_valid_upper:
            valid_types.append(rt_normalized)
        else:
            invalid_types.append(rt_normalized)
            
            if rt_upper in aws_valid_upper and provider == "gcp":
                if rt_normalized in cross_provider_suggestions.get("aws", {}):
                    suggestion = cross_provider_suggestions["aws"][rt_normalized].get("gcp")
                    if suggestion:
                        suggestions[rt_normalized] = suggestion
            elif rt_upper in aws_valid_upper and provider == "azure":
                if rt_normalized in cross_provider_suggestions.get("aws", {}):
                    suggestion = cross_provider_suggestions["aws"][rt_normalized].get("azure")
                    if suggestion:
                        suggestions[rt_normalized] = suggestion
            elif rt_upper in gcp_valid_upper and provider == "aws":
                if rt_normalized in cross_provider_suggestions.get("gcp", {}):
                    suggestion = cross_provider_suggestions["gcp"][rt_normalized].get("aws")
                    if suggestion:
                        suggestions[rt_normalized] = suggestion
            elif rt_upper in gcp_valid_upper and provider == "azure":
                if rt_normalized in cross_provider_suggestions.get("gcp", {}):
                    suggestion = cross_provider_suggestions["gcp"][rt_normalized].get("azure")
                    if suggestion:
                        suggestions[rt_normalized] = suggestion
            elif rt_upper in azure_valid_upper and provider == "aws":
                if rt_normalized in cross_provider_suggestions.get("azure", {}):
                    suggestion = cross_provider_suggestions["azure"][rt_normalized].get("aws")
                    if suggestion:
                        suggestions[rt_normalized] = suggestion
            elif rt_upper in azure_valid_upper and provider == "gcp":
                if rt_normalized in cross_provider_suggestions.get("azure", {}):
                    suggestion = cross_provider_suggestions["azure"][rt_normalized].get("gcp")
                    if suggestion:
                        suggestions[rt_normalized] = suggestion
    
    return valid_types, invalid_types, suggestions

