"""Spinnaker pipeline parser."""

import json
import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class SpinnakerParser(ToolParser):
    """Parser for Spinnaker pipeline configurations."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Spinnaker pipeline stages.
        
        Args:
            code: Spinnaker pipeline JSON/YAML content
            
        Returns:
            List of stage names
        """
        resources = []
        pipeline = self._parse_pipeline(code)
        
        if not pipeline:
            return resources
        
        stages = pipeline.get("stages", [])
        for stage in stages:
            stage_name = stage.get("name", "")
            stage_type = stage.get("type", "")
            if stage_name:
                resources.append(f"{stage_type}:{stage_name}")
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Spinnaker pipeline.
        
        Args:
            code: Spinnaker pipeline JSON/YAML content
            
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
        """Extract services deployed.
        
        Args:
            code: Spinnaker pipeline JSON/YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("kubernetes")
        if "ec2" in code_lower:
            services.append("ec2")
        if "eks" in code_lower:
            services.append("eks")
        if "gke" in code_lower:
            services.append("gke")
        if "aks" in code_lower:
            services.append("aks")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Spinnaker pipeline metadata.
        
        Args:
            code: Spinnaker pipeline JSON/YAML content
            
        Returns:
            Dictionary with Spinnaker metadata
        """
        metadata = {}
        try:
            pipeline = self._parse_pipeline(code)
            
            if pipeline:
                metadata["application"] = pipeline.get("application")
                metadata["name"] = pipeline.get("name")
                metadata["stages_count"] = len(pipeline.get("stages", []))
                
                stages = pipeline.get("stages", [])
                stage_types = [stage.get("type", "") for stage in stages if stage.get("type")]
                metadata["stage_types"] = list(set(stage_types))
        except (AttributeError, TypeError):
            pass
        
        return metadata

    def _parse_pipeline(self, code: str) -> dict[str, Any] | None:
        """Parse Spinnaker pipeline (JSON or YAML).
        
        Args:
            code: Pipeline content
            
        Returns:
            Parsed pipeline dictionary or None
        """
        try:
            if code.strip().startswith("{"):
                return json.loads(code)
            else:
                return yaml.safe_load(code)
        except (json.JSONDecodeError, yaml.YAMLError):
            return None

    def validate_syntax(self, code: str) -> bool:
        """Validate Spinnaker pipeline syntax.
        
        Args:
            code: Spinnaker pipeline JSON/YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        pipeline = self._parse_pipeline(code)
        if not pipeline:
            return False
        
        has_application = "application" in pipeline
        has_stages = "stages" in pipeline
        
        return has_application and has_stages

