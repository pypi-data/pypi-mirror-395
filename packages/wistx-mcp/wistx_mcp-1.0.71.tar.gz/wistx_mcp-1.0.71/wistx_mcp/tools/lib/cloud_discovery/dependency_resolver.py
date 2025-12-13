"""Dependency Resolver for Cloud Resources.

Implements Directed Acyclic Graph (DAG) based dependency resolution
using Kahn's Algorithm for topological sorting to determine the
correct order for Terraform import operations.

Import Order Phases:
1. Foundation - VPCs, Route53 Zones (no dependencies)
2. Networking - Subnets, IGWs, NAT Gateways, Route Tables
3. Security - Security Groups, IAM Roles, KMS Keys, ACM Certs
4. Data Layer - S3 Buckets, SSM Parameters, Log Groups
5. Databases - RDS, DynamoDB, ElastiCache
6. Load Balancing - ALB, NLB, Target Groups
7. Compute - EC2, Lambda, ECS, EKS
"""

import logging
from collections import defaultdict, deque
from typing import Any

from wistx_mcp.models.cloud_discovery import (
    CloudProvider,
    DependencyGraph,
    DiscoveredResource,
    ImportPhase,
    ResourceDependency,
)
from wistx_mcp.tools.lib.cloud_discovery.terraform_mapping_loader import (
    TerraformMapping,
    TerraformMappingLoader,
    get_terraform_mapping_loader,
)

logger = logging.getLogger(__name__)


# Import phase priority (lower = earlier)
PHASE_PRIORITY = {
    ImportPhase.FOUNDATION: 1,
    ImportPhase.NETWORKING: 2,
    ImportPhase.SECURITY: 3,
    ImportPhase.DATA_LAYER: 4,
    ImportPhase.DATABASES: 5,
    ImportPhase.LOAD_BALANCING: 6,
    ImportPhase.COMPUTE: 7,
}


