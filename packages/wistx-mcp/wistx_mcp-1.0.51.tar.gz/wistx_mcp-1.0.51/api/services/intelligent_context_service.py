"""Intelligent context service for multi-resource context storage with automatic analysis."""

import logging
import secrets
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.intelligent_context import (
    ContextAnalysis,
    ContextLink,
    ContextStatus,
    ContextType,
    CostContext,
    InfrastructureResource,
    IntelligentContext,
    SecurityContext,
)

logger = logging.getLogger(__name__)


def generate_context_id() -> str:
    """Generate unique context ID.

    Returns:
        Unique context ID (e.g., 'ctx_abc123')
    """
    random_part = secrets.token_urlsafe(8)[:8]
    return f"ctx_{random_part}"


def generate_link_id() -> str:
    """Generate unique link ID.

    Returns:
        Unique link ID (e.g., 'link_abc123')
    """
    random_part = secrets.token_urlsafe(8)[:8]
    return f"link_{random_part}"


class IntelligentContextService:
    """Service for intelligent context management with infrastructure awareness."""

    def __init__(self):
        """Initialize intelligent context service."""
        self._db = None

    def _get_db(self):
        """Get MongoDB database instance."""
        if self._db is None:
            self._db = mongodb_manager.get_database()
        return self._db

    async def save_context_with_analysis(
        self,
        user_id: str,
        context_type: ContextType,
        title: str,
        summary: str,
        description: Optional[str] = None,
        conversation_history: Optional[list[dict[str, Any]]] = None,
        code_snippets: Optional[list[dict[str, Any]]] = None,
        plans: Optional[list[dict[str, Any]]] = None,
        decisions: Optional[list[dict[str, Any]]] = None,
        infrastructure_resources: Optional[list[dict[str, Any]]] = None,
        linked_resources: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
        workspace: Optional[str] = None,
        organization_id: Optional[str] = None,
        auto_analyze: bool = True,
    ) -> IntelligentContext:
        """Save context with automatic infrastructure analysis.

        Args:
            user_id: User ID
            context_type: Type of context
            title: Context title
            summary: Context summary
            description: Detailed description
            conversation_history: Conversation history
            code_snippets: Code snippets
            plans: Plans or workflows
            decisions: Decisions made
            infrastructure_resources: Infrastructure resources referenced
            linked_resources: Linked resource IDs
            tags: Tags for categorization
            workspace: Workspace identifier
            organization_id: Organization ID
            auto_analyze: Automatically analyze infrastructure, compliance, costs, security

        Returns:
            Created IntelligentContext with analysis
        """
        context_id = generate_context_id()

        infrastructure_resources_list = []
        if infrastructure_resources:
            for resource in infrastructure_resources:
                infrastructure_resources_list.append(InfrastructureResource(**resource))

        context = IntelligentContext(
            context_id=context_id,
            user_id=user_id,
            organization_id=organization_id,
            context_type=context_type,
            status=ContextStatus.ACTIVE,
            title=title,
            summary=summary,
            description=description,
            conversation_history=conversation_history or [],
            code_snippets=code_snippets or [],
            plans=plans or [],
            decisions=decisions or [],
            infrastructure_resources=infrastructure_resources_list,
            linked_resources=linked_resources or [],
            tags=tags or [],
            workspace=workspace,
        )

        if auto_analyze:
            analysis = await self._perform_automatic_analysis(context)
            context.analysis = analysis

        db = self._get_db()
        collection = db.contexts
        context_dict = context.to_dict()
        collection.insert_one(context_dict)

        logger.info(
            "Created context with analysis: context_id=%s, type=%s, user_id=%s",
            context_id,
            context_type,
            user_id,
        )

        return context

    async def _perform_automatic_analysis(
        self, context: IntelligentContext
    ) -> ContextAnalysis:
        """Perform automatic analysis on context.

        Args:
            context: Context to analyze

        Returns:
            ContextAnalysis with all analysis results
        """
        compliance_analysis = None
        cost_analysis = None
        security_analysis = None
        infrastructure_analysis = None

        if context.infrastructure_resources:
            try:
                compliance_analysis = await self._analyze_compliance(context)
                cost_analysis = await self._analyze_costs(context)
                security_analysis = await self._analyze_security(context)
                infrastructure_analysis = await self._analyze_infrastructure(context)
            except Exception as e:
                logger.warning("Error during automatic analysis: %s", e, exc_info=True)

        return ContextAnalysis(
            compliance=compliance_analysis,
            costs=cost_analysis,
            security=security_analysis,
            infrastructure=infrastructure_analysis,
        )

    async def _analyze_compliance(
        self, context: IntelligentContext
    ) -> Optional[Any]:
        """Analyze compliance implications.

        Args:
            context: Context to analyze

        Returns:
            ComplianceContext or None
        """
        from api.models.intelligent_context import ComplianceContext

        standards = set()
        controls = []
        status = {}

        for resource in context.infrastructure_resources:
            try:
                from api.services.compliance_service import compliance_service

                resource_types = []
                if resource.resource_type == "terraform":
                    resource_types = ["aws_rds_instance", "aws_s3_bucket"]
                elif resource.resource_type == "kubernetes":
                    resource_types = ["kubernetes_deployment", "kubernetes_service"]

                if resource_types:
                    compliance_result = await compliance_service.get_compliance_requirements(
                        request={
                            "resource_types": resource_types,
                            "standards": [],
                        },
                    )

                    if compliance_result and compliance_result.get("controls"):
                        for control in compliance_result["controls"]:
                            standard = control.get("standard", "")
                            if standard:
                                standards.add(standard)
                            controls.append(control)
                            status[standard] = "compliant"

            except Exception as e:
                logger.debug("Error analyzing compliance for resource: %s", e)

        if standards:
            return ComplianceContext(
                standards=list(standards),
                controls=controls,
                status=status,
            )

        return None

    async def _analyze_costs(self, context: IntelligentContext) -> Optional[CostContext]:
        """Analyze cost implications.

        Args:
            context: Context to analyze

        Returns:
            CostContext or None
        """
        total_monthly = 0.0
        breakdown = {}

        for resource in context.infrastructure_resources:
            try:
                from api.services.pricing_service import pricing_service

                if resource.resource_type == "terraform":
                    cost_result = await pricing_service.calculate_cost(
                        resources=[
                            {
                                "cloud": "aws",
                                "service": "rds",
                                "instance_type": "db.t3.medium",
                                "quantity": 1,
                                "region": "us-east-1",
                            }
                        ],
                    )

                    if cost_result and cost_result.get("monthly_cost"):
                        monthly = cost_result["monthly_cost"]
                        total_monthly += monthly
                        breakdown[resource.name] = monthly

            except Exception as e:
                logger.debug("Error analyzing costs for resource: %s", e)

        if total_monthly > 0:
            return CostContext(
                estimated_monthly=total_monthly,
                estimated_annual=total_monthly * 12,
                breakdown=breakdown,
            )

        return None

    async def _analyze_security(
        self, context: IntelligentContext
    ) -> Optional[SecurityContext]:
        """Analyze security implications.

        Args:
            context: Context to analyze

        Returns:
            SecurityContext or None
        """
        issues = []
        vulnerabilities = []
        recommendations = []

        for resource in context.infrastructure_resources:
            if resource.changes:
                for change in resource.changes:
                    if "security" in str(change).lower() or "vulnerability" in str(change).lower():
                        issues.append({
                            "resource": resource.name,
                            "issue": str(change),
                            "severity": "medium",
                        })

        if issues:
            return SecurityContext(
                issues=issues,
                vulnerabilities=vulnerabilities,
                recommendations=recommendations,
                score=85.0,
            )

        return None

    async def _analyze_infrastructure(
        self, context: IntelligentContext
    ) -> Optional[dict[str, Any]]:
        """Analyze infrastructure implications.

        Args:
            context: Context to analyze

        Returns:
            Infrastructure analysis dictionary or None
        """
        resource_types = {}
        cloud_providers = set()

        for resource in context.infrastructure_resources:
            resource_types[resource.resource_type] = resource_types.get(resource.resource_type, 0) + 1
            if "aws" in resource.resource_type.lower():
                cloud_providers.add("aws")
            elif "gcp" in resource.resource_type.lower():
                cloud_providers.add("gcp")
            elif "azure" in resource.resource_type.lower():
                cloud_providers.add("azure")

        if resource_types:
            return {
                "resource_types": resource_types,
                "cloud_providers": list(cloud_providers),
                "total_resources": len(context.infrastructure_resources),
            }

        return None

    async def get_context(
        self, context_id: str, user_id: Optional[str] = None, organization_id: Optional[str] = None
    ) -> Optional[IntelligentContext]:
        """Get context by ID.

        Args:
            context_id: Context ID
            user_id: User ID (for access control)
            organization_id: Organization ID (for organization-shared context access)

        Returns:
            IntelligentContext if found, None otherwise
        """
        db = self._get_db()
        collection = db.contexts

        query = {"_id": context_id}
        if user_id:
            if organization_id:
                query["$or"] = [
                    {"user_id": ObjectId(user_id)},
                    {"organization_id": ObjectId(organization_id)},
                ]
            else:
                query["user_id"] = ObjectId(user_id)

        doc = collection.find_one(query)
        if not doc:
            return None

        context = IntelligentContext.from_dict(doc)

        collection.update_one(
            {"_id": context_id},
            {"$set": {"accessed_at": datetime.utcnow()}},
        )

        return context

    async def list_contexts(
        self,
        user_id: str,
        context_type: Optional[ContextType] = None,
        status: Optional[ContextStatus] = None,
        workspace: Optional[str] = None,
        tags: Optional[list[str]] = None,
        limit: int = 100,
        offset: int = 0,
        organization_id: Optional[str] = None,
        include_organization: bool = False,
    ) -> list[dict[str, Any]]:
        """List contexts with filtering.

        Args:
            user_id: User ID
            context_type: Filter by context type
            status: Filter by status
            workspace: Filter by workspace
            tags: Filter by tags
            limit: Maximum number of results
            offset: Offset for pagination
            organization_id: Organization ID (if filtering by organization)
            include_organization: If True, include organization-shared contexts

        Returns:
            List of context dictionaries
        """
        db = self._get_db()
        collection = db.contexts

        if include_organization and organization_id:
            query: dict[str, Any] = {
                "$or": [
                    {"user_id": ObjectId(user_id)},
                    {"organization_id": ObjectId(organization_id), "status": {"$ne": ContextStatus.DELETED.value}},
                ]
            }
        else:
            query: dict[str, Any] = {"user_id": ObjectId(user_id)}

        if context_type:
            query["context_type"] = context_type.value
        if status:
            query["status"] = status.value
        if workspace:
            query["workspace"] = workspace
        if tags:
            query["tags"] = {"$in": tags}

        cursor = collection.find(query).sort("created_at", -1).skip(offset).limit(limit)

        contexts = []
        for doc in cursor:
            context = IntelligentContext.from_dict(doc)
            contexts.append(context.model_dump())

        return contexts

    async def search_contexts_intelligently(
        self,
        user_id: str,
        query: str,
        context_type: Optional[ContextType] = None,
        compliance_standard: Optional[str] = None,
        cost_range: Optional[dict[str, float]] = None,
        security_score_min: Optional[float] = None,
        limit: int = 50,
        organization_id: Optional[str] = None,
        include_organization: bool = False,
    ) -> list[dict[str, Any]]:
        """Intelligent context search with infrastructure awareness.

        Args:
            user_id: User ID
            query: Search query
            context_type: Filter by context type
            compliance_standard: Filter by compliance standard
            cost_range: Filter by cost range (min, max)
            security_score_min: Minimum security score
            limit: Maximum number of results
            organization_id: Organization ID (if filtering by organization)
            include_organization: If True, include organization-shared contexts

        Returns:
            List of matching contexts
        """
        db = self._get_db()
        collection = db.contexts

        if include_organization and organization_id:
            search_query: dict[str, Any] = {
                "$and": [
                    {
                        "$or": [
                            {"user_id": ObjectId(user_id)},
                            {"organization_id": ObjectId(organization_id)},
                        ]
                    },
                    {
                        "$or": [
                            {"title": {"$regex": query, "$options": "i"}},
                            {"summary": {"$regex": query, "$options": "i"}},
                            {"description": {"$regex": query, "$options": "i"}},
                        ]
                    },
                ],
                "status": {"$ne": ContextStatus.DELETED.value},
            }
        else:
            search_query: dict[str, Any] = {
                "user_id": ObjectId(user_id),
                "status": {"$ne": ContextStatus.DELETED.value},
                "$or": [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"summary": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                ],
            }

        if context_type:
            search_query["context_type"] = context_type.value

        if compliance_standard:
            search_query["analysis.compliance.standards"] = compliance_standard

        if cost_range:
            min_cost = cost_range.get("min", 0.0)
            max_cost = cost_range.get("max", float("inf"))
            search_query["analysis.costs.estimated_monthly"] = {
                "$gte": min_cost,
                "$lte": max_cost,
            }

        if security_score_min is not None:
            search_query["analysis.security.score"] = {"$gte": security_score_min}

        cursor = collection.find(search_query).sort("created_at", -1).limit(limit)

        results = []
        for doc in cursor:
            context = IntelligentContext.from_dict(doc)
            results.append(context.model_dump())

        return results

    async def link_contexts(
        self,
        source_context_id: str,
        target_context_id: str,
        relationship_type: str,
        strength: float = 1.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> ContextLink:
        """Link contexts with semantic relationship.

        Args:
            source_context_id: Source context ID
            target_context_id: Target context ID
            relationship_type: Relationship type (depends_on, related_to, etc.)
            strength: Relationship strength (0.0-1.0)
            metadata: Additional metadata

        Returns:
            Created ContextLink
        """
        link_id = generate_link_id()

        link = ContextLink(
            link_id=link_id,
            source_context_id=source_context_id,
            target_context_id=target_context_id,
            relationship_type=relationship_type,
            strength=strength,
            metadata=metadata or {},
        )

        db = self._get_db()
        collection = db.context_links
        link_dict = link.to_dict()
        collection.insert_one(link_dict)

        contexts_collection = db.contexts
        contexts_collection.update_one(
            {"_id": source_context_id},
            {"$addToSet": {"linked_contexts": target_context_id}},
        )
        contexts_collection.update_one(
            {"_id": target_context_id},
            {"$addToSet": {"linked_contexts": source_context_id}},
        )

        logger.info(
            "Linked contexts: source=%s, target=%s, type=%s",
            source_context_id,
            target_context_id,
            relationship_type,
        )

        return link

    async def get_context_graph(
        self,
        context_id: str,
        depth: int = 2,
        user_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get context dependency graph.

        Args:
            context_id: Root context ID
            depth: Maximum depth to traverse
            user_id: User ID (for access control)

        Returns:
            Graph structure dictionary
        """
        db = self._get_db()
        contexts_collection = db.contexts
        links_collection = db.context_links

        visited = set()
        graph: dict[str, Any] = {
            "root_context_id": context_id,
            "nodes": [],
            "edges": [],
        }

        def traverse(context_id: str, current_depth: int) -> None:
            """Recursively traverse context graph."""
            if current_depth > depth or context_id in visited:
                return

            visited.add(context_id)

            context_doc = contexts_collection.find_one({"_id": context_id})
            if not context_doc:
                return

            if user_id and context_doc.get("user_id") != ObjectId(user_id):
                return

            context = IntelligentContext.from_dict(context_doc)
            graph["nodes"].append({
                "context_id": context_id,
                "title": context.title,
                "type": context.context_type.value,
            })

            links = links_collection.find({
                "$or": [
                    {"source_context_id": context_id},
                    {"target_context_id": context_id},
                ],
            })

            for link_doc in links:
                link = ContextLink.from_dict(link_doc)
                other_id = (
                    link.target_context_id
                    if link.source_context_id == context_id
                    else link.source_context_id
                )

                if other_id not in visited:
                    graph["edges"].append({
                        "source": context_id,
                        "target": other_id,
                        "relationship": link.relationship_type,
                        "strength": link.strength,
                    })
                    traverse(other_id, current_depth + 1)

        traverse(context_id, 0)

        return graph

    async def update_context(
        self,
        context_id: str,
        user_id: str,
        updates: dict[str, Any],
    ) -> Optional[IntelligentContext]:
        """Update context.

        Args:
            context_id: Context ID
            user_id: User ID (for access control)
            updates: Updates to apply

        Returns:
            Updated IntelligentContext if found, None otherwise
        """
        db = self._get_db()
        collection = db.contexts

        updates["updated_at"] = datetime.utcnow()

        result = collection.update_one(
            {"_id": context_id, "user_id": ObjectId(user_id)},
            {"$set": updates},
        )

        if result.modified_count > 0:
            return await self.get_context(context_id, user_id)

        return None

    async def delete_context(
        self, context_id: str, user_id: str
    ) -> bool:
        """Delete context (soft delete).

        Args:
            context_id: Context ID
            user_id: User ID (for access control)

        Returns:
            True if deleted, False if not found
        """
        db = self._get_db()
        collection = db.contexts

        result = collection.update_one(
            {"_id": context_id, "user_id": ObjectId(user_id)},
            {"$set": {"status": ContextStatus.DELETED.value}},
        )

        return result.modified_count > 0

    async def share_context_with_organization(
        self,
        context_id: str,
        user_id: str,
        organization_id: str,
    ) -> Optional[IntelligentContext]:
        """Share context with organization.

        Args:
            context_id: Context ID
            user_id: User ID (must be owner of context)
            organization_id: Organization ID to share with

        Returns:
            Updated IntelligentContext if found, None otherwise
        """
        db = self._get_db()
        collection = db.contexts

        context_doc = collection.find_one({"_id": context_id, "user_id": ObjectId(user_id)})
        if not context_doc:
            return None

        result = collection.update_one(
            {"_id": context_id},
            {"$set": {"organization_id": ObjectId(organization_id), "updated_at": datetime.utcnow()}},
        )

        if result.modified_count > 0:
            return await self.get_context(context_id, user_id, organization_id)

        return None

    async def unshare_context_from_organization(
        self,
        context_id: str,
        user_id: str,
    ) -> Optional[IntelligentContext]:
        """Unshare context from organization (make it private).

        Args:
            context_id: Context ID
            user_id: User ID (must be owner of context)

        Returns:
            Updated IntelligentContext if found, None otherwise
        """
        db = self._get_db()
        collection = db.contexts

        result = collection.update_one(
            {"_id": context_id, "user_id": ObjectId(user_id)},
            {"$unset": {"organization_id": ""}, "$set": {"updated_at": datetime.utcnow()}},
        )

        if result.modified_count > 0:
            return await self.get_context(context_id, user_id)

        return None


intelligent_context_service = IntelligentContextService()

