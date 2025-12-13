"""AWS CloudFormation template parser."""

import json
import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class CloudFormationParser(ToolParser):
    """Parser for AWS CloudFormation templates."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract CloudFormation resource types.
        
        Args:
            code: CloudFormation template content
            
        Returns:
            List of resource types (e.g., ["AWS::RDS::DBInstance", "AWS::S3::Bucket"])
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
        """Extract cloud provider from CloudFormation.
        
        Args:
            code: CloudFormation template content
            
        Returns:
            Always returns "aws" for CloudFormation
        """
        return "aws"

    def extract_services(self, code: str) -> list[str]:
        """Extract AWS services from CloudFormation.
        
        Args:
            code: CloudFormation template content
            
        Returns:
            List of service names
        """
        services = []
        resources = self.extract_resources(code)
        
        service_mapping = {
            "AWS::RDS::DBInstance": "rds",
            "AWS::RDS::DBCluster": "rds",
            "AWS::S3::Bucket": "s3",
            "AWS::EC2::Instance": "ec2",
            "AWS::EKS::Cluster": "eks",
            "AWS::Lambda::Function": "lambda",
            "AWS::ECS::Service": "ecs",
            "AWS::ECS::Cluster": "ecs",
            "AWS::DynamoDB::Table": "dynamodb",
            "AWS::ElastiCache::CacheCluster": "elasticache",
        }
        
        for resource_type in resources:
            service = service_mapping.get(resource_type)
            if service and service not in services:
                services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract CloudFormation-specific metadata.
        
        Args:
            code: CloudFormation template content
            
        Returns:
            Dictionary with CloudFormation metadata
        """
        metadata = {}
        template = self._parse_template(code)
        
        if template:
            metadata["description"] = template.get("Description")
            metadata["parameters"] = list(template.get("Parameters", {}).keys())
            metadata["outputs"] = list(template.get("Outputs", {}).keys())
            metadata["resources_count"] = len(template.get("Resources", {}))
            metadata["transform"] = template.get("Transform")
        
        return metadata

    def _parse_template(self, code: str) -> dict[str, Any] | None:
        """Parse CloudFormation template (YAML or JSON).
        
        Args:
            code: Template content
            
        Returns:
            Parsed template dictionary or None
        """
        try:
            if code.strip().startswith("{"):
                return json.loads(code)
            else:
                return yaml.safe_load(code)
        except (json.JSONDecodeError, yaml.YAMLError):
            return None

    def validate_syntax(self, code: str) -> bool:
        """Basic CloudFormation syntax validation.
        
        Args:
            code: CloudFormation template content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        template = self._parse_template(code)
        if not template:
            return False
        
        has_resources = "Resources" in template
        has_awstemplate = "AWSTemplateFormatVersion" in template or "Transform" in template
        
        return has_resources or has_awstemplate

