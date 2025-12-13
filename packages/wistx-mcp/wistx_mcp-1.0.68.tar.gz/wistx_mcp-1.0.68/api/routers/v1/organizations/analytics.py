"""Organization usage analytics endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from api.dependencies.organization import (
    OrganizationContext,
    require_organization_member_from_path,
)
from api.models.organization_usage import (
    OrganizationQuotaStatus,
    OrganizationUsageSummary,
    OrganizationUsageTrends,
)
from api.services.organization_analytics_service import organization_analytics_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations/{org_id}/analytics", tags=["organization-analytics"])


@router.get("/usage", response_model=OrganizationUsageSummary)
async def get_organization_usage(
    org_id: str,
    start_date: Optional[datetime] = Query(default=None, description="Start date (ISO format)"),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"),
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)] = None,
) -> OrganizationUsageSummary:
    """Get organization usage summary with member breakdown.

    **CRITICAL**: Only organization members can view usage analytics.

    Args:
        org_id: Organization ID
        start_date: Start date for usage period
        end_date: End date for usage period
        days: Number of days to retrieve (default: 30)
        org_context: Organization context (ensures membership)

    Returns:
        Organization usage summary

    Raises:
        HTTPException: If organization not found or invalid date range
    """
    if not start_date:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
    elif not end_date:
        end_date = datetime.utcnow()

    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date",
        )

    try:
        return await organization_analytics_service.get_organization_usage_summary(
            organization_id=org_id,
            start_date=start_date,
            end_date=end_date,
        )
    except ValueError as e:
        logger.error("Error retrieving organization usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unexpected error retrieving organization usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve organization usage statistics",
        ) from e


@router.get("/usage/daily", response_model=OrganizationUsageTrends)
async def get_daily_organization_usage(
    org_id: str,
    days: int = Query(default=30, ge=1, le=365, description="Number of days to retrieve"),
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)] = None,
) -> OrganizationUsageTrends:
    """Get daily organization usage trends.

    **CRITICAL**: Only organization members can view usage analytics.

    Args:
        org_id: Organization ID
        days: Number of days to retrieve
        org_context: Organization context (ensures membership)

    Returns:
        Organization usage trends

    Raises:
        HTTPException: If organization not found
    """
    try:
        return await organization_analytics_service.get_daily_organization_usage(
            organization_id=org_id,
            days=days,
        )
    except ValueError as e:
        logger.error("Error retrieving daily organization usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unexpected error retrieving daily organization usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve daily organization usage statistics",
        ) from e


@router.get("/quota", response_model=OrganizationQuotaStatus)
async def get_organization_quota_status(
    org_id: str,
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)] = None,
) -> OrganizationQuotaStatus:
    """Get organization quota status with member breakdown.

    **CRITICAL**: Only organization members can view quota status.

    Args:
        org_id: Organization ID
        org_context: Organization context (ensures membership)

    Returns:
        Organization quota status

    Raises:
        HTTPException: If organization not found
    """
    try:
        return await organization_analytics_service.get_organization_quota_status(
            organization_id=org_id,
        )
    except ValueError as e:
        logger.error("Error retrieving organization quota status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unexpected error retrieving organization quota status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve organization quota status",
        ) from e


@router.get("/usage/export")
async def export_organization_usage(
    org_id: str,
    start_date: Optional[datetime] = Query(default=None, description="Start date (ISO format)"),
    end_date: Optional[datetime] = Query(default=None, description="End date (ISO format)"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to retrieve (if dates not provided)"),
    format: str = Query(default="csv", regex="^(csv|json)$", description="Export format (csv or json)"),
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)] = None,
) -> Response:
    """Export organization usage data.

    **CRITICAL**: Only organization members can export usage data.

    Args:
        org_id: Organization ID
        start_date: Start date for usage period
        end_date: End date for usage period
        days: Number of days to retrieve (default: 30)
        format: Export format (csv or json)
        org_context: Organization context (ensures membership)

    Returns:
        Exported usage data

    Raises:
        HTTPException: If organization not found or invalid date range
    """
    if not start_date:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
    elif not end_date:
        end_date = datetime.utcnow()

    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date",
        )

    try:
        usage_summary = await organization_analytics_service.get_organization_usage_summary(
            organization_id=org_id,
            start_date=start_date,
            end_date=end_date,
        )

        if format == "csv":
            import csv
            import io

            output = io.StringIO()
            writer = csv.writer(output)

            writer.writerow(["Organization Usage Export"])
            writer.writerow(["Organization ID", usage_summary.organization_id])
            writer.writerow(["Organization Name", usage_summary.organization_name])
            writer.writerow(["Plan", usage_summary.plan_id])
            writer.writerow(["Start Date", usage_summary.start_date.isoformat()])
            writer.writerow(["End Date", usage_summary.end_date.isoformat()])
            writer.writerow([])

            writer.writerow(["Summary"])
            writer.writerow(["Total Requests", usage_summary.total_requests])
            writer.writerow(["Successful Requests", usage_summary.successful_requests])
            writer.writerow(["Failed Requests", usage_summary.failed_requests])
            writer.writerow(["Success Rate (%)", f"{usage_summary.success_rate:.2f}"])
            writer.writerow(["Total Queries", usage_summary.queries.total_queries])
            writer.writerow(["Total Indexes", usage_summary.indexes.total_indexes])
            writer.writerow(["Total Storage (MB)", f"{usage_summary.indexes.storage_mb:.2f}"])
            writer.writerow([])

            writer.writerow(["Member Breakdown"])
            writer.writerow(
                [
                    "User ID",
                    "Email",
                    "Full Name",
                    "Role",
                    "Queries",
                    "Indexes",
                    "Storage (MB)",
                    "Total Requests",
                    "Success Rate (%)",
                ]
            )

            for member in usage_summary.member_breakdown:
                writer.writerow(
                    [
                        member.user_id,
                        member.email,
                        member.full_name or "",
                        member.role,
                        member.queries,
                        member.indexes,
                        f"{member.storage_mb:.2f}",
                        member.total_requests,
                        f"{member.success_rate:.2f}",
                    ]
                )

            csv_content = output.getvalue()
            output.close()

            return Response(
                content=csv_content,
                media_type="text/csv",
                headers={
                    "Content-Disposition": f'attachment; filename="organization_usage_{org_id}_{start_date.date()}_to_{end_date.date()}.csv"'
                },
            )
        else:
            import json

            json_content = json.dumps(usage_summary.model_dump(), indent=2, default=str)

            return Response(
                content=json_content,
                media_type="application/json",
                headers={
                    "Content-Disposition": f'attachment; filename="organization_usage_{org_id}_{start_date.date()}_to_{end_date.date()}.json"'
                },
            )
    except ValueError as e:
        logger.error("Error exporting organization usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unexpected error exporting organization usage: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export organization usage data",
        ) from e


@router.post("/alerts/check")
async def check_organization_usage_alerts(
    org_id: str,
    alert_threshold_percent: float = Query(default=80.0, ge=0.0, le=100.0, description="Alert threshold percentage"),
    critical_threshold_percent: float = Query(default=95.0, ge=0.0, le=100.0, description="Critical threshold percentage"),
    org_context: Annotated[OrganizationContext, Depends(require_organization_member_from_path)] = None,
) -> dict[str, Any]:
    """Check organization usage and create alerts if thresholds exceeded.

    **CRITICAL**: Only organization members can check usage alerts.

    Args:
        org_id: Organization ID
        alert_threshold_percent: Alert threshold percentage (default: 80%)
        critical_threshold_percent: Critical threshold percentage (default: 95%)
        org_context: Organization context (ensures membership)

    Returns:
        Dictionary with alerts created

    Raises:
        HTTPException: If organization not found
    """
    try:
        alerts_created = await organization_analytics_service.check_usage_alerts(
            organization_id=org_id,
            alert_threshold_percent=alert_threshold_percent,
            critical_threshold_percent=critical_threshold_percent,
        )

        return {
            "organization_id": org_id,
            "alerts_created": len(alerts_created),
            "alerts": alerts_created,
        }
    except ValueError as e:
        logger.error("Error checking organization usage alerts: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unexpected error checking organization usage alerts: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check organization usage alerts",
        ) from e

