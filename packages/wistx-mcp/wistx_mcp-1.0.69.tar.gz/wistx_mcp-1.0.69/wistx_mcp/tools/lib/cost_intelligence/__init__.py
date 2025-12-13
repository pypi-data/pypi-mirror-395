"""Cost Intelligence Module.

Provides intelligent cost analysis, forecasting, and optimization recommendations
for AI coding assistants during code generation.

This module exceeds industry standards by providing cost intelligence at code
generation time, not post-deployment dashboards.
"""

from wistx_mcp.tools.lib.cost_intelligence.models import (
    CostRecord,
    CostAnomaly,
    CostForecast,
    DailyForecast,
    OptimizationRecommendation,
    CostAlternative,
    ResourceCostBreakdown,
    BudgetStatus,
    UnitEconomics,
    CostContext,
    ReservationUtilization,
    RightsizingRecommendation,
    AnomalySeverity,
    RecommendationType,
    RecommendationStrength,
)

from wistx_mcp.tools.lib.cost_intelligence.cost_context_generator import (
    CostContextGenerator,
)
from wistx_mcp.tools.lib.cost_intelligence.anomaly_detector import (
    CostAnomalyDetector,
)
from wistx_mcp.tools.lib.cost_intelligence.cost_forecaster import (
    CostForecaster,
)
from wistx_mcp.tools.lib.cost_intelligence.unit_economics import (
    UnitEconomicsService,
    CostUnit,
    EfficiencyRating,
    CostPerUnit,
    TeamCostAllocation,
    EnvironmentCostBreakdown,
    DeploymentCost,
)
from wistx_mcp.tools.lib.cost_intelligence.cost_allocation import (
    CostAllocationEngine,
    AllocationStrategy,
    CostCategory,
    AllocationRule,
    AllocationResult,
    TargetAllocation,
    TaggingAnalysis,
)
from wistx_mcp.tools.lib.cost_intelligence.efficiency_metrics import (
    EfficiencyMetricsCalculator,
    EfficiencyKPI,
    HealthStatus,
    KPIResult,
    EfficiencyReport,
    CostBenchmark,
)
from wistx_mcp.tools.lib.cost_intelligence.commitment_optimizer import (
    CommitmentOptimizer,
    CommitmentType,
    PaymentOption,
    Term,
    CommitmentRisk,
    CoverageAnalysis,
    UtilizationAnalysis,
    CommitmentRecommendation,
    CommitmentPortfolio,
)
from wistx_mcp.tools.lib.cost_intelligence.spot_advisor import (
    SpotInstanceAdvisor,
    WorkloadType,
    SpotSuitability,
    InterruptionRisk,
    InstancePoolInfo,
    SpotRecommendation,
    SpotAnalysis,
)
from wistx_mcp.tools.lib.cost_intelligence.rightsizing_analyzer import (
    RightsizingAnalyzer,
    RightsizingAction,
    RightsizingRisk,
    ResourceHealth,
    UtilizationMetrics,
    InstanceSpec,
    RightsizingRecommendation as RightsizingRec,
    RightsizingAnalysis,
)
from wistx_mcp.tools.lib.cost_intelligence.optimization_orchestrator import (
    OptimizationOrchestrator,
    OptimizationCategory,
    OptimizationPriority,
    UnifiedRecommendation,
    OptimizationSummary,
)

__all__ = [
    # Models
    "CostRecord",
    "CostAnomaly",
    "CostForecast",
    "DailyForecast",
    "OptimizationRecommendation",
    "CostAlternative",
    "ResourceCostBreakdown",
    "BudgetStatus",
    "UnitEconomics",
    "CostContext",
    "ReservationUtilization",
    "RightsizingRecommendation",
    # Unit Economics Models
    "CostPerUnit",
    "TeamCostAllocation",
    "EnvironmentCostBreakdown",
    "DeploymentCost",
    # Allocation Models
    "AllocationRule",
    "AllocationResult",
    "TargetAllocation",
    "TaggingAnalysis",
    # Efficiency Models
    "KPIResult",
    "EfficiencyReport",
    "CostBenchmark",
    # Enums
    "AnomalySeverity",
    "RecommendationType",
    "RecommendationStrength",
    "CostUnit",
    "EfficiencyRating",
    "AllocationStrategy",
    "CostCategory",
    "EfficiencyKPI",
    "HealthStatus",
    # Services
    "CostContextGenerator",
    "CostAnomalyDetector",
    "CostForecaster",
    "UnitEconomicsService",
    "CostAllocationEngine",
    "EfficiencyMetricsCalculator",
    # Phase 3: Advanced Optimization
    # Commitment Optimizer
    "CommitmentOptimizer",
    "CommitmentType",
    "PaymentOption",
    "Term",
    "CommitmentRisk",
    "CoverageAnalysis",
    "UtilizationAnalysis",
    "CommitmentRecommendation",
    "CommitmentPortfolio",
    # Spot Instance Advisor
    "SpotInstanceAdvisor",
    "WorkloadType",
    "SpotSuitability",
    "InterruptionRisk",
    "InstancePoolInfo",
    "SpotRecommendation",
    "SpotAnalysis",
    # Rightsizing Analyzer
    "RightsizingAnalyzer",
    "RightsizingAction",
    "RightsizingRisk",
    "ResourceHealth",
    "UtilizationMetrics",
    "InstanceSpec",
    "RightsizingRec",
    "RightsizingAnalysis",
    # Optimization Orchestrator
    "OptimizationOrchestrator",
    "OptimizationCategory",
    "OptimizationPriority",
    "UnifiedRecommendation",
    "OptimizationSummary",
]

