"""Dockerfile parser."""

import re
from typing import Any

from data_pipelines.processors.parsers.base_parser import ToolParser


class DockerParser(ToolParser):
    """Parser for Dockerfiles and docker-compose files."""

    def extract_resources(self, code: str) -> list[str]:
        """Extract Docker instructions/services.
        
        Args:
            code: Dockerfile or docker-compose content
            
        Returns:
            List of Docker instructions or service names
        """
        resources = []
        
        if "docker-compose" in code.lower() or "version:" in code.lower():
            resources.extend(self._extract_compose_services(code))
        else:
            resources.extend(self._extract_dockerfile_instructions(code))
        
        return list(set(resources))

    def _extract_dockerfile_instructions(self, code: str) -> list[str]:
        """Extract Dockerfile instructions."""
        instructions = []
        pattern = r'^\s*([A-Z]+)\s+'
        matches = re.findall(pattern, code, re.MULTILINE)
        instructions.extend(matches)
        return instructions

    def _extract_compose_services(self, code: str) -> list[str]:
        """Extract docker-compose service names."""
        services = []
        try:
            import yaml
            compose = yaml.safe_load(code)
            if isinstance(compose, dict) and "services" in compose:
                services.extend(list(compose["services"].keys()))
        except Exception:
            pass
        return services

    def extract_cloud_provider(self, code: str) -> str | None:
        """Extract cloud provider from Docker config.
        
        Args:
            code: Dockerfile or docker-compose content
            
        Returns:
            Cloud provider name or None (Docker is cloud-agnostic)
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
        """Extract services/components.
        
        Args:
            code: Dockerfile or docker-compose content
            
        Returns:
            List of service names
        """
        services = ["docker"]
        
        if "docker-compose" in code.lower():
            compose_services = self._extract_compose_services(code)
            services.extend(compose_services)
        
        return list(set(services))

    def extract_metadata(self, code: str) -> dict[str, Any]:
        """Extract Docker-specific metadata.
        
        Args:
            code: Dockerfile or docker-compose content
            
        Returns:
            Dictionary with Docker metadata
        """
        metadata = {}
        
        if "docker-compose" in code.lower() or "version:" in code.lower():
            metadata.update(self._extract_compose_metadata(code))
        else:
            metadata.update(self._extract_dockerfile_metadata(code))
        
        return metadata

    def _extract_dockerfile_metadata(self, code: str) -> dict[str, Any]:
        """Extract Dockerfile metadata."""
        metadata = {}
        
        base_image_match = re.search(r'FROM\s+([^\s]+)', code, re.IGNORECASE)
        if base_image_match:
            metadata["base_image"] = base_image_match.group(1)
        
        exposed_ports = re.findall(r'EXPOSE\s+(\d+)', code, re.IGNORECASE)
        if exposed_ports:
            metadata["exposed_ports"] = exposed_ports
        
        metadata["instructions_count"] = len(re.findall(r'^\s*[A-Z]+', code, re.MULTILINE))
        
        return metadata

    def _extract_compose_metadata(self, code: str) -> dict[str, Any]:
        """Extract docker-compose metadata."""
        metadata = {}
        try:
            import yaml
            compose = yaml.safe_load(code)
            
            if isinstance(compose, dict):
                metadata["version"] = compose.get("version")
                metadata["services_count"] = len(compose.get("services", {}))
                metadata["networks"] = list(compose.get("networks", {}).keys())
                metadata["volumes"] = list(compose.get("volumes", {}).keys())
        except Exception:
            pass
        
        return metadata

    def validate_syntax(self, code: str) -> bool:
        """Validate Docker syntax.
        
        Args:
            code: Dockerfile or docker-compose content
            
        Returns:
            True if syntax appears valid
        """
        if not code or len(code.strip()) < 10:
            return False
        
        code_lower = code.lower()
        
        if "docker-compose" in code_lower or "version:" in code_lower:
            try:
                import yaml
                compose = yaml.safe_load(code)
                return isinstance(compose, dict) and "services" in compose
            except Exception:
                return False
        else:
            has_from = bool(re.search(r'FROM\s+', code, re.IGNORECASE))
            has_instruction = bool(re.search(r'^\s*(RUN|COPY|ADD|CMD|ENTRYPOINT|ENV|WORKDIR)', code, re.MULTILINE | re.IGNORECASE))
            return has_from or has_instruction

