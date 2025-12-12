"""AWS Name Resolver.

Resolves Terraform resource names from AWS resources using:
1. Name tag (primary source) - most AWS resources support Name tag
2. Resource identifier (fallback) - DBInstanceIdentifier, FunctionName, etc.
3. Resource ID (final fallback) - i-1234567890abcdef0, vpc-12345678, etc.

The resolved name is sanitized to be a valid Terraform identifier.
"""

import logging
import re
from typing import Any

from wistx_mcp.models.cloud_discovery import (
    CloudProvider,
    DiscoveredResource,
    NameResolution,
    NameSource,
)
from wistx_mcp.tools.lib.cloud_discovery.base_provider import CloudResourceNameResolver
from wistx_mcp.tools.lib.cloud_discovery.terraform_mapping_loader import (
    TerraformMapping,
    TerraformMappingLoader,
    get_terraform_mapping_loader,
)

logger = logging.getLogger(__name__)


class AWSNameResolver(CloudResourceNameResolver):
    """Resolves Terraform names for AWS resources.
    
    Name Resolution Strategy:
    1. Check "Name" tag (most common naming convention in AWS)
    2. Check resource-specific name field (from mapping configuration)
    3. Fall back to resource ID
    
    Conflict Resolution:
    - Track used names per resource type
    - Append numeric suffix for duplicates (e.g., web_server, web_server_2)
    
    Sanitization Rules (Terraform identifiers):
    - Must start with letter or underscore
    - Can only contain letters, digits, underscores, hyphens
    - Convert to lowercase for consistency
    """
    
    def __init__(self, mapping_loader: TerraformMappingLoader | None = None):
        """Initialize the AWS name resolver.
        
        Args:
            mapping_loader: Optional TerraformMappingLoader for name path config
        """
        self._mapping_loader = mapping_loader or get_terraform_mapping_loader()
        self._mappings: dict[str, TerraformMapping] | None = None
        
        # Track used names per terraform type to avoid conflicts
        self._used_names: dict[str, set[str]] = {}
    
    @property
    def provider(self) -> CloudProvider:
        """Return AWS as the provider."""
        return CloudProvider.AWS
    
    def _get_mappings_dict(self) -> dict[str, TerraformMapping]:
        """Get cached mappings dictionary."""
        if self._mappings is None:
            self._mappings = self._mapping_loader.load_mappings(CloudProvider.AWS)
        return self._mappings
    
    def resolve_terraform_name(
        self,
        resource: DiscoveredResource,
    ) -> NameResolution:
        """Resolve a Terraform name for an AWS resource.
        
        Args:
            resource: The discovered AWS resource
            
        Returns:
            NameResolution with the resolved name and source
        """
        mapping = self._get_mappings_dict().get(resource.cloud_resource_type)
        
        original_name = None
        source = NameSource.RESOURCE_ID  # Default fallback

        # Strategy 1: Try Name tag
        if resource.tags and "Name" in resource.tags:
            original_name = resource.tags["Name"]
            source = NameSource.TAGS_NAME
            logger.debug(
                "Using Name tag for %s: %s",
                resource.cloud_resource_id,
                original_name,
            )

        # Strategy 2: Try resource-specific name field
        elif mapping and mapping.name_tag_path:
            name = self._extract_name_from_path(resource, mapping.name_tag_path)
            if name:
                original_name = name
                source = NameSource.RESOURCE_NAME
                logger.debug(
                    "Using %s for %s: %s",
                    mapping.name_tag_path,
                    resource.cloud_resource_id,
                    original_name,
                )

        # Strategy 3: Try fallback name path
        elif mapping and mapping.fallback_name_path:
            name = self._extract_name_from_path(resource, mapping.fallback_name_path)
            if name:
                original_name = name
                source = NameSource.RESOURCE_NAME

        # Final fallback: use resource ID
        if not original_name:
            original_name = resource.cloud_resource_id
            source = NameSource.RESOURCE_ID
            logger.debug(
                "Using resource ID as name for %s",
                resource.cloud_resource_id,
            )
        
        # Sanitize the name
        sanitized = self.sanitize_terraform_name(original_name)

        # Ensure uniqueness per terraform resource type
        terraform_type = resource.terraform_resource_type or "resource"
        unique_name = self._ensure_unique_name(terraform_type, sanitized)

        # Calculate confidence based on source
        confidence = 1.0 if source == NameSource.TAGS_NAME else (
            0.8 if source == NameSource.RESOURCE_NAME else 0.5
        )

        return NameResolution(
            terraform_name=unique_name,
            source=source,
            original_cloud_name=original_name,
            confidence=confidence,
        )
    
    def _extract_name_from_path(
        self,
        resource: DiscoveredResource,
        path: str,
    ) -> str | None:
        """Extract name from resource using path expression.
        
        Supports simple paths like:
        - "DBInstanceIdentifier" -> resource.raw_config.get("DBInstanceIdentifier")
        - "Tags[?Key=='Name'].Value | [0]" -> JMESPath-like expression
        """
        if not path or not resource.raw_config:
            return None
        
        # Handle JMESPath-like tag extraction
        if "Tags[?" in path:
            tags = resource.raw_config.get("Tags", [])
            if isinstance(tags, list):
                for tag in tags:
                    if tag.get("Key") == "Name":
                        return tag.get("Value")
            return None
        
        # Simple property access
        return resource.raw_config.get(path)
    
    def _ensure_unique_name(
        self,
        terraform_type: str,
        base_name: str,
    ) -> str:
        """Ensure name is unique within the terraform resource type."""
        if terraform_type not in self._used_names:
            self._used_names[terraform_type] = set()
        
        used = self._used_names[terraform_type]
        
        if base_name not in used:
            used.add(base_name)
            return base_name
        
        # Find next available suffix
        counter = 2
        while f"{base_name}_{counter}" in used:
            counter += 1
        
        unique = f"{base_name}_{counter}"
        used.add(unique)
        return unique
    
    def reset_used_names(self) -> None:
        """Reset the used names tracker.
        
        Call this between discovery sessions to start fresh.
        """
        self._used_names.clear()
    
    def get_used_names(self, terraform_type: str | None = None) -> dict[str, set[str]]:
        """Get currently used names.
        
        Args:
            terraform_type: Optional filter by terraform type
            
        Returns:
            Dictionary of terraform_type -> set of used names
        """
        if terraform_type:
            return {terraform_type: self._used_names.get(terraform_type, set())}
        return dict(self._used_names)

