"""Prometheus configuration parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class PrometheusParser(ToolParser):
    """Parser for Prometheus configuration files."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract scrape targets/jobs.
        
        Args:
            code: Prometheus config YAML
            
        Returns:
            List of job names
        """
        resources = []
        try:
            config = yaml.safe_load(code)
            scrape_configs = config.get("scrape_configs", [])
            for job in scrape_configs:
                job_name = job.get("job_name", "")
                if job_name:
                    resources.append(job_name)
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Prometheus config.
        
        Args:
            code: Prometheus config YAML
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "ec2" in code_lower or "eks" in code_lower:
            return "aws"
        if "gke" in code_lower:
            return "gcp"
        if "aks" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract monitored services.
        
        Args:
            code: Prometheus config YAML
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "node" in code_lower:
            services.append("node-exporter")
        if "apiserver" in code_lower:
            services.append("kube-apiserver")
        if "etcd" in code_lower:
            services.append("etcd")
        if "cadvisor" in code_lower:
            services.append("cadvisor")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Prometheus metadata.
        
        Args:
            code: Prometheus config YAML
            
        Returns:
            Dictionary with Prometheus metadata
        """
        metadata = {}
        try:
            config = yaml.safe_load(code)
            
            metadata["scrape_configs_count"] = len(config.get("scrape_configs", []))
            metadata["alerting"] = bool(config.get("alerting"))
            metadata["recording_rules_count"] = len(config.get("recording_rules", []))
            metadata["alert_rules_count"] = len(config.get("alert_rules", []))
            metadata["global"] = config.get("global", {})
        except (yaml.YAMLError, AttributeError, TypeError):
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Prometheus config syntax.
        
        Args:
            code: Prometheus config YAML
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        try:
            config = yaml.safe_load(code)
            if not isinstance(config, dict):
                return False
            
            has_scrape = "scrape_configs" in config
            has_global = "global" in config
            
            return has_scrape or has_global
        except yaml.YAMLError:
            return False

