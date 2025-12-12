"""Base classes for cloud discovery providers.

This module defines the abstract interfaces that all cloud providers must implement.
"""

from abc import ABC, abstractmethod
from typing import Any, NamedTuple

from wistx_mcp.models.cloud_discovery import (
    CloudProvider,
    DiscoveredResource,
    NameResolution,
)


class CloudCredentials(NamedTuple):
    """Generic cloud credentials container."""
    
    provider: CloudProvider
    credentials: dict[str, Any]
    expires_at: Any | None = None


class CloudCredentialProvider(ABC):
    """Abstract base class for cloud credential providers.
    
    All credential providers must implement this interface.
    Credentials are NEVER persisted - they exist only in memory.
    """
    
    @property
    @abstractmethod
    def provider(self) -> CloudProvider:
        """Return the cloud provider this credential provider supports."""
        ...
    
    @abstractmethod
    async def get_credentials(self, **kwargs: Any) -> CloudCredentials:
        """Get credentials for the cloud provider.
        
        Args:
            **kwargs: Provider-specific arguments (e.g., role_arn for AWS)
            
        Returns:
            CloudCredentials with temporary credentials
            
        Raises:
            PermissionError: If credentials cannot be obtained
            ValueError: If required arguments are missing
        """
        ...
    
    @abstractmethod
    def clear_credentials(self) -> None:
        """Clear any cached credentials from memory.
        
        Must be called after use to ensure credentials don't persist.
        """
        ...
    
    @abstractmethod
    def is_expired(self) -> bool:
        """Check if current credentials are expired."""
        ...


class CloudResourceNameResolver(ABC):
    """Abstract base class for resolving cloud resource names to Terraform names.
    
    Each cloud provider has different naming conventions. This interface
    allows provider-specific implementations while maintaining consistency.
    """
    
    @property
    @abstractmethod
    def provider(self) -> CloudProvider:
        """Return the cloud provider this resolver supports."""
        ...
    
    @abstractmethod
    def resolve_terraform_name(
        self,
        resource: DiscoveredResource,
    ) -> NameResolution:
        """Resolve a Terraform name for the given resource.
        
        Args:
            resource: The discovered resource needing a name
            
        Returns:
            NameResolution with the resolved name and metadata
        """
        ...
    
    def sanitize_terraform_name(self, name: str) -> str:
        """Sanitize a name to be a valid Terraform identifier.
        
        Terraform identifiers must:
        - Start with a letter or underscore
        - Contain only letters, digits, underscores, and hyphens
        - Not be empty
        
        Args:
            name: The name to sanitize
            
        Returns:
            A valid Terraform identifier
        """
        import re
        
        if not name:
            return "unnamed_resource"
        
        # Replace spaces and special chars with underscores
        sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", name.lower())
        
        # Remove consecutive underscores
        sanitized = re.sub(r"_+", "_", sanitized)
        
        # Ensure starts with letter or underscore
        if sanitized[0].isdigit() or sanitized[0] == "-":
            sanitized = f"r_{sanitized}"
        
        # Remove trailing underscores
        sanitized = sanitized.rstrip("_")
        
        return sanitized or "unnamed_resource"


class CloudDiscoveryProvider(ABC):
    """Abstract base class for cloud resource discovery.
    
    All cloud providers must implement this interface to enable
    resource discovery and context generation.
    """
    
    @property
    @abstractmethod
    def provider(self) -> CloudProvider:
        """Return the cloud provider this discovery provider supports."""
        ...
    
    @property
    @abstractmethod
    def supported_resource_types(self) -> list[str]:
        """Return list of supported cloud resource types."""
        ...
    
    @abstractmethod
    async def discover_resources(
        self,
        credentials: CloudCredentials,
        regions: list[str] | None = None,
        resource_types: list[str] | None = None,
        tag_filters: dict[str, str] | None = None,
    ) -> list[DiscoveredResource]:
        """Discover resources in the cloud account.

        Args:
            credentials: Credentials for the cloud provider
            regions: Regions to scan (None = all available)
            resource_types: Filter by resource types (None = all supported)
            tag_filters: Filter by tags

        Returns:
            List of discovered resources

        Raises:
            PermissionError: If credentials are invalid or insufficient
            RuntimeError: If discovery fails
        """
        ...

    @abstractmethod
    def get_terraform_resource_type(self, cloud_resource_type: str) -> str:
        """Map cloud resource type to Terraform resource type.

        Args:
            cloud_resource_type: Cloud provider resource type
                (e.g., AWS::EC2::Instance)

        Returns:
            Terraform resource type (e.g., aws_instance)
        """
        ...

    @abstractmethod
    def get_terraform_import_id(
        self,
        resource: DiscoveredResource,
    ) -> str:
        """Get the ID to use for terraform import command.

        Args:
            resource: The discovered resource

        Returns:
            The ID to pass to `terraform import`
        """
        ...

    @abstractmethod
    async def get_available_regions(
        self,
        credentials: CloudCredentials,
    ) -> list[str]:
        """Get list of available regions for the account.

        Args:
            credentials: Credentials for the cloud provider

        Returns:
            List of region identifiers
        """
        ...

    @abstractmethod
    async def get_resource_details(
        self,
        credentials: CloudCredentials,
        resource: DiscoveredResource,
    ) -> dict[str, Any]:
        """Get detailed configuration for a specific resource.

        Args:
            credentials: Credentials for the cloud provider
            resource: The resource to get details for

        Returns:
            Detailed configuration dictionary
        """
        ...

