"""Grafana dashboard parser."""

import json
import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class GrafanaParser(ToolParser):
    """Parser for Grafana dashboard JSON/YAML."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract dashboard panels/datasources.
        
        Args:
            code: Grafana dashboard JSON/YAML content
            
        Returns:
            List of panel/datasource names
        """
        resources = []
        dashboard = self._parse_dashboard(code)
        
        if not dashboard:
            return resources
        
        panels = dashboard.get("panels", [])
        for panel in panels:
            title = panel.get("title", "")
            if title:
                resources.append(f"panel:{title}")
        
        targets = []
        for panel in panels:
            panel_targets = panel.get("targets", [])
            for target in panel_targets:
                ref_id = target.get("refId", "")
                if ref_id:
                    targets.append(ref_id)
        
        resources.extend([f"target:{t}" for t in set(targets)])
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Grafana dashboard.
        
        Args:
            code: Grafana dashboard JSON/YAML content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "cloudwatch" in code_lower:
            return "aws"
        if "gcp" in code_lower or "stackdriver" in code_lower:
            return "gcp"
        if "azure" in code_lower or "azuremonitor" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract monitored services.
        
        Args:
            code: Grafana dashboard JSON/YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "prometheus" in code_lower:
            services.append("prometheus")
        if "cloudwatch" in code_lower:
            services.append("cloudwatch")
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "elasticsearch" in code_lower:
            services.append("elasticsearch")
        if "influxdb" in code_lower:
            services.append("influxdb")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Grafana dashboard metadata.
        
        Args:
            code: Grafana dashboard JSON/YAML content
            
        Returns:
            Dictionary with Grafana metadata
        """
        metadata = {}
        dashboard = self._parse_dashboard(code)
        
        if dashboard:
            metadata["title"] = dashboard.get("title")
            metadata["uid"] = dashboard.get("uid")
            metadata["version"] = dashboard.get("version")
            metadata["panels_count"] = len(dashboard.get("panels", []))
            
            datasources = set()
            for panel in dashboard.get("panels", []):
                for target in panel.get("targets", []):
                    datasource = target.get("datasource", {})
                    if isinstance(datasource, dict):
                        ds_type = datasource.get("type", "")
                        if ds_type:
                            datasources.add(ds_type)
                    elif isinstance(datasource, str):
                        datasources.add(datasource)
            
            metadata["datasources"] = list(datasources)
        
        return metadata

    def _parse_dashboard(self, code: str) -> dict[str, Any] | None:
        """Parse Grafana dashboard (JSON or YAML).
        
        Args:
            code: Dashboard content
            
        Returns:
            Parsed dashboard dictionary or None
        """
        try:
            if code.strip().startswith("{"):
                return json.loads(code)
            else:
                return yaml.safe_load(code)
        except (json.JSONDecodeError, yaml.YAMLError):
            return None

    def validate_syntax(self, code: str) -> bool:
        """Validate Grafana dashboard syntax.
        
        Args:
            code: Grafana dashboard JSON/YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        dashboard = self._parse_dashboard(code)
        if not dashboard:
            return False
        
        has_dashboard = isinstance(dashboard, dict)
        has_panels = "panels" in dashboard or "dashboard" in dashboard
        
        return has_dashboard and has_panels

