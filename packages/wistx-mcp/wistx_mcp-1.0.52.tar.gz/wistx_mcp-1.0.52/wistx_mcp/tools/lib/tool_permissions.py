"""Tool permission matrix for authorization enforcement."""

from typing import Any

TOOL_PERMISSIONS: dict[str, dict[str, Any]] = {
    "wistx_get_compliance_requirements": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_calculate_infrastructure_cost": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_research_knowledge_base": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_get_devops_infra_code_examples": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_index_repository": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_index_resource": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_list_resources": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_check_resource_status": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_delete_resource": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_search_codebase": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_regex_search": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_web_search": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_design_architecture": {
        "required_plan": "team",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_troubleshoot_issue": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_generate_documentation": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_manage_integration": {
        "required_plan": "team",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_manage_infrastructure": {
        "required_plan": "team",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_get_github_file_tree": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_visualize_infra_flow": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_get_infrastructure_context": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_search_packages": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_resolve_incident": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": True,
    },
    "wistx_get_recommended_tools": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": False,
    },
    "wistx_list_tools_by_category": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": False,
    },
    "wistx_get_tool_documentation": {
        "required_plan": "professional",
        "required_permission": None,
        "quota_required": False,
    },
}

def get_plan_hierarchy() -> dict[str, int]:
    """Get plan hierarchy from plan service.
    
    Returns:
        Dictionary mapping plan IDs to hierarchy levels
    """
    try:
        from api.services.plan_service import plan_service
        
        plan_order = ["professional", "team", "enterprise"]
        plans = plan_service.list_plans()
        hierarchy = {}
        
        for plan in plans:
            plan_id = plan.plan_id
            if plan_id in plan_order:
                hierarchy[plan_id] = plan_order.index(plan_id) + 1
            else:
                hierarchy[plan_id] = 999
        
        if not hierarchy:
            return {"professional": 1, "team": 2, "enterprise": 3}
        
        return hierarchy
    except (ImportError, AttributeError):
        return {"professional": 1, "team": 2, "enterprise": 3}


PLAN_HIERARCHY = get_plan_hierarchy()


def get_default_plan() -> str:
    """Get default plan ID from plan service.
    
    Returns:
        Default plan ID (usually "professional")
    """
    try:
        from api.services.plan_service import plan_service
        
        plans = plan_service.list_plans()
        if plans:
            professional_plan = plan_service.get_plan("professional")
            if professional_plan:
                return "professional"
            return plans[0].plan_id
        return "professional"
    except (ImportError, AttributeError):
        return "professional"


def get_tool_permissions(tool_name: str) -> dict[str, Any]:
    """Get permission requirements for a tool.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Dictionary with required_plan, required_permission, quota_required
    """
    default_plan = get_default_plan()
    return TOOL_PERMISSIONS.get(tool_name, {
        "required_plan": default_plan,
        "required_permission": None,
        "quota_required": True,
    })


def check_plan_access(user_plan: str, required_plan: str) -> bool:
    """Check if user plan meets minimum requirement.
    
    Args:
        user_plan: User's current plan
        required_plan: Minimum required plan
    
    Returns:
        True if user plan meets requirement
    """
    hierarchy = get_plan_hierarchy()
    user_level = hierarchy.get(user_plan, 0)
    required_level = hierarchy.get(required_plan, 999)
    return user_level >= required_level


def check_tool_permission(
    user_info: dict[str, Any],
    required_permission: str,
) -> bool:
    """Check if user has required permission for a tool.
    
    Uses same logic as API (api/auth/rbac.py:has_permission()):
    - Super admins: Always allowed (bypass all checks)
    - Admin users: Check admin_permissions (with wildcard "*" support)
    - Regular users: Check plan features for indexing permission
    
    Args:
        user_info: User information dictionary (from auth_ctx.user_info)
        required_permission: Required permission name (e.g., "indexing")
    
    Returns:
        True if user has permission, False otherwise
    """
    if not required_permission:
        return True
    
    is_super_admin = user_info.get("is_super_admin", False)
    if is_super_admin:
        return True
    
    admin_permissions = user_info.get("admin_permissions", [])
    if "*" in admin_permissions:
        return True
    
    if required_permission in admin_permissions:
        return True
    
    if required_permission == "indexing":
        plan = user_info.get("plan", get_default_plan())
        try:
            from api.services.plan_service import plan_service
            
            plan_features = plan_service.get_plan_features(plan)
            if plan_features:
                return plan_features.repository_indexing or plan_features.document_indexing
            else:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning("Plan features not found for plan: %s", plan)
        except (ImportError, AttributeError) as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Failed to check plan features for indexing permission: %s", e, exc_info=True)
    
    return False

