"""Efficiency Metrics Calculator.

Calculates cost efficiency ratios, benchmarks, and KPIs for infrastructure.
Provides actionable insights during code generation.

Industry Comparison:
- FinOps Foundation KPIs: Standard metrics
- CloudZero Unit Economics: Good but post-hoc
- WISTX: Real-time efficiency guidance during code generation
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any
from statistics import mean

from wistx_mcp.tools.lib.cost_intelligence.models import CostRecord

logger = logging.getLogger(__name__)


class EfficiencyKPI(str, Enum):
    """Standard FinOps efficiency KPIs."""
    # Commitment KPIs
    RESERVATION_COVERAGE = "reservation_coverage"
    RESERVATION_UTILIZATION = "reservation_utilization"
    SAVINGS_PLAN_COVERAGE = "savings_plan_coverage"
    
    # Usage KPIs
    SPOT_UTILIZATION = "spot_utilization"
    IDLE_RESOURCES = "idle_resources"
    RIGHTSIZING_POTENTIAL = "rightsizing_potential"
    
    # Allocation KPIs
    TAGGING_COMPLIANCE = "tagging_compliance"
    COST_ALLOCATION_RATE = "cost_allocation_rate"
    
    # Trend KPIs
    COST_PER_UNIT = "cost_per_unit"
    COST_VARIANCE = "cost_variance"


class HealthStatus(str, Enum):
    """Health status for metrics."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class KPIResult:
    """Result for a single KPI calculation."""
    kpi: EfficiencyKPI
    name: str
    value: float
    unit: str  # %, $, ratio
    
    # Benchmarks
    target: float
    industry_average: float
    
    # Status
    status: HealthStatus
    vs_target: float  # % difference from target
    vs_industry: float  # % difference from industry avg
    
    # Actionable insight
    insight: str
    recommendation: str | None = None
    
    # Trend
    trend: str | None = None  # improving, stable, declining
    previous_value: float | None = None


@dataclass
class EfficiencyReport:
    """Comprehensive efficiency report."""
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    
    # Overall score
    overall_efficiency_score: float  # 0-100
    overall_status: HealthStatus
    
    # KPIs
    kpis: list[KPIResult] = field(default_factory=list)
    
    # Top issues
    critical_issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    
    # Recommendations (prioritized)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    
    # Potential savings
    total_savings_potential: float = 0.0
    quick_wins: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class CostBenchmark:
    """Benchmark data for a resource type."""
    resource_type: str
    
    # Cost benchmarks (monthly)
    p50_cost: float  # Median
    p75_cost: float
    p90_cost: float
    
    # Efficiency benchmarks
    target_utilization: float
    typical_rightsizing_savings: float
    
    # Recommendations
    recommended_instance_types: list[str] = field(default_factory=list)
    cost_optimization_tips: list[str] = field(default_factory=list)


