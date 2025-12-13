"""Cost allocation processor with multi-dimensional allocation."""

from typing import Any

from ..models.cost_data import CostAllocationDimension, FOCUSCostData
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class CostAllocationProcessor:
    """Process cost allocation using multi-dimensional allocation strategies.

    Follows FinOps Foundation cost allocation best practices:
    - Structural hierarchy (Business Unit → Department → Team → Project)
    - Application hierarchy (Application → Service → Component)
    - Environment-based allocation
    - Tag-based allocation
    - Default allocation rules
    """

    def __init__(self):
        """Initialize cost allocation processor."""
        self.default_allocation_rules = {
            "environment": {
                "prod": {"cost_center": "PROD-001"},
                "staging": {"cost_center": "STAGING-001"},
                "dev": {"cost_center": "DEV-001"},
            },
            "service_category": {
                "Compute": {"business_unit": "Engineering"},
                "Storage": {"business_unit": "Engineering"},
                "Database": {"business_unit": "Engineering"},
                "Network": {"business_unit": "Infrastructure"},
                "Security": {"business_unit": "Security"},
            },
        }

    def allocate_cost(
        self, cost_record: FOCUSCostData, allocation_rules: dict[str, Any] | None = None
    ) -> FOCUSCostData:
        """Allocate cost to business dimensions.

        Args:
            cost_record: FOCUS cost data record
            allocation_rules: Optional custom allocation rules

        Returns:
            FOCUS cost data record with allocation tags
        """
        if allocation_rules is None:
            allocation_rules = {}

        tags = cost_record.tags.copy()

        allocation = self._extract_allocation_from_tags(tags)
        allocation = self._apply_allocation_rules(allocation, cost_record, allocation_rules)
        allocation = self._apply_default_rules(allocation, cost_record)

        tags.update(self._allocation_to_tags(allocation))

        cost_record_dict = cost_record.model_dump()
        cost_record_dict["tags"] = tags

        return FOCUSCostData(**cost_record_dict)

    def _extract_allocation_from_tags(self, tags: dict[str, str]) -> CostAllocationDimension:
        """Extract allocation dimensions from tags.

        Args:
            tags: Cost allocation tags

        Returns:
            CostAllocationDimension object
        """
        return CostAllocationDimension(
            business_unit=tags.get("BusinessUnit") or tags.get("business_unit"),
            department=tags.get("Department") or tags.get("department"),
            team=tags.get("Team") or tags.get("team"),
            project=tags.get("Project") or tags.get("project"),
            environment=tags.get("Environment") or tags.get("environment"),
            application=tags.get("Application") or tags.get("application"),
            service=tags.get("Service") or tags.get("service"),
            component=tags.get("Component") or tags.get("component"),
            cost_center=tags.get("CostCenter") or tags.get("cost_center"),
            owner_email=tags.get("Owner") or tags.get("owner_email"),
            owner_team=tags.get("OwnerTeam") or tags.get("owner_team"),
            custom_tags={k: v for k, v in tags.items() if k not in self._standard_tag_keys()},
        )

    def _apply_allocation_rules(
        self,
        allocation: CostAllocationDimension,
        cost_record: FOCUSCostData,
        rules: dict[str, Any],
    ) -> CostAllocationDimension:
        """Apply custom allocation rules.

        Args:
            allocation: Current allocation dimensions
            cost_record: Cost data record
            rules: Custom allocation rules

        Returns:
            Updated allocation dimensions
        """
        allocation_dict = allocation.model_dump()

        for rule_type, rule_value in rules.items():
            if rule_type == "environment" and allocation.environment:
                if allocation.environment in rule_value:
                    allocation_dict.update(rule_value[allocation.environment])
            elif rule_type == "service_category" and cost_record.service_category:
                if cost_record.service_category in rule_value:
                    allocation_dict.update(rule_value[cost_record.service_category])
            elif rule_type == "service_name" and cost_record.service_name:
                if cost_record.service_name in rule_value:
                    allocation_dict.update(rule_value[cost_record.service_name])
            elif rule_type == "region" and cost_record.region_id:
                if cost_record.region_id in rule_value:
                    allocation_dict.update(rule_value[cost_record.region_id])

        return CostAllocationDimension(**allocation_dict)

    def _apply_default_rules(
        self, allocation: CostAllocationDimension, cost_record: FOCUSCostData
    ) -> CostAllocationDimension:
        """Apply default allocation rules.

        Args:
            allocation: Current allocation dimensions
            cost_record: Cost data record

        Returns:
            Updated allocation dimensions
        """
        allocation_dict = allocation.model_dump()

        if not allocation.environment and cost_record.tags.get("environment"):
            env = cost_record.tags.get("environment")
            if env in self.default_allocation_rules["environment"]:
                allocation_dict.update(self.default_allocation_rules["environment"][env])

        if not allocation.business_unit and cost_record.service_category:
            if cost_record.service_category in self.default_allocation_rules["service_category"]:
                allocation_dict.update(
                    self.default_allocation_rules["service_category"][cost_record.service_category]
                )

        return CostAllocationDimension(**allocation_dict)

    def _allocation_to_tags(self, allocation: CostAllocationDimension) -> dict[str, str]:
        """Convert allocation dimensions to tags.

        Args:
            allocation: Cost allocation dimensions

        Returns:
            Dictionary of tags
        """
        tags = {}

        if allocation.business_unit:
            tags["BusinessUnit"] = allocation.business_unit
        if allocation.department:
            tags["Department"] = allocation.department
        if allocation.team:
            tags["Team"] = allocation.team
        if allocation.project:
            tags["Project"] = allocation.project
        if allocation.environment:
            tags["Environment"] = allocation.environment
        if allocation.application:
            tags["Application"] = allocation.application
        if allocation.service:
            tags["Service"] = allocation.service
        if allocation.component:
            tags["Component"] = allocation.component
        if allocation.cost_center:
            tags["CostCenter"] = allocation.cost_center
        if allocation.owner_email:
            tags["Owner"] = allocation.owner_email
        if allocation.owner_team:
            tags["OwnerTeam"] = allocation.owner_team

        tags.update(allocation.custom_tags)

        return tags

    def _standard_tag_keys(self) -> set[str]:
        """Get standard tag keys.

        Returns:
            Set of standard tag keys
        """
        return {
            "BusinessUnit",
            "business_unit",
            "Department",
            "department",
            "Team",
            "team",
            "Project",
            "project",
            "Environment",
            "environment",
            "Application",
            "application",
            "Service",
            "service",
            "Component",
            "component",
            "CostCenter",
            "cost_center",
            "Owner",
            "owner_email",
            "OwnerTeam",
            "owner_team",
        }

    def allocate_batch(
        self, cost_records: list[FOCUSCostData], allocation_rules: dict[str, Any] | None = None
    ) -> list[FOCUSCostData]:
        """Allocate costs for a batch of records.

        Args:
            cost_records: List of FOCUS cost data records
            allocation_rules: Optional custom allocation rules

        Returns:
            List of allocated cost records
        """
        allocated = []

        for record in cost_records:
            try:
                allocated_record = self.allocate_cost(record, allocation_rules)
                allocated.append(allocated_record)
            except Exception as e:
                logger.warning("Failed to allocate cost for record %s: %s", record.lookup_key, e)
                allocated.append(record)

        logger.info("Allocated %d/%d cost records", len(allocated), len(cost_records))

        return allocated

