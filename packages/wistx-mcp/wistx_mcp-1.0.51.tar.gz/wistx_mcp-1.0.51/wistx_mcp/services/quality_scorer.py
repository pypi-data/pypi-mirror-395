"""Quality scorer service for repository trees and infrastructure visualizations."""

import logging
from typing import Any

from wistx_mcp.models.quality_score import QualityScoreBreakdown, QualityScoreResult

logger = logging.getLogger(__name__)


class QualityScorer:
    """Service for scoring repository trees and infrastructure visualizations."""

    STORAGE_THRESHOLD = 80.0

    def score_repository_tree(self, tree_data: dict[str, Any]) -> QualityScoreResult:
        """Score repository tree quality.

        Args:
            tree_data: Repository tree data from get_github_file_tree

        Returns:
            QualityScoreResult with overall score and breakdown
        """
        structure = tree_data.get("structure", {})
        metadata = tree_data.get("metadata", {})

        breakdown = QualityScoreBreakdown()

        breakdown.structure_completeness = self._evaluate_structure_completeness(structure)
        breakdown.infrastructure_quality = self._evaluate_infrastructure_quality(structure, metadata)
        breakdown.devops_maturity = self._evaluate_devops_maturity(structure)
        breakdown.documentation_quality = self._evaluate_documentation_quality(structure)
        breakdown.compliance_security = self._evaluate_compliance_security(structure)
        breakdown.code_organization = self._evaluate_code_organization(structure, metadata)

        overall_score = (
            breakdown.structure_completeness * 0.25
            + breakdown.infrastructure_quality * 0.20
            + breakdown.devops_maturity * 0.20
            + breakdown.documentation_quality * 0.15
            + breakdown.compliance_security * 0.10
            + breakdown.code_organization * 0.10
        )

        score_dict = {
            "structure_completeness": breakdown.structure_completeness * 100,
            "infrastructure_quality": breakdown.infrastructure_quality * 100,
            "devops_maturity": breakdown.devops_maturity * 100,
            "documentation_quality": breakdown.documentation_quality * 100,
            "compliance_security": breakdown.compliance_security * 100,
            "code_organization": breakdown.code_organization * 100,
        }

        recommendations = self._generate_recommendations(breakdown)

        return QualityScoreResult(
            overall_score=round(overall_score * 100, 2),
            score_breakdown=score_dict,
            recommendations=recommendations,
            metadata={
                "total_files": metadata.get("total_files", 0),
                "total_directories": metadata.get("total_directories", 0),
                "languages": metadata.get("languages", []),
            },
            meets_threshold=overall_score * 100 >= self.STORAGE_THRESHOLD,
        )

    def score_infrastructure_visualization(
        self, viz_data: dict[str, Any]
    ) -> QualityScoreResult:
        """Score infrastructure visualization quality.

        Args:
            viz_data: Visualization data from visualize_infra_flow

        Returns:
            QualityScoreResult with overall score and breakdown
        """
        components = viz_data.get("components", [])
        connections = viz_data.get("connections", [])
        visualization = viz_data.get("visualization", "")
        format_type = viz_data.get("format", "mermaid")
        metadata = viz_data.get("metadata", {})

        breakdown = QualityScoreBreakdown()

        breakdown.diagram_completeness = self._evaluate_diagram_completeness(components, connections)
        breakdown.visualization_accuracy = self._evaluate_visualization_accuracy(components, connections)
        breakdown.diagram_quality = self._evaluate_diagram_quality(visualization, format_type)
        breakdown.infrastructure_complexity = self._evaluate_infrastructure_complexity(components, connections)
        breakdown.best_practices = self._evaluate_best_practices(components, connections)

        overall_score = (
            breakdown.diagram_completeness * 0.30
            + breakdown.visualization_accuracy * 0.25
            + breakdown.diagram_quality * 0.20
            + breakdown.infrastructure_complexity * 0.15
            + breakdown.best_practices * 0.10
        )

        score_dict = {
            "diagram_completeness": breakdown.diagram_completeness * 100,
            "visualization_accuracy": breakdown.visualization_accuracy * 100,
            "diagram_quality": breakdown.diagram_quality * 100,
            "infrastructure_complexity": breakdown.infrastructure_complexity * 100,
            "best_practices": breakdown.best_practices * 100,
        }

        recommendations = self._generate_viz_recommendations(breakdown, components, connections)

        return QualityScoreResult(
            overall_score=round(overall_score * 100, 2),
            score_breakdown=score_dict,
            recommendations=recommendations,
            metadata={
                "component_count": len(components),
                "connection_count": len(connections),
                "format": format_type,
            },
            meets_threshold=overall_score * 100 >= self.STORAGE_THRESHOLD,
        )

    def _evaluate_structure_completeness(self, structure: dict[str, Any]) -> float:
        """Evaluate structure completeness (0-1.0)."""
        if not structure:
            return 0.0

        score = 0.0
        essential_dirs = {
            "config": 0.15,
            "scripts": 0.15,
            "tests": 0.15,
            "docs": 0.10,
            "infrastructure": 0.15,
            "monitoring": 0.10,
            "security": 0.10,
            "compliance": 0.10,
        }

        structure_paths = self._get_all_paths(structure)

        for dir_name, weight in essential_dirs.items():
            if self._has_directory(structure_paths, dir_name):
                score += weight

        return min(score, 1.0)

    def _evaluate_infrastructure_quality(
        self, structure: dict[str, Any], metadata: dict[str, Any]
    ) -> float:
        """Evaluate infrastructure code quality (0-1.0)."""
        score = 0.0
        structure_paths = self._get_all_paths(structure)

        has_terraform = self._has_file_pattern(structure_paths, "**/*.tf")
        has_kubernetes = self._has_file_pattern(structure_paths, "**/*.yaml", "**/*.yml")
        has_docker = self._has_file_pattern(structure_paths, "**/Dockerfile", "**/docker-compose.yml")

        if has_terraform:
            score += 0.4
            if self._has_directory(structure_paths, "modules"):
                score += 0.2
            if self._has_directory(structure_paths, "environments"):
                score += 0.2
            if self._has_file_pattern(structure_paths, "**/.terraform.lock.hcl"):
                score += 0.2

        if has_kubernetes:
            score += 0.3
            if self._has_directory(structure_paths, "manifests", "k8s"):
                score += 0.2

        if has_docker:
            score += 0.3

        return min(score, 1.0)

    def _evaluate_devops_maturity(self, structure: dict[str, Any]) -> float:
        """Evaluate DevOps maturity (0-1.0)."""
        score = 0.0
        structure_paths = self._get_all_paths(structure)

        has_github_actions = self._has_directory(structure_paths, ".github/workflows")
        has_gitlab_ci = self._has_file_pattern(structure_paths, ".gitlab-ci.yml")
        has_jenkins = self._has_file_pattern(structure_paths, "Jenkinsfile")

        if has_github_actions or has_gitlab_ci or has_jenkins:
            score += 0.4

        if self._has_file_pattern(structure_paths, "**/Dockerfile"):
            score += 0.2
        if self._has_file_pattern(structure_paths, "**/docker-compose.yml"):
            score += 0.1

        if self._has_directory(structure_paths, "monitoring", "prometheus", "grafana"):
            score += 0.2

        if self._has_directory(structure_paths, "security", ".security"):
            score += 0.1

        return min(score, 1.0)

    def _evaluate_documentation_quality(self, structure: dict[str, Any]) -> float:
        """Evaluate documentation quality (0-1.0)."""
        score = 0.0
        structure_paths = self._get_all_paths(structure)

        has_readme = any("readme" in path.lower() for path in structure_paths)
        has_docs = any("doc" in path.lower() for path in structure_paths)

        if has_readme:
            score += 0.5
        if has_docs:
            score += 0.25

        readme_content = self._get_file_content(structure, "README.md")
        if readme_content and len(readme_content) > 500:
            score += 0.25

        return min(score, 1.0)

    def _evaluate_compliance_security(self, structure: dict[str, Any]) -> float:
        """Evaluate compliance and security (0-1.0)."""
        score = 0.0
        structure_paths = self._get_all_paths(structure)

        if self._has_directory(structure_paths, "compliance"):
            score += 0.4
        if self._has_directory(structure_paths, "security"):
            score += 0.3
        if self._has_file_pattern(structure_paths, "**/.gitignore"):
            score += 0.2
        if self._has_file_pattern(structure_paths, "**/.security"):
            score += 0.1

        return min(score, 1.0)

    def _evaluate_code_organization(
        self, structure: dict[str, Any], metadata: dict[str, Any]
    ) -> float:
        """Evaluate code organization (0-1.0)."""
        score = 0.5

        languages = metadata.get("languages", [])
        if len(languages) > 0:
            score += 0.2

        structure_paths = self._get_all_paths(structure)
        if self._has_file_pattern(structure_paths, "**/package.json", "**/requirements.txt", "**/go.mod", "**/Cargo.toml"):
            score += 0.3

        return min(score, 1.0)

    def _evaluate_diagram_completeness(
        self, components: list[dict[str, Any]], connections: list[dict[str, Any]]
    ) -> float:
        """Evaluate diagram completeness (0-1.0)."""
        if not components:
            return 0.0

        score = 0.0

        component_count_score = min(len(components) / 20.0, 1.0) * 0.4
        score += component_count_score

        connection_count_score = min(len(connections) / 15.0, 1.0) * 0.3
        score += connection_count_score

        resource_types = set(c.get("type", "") for c in components if c.get("type"))
        diversity_score = min(len(resource_types) / 10.0, 1.0) * 0.3
        score += diversity_score

        return min(score, 1.0)

    def _evaluate_visualization_accuracy(
        self, components: list[dict[str, Any]], connections: list[dict[str, Any]]
    ) -> float:
        """Evaluate visualization accuracy (0-1.0)."""
        if not components:
            return 0.0

        score = 0.0

        valid_components = sum(1 for c in components if c.get("id") and c.get("type"))
        if components:
            score += (valid_components / len(components)) * 0.5

        valid_connections = sum(
            1 for c in connections if c.get("from") and c.get("to") and c.get("type")
        )
        if connections:
            score += (valid_connections / len(connections)) * 0.5

        return min(score, 1.0)

    def _evaluate_diagram_quality(self, visualization: str, format_type: str) -> float:
        """Evaluate diagram quality (0-1.0)."""
        if not visualization:
            return 0.0

        score = 0.0

        if format_type == "mermaid":
            if visualization.startswith("graph"):
                score += 0.4
            if "-->" in visualization or "---" in visualization:
                score += 0.3
            if '["' in visualization or "[" in visualization:
                score += 0.3
        elif format_type == "plantuml":
            if visualization.startswith("@startuml"):
                score += 0.4
            if visualization.endswith("@enduml"):
                score += 0.3
            if "-->" in visualization:
                score += 0.3

        return min(score, 1.0)

    def _evaluate_infrastructure_complexity(
        self, components: list[dict[str, Any]], connections: list[dict[str, Any]]
    ) -> float:
        """Evaluate infrastructure complexity (0-1.0)."""
        if not components:
            return 0.0

        score = 0.0

        component_types = set(c.get("type", "") for c in components)
        if len(component_types) >= 5:
            score += 0.4

        network_connections = sum(1 for c in connections if c.get("type") == "network")
        if network_connections > 0:
            score += 0.3

        service_connections = sum(1 for c in connections if c.get("type") == "service")
        if service_connections > 0:
            score += 0.3

        return min(score, 1.0)

    def _evaluate_best_practices(
        self, components: list[dict[str, Any]], connections: list[dict[str, Any]]
    ) -> float:
        """Evaluate best practices adherence (0-1.0)."""
        score = 0.0

        component_types = [c.get("type", "").lower() for c in components]

        if any("load" in t or "balancer" in t for t in component_types):
            score += 0.3
        if any("monitor" in t or "log" in t for t in component_types):
            score += 0.3
        if any("security" in t or "firewall" in t for t in component_types):
            score += 0.2
        if len(connections) > len(components) * 0.5:
            score += 0.2

        return min(score, 1.0)

    def _generate_recommendations(self, breakdown: QualityScoreBreakdown) -> list[str]:
        """Generate improvement recommendations."""
        recommendations = []

        if breakdown.structure_completeness < 0.5:
            recommendations.append("Add essential directories: config/, scripts/, tests/, docs/")
        if breakdown.infrastructure_quality < 0.5:
            recommendations.append("Add infrastructure-as-code files (Terraform/Kubernetes)")
        if breakdown.devops_maturity < 0.5:
            recommendations.append("Add CI/CD pipeline configurations")
        if breakdown.documentation_quality < 0.5:
            recommendations.append("Improve documentation (README.md, docs/)")
        if breakdown.compliance_security < 0.5:
            recommendations.append("Add compliance and security configurations")
        if breakdown.code_organization < 0.5:
            recommendations.append("Improve code organization and structure")

        return recommendations

    def _generate_viz_recommendations(
        self,
        breakdown: QualityScoreBreakdown,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
    ) -> list[str]:
        """Generate visualization improvement recommendations."""
        recommendations = []

        if breakdown.diagram_completeness < 0.5:
            recommendations.append("Add more components and connections to the diagram")
        if breakdown.visualization_accuracy < 0.5:
            recommendations.append("Ensure all components have valid IDs and types")
        if breakdown.diagram_quality < 0.5:
            recommendations.append("Improve diagram syntax and formatting")
        if breakdown.infrastructure_complexity < 0.5:
            recommendations.append("Add more infrastructure components and relationships")
        if breakdown.best_practices < 0.5:
            recommendations.append("Include load balancers, monitoring, and security components")

        return recommendations

    def _get_all_paths(self, structure: dict[str, Any], prefix: str = "") -> list[str]:
        """Get all paths from nested structure."""
        paths = []
        children = structure.get("children", [])

        for child in children:
            child_path = child.get("path", child.get("name", ""))
            if prefix:
                child_path = f"{prefix}/{child_path}" if child_path else prefix
            paths.append(child_path)

            if child.get("type") == "directory":
                paths.extend(self._get_all_paths(child, child_path))

        return paths

    def _has_directory(self, paths: list[str], *dir_names: str) -> bool:
        """Check if any directory exists in paths."""
        return any(any(dir_name.lower() in path.lower() for dir_name in dir_names) for path in paths)

    def _has_file_pattern(self, paths: list[str], *patterns: str) -> bool:
        """Check if any file pattern matches paths."""
        import fnmatch

        for path in paths:
            for pattern in patterns:
                if fnmatch.fnmatch(path, pattern):
                    return True
        return False

    def _get_file_content(self, structure: dict[str, Any], filename: str) -> str | None:
        """Get file content from structure."""
        children = structure.get("children", [])

        for child in children:
            if child.get("name") == filename and child.get("type") == "file":
                return child.get("content", "")
            if child.get("type") == "directory":
                content = self._get_file_content(child, filename)
                if content:
                    return content

        return None

