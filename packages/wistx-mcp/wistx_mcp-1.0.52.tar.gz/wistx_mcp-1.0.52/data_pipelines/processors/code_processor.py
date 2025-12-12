"""Code examples processor.

Processes raw code examples from collectors and enriches them with metadata,
compliance analysis, cost analysis, and best practices.
"""

import hashlib
import logging
from datetime import datetime
from typing import Any

from data_pipelines.models.code_example import CodeExample
from data_pipelines.processors.parsers import ToolParser
from data_pipelines.processors.parsers.base_parser import ToolParser as BaseParser

logger = logging.getLogger(__name__)


class CodeProcessor:
    """Process code examples with tool categorization and basic enrichment."""

    def __init__(self):
        """Initialize code processor."""
        self.parsers: dict[str, BaseParser] = {}

    def register_parser(self, code_type: str, parser: BaseParser) -> None:
        """Register a parser for a code type.
        
        Args:
            code_type: Code type identifier (e.g., "terraform", "kubernetes")
            parser: Parser instance implementing ToolParser interface
        """
        self.parsers[code_type] = parser
        logger.debug("Registered parser for code type: %s", code_type)

    def process_raw_data(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Process raw code example data.
        
        Args:
            raw_data: Raw code example dictionary from collector
            
        Returns:
            Processed code example dictionary ready for enrichment
        """
        code_type = raw_data.get("code_type", "unknown")
        code = raw_data.get("code", "")
        
        if not code or len(code.strip()) < 10:
            raise ValueError(f"Code content too short: {len(code)} characters")
        
        parser = self.parsers.get(code_type)
        if not parser:
            logger.warning("No parser registered for code type: %s", code_type)
            parser = self._get_fallback_parser()
        
        if not parser.validate_syntax(code):
            raise ValueError(f"Invalid syntax for code type: {code_type}")
        
        cloud_provider = parser.extract_cloud_provider(code) or "unknown"
        services = parser.extract_services(code) or []
        resources = parser.extract_resources(code) or []
        metadata = parser.extract_metadata(code) or {}
        
        example_id = self._generate_example_id(
            github_url=raw_data.get("github_url", ""),
            file_path=raw_data.get("file_path", ""),
            code_type=code_type,
        )
        
        processed = {
            "example_id": example_id,
            "title": raw_data.get("title", "Untitled Code Example"),
            "description": raw_data.get("description", ""),
            "code": code,
            "code_type": code_type,
            "cloud_provider": cloud_provider,
            "services": services,
            "resources": resources,
            "github_url": raw_data.get("github_url", ""),
            "file_path": raw_data.get("file_path", ""),
            "stars": raw_data.get("stars", 0),
            "quality_score": raw_data.get("quality_score", 0),
            "metadata": metadata,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        return processed

    def _generate_example_id(
        self,
        github_url: str,
        file_path: str,
        code_type: str,
    ) -> str:
        """Generate unique example ID.
        
        Args:
            github_url: GitHub repository URL
            file_path: File path in repository
            code_type: Code type
            
        Returns:
            Unique example ID
        """
        unique_string = f"{github_url}:{file_path}:{code_type}"
        hash_obj = hashlib.sha256(unique_string.encode("utf-8"))
        return hash_obj.hexdigest()[:24]

    def _get_fallback_parser(self) -> BaseParser:
        """Get fallback parser for unknown code types.
        
        Returns:
            Fallback parser instance
        """
        class FallbackParser(BaseParser):
            def extract_resources(self, code: str) -> list[str]:
                return []
            
            def extract_cloud_provider(self, code: str) -> str | None:
                return None
            
            def extract_services(self, code: str) -> list[str]:
                return []
            
            def extract_metadata(self, code: str) -> dict[str, Any]:
                return {}
            
            def validate_syntax(self, code: str) -> bool:
                return len(code.strip()) > 10
        
        return FallbackParser()
