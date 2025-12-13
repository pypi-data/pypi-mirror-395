"""Jenkins pipeline parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class JenkinsParser(ToolParser):
    """Parser for Jenkins pipeline files (Groovy)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract pipeline stages.
        
        Args:
            code: Jenkinsfile Groovy content
            
        Returns:
            List of stage names
        """
        resources = []
        
        stage_pattern = r'stage\s*\(["\']([^"\']+)["\']'
        matches = re.findall(stage_pattern, code, re.IGNORECASE)
        resources.extend(matches)
        
        parallel_pattern = r'parallel\s*\{([^}]+)\}'
        parallel_matches = re.findall(parallel_pattern, code, re.DOTALL | re.IGNORECASE)
        for parallel_block in parallel_matches:
            stage_matches = re.findall(stage_pattern, parallel_block, re.IGNORECASE)
            resources.extend(stage_matches)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Jenkins pipeline.
        
        Args:
            code: Jenkinsfile Groovy content
            
        Returns:
            Cloud provider name or None
        """
        code_lower = code.lower()
        
        if "aws" in code_lower or "amazon" in code_lower or "ec2" in code_lower:
            return "aws"
        if "gcp" in code_lower or "google" in code_lower or "gke" in code_lower:
            return "gcp"
        if "azure" in code_lower or "aks" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract services deployed/tested.
        
        Args:
            code: Jenkinsfile Groovy content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "eks" in code_lower or "kubernetes" in code_lower or "k8s" in code_lower:
            services.append("eks")
        if "ec2" in code_lower:
            services.append("ec2")
        if "lambda" in code_lower:
            services.append("lambda")
        if "s3" in code_lower:
            services.append("s3")
        if "docker" in code_lower:
            services.append("docker")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Jenkins pipeline metadata.
        
        Args:
            code: Jenkinsfile Groovy content
            
        Returns:
            Dictionary with Jenkins metadata
        """
        metadata = {}
        
        agent_match = re.search(r'agent\s*\{([^}]+)\}', code, re.IGNORECASE | re.DOTALL)
        if agent_match:
            metadata["agent"] = agent_match.group(1).strip()
        
        triggers_match = re.search(r'triggers\s*\{([^}]+)\}', code, re.IGNORECASE | re.DOTALL)
        if triggers_match:
            metadata["triggers"] = triggers_match.group(1).strip()
        
        environment_match = re.search(r'environment\s*\{([^}]+)\}', code, re.IGNORECASE | re.DOTALL)
        if environment_match:
            metadata["environment"] = environment_match.group(1).strip()
        
        stages = self.extract_resources(code)
        metadata["stages"] = stages
        metadata["stages_count"] = len(stages)
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Jenkins pipeline syntax.
        
        Args:
            code: Jenkinsfile Groovy content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        
        has_pipeline = "pipeline" in code_lower
        has_stage = "stage" in code_lower
        has_node = "node" in code_lower
        
        return has_pipeline or (has_stage and has_node)

