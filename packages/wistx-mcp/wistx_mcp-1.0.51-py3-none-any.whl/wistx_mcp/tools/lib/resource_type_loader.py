"""Filesystem-based resource type loader with caching."""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_RESOURCE_TYPES_CACHE: dict[str, dict[str, Any]] = {}
_DATA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "resource_types"


def _load_resource_types_file(provider: str) -> dict[str, Any] | None:
    """Load resource types from JSON file for a provider.
    
    Args:
        provider: Cloud provider (aws, gcp, azure)
        
    Returns:
        Dictionary with resource_types, normalization_map, and cross_provider_equivalents
        or None if file doesn't exist
    """
    if provider in _RESOURCE_TYPES_CACHE:
        return _RESOURCE_TYPES_CACHE[provider]
    
    file_path = _DATA_DIR / f"{provider}.json"
    
    if not file_path.exists():
        logger.debug("Resource types file not found: %s", file_path)
        return None
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            _RESOURCE_TYPES_CACHE[provider] = data
            logger.info(
                "Loaded %d resource types for %s from %s",
                len(data.get("resource_types", [])),
                provider.upper(),
                file_path,
            )
            return data
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in resource types file %s: %s", file_path, e)
        return None
    except IOError as e:
        logger.error("IO error loading resource types file %s: %s", file_path, e)
        return None


def get_resource_types(provider: str) -> set[str]:
    """Get valid resource types for a provider from filesystem.
    
    Falls back to hardcoded lists if file doesn't exist.
    
    Args:
        provider: Cloud provider (aws, gcp, azure)
        
    Returns:
        Set of valid resource types
    """
    data = _load_resource_types_file(provider)
    
    if data and "resource_types" in data:
        return set(data["resource_types"])
    
    logger.debug("Falling back to hardcoded resource types for %s", provider)
    from api.utils.resource_types import (
        VALID_AWS_RESOURCE_TYPES,
        VALID_AZURE_RESOURCE_TYPES,
        VALID_GCP_RESOURCE_TYPES,
    )
    
    if provider == "aws":
        return VALID_AWS_RESOURCE_TYPES
    elif provider == "gcp":
        return VALID_GCP_RESOURCE_TYPES
    elif provider == "azure":
        return VALID_AZURE_RESOURCE_TYPES
    
    return set()


def get_normalization_map(provider: str) -> dict[str, str]:
    """Get normalization map for a provider from filesystem.
    
    Falls back to empty dict if file doesn't exist.
    
    Args:
        provider: Cloud provider (aws, gcp, azure)
        
    Returns:
        Dictionary mapping normalized_key -> canonical_name
    """
    data = _load_resource_types_file(provider)
    
    if data and "normalization_map" in data:
        return data["normalization_map"]
    
    return {}


def get_cross_provider_equivalents(_provider: str) -> dict[str, dict[str, str]]:
    """Get cross-provider equivalents from filesystem.
    
    Falls back to empty dict if file doesn't exist.
    
    Args:
        provider: Cloud provider (aws, gcp, azure)
        
    Returns:
        Dictionary mapping {resource_type -> {target_provider -> equivalent_type}}
    """
    data = _load_resource_types_file("aws")
    
    if data and "cross_provider_equivalents" in data:
        return data["cross_provider_equivalents"]
    
    return {}


def reload_cache() -> None:
    """Reload resource types cache from filesystem.
    
    Useful for hot-reloading during development or after file updates.
    """
    global _RESOURCE_TYPES_CACHE
    _RESOURCE_TYPES_CACHE.clear()
    logger.info("Resource types cache cleared, will reload on next access")


def get_all_resource_types() -> set[str]:
    """Get all resource types across all providers.
    
    Returns:
        Set of all valid resource types
    """
    all_types = set()
    for provider in ["aws", "gcp", "azure"]:
        all_types.update(get_resource_types(provider))
    return all_types

