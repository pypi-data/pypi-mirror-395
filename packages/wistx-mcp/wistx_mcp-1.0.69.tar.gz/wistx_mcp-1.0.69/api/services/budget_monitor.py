"""Scheduled budget monitoring service."""

import logging
from datetime import datetime
from typing import Any

from api.services.budget_service import budget_service
from api.models.budget import BudgetStatus

logger = logging.getLogger(__name__)


class BudgetMonitor:
    """Service for scheduled budget monitoring."""

    async def check_all_budgets(self) -> dict[str, Any]:
        """Check all active budgets and send alerts if needed.

        This should be called periodically (e.g., every hour via cron/scheduler).

        Returns:
            Dictionary with monitoring results
        """
        logger.info("Starting scheduled budget monitoring check")

        from api.database.mongodb import mongodb_manager

        db = mongodb_manager.get_database()
        budgets_collection = db.infrastructure_budgets

        active_budgets = list(
            budgets_collection.find({"status": BudgetStatus.ACTIVE.value})
        )

        results = {
            "checked": 0,
            "alerts_sent": 0,
            "errors": 0,
            "timestamp": datetime.utcnow().isoformat(),
        }

        for budget_doc in active_budgets:
            try:
                budget = await budget_service.get_budget(budget_doc["_id"])
                if not budget:
                    continue

                await self.check_budget(budget.budget_id, budget.user_id)
                results["checked"] += 1
            except (ValueError, RuntimeError, ConnectionError) as e:
                logger.error(
                    "Error checking budget %s: %s",
                    budget_doc.get("_id"),
                    e,
                    exc_info=True,
                )
                results["errors"] += 1

        logger.info(
            "Budget monitoring check complete: %d budgets checked, %d alerts sent",
            results["checked"],
            results["alerts_sent"],
        )

        return results

    async def check_budget(self, budget_id: str, user_id: str) -> None:
        """Check a specific budget and send alerts if needed.

        Args:
            budget_id: Budget ID to check
            user_id: User ID who owns the budget
        """
        budget = await budget_service.get_budget(budget_id)
        if not budget:
            logger.warning("Budget not found: %s", budget_id)
            return

        status = await budget_service.get_budget_status(budget_id)
        if not status:
            logger.debug("No spending data for budget %s yet", budget_id)
            return

        utilization = (
            (status.total_spent_usd / budget.monthly_limit_usd) * 100
            if budget.monthly_limit_usd > 0
            else 0
        )

        if utilization >= budget.alert_threshold_percent:
            alert_type = self._calculate_status(utilization, budget)
            message = self._get_alert_message(utilization, budget)

            try:
                from api.services.alert_service import alert_service

                await alert_service.create_alert(
                    budget_id=budget_id,
                    user_id=user_id,
                    alert_type=alert_type,
                    message=message,
                    utilization_percent=utilization,
                )
                logger.info(
                    "Sent alert for budget %s: %s (%.1f%%)",
                    budget_id,
                    alert_type,
                    utilization,
                )
            except (ValueError, RuntimeError, ConnectionError) as e:
                logger.error(
                    "Failed to send alert for budget %s: %s",
                    budget_id,
                    e,
                    exc_info=True,
                )

    async def check_budgets_for_user(self, user_id: str) -> dict[str, Any]:
        """Check all budgets for a specific user.

        Args:
            user_id: User ID

        Returns:
            Dictionary with monitoring results
        """
        budgets = await budget_service.get_budgets(user_id, status=BudgetStatus.ACTIVE)

        results = {
            "user_id": user_id,
            "checked": 0,
            "alerts_sent": 0,
            "errors": 0,
            "timestamp": datetime.utcnow().isoformat(),
        }

        for budget in budgets:
            try:
                await self.check_budget(budget.budget_id, user_id)
                results["checked"] += 1
            except (ValueError, RuntimeError, ConnectionError) as e:
                logger.error(
                    "Error checking budget %s for user %s: %s",
                    budget.budget_id,
                    user_id,
                    e,
                    exc_info=True,
                )
                results["errors"] += 1

        return results

    def _calculate_status(
        self,
        utilization_percent: float,
        budget: Any,
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

    def _get_alert_message(
        self,
        utilization_percent: float,
        budget: Any,
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


budget_monitor = BudgetMonitor()

