"""Budget service for infrastructure budget management."""

import logging
from datetime import datetime
from typing import Any, Optional

from bson import ObjectId

from api.database.mongodb import mongodb_manager
from api.models.budget import (
    BudgetScope,
    BudgetScopeType,
    BudgetStatus,
    EnforcementMode,
    InfrastructureBudget,
    generate_budget_id,
    get_month_period,
)
from api.models.spending import InfrastructureSpending, generate_spending_id
from api.models.budget_status import BudgetStatusAggregate
from api.exceptions import ValidationError, NotFoundError, DatabaseError

logger = logging.getLogger(__name__)


class BudgetService:
    """Service for managing infrastructure budgets."""

    async def create_budget(
        self,
        user_id: str,
        name: str,
        scope: dict[str, Any],
        monthly_limit_usd: float,
        alert_threshold_percent: float = 80.0,
        critical_threshold_percent: float = 95.0,
        organization_id: Optional[str] = None,
        description: Optional[str] = None,
        enforcement_mode: EnforcementMode = EnforcementMode.ALERT,
    ) -> InfrastructureBudget:
        """Create a new infrastructure budget.

        Args:
            user_id: User ID
            name: Budget name
            scope: Budget scope dictionary
            monthly_limit_usd: Monthly budget limit
            alert_threshold_percent: Alert threshold percentage
            critical_threshold_percent: Critical threshold percentage
            organization_id: Organization ID (optional)
            description: Budget description (optional)
            enforcement_mode: Enforcement mode (default: alert)

        Returns:
            Created InfrastructureBudget

        Raises:
            ValueError: If scope validation fails
        """
        budget_id = generate_budget_id()
        period_start, period_end = get_month_period()

        scope_obj = BudgetScopeType(scope["type"])
        
        if scope_obj == BudgetScopeType.CLOUD_PROVIDER:
            if not scope.get("cloud_provider") and not scope.get("environment_name"):
                raise ValidationError(
                    message="cloud_provider is required for cloud_provider scope",
                    user_message="Cloud provider is required for cloud provider budget scope (unless environment name is also set)",
                    error_code="MISSING_CLOUD_PROVIDER",
                    details={"scope_type": scope_obj, "scope": scope}
                )
        
        if scope_obj == BudgetScopeType.ENVIRONMENT:
            if not scope.get("environment_name") and not scope.get("cloud_provider"):
                raise ValidationError(
                    message="environment_name is required for environment scope",
                    user_message="Environment name is required for environment budget scope (unless cloud provider is also set)",
                    error_code="MISSING_ENVIRONMENT_NAME",
                    details={"scope_type": scope_obj, "scope": scope}
                )

        budget_scope = BudgetScope(**scope)

        budget = InfrastructureBudget(
            budget_id=budget_id,
            user_id=user_id,
            organization_id=organization_id,
            name=name,
            description=description,
            scope=budget_scope,
            monthly_limit_usd=monthly_limit_usd,
            alert_threshold_percent=alert_threshold_percent,
            critical_threshold_percent=critical_threshold_percent,
            current_period_start=period_start,
            current_period_end=period_end,
            enforcement_mode=enforcement_mode,
            created_by=user_id,
        )

        db = mongodb_manager.get_database()
        collection = db.infrastructure_budgets

        budget_dict = budget.to_dict()
        collection.insert_one(budget_dict)

        await self._initialize_budget_status(budget_id, period_start)

        logger.info(
            "Created budget: %s (user: %s, type: %s, limit: $%.2f/month)",
            budget_id,
            user_id,
            scope["type"],
            monthly_limit_usd,
        )

        return budget

    async def _initialize_budget_status(
        self,
        budget_id: str,
        period_start: datetime,
    ) -> None:
        """Initialize budget status cache for new budget.

        Args:
            budget_id: Budget ID
            period_start: Period start date
        """
        period_str = period_start.strftime("%Y-%m")
        
        db = mongodb_manager.get_database()
        collection = db.budget_status

        budget = await self.get_budget(budget_id)
        if not budget:
            return

        status = BudgetStatusAggregate(
            budget_id=budget_id,
            period=period_str,
            total_spent_usd=0.0,
            budget_limit_usd=budget.monthly_limit_usd,
            remaining_usd=budget.monthly_limit_usd,
            utilization_percent=0.0,
            status="on_track",
        )

        collection.insert_one(status.to_dict())

    async def get_budget(
        self,
        budget_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[InfrastructureBudget]:
        """Get budget by ID.

        Args:
            budget_id: Budget ID
            user_id: User ID (for access control)

        Returns:
            InfrastructureBudget or None if not found
        """
        db = mongodb_manager.get_database()
        collection = db.infrastructure_budgets

        query = {"_id": budget_id}
        if user_id:
            query["user_id"] = ObjectId(user_id)

        doc = collection.find_one(query)
        if not doc:
            return None

        return InfrastructureBudget.from_dict(doc)

    async def get_budgets(
        self,
        user_id: str,
        organization_id: Optional[str] = None,
        scope_type: Optional[BudgetScopeType] = None,
        status: Optional[BudgetStatus] = None,
    ) -> list[InfrastructureBudget]:
        """Get budgets for user/org.

        Args:
            user_id: User ID
            organization_id: Organization ID (optional filter)
            scope_type: Scope type filter (optional)
            status: Status filter (optional)

        Returns:
            List of InfrastructureBudget
        """
        db = mongodb_manager.get_database()
        collection = db.infrastructure_budgets

        query: dict[str, Any] = {"user_id": ObjectId(user_id)}
        
        if organization_id:
            query["organization_id"] = ObjectId(organization_id)
        elif organization_id is None:
            query["$or"] = [
                {"organization_id": None},
                {"organization_id": {"$exists": False}},
            ]
        
        if scope_type:
            query["scope.type"] = scope_type.value
        
        if status:
            query["status"] = status.value

        budgets = []
        for doc in collection.find(query).sort("created_at", -1):
            budgets.append(InfrastructureBudget.from_dict(doc))

        return budgets

    async def update_budget(
        self,
        budget_id: str,
        user_id: str,
        updates: dict[str, Any],
    ) -> InfrastructureBudget:
        """Update budget.

        Args:
            budget_id: Budget ID
            user_id: User ID (for access control)
            updates: Dictionary of fields to update

        Returns:
            Updated InfrastructureBudget

        Raises:
            ValueError: If budget not found or access denied
        """
        budget = await self.get_budget(budget_id, user_id)
        if not budget:
            raise NotFoundError(
                message=f"Budget not found: {budget_id}",
                user_message="Budget not found",
                error_code="BUDGET_NOT_FOUND",
                details={"budget_id": budget_id, "user_id": user_id}
            )

        updates["updated_at"] = datetime.utcnow()

        db = mongodb_manager.get_database()
        collection = db.infrastructure_budgets

        collection.update_one(
            {"_id": budget_id},
            {"$set": updates},
        )

        updated_budget = await self.get_budget(budget_id, user_id)
        if not updated_budget:
            raise DatabaseError(
                message="Failed to retrieve updated budget",
                user_message="Failed to retrieve updated budget. Please try again later.",
                error_code="BUDGET_RETRIEVAL_ERROR",
                details={"budget_id": budget_id, "user_id": user_id}
            )

        logger.info("Updated budget: %s", budget_id)

        return updated_budget

    async def delete_budget(
        self,
        budget_id: str,
        user_id: str,
    ) -> None:
        """Delete budget.

        Args:
            budget_id: Budget ID
            user_id: User ID (for access control)

        Raises:
            ValueError: If budget not found or access denied
        """
        budget = await self.get_budget(budget_id, user_id)
        if not budget:
            raise NotFoundError(
                message=f"Budget not found: {budget_id}",
                user_message="Budget not found",
                error_code="BUDGET_NOT_FOUND",
                details={"budget_id": budget_id, "user_id": user_id}
            )

        db = mongodb_manager.get_database()
        budgets_collection = db.infrastructure_budgets
        status_collection = db.budget_status

        budgets_collection.delete_one({"_id": budget_id})
        status_collection.delete_many({"budget_id": budget_id})

        logger.info("Deleted budget: %s", budget_id)

    async def check_budgets(
        self,
        user_id: str,
        estimated_cost: float,
        scope: dict[str, Any],
    ) -> dict[str, Any]:
        """Check budgets against estimated cost (INTERNAL METHOD).

        This is an internal service method, not exposed as MCP tool.

        Args:
            user_id: User ID
            estimated_cost: Estimated cost for infrastructure
            scope: Scope dictionary with cloud_providers, environment_id

        Returns:
            Dictionary with budget status and alerts
        """
        applicable_budgets = await self._find_applicable_budgets(user_id, scope)
        
        if not applicable_budgets:
            return {
                "status": "no_budgets",
                "applicable_budgets": [],
                "alerts": [],
            }

        budget_statuses = []
        worst_status = "on_track"
        alerts = []

        for budget in applicable_budgets:
            status = await self.get_budget_status(budget.budget_id)
            
            if not status:
                continue

            projected_spending = status.total_spent_usd + estimated_cost
            utilization = (projected_spending / budget.monthly_limit_usd) * 100

            budget_status = {
                "budget_id": budget.budget_id,
                "name": budget.name,
                "status": self._calculate_status(utilization, budget),
                "enforcement_mode": budget.enforcement_mode.value,
                "current_spending": status.total_spent_usd,
                "estimated_cost": estimated_cost,
                "projected_spending": projected_spending,
                "budget_limit": budget.monthly_limit_usd,
                "utilization_percent": utilization,
                "remaining": budget.monthly_limit_usd - projected_spending,
            }

            budget_statuses.append(budget_status)

            status_priority = {"on_track": 0, "warning": 1, "critical": 2, "exceeded": 3}
            if status_priority.get(budget_status["status"], 0) > status_priority.get(worst_status, 0):
                worst_status = budget_status["status"]

            if utilization >= budget.alert_threshold_percent:
                alert_data = {
                    "budget_id": budget.budget_id,
                    "budget_name": budget.name,
                    "type": self._get_alert_type(utilization, budget),
                    "message": self._get_alert_message(utilization, budget),
                    "utilization_percent": utilization,
                }
                alerts.append(alert_data)
                
                try:
                    from api.services.alert_service import alert_service
                    
                    await alert_service.create_alert(
                        budget_id=budget.budget_id,
                        user_id=user_id,
                        alert_type=self._get_alert_type(utilization, budget),
                        message=self._get_alert_message(utilization, budget),
                        utilization_percent=utilization,
                    )
                except Exception as e:
                    logger.warning("Failed to send budget alert: %s", e)

        return {
            "status": worst_status,
            "applicable_budgets": budget_statuses,
            "alerts": alerts,
        }

    async def _find_applicable_budgets(
        self,
        user_id: str,
        scope: dict[str, Any],
    ) -> list[InfrastructureBudget]:
        """Find budgets applicable to given scope.

        Simplified matching logic:
        - OVERALL: Always matches
        - CLOUD_PROVIDER: Matches if cloud matches AND (no env filter OR env matches)
        - ENVIRONMENT: Matches if env matches AND (no cloud filter OR cloud matches)

        Args:
            user_id: User ID
            scope: Scope dictionary with cloud_providers and environment_name

        Returns:
            List of applicable budgets
        """
        all_budgets = await self.get_budgets(user_id, status=BudgetStatus.ACTIVE)
        
        applicable = []
        cloud_providers = [cp.lower() if cp else None for cp in scope.get("cloud_providers", [])]
        environment_name = scope.get("environment_name")
        env_name_lower = environment_name.lower() if environment_name else None

        for budget in all_budgets:
            budget_cloud = budget.scope.cloud_provider.lower() if budget.scope.cloud_provider else None
            budget_env_name = budget.scope.environment_name.lower() if budget.scope.environment_name else None

            if budget.scope.type == BudgetScopeType.OVERALL:
                applicable.append(budget)
            elif budget.scope.type == BudgetScopeType.CLOUD_PROVIDER:
                cloud_matches = budget_cloud and budget_cloud in cloud_providers
                env_matches = not budget_env_name or (env_name_lower and budget_env_name == env_name_lower)
                if cloud_matches and env_matches:
                    applicable.append(budget)
            elif budget.scope.type == BudgetScopeType.ENVIRONMENT:
                env_matches = budget_env_name and env_name_lower and budget_env_name == env_name_lower
                cloud_matches = not budget_cloud or (budget_cloud in cloud_providers)
                if env_matches and cloud_matches:
                    applicable.append(budget)

        return applicable

    def _calculate_status(
        self,
        utilization_percent: float,
        budget: InfrastructureBudget,
    ) -> str:
        """Calculate budget status from utilization.

        Args:
            utilization_percent: Utilization percentage
            budget: Budget object

        Returns:
            Status string
        """
        if utilization_percent >= 100:
            return "exceeded"
        if utilization_percent >= budget.critical_threshold_percent:
            return "critical"
        if utilization_percent >= budget.alert_threshold_percent:
            return "warning"
        return "on_track"

    def _get_alert_type(
        self,
        utilization_percent: float,
        budget: InfrastructureBudget,
    ) -> str:
        """Get alert type from utilization.

        Args:
            utilization_percent: Utilization percentage
            budget: Budget object

        Returns:
            Alert type string
        """
        if utilization_percent >= 100:
            return "exceeded"
        if utilization_percent >= budget.critical_threshold_percent:
            return "critical"
        return "warning"

    def _get_alert_message(
        self,
        utilization_percent: float,
        budget: InfrastructureBudget,
    ) -> str:
        """Get alert message from utilization.

        Args:
            utilization_percent: Utilization percentage
            budget: Budget object

        Returns:
            Alert message string
        """
        if utilization_percent >= 100:
            return f"Budget '{budget.name}' exceeded ({utilization_percent:.1f}%)"
        if utilization_percent >= budget.critical_threshold_percent:
            return f"Budget '{budget.name}' near limit ({utilization_percent:.1f}%)"
        return f"Budget '{budget.name}' approaching limit ({utilization_percent:.1f}%)"

    async def record_spending(
        self,
        user_id: str,
        amount_usd: float,
        source_type: str,
        source_id: Optional[str] = None,
        component_id: Optional[str] = None,
        cloud_provider: Optional[str] = None,
        environment_name: Optional[str] = None,
        service: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_spec: Optional[dict[str, Any]] = None,
    ) -> None:
        """Record spending from analysis documents.

        Args:
            user_id: User ID
            amount_usd: Spending amount
            source_type: Source type
            source_id: Source ID (resource_id)
            component_id: Component article_id
            cloud_provider: Cloud provider
            environment_id: Environment ID
            service: Service name
            resource_type: Resource type
            resource_spec: Resource specification
        """
        if amount_usd <= 0:
            return

        applicable_budgets = await self._find_applicable_budgets(
            user_id,
            {
                "cloud_providers": [cloud_provider] if cloud_provider else [],
                "environment_name": environment_name,
            },
        )

        if not applicable_budgets:
            return

        period_start, _ = get_month_period()
        period_str = period_start.strftime("%Y-%m")

        db = mongodb_manager.get_database()
        spending_collection = db.infrastructure_spending

        for budget in applicable_budgets:
            deduplication_key = {
                "source_type": source_type,
                "source_id": source_id,
                "period": period_str,
                "budget_id": budget.budget_id,
            }

            existing = spending_collection.find_one(deduplication_key)
            if existing:
                logger.debug(
                    "Skipping duplicate spending record: %s (budget: %s, period: %s)",
                    source_id,
                    budget.budget_id,
                    period_str,
                )
                continue

            spending_id = generate_spending_id()

            spending = InfrastructureSpending(
                spending_id=spending_id,
                budget_id=budget.budget_id,
                user_id=user_id,
                organization_id=budget.organization_id,
                source_type=source_type,
                source_id=source_id,
                component_id=component_id,
                amount_usd=amount_usd,
                period=period_str,
                date=datetime.utcnow(),
                cloud_provider=cloud_provider,
                environment_name=environment_name,
                service=service,
                resource_type=resource_type,
                resource_spec=resource_spec,
            )

            spending_collection.insert_one(spending.to_dict())

            await self._update_budget_status(budget.budget_id, period_str)

        logger.debug(
            "Recorded spending: $%.2f for user %s (%d budgets)",
            amount_usd,
            user_id,
            len(applicable_budgets),
        )

    async def _update_budget_status(
        self,
        budget_id: str,
        period: str,
    ) -> None:
        """Update budget status cache.

        Args:
            budget_id: Budget ID
            period: Period string (YYYY-MM)
        """
        db = mongodb_manager.get_database()
        spending_collection = db.infrastructure_spending
        status_collection = db.budget_status

        spending_records = list(
            spending_collection.find({"budget_id": budget_id, "period": period})
        )

        total_spent = sum(record.get("amount_usd", 0) for record in spending_records)

        budget = await self.get_budget(budget_id)
        if not budget:
            return

        utilization = (total_spent / budget.monthly_limit_usd) * 100 if budget.monthly_limit_usd > 0 else 0
        status_str = self._calculate_status(utilization, budget)

        breakdown_by_cloud = {}
        breakdown_by_service = {}
        breakdown_by_type = {}

        for record in spending_records:
            cloud = record.get("cloud_provider")
            if cloud:
                breakdown_by_cloud[cloud] = breakdown_by_cloud.get(cloud, 0) + record.get("amount_usd", 0)
            
            svc = record.get("service")
            if svc:
                breakdown_by_service[svc] = breakdown_by_service.get(svc, 0) + record.get("amount_usd", 0)
            
            rtype = record.get("resource_type")
            if rtype:
                breakdown_by_type[rtype] = breakdown_by_type.get(rtype, 0) + record.get("amount_usd", 0)

        days_elapsed = (datetime.utcnow() - budget.current_period_start).days + 1
        days_in_month = (budget.current_period_end - budget.current_period_start).days + 1
        
        if days_elapsed > 0:
            projected_spend = (total_spent / days_elapsed) * days_in_month
        else:
            projected_spend = 0.0

        status = BudgetStatusAggregate(
            budget_id=budget_id,
            period=period,
            total_spent_usd=total_spent,
            budget_limit_usd=budget.monthly_limit_usd,
            remaining_usd=budget.monthly_limit_usd - total_spent,
            utilization_percent=utilization,
            status=status_str,
            by_cloud_provider=breakdown_by_cloud,
            by_service=breakdown_by_service,
            by_resource_type=breakdown_by_type,
            projected_monthly_spend=projected_spend,
            projected_exceed=projected_spend > budget.monthly_limit_usd,
            days_until_exceed=self._calculate_days_until_exceed(
                total_spent,
                budget.monthly_limit_usd,
                days_elapsed,
                days_in_month,
            ),
            last_updated=datetime.utcnow(),
        )

        status_collection.replace_one(
            {"budget_id": budget_id, "period": period},
            status.to_dict(),
            upsert=True,
        )

    def _calculate_days_until_exceed(
        self,
        current_spent: float,
        budget_limit: float,
        days_elapsed: int,
        days_in_month: int,
    ) -> Optional[int]:
        """Calculate days until budget exceeded.

        Args:
            current_spent: Current spending
            budget_limit: Budget limit
            days_elapsed: Days elapsed in period
            days_in_month: Total days in period

        Returns:
            Days until exceed or None if not projected to exceed
        """
        if days_elapsed <= 0 or current_spent <= 0:
            return None

        daily_rate = current_spent / days_elapsed
        if daily_rate <= 0:
            return None

        remaining_budget = budget_limit - current_spent
        if remaining_budget <= 0:
            return 0

        days_until = int(remaining_budget / daily_rate)
        
        if days_until > days_in_month - days_elapsed:
            return None

        return days_until

    async def get_budget_status(
        self,
        budget_id: str,
        period: Optional[str] = None,
    ) -> Optional[BudgetStatusAggregate]:
        """Get aggregated budget status.

        Handles period rollover - ensures budget uses current period.

        Args:
            budget_id: Budget ID
            period: Period string (YYYY-MM), defaults to current month

        Returns:
            BudgetStatusAggregate or None if not found
        """
        budget = await self.get_budget(budget_id)
        if not budget:
            return None

        current_period_start, current_period_end = get_month_period()
        current_period = current_period_start.strftime("%Y-%m")

        if period is None:
            period = current_period

        if period != current_period:
            if budget.current_period_start != current_period_start:
                budget.current_period_start = current_period_start
                budget.current_period_end = current_period_end
                db = mongodb_manager.get_database()
                budgets_collection = db.infrastructure_budgets
                budgets_collection.update_one(
                    {"_id": budget_id},
                    {
                        "$set": {
                            "current_period_start": current_period_start,
                            "current_period_end": current_period_end,
                        }
                    },
                )

        db = mongodb_manager.get_database()
        collection = db.budget_status

        doc = collection.find_one({"budget_id": budget_id, "period": period})
        if not doc:
            if period == current_period:
                await self._initialize_budget_status(budget_id, current_period_start)
                doc = collection.find_one({"budget_id": budget_id, "period": period})
                if not doc:
                    return None
            else:
                return None

        return BudgetStatusAggregate.from_dict(doc)

    async def aggregate_spending_from_analysis(
        self,
        user_id: str,
        period_start: datetime,
        period_end: datetime,
    ) -> dict[str, Any]:
        """Aggregate spending from KnowledgeArticle analysis documents.

        Args:
            user_id: User ID
            period_start: Period start date
            period_end: Period end date

        Returns:
            Dictionary with aggregated spending
        """
        db = mongodb_manager.get_database()
        articles_collection = db.knowledge_articles

        query = {
            "user_id": ObjectId(user_id),
            "source_type": "repository-analysis",
            "cost_impact.total_monthly": {"$exists": True, "$gt": 0},
            "analyzed_at": {
                "$gte": period_start,
                "$lte": period_end,
            },
        }

        total_spent = 0.0
        by_cloud = {}
        by_service = {}
        by_resource_type = {}

        for article in articles_collection.find(query):
            cost_data = article.get("cost_impact", {})
            monthly_cost = cost_data.get("total_monthly", 0)
            
            if monthly_cost <= 0:
                continue

            total_spent += monthly_cost

            cloud_providers = article.get("cloud_providers", [])
            for cloud in cloud_providers:
                by_cloud[cloud] = by_cloud.get(cloud, 0) + monthly_cost

            services = article.get("services", [])
            for service in services:
                by_service[service] = by_service.get(service, 0) + monthly_cost

        return {
            "total_spent_usd": total_spent,
            "by_cloud_provider": by_cloud,
            "by_service": by_service,
            "by_resource_type": by_resource_type,
            "component_count": articles_collection.count_documents(query),
        }


budget_service = BudgetService()

