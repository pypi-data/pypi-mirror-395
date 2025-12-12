"""Monitoring and metrics for data processing pipeline."""

import gc
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from ..utils.logger import setup_logger

logger = setup_logger(__name__)

try:
    from prometheus_client import Counter, Gauge, Histogram
except ImportError:
    logger.warning("Prometheus client not installed. Metrics will be disabled.")
    Counter = None
    Gauge = None
    Histogram = None


@dataclass
class StageMetrics:
    """Metrics for a pipeline stage."""

    stage_name: str
    items_processed: int = 0
    items_succeeded: int = 0
    items_failed: int = 0
    duration_seconds: float = 0.0
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    errors: list[dict[str, Any]] = field(default_factory=list)

    def finish(self):
        """Mark stage as finished."""
        self.end_time = time.time()
        self.duration_seconds = self.end_time - self.start_time

    def items_per_second(self) -> float:
        """Calculate items processed per second."""
        if self.duration_seconds == 0:
            return 0.0
        return self.items_processed / self.duration_seconds

    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.items_processed == 0:
            return 0.0
        return self.items_succeeded / self.items_processed


class PipelineMetrics:
    """Metrics collector for data processing pipeline.

    Tracks metrics for all pipeline stages and provides Prometheus integration.
    """

    def __init__(self, enable_prometheus: bool = True):
        """Initialize metrics collector.

        Args:
            enable_prometheus: Enable Prometheus metrics (requires prometheus_client)
        """
        self.enable_prometheus = enable_prometheus and Counter is not None
        self.stage_metrics: dict[str, StageMetrics] = {}

        if self.enable_prometheus:
            self.items_processed = Counter(
                "pipeline_items_processed_total",
                "Total items processed",
                ["stage", "data_type"],
            )
            self.items_succeeded = Counter(
                "pipeline_items_succeeded_total",
                "Total items succeeded",
                ["stage", "data_type"],
            )
            self.items_failed = Counter(
                "pipeline_items_failed_total",
                "Total items failed",
                ["stage", "data_type"],
            )
            self.stage_duration = Histogram(
                "pipeline_stage_duration_seconds",
                "Stage processing duration",
                ["stage", "data_type"],
            )
            self.items_in_queue = Gauge(
                "pipeline_items_in_queue",
                "Items waiting to be processed",
                ["stage", "data_type"],
            )
            self.pipeline_errors = Counter(
                "pipeline_errors_total",
                "Total pipeline errors",
                ["stage", "error_type"],
            )
            self.bulk_operation_duration = Histogram(
                "pipeline_bulk_operation_duration_seconds",
                "Bulk operation duration",
                ["operation_type", "collection"],
            )
            self.bulk_operation_size = Histogram(
                "pipeline_bulk_operation_size",
                "Bulk operation batch size",
                ["operation_type", "collection"],
            )
            self.memory_usage_bytes = Gauge(
                "pipeline_memory_usage_bytes",
                "Memory usage in bytes",
                ["stage"],
            )
            self.database_query_duration = Histogram(
                "pipeline_database_query_duration_seconds",
                "Database query duration",
                ["query_type", "collection"],
            )

    def start_stage(self, stage_name: str, data_type: str = "compliance") -> StageMetrics:
        """Start tracking a pipeline stage.

        Args:
            stage_name: Name of the stage (collection, processing, embedding, loading)
            data_type: Type of data being processed

        Returns:
            StageMetrics object
        """
        metrics = StageMetrics(stage_name=stage_name)
        key = f"{stage_name}_{data_type}"
        self.stage_metrics[key] = metrics

        logger.info("Starting stage: %s (%s)", stage_name, data_type)

        return metrics

    def record_item_processed(
        self, stage_name: str, data_type: str = "compliance", success: bool = True
    ):
        """Record a processed item.

        Args:
            stage_name: Name of the stage
            data_type: Type of data
            success: Whether processing succeeded
        """
        key = f"{stage_name}_{data_type}"
        if key not in self.stage_metrics:
            self.start_stage(stage_name, data_type)

        metrics = self.stage_metrics[key]
        metrics.items_processed += 1

        if success:
            metrics.items_succeeded += 1
        else:
            metrics.items_failed += 1

        if self.enable_prometheus:
            self.items_processed.labels(stage=stage_name, data_type=data_type).inc()
            if success:
                self.items_succeeded.labels(stage=stage_name, data_type=data_type).inc()
            else:
                self.items_failed.labels(stage=stage_name, data_type=data_type).inc()

    def record_error(
        self, stage_name: str, error_type: str, error_message: str, data_type: str = "compliance"
    ):
        """Record an error.

        Args:
            stage_name: Name of the stage
            error_type: Type of error
            error_message: Error message
            data_type: Type of data
        """
        key = f"{stage_name}_{data_type}"
        if key not in self.stage_metrics:
            self.start_stage(stage_name, data_type)

        metrics = self.stage_metrics[key]
        metrics.errors.append(
            {
                "error_type": error_type,
                "error_message": error_message,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        if self.enable_prometheus:
            self.pipeline_errors.labels(stage=stage_name, error_type=error_type).inc()

    def finish_stage(self, stage_name: str, data_type: str = "compliance"):
        """Finish tracking a pipeline stage.

        Args:
            stage_name: Name of the stage
            data_type: Type of data
        """
        key = f"{stage_name}_{data_type}"
        if key in self.stage_metrics:
            metrics = self.stage_metrics[key]
            metrics.finish()

            if self.enable_prometheus:
                self.stage_duration.labels(stage=stage_name, data_type=data_type).observe(
                    metrics.duration_seconds
                )

            logger.info(
                "Finished stage: %s (%s) - Processed: %d, Succeeded: %d, Failed: %d, Duration: %.2fs, Rate: %.2f items/s",
                stage_name,
                data_type,
                metrics.items_processed,
                metrics.items_succeeded,
                metrics.items_failed,
                metrics.duration_seconds,
                metrics.items_per_second(),
            )

    def get_stage_metrics(self, stage_name: str, data_type: str = "compliance") -> StageMetrics | None:
        """Get metrics for a specific stage.

        Args:
            stage_name: Name of the stage
            data_type: Type of data

        Returns:
            StageMetrics object or None if not found
        """
        key = f"{stage_name}_{data_type}"
        return self.stage_metrics.get(key)

    def get_summary(self) -> dict[str, Any]:
        """Get summary of all metrics.

        Returns:
            Dictionary with summary statistics
        """
        summary = {
            "stages": {},
            "total_items_processed": 0,
            "total_items_succeeded": 0,
            "total_items_failed": 0,
            "total_duration_seconds": 0.0,
        }

        for key, metrics in self.stage_metrics.items():
            summary["stages"][key] = {
                "items_processed": metrics.items_processed,
                "items_succeeded": metrics.items_succeeded,
                "items_failed": metrics.items_failed,
                "duration_seconds": metrics.duration_seconds,
                "items_per_second": metrics.items_per_second(),
                "success_rate": metrics.success_rate(),
                "error_count": len(metrics.errors),
            }

            summary["total_items_processed"] += metrics.items_processed
            summary["total_items_succeeded"] += metrics.items_succeeded
            summary["total_items_failed"] += metrics.items_failed
            summary["total_duration_seconds"] += metrics.duration_seconds

        return summary

    def record_bulk_operation(
        self,
        operation_type: str,
        collection: str,
        batch_size: int,
        duration_seconds: float,
    ):
        """Record bulk operation metrics.

        Args:
            operation_type: Type of operation (insert, update, upsert)
            collection: Collection name
            batch_size: Number of operations in batch
            duration_seconds: Duration of operation
        """
        if self.enable_prometheus:
            self.bulk_operation_duration.labels(
                operation_type=operation_type, collection=collection
            ).observe(duration_seconds)
            self.bulk_operation_size.labels(
                operation_type=operation_type, collection=collection
            ).observe(batch_size)

    def record_database_query(
        self,
        query_type: str,
        collection: str,
        duration_seconds: float,
    ):
        """Record database query metrics.

        Args:
            query_type: Type of query (find, find_one, bulk_write)
            collection: Collection name
            duration_seconds: Duration of query
        """
        if self.enable_prometheus:
            self.database_query_duration.labels(
                query_type=query_type, collection=collection
            ).observe(duration_seconds)

    def record_memory_usage(self, stage_name: str):
        """Record memory usage for a stage.

        Args:
            stage_name: Name of the stage
        """
        if self.enable_prometheus:
            try:
                import psutil
                import os

                process = psutil.Process(os.getpid())
                memory_bytes = process.memory_info().rss
                self.memory_usage_bytes.labels(stage=stage_name).set(memory_bytes)
            except ImportError:
                pass
            except Exception as e:
                logger.debug("Failed to record memory usage: %s", e)


class HealthCheck:
    """Health check for pipeline components."""

    def __init__(self):
        """Initialize health check."""
        self.checks: dict[str, bool] = {}

    async def check_mongodb(self, mongodb_manager) -> bool:
        """Check MongoDB health.

        Args:
            mongodb_manager: MongoDB manager instance

        Returns:
            True if healthy, False otherwise
        """
        try:
            is_healthy = mongodb_manager.is_healthy()
            self.checks["mongodb"] = is_healthy
            return is_healthy
        except (ValueError, RuntimeError, AttributeError) as e:
            logger.error("MongoDB health check failed: %s", e)
            self.checks["mongodb"] = False
            return False

    async def check_pinecone(self, pinecone_loader) -> bool:
        """Check Pinecone health.

        Args:
            pinecone_loader: Pinecone loader instance

        Returns:
            True if healthy, False otherwise
        """
        try:
            pinecone_loader.index.describe_index_stats()
            self.checks["pinecone"] = True
            return True
        except (ValueError, RuntimeError, AttributeError) as e:
            logger.error("Pinecone health check failed: %s", e)
            self.checks["pinecone"] = False
            return False

    async def check_gemini(self, gemini_client) -> bool:
        """Check Gemini API health.

        Args:
            gemini_client: Gemini client instance

        Returns:
            True if healthy, False otherwise
        """
        try:
            if gemini_client and gemini_client.is_available():
                await gemini_client.create_embedding("test")
                self.checks["gemini"] = True
                return True
            self.checks["gemini"] = False
            return False
        except (ValueError, RuntimeError, AttributeError) as e:
            logger.error("Gemini health check failed: %s", e)
            self.checks["gemini"] = False
            return False

    def get_health_status(self) -> dict[str, Any]:
        """Get overall health status.

        Returns:
            Dictionary with health status
        """
        all_healthy = all(self.checks.values())

        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": self.checks.copy(),
            "timestamp": datetime.utcnow().isoformat(),
        }

