"""Terraform State Parser for filtering already-managed resources."""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def parse_terraform_state(state_content: str) -> set[str]:
    """Extract managed resource IDs from Terraform state.
    
    Parses Terraform state file (JSON format) and extracts all resource IDs
    that are already managed. Supports both state v3 and v4 formats.
    
    Args:
        state_content: JSON string of terraform.tfstate file content
        
    Returns:
        Set of managed resource identifiers (IDs, ARNs, names)
        
    Raises:
        ValueError: If state content is invalid JSON
        KeyError: If state structure is unexpected
    """
    try:
        state = json.loads(state_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in Terraform state: {e}") from e
    
    managed_ids = set()
    
    # Handle state v3 format (resources at root level)
    resources = state.get("resources", [])
    
    # Handle state v4 format (resources in values.root_module)
    if not resources:
        values = state.get("values", {})
        if values:
            root_module = values.get("root_module", {})
            resources = root_module.get("resources", [])
    
    for resource in resources:
        resource_type = resource.get("type", "")
        instances = resource.get("instances", [])
        
        for instance in instances:
            attributes = instance.get("attributes", {})
            
            # Extract resource ID - try multiple fields
            # Different resource types use different ID fields
            resource_id = (
                attributes.get("id") or
                attributes.get("arn") or
                attributes.get("name") or
                attributes.get("resource_id") or
                attributes.get("instance_id") or
                attributes.get("db_instance_identifier") or
                attributes.get("bucket") or
                attributes.get("function_name") or
                attributes.get("role_name") or
                attributes.get("policy_arn")
            )
            
            if resource_id:
                managed_ids.add(str(resource_id))
            
            # Also add ARN if present (for resources that use ARNs)
            arn = attributes.get("arn")
            if arn and arn != resource_id:
                managed_ids.add(str(arn))
    
    logger.info("Extracted %d managed resource IDs from Terraform state", len(managed_ids))
    return managed_ids


def is_resource_managed(
    resource_id: str,
    arn: str | None,
    name: str | None,
    managed_ids: set[str],
) -> bool:
    """Check if a discovered resource is already managed.
    
    Args:
        resource_id: Cloud resource ID
        arn: Resource ARN (if available)
        name: Resource name (if available)
        managed_ids: Set of managed resource IDs from state
        
    Returns:
        True if resource is already managed
    """
    if resource_id in managed_ids:
        return True
    
    if arn and arn in managed_ids:
        return True
    
    if name and name in managed_ids:
        return True
    
    return False

