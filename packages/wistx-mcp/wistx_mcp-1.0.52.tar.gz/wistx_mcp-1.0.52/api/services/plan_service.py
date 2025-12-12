"""Plan definitions and management service."""

from api.models.billing import PlanFeatures, PlanLimits, SubscriptionPlan
from api.exceptions import ValidationError, AuthorizationError


class PlanService:
    """Service for managing subscription plans."""

    PLANS: dict[str, SubscriptionPlan] = {
        "professional": SubscriptionPlan(
            plan_id="professional",
            name="Professional",
            description="For startup founders and independent consultants",
            monthly_price=99.0,
            annual_price=990.0,
            stripe_monthly_price_id="price_1SZgTDLoOXxJLV3bBUfln1OK",
            stripe_annual_price_id="price_1SZgTDLoOXxJLV3bIoOhkeIQ",
            limits=PlanLimits(
                queries_per_month=2000,
                indexes_per_month=5,
                storage_mb=20480,
                requests_per_minute=60,
                max_api_keys=2,
            ),
            features=PlanFeatures(
                compliance_queries=True,
                knowledge_queries=True,
                repository_indexing=True,
                document_indexing=True,
                custom_indexes=True,
                priority_support=False,
                sso=False,
                api_access=True,
            ),
            popular=True,
            is_active=True,
        ),
        "team": SubscriptionPlan(
            plan_id="team",
            name="Team",
            description="For enterprise DevOps teams - reduce compliance risk & optimize costs",
            monthly_price=999.0,
            annual_price=9990.0,
            stripe_monthly_price_id="price_1SZgUgLoOXxJLV3b6kVaa41P",
            stripe_annual_price_id="price_1SZgUgLoOXxJLV3bzO2V5Bbu",
            limits=PlanLimits(
                queries_per_month=10000,
                indexes_per_month=10,
                storage_mb=51200,
                requests_per_minute=60,
                max_api_keys=5,
            ),
            features=PlanFeatures(
                compliance_queries=True,
                knowledge_queries=True,
                repository_indexing=True,
                document_indexing=True,
                custom_indexes=True,
                priority_support=True,
                sso=False,
                api_access=True,
            ),
            popular=False,
            is_active=True,
        ),
        "enterprise": SubscriptionPlan(
            plan_id="enterprise",
            name="Enterprise",
            description="Enterprise-grade for large DevOps organizations - reduce audit time by 80%",
            monthly_price=0.0,
            annual_price=0.0,
            stripe_monthly_price_id="price_1SZgW4LoOXxJLV3b9tTUM8Vs",
            stripe_annual_price_id="price_1SZgW4LoOXxJLV3b9tTUM8Vs",
            limits=PlanLimits(
                queries_per_month=-1,
                indexes_per_month=-1,
                storage_mb=-1,
                requests_per_minute=1000,
                max_api_keys=100,
            ),
            features=PlanFeatures(
                compliance_queries=True,
                knowledge_queries=True,
                repository_indexing=True,
                document_indexing=True,
                custom_indexes=True,
                priority_support=True,
                sso=True,
                api_access=True,
            ),
            popular=False,
            is_active=True,
        ),
    }

    @classmethod
    def get_plan(cls, plan_id: str) -> SubscriptionPlan | None:
        """Get plan by ID.

        Args:
            plan_id: Plan ID

        Returns:
            SubscriptionPlan or None
        """
        return cls.PLANS.get(plan_id)

    @classmethod
    def list_plans(cls, active_only: bool = False) -> list[SubscriptionPlan]:
        """List all available plans.

        Args:
            active_only: If True, return only active plans available for new signups

        Returns:
            List of subscription plans
        """
        plans = list(cls.PLANS.values())
        if active_only:
            return [plan for plan in plans if plan.is_active]
        return plans

    @classmethod
    def get_plan_limits(cls, plan_id: str) -> PlanLimits | None:
        """Get plan limits.

        Args:
            plan_id: Plan ID

        Returns:
            PlanLimits or None
        """
        plan = cls.get_plan(plan_id)
        return plan.limits if plan else None

    @classmethod
    def get_plan_features(cls, plan_id: str) -> PlanFeatures | None:
        """Get plan features.

        Args:
            plan_id: Plan ID

        Returns:
            PlanFeatures or None
        """
        plan = cls.get_plan(plan_id)
        return plan.features if plan else None


plan_service = PlanService()


class PlanEnforcement:
    """Centralized plan enforcement utilities."""

    @staticmethod
    def check_feature_access(plan_id: str, feature_name: str) -> bool:
        """Check if plan has access to a feature.

        Args:
            plan_id: Plan ID
            feature_name: Feature name to check

        Returns:
            True if feature is available, False otherwise
        """
        plan_features = plan_service.get_plan_features(plan_id)
        if not plan_features:
            return False

        return getattr(plan_features, feature_name, False)

    @staticmethod
    def require_feature(plan_id: str, feature_name: str) -> None:
        """Require a feature, raise exception if not available.

        Args:
            plan_id: Plan ID
            feature_name: Feature name required

        Raises:
            ValueError: If feature not available
        """
        if not PlanEnforcement.check_feature_access(plan_id, feature_name):
            raise ValidationError(
                message=f"Feature '{feature_name}' is not available on {plan_id} plan",
                user_message=f"Feature '{feature_name}' is not available on {plan_id} plan. Please upgrade to access this feature.",
                error_code="FEATURE_NOT_AVAILABLE",
                details={"feature_name": feature_name, "plan_id": plan_id}
            )

    @staticmethod
    def check_minimum_plan(user_plan: str, required_plan: str) -> bool:
        """Check if user plan meets minimum requirement.

        Args:
            user_plan: User's current plan
            required_plan: Minimum required plan

        Returns:
            True if user plan meets requirement
        """
        plan_hierarchy = {
            "professional": 1,
            "team": 2,
            "enterprise": 3,
        }
        user_level = plan_hierarchy.get(user_plan, 0)
        required_level = plan_hierarchy.get(required_plan, 999)
        return user_level >= required_level

    @staticmethod
    def require_minimum_plan(user_plan: str, required_plan: str) -> None:
        """Require minimum plan, raise exception if not met.

        Args:
            user_plan: User's current plan
            required_plan: Minimum required plan

        Raises:
            ValueError: If plan requirement not met
        """
        if not PlanEnforcement.check_minimum_plan(user_plan, required_plan):
            raise AuthorizationError(
                message=f"This feature requires {required_plan} plan or higher",
                user_message=f"This feature requires {required_plan} plan or higher. Your current plan: {user_plan}",
                error_code="INSUFFICIENT_PLAN",
                details={"user_plan": user_plan, "required_plan": required_plan}
            )


plan_enforcement = PlanEnforcement()

