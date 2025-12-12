"""OpenTelemetry collector parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class OpenTelemetryParser(ToolParser):
    """Parser for OpenTelemetry collector configuration."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract OpenTelemetry components.
        
        Args:
            code: OpenTelemetry collector YAML content
            
        Returns:
            List of receiver/processor/exporter names
        """
        resources = []
        try:
            config = yaml.safe_load(code)
            
            receivers = config.get("receivers", {})
            resources.extend([f"receiver:{name}" for name in receivers.keys()])
            
            processors = config.get("processors", {})
            resources.extend([f"processor:{name}" for name in processors.keys()])
            
            exporters = config.get("exporters", {})
            resources.extend([f"exporter:{name}" for name in exporters.keys()])
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from OpenTelemetry config.
        
        Args:
            code: OpenTelemetry collector YAML content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "xray" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower:
            return "gcp"
        if "azure" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract monitored services.
        
        Args:
            code: OpenTelemetry collector YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "prometheus" in code_lower:
            services.append("prometheus")
        if "jaeger" in code_lower:
            services.append("jaeger")
        if "zipkin" in code_lower:
            services.append("zipkin")
        if "otlp" in code_lower:
            services.append("otlp")
        if "xray" in code_lower:
            services.append("xray")
        if "cloudwatch" in code_lower:
            services.append("cloudwatch")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract OpenTelemetry metadata.
        
        Args:
            code: OpenTelemetry collector YAML content
            
        Returns:
            Dictionary with OpenTelemetry metadata
        """
        metadata = {}
        try:
            config = yaml.safe_load(code)
            
            metadata["receivers_count"] = len(config.get("receivers", {}))
            metadata["processors_count"] = len(config.get("processors", {}))
            metadata["exporters_count"] = len(config.get("exporters", {}))
            
            service = config.get("service", {})
            metadata["service_pipelines"] = list(service.get("pipelines", {}).keys())
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate OpenTelemetry collector syntax.
        
        Args:
            code: OpenTelemetry collector YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            config = yaml.safe_load(code)
            if not isinstance(config, dict):
                return False
            
            has_receivers = "receivers" in config
            has_processors = "processors" in config
            has_exporters = "exporters" in config
            has_service = "service" in config
            
            return (has_receivers or has_processors or has_exporters) and has_service
        except yaml.YAMLError:
            return False

