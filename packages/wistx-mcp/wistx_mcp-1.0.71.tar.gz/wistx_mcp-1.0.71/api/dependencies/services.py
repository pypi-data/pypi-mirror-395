"""Service dependency providers for FastAPI dependency injection.

This module provides dependency injection for services, following industry best practices.
Services are injected via FastAPI's Depends() system rather than using global singletons.
"""

import logging
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from api.database.mongodb import get_database, mongodb_manager
from api.services.alerting_service import AlertingService
from api.services.user_invitation_service import UserInvitationService
from api.services.retrieval_evaluation_service import RetrievalEvaluationService
from api.services.hybrid_retrieval_service import HybridRetrievalService
from api.services.research_orchestrator import ResearchOrchestrator
from api.services.quota_service import QuotaService
from api.services.indexing_service import IndexingService
from api.services.billing_service import BillingService
from api.services.plan_service import PlanService
from api.services.organization_service import OrganizationService
from api.services.knowledge_service import KnowledgeService
from api.services.search_service import SearchService
from api.services.compliance_service import ComplianceService
from api.services.pricing_service import PricingService
from api.services.code_examples_service import CodeExamplesService
from api.services.architecture_service import ArchitectureService
from api.services.infrastructure_service import InfrastructureService
from api.services.custom_compliance_service import CustomComplianceService
from api.services.audit_log_service import AuditLogService
from api.services.alert_service import AlertService
from api.services.status_service import StatusService
from api.services.oauth_service import OAuthService
from api.services.github_service import GitHubService
from api.services.user_profile_service import UserProfileService
from api.services.budget_service import BudgetService
from api.services.virtual_filesystem_service import VirtualFilesystemService
from api.services.predictive_cache_service import PredictiveCacheService
from api.services.intelligent_context_service import IntelligentContextService
from api.services.organization_analytics_service import OrganizationAnalyticsService
from api.services.pipeline_execution_service import PipelineExecutionService
from api.services.version_tracking_service import VersionTrackingService
from api.services.agent_metrics import AgentMetricsService
from api.services.cloud_discovery_service import CloudDiscoveryService
from api.services.setup_script_service import SetupScriptService
from api.services.mcp_http_service import MCPHTTPService

logger = logging.getLogger(__name__)


@lru_cache()
def get_alerting_service() -> AlertingService:
    """Get alerting service instance (singleton via lru_cache).
    
    Returns:
        AlertingService instance
    """
    return AlertingService()


@lru_cache()
def get_user_invitation_service() -> UserInvitationService:
    """Get user invitation service instance (singleton via lru_cache).
    
    Returns:
        UserInvitationService instance
    """
    return UserInvitationService()


@lru_cache()
def get_retrieval_evaluation_service() -> RetrievalEvaluationService:
    """Get retrieval evaluation service instance (singleton via lru_cache).
    
    Returns:
        RetrievalEvaluationService instance
    """
    return RetrievalEvaluationService()


@lru_cache()
def get_hybrid_retrieval_service() -> HybridRetrievalService:
    """Get hybrid retrieval service instance (singleton via lru_cache).
    
    Returns:
        HybridRetrievalService instance
    """
    return HybridRetrievalService()


@lru_cache()
def get_research_orchestrator() -> ResearchOrchestrator:
    """Get research orchestrator instance (singleton via lru_cache).
    
    Returns:
        ResearchOrchestrator instance
    """
    return ResearchOrchestrator()


@lru_cache()
def get_quota_service() -> QuotaService:
    """Get quota service instance (singleton via lru_cache)."""
    return QuotaService()


@lru_cache()
def get_indexing_service() -> IndexingService:
    """Get indexing service instance (singleton via lru_cache)."""
    return IndexingService()


@lru_cache()
def get_billing_service() -> BillingService:
    """Get billing service instance (singleton via lru_cache)."""
    return BillingService()


@lru_cache()
def get_plan_service() -> PlanService:
    """Get plan service instance (singleton via lru_cache)."""
    return PlanService()


