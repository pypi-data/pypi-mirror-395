"""Cost Allocation Engine.

Provides tag-based cost allocation with intelligent shared cost distribution.
Supports multiple allocation strategies and showback/chargeback models.

Industry Comparison:
- CloudHealth: Good allocation but complex setup
- Finout: Strong virtual tagging
- WISTX: AI-assisted allocation during code generation
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from wistx_mcp.tools.lib.cost_intelligence.models import CostRecord

logger = logging.getLogger(__name__)


class AllocationStrategy(str, Enum):
    """Cost allocation strategies."""
    PROPORTIONAL = "proportional"  # Based on direct cost ratio
    EQUAL = "equal"  # Split equally
    USAGE_BASED = "usage_based"  # Based on usage metrics
    FIXED_PERCENTAGE = "fixed_percentage"  # Predefined percentages
    HEADCOUNT = "headcount"  # Based on team size


class CostCategory(str, Enum):
    """Categories for cost classification."""
    DIRECT = "direct"  # Directly attributable
    SHARED = "shared"  # Shared infrastructure
    PLATFORM = "platform"  # Platform/tooling costs
    UNALLOCATED = "unallocated"  # Cannot be attributed


@dataclass
class AllocationRule:
    """Rule for cost allocation."""
    rule_id: str
    name: str
    description: str
    
    # Matching criteria
    service_pattern: str | None = None  # Regex for service name
    tag_filters: dict[str, str] = field(default_factory=dict)
    resource_type_pattern: str | None = None
    
    # Allocation target
    target_dimension: str = "Team"  # Team, Project, CostCenter, etc.
    
    # Strategy
    strategy: AllocationStrategy = AllocationStrategy.PROPORTIONAL
    fixed_percentages: dict[str, float] | None = None  # For FIXED_PERCENTAGE
    
    # Priority (higher = processed first)
    priority: int = 0


@dataclass
class AllocationResult:
    """Result of cost allocation."""
    allocation_id: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    
    # Total costs
    total_cost: float
    direct_cost: float
    shared_cost: float
    unallocated_cost: float
    
    # Allocations by target (e.g., by team)
    allocations: dict[str, "TargetAllocation"] = field(default_factory=dict)
    
    # Unallocated breakdown
    unallocated_reasons: list[str] = field(default_factory=list)
    
    # Metadata
    rules_applied: list[str] = field(default_factory=list)
    allocation_quality_score: float = 0.0  # 0-100, based on tagging coverage


@dataclass
class TargetAllocation:
    """Allocation for a specific target (team, project, etc.)."""
    target_id: str
    target_name: str
    
    # Costs
    direct_cost: float
    allocated_shared_cost: float
    total_cost: float
    
    # Percentage of total
    percentage_of_total: float
    
    # Breakdown
    by_service: dict[str, float] = field(default_factory=dict)
    by_environment: dict[str, float] = field(default_factory=dict)
    by_category: dict[str, float] = field(default_factory=dict)
    
    # Trend
    vs_previous_period: float | None = None  # % change


@dataclass 
class TaggingAnalysis:
    """Analysis of cost tagging coverage."""
    total_resources: int
    tagged_resources: int
    tagging_coverage: float  # 0-100%
    
    # By tag key
    coverage_by_tag: dict[str, float] = field(default_factory=dict)
    
    # Recommendations
    missing_tags: list[str] = field(default_factory=list)
    inconsistent_values: dict[str, list[str]] = field(default_factory=dict)
    
    # Impact
    untagged_cost: float = 0.0
    untagged_percentage: float = 0.0


class CostAllocationEngine:
    """Engine for allocating costs to teams, projects, and cost centers.
    
    Supports:
    1. Tag-based allocation
    2. Shared cost distribution
    3. Virtual tagging (rule-based)
    4. Showback/chargeback reporting
    """
    
    # Default shared services that should be distributed
    DEFAULT_SHARED_SERVICES = [
        "networking",
        "vpc",
        "cloudtrail",
        "config",
        "guardduty",
        "securityhub",
        "waf",
        "route53",
        "cloudfront",  # Often shared
    ]
    
    # Default required tags for good allocation
    RECOMMENDED_TAGS = [
        "Team",
        "Environment",
        "Project",
        "CostCenter",
        "Owner",
    ]

    def __init__(
        self,
        shared_services: list[str] | None = None,
        required_tags: list[str] | None = None,
    ):
        """Initialize the allocation engine.

        Args:
            shared_services: Services to treat as shared costs
            required_tags: Tags required for full allocation
        """
        self.shared_services = shared_services or self.DEFAULT_SHARED_SERVICES
        self.required_tags = required_tags or self.RECOMMENDED_TAGS
        self._rules: list[AllocationRule] = []

    def add_rule(self, rule: AllocationRule) -> None:
        """Add an allocation rule."""
        self._rules.append(rule)
        # Keep sorted by priority (descending)
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    def allocate_costs(
        self,
        cost_records: list[CostRecord],
        target_dimension: str = "Team",
        strategy: AllocationStrategy = AllocationStrategy.PROPORTIONAL,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> AllocationResult:
        """Allocate costs to targets (teams, projects, etc.).

        Args:
            cost_records: Cost records to allocate
            target_dimension: Tag key for allocation target
            strategy: Strategy for shared cost distribution
            period_start: Start of allocation period
            period_end: End of allocation period

        Returns:
            AllocationResult with full breakdown
        """
        now = datetime.now(timezone.utc)
        period_start = period_start or now.replace(day=1)
        period_end = period_end or now

        # Categorize costs
        direct_records: dict[str, list[CostRecord]] = {}  # By target
        shared_records: list[CostRecord] = []
        unallocated_records: list[CostRecord] = []
        unallocated_reasons: list[str] = []

        for record in cost_records:
            category = self._categorize_record(record)

            if category == CostCategory.SHARED:
                shared_records.append(record)
            elif category == CostCategory.UNALLOCATED:
                unallocated_records.append(record)
                if record.resource_id:
                    unallocated_reasons.append(
                        f"Resource {record.resource_id}: missing '{target_dimension}' tag"
                    )
            else:
                # Direct cost - attribute to target
                target = self._get_target(record, target_dimension)
                if target:
                    if target not in direct_records:
                        direct_records[target] = []
                    direct_records[target].append(record)
                else:
                    unallocated_records.append(record)

        # Calculate totals
        total_direct = sum(
            sum(r.billed_cost for r in records)
            for records in direct_records.values()
        )
        total_shared = sum(r.billed_cost for r in shared_records)
        total_unallocated = sum(r.billed_cost for r in unallocated_records)
        total_cost = total_direct + total_shared + total_unallocated

        # Allocate shared costs
        allocations: dict[str, TargetAllocation] = {}

        for target, records in direct_records.items():
            direct_cost = sum(r.billed_cost for r in records)

            # Calculate shared allocation based on strategy
            if strategy == AllocationStrategy.PROPORTIONAL:
                share_ratio = direct_cost / total_direct if total_direct > 0 else 0
                shared_allocation = total_shared * share_ratio
            elif strategy == AllocationStrategy.EQUAL:
                shared_allocation = total_shared / len(direct_records) if direct_records else 0
            else:
                shared_allocation = total_shared / len(direct_records) if direct_records else 0

            # Build breakdowns
            by_service: dict[str, float] = {}
            by_environment: dict[str, float] = {}

            for record in records:
                svc = record.service_name or "unknown"
                by_service[svc] = by_service.get(svc, 0) + record.billed_cost

                env = self._get_tag(record, "Environment") or "untagged"
                by_environment[env] = by_environment.get(env, 0) + record.billed_cost

            total = direct_cost + shared_allocation

            allocations[target] = TargetAllocation(
                target_id=target.lower().replace(" ", "_"),
                target_name=target,
                direct_cost=direct_cost,
                allocated_shared_cost=shared_allocation,
                total_cost=total,
                percentage_of_total=(total / total_cost * 100) if total_cost > 0 else 0,
                by_service=by_service,
                by_environment=by_environment,
                by_category={
                    CostCategory.DIRECT.value: direct_cost,
                    CostCategory.SHARED.value: shared_allocation,
                },
            )

        # Calculate allocation quality
        quality_score = self._calculate_allocation_quality(
            total_cost, total_unallocated, cost_records
        )

        return AllocationResult(
            allocation_id=str(uuid.uuid4()),
            generated_at=now,
            period_start=period_start,
            period_end=period_end,
            total_cost=total_cost,
            direct_cost=total_direct,
            shared_cost=total_shared,
            unallocated_cost=total_unallocated,
            allocations=allocations,
            unallocated_reasons=unallocated_reasons[:10],  # Limit to 10
            rules_applied=[r.name for r in self._rules],
            allocation_quality_score=quality_score,
        )

    def analyze_tagging(
        self,
        cost_records: list[CostRecord],
    ) -> TaggingAnalysis:
        """Analyze tagging coverage and quality.

        Args:
            cost_records: Cost records to analyze

        Returns:
            TaggingAnalysis with recommendations
        """
        # Count resources (by unique resource_id)
        resources: dict[str, CostRecord] = {}
        for record in cost_records:
            if record.resource_id and record.resource_id not in resources:
                resources[record.resource_id] = record

        total_resources = len(resources)

        # Analyze tagging coverage
        coverage_by_tag: dict[str, int] = {tag: 0 for tag in self.required_tags}
        tagged_count = 0

        for resource_id, record in resources.items():
            has_any_tag = False

            for tag_key in self.required_tags:
                if self._get_tag(record, tag_key):
                    coverage_by_tag[tag_key] += 1
                    has_any_tag = True

            if has_any_tag:
                tagged_count += 1

        # Convert to percentages
        coverage_pct = {
            tag: (count / total_resources * 100) if total_resources > 0 else 0
            for tag, count in coverage_by_tag.items()
        }

        # Find missing tags (coverage < 50%)
        missing_tags = [
            tag for tag, pct in coverage_pct.items()
            if pct < 50
        ]

        # Calculate untagged cost
        untagged_cost = sum(
            r.billed_cost for r in cost_records
            if not r.tags or not any(
                self._get_tag(r, tag) for tag in self.required_tags
            )
        )
        total_cost = sum(r.billed_cost for r in cost_records)

        return TaggingAnalysis(
            total_resources=total_resources,
            tagged_resources=tagged_count,
            tagging_coverage=(tagged_count / total_resources * 100) if total_resources > 0 else 0,
            coverage_by_tag=coverage_pct,
            missing_tags=missing_tags,
            untagged_cost=untagged_cost,
            untagged_percentage=(untagged_cost / total_cost * 100) if total_cost > 0 else 0,
        )

    def generate_tagging_recommendations(
        self,
        resources: list[dict[str, Any]],
        environment: str | None = None,
        team: str | None = None,
        project: str | None = None,
    ) -> list[dict[str, Any]]:
        """Generate tagging recommendations for new resources.

        This is used during code generation to suggest proper tags.

        Args:
            resources: Resources being created
            environment: Target environment
            team: Team name
            project: Project name

        Returns:
            List of tagging recommendations
        """
        recommendations = []

        for resource in resources:
            existing_tags = resource.get("tags", {})
            suggested_tags = {}

            # Environment tag
            if "Environment" not in existing_tags:
                if environment:
                    suggested_tags["Environment"] = environment
                else:
                    suggested_tags["Environment"] = "<REQUIRED: production|staging|development>"

            # Team tag
            if "Team" not in existing_tags:
                if team:
                    suggested_tags["Team"] = team
                else:
                    suggested_tags["Team"] = "<REQUIRED: team-name>"

            # Project tag
            if "Project" not in existing_tags:
                if project:
                    suggested_tags["Project"] = project
                else:
                    suggested_tags["Project"] = "<RECOMMENDED: project-name>"

            # Cost center (derive from team if possible)
            if "CostCenter" not in existing_tags:
                suggested_tags["CostCenter"] = "<RECOMMENDED: cost-center-id>"

            # Owner
            if "Owner" not in existing_tags:
                suggested_tags["Owner"] = "<RECOMMENDED: owner-email>"

            if suggested_tags:
                recommendations.append({
                    "resource": resource.get("name", resource.get("type", "unknown")),
                    "resource_type": resource.get("type"),
                    "existing_tags": existing_tags,
                    "suggested_tags": suggested_tags,
                    "importance": "high" if "Environment" in suggested_tags or "Team" in suggested_tags else "medium",
                    "reason": "Required for cost allocation and showback",
                })

        return recommendations

    def _categorize_record(self, record: CostRecord) -> CostCategory:
        """Categorize a cost record."""
        service = (record.service_name or "").lower()

        # Check if it's a shared service
        for shared in self.shared_services:
            if shared.lower() in service:
                return CostCategory.SHARED

        # Check if it has required tags
        has_required_tag = any(
            self._get_tag(record, tag) for tag in self.required_tags[:3]  # Team, Env, Project
        )

        if has_required_tag:
            return CostCategory.DIRECT

        return CostCategory.UNALLOCATED

    def _get_target(
        self,
        record: CostRecord,
        dimension: str,
    ) -> str | None:
        """Get allocation target from record."""
        return self._get_tag(record, dimension)

    def _get_tag(
        self,
        record: CostRecord,
        tag_key: str,
    ) -> str | None:
        """Get tag value from record (case-insensitive)."""
        if not record.tags:
            return None

        # Try exact match
        if tag_key in record.tags:
            return record.tags[tag_key]

        # Try case-insensitive
        for key, value in record.tags.items():
            if key.lower() == tag_key.lower():
                return value

        return None

    def _calculate_allocation_quality(
        self,
        total_cost: float,
        unallocated_cost: float,
        cost_records: list[CostRecord],
    ) -> float:
        """Calculate allocation quality score (0-100)."""
        if total_cost == 0:
            return 100.0

        # Base score from allocation coverage
        allocation_rate = (total_cost - unallocated_cost) / total_cost
        score = allocation_rate * 80  # Up to 80 points for allocation

        # Bonus for tagging quality
        tagged_count = sum(1 for r in cost_records if r.tags and len(r.tags) >= 3)
        tag_quality = tagged_count / len(cost_records) if cost_records else 0
        score += tag_quality * 20  # Up to 20 points for tagging

        return min(100, max(0, score))
