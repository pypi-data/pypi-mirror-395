"""Datadog monitor parser."""

import json
import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class DatadogParser(ToolParser):
    """Parser for Datadog monitor configurations."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract monitor/metric names.
        
        Args:
            code: Datadog config YAML/JSON content
            
        Returns:
            List of monitor/metric names
        """
        resources = []
        config = self._parse_config(code)
        
        if not config:
            return resources
        
        monitors = config.get("monitors", [])
        for monitor in monitors:
            name = monitor.get("name", "")
            if name:
                resources.append(name)
        
        instances = config.get("instances", [])
        for instance in instances:
            if isinstance(instance, dict):
                name = instance.get("name", "")
                if name:
                    resources.append(name)
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Datadog config.
        
        Args:
            code: Datadog config YAML/JSON content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "amazon" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower:
            return "gcp"
        if "azure" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract monitored services.
        
        Args:
            code: Datadog config YAML/JSON content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "ec2" in code_lower:
            services.append("ec2")
        if "rds" in code_lower:
            services.append("rds")
        if "lambda" in code_lower:
            services.append("lambda")
        if "elasticsearch" in code_lower:
            services.append("elasticsearch")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Datadog metadata.
        
        Args:
            code: Datadog config YAML/JSON content
            
        Returns:
            Dictionary with Datadog metadata
        """
        metadata = {}
        config = self._parse_config(code)
        
        if config:
            metadata["init_config"] = config.get("init_config", {})
            metadata["instances_count"] = len(config.get("instances", []))
            metadata["logs"] = config.get("logs", [])
            metadata["metrics"] = config.get("metrics", [])
            metadata["monitors_count"] = len(config.get("monitors", []))
        
        return metadata

    def _parse_config(self, code: str) -> dict[str, Any] | None:
        """Parse Datadog config (YAML or JSON).
        
        Args:
            code: Config content
            
        Returns:
            Parsed config dictionary or None
        """
        try:
            if code.strip().startswith("{"):
                return json.loads(code)
            else:
                return yaml.safe_load(code)
        except (json.JSONDecodeError, yaml.YAMLError):
            return None

    def validate_syntax(self, code: str) -> bool:
        """Validate Datadog config syntax.
        
        Args:
            code: Datadog config YAML/JSON content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        config = self._parse_config(code)
        if not config:
            return False
        
        has_instances = "instances" in config
        has_init_config = "init_config" in config
        has_monitors = "monitors" in config
        
        return has_instances or has_init_config or has_monitors