@lru_cache()
def get_organization_service() -> OrganizationService:
    """Get organization service instance (singleton via lru_cache)."""
    return OrganizationService()


@lru_cache()
def get_knowledge_service() -> KnowledgeService:
    """Get knowledge service instance (singleton via lru_cache)."""
    return KnowledgeService()


@lru_cache()
def get_search_service() -> SearchService:
    """Get search service instance (singleton via lru_cache)."""
    return SearchService()


@lru_cache()
def get_compliance_service() -> ComplianceService:
    """Get compliance service instance (singleton via lru_cache)."""
    return ComplianceService()


@lru_cache()
def get_pricing_service() -> PricingService:
    """Get pricing service instance (singleton via lru_cache)."""
    return PricingService()


@lru_cache()
def get_code_examples_service() -> CodeExamplesService:
    """Get code examples service instance (singleton via lru_cache)."""
    return CodeExamplesService()


@lru_cache()
def get_architecture_service() -> ArchitectureService:
    """Get architecture service instance (singleton via lru_cache)."""
    return ArchitectureService()


@lru_cache()
def get_infrastructure_service() -> InfrastructureService:
    """Get infrastructure service instance (singleton via lru_cache)."""
    return InfrastructureService()


@lru_cache()
def get_custom_compliance_service() -> CustomComplianceService:
    """Get custom compliance service instance (singleton via lru_cache)."""
    return CustomComplianceService()


@lru_cache()
def get_audit_log_service() -> AuditLogService:
    """Get audit log service instance (singleton via lru_cache)."""
    return AuditLogService()


@lru_cache()
def get_alert_service() -> AlertService:
    """Get alert service instance (singleton via lru_cache)."""
    return AlertService()


@lru_cache()
def get_status_service() -> StatusService:
    """Get status service instance (singleton via lru_cache)."""
    return StatusService()


@lru_cache()
def get_oauth_service() -> OAuthService:
    """Get OAuth service instance (singleton via lru_cache)."""
    return OAuthService()


@lru_cache()
def get_github_service() -> GitHubService:
    """Get GitHub service instance (singleton via lru_cache)."""
    return GitHubService()


@lru_cache()
def get_user_profile_service() -> UserProfileService:
    """Get user profile service instance (singleton via lru_cache)."""
    return UserProfileService()


@lru_cache()
def get_budget_service() -> BudgetService:
    """Get budget service instance (singleton via lru_cache)."""
    return BudgetService()


@lru_cache()
def get_virtual_filesystem_service() -> VirtualFilesystemService:
    """Get virtual filesystem service instance (singleton via lru_cache)."""
    return VirtualFilesystemService()


@lru_cache()
def get_predictive_cache_service() -> PredictiveCacheService:
    """Get predictive cache service instance (singleton via lru_cache)."""
    return PredictiveCacheService()


@lru_cache()
def get_intelligent_context_service() -> IntelligentContextService:
    """Get intelligent context service instance (singleton via lru_cache)."""
    return IntelligentContextService()


@lru_cache()
def get_organization_analytics_service() -> OrganizationAnalyticsService:
    """Get organization analytics service instance (singleton via lru_cache)."""
    return OrganizationAnalyticsService()


@lru_cache()
def get_pipeline_execution_service() -> PipelineExecutionService:
    """Get pipeline execution service instance (singleton via lru_cache)."""
    return PipelineExecutionService()


@lru_cache()
def get_version_tracking_service() -> VersionTrackingService:
    """Get version tracking service instance (singleton via lru_cache)."""
    return VersionTrackingService()


@lru_cache()
def get_agent_metrics_service() -> AgentMetricsService:
    """Get agent metrics service instance (singleton via lru_cache)."""
    return AgentMetricsService()


@lru_cache()
def get_cloud_discovery_service() -> CloudDiscoveryService:
    """Get cloud discovery service instance (singleton via lru_cache)."""
    return CloudDiscoveryService()


