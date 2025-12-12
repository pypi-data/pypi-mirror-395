"""AWS SAM template parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class SAMParser(ToolParser):
    """Parser for AWS SAM (Serverless Application Model) templates."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract SAM resource types.
        
        Args:
            code: SAM template YAML content
            
        Returns:
            List of resource types (e.g., ["AWS::Serverless::Function", "AWS::Serverless::Api"])
        """
        resources = []
        template = self._parse_template(code)
        
        if not template:
            return resources
        
        resources_section = template.get("Resources", {})
        for resource_name, resource_def in resources_section.items():
            if isinstance(resource_def, dict):
                resource_type = resource_def.get("Type", "")
                if resource_type:
                    resources.append(resource_type)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from SAM template.
        
        Args:
            code: SAM template YAML content
            
        Returns:
            Always returns "aws" for SAM
        """
        return "aws"

    def extract_services(self, code: str) -> list[str]:
        """Extract AWS services from SAM template.
        
        Args:
            code: SAM template YAML content
            
        Returns:
            List of service names
        """
        services = []
        resources = self.extract_resources(code)
        
        service_mapping = {
            "AWS::Serverless::Function": "lambda",
            "AWS::Serverless::Api": "apigateway",
            "AWS::Serverless::SimpleTable": "dynamodb",
            "AWS::Serverless::HttpApi": "apigateway",
            "AWS::Serverless::StateMachine": "stepfunctions",
        }
        
        for resource_type in resources:
            service = service_mapping.get(resource_type)
            if service and service not in services:
                services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract SAM template metadata.
        
        Args:
            code: SAM template YAML content
            
        Returns:
            Dictionary with SAM metadata
        """
        metadata = {}
        try:
            template = self._parse_template(code)
            
            if template:
                metadata["transform"] = template.get("Transform")
                metadata["description"] = template.get("Description")
                metadata["parameters"] = list(template.get("Parameters", {}).keys())
                metadata["outputs"] = list(template.get("Outputs", {}).keys())
                metadata["resources_count"] = len(template.get("Resources", {}))
        except (AttributeError, TypeError):
            pass
        
        return metadata

    def _parse_template(self, code: str) -> dict[str, Any] | None:
        """Parse SAM template YAML.
        
        Args:
            code: Template content
            
        Returns:
            Parsed template dictionary or None
        """
        try:
            return yaml.safe_load(code)
        except yaml.YAMLError:
            return None

    def validate_syntax(self, code: str) -> bool:
        """Validate SAM template syntax.
        
        Args:
            code: SAM template YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        template = self._parse_template(code)
        if not template:
            return False
        
        has_transform = template.get("Transform") == "AWS::Serverless-2016-10-31"
        has_resources = "Resources" in template
        
        return has_transform and has_resources

