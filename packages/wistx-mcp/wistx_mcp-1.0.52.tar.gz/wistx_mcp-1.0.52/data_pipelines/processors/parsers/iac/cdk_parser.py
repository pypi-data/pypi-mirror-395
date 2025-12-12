"""AWS CDK parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class CDKParser(ToolParser):
    """Parser for AWS CDK code (TypeScript, Python, Java, C#)."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract CDK construct types.
        
        Args:
            code: CDK code content
            
        Returns:
            List of construct types (e.g., ["Bucket", "Function", "Cluster"])
        """
        resources = []
        
        patterns = [
            r'new\s+(\w+)\s*\(',  # TypeScript: new Bucket(...)
            r'(\w+)\(self,',  # Python: Bucket(self, ...)
            r'new\s+(\w+)\(this,',  # Java/C#: new Bucket(this, ...)
            r'@aws-cdk/([a-zA-Z-]+)',  # TypeScript imports
            r'aws_cdk\.([a-zA-Z_]+)',  # Python imports
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, code)
            resources.extend(matches)
        
        aws_constructs = [
            "Bucket", "Function", "Cluster", "Table", "Instance", "Database",
            "Queue", "Topic", "Distribution", "Certificate", "Vpc", "Subnet",
        ]
        
        found_constructs = [c for c in aws_constructs if c in code]
        resources.extend(found_constructs)
        
        return list(set(resources))

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from CDK code.
        
        Args:
            code: CDK code content
            
        Returns:
            Always returns "aws" for AWS CDK
        """
        code_lower = code.lower()
        
        if "aws-cdk" in code_lower or "aws_cdk" in code_lower or "cdk" in code_lower:
            return "aws"
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract AWS services from CDK code.
        
        Args:
            code: CDK code content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        service_mapping = {
            "s3": ["bucket", "s3"],
            "lambda": ["function", "lambda"],
            "rds": ["database", "rds", "dbinstance"],
            "ec2": ["instance", "vpc", "subnet"],
            "eks": ["cluster", "eks"],
            "ecs": ["service", "cluster", "ecs"],
            "dynamodb": ["table", "dynamodb"],
            "cloudfront": ["distribution", "cloudfront"],
            "sns": ["topic", "sns"],
            "sqs": ["queue", "sqs"],
        }
        
        for service, patterns in service_mapping.items():
            if any(pattern in code_lower for pattern in patterns):
                if service not in services:
                    services.append(service)
        
        return services

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract CDK-specific metadata.
        
        Args:
            code: CDK code content
            
        Returns:
            Dictionary with CDK metadata
        """
        metadata = {
            "language": self._detect_language(code),
            "stack_name": self._extract_stack_name(code),
            "constructs": self.extract_resources(code),
        }
        return metadata

    def _detect_language(self, code: str) -> str | None:
        """Detect programming language."""
        if "import * as cdk" in code or "from aws_cdk" in code:
            return "typescript"
        if "from aws_cdk" in code or "import aws_cdk" in code:
            return "python"
        if "package" in code and "import software.amazon.awscdk" in code:
            return "java"
        if "using Amazon.CDK" in code:
            return "csharp"
        return None

    def _extract_stack_name(self, code: str) -> str | None:
        """Extract stack name."""
        pattern = r'class\s+(\w+)\s+extends\s+Stack'
        match = re.search(pattern, code)
        if match:
            return match.group(1)
        return None

    def validate_syntax(self, code: str) -> bool:
        """Basic CDK syntax validation.
        
        Args:
            code: CDK code content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        has_cdk = "cdk" in code_lower or "aws-cdk" in code_lower
        has_stack = "stack" in code_lower or "construct" in code_lower
        has_construct = any(construct in code for construct in ["Bucket", "Function", "Cluster", "Table"])
        
        return has_cdk and (has_stack or has_construct)

