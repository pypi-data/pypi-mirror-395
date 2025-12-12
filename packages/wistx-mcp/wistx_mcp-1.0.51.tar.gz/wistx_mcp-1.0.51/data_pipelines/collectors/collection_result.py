"""Collection result and metrics classes for universal collectors."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class CollectionMetrics:
    """Metrics for a collection run."""

    total_urls: int = 0
    successful_urls: int = 0
    failed_urls: int = 0
    total_items_collected: int = 0
    items_after_deduplication: int = 0
    validation_errors: int = 0
    parsing_errors: int = 0
    network_errors: int = 0
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: datetime | None = None
    duration_seconds: float = 0.0
    field_completeness: dict[str, float] = field(default_factory=dict)

    def calculate_duration(self) -> None:
        """Calculate collection duration."""
        if self.end_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()

    def get_success_rate(self) -> float:
        """Calculate URL success rate.

        Returns:
            Success rate as float between 0.0 and 1.0
        """
        if self.total_urls == 0:
            return 0.0
        return self.successful_urls / self.total_urls

    def get_completeness_score(self) -> float:
        """Calculate overall completeness score.

        Returns:
            Completeness score as float between 0.0 and 1.0
        """
        if self.total_items_collected == 0:
            return 0.0
        return (self.items_after_deduplication - self.validation_errors) / self.total_items_collected

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary.

        Returns:
            Dictionary representation of metrics
        """
        return {
            "total_urls": self.total_urls,
            "successful_urls": self.successful_urls,
            "failed_urls": self.failed_urls,
            "success_rate": self.get_success_rate(),
            "total_items_collected": self.total_items_collected,
            "items_after_deduplication": self.items_after_deduplication,
            "validation_errors": self.validation_errors,
            "parsing_errors": self.parsing_errors,
            "network_errors": self.network_errors,
            "duration_seconds": self.duration_seconds,
            "completeness_score": self.get_completeness_score(),
            "field_completeness": self.field_completeness,
        }


@dataclass
class CollectionError:
    """Represents a collection error."""

    url: str
    error_type: str
    error_message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    attempt_number: int = 1

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary.

        Returns:
            Dictionary representation of error
        """
        return {
            "url": self.url,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat(),
            "attempt_number": self.attempt_number,
        }


@dataclass
class CollectionResult:
    """Result of a collection run."""

    collector_name: str
    version: str
    success: bool
    items: list[dict[str, Any]] = field(default_factory=list)
    errors: list[CollectionError] = field(default_factory=list)
    metrics: CollectionMetrics = field(default_factory=CollectionMetrics)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_error(
        self,
        url: str,
        error_type: str,
        error_message: str,
        attempt_number: int = 1,
    ) -> None:
        """Add an error to the result.

        Args:
            url: URL that failed
            error_type: Type of error (network, parsing, validation, etc.)
            error_message: Error message
            attempt_number: Attempt number (for retries)
        """
        error = CollectionError(
            url=url,
            error_type=error_type,
            error_message=error_message,
            attempt_number=attempt_number,
        )
        self.errors.append(error)

    def finalize(self) -> None:
        """Finalize the result and calculate metrics."""
        self.metrics.end_time = datetime.utcnow()
        self.metrics.calculate_duration()
        self.metrics.items_after_deduplication = len(self.items)
        self.success = (
            len(self.errors) == 0
            and self.metrics.successful_urls > 0
            and len(self.items) > 0
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary.

        Returns:
            Dictionary representation of result
        """
        return {
            "collector_name": self.collector_name,
            "version": self.version,
            "success": self.success,
            "items_count": len(self.items),
            "errors_count": len(self.errors),
            "metrics": self.metrics.to_dict(),
            "errors": [e.to_dict() for e in self.errors],
            "metadata": self.metadata,
        }

