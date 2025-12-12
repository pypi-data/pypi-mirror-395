"""Compliance service - business logic for compliance operations."""

import logging
import time

from api.models.v1_requests import ComplianceRequirementsRequest
from api.models.v1_responses import (
    ComplianceControlResponse,
    ComplianceRequirementsResponse,
    ComplianceRequirementsSummary,
)
from api.database.async_mongodb import async_mongodb_adapter
from api.utils.resource_types import validate_resource_types, VALID_RESOURCE_TYPES
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.retry_utils import with_timeout_and_retry
from api.config import settings
from api.exceptions import ValidationError, DatabaseError, ExternalServiceError

logger = logging.getLogger(__name__)

FAILURE_RATE_THRESHOLD = 0.5


class ComplianceService:
    """Service for compliance operations."""

    def __init__(self):
        """Initialize compliance service."""
        self.mongodb_adapter = async_mongodb_adapter
        mcp_mongodb_client = MongoDBClient()
        self.vector_search = VectorSearch(
            mcp_mongodb_client,
            gemini_api_key=settings.gemini_api_key,
            pinecone_api_key=settings.pinecone_api_key,
            pinecone_index_name=settings.pinecone_index_name,
        )

    async def get_compliance_requirements(
        self, request: ComplianceRequirementsRequest, request_id: str | None = None
    ) -> ComplianceRequirementsResponse:
        """Get compliance requirements for infrastructure resources.

        Args:
            request: Compliance requirements request
            request_id: Optional request ID for tracing

        Returns:
            Compliance requirements response with controls and summary

        Raises:
            RuntimeError: If operation times out or fails, or if failure rate exceeds threshold
            ValueError: If request is invalid
        """
        start_time = time.time()

        if not request.resource_types:
            raise ValidationError(
                message="At least one resource type is required",
                user_message="Please specify at least one resource type (e.g., RDS, S3, EC2)",
                error_code="MISSING_RESOURCE_TYPES",
                details={"request_id": request_id}
            )

        valid_resource_types, invalid_resource_types = validate_resource_types(request.resource_types)

        # Log warning for invalid types but continue with valid ones
        # This allows the system to gracefully handle unknown resource types
        if invalid_resource_types:
            logger.info(
                "Unrecognized resource types (will be processed with generic compliance guidance): %s [request_id=%s]",
                invalid_resource_types,
                request_id or "unknown",
            )

        # If ALL types are invalid, use them anyway with generic compliance guidance
        # This ensures the system can handle any DevOps/Infrastructure resource type
        if not valid_resource_types:
            logger.info(
                "No pre-mapped resource types found. Using generic compliance search for: %s [request_id=%s]",
                request.resource_types,
                request_id or "unknown",
            )
            # Use the original resource types for semantic search even if not in our predefined list
            valid_resource_types = [rt.strip() for rt in request.resource_types if rt and rt.strip()]

        if request.standards:
            valid_standards = {
                "PCI-DSS", "HIPAA", "CIS", "SOC2", "NIST-800-53",
                "ISO-27001", "GDPR", "FedRAMP", "CCPA", "SOX", "GLBA",
            }
            invalid_standards = [s for s in request.standards if s not in valid_standards]
            if invalid_standards:
                logger.error(
                    "Invalid standards requested: %s. Valid standards: %s [request_id=%s]",
                    invalid_standards,
                    sorted(valid_standards),
                    request_id or "unknown",
                )
                raise ValidationError(
                    message=f"Invalid standards: {invalid_standards}",
                    user_message=f"Invalid compliance standards: {', '.join(invalid_standards)}. Valid standards: {', '.join(sorted(valid_standards))}",
                    error_code="INVALID_STANDARDS",
                    details={
                        "invalid_standards": invalid_standards,
                        "valid_standards": sorted(valid_standards),
                        "request_id": request_id
                    }
                )

        await self.mongodb_adapter.connect()

        query_parts = []
        for resource_type in valid_resource_types:
            query_parts.append(f"{resource_type} compliance")
        if request.standards:
            query_parts.extend([s.strip() for s in request.standards if s.strip()])

        if not query_parts:
            raise ValidationError(
                message="No valid query parts generated from request",
                user_message="Unable to generate search query from provided resource types and standards",
                error_code="INVALID_QUERY",
                details={"request_id": request_id, "resource_types": request.resource_types}
            )

        query = " ".join(query_parts)

        limit = getattr(request, "limit", None) or getattr(settings, "compliance_query_limit", 100)
        limit = min(max(limit, 1), 1000)

        try:
            results = await with_timeout_and_retry(
                self.vector_search.search_compliance,
                timeout_seconds=30.0,
                max_attempts=3,
                retryable_exceptions=(RuntimeError, ConnectionError, TimeoutError),
                query=query,
                standards=request.standards if request.standards else None,
                severity=request.severity,
                limit=limit,
            )
        except (RuntimeError, ConnectionError, TimeoutError) as e:
            logger.error("Vector search failed: %s", e, exc_info=True)
            raise ExternalServiceError(
                message=f"Search operation failed: {e}",
                user_message="Unable to search compliance requirements. Please try again later.",
                error_code="SEARCH_SERVICE_ERROR",
                details={"request_id": request_id, "operation": "vector_search"}
            ) from e

        if not results:
            logger.info("No compliance controls found for query: %s", query[:100])

        controls = []
        failed_count = 0
        for result in results:
            if not isinstance(result, dict):
                logger.warning("Invalid result type: %s", type(result))
                failed_count += 1
                continue

            try:
                control_id = result.get("control_id") or ""
                standard = result.get("standard") or ""
                title = result.get("title") or ""
                description = result.get("description") or ""

                if not control_id or not standard:
                    logger.warning("Missing required fields in result: control_id=%s, standard=%s", control_id, standard)
                    failed_count += 1
                    continue

                control = ComplianceControlResponse(
                    control_id=control_id,
                    standard=standard,
                    title=title,
                    description=description,
                    severity=result.get("severity", "MEDIUM"),
                    category=result.get("category"),
                    subcategory=result.get("subcategory"),
                    applies_to=result.get("applies_to", []) if isinstance(result.get("applies_to"), list) else [],
                    remediation=result.get("remediation") if request.include_remediation else None,
                    verification=result.get("verification") if request.include_verification else None,
                    references=result.get("references", []) if isinstance(result.get("references"), list) else [],
                    source_url=result.get("source_url"),
                )
                controls.append(control)
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                logger.warning("Failed to create control response: %s", e, exc_info=True)
                failed_count += 1
                continue

        failure_rate = failed_count / len(results) if results else 0.0

        if failed_count > 0:
            logger.warning(
                "Failed to process %d out of %d results (%.1f%% failure rate) [request_id=%s]",
                failed_count,
                len(results),
                failure_rate * 100,
                request_id or "unknown",
            )

            if failure_rate > FAILURE_RATE_THRESHOLD:
                error_msg = (
                    f"High failure rate detected: {failure_rate * 100:.1f}% "
                    f"(threshold: {FAILURE_RATE_THRESHOLD * 100}%). "
                    f"Only {len(controls)} out of {len(results)} results processed successfully."
                )
                logger.error("%s [request_id=%s]", error_msg, request_id or "unknown")
                raise RuntimeError(error_msg)

        by_severity: dict[str, int] = {}
        by_standard: dict[str, int] = {}

        for control in controls:
            by_severity[control.severity] = by_severity.get(control.severity, 0) + 1
            by_standard[control.standard] = by_standard.get(control.standard, 0) + 1

        summary = ComplianceRequirementsSummary(
            total=len(controls),
            by_severity=by_severity,
            by_standard=by_standard,
        )

        query_time_ms = int((time.time() - start_time) * 1000)

        metadata = {
            "query_time_ms": query_time_ms,
            "sources": list(set(control.source_url for control in controls if control.source_url)),
        }

        if request_id:
            metadata["request_id"] = request_id

        if failed_count > 0:
            metadata["failed_count"] = failed_count
            metadata["failure_rate"] = round(failure_rate, 4)
            metadata["total_results"] = len(results)
            metadata["successful_results"] = len(controls)

        return ComplianceRequirementsResponse(
            controls=controls,
            summary=summary,
            metadata=metadata,
        )