@lru_cache()
def get_setup_script_service() -> SetupScriptService:
    """Get setup script service instance (singleton via lru_cache)."""
    return SetupScriptService()


@lru_cache()
def get_mcp_http_service() -> MCPHTTPService:
    """Get MCP HTTP service instance (singleton via lru_cache)."""
    return MCPHTTPService()


# Type aliases for cleaner route signatures
AlertingServiceDep = Annotated[AlertingService, Depends(get_alerting_service)]
UserInvitationServiceDep = Annotated[UserInvitationService, Depends(get_user_invitation_service)]
RetrievalEvaluationServiceDep = Annotated[RetrievalEvaluationService, Depends(get_retrieval_evaluation_service)]
HybridRetrievalServiceDep = Annotated[HybridRetrievalService, Depends(get_hybrid_retrieval_service)]
ResearchOrchestratorDep = Annotated[ResearchOrchestrator, Depends(get_research_orchestrator)]
QuotaServiceDep = Annotated[QuotaService, Depends(get_quota_service)]
IndexingServiceDep = Annotated[IndexingService, Depends(get_indexing_service)]
BillingServiceDep = Annotated[BillingService, Depends(get_billing_service)]
PlanServiceDep = Annotated[PlanService, Depends(get_plan_service)]
OrganizationServiceDep = Annotated[OrganizationService, Depends(get_organization_service)]
KnowledgeServiceDep = Annotated[KnowledgeService, Depends(get_knowledge_service)]
SearchServiceDep = Annotated[SearchService, Depends(get_search_service)]
ComplianceServiceDep = Annotated[ComplianceService, Depends(get_compliance_service)]
PricingServiceDep = Annotated[PricingService, Depends(get_pricing_service)]
CodeExamplesServiceDep = Annotated[CodeExamplesService, Depends(get_code_examples_service)]
ArchitectureServiceDep = Annotated[ArchitectureService, Depends(get_architecture_service)]
InfrastructureServiceDep = Annotated[InfrastructureService, Depends(get_infrastructure_service)]
CustomComplianceServiceDep = Annotated[CustomComplianceService, Depends(get_custom_compliance_service)]
AuditLogServiceDep = Annotated[AuditLogService, Depends(get_audit_log_service)]
AlertServiceDep = Annotated[AlertService, Depends(get_alert_service)]
StatusServiceDep = Annotated[StatusService, Depends(get_status_service)]
OAuthServiceDep = Annotated[OAuthService, Depends(get_oauth_service)]
GitHubServiceDep = Annotated[GitHubService, Depends(get_github_service)]
UserProfileServiceDep = Annotated[UserProfileService, Depends(get_user_profile_service)]
BudgetServiceDep = Annotated[BudgetService, Depends(get_budget_service)]
VirtualFilesystemServiceDep = Annotated[VirtualFilesystemService, Depends(get_virtual_filesystem_service)]
PredictiveCacheServiceDep = Annotated[PredictiveCacheService, Depends(get_predictive_cache_service)]
IntelligentContextServiceDep = Annotated[IntelligentContextService, Depends(get_intelligent_context_service)]
OrganizationAnalyticsServiceDep = Annotated[OrganizationAnalyticsService, Depends(get_organization_analytics_service)]
PipelineExecutionServiceDep = Annotated[PipelineExecutionService, Depends(get_pipeline_execution_service)]
VersionTrackingServiceDep = Annotated[VersionTrackingService, Depends(get_version_tracking_service)]
AgentMetricsServiceDep = Annotated[AgentMetricsService, Depends(get_agent_metrics_service)]
CloudDiscoveryServiceDep = Annotated[CloudDiscoveryService, Depends(get_cloud_discovery_service)]
SetupScriptServiceDep = Annotated[SetupScriptService, Depends(get_setup_script_service)]
MCPHTTPServiceDep = Annotated[MCPHTTPService, Depends(get_mcp_http_service)]

