"""Base compliance collector - thin wrapper around universal BaseCollector.

This maintains backward compatibility while using the universal base.
"""

from typing import Any

from bs4 import BeautifulSoup

from .base_collector_universal import BaseCollector
from .collection_result import CollectionResult
from .validation_models import RawComplianceControl


class BaseComplianceCollector(BaseCollector):
    """Base class for compliance standard collectors.

    Thin wrapper around BaseCollector with compliance-specific defaults.
    Maintains backward compatibility with existing compliance collectors.
    """

    def __init__(
        self,
        standard_name: str,
        version: str,
        enable_deep_crawl: bool = True,
        max_depth: int = 10,
        max_pages: int = 200,
    ):
        """Initialize compliance collector.

        Args:
            standard_name: Name of compliance standard (e.g., "PCI-DSS", "CIS")
            version: Standard version (e.g., "4.0", "2.0")
            enable_deep_crawl: Enable deep crawling of linked pages (default: True)
            max_depth: Maximum crawl depth (default: 10 = initial + 10 levels)
            max_pages: Maximum pages to crawl per URL (default: 200)
        """
        super().__init__(
            collector_name=standard_name,
            version=version,
            data_type="compliance",
            rate_limit=(100, 120),
            data_subdir="compliance",
            enable_deep_crawl=enable_deep_crawl,
            max_depth=max_depth,
            max_pages=max_pages,
            include_external=False,
            score_threshold=0.3,
        )
        self.standard_name = standard_name

    def get_validation_model(self) -> type[RawComplianceControl]:
        """Get compliance validation model.

        Returns:
            RawComplianceControl Pydantic model
        """
        return RawComplianceControl

    def get_deduplication_key(self, item: dict[str, Any]) -> tuple[str, ...]:
        """Get deduplication key for compliance control.

        Deduplicates based on control_id only, allowing merging of controls
        from different sources.

        Args:
            item: Control dictionary

        Returns:
            Tuple of (control_id,) for deduplication
        """
        control_id = (
            item.get("control_id")
            or item.get("benchmark_id")
            or item.get("article_id")
            or item.get("requirement_id")
            or ""
        )
        return (str(control_id),)

    def parse_data(
        self,
        response: str | BeautifulSoup | dict[str, Any] | list[dict[str, Any]],
        url: str,
    ) -> list[dict[str, Any]]:
        """Parse compliance controls from response.

        Delegates to parse_control() or parse_control_markdown() for backward compatibility.

        Args:
            response: Parsed response:
                - str: Markdown content (if use_markdown=True)
                - BeautifulSoup: Parsed HTML (if use_markdown=False)
                - dict/list: JSON data
            url: Source URL

        Returns:
            List of control dictionaries
        """
        if isinstance(response, str):
            return self.parse_control_markdown(response, url)
        elif isinstance(response, BeautifulSoup):
            return self.parse_control(response, url)
        elif isinstance(response, (dict, list)):
            return self.parse_control_json(response, url)
        else:
            return []

    def parse_control_markdown(self, markdown: str, url: str) -> list[dict[str, Any]]:
        """Parse controls from markdown content.

        Default implementation converts markdown to BeautifulSoup and calls parse_control().
        Override in subclasses for markdown-specific parsing.

        Args:
            markdown: Markdown content string
            url: Source URL

        Returns:
            List of control dictionaries
        """
        soup = BeautifulSoup(markdown, "html.parser")
        return self.parse_control(soup, url)

    def parse_control(self, soup: BeautifulSoup, url: str) -> list[dict[str, Any]]:
        """Parse controls from HTML page.

        Args:
            soup: Parsed BeautifulSoup object
            url: Source URL

        Returns:
            List of control dictionaries
        """
        raise NotImplementedError("Subclasses must implement parse_control()")

    def parse_control_json(
        self, data: dict[str, Any] | list[dict[str, Any]], url: str
    ) -> list[dict[str, Any]]:
        """Parse controls from JSON data.

        Default implementation returns empty list.
        Override in subclasses that handle JSON sources.

        Args:
            data: JSON data (dict or list)
            url: Source URL

        Returns:
            List of control dictionaries
        """
        _ = data, url
        return []

    def collect(self) -> list[dict[str, Any]]:
        """Collect all controls for this standard.

        Maintains backward compatibility by returning list instead of CollectionResult.

        Returns:
            List of raw control data dictionaries
        """
        result: CollectionResult = super().collect()
        return result.items

    def collect_with_result(self) -> CollectionResult:
        """Collect all controls and return full CollectionResult.

        Returns:
            CollectionResult with items, errors, and metrics
        """
        return super().collect()
