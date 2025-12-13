"""Rightsizing Analyzer.

Analyzes resource utilization and recommends optimal instance sizes.
Provides recommendations during infrastructure code generation.

Industry Comparison:
- AWS Cost Explorer: Basic rightsizing recommendations
- CloudHealth: Rightsizing with memory analysis
- WISTX: Proactive rightsizing at code generation time with workload-aware sizing

Key Features:
1. Utilization-based rightsizing (CPU, memory, network, storage)
2. Instance family recommendations for workload type
3. Cost impact analysis
4. Risk assessment for changes
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class RightsizingAction(str, Enum):
    """Types of rightsizing actions."""
    DOWNSIZE = "downsize"
    UPSIZE = "upsize"
    MODERNIZE = "modernize"  # Move to newer generation
    CHANGE_FAMILY = "change_family"
    OPTIMAL = "optimal"  # Already right-sized


class RightsizingRisk(str, Enum):
    """Risk level of rightsizing change."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ResourceHealth(str, Enum):
    """Resource health status based on utilization."""
    OVERSIZED = "oversized"  # <20% utilization
    UNDERUTILIZED = "underutilized"  # 20-40%
    OPTIMAL = "optimal"  # 40-80%
    CONSTRAINED = "constrained"  # 80-90%
    CRITICAL = "critical"  # >90%


@dataclass
class UtilizationMetrics:
    """Utilization metrics for a resource."""
    cpu_avg: float = 0.0
    cpu_max: float = 0.0
    memory_avg: float = 0.0
    memory_max: float = 0.0
    network_in_avg: float = 0.0  # Mbps
    network_out_avg: float = 0.0
    disk_read_avg: float = 0.0  # MB/s
    disk_write_avg: float = 0.0
    
    # Derived
    cpu_health: ResourceHealth = ResourceHealth.OPTIMAL
    memory_health: ResourceHealth = ResourceHealth.OPTIMAL


@dataclass
class InstanceSpec:
    """Specification of an instance type."""
    instance_type: str
    vcpu: int
    memory_gb: float
    network_performance: str
    storage_type: str
    generation: int  # 5, 6, 7 for m5, m6, m7
    hourly_cost: float


@dataclass
class RightsizingRecommendation:
    """Recommendation for rightsizing a resource."""
    recommendation_id: str
    resource_id: str
    resource_type: str

    # Current state
    current_instance: InstanceSpec
    current_utilization: UtilizationMetrics
    current_health: ResourceHealth

    # Recommendation
    action: RightsizingAction
    recommended_instance: InstanceSpec

    # Impact
    monthly_savings: float
    savings_percentage: float

    # Risk
    risk_level: RightsizingRisk

    # Context
    rationale: str

    # Fields with defaults must come last
    risk_factors: list[str] = field(default_factory=list)
    validation_steps: list[str] = field(default_factory=list)


@dataclass
class RightsizingAnalysis:
    """Complete rightsizing analysis for resources."""
    analysis_id: str
    generated_at: datetime
    
    # Summary
    total_resources_analyzed: int
    oversized_count: int
    undersized_count: int
    optimal_count: int
    
    # Recommendations
    recommendations: list[RightsizingRecommendation] = field(default_factory=list)
    
    # Savings
    total_monthly_savings: float = 0.0
    total_annual_savings: float = 0.0
    
    # By category
    savings_by_action: dict[str, float] = field(default_factory=dict)
    
    # Quick wins
    quick_wins: list[RightsizingRecommendation] = field(default_factory=list)


