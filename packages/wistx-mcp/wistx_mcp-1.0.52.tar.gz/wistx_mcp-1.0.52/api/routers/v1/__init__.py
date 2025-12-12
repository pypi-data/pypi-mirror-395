"""V1 API routers."""

from fastapi import APIRouter

from api.routers.v1 import auth, alerts, architecture, audit_logs, billing, budget, cache, cloud_discovery, code_examples, compliance, compliance_custom, contexts, cost_search, csrf, document_updates, evaluation, filesystem, health, infrastructure, indexing, knowledge, metrics, notifications, oauth, organizations, pricing, reports, research_sessions, search, troubleshoot, usage, users, versioning, websocket
from api.routers.v1.admin import (
    users as admin_users,
    activity as admin_activity,
    analytics as admin_analytics,
    security as admin_security,
    system as admin_system,
    invitations as admin_invitations,
    admins as admin_admins,
    pipelines as admin_pipelines,
)

router = APIRouter()

router.include_router(health.router)
router.include_router(csrf.router)
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(billing.router)
router.include_router(budget.router)
router.include_router(alerts.router)
router.include_router(usage.router)
router.include_router(compliance.router)
router.include_router(compliance_custom.router)
router.include_router(cost_search.router)
router.include_router(pricing.router)
router.include_router(code_examples.router)
router.include_router(knowledge.router)
router.include_router(research_sessions.router)
router.include_router(evaluation.router)
router.include_router(indexing.router)
router.include_router(filesystem.router)
router.include_router(contexts.router)
router.include_router(cache.router)
router.include_router(document_updates.router)
router.include_router(reports.router)
router.include_router(metrics.router)
router.include_router(search.router)
router.include_router(troubleshoot.router)
router.include_router(architecture.router)
router.include_router(infrastructure.router)
router.include_router(cloud_discovery.router)
router.include_router(versioning.router)
router.include_router(audit_logs.router)
router.include_router(notifications.router)
router.include_router(oauth.router, prefix="/oauth", tags=["oauth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(organizations.router)
router.include_router(admin_users.router, prefix="/admin", tags=["admin"])
router.include_router(admin_activity.router, prefix="/admin", tags=["admin"])
router.include_router(admin_analytics.router, prefix="/admin", tags=["admin"])
router.include_router(admin_security.router, prefix="/admin", tags=["admin"])
router.include_router(admin_system.router, prefix="/admin", tags=["admin"])
router.include_router(admin_invitations.router, prefix="/admin", tags=["admin"])
router.include_router(admin_admins.router, prefix="/admin", tags=["admin"])
router.include_router(admin_pipelines.router, prefix="/admin", tags=["admin"])
router.include_router(websocket.router, tags=["websocket"])

