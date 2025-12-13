"""Spot Instance Advisor.

Provides intelligent Spot instance recommendations with interruption risk
analysis and cost savings estimates. Recommends when and how to use Spot
instances during infrastructure code generation.

Industry Comparison:
- Spot.io: Automated Spot management
- Xosphere: Spot optimization
- WISTX: Proactive Spot recommendations at code generation time

Key Features:
1. Interruption risk analysis by instance type and region
2. Diversification recommendations across pools
3. Cost savings estimation vs On-Demand
4. Workload suitability assessment
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class WorkloadType(str, Enum):
    """Types of workloads for Spot suitability."""
    STATELESS_WEB = "stateless_web"
    BATCH_PROCESSING = "batch_processing"
    CI_CD = "ci_cd"
    DEV_TEST = "dev_test"
    DATA_PROCESSING = "data_processing"
    MACHINE_LEARNING = "machine_learning"
    CONTAINERIZED = "containerized"
    STATEFUL = "stateful"
    DATABASE = "database"


class SpotSuitability(str, Enum):
    """Suitability rating for Spot instances."""
    EXCELLENT = "excellent"  # >40% savings, low risk
    GOOD = "good"  # 30-40% savings, manageable risk
    MODERATE = "moderate"  # 20-30% savings, medium risk
    NOT_RECOMMENDED = "not_recommended"  # High risk or stateful


class InterruptionRisk(str, Enum):
    """Risk of Spot interruption."""
    VERY_LOW = "very_low"  # <5% frequency
    LOW = "low"  # 5-10%
    MEDIUM = "medium"  # 10-15%
    HIGH = "high"  # 15-20%
    VERY_HIGH = "very_high"  # >20%


@dataclass
class InstancePoolInfo:
    """Information about a Spot instance pool."""
    instance_type: str
    region: str
    availability_zone: str | None
    
    # Pricing
    current_spot_price: float
    on_demand_price: float
    savings_percentage: float
    
    # Risk
    interruption_risk: InterruptionRisk
    interruption_frequency: float  # % in last 30 days
    
    # Capacity
    capacity_status: str  # "available", "constrained", "unavailable"


@dataclass
class SpotRecommendation:
    """Recommendation for using Spot instances."""
    recommendation_id: str

    # Instance details
    instance_type: str

    # Suitability
    suitability: SpotSuitability
    workload_type: WorkloadType

    # Savings
    estimated_savings_percentage: float
    estimated_monthly_savings: float

    # Risk mitigation
    risk_level: InterruptionRisk
    diversification_strategy: str

    # Implementation
    recommended_allocation_strategy: str  # "capacity-optimized", "lowest-price", "diversified"
    min_on_demand_percentage: int  # Recommended On-Demand baseline

    # Context
    rationale: str

    # Fields with defaults must come last
    recommended_pools: list[InstancePoolInfo] = field(default_factory=list)
    fallback_instance_types: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class SpotAnalysis:
    """Complete Spot instance analysis for a workload."""
    analysis_id: str
    generated_at: datetime
    
    # Workload assessment
    workload_type: WorkloadType
    is_spot_suitable: bool
    suitability_rating: SpotSuitability
    suitability_reasons: list[str] = field(default_factory=list)
    
    # Recommendations
    recommendations: list[SpotRecommendation] = field(default_factory=list)
    
    # Summary
    total_potential_savings: float = 0.0
    recommended_spot_percentage: int = 0
    
    # Guidance
    implementation_steps: list[str] = field(default_factory=list)
    best_practices: list[str] = field(default_factory=list)


class SpotInstanceAdvisor:
    """Advisor for AWS Spot instance usage.
    
    Provides:
    1. Workload suitability assessment
    2. Instance pool recommendations
    3. Interruption risk analysis
    4. Cost savings estimates
    5. Diversification strategies
    """
    
    # Workload suitability mapping
    WORKLOAD_SUITABILITY = {
        WorkloadType.BATCH_PROCESSING: SpotSuitability.EXCELLENT,
        WorkloadType.CI_CD: SpotSuitability.EXCELLENT,
        WorkloadType.DEV_TEST: SpotSuitability.EXCELLENT,
        WorkloadType.DATA_PROCESSING: SpotSuitability.GOOD,
        WorkloadType.MACHINE_LEARNING: SpotSuitability.GOOD,
        WorkloadType.CONTAINERIZED: SpotSuitability.GOOD,
        WorkloadType.STATELESS_WEB: SpotSuitability.MODERATE,
        WorkloadType.STATEFUL: SpotSuitability.NOT_RECOMMENDED,
        WorkloadType.DATABASE: SpotSuitability.NOT_RECOMMENDED,
    }

    # Recommended Spot percentage by suitability
    RECOMMENDED_SPOT_PERCENTAGE = {
        SpotSuitability.EXCELLENT: 80,
        SpotSuitability.GOOD: 60,
        SpotSuitability.MODERATE: 30,
        SpotSuitability.NOT_RECOMMENDED: 0,
    }

    # Average Spot savings by instance family (approximate)
    SPOT_SAVINGS_BY_FAMILY = {
        "t3": 0.65,  # 65% savings
        "t3a": 0.70,
        "m5": 0.60,
        "m5a": 0.65,
        "m6i": 0.55,
        "c5": 0.60,
        "c5a": 0.65,
        "c6i": 0.55,
        "r5": 0.55,
        "r5a": 0.60,
        "g4dn": 0.70,  # GPU instances often have good savings
        "p3": 0.65,
        "default": 0.60,
    }

    # Interruption frequency by instance category (estimates based on AWS data)
    INTERRUPTION_FREQUENCY = {
        "general_purpose": 0.08,  # 8%
        "compute_optimized": 0.10,
        "memory_optimized": 0.12,
        "storage_optimized": 0.15,
        "accelerated": 0.18,  # GPU instances
    }

    def __init__(self):
        """Initialize the Spot Instance Advisor."""
        pass

    def assess_workload(
        self,
        workload_type: WorkloadType | str,
        instance_type: str | None = None,
        is_stateful: bool = False,
        requires_persistence: bool = False,
        can_handle_interruption: bool = True,
        has_checkpointing: bool = False,
    ) -> SpotAnalysis:
        """Assess a workload for Spot instance suitability.

        Args:
            workload_type: Type of workload
            instance_type: Target instance type (optional)
            is_stateful: Whether workload maintains state
            requires_persistence: Whether local storage must persist
            can_handle_interruption: Whether workload can handle 2-min warning
            has_checkpointing: Whether workload has checkpointing capability

        Returns:
            SpotAnalysis with suitability and recommendations
        """
        # Convert string to enum if needed
        if isinstance(workload_type, str):
            workload_type = self._parse_workload_type(workload_type)

        # Base suitability from workload type
        base_suitability = self.WORKLOAD_SUITABILITY.get(
            workload_type, SpotSuitability.MODERATE
        )

        # Adjust based on characteristics
        suitability, reasons = self._adjust_suitability(
            base_suitability,
            workload_type,
            is_stateful,
            requires_persistence,
            can_handle_interruption,
            has_checkpointing,
        )

        # Generate recommendations if suitable
        recommendations = []
        if suitability != SpotSuitability.NOT_RECOMMENDED:
            recommendations = self._generate_spot_recommendations(
                workload_type,
                suitability,
                instance_type,
            )

        # Calculate potential savings
        spot_pct = self.RECOMMENDED_SPOT_PERCENTAGE.get(suitability, 0)
        avg_savings = self.SPOT_SAVINGS_BY_FAMILY.get("default", 0.60)

        # Implementation steps
        impl_steps = self._get_implementation_steps(workload_type, suitability)

        # Best practices
        best_practices = self._get_best_practices(workload_type)

        return SpotAnalysis(
            analysis_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            workload_type=workload_type,
            is_spot_suitable=suitability != SpotSuitability.NOT_RECOMMENDED,
            suitability_rating=suitability,
            suitability_reasons=reasons,
            recommendations=recommendations,
            total_potential_savings=avg_savings * 100,  # As percentage
            recommended_spot_percentage=spot_pct,
            implementation_steps=impl_steps,
            best_practices=best_practices,
        )

    def get_instance_recommendation(
        self,
        instance_type: str,
        region: str,
        on_demand_price: float,
        workload_type: WorkloadType = WorkloadType.CONTAINERIZED,
    ) -> SpotRecommendation:
        """Get Spot recommendation for a specific instance type.

        Args:
            instance_type: AWS instance type (e.g., "m5.large")
            region: AWS region
            on_demand_price: On-demand hourly price
            workload_type: Type of workload

        Returns:
            SpotRecommendation with details
        """
        # Get instance family
        family = self._get_instance_family(instance_type)

        # Estimate Spot savings
        savings_pct = self.SPOT_SAVINGS_BY_FAMILY.get(
            family, self.SPOT_SAVINGS_BY_FAMILY["default"]
        )
        spot_price = on_demand_price * (1 - savings_pct)
        monthly_savings = (on_demand_price - spot_price) * 730  # Hours in month

        # Get interruption risk
        category = self._get_instance_category(family)
        int_freq = self.INTERRUPTION_FREQUENCY.get(category, 0.10)
        risk = self._frequency_to_risk(int_freq)

        # Generate diversification strategy
        fallbacks = self._get_fallback_instances(instance_type)

        # Determine allocation strategy
        suitability = self.WORKLOAD_SUITABILITY.get(workload_type, SpotSuitability.MODERATE)

        if suitability == SpotSuitability.EXCELLENT:
            strategy = "capacity-optimized"
            min_od = 10
        elif suitability == SpotSuitability.GOOD:
            strategy = "capacity-optimized"
            min_od = 20
        else:
            strategy = "diversified"
            min_od = 50

        # Create pool info
        pools = [
            InstancePoolInfo(
                instance_type=instance_type,
                region=region,
                availability_zone=None,
                current_spot_price=spot_price,
                on_demand_price=on_demand_price,
                savings_percentage=savings_pct * 100,
                interruption_risk=risk,
                interruption_frequency=int_freq * 100,
                capacity_status="available",
            )
        ]

        # Add fallback pools
        for fb in fallbacks[:2]:
            fb_family = self._get_instance_family(fb)
            fb_savings = self.SPOT_SAVINGS_BY_FAMILY.get(
                fb_family, self.SPOT_SAVINGS_BY_FAMILY["default"]
            )
            pools.append(InstancePoolInfo(
                instance_type=fb,
                region=region,
                availability_zone=None,
                current_spot_price=on_demand_price * (1 - fb_savings),
                on_demand_price=on_demand_price,
                savings_percentage=fb_savings * 100,
                interruption_risk=risk,
                interruption_frequency=int_freq * 100,
                capacity_status="available",
            ))

        return SpotRecommendation(
            recommendation_id=str(uuid.uuid4()),
            instance_type=instance_type,
            recommended_pools=pools,
            suitability=suitability,
            workload_type=workload_type,
            estimated_savings_percentage=savings_pct * 100,
            estimated_monthly_savings=monthly_savings,
            risk_level=risk,
            diversification_strategy=f"Use {len(pools)} instance pools for capacity resilience",
            fallback_instance_types=fallbacks,
            recommended_allocation_strategy=strategy,
            min_on_demand_percentage=min_od,
            rationale=self._generate_spot_rationale(
                instance_type, savings_pct, risk, workload_type
            ),
            prerequisites=self._get_prerequisites(workload_type),
            warnings=self._get_warnings(risk, workload_type),
        )

    def _parse_workload_type(self, workload_str: str) -> WorkloadType:
        """Parse workload type from string."""
        workload_lower = workload_str.lower()

        if "batch" in workload_lower or "job" in workload_lower:
            return WorkloadType.BATCH_PROCESSING
        elif "ci" in workload_lower or "cd" in workload_lower or "pipeline" in workload_lower:
            return WorkloadType.CI_CD
        elif "dev" in workload_lower or "test" in workload_lower:
            return WorkloadType.DEV_TEST
        elif "data" in workload_lower or "etl" in workload_lower or "spark" in workload_lower:
            return WorkloadType.DATA_PROCESSING
        elif "ml" in workload_lower or "machine" in workload_lower or "training" in workload_lower:
            return WorkloadType.MACHINE_LEARNING
        elif "container" in workload_lower or "ecs" in workload_lower or "kubernetes" in workload_lower:
            return WorkloadType.CONTAINERIZED
        elif "web" in workload_lower or "api" in workload_lower:
            return WorkloadType.STATELESS_WEB
        elif "database" in workload_lower or "db" in workload_lower or "rds" in workload_lower:
            return WorkloadType.DATABASE
        elif "stateful" in workload_lower:
            return WorkloadType.STATEFUL

        return WorkloadType.CONTAINERIZED  # Default

    def _adjust_suitability(
        self,
        base: SpotSuitability,
        workload_type: WorkloadType,
        is_stateful: bool,
        requires_persistence: bool,
        can_handle_interruption: bool,
        has_checkpointing: bool,
    ) -> tuple[SpotSuitability, list[str]]:
        """Adjust suitability based on workload characteristics."""
        reasons = []
        current = base

        # Negative adjustments
        if is_stateful:
            current = SpotSuitability.NOT_RECOMMENDED
            reasons.append("Stateful workloads are not recommended for Spot")

        if requires_persistence:
            if current != SpotSuitability.NOT_RECOMMENDED:
                current = SpotSuitability.NOT_RECOMMENDED
            reasons.append("Local storage persistence required - not suitable for Spot")

        if not can_handle_interruption:
            if current != SpotSuitability.NOT_RECOMMENDED:
                current = SpotSuitability.NOT_RECOMMENDED
            reasons.append("Cannot handle 2-minute interruption warning")

        # Positive adjustments
        if has_checkpointing and current not in [SpotSuitability.EXCELLENT, SpotSuitability.NOT_RECOMMENDED]:
            if current == SpotSuitability.MODERATE:
                current = SpotSuitability.GOOD
            elif current == SpotSuitability.GOOD:
                current = SpotSuitability.EXCELLENT
            reasons.append("Checkpointing capability improves Spot suitability")

        # Add base reason if not modified
        if not reasons:
            reasons.append(f"{workload_type.value} workloads are {current.value} for Spot instances")

        return current, reasons

    def _generate_spot_recommendations(
        self,
        workload_type: WorkloadType,
        suitability: SpotSuitability,
        instance_type: str | None,
    ) -> list[SpotRecommendation]:
        """Generate Spot recommendations for a workload."""
        recommendations = []

        # Default instance types by workload
        default_instances = {
            WorkloadType.BATCH_PROCESSING: ["m5.large", "m5a.large", "c5.large"],
            WorkloadType.CI_CD: ["t3.medium", "m5.large", "c5.large"],
            WorkloadType.DEV_TEST: ["t3.medium", "t3a.medium", "m5.large"],
            WorkloadType.DATA_PROCESSING: ["r5.large", "r5a.large", "m5.xlarge"],
            WorkloadType.MACHINE_LEARNING: ["g4dn.xlarge", "p3.2xlarge", "c5.4xlarge"],
            WorkloadType.CONTAINERIZED: ["m5.large", "m5a.large", "c5.large"],
            WorkloadType.STATELESS_WEB: ["t3.medium", "m5.large", "c5.large"],
        }

        target_instances = [instance_type] if instance_type else default_instances.get(
            workload_type, ["m5.large"]
        )

        for inst in target_instances[:3]:  # Max 3 recommendations
            rec = self.get_instance_recommendation(
                instance_type=inst,
                region="us-east-1",  # Default, would be context-dependent
                on_demand_price=self._estimate_on_demand_price(inst),
                workload_type=workload_type,
            )
            recommendations.append(rec)

        return recommendations

    def _estimate_on_demand_price(self, instance_type: str) -> float:
        """Estimate on-demand price for an instance type."""
        # Rough estimates for common instance types
        prices = {
            "t3.micro": 0.0104,
            "t3.small": 0.0208,
            "t3.medium": 0.0416,
            "t3.large": 0.0832,
            "t3a.medium": 0.0376,
            "t3a.large": 0.0752,
            "m5.large": 0.096,
            "m5.xlarge": 0.192,
            "m5a.large": 0.086,
            "m5a.xlarge": 0.172,
            "c5.large": 0.085,
            "c5.xlarge": 0.17,
            "c5a.large": 0.077,
            "r5.large": 0.126,
            "r5.xlarge": 0.252,
            "r5a.large": 0.113,
            "g4dn.xlarge": 0.526,
            "p3.2xlarge": 3.06,
        }
        return prices.get(instance_type, 0.10)

    def _get_instance_family(self, instance_type: str) -> str:
        """Extract instance family from type."""
        # e.g., "m5.large" -> "m5"
        parts = instance_type.split(".")
        return parts[0] if parts else "m5"

    def _get_instance_category(self, family: str) -> str:
        """Get instance category from family."""
        if family.startswith(("t", "m")):
            return "general_purpose"
        elif family.startswith("c"):
            return "compute_optimized"
        elif family.startswith("r"):
            return "memory_optimized"
        elif family.startswith(("i", "d")):
            return "storage_optimized"
        elif family.startswith(("p", "g", "inf")):
            return "accelerated"
        return "general_purpose"

    def _frequency_to_risk(self, frequency: float) -> InterruptionRisk:
        """Convert interruption frequency to risk level."""
        if frequency < 0.05:
            return InterruptionRisk.VERY_LOW
        elif frequency < 0.10:
            return InterruptionRisk.LOW
        elif frequency < 0.15:
            return InterruptionRisk.MEDIUM
        elif frequency < 0.20:
            return InterruptionRisk.HIGH
        return InterruptionRisk.VERY_HIGH

    def _get_fallback_instances(self, instance_type: str) -> list[str]:
        """Get fallback instance types for diversification."""
        family = self._get_instance_family(instance_type)
        size = instance_type.split(".")[-1] if "." in instance_type else "large"

        # Similar families for fallback
        fallback_families = {
            "t3": ["t3a", "t2", "m5"],
            "t3a": ["t3", "t2", "m5a"],
            "m5": ["m5a", "m6i", "m5n"],
            "m5a": ["m5", "m6a", "m5n"],
            "c5": ["c5a", "c6i", "c5n"],
            "c5a": ["c5", "c6a", "c5n"],
            "r5": ["r5a", "r6i", "r5n"],
            "r5a": ["r5", "r6a", "r5n"],
        }

        alternatives = fallback_families.get(family, [f"{family}a", f"{family}n"])
        return [f"{alt}.{size}" for alt in alternatives[:3]]

    def _generate_spot_rationale(
        self,
        instance_type: str,
        savings_pct: float,
        risk: InterruptionRisk,
        workload_type: WorkloadType,
    ) -> str:
        """Generate rationale for Spot recommendation."""
        return (
            f"{instance_type} offers {savings_pct*100:.0f}% savings as Spot with "
            f"{risk.value} interruption risk. {workload_type.value} workloads "
            f"are well-suited for Spot due to their fault-tolerant nature."
        )

    def _get_prerequisites(self, workload_type: WorkloadType) -> list[str]:
        """Get prerequisites for Spot usage."""
        prereqs = [
            "Implement graceful shutdown handling for 2-minute warning",
            "Use Instance Metadata Service (IMDS) to detect interruption",
        ]

        if workload_type in [WorkloadType.BATCH_PROCESSING, WorkloadType.DATA_PROCESSING]:
            prereqs.append("Implement job checkpointing for long-running tasks")

        if workload_type == WorkloadType.CONTAINERIZED:
            prereqs.append("Configure container orchestrator for Spot (ECS/EKS)")
            prereqs.append("Set up capacity providers with Spot support")

        if workload_type == WorkloadType.MACHINE_LEARNING:
            prereqs.append("Enable training checkpoints to S3")
            prereqs.append("Use SageMaker Managed Spot Training if applicable")

        return prereqs

    def _get_warnings(
        self,
        risk: InterruptionRisk,
        workload_type: WorkloadType,
    ) -> list[str]:
        """Get warnings for Spot usage."""
        warnings = []

        if risk in [InterruptionRisk.HIGH, InterruptionRisk.VERY_HIGH]:
            warnings.append(
                f"High interruption risk ({risk.value}) - ensure robust failover"
            )

        if workload_type == WorkloadType.STATELESS_WEB:
            warnings.append(
                "Maintain On-Demand baseline for production traffic stability"
            )

        warnings.append(
            "Spot prices vary by region and AZ - diversify across pools"
        )

        return warnings

    def _get_implementation_steps(
        self,
        workload_type: WorkloadType,
        suitability: SpotSuitability,
    ) -> list[str]:
        """Get implementation steps for Spot adoption."""
        if suitability == SpotSuitability.NOT_RECOMMENDED:
            return ["This workload is not recommended for Spot instances"]

        steps = [
            "1. Configure Auto Scaling Group with mixed instances policy",
            "2. Set capacity-optimized allocation strategy",
            f"3. Configure {self.RECOMMENDED_SPOT_PERCENTAGE.get(suitability, 50)}% Spot / On-Demand ratio",
            "4. Implement interruption handling in application",
            "5. Set up CloudWatch alarms for Spot interruption events",
        ]

        if workload_type == WorkloadType.CONTAINERIZED:
            steps.insert(2, "2a. Configure ECS/EKS capacity providers for Spot")

        return steps

    def _get_best_practices(self, workload_type: WorkloadType) -> list[str]:
        """Get best practices for Spot usage."""
        practices = [
            "Diversify across multiple instance types and AZs",
            "Use capacity-optimized allocation strategy",
            "Set up Spot Instance interruption notices via EventBridge",
            "Maintain minimum On-Demand capacity for stability",
            "Use EC2 Fleet or Auto Scaling for automatic replacement",
        ]

        if workload_type in [WorkloadType.BATCH_PROCESSING, WorkloadType.DATA_PROCESSING]:
            practices.append("Implement checkpointing every 15-30 minutes")
            practices.append("Use AWS Batch with Spot for managed execution")

        if workload_type == WorkloadType.MACHINE_LEARNING:
            practices.append("Use SageMaker Managed Spot Training for ML workloads")
            practices.append("Store checkpoints to S3 frequently")

        return practices