class RightsizingAnalyzer:
    """Analyzer for resource rightsizing recommendations.
    
    Provides:
    1. Utilization analysis based on CloudWatch metrics
    2. Instance type recommendations
    3. Cost savings calculation
    4. Risk assessment
    5. Workload-aware sizing during code generation
    """
    
    # Instance specifications (subset for common types)
    INSTANCE_SPECS = {
        # T3 family
        "t3.micro": InstanceSpec("t3.micro", 2, 1.0, "Low", "EBS", 3, 0.0104),
        "t3.small": InstanceSpec("t3.small", 2, 2.0, "Low", "EBS", 3, 0.0208),
        "t3.medium": InstanceSpec("t3.medium", 2, 4.0, "Low", "EBS", 3, 0.0416),
        "t3.large": InstanceSpec("t3.large", 2, 8.0, "Low", "EBS", 3, 0.0832),
        "t3.xlarge": InstanceSpec("t3.xlarge", 4, 16.0, "Moderate", "EBS", 3, 0.1664),
        # M5 family
        "m5.large": InstanceSpec("m5.large", 2, 8.0, "Up to 10 Gbps", "EBS", 5, 0.096),
        "m5.xlarge": InstanceSpec("m5.xlarge", 4, 16.0, "Up to 10 Gbps", "EBS", 5, 0.192),
        "m5.2xlarge": InstanceSpec("m5.2xlarge", 8, 32.0, "Up to 10 Gbps", "EBS", 5, 0.384),
        "m5.4xlarge": InstanceSpec("m5.4xlarge", 16, 64.0, "Up to 10 Gbps", "EBS", 5, 0.768),
        # M6i family (newer generation)
        "m6i.large": InstanceSpec("m6i.large", 2, 8.0, "Up to 12.5 Gbps", "EBS", 6, 0.096),
        "m6i.xlarge": InstanceSpec("m6i.xlarge", 4, 16.0, "Up to 12.5 Gbps", "EBS", 6, 0.192),
        "m6i.2xlarge": InstanceSpec("m6i.2xlarge", 8, 32.0, "Up to 12.5 Gbps", "EBS", 6, 0.384),
        # C5 family (compute optimized)
        "c5.large": InstanceSpec("c5.large", 2, 4.0, "Up to 10 Gbps", "EBS", 5, 0.085),
        "c5.xlarge": InstanceSpec("c5.xlarge", 4, 8.0, "Up to 10 Gbps", "EBS", 5, 0.17),
        "c5.2xlarge": InstanceSpec("c5.2xlarge", 8, 16.0, "Up to 10 Gbps", "EBS", 5, 0.34),
        # R5 family (memory optimized)
        "r5.large": InstanceSpec("r5.large", 2, 16.0, "Up to 10 Gbps", "EBS", 5, 0.126),
        "r5.xlarge": InstanceSpec("r5.xlarge", 4, 32.0, "Up to 10 Gbps", "EBS", 5, 0.252),
        "r5.2xlarge": InstanceSpec("r5.2xlarge", 8, 64.0, "Up to 10 Gbps", "EBS", 5, 0.504),
    }

    # Utilization thresholds
    OVERSIZED_THRESHOLD = 20.0  # <20% = oversized
    UNDERUTILIZED_THRESHOLD = 40.0  # 20-40% = underutilized
    OPTIMAL_LOWER = 40.0
    OPTIMAL_UPPER = 80.0
    CONSTRAINED_THRESHOLD = 90.0  # 80-90% = constrained, >90% = critical

    # Size ordering within families
    SIZE_ORDER = ["nano", "micro", "small", "medium", "large", "xlarge", "2xlarge", "4xlarge", "8xlarge", "12xlarge", "16xlarge", "24xlarge"]

    def __init__(self):
        """Initialize the rightsizing analyzer."""
        pass

    def analyze_utilization(
        self,
        cpu_avg: float,
        cpu_max: float,
        memory_avg: float = 0.0,
        memory_max: float = 0.0,
    ) -> UtilizationMetrics:
        """Analyze utilization metrics to determine health.

        Args:
            cpu_avg: Average CPU utilization (0-100)
            cpu_max: Maximum CPU utilization
            memory_avg: Average memory utilization
            memory_max: Maximum memory utilization

        Returns:
            UtilizationMetrics with health status
        """
        cpu_health = self._get_health_status(cpu_avg, cpu_max)
        memory_health = self._get_health_status(memory_avg, memory_max) if memory_avg > 0 else ResourceHealth.OPTIMAL

        return UtilizationMetrics(
            cpu_avg=cpu_avg,
            cpu_max=cpu_max,
            memory_avg=memory_avg,
            memory_max=memory_max,
            cpu_health=cpu_health,
            memory_health=memory_health,
        )

    def _get_health_status(self, avg: float, max_val: float) -> ResourceHealth:
        """Determine health status from utilization."""
        # Use the higher of avg and weighted max for decision
        effective = max(avg, max_val * 0.7)  # 70% weight to max

        if effective < self.OVERSIZED_THRESHOLD:
            return ResourceHealth.OVERSIZED
        elif effective < self.UNDERUTILIZED_THRESHOLD:
            return ResourceHealth.UNDERUTILIZED
        elif effective < self.OPTIMAL_UPPER:
            return ResourceHealth.OPTIMAL
        elif effective < self.CONSTRAINED_THRESHOLD:
            return ResourceHealth.CONSTRAINED
        return ResourceHealth.CRITICAL

    def get_rightsizing_recommendation(
        self,
        resource_id: str,
        current_instance_type: str,
        utilization: UtilizationMetrics,
        monthly_hours: float = 730.0,
    ) -> RightsizingRecommendation | None:
        """Get rightsizing recommendation for a resource.

        Args:
            resource_id: Resource identifier
            current_instance_type: Current instance type
            utilization: Utilization metrics
            monthly_hours: Hours running per month

        Returns:
            RightsizingRecommendation or None if optimal
        """
        current_spec = self.INSTANCE_SPECS.get(current_instance_type)
        if not current_spec:
            # Create estimated spec
            current_spec = self._estimate_instance_spec(current_instance_type)

        # Determine overall health
        overall_health = self._get_overall_health(utilization)

        # Determine action
        action, target_spec = self._determine_action(
            current_spec, utilization, overall_health
        )

        if action == RightsizingAction.OPTIMAL:
            return None

        # Calculate savings
        current_monthly = current_spec.hourly_cost * monthly_hours
        target_monthly = target_spec.hourly_cost * monthly_hours
        savings = current_monthly - target_monthly
        savings_pct = (savings / current_monthly * 100) if current_monthly > 0 else 0

        # Assess risk
        risk, risk_factors = self._assess_risk(action, utilization, current_spec, target_spec)

        return RightsizingRecommendation(
            recommendation_id=str(uuid.uuid4()),
            resource_id=resource_id,
            resource_type="EC2",
            current_instance=current_spec,
            current_utilization=utilization,
            current_health=overall_health,
            action=action,
            recommended_instance=target_spec,
            monthly_savings=savings,
            savings_percentage=savings_pct,
            risk_level=risk,
            risk_factors=risk_factors,
            rationale=self._generate_rationale(action, current_spec, target_spec, utilization),
            validation_steps=self._get_validation_steps(action),
        )

    def recommend_initial_size(
        self,
        workload_description: str,
        expected_cpu_load: str = "medium",
        expected_memory_gb: float = 4.0,
        needs_high_network: bool = False,
        is_production: bool = False,
    ) -> InstanceSpec:
        """Recommend initial instance size for a new workload.

        Used during code generation to suggest appropriate sizing.

        Args:
            workload_description: Description of workload
            expected_cpu_load: "low", "medium", "high"
            expected_memory_gb: Expected memory requirement
            needs_high_network: Whether high network is needed
            is_production: Whether this is production

        Returns:
            Recommended InstanceSpec
        """
        # Determine family based on workload
        family = self._determine_family(
            workload_description, expected_cpu_load, expected_memory_gb
        )

        # Determine size
        size = self._determine_size(
            expected_cpu_load, expected_memory_gb, is_production
        )

        instance_type = f"{family}.{size}"

        # Return spec if known, otherwise estimate
        return self.INSTANCE_SPECS.get(
            instance_type,
            self._estimate_instance_spec(instance_type)
        )

    def analyze_resources(
        self,
        resources: list[dict[str, Any]],
    ) -> RightsizingAnalysis:
        """Analyze multiple resources for rightsizing.

        Args:
            resources: List of dicts with resource_id, instance_type, and utilization

        Returns:
            RightsizingAnalysis with all recommendations
        """
        recommendations = []
        oversized = 0
        undersized = 0
        optimal = 0

        for resource in resources:
            utilization = UtilizationMetrics(
                cpu_avg=resource.get("cpu_avg", 50),
                cpu_max=resource.get("cpu_max", 70),
                memory_avg=resource.get("memory_avg", 0),
                memory_max=resource.get("memory_max", 0),
            )
            utilization.cpu_health = self._get_health_status(utilization.cpu_avg, utilization.cpu_max)
            utilization.memory_health = self._get_health_status(utilization.memory_avg, utilization.memory_max)

            rec = self.get_rightsizing_recommendation(
                resource_id=resource.get("resource_id", "unknown"),
                current_instance_type=resource.get("instance_type", "m5.large"),
                utilization=utilization,
            )

            if rec:
                recommendations.append(rec)
                if rec.action == RightsizingAction.DOWNSIZE:
                    oversized += 1
                elif rec.action == RightsizingAction.UPSIZE:
                    undersized += 1
            else:
                optimal += 1

        # Calculate totals
        total_monthly = sum(r.monthly_savings for r in recommendations)

        # Identify quick wins (low risk, high savings)
        quick_wins = [
            r for r in recommendations
            if r.risk_level == RightsizingRisk.LOW and r.monthly_savings > 50
        ]
        quick_wins.sort(key=lambda r: r.monthly_savings, reverse=True)

        # Savings by action
        savings_by_action: dict[str, float] = {}
        for rec in recommendations:
            action = rec.action.value
            savings_by_action[action] = savings_by_action.get(action, 0) + rec.monthly_savings

        return RightsizingAnalysis(
            analysis_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            total_resources_analyzed=len(resources),
            oversized_count=oversized,
            undersized_count=undersized,
            optimal_count=optimal,
            recommendations=recommendations,
            total_monthly_savings=total_monthly,
            total_annual_savings=total_monthly * 12,
            savings_by_action=savings_by_action,
            quick_wins=quick_wins[:5],
        )

    def _get_overall_health(self, utilization: UtilizationMetrics) -> ResourceHealth:
        """Get overall health considering CPU and memory."""
        # CPU is primary, memory secondary
        if utilization.memory_avg > 0:
            # Both available - use most constrained
            cpu_rank = list(ResourceHealth).index(utilization.cpu_health)
            mem_rank = list(ResourceHealth).index(utilization.memory_health)
            return list(ResourceHealth)[max(cpu_rank, mem_rank)]
        return utilization.cpu_health

    def _determine_action(
        self,
        current: InstanceSpec,
        utilization: UtilizationMetrics,
        health: ResourceHealth,
    ) -> tuple[RightsizingAction, InstanceSpec]:
        """Determine rightsizing action and target instance."""
        family = self._get_family(current.instance_type)
        current_size = self._get_size(current.instance_type)

        if health in [ResourceHealth.OVERSIZED, ResourceHealth.UNDERUTILIZED]:
            # Downsize
            target_size = self._get_smaller_size(current_size)
            if target_size:
                target_type = f"{family}.{target_size}"
                target = self.INSTANCE_SPECS.get(target_type)
                if target:
                    return RightsizingAction.DOWNSIZE, target

        elif health in [ResourceHealth.CONSTRAINED, ResourceHealth.CRITICAL]:
            # Upsize
            target_size = self._get_larger_size(current_size)
            if target_size:
                target_type = f"{family}.{target_size}"
                target = self.INSTANCE_SPECS.get(target_type)
                if target:
                    return RightsizingAction.UPSIZE, target

        # Check if modernization makes sense
        if current.generation < 6:
            modern_family = self._get_modern_family(family)
            modern_type = f"{modern_family}.{current_size}"
            modern = self.INSTANCE_SPECS.get(modern_type)
            if modern and modern.hourly_cost <= current.hourly_cost:
                return RightsizingAction.MODERNIZE, modern

        return RightsizingAction.OPTIMAL, current

    def _get_family(self, instance_type: str) -> str:
        """Extract family from instance type."""
        return instance_type.split(".")[0]

    def _get_size(self, instance_type: str) -> str:
        """Extract size from instance type."""
        parts = instance_type.split(".")
        return parts[1] if len(parts) > 1 else "large"

    def _get_smaller_size(self, current_size: str) -> str | None:
        """Get next smaller size."""
        if current_size in self.SIZE_ORDER:
            idx = self.SIZE_ORDER.index(current_size)
            if idx > 0:
                return self.SIZE_ORDER[idx - 1]
        return None

    def _get_larger_size(self, current_size: str) -> str | None:
        """Get next larger size."""
        if current_size in self.SIZE_ORDER:
            idx = self.SIZE_ORDER.index(current_size)
            if idx < len(self.SIZE_ORDER) - 1:
                return self.SIZE_ORDER[idx + 1]
        return None

    def _get_modern_family(self, family: str) -> str:
        """Get modern equivalent of instance family."""
        modernization = {
            "m4": "m6i",
            "m5": "m6i",
            "c4": "c6i",
            "c5": "c6i",
            "r4": "r6i",
            "r5": "r6i",
            "t2": "t3",
        }
        return modernization.get(family, family)

    def _estimate_instance_spec(self, instance_type: str) -> InstanceSpec:
        """Estimate spec for unknown instance type."""
        family = self._get_family(instance_type)
        size = self._get_size(instance_type)

        # Base estimates
        size_multipliers = {
            "nano": (0.5, 0.5),
            "micro": (1, 1),
            "small": (1, 2),
            "medium": (2, 4),
            "large": (2, 8),
            "xlarge": (4, 16),
            "2xlarge": (8, 32),
            "4xlarge": (16, 64),
        }

        vcpu, mem = size_multipliers.get(size, (2, 8))

        # Estimate cost based on vcpu
        cost = vcpu * 0.048  # ~$0.048 per vCPU hour for general purpose

        return InstanceSpec(
            instance_type=instance_type,
            vcpu=vcpu,
            memory_gb=mem,
            network_performance="Moderate",
            storage_type="EBS",
            generation=5,
            hourly_cost=cost,
        )

    def _assess_risk(
        self,
        action: RightsizingAction,
        utilization: UtilizationMetrics,
        current: InstanceSpec,
        target: InstanceSpec,
    ) -> tuple[RightsizingRisk, list[str]]:
        """Assess risk of rightsizing change."""
        factors = []
        risk = RightsizingRisk.LOW

        if action == RightsizingAction.DOWNSIZE:
            # Risk factors for downsizing
            if utilization.cpu_max > 60:
                factors.append(f"CPU peaks at {utilization.cpu_max:.0f}% - may hit limits")
                risk = RightsizingRisk.MEDIUM

            if utilization.memory_max > 70:
                factors.append(f"Memory peaks at {utilization.memory_max:.0f}% - monitor closely")
                risk = RightsizingRisk.MEDIUM

            size_diff = current.vcpu - target.vcpu
            if size_diff > 2:
                factors.append(f"Large change ({size_diff} vCPU reduction)")
                risk = RightsizingRisk.HIGH

        elif action == RightsizingAction.UPSIZE:
            # Lower risk for upsizing
            factors.append("Upsizing typically low risk")

        elif action == RightsizingAction.MODERNIZE:
            factors.append("Generation upgrade - test for compatibility")
            risk = RightsizingRisk.MEDIUM

        return risk, factors

    def _generate_rationale(
        self,
        action: RightsizingAction,
        current: InstanceSpec,
        target: InstanceSpec,
        utilization: UtilizationMetrics,
    ) -> str:
        """Generate human-readable rationale."""
        if action == RightsizingAction.DOWNSIZE:
            return (
                f"CPU utilization averaging {utilization.cpu_avg:.0f}% suggests "
                f"{current.instance_type} is oversized. {target.instance_type} "
                f"provides sufficient capacity while reducing costs."
            )
        elif action == RightsizingAction.UPSIZE:
            return (
                f"CPU utilization at {utilization.cpu_avg:.0f}% (peak {utilization.cpu_max:.0f}%) "
                f"indicates {current.instance_type} is constrained. "
                f"Upgrading to {target.instance_type} will improve performance."
            )
        elif action == RightsizingAction.MODERNIZE:
            return (
                f"{current.instance_type} is a previous generation. "
                f"Modernizing to {target.instance_type} provides better "
                f"performance at similar or lower cost."
            )
        return "Resource is optimally sized."

    def _get_validation_steps(self, action: RightsizingAction) -> list[str]:
        """Get validation steps for change."""
        steps = [
            "1. Review CloudWatch metrics for the last 14 days",
            "2. Check for scheduled jobs that may spike utilization",
            "3. Test in staging environment first",
        ]

        if action == RightsizingAction.DOWNSIZE:
            steps.append("4. Use EC2 instance size flexibility if using RIs")
            steps.append("5. Monitor for 48 hours after change")
        elif action == RightsizingAction.MODERNIZE:
            steps.append("4. Verify application compatibility with new instance family")
            steps.append("5. Check for driver/kernel requirements")

        return steps

    def _determine_family(
        self,
        workload_description: str,
        expected_cpu_load: str,
        expected_memory_gb: float,
    ) -> str:
        """Determine best instance family for workload."""
        desc_lower = workload_description.lower()

        # Memory intensive
        if expected_memory_gb > 32 or "cache" in desc_lower or "memory" in desc_lower:
            return "r5"

        # Compute intensive
        if expected_cpu_load == "high" or "compute" in desc_lower or "cpu" in desc_lower:
            return "c5"

        # Burstable (dev/test or low utilization)
        if expected_cpu_load == "low" or "dev" in desc_lower or "test" in desc_lower:
            return "t3"

        # General purpose (default)
        return "m5"

    def _determine_size(
        self,
        expected_cpu_load: str,
        expected_memory_gb: float,
        is_production: bool,
    ) -> str:
        """Determine instance size."""
        # Base on memory requirement
        if expected_memory_gb <= 2:
            size = "small"
        elif expected_memory_gb <= 4:
            size = "medium"
        elif expected_memory_gb <= 8:
            size = "large"
        elif expected_memory_gb <= 16:
            size = "xlarge"
        elif expected_memory_gb <= 32:
            size = "2xlarge"
        else:
            size = "4xlarge"

        # Adjust for CPU load
        if expected_cpu_load == "high":
            idx = self.SIZE_ORDER.index(size) if size in self.SIZE_ORDER else 4
            if idx < len(self.SIZE_ORDER) - 1:
                size = self.SIZE_ORDER[idx + 1]

        # Production buffer
        if is_production and size in ["small", "medium"]:
            idx = self.SIZE_ORDER.index(size)
            size = self.SIZE_ORDER[idx + 1]

        return size
