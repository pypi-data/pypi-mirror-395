"""Quota enforcement service for plan limits."""

import logging
import time
from datetime import datetime, timedelta
from typing import Any, Optional

from bson import ObjectId
from fastapi import HTTPException, status

from api.database.mongodb import mongodb_manager
from api.models.billing import PlanLimits
from api.services.exceptions import QuotaExceededError
from api.services.organization_quota_service import (
    OrganizationQuotaExceededError,
    organization_quota_service,
)
from api.services.plan_service import plan_service
from api.services.usage_aggregator import usage_aggregator

logger = logging.getLogger(__name__)

_MAX_TIME_DRIFT_SECONDS = 300


class QuotaService:
    """Service for enforcing plan-based quotas."""

    def _get_validated_time(self) -> datetime:
        """Get current UTC time with clock manipulation detection.

        Returns:
            Current UTC datetime

        Raises:
            RuntimeError: If system clock appears to be manipulated
        """
        now = datetime.utcnow()
        
        try:
            system_time = time.time()
            now_timestamp = now.timestamp()
            drift = abs(system_time - now_timestamp)
            
            if drift > _MAX_TIME_DRIFT_SECONDS:
                logger.warning(
                    "System time drift detected: %.1f seconds (max allowed: %d). "
                    "This may indicate clock manipulation.",
                    drift,
                    _MAX_TIME_DRIFT_SECONDS,
                )
        except Exception as e:
            logger.warning("Failed to validate system time: %s", e)
        
        return now

    def _get_user(self, user_id: str) -> dict[str, Any] | None:
        """Get user document from database.

        Args:
            user_id: User ID

        Returns:
            User document or None
        """
        db = mongodb_manager.get_database()
        try:
            user = db.users.find_one({"_id": ObjectId(user_id)})
            return user
        except Exception as e:
            logger.warning("Failed to get user %s: %s", user_id, e)
            return None

    def _mark_free_tier_exhausted(self, user_id: str) -> None:
        """Mark free tier as permanently exhausted for user.

        Args:
            user_id: User ID
        """
        db = mongodb_manager.get_database()
        try:
            result = db.users.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "free_tier_exhausted": True,
                        "free_tier_exhausted_at": self._get_validated_time(),
                    }
                }
            )
            if result.modified_count > 0:
                logger.info("Marked free tier as exhausted for user %s", user_id)
        except Exception as e:
            logger.error("Failed to mark free tier as exhausted for user %s: %s", user_id, e)

    def _is_trial_active(self, user: dict[str, Any] | None) -> bool:
        """Check if user has an active trial.

        Args:
            user: User document

        Returns:
            True if trial is active, False otherwise
        """
        if not user:
            return False

        trial_start = user.get("trial_start")
        trial_end = user.get("trial_end")

        if not trial_start or not trial_end:
            return False

        if isinstance(trial_start, datetime) and isinstance(trial_end, datetime):
            now = self._get_validated_time()
            return trial_start <= now <= trial_end

        return False

    def _get_upgrade_message(self, plan: str) -> str:
        """Get upgrade message with clear upgrade path.

        Args:
            plan: Current plan ID

        Returns:
            Upgrade message with upgrade options
        """
        if plan == "professional":
            return (
                "Upgrade to Team ($999/month) for team collaboration, 10,000 queries/month (team-wide), "
                "priority support (30-min SLA), and team knowledge base. "
                "Visit https://app.wistx.ai/billing to upgrade."
            )
        elif plan == "team":
            return (
                "Upgrade to Enterprise for unlimited queries, custom compliance frameworks, SSO/SAML, "
                "and dedicated support. Contact sales at hi@wistx.ai to discuss Enterprise options."
            )
        elif plan == "enterprise":
            return (
                "You're on the highest tier plan. If you need additional resources, please contact support at hi@wistx.ai."
            )
        else:
            return (
                "Please upgrade your plan to continue using WISTX. "
                "Visit https://app.wistx.ai/billing to upgrade."
            )

    async def check_query_quota(self, user_id: str, plan: str) -> None:
        """Check if user can make a query (within monthly limit).

        Args:
            user_id: User ID
            plan: User's plan ID

        Raises:
            QuotaExceededError: If quota is exceeded
            HTTPException: If plan not found
        """
        if plan == "enterprise":
            user = self._get_user(user_id)
            is_self_hosted = user.get("is_self_hosted", False) if user else False
            if is_self_hosted:
                return

        if plan not in ["professional", "team", "enterprise"]:
            user = self._get_user(user_id)
            if not user:
                raise QuotaExceededError(
                    "User not found. Please contact support.",
                    "user_not_found",
                    0,
                    0,
                )

            if self._is_trial_active(user):
                return

            trial_end = user.get("trial_end")
            if trial_end and isinstance(trial_end, datetime):
                if self._get_validated_time() > trial_end:
                    upgrade_message = self._get_upgrade_message(plan)
                    raise QuotaExceededError(
                        f"Your 7-day free trial has ended. {upgrade_message}",
                        "trial_expired",
                        0,
                        0,
                    )

            subscription_status = user.get("subscription_status")

            if subscription_status == "past_due":
                raise QuotaExceededError(
                    "Payment failed. Please update your payment method at https://app.wistx.ai/billing to continue using WISTX.",
                    "payment_failed",
                    0,
                    0,
                )

            if subscription_status == "canceled":
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription canceled. {upgrade_message}",
                    "subscription_canceled",
                    0,
                    0,
                )

            if not subscription_status or subscription_status not in ["active", "trialing"]:
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription not active. {upgrade_message}",
                    "subscription_inactive",
                    0,
                    0,
                )

        user = self._get_user(user_id)
        if not user:
            raise QuotaExceededError(
                "User not found. Please contact support.",
                "user_not_found",
                0,
                0,
            )

        organization_id = user.get("organization_id")

        if plan == "professional":
            subscription_status = user.get("subscription_status")

            if subscription_status == "past_due":
                raise QuotaExceededError(
                    "Payment failed. Please update your payment method at https://app.wistx.ai/billing to continue using WISTX.",
                    "payment_failed",
                    0,
                    0,
                )

            if subscription_status == "canceled":
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription canceled. {upgrade_message}",
                    "subscription_canceled",
                    0,
                    0,
                )

            if not subscription_status or subscription_status not in ["active", "trialing"]:
                raise QuotaExceededError(
                    f"Subscription not active. Please subscribe to Professional plan at https://app.wistx.ai/billing to continue using WISTX.",
                    "subscription_inactive",
                    0,
                    0,
                )

            plan_limits = plan_service.get_plan_limits(plan)
            if not plan_limits:
                logger.warning("Plan not found: %s, defaulting to professional plan", plan)
                plan_limits = plan_service.get_plan_limits("professional")
                if not plan_limits:
                    raise DatabaseError(
                        message="Plan configuration error: professional plan limits not found",
                        user_message="Plan configuration error. Please contact support.",
                        error_code="PLAN_CONFIG_ERROR",
                        details={"plan": "professional"}
                    )

            if plan_limits.queries_per_month == -1:
                return

            now = self._get_validated_time()
            start_of_month = datetime(now.year, now.month, 1)
            end_of_month = start_of_month + timedelta(days=32)
            end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

            usage = await usage_aggregator.aggregate_user_usage(user_id, start_of_month, end_of_month)
            current_queries = usage.get("total_queries", 0)

            if current_queries >= plan_limits.queries_per_month:
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Query quota exceeded (used {current_queries}/{plan_limits.queries_per_month}). {upgrade_message}",
                    "queries_per_month",
                    current_queries,
                    plan_limits.queries_per_month,
                )
            return

        if plan == "enterprise":
            if not organization_id:
                raise ValidationError(
                    message="Enterprise plan requires organization membership",
                    user_message="Enterprise plan requires organization membership. Please create or join an organization.",
                    error_code="ENTERPRISE_REQUIRES_ORGANIZATION",
                    details={"plan": plan}
                )
            return

        if plan == "team":
            subscription_status = user.get("subscription_status")

            if subscription_status == "past_due":
                raise QuotaExceededError(
                    "Payment failed. Please update your payment method at https://app.wistx.ai/billing to continue using WISTX.",
                    "payment_failed",
                    0,
                    0,
                )

            if subscription_status == "canceled":
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription canceled. {upgrade_message}",
                    "subscription_canceled",
                    0,
                    0,
                )

            if not subscription_status or subscription_status not in ["active", "trialing"]:
                raise QuotaExceededError(
                    f"Subscription not active. Please subscribe to Team plan at https://app.wistx.ai/billing to continue using WISTX.",
                    "subscription_inactive",
                    0,
                    0,
                )

            if not organization_id:
                raise ValidationError(
                    message="Team plan requires organization membership",
                    user_message="Team plan requires organization membership. Please create or join an organization.",
                    error_code="TEAM_REQUIRES_ORGANIZATION",
                    details={"plan": plan}
                )

            await organization_quota_service.check_organization_query_quota(
                str(organization_id), plan
            )
            return

        plan_limits = plan_service.get_plan_limits(plan)
        if not plan_limits:
            logger.warning("Plan not found: %s, defaulting to professional plan", plan)
            plan_limits = plan_service.get_plan_limits("professional")
            if not plan_limits:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Plan configuration error",
                )

        if plan_limits.queries_per_month == -1:
            return

        now = self._get_validated_time()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

        usage = await usage_aggregator.aggregate_user_usage(user_id, start_of_month, end_of_month)
        current_queries = usage.get("total_queries", 0)

        if current_queries >= plan_limits.queries_per_month:
            upgrade_message = self._get_upgrade_message(plan)
            raise QuotaExceededError(
                f"Query quota exceeded (used {current_queries}/{plan_limits.queries_per_month}). {upgrade_message}",
                "queries_per_month",
                current_queries,
                plan_limits.queries_per_month,
            )

    async def check_indexing_quota(
        self,
        user_id: str,
        plan: str,
        estimated_storage_mb: float = 0.0,
    ) -> None:
        """Check if user can index a resource.

        Args:
            user_id: User ID
            plan: User's plan ID
            estimated_storage_mb: Estimated storage in MB for this operation

        Raises:
            QuotaExceededError: If quota is exceeded
            HTTPException: If plan not found
        """
        if plan == "professional":
            user = self._get_user(user_id)
            if not user:
                raise QuotaExceededError(
                    "User not found. Please contact support.",
                    "user_not_found",
                    0,
                    0,
                )

        if plan in ["professional", "team"]:
            user = self._get_user(user_id)
            if not user:
                raise QuotaExceededError(
                    "User not found. Please contact support.",
                    "user_not_found",
                    0,
                    0,
                )

            if self._is_trial_active(user):
                return

            trial_end = user.get("trial_end")
            if trial_end and isinstance(trial_end, datetime):
                if self._get_validated_time() > trial_end:
                    upgrade_message = self._get_upgrade_message(plan)
                    raise QuotaExceededError(
                        f"Your 7-day free trial has ended. {upgrade_message}",
                        "trial_expired",
                        0,
                        0,
                    )

            subscription_status = user.get("subscription_status")

            if subscription_status == "past_due":
                raise QuotaExceededError(
                    "Payment failed. Please update your payment method at https://app.wistx.ai/billing to continue using WISTX.",
                    "payment_failed",
                    0,
                    0,
                )

            if subscription_status == "canceled":
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription canceled. {upgrade_message}",
                    "subscription_canceled",
                    0,
                    0,
                )

            if not subscription_status or subscription_status not in ["active", "trialing"]:
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription not active. {upgrade_message}",
                    "subscription_inactive",
                    0,
                    0,
                )

        user = self._get_user(user_id)
        if not user:
            raise QuotaExceededError(
                "User not found. Please contact support.",
                "user_not_found",
                0,
                0,
            )

        organization_id = user.get("organization_id")

        if plan == "professional":
            subscription_status = user.get("subscription_status")

            if subscription_status == "past_due":
                raise QuotaExceededError(
                    "Payment failed. Please update your payment method at https://app.wistx.ai/billing to continue using WISTX.",
                    "payment_failed",
                    0,
                    0,
                )

            if subscription_status == "canceled":
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription canceled. {upgrade_message}",
                    "subscription_canceled",
                    0,
                    0,
                )

            if not subscription_status or subscription_status not in ["active", "trialing"]:
                raise QuotaExceededError(
                    f"Subscription not active. Please subscribe to Professional plan at https://app.wistx.ai/billing to continue using WISTX.",
                    "subscription_inactive",
                    0,
                    0,
                )

        if plan == "enterprise":
            if not organization_id:
                raise ValidationError(
                    message="Enterprise plan requires organization membership",
                    user_message="Enterprise plan requires organization membership. Please create or join an organization.",
                    error_code="ENTERPRISE_REQUIRES_ORGANIZATION",
                    details={"plan": plan}
                )
            is_self_hosted = user.get("is_self_hosted", False)
            if is_self_hosted:
                return
            return

        if plan == "team":
            subscription_status = user.get("subscription_status")

            if subscription_status == "past_due":
                raise QuotaExceededError(
                    "Payment failed. Please update your payment method at https://app.wistx.ai/billing to continue using WISTX.",
                    "payment_failed",
                    0,
                    0,
                )

            if subscription_status == "canceled":
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Subscription canceled. {upgrade_message}",
                    "subscription_canceled",
                    0,
                    0,
                )

            if not subscription_status or subscription_status not in ["active", "trialing"]:
                raise QuotaExceededError(
                    f"Subscription not active. Please subscribe to Team plan at https://app.wistx.ai/billing to continue using WISTX.",
                    "subscription_inactive",
                    0,
                    0,
                )

            if not organization_id:
                raise ValidationError(
                    message="Team plan requires organization membership",
                    user_message="Team plan requires organization membership. Please create or join an organization.",
                    error_code="TEAM_REQUIRES_ORGANIZATION",
                    details={"plan": plan}
                )

            await organization_quota_service.check_organization_indexing_quota(
                str(organization_id), plan, estimated_storage_mb
            )
            return

        if plan == "enterprise":
            is_self_hosted = user.get("is_self_hosted", False)
            if is_self_hosted:
                return

        plan_limits = plan_service.get_plan_limits(plan)
        if not plan_limits:
            logger.warning("Plan not found: %s, defaulting to professional plan", plan)
            plan_limits = plan_service.get_plan_limits("professional")
            if not plan_limits:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Plan configuration error",
                )

        plan_features = plan_service.get_plan_features(plan)
        if not plan_features:
            raise DatabaseError(
                message=f"Plan features not found for plan: {plan}",
                user_message="Plan configuration error. Please contact support.",
                error_code="PLAN_FEATURES_NOT_FOUND",
                details={"plan": plan}
            )

        if not plan_features.repository_indexing and not plan_features.document_indexing:
            raise QuotaExceededError(
                "Indexing not available on your plan. Please upgrade to a plan that supports indexing.",
                "indexing_feature",
                0,
                0,
            )

        now = self._get_validated_time()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

        usage = await usage_aggregator.aggregate_user_usage(user_id, start_of_month, end_of_month)
        current_indexes = usage.get("total_indexes", 0)
        current_storage_mb = usage.get("total_storage_mb", 0.0)

        if plan_limits.indexes_per_month != -1 and current_indexes >= plan_limits.indexes_per_month:
            upgrade_message = self._get_upgrade_message(plan)
            raise QuotaExceededError(
                f"Indexing quota exceeded (used {current_indexes}/{plan_limits.indexes_per_month}). {upgrade_message}",
                "indexes_per_month",
                current_indexes,
                plan_limits.indexes_per_month,
            )

        if plan_limits.storage_mb != -1:
            new_storage = current_storage_mb + estimated_storage_mb
            if new_storage > plan_limits.storage_mb:
                upgrade_message = self._get_upgrade_message(plan)
                raise QuotaExceededError(
                    f"Storage quota exceeded (used {current_storage_mb:.2f}/{plan_limits.storage_mb} MB). {upgrade_message}",
                    "storage_mb",
                    new_storage,
                    plan_limits.storage_mb,
                )

    async def get_storage_usage(self, user_id: str) -> dict[str, Any]:
        """Get current storage usage for user.

        Args:
            user_id: User ID

        Returns:
            Dictionary with storage usage details
        """
        db = mongodb_manager.get_database()

        now = self._get_validated_time()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

        usage = await usage_aggregator.aggregate_user_usage(user_id, start_of_month, end_of_month)

        knowledge_articles_count = db.knowledge_articles.count_documents(
            {"user_id": ObjectId(user_id)}
        )

        indexed_resources_count = 0
        if "indexed_resources" in db.list_collection_names():
            indexed_resources_count = db.indexed_resources.count_documents(
                {"user_id": ObjectId(user_id), "status": {"$ne": "deleted"}}
            )

        return {
            "storage_mb": usage.get("total_storage_mb", 0.0),
            "knowledge_articles": knowledge_articles_count,
            "indexed_resources": indexed_resources_count,
            "total_indexes": usage.get("total_indexes", 0),
            "period": {
                "start": start_of_month.isoformat(),
                "end": end_of_month.isoformat(),
            },
        }

    async def get_quota_status(self, user_id: str, plan: str) -> dict[str, Any]:
        """Get current quota status for user.

        Args:
            user_id: User ID
            plan: User's plan ID

        Returns:
            Dictionary with quota status
        """
        plan_limits = plan_service.get_plan_limits(plan)
        if not plan_limits:
            plan_limits = plan_service.get_plan_limits("professional")
            if not plan_limits:
                return {
                    "error": "Plan configuration error",
                }

        now = self._get_validated_time()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = start_of_month + timedelta(days=32)
        end_of_month = end_of_month.replace(day=1) - timedelta(seconds=1)

        usage = await usage_aggregator.aggregate_user_usage(user_id, start_of_month, end_of_month)
        storage_usage = await self.get_storage_usage(user_id)

        return {
            "plan": plan,
            "period": {
                "start": start_of_month.isoformat(),
                "end": end_of_month.isoformat(),
            },
            "queries": {
                "used": usage.get("total_queries", 0),
                "limit": plan_limits.queries_per_month,
                "unlimited": plan_limits.queries_per_month == -1,
            },
            "indexes": {
                "used": usage.get("total_indexes", 0),
                "limit": plan_limits.indexes_per_month,
                "unlimited": plan_limits.indexes_per_month == -1,
            },
            "storage": {
                "used_mb": storage_usage.get("storage_mb", 0.0),
                "limit_mb": plan_limits.storage_mb,
                "unlimited": plan_limits.storage_mb == -1,
            },
        }

    def start_trial(self, user_id: str, plan: str) -> None:
        """Start 7-day free trial (deprecated - no longer supported).

        Args:
            user_id: User ID
            plan: Plan ID

        Raises:
            ValueError: Trials are no longer supported
        """
        raise ValueError(
            f"Free trials are no longer available. "
            f"Please subscribe to Professional ($99/month), Team ($999/month), or Enterprise. "
            f"Visit https://app.wistx.ai/billing to subscribe."
        )

        db = mongodb_manager.get_database()
        user = self._get_user(user_id)

        if not user:
            raise ValueError(f"User not found: {user_id}")

        if user.get("trial_used"):
            raise ValueError("Free trial already used. Please subscribe to continue using WISTX.")

        if self._is_trial_active(user):
            logger.info("User %s already has active trial", user_id)
            return

        trial_start = self._get_validated_time()
        trial_end = trial_start + timedelta(days=7)

        try:
            result = db.users.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "trial_start": trial_start,
                        "trial_end": trial_end,
                        "trial_plan": plan,
                        "plan": plan,
                    }
                }
            )
            if result.modified_count > 0:
                logger.info("Started 7-day free trial for user %s on plan %s", user_id, plan)
        except Exception as e:
            logger.error("Failed to start trial for user %s: %s", user_id, e)
            raise

    async def check_custom_controls_quota(
        self,
        user_id: str,
        plan: str,
        controls_count: int = 1,
    ) -> None:
        """Check if user can upload custom compliance controls.

        Args:
            user_id: User ID
            plan: User's plan ID
            controls_count: Number of controls to upload

        Raises:
            QuotaExceededError: If quota exceeded
            HTTPException: If plan not found
        """
        plan_limits = plan_service.get_plan_limits(plan)
        if not plan_limits:
            logger.warning("Plan not found: %s, defaulting to professional plan", plan)
            plan_limits = plan_service.get_plan_limits("professional")
            if not plan_limits:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Plan configuration error",
                )

        limits = {
            "professional": 100,
            "team": 1000,
            "enterprise": -1,
        }

        limit = limits.get(plan, 0)

        if limit == -1:
            return

        if limit == 0:
            raise QuotaExceededError(
                "Custom compliance controls require Professional plan or higher. Upgrade at https://app.wistx.ai/billing",
                "custom_controls",
                0,
                0,
            )

        db = mongodb_manager.get_database()
        try:
            current_count = db.compliance_controls.count_documents({
                "user_id": ObjectId(user_id),
                "is_custom": True,
            })
        except Exception as e:
            logger.error("Failed to count custom controls for user %s: %s", user_id, e)
            current_count = 0

        if current_count + controls_count > limit:
            upgrade_message = self._get_upgrade_message(plan)
            raise QuotaExceededError(
                f"Custom controls quota exceeded (used {current_count}/{limit}). {upgrade_message}",
                "custom_controls",
                current_count,
                limit,
            )


quota_service = QuotaService()

