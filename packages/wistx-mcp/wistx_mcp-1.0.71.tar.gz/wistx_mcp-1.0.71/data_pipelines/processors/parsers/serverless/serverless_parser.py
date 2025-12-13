"""Serverless Framework parser."""

import yaml
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class ServerlessParser(ToolParser):
    """Parser for Serverless Framework configuration files."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Serverless Framework functions/plugins.
        
        Args:
            code: Serverless Framework YAML content
            
        Returns:
            List of function names
        """
        resources = []
        config = self._parse_config(code)
        
        if not config:
            return resources
        
        functions = config.get("functions", {})
        resources.extend(list(functions.keys()))
        
        plugins = config.get("plugins", [])
        resources.extend([f"plugin:{p}" for p in plugins])
        
        return resources

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Serverless Framework config.
        
        Args:
            code: Serverless Framework YAML content
            
        Returns:
            Cloud provider name or None
        """
        config = self._parse_config(code)
        
        if not config:
            code_lower = code.lower()
            if "aws" in code_lower:
                return "aws"
            if "azure" in code_lower:
                return "azure"
            if "gcp" in code_lower or "google" in code_lower:
                return "gcp"
            return None
        
        provider = config.get("provider", {})
        if isinstance(provider, dict):
            provider_name = provider.get("name", "")
            if provider_name:
                return provider_name.lower()
        elif isinstance(provider, str):
            return provider.lower()
        
        return None

    def extract_services(self, code: str) -> list[str]:
        """Extract cloud services from Serverless Framework config.
        
        Args:
            code: Serverless Framework YAML content
            
        Returns:
            List of service names
        """
        services = []
        code_lower = code.lower()
        
        if "lambda" in code_lower or "functions" in code_lower:
            services.append("lambda")
        if "api gateway" in code_lower or "apigateway" in code_lower:
            services.append("apigateway")
        if "dynamodb" in code_lower:
            services.append("dynamodb")
        if "s3" in code_lower:
            services.append("s3")
        if "sns" in code_lower:
            services.append("sns")
        if "sqs" in code_lower:
            services.append("sqs")
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Serverless Framework metadata.
        
        Args:
            code: Serverless Framework YAML content
            
        Returns:
            Dictionary with Serverless Framework metadata
        """
        metadata = {}
        try:
            config = self._parse_config(code)
            
            if config:
                metadata["service"] = config.get("service")
                metadata["frameworkVersion"] = config.get("frameworkVersion")
                metadata["functions_count"] = len(config.get("functions", {}))
                metadata["plugins"] = config.get("plugins", [])
                
                provider = config.get("provider", {})
                if isinstance(provider, dict):
                    metadata["provider_name"] = provider.get("name")
                    metadata["provider_runtime"] = provider.get("runtime")
                    metadata["provider_region"] = provider.get("region")
        except (AttributeError, TypeError):
            pass
        
        return metadata

    def _parse_config(self, code: str) -> dict[str, Any] | None:
        """Parse Serverless Framework config YAML.
        
        Args:
            code: Config content
            
        Returns:
            Parsed config dictionary or None
        """
        try:
            return yaml.safe_load(code)
        except yaml.YAMLError:
            return None

    def validate_syntax(self, code: str) -> bool:
        """Validate Serverless Framework config syntax.
        
        Args:
            code: Serverless Framework YAML content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        config = self._parse_config(code)
        if not config:
            return False
        
        has_service = "service" in config
        has_provider = "provider" in config
        has_functions = "functions" in config
        
        return has_service and (has_provider or has_functions)