class EfficiencyMetricsCalculator:
    """Calculator for FinOps efficiency metrics and benchmarks.
    
    Provides:
    1. Standard FinOps KPI calculations
    2. Industry benchmark comparisons
    3. Actionable recommendations
    4. Efficiency scoring
    """
    
    # Industry benchmarks (from FinOps Foundation and industry research)
    INDUSTRY_BENCHMARKS = {
        EfficiencyKPI.RESERVATION_COVERAGE: {"target": 70, "industry_avg": 55},
        EfficiencyKPI.RESERVATION_UTILIZATION: {"target": 85, "industry_avg": 72},
        EfficiencyKPI.SAVINGS_PLAN_COVERAGE: {"target": 60, "industry_avg": 45},
        EfficiencyKPI.SPOT_UTILIZATION: {"target": 30, "industry_avg": 15},
        EfficiencyKPI.IDLE_RESOURCES: {"target": 5, "industry_avg": 15},
        EfficiencyKPI.RIGHTSIZING_POTENTIAL: {"target": 10, "industry_avg": 25},
        EfficiencyKPI.TAGGING_COMPLIANCE: {"target": 90, "industry_avg": 65},
        EfficiencyKPI.COST_ALLOCATION_RATE: {"target": 95, "industry_avg": 75},
        EfficiencyKPI.COST_VARIANCE: {"target": 5, "industry_avg": 15},
    }
    
    # Resource type benchmarks
    RESOURCE_BENCHMARKS = {
        "ec2": CostBenchmark(
            resource_type="ec2",
            p50_cost=150,
            p75_cost=350,
            p90_cost=800,
            target_utilization=0.65,
            typical_rightsizing_savings=0.25,
            recommended_instance_types=["t3", "t3a", "m6i", "c6i"],
            cost_optimization_tips=[
                "Use spot instances for fault-tolerant workloads",
                "Consider graviton instances for 20% savings",
                "Right-size based on actual CPU/memory usage",
            ],
        ),
        "rds": CostBenchmark(
            resource_type="rds",
            p50_cost=200,
            p75_cost=500,
            p90_cost=1500,
            target_utilization=0.70,
            typical_rightsizing_savings=0.20,
            recommended_instance_types=["db.t3", "db.r6g", "db.m6g"],
            cost_optimization_tips=[
                "Use reserved instances for production databases",
                "Consider Aurora Serverless for variable workloads",
                "Enable storage autoscaling to avoid over-provisioning",
            ],
        ),
        "lambda": CostBenchmark(
            resource_type="lambda",
            p50_cost=10,
            p75_cost=50,
            p90_cost=200,
            target_utilization=0.80,
            typical_rightsizing_savings=0.15,
            recommended_instance_types=[],
            cost_optimization_tips=[
                "Right-size memory allocation based on actual usage",
                "Use provisioned concurrency only when needed",
                "Consider ARM architecture for cost savings",
            ],
        ),
        "s3": CostBenchmark(
            resource_type="s3",
            p50_cost=25,
            p75_cost=100,
            p90_cost=500,
            target_utilization=0.90,
            typical_rightsizing_savings=0.30,
            recommended_instance_types=[],
            cost_optimization_tips=[
                "Enable lifecycle policies to transition to cheaper tiers",
                "Use Intelligent Tiering for unknown access patterns",
                "Enable S3 Analytics to identify optimization opportunities",
            ],
        ),
    }

    def __init__(self):
        """Initialize the calculator."""
        pass

    def calculate_all_kpis(
        self,
        cost_records: list[CostRecord],
        reservation_data: dict[str, Any] | None = None,
        tagging_coverage: float | None = None,
    ) -> list[KPIResult]:
        """Calculate all efficiency KPIs.

        Args:
            cost_records: Cost records for analysis
            reservation_data: Optional reservation/savings plan data
            tagging_coverage: Pre-calculated tagging coverage %

        Returns:
            List of KPI results
        """
        kpis = []

        # Tagging compliance
        if tagging_coverage is not None:
            kpis.append(self._calculate_tagging_kpi(tagging_coverage))
        else:
            # Calculate from records
            tagged = sum(1 for r in cost_records if r.tags and len(r.tags) >= 2)
            coverage = (tagged / len(cost_records) * 100) if cost_records else 0
            kpis.append(self._calculate_tagging_kpi(coverage))

        # Cost allocation rate
        allocated = sum(
            r.billed_cost for r in cost_records
            if r.tags and any(
                k.lower() in ["team", "project", "costcenter"]
                for k in r.tags.keys()
            )
        )
        total = sum(r.billed_cost for r in cost_records)
        allocation_rate = (allocated / total * 100) if total > 0 else 0
        kpis.append(self._calculate_allocation_kpi(allocation_rate))

        # Idle resources (estimate based on low-cost resources)
        avg_cost = mean([r.billed_cost for r in cost_records]) if cost_records else 0
        idle_count = sum(1 for r in cost_records if r.billed_cost < avg_cost * 0.1)
        idle_pct = (idle_count / len(cost_records) * 100) if cost_records else 0
        kpis.append(self._calculate_idle_kpi(idle_pct))

        # Cost variance
        if len(cost_records) >= 14:
            variance = self._calculate_cost_variance(cost_records)
            kpis.append(self._calculate_variance_kpi(variance))

        # Reservation coverage (if data provided)
        if reservation_data:
            coverage = reservation_data.get("coverage_percentage", 0)
            utilization = reservation_data.get("utilization_percentage", 0)
            kpis.append(self._calculate_reservation_coverage_kpi(coverage))
            kpis.append(self._calculate_reservation_utilization_kpi(utilization))

        return kpis

    def generate_efficiency_report(
        self,
        cost_records: list[CostRecord],
        reservation_data: dict[str, Any] | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> EfficiencyReport:
        """Generate comprehensive efficiency report.

        Args:
            cost_records: Cost records for analysis
            reservation_data: Optional reservation data
            period_start: Report period start
            period_end: Report period end

        Returns:
            Complete efficiency report
        """
        now = datetime.now(timezone.utc)
        period_start = period_start or now - timedelta(days=30)
        period_end = period_end or now

        # Calculate all KPIs
        kpis = self.calculate_all_kpis(cost_records, reservation_data)

        # Calculate overall score
        kpi_scores = []
        for kpi in kpis:
            benchmark = self.INDUSTRY_BENCHMARKS.get(kpi.kpi, {})
            target = benchmark.get("target", 50)

            # Lower is better for some KPIs
            if kpi.kpi in [EfficiencyKPI.IDLE_RESOURCES, EfficiencyKPI.RIGHTSIZING_POTENTIAL, EfficiencyKPI.COST_VARIANCE]:
                score = max(0, 100 - (kpi.value / target * 100)) if target > 0 else 50
            else:
                score = min(100, kpi.value / target * 100) if target > 0 else 50

            kpi_scores.append(score)

        overall_score = mean(kpi_scores) if kpi_scores else 50

        # Determine overall status
        if overall_score >= 80:
            overall_status = HealthStatus.HEALTHY
        elif overall_score >= 60:
            overall_status = HealthStatus.WARNING
        else:
            overall_status = HealthStatus.CRITICAL

        # Identify issues
        critical_issues = [
            kpi.insight for kpi in kpis
            if kpi.status == HealthStatus.CRITICAL
        ]
        warnings = [
            kpi.insight for kpi in kpis
            if kpi.status == HealthStatus.WARNING
        ]

        # Generate recommendations
        recommendations = []
        for kpi in kpis:
            if kpi.recommendation and kpi.status != HealthStatus.HEALTHY:
                recommendations.append({
                    "kpi": kpi.kpi.value,
                    "priority": "high" if kpi.status == HealthStatus.CRITICAL else "medium",
                    "recommendation": kpi.recommendation,
                    "potential_improvement": f"{abs(kpi.vs_target):.1f}% improvement possible",
                })

        # Sort by priority
        recommendations.sort(key=lambda x: 0 if x["priority"] == "high" else 1)

        # Calculate savings potential
        total_cost = sum(r.billed_cost for r in cost_records)
        savings_potential = self._estimate_savings_potential(kpis, total_cost)

        # Identify quick wins
        quick_wins = self._identify_quick_wins(kpis, total_cost)

        return EfficiencyReport(
            generated_at=now,
            period_start=period_start,
            period_end=period_end,
            overall_efficiency_score=overall_score,
            overall_status=overall_status,
            kpis=kpis,
            critical_issues=critical_issues,
            warnings=warnings,
            recommendations=recommendations,
            total_savings_potential=savings_potential,
            quick_wins=quick_wins,
        )

    def get_resource_benchmark(
        self,
        resource_type: str,
        current_cost: float,
    ) -> dict[str, Any]:
        """Get benchmark comparison for a resource.

        Args:
            resource_type: Type of resource (ec2, rds, etc.)
            current_cost: Current monthly cost

        Returns:
            Benchmark comparison with recommendations
        """
        rt_lower = resource_type.lower()

        # Find matching benchmark
        benchmark = None
        for key, bm in self.RESOURCE_BENCHMARKS.items():
            if key in rt_lower:
                benchmark = bm
                break

        if not benchmark:
            return {
                "resource_type": resource_type,
                "benchmark_available": False,
                "message": "No benchmark data available for this resource type",
            }

        # Determine percentile
        if current_cost <= benchmark.p50_cost:
            percentile = "below_median"
            status = "excellent"
        elif current_cost <= benchmark.p75_cost:
            percentile = "50th-75th"
            status = "good"
        elif current_cost <= benchmark.p90_cost:
            percentile = "75th-90th"
            status = "review_recommended"
        else:
            percentile = "above_90th"
            status = "optimization_needed"

        return {
            "resource_type": resource_type,
            "benchmark_available": True,
            "current_cost": current_cost,
            "benchmarks": {
                "p50": benchmark.p50_cost,
                "p75": benchmark.p75_cost,
                "p90": benchmark.p90_cost,
            },
            "percentile": percentile,
            "status": status,
            "target_utilization": benchmark.target_utilization,
            "typical_savings_potential": f"{benchmark.typical_rightsizing_savings * 100:.0f}%",
            "recommended_types": benchmark.recommended_instance_types,
            "optimization_tips": benchmark.cost_optimization_tips,
        }

    def _calculate_tagging_kpi(self, coverage: float) -> KPIResult:
        """Calculate tagging compliance KPI."""
        benchmark = self.INDUSTRY_BENCHMARKS[EfficiencyKPI.TAGGING_COMPLIANCE]
        target = benchmark["target"]
        industry = benchmark["industry_avg"]

        if coverage >= target:
            status = HealthStatus.HEALTHY
        elif coverage >= industry:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        return KPIResult(
            kpi=EfficiencyKPI.TAGGING_COMPLIANCE,
            name="Tagging Compliance",
            value=coverage,
            unit="%",
            target=target,
            industry_average=industry,
            status=status,
            vs_target=coverage - target,
            vs_industry=coverage - industry,
            insight=f"Tagging coverage is {coverage:.1f}% (target: {target}%)",
            recommendation=(
                "Implement mandatory tagging policy with Team, Environment, and Project tags"
                if status != HealthStatus.HEALTHY else None
            ),
        )

    def _calculate_allocation_kpi(self, rate: float) -> KPIResult:
        """Calculate cost allocation rate KPI."""
        benchmark = self.INDUSTRY_BENCHMARKS[EfficiencyKPI.COST_ALLOCATION_RATE]
        target = benchmark["target"]
        industry = benchmark["industry_avg"]

        if rate >= target:
            status = HealthStatus.HEALTHY
        elif rate >= industry:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        return KPIResult(
            kpi=EfficiencyKPI.COST_ALLOCATION_RATE,
            name="Cost Allocation Rate",
            value=rate,
            unit="%",
            target=target,
            industry_average=industry,
            status=status,
            vs_target=rate - target,
            vs_industry=rate - industry,
            insight=f"Cost allocation rate is {rate:.1f}% (target: {target}%)",
            recommendation=(
                "Add allocation tags (Team, Project, CostCenter) to unallocated resources"
                if status != HealthStatus.HEALTHY else None
            ),
        )

    def _calculate_idle_kpi(self, idle_pct: float) -> KPIResult:
        """Calculate idle resources KPI."""
        benchmark = self.INDUSTRY_BENCHMARKS[EfficiencyKPI.IDLE_RESOURCES]
        target = benchmark["target"]
        industry = benchmark["industry_avg"]

        # Lower is better
        if idle_pct <= target:
            status = HealthStatus.HEALTHY
        elif idle_pct <= industry:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        return KPIResult(
            kpi=EfficiencyKPI.IDLE_RESOURCES,
            name="Idle Resources",
            value=idle_pct,
            unit="%",
            target=target,
            industry_average=industry,
            status=status,
            vs_target=idle_pct - target,
            vs_industry=idle_pct - industry,
            insight=f"Estimated {idle_pct:.1f}% idle resources (target: <{target}%)",
            recommendation=(
                "Review and terminate or downsize idle resources"
                if status != HealthStatus.HEALTHY else None
            ),
        )

    def _calculate_variance_kpi(self, variance: float) -> KPIResult:
        """Calculate cost variance KPI."""
        benchmark = self.INDUSTRY_BENCHMARKS[EfficiencyKPI.COST_VARIANCE]
        target = benchmark["target"]
        industry = benchmark["industry_avg"]

        if variance <= target:
            status = HealthStatus.HEALTHY
        elif variance <= industry:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        return KPIResult(
            kpi=EfficiencyKPI.COST_VARIANCE,
            name="Cost Variance",
            value=variance,
            unit="%",
            target=target,
            industry_average=industry,
            status=status,
            vs_target=variance - target,
            vs_industry=variance - industry,
            insight=f"Cost variance is {variance:.1f}% (target: <{target}%)",
            recommendation=(
                "Investigate cost fluctuations and implement budget alerts"
                if status != HealthStatus.HEALTHY else None
            ),
        )

    def _calculate_reservation_coverage_kpi(self, coverage: float) -> KPIResult:
        """Calculate reservation coverage KPI."""
        benchmark = self.INDUSTRY_BENCHMARKS[EfficiencyKPI.RESERVATION_COVERAGE]
        target = benchmark["target"]
        industry = benchmark["industry_avg"]

        if coverage >= target:
            status = HealthStatus.HEALTHY
        elif coverage >= industry:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        return KPIResult(
            kpi=EfficiencyKPI.RESERVATION_COVERAGE,
            name="Reservation Coverage",
            value=coverage,
            unit="%",
            target=target,
            industry_average=industry,
            status=status,
            vs_target=coverage - target,
            vs_industry=coverage - industry,
            insight=f"Reservation coverage is {coverage:.1f}% (target: {target}%)",
            recommendation=(
                "Purchase Reserved Instances or Savings Plans for stable workloads"
                if status != HealthStatus.HEALTHY else None
            ),
        )

    def _calculate_reservation_utilization_kpi(self, utilization: float) -> KPIResult:
        """Calculate reservation utilization KPI."""
        benchmark = self.INDUSTRY_BENCHMARKS[EfficiencyKPI.RESERVATION_UTILIZATION]
        target = benchmark["target"]
        industry = benchmark["industry_avg"]

        if utilization >= target:
            status = HealthStatus.HEALTHY
        elif utilization >= industry:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.CRITICAL

        return KPIResult(
            kpi=EfficiencyKPI.RESERVATION_UTILIZATION,
            name="Reservation Utilization",
            value=utilization,
            unit="%",
            target=target,
            industry_average=industry,
            status=status,
            vs_target=utilization - target,
            vs_industry=utilization - industry,
            insight=f"Reservation utilization is {utilization:.1f}% (target: {target}%)",
            recommendation=(
                "Review and sell unused reservations or modify to match workloads"
                if status != HealthStatus.HEALTHY else None
            ),
        )

    def _calculate_cost_variance(self, cost_records: list[CostRecord]) -> float:
        """Calculate cost variance from records."""
        # Group by day
        daily: dict[str, float] = {}
        for record in cost_records:
            date_key = record.billing_period_start.strftime("%Y-%m-%d")
            daily[date_key] = daily.get(date_key, 0) + record.billed_cost

        if len(daily) < 2:
            return 0.0

        costs = list(daily.values())
        avg = mean(costs)

        if avg == 0:
            return 0.0

        # Calculate coefficient of variation
        variance = sum((c - avg) ** 2 for c in costs) / len(costs)
        std_dev = variance ** 0.5

        return (std_dev / avg) * 100

    def _estimate_savings_potential(
        self,
        kpis: list[KPIResult],
        total_cost: float,
    ) -> float:
        """Estimate total savings potential from KPIs."""
        savings = 0.0

        for kpi in kpis:
            if kpi.status == HealthStatus.CRITICAL:
                # Estimate 15% savings for critical issues
                savings += total_cost * 0.15 / len(kpis)
            elif kpi.status == HealthStatus.WARNING:
                # Estimate 8% savings for warnings
                savings += total_cost * 0.08 / len(kpis)

        return savings

    def _identify_quick_wins(
        self,
        kpis: list[KPIResult],
        total_cost: float,
    ) -> list[dict[str, Any]]:
        """Identify quick win optimizations."""
        quick_wins = []

        for kpi in kpis:
            if kpi.status == HealthStatus.CRITICAL:
                estimated_savings = total_cost * 0.10  # 10% of total

                quick_wins.append({
                    "kpi": kpi.name,
                    "action": kpi.recommendation,
                    "estimated_savings": estimated_savings,
                    "effort": "low" if kpi.kpi in [
                        EfficiencyKPI.TAGGING_COMPLIANCE,
                        EfficiencyKPI.IDLE_RESOURCES,
                    ] else "medium",
                    "time_to_value": "1-2 weeks",
                })

        return quick_wins[:3]  # Top 3 quick wins
