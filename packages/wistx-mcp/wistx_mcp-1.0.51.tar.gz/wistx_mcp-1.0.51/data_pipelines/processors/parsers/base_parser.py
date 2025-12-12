"""Base parser interface for DevOps/Cloud tools."""

from abc import ABC, abstractmethod
from typing import Any


class ToolParser(ABC):
    """Base parser for DevOps/Cloud tools.
    
    Each tool-specific parser implements methods to extract:
    - Resources/components from code
    - Cloud provider
    - Services used
    - Tool-specific metadata
    """

    @abstractmethod
    def extract_resources(self, code: str) -> list[str]:
        """Extract resource types from code.
        
        For IAC: Returns cloud resources (e.g., ["AWS::RDS::DBInstance"])
        For CI/CD: Returns pipeline stages/jobs
        For Monitoring: Returns monitored resources/services
        For Platform: Returns platform resources/components
        
        Args:
            code: Code content
            
        Returns:
            List of resource identifiers
        """
        pass

    @abstractmethod
    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from code.
        
        Args:
            code: Code content
            
        Returns:
            Cloud provider name (aws, gcp, azure) or None
        """
        pass

    @abstractmethod
    def extract_services(self, code: str) -> list[str]:
        """Extract cloud services used.
        
        For IAC: Returns cloud services (e.g., ["rds", "s3"])
        For CI/CD: Returns services deployed/tested
        For Monitoring: Returns services monitored
        
        Args:
            code: Code content
            
        Returns:
            List of service names
        """
        pass

    @abstractmethod
    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract tool-specific metadata.
        
        Returns:
            Dictionary with tool-specific metadata:
            - For CI/CD: stages, triggers, environments
            - For Monitoring: metrics, alerts, dashboards
            - For Platform: components, resources, policies
            - For IAC: modules, variables, outputs
        """
        pass

    @abstractmethod
    def validate_syntax(self, code: str) -> bool:
        """Validate code syntax.
        
        Args:
            code: Code content
            
        Returns:
            True if syntax appears valid
        """
        pass

