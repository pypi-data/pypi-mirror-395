"""Infrastructure visualizer - generate diagrams from infrastructure code."""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


class InfrastructureVisualizer:
    """Visualizer for infrastructure code."""

    def __init__(self, mongodb_client=None):
        """Initialize visualizer.

        Args:
            mongodb_client: MongoDB client (optional, for future enhancements)
        """
        self.mongodb_client = mongodb_client

    async def generate_visualization(
        self,
        infrastructure_code: str | None = None,
        infrastructure_type: str | None = None,
        visualization_type: str = "flow",
        format: str = "mermaid",
        include_resources: bool = True,
        include_networking: bool = True,
        depth: int = 3,
        focus_area: str | None = None,
    ) -> dict[str, Any]:
        """Generate visualization.

        Args:
            infrastructure_code: Infrastructure code
            infrastructure_type: Type of infrastructure
            visualization_type: Type of visualization (flow, architecture, dependencies, network)
            format: Output format (mermaid, plantuml)
            include_resources: Include resource details
            include_networking: Include networking
            depth: Depth level
            focus_area: Focus area

        Returns:
            Visualization data dictionary
        """
        if not infrastructure_code:
            return self._generate_empty_visualization(format)

        if infrastructure_type == "terraform" or (not infrastructure_type and ("resource" in infrastructure_code.lower() or "provider" in infrastructure_code.lower())):
            components, connections = self._parse_terraform(infrastructure_code)
        elif infrastructure_type == "kubernetes" or (not infrastructure_type and ("apiVersion" in infrastructure_code or "kind:" in infrastructure_code)):
            components, connections = self._parse_kubernetes(infrastructure_code)
        else:
            components, connections = [], []

        if focus_area:
            components, connections = self._filter_by_focus(components, connections, focus_area)

        if format == "mermaid":
            diagram = self._generate_mermaid_diagram(
                components,
                connections,
                visualization_type,
                include_resources,
                include_networking,
            )
        elif format == "plantuml":
            diagram = self._generate_plantuml_diagram(
                components,
                connections,
                visualization_type,
            )
        else:
            diagram = self._generate_mermaid_diagram(
                components,
                connections,
                visualization_type,
            )

        return {
            "diagram": diagram,
            "components": components,
            "connections": connections,
            "metadata": {
                "component_count": len(components),
                "connection_count": len(connections),
                "visualization_type": visualization_type,
                "format": format,
            },
        }

    def _parse_terraform(self, code: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Parse Terraform code to extract components and connections.

        Args:
            code: Terraform code

        Returns:
            Tuple of (components, connections)
        """
        components = []
        connections = []

        try:
            import hcl2

            parsed = hcl2.loads(code)

            resources = parsed.get("resource", {})

            for resource_type, resource_instances in resources.items():
                for instance_name, instance_config in resource_instances.items():
                    component_id = f"{resource_type}_{instance_name}"

                    components.append({
                        "id": component_id,
                        "type": resource_type,
                        "name": instance_name,
                        "config": instance_config,
                    })

                    config_str = str(instance_config)
                    dep_pattern = r"(\w+\.\w+\.\w+)"
                    deps = re.findall(dep_pattern, config_str)

                    for dep in deps:
                        connections.append({
                            "from": dep,
                            "to": component_id,
                            "type": "dependency",
                        })

        except ImportError:
            logger.warning("hcl2 library not available, using regex parsing")
            self._parse_terraform_regex(code, components, connections)
        except Exception as e:
            logger.warning("Failed to parse Terraform: %s", e)
            self._parse_terraform_regex(code, components, connections)

        return components, connections

    def _parse_terraform_regex(
        self,
        code: str,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
    ) -> None:
        """Parse Terraform using regex fallback.

        Args:
            code: Terraform code
            components: Components list to populate
            connections: Connections list to populate
        """
        resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"'
        matches = re.finditer(resource_pattern, code)

        for match in matches:
            resource_type = match.group(1)
            instance_name = match.group(2)
            component_id = f"{resource_type}_{instance_name}"

            components.append({
                "id": component_id,
                "type": resource_type,
                "name": instance_name,
            })

    def _parse_kubernetes(self, code: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Parse Kubernetes manifests.

        Args:
            code: Kubernetes YAML code

        Returns:
            Tuple of (components, connections)
        """
        components = []
        connections = []

        try:
            import yaml

            documents = yaml.safe_load_all(code)

            for doc in documents:
                if not doc:
                    continue

                kind = doc.get("kind")
                metadata = doc.get("metadata", {})
                name = metadata.get("name", "unknown")

                component_id = f"{kind.lower()}_{name}"

                components.append({
                    "id": component_id,
                    "type": kind,
                    "name": name,
                    "config": doc,
                })

                if kind == "Service":
                    spec = doc.get("spec", {})
                    selector = spec.get("selector", {})
                    if selector:
                        app = selector.get("app") or selector.get("name")
                        if app:
                            connections.append({
                                "from": f"deployment_{app}",
                                "to": component_id,
                                "type": "service",
                            })

                if kind == "Ingress":
                    spec = doc.get("spec", {})
                    rules = spec.get("rules", [])
                    for rule in rules:
                        http = rule.get("http", {})
                        paths = http.get("paths", [])
                        for path in paths:
                            backend = path.get("backend", {})
                            service = backend.get("service", {})
                            service_name = service.get("name")
                            if service_name:
                                connections.append({
                                    "from": component_id,
                                    "to": f"service_{service_name}",
                                    "type": "network",
                                })

        except ImportError:
            logger.warning("yaml library not available, using basic parsing")
        except Exception as e:
            logger.warning("Failed to parse Kubernetes: %s", e)

        return components, connections

    def _filter_by_focus(
        self,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
        focus_area: str,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Filter components and connections by focus area.

        Args:
            components: Components list
            connections: Connections list
            focus_area: Focus area keyword

        Returns:
            Filtered (components, connections)
        """
        focus_lower = focus_area.lower()

        filtered_components = [
            comp
            for comp in components
            if focus_lower in comp.get("type", "").lower() or focus_lower in comp.get("name", "").lower()
        ]

        component_ids = {comp["id"] for comp in filtered_components}

        filtered_connections = [
            conn
            for conn in connections
            if conn.get("from") in component_ids or conn.get("to") in component_ids
        ]

        return filtered_components, filtered_connections

    def _generate_mermaid_diagram(
        self,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
        viz_type: str,
        include_resources: bool = True,
        include_networking: bool = True,
    ) -> str:
        """Generate Mermaid diagram.

        Args:
            components: Components list
            connections: Connections list
            viz_type: Visualization type
            include_resources: Include resources
            include_networking: Include networking

        Returns:
            Mermaid diagram string
        """
        if viz_type == "flow":
            return self._generate_mermaid_flow(components, connections)
        elif viz_type == "architecture":
            return self._generate_mermaid_architecture(components, connections)
        elif viz_type == "dependencies":
            return self._generate_mermaid_dependencies(components, connections)
        elif viz_type == "network":
            return self._generate_mermaid_network(components, connections)
        else:
            return self._generate_mermaid_flow(components, connections)

    def _generate_mermaid_flow(
        self,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
    ) -> str:
        """Generate Mermaid flow diagram.

        Args:
            components: Components list
            connections: Connections list

        Returns:
            Mermaid flow diagram string
        """
        lines = ["graph TD"]

        for comp in components:
            comp_id = self._sanitize_id(comp["id"])
            comp_name = comp.get("name", comp_id)
            comp_type = comp.get("type", "resource")

            shape = self._get_mermaid_shape(comp_type)
            label = f"{comp_name}<br/>{comp_type}"
            lines.append(f'    {comp_id}["{label}"]')

        for conn in connections:
            from_id = self._sanitize_id(conn["from"])
            to_id = self._sanitize_id(conn["to"])
            conn_type = conn.get("type", "dependency")

            arrow = "-->"
            if conn_type == "network":
                arrow = "---"
            elif conn_type == "service":
                arrow = "==>"

            lines.append(f"    {from_id} {arrow} {to_id}")

        return "\n".join(lines)

    def _generate_mermaid_architecture(
        self,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
    ) -> str:
        """Generate architecture diagram.

        Args:
            components: Components list
            connections: Connections list

        Returns:
            Mermaid architecture diagram string
        """
        return self._generate_mermaid_flow(components, connections)

    def _generate_mermaid_dependencies(
        self,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
    ) -> str:
        """Generate dependency diagram.

        Args:
            components: Components list
            connections: Connections list

        Returns:
            Mermaid dependency diagram string
        """
        lines = ["graph LR"]

        dep_connections = [c for c in connections if c.get("type") == "dependency"]

        for comp in components:
            comp_id = self._sanitize_id(comp["id"])
            comp_name = comp.get("name", comp_id)
            lines.append(f'    {comp_id}["{comp_name}"]')

        for conn in dep_connections:
            from_id = self._sanitize_id(conn["from"])
            to_id = self._sanitize_id(conn["to"])
            lines.append(f"    {from_id} --> {to_id}")

        return "\n".join(lines)

    def _generate_mermaid_network(
        self,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
    ) -> str:
        """Generate network diagram.

        Args:
            components: Components list
            connections: Connections list

        Returns:
            Mermaid network diagram string
        """
        lines = ["graph TB"]

        network_connections = [c for c in connections if c.get("type") == "network"]

        for comp in components:
            comp_id = self._sanitize_id(comp["id"])
            comp_name = comp.get("name", comp_id)
            lines.append(f'    {comp_id}["{comp_name}"]')

        for conn in network_connections:
            from_id = self._sanitize_id(conn["from"])
            to_id = self._sanitize_id(conn["to"])
            lines.append(f"    {from_id} --- {to_id}")

        return "\n".join(lines)

    def _generate_plantuml_diagram(
        self,
        components: list[dict[str, Any]],
        connections: list[dict[str, Any]],
        viz_type: str,
    ) -> str:
        """Generate PlantUML diagram.

        Args:
            components: Components list
            connections: Connections list
            viz_type: Visualization type

        Returns:
            PlantUML diagram string
        """
        lines = ["@startuml"]

        for comp in components:
            comp_id = self._sanitize_id(comp["id"])
            comp_name = comp.get("name", comp_id)
            comp_type = comp.get("type", "component")
            lines.append(f'component "{comp_name}" as {comp_id}')

        for conn in connections:
            from_id = self._sanitize_id(conn["from"])
            to_id = self._sanitize_id(conn["to"])
            lines.append(f"{from_id} --> {to_id}")

        lines.append("@enduml")
        return "\n".join(lines)

    def _sanitize_id(self, comp_id: str) -> str:
        """Sanitize component ID for diagram.

        Args:
            comp_id: Component ID

        Returns:
            Sanitized ID
        """
        return comp_id.replace(".", "_").replace("-", "_").replace("/", "_")

    def _get_mermaid_shape(self, resource_type: str) -> str:
        """Get Mermaid shape for resource type.

        Args:
            resource_type: Resource type

        Returns:
            Shape string (not used in current implementation but kept for future)
        """
        shapes = {
            "aws_instance": "((EC2))",
            "aws_rds_instance": "[(RDS)]",
            "aws_s3_bucket": "[S3]",
            "aws_lambda_function": "([Lambda])",
            "Service": "([Service])",
            "Deployment": "([Deployment])",
        }
        return shapes.get(resource_type, "[Resource]")

    def _generate_empty_visualization(self, format: str) -> dict[str, Any]:
        """Generate empty visualization.

        Args:
            format: Output format

        Returns:
            Empty visualization dictionary
        """
        if format == "mermaid":
            diagram = "graph TD\n    Empty[No infrastructure code provided]"
        else:
            diagram = "No infrastructure code provided"

        return {
            "diagram": diagram,
            "components": [],
            "connections": [],
            "metadata": {},
        }