class DependencyResolver:
    """Resolves resource dependencies and determines import order.
    
    Uses a two-phase approach:
    1. Phase-based ordering: Group resources by import phase
    2. Dependency-based ordering: Topological sort within phases
    
    This ensures that:
    - Infrastructure foundations are imported first
    - Dependencies are imported before dependents
    - Circular dependencies are detected and reported
    """
    
    def __init__(self, mapping_loader: TerraformMappingLoader | None = None):
        """Initialize the dependency resolver.
        
        Args:
            mapping_loader: Optional TerraformMappingLoader for dependency info
        """
        self._mapping_loader = mapping_loader or get_terraform_mapping_loader()
        self._mappings: dict[CloudProvider, dict[str, TerraformMapping]] = {}
    
    def _get_mappings(self, provider: CloudProvider) -> dict[str, TerraformMapping]:
        """Get cached mappings for a provider."""
        if provider not in self._mappings:
            self._mappings[provider] = self._mapping_loader.load_mappings(provider)
        return self._mappings[provider]
    
    def resolve_dependencies(
        self,
        resources: list[DiscoveredResource],
    ) -> DependencyGraph:
        """Build a dependency graph and determine import order.
        
        Args:
            resources: List of discovered resources
            
        Returns:
            DependencyGraph with ordered resources and dependency info
        """
        if not resources:
            return DependencyGraph(
                nodes=[],
                edges=[],
                topological_order=[],
                phases={phase.value: [] for phase in ImportPhase},
                has_cycles=False,
            )
        
        # Group resources by terraform type for dependency matching
        by_terraform_type: dict[str, list[DiscoveredResource]] = defaultdict(list)
        for resource in resources:
            by_terraform_type[resource.terraform_resource_type].append(resource)
        
        # Build dependency relationships
        dependencies: list[ResourceDependency] = []
        adjacency: dict[str, list[str]] = defaultdict(list)  # resource_id -> dependents
        in_degree: dict[str, int] = {r.cloud_resource_id: 0 for r in resources}
        
        for resource in resources:
            mapping = self._get_mapping_for_resource(resource)
            if not mapping or not mapping.dependencies:
                continue
            
            # Find resources this resource depends on
            for dep_tf_type in mapping.dependencies:
                if dep_tf_type in by_terraform_type:
                    for dep_resource in by_terraform_type[dep_tf_type]:
                        # Check if there's an actual relationship
                        if self._resources_are_related(resource, dep_resource):
                            dependencies.append(ResourceDependency(
                                source_id=resource.cloud_resource_id,
                                target_id=dep_resource.cloud_resource_id,
                                dependency_type="requires",
                                is_hard_dependency=True,
                            ))
                            adjacency[dep_resource.cloud_resource_id].append(
                                resource.cloud_resource_id
                            )
                            in_degree[resource.cloud_resource_id] += 1
        
        # Perform topological sort using Kahn's algorithm
        import_order, has_cycles = self._topological_sort(
            resources, adjacency, in_degree
        )

        # Group by phase (use string keys for the model)
        phases: dict[str, list[str]] = {phase.value: [] for phase in ImportPhase}
        for resource_id in import_order:
            resource = next((r for r in resources if r.cloud_resource_id == resource_id), None)
            if resource:
                phases[resource.import_phase.value].append(resource_id)

        # Store resources for later use (not in model, but needed for helper methods)
        self._last_resources = resources

        return DependencyGraph(
            nodes=[r.cloud_resource_id for r in resources],
            edges=dependencies,
            topological_order=import_order,
            phases=phases,
            has_cycles=has_cycles,
        )
    
    def _get_mapping_for_resource(
        self,
        resource: DiscoveredResource,
    ) -> TerraformMapping | None:
        """Get terraform mapping for a resource."""
        mappings = self._get_mappings(resource.cloud_provider)
        return mappings.get(resource.cloud_resource_type)
    
    def _resources_are_related(
        self,
        resource: DiscoveredResource,
        potential_dependency: DiscoveredResource,
    ) -> bool:
        """Check if two resources have an actual relationship.

        Uses multiple strategies:
        1. Same region (basic filter)
        2. VPC ID matching (for VPC-bound resources)
        3. ARN references in configuration
        """
        # Must be in same region (except for global resources)
        if resource.region != potential_dependency.region:
            if potential_dependency.region not in ("global", "us-east-1"):
                return False

        # Check VPC relationship
        resource_vpc = self._extract_vpc_id(resource)
        dep_vpc = self._extract_vpc_id(potential_dependency)

        if resource_vpc and dep_vpc:
            return resource_vpc == dep_vpc

        # Check if dependency is referenced in resource's raw_config
        if potential_dependency.arn and resource.raw_config:
            config_str = str(resource.raw_config)
            if potential_dependency.arn in config_str:
                return True
            if potential_dependency.cloud_resource_id in config_str:
                return True

        # Default to same region relationship
        return True

    def _extract_vpc_id(self, resource: DiscoveredResource) -> str | None:
        """Extract VPC ID from resource configuration."""
        if not resource.raw_config:
            return None

        # Direct VPC resources
        if resource.cloud_resource_type == "AWS::EC2::VPC":
            return resource.cloud_resource_id

        # Resources with VpcId property
        vpc_id = resource.raw_config.get("VpcId")
        if vpc_id:
            return vpc_id

        # Subnets have VpcId
        if "Subnet" in resource.cloud_resource_type:
            return resource.raw_config.get("VpcId")

        return None

    def _topological_sort(
        self,
        resources: list[DiscoveredResource],
        adjacency: dict[str, list[str]],
        in_degree: dict[str, int],
    ) -> tuple[list[str], bool]:
        """Perform topological sort using Kahn's algorithm.

        Returns:
            Tuple of (sorted_resource_ids, has_cycles)
        """
        # Create priority queue based on import phase
        resource_map = {r.cloud_resource_id: r for r in resources}

        def get_priority(resource_id: str) -> tuple[int, str]:
            resource = resource_map.get(resource_id)
            if resource:
                phase_priority = PHASE_PRIORITY.get(resource.import_phase, 99)
                return (phase_priority, resource_id)
            return (99, resource_id)

        # Initialize queue with zero in-degree nodes, sorted by phase priority
        queue = deque(
            sorted(
                [rid for rid, deg in in_degree.items() if deg == 0],
                key=get_priority,
            )
        )

        result: list[str] = []
        visited = 0

        while queue:
            current = queue.popleft()
            result.append(current)
            visited += 1

            # Process all dependents
            dependents = sorted(adjacency[current], key=get_priority)
            for dependent in dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    # Insert in sorted position
                    inserted = False
                    for i, item in enumerate(queue):
                        if get_priority(dependent) < get_priority(item):
                            queue.insert(i, dependent)
                            inserted = True
                            break
                    if not inserted:
                        queue.append(dependent)

        # Check for cycles
        has_cycles = visited != len(resources)

        if has_cycles:
            # Add remaining resources (those in cycles) at the end
            remaining = [r.cloud_resource_id for r in resources if r.cloud_resource_id not in result]
            logger.warning(
                "Circular dependencies detected involving %d resources: %s",
                len(remaining),
                remaining[:5],  # Log first 5
            )
            result.extend(sorted(remaining, key=get_priority))

        return result, has_cycles

    def get_import_order_by_phase(
        self,
        graph: DependencyGraph,
        resources: list[DiscoveredResource] | None = None,
    ) -> list[tuple[ImportPhase, list[DiscoveredResource]]]:
        """Get resources grouped and ordered by import phase.

        Args:
            graph: The dependency graph
            resources: Optional list of resources (uses cached if not provided)

        Returns:
            List of (phase, resources) tuples in import order
        """
        resources = resources or getattr(self, "_last_resources", [])
        resource_map = {r.cloud_resource_id: r for r in resources}

        result = []
        for phase in sorted(ImportPhase, key=lambda p: PHASE_PRIORITY.get(p, 99)):
            phase_resources = []
            for resource_id in graph.phases.get(phase.value, []):
                resource = resource_map.get(resource_id)
                if resource:
                    phase_resources.append(resource)

            if phase_resources:
                result.append((phase, phase_resources))

        return result

    def generate_import_commands(
        self,
        graph: DependencyGraph,
        terraform_resource_names: dict[str, str],
        resources: list[DiscoveredResource] | None = None,
    ) -> list[str]:
        """Generate Terraform import commands in correct order.

        Args:
            graph: The dependency graph
            terraform_resource_names: Map of cloud_resource_id -> terraform_name
            resources: Optional list of resources (uses cached if not provided)

        Returns:
            List of terraform import commands
        """
        resources = resources or getattr(self, "_last_resources", [])
        resource_map = {r.cloud_resource_id: r for r in resources}
        commands = []

        for resource_id in graph.topological_order:
            resource = resource_map.get(resource_id)
            if not resource:
                continue

            tf_name = terraform_resource_names.get(resource_id, resource_id)
            tf_type = resource.terraform_resource_type
            import_id = resource.cloud_resource_id  # Would use get_terraform_import_id in practice

            commands.append(
                f"terraform import {tf_type}.{tf_name} {import_id}"
            )

        return commands

    def validate_dependencies(
        self,
        graph: DependencyGraph,
        resources: list[DiscoveredResource] | None = None,
    ) -> list[str]:
        """Validate the dependency graph for potential issues.

        Args:
            graph: The dependency graph
            resources: Optional list of resources (uses cached if not provided)

        Returns:
            List of warning/error messages
        """
        resources = resources or getattr(self, "_last_resources", [])
        issues = []

        if graph.has_cycles:
            issues.append(
                "WARNING: Circular dependencies detected. Manual intervention may be required."
            )

        # Check for missing dependencies (orphaned references)
        resource_ids = set(graph.nodes)
        for dep in graph.edges:
            if dep.target_id not in resource_ids:
                issues.append(
                    f"WARNING: Resource {dep.source_id} references missing resource {dep.target_id}"
                )

        # Check for resources without any dependencies in late phases
        late_phases = {ImportPhase.COMPUTE, ImportPhase.LOAD_BALANCING}
        for resource in resources:
            if resource.import_phase in late_phases:
                has_deps = any(
                    d.source_id == resource.cloud_resource_id
                    for d in graph.edges
                )
                if not has_deps and resource.terraform_resource_type not in {
                    "aws_cloudwatch_metric_alarm",
                    "aws_lambda_function",
                }:
                    issues.append(
                        f"INFO: {resource.cloud_resource_id} has no detected dependencies"
                    )

        return issues

