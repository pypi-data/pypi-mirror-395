"""Terraform resource mapping loader.

Loads and caches mappings between cloud provider resource types
and Terraform resource types.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

from wistx_mcp.models.cloud_discovery import CloudProvider, ImportPhase

logger = logging.getLogger(__name__)


class TerraformMapping:
    """A mapping from cloud resource type to Terraform resource type."""
    
    def __init__(
        self,
        cloud_type: str,
        terraform_type: str,
        import_id_template: str,
        import_phase: ImportPhase,
        name_tag_path: str | None,
        fallback_name_path: str | None,
        discovery_api: str,
        dependencies: list[str],
    ):
        self.cloud_type = cloud_type
        self.terraform_type = terraform_type
        self.import_id_template = import_id_template
        self.import_phase = import_phase
        self.name_tag_path = name_tag_path
        self.fallback_name_path = fallback_name_path
        self.discovery_api = discovery_api
        self.dependencies = dependencies


class TerraformMappingLoader:
    """Loads and provides access to Terraform resource mappings."""
    
    # Path to mapping files relative to project root
    MAPPING_FILES = {
        CloudProvider.AWS: "data/resource_types/aws_terraform_mappings.json",
    }
    
    def __init__(self, base_path: Path | None = None):
        """Initialize the loader.
        
        Args:
            base_path: Base path for finding mapping files. If None,
                      uses the project root.
        """
        if base_path is None:
            # Navigate from this file to project root
            base_path = Path(__file__).parent.parent.parent.parent.parent
        self.base_path = base_path
        self._cache: dict[CloudProvider, dict[str, TerraformMapping]] = {}
    
    def load_mappings(self, provider: CloudProvider) -> dict[str, TerraformMapping]:
        """Load mappings for a cloud provider.
        
        Args:
            provider: The cloud provider to load mappings for
            
        Returns:
            Dictionary mapping cloud resource types to TerraformMapping
            
        Raises:
            FileNotFoundError: If mapping file doesn't exist
            ValueError: If mapping file is invalid
        """
        if provider in self._cache:
            return self._cache[provider]
        
        if provider not in self.MAPPING_FILES:
            raise ValueError(f"No mapping file configured for provider: {provider}")
        
        mapping_path = self.base_path / self.MAPPING_FILES[provider]
        
        if not mapping_path.exists():
            raise FileNotFoundError(
                f"Terraform mapping file not found: {mapping_path}"
            )
        
        logger.info("Loading Terraform mappings from %s", mapping_path)
        
        try:
            with open(mapping_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in mapping file: {e}") from e
        
        mappings: dict[str, TerraformMapping] = {}
        
        for cloud_type, config in data.get("mappings", {}).items():
            try:
                phase_str = config.get("import_phase", "Compute")
                import_phase = ImportPhase(phase_str)
            except ValueError:
                logger.warning(
                    "Unknown import phase '%s' for %s, defaulting to Compute",
                    phase_str,
                    cloud_type,
                )
                import_phase = ImportPhase.COMPUTE
            
            mappings[cloud_type] = TerraformMapping(
                cloud_type=cloud_type,
                terraform_type=config["terraform_type"],
                import_id_template=config["import_id_template"],
                import_phase=import_phase,
                name_tag_path=config.get("name_tag_path"),
                fallback_name_path=config.get("fallback_name_path"),
                discovery_api=config.get("discovery_api", ""),
                dependencies=config.get("dependencies", []),
            )
        
        self._cache[provider] = mappings
        provider_name = provider.value if hasattr(provider, 'value') else str(provider)
        logger.info(
            "Loaded %d Terraform mappings for %s",
            len(mappings),
            provider_name,
        )
        
        return mappings
    
    def get_mapping(
        self,
        provider: CloudProvider,
        cloud_type: str,
    ) -> TerraformMapping | None:
        """Get mapping for a specific cloud resource type.
        
        Args:
            provider: The cloud provider
            cloud_type: The cloud resource type (e.g., AWS::EC2::Instance)
            
        Returns:
            TerraformMapping if found, None otherwise
        """
        mappings = self.load_mappings(provider)
        return mappings.get(cloud_type)
    
    def get_terraform_type(
        self,
        provider: CloudProvider,
        cloud_type: str,
    ) -> str | None:
        """Get Terraform resource type for a cloud resource type.
        
        Args:
            provider: The cloud provider
            cloud_type: The cloud resource type
            
        Returns:
            Terraform resource type if found, None otherwise
        """
        mapping = self.get_mapping(provider, cloud_type)
        return mapping.terraform_type if mapping else None
    
    def get_supported_types(self, provider: CloudProvider) -> list[str]:
        """Get list of supported cloud resource types.
        
        Args:
            provider: The cloud provider
            
        Returns:
            List of supported cloud resource types
        """
        mappings = self.load_mappings(provider)
        return list(mappings.keys())


# Global singleton instance
_loader: TerraformMappingLoader | None = None


def get_terraform_mapping_loader() -> TerraformMappingLoader:
    """Get the global TerraformMappingLoader instance."""
    global _loader
    if _loader is None:
        _loader = TerraformMappingLoader()
    return _loader

