"""CDK8s parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class CDK8sParser(ToolParser):
    """Parser for CDK8s code (Kubernetes CDK)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract CDK8s Kubernetes resource types.
        
        Args:
            code: CDK8s code content
            
        Returns:
            List of Kubernetes resource types (e.g., ["Deployment", "Service"])
        """
        resources = []
        
        k8s_resources = [
            "Deployment", "Service", "ConfigMap", "Secret", "Ingress",
            "StatefulSet", "DaemonSet", "Job", "CronJob", "PersistentVolume",
        ]
        
        for resource in k8s_resources:
            if resource in code:
                resources.append(resource)
        
        pattern = r'new\s+k8s\.([A-Z][a-zA-Z]+)\('
        matches = re.findall(pattern, code)
        resources.extend(matches)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from CDK8s code.
        
        Args:
            code: CDK8s code content
            
        Returns:
            Cloud provider name or None (CDK8s is cloud-agnostic)
        """
        code_lower = code.lower()
        
        if "eks" in code_lower:
            return "aws"
        if "gke" in code_lower:
            return "gcp"
        if "aks" in code_lower:
            return "azure"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract Kubernetes services/components.
        
        Args:
            code: CDK8s code content
            
        Returns:
            List of service names
        """
        services = ["kubernetes"]
        
        code_lower = code.lower()
        if "deployment" in code_lower:
            services.append("kubernetes")
        if "service" in code_lower:
            services.append("kubernetes")
        if "ingress" in code_lower:
            services.append("kubernetes")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract CDK8s-specific metadata.
        
        Args:
            code: CDK8s code content
            
        Returns:
            Dictionary with CDK8s metadata
        """
        metadata = {
            "language": self._detect_language(code),
            "constructs": self.extract_resources(code),
        }
        return metadata

    def _detect_language(self, code: str) -> str | None:
        """Detect programming language."""
        if "import * as k8s" in code or "from cdk8s" in code:
            return "typescript"
        if "import cdk8s" in code:
            return "python"
        return None

    def validate_syntax(self, code: str) -> bool:
        """Basic CDK8s syntax validation.
        
        Args:
            code: CDK8s code content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        has_cdk8s = "cdk8s" in code_lower or "cdk8s" in code
        has_k8s = "k8s" in code_lower or "k8s." in code
        has_construct = any(resource in code for resource in ["Deployment", "Service", "ConfigMap"])
        
        return has_cdk8s and has_k8s and has_construct

