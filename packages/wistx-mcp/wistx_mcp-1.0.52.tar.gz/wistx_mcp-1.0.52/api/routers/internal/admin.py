"""Internal admin endpoints for system operations."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from api.dependencies.auth import require_admin
from api.services.code_examples_cost_refresh_service import code_examples_cost_refresh_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/code-examples/refresh-costs",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Refresh cost data for code examples",
    description="Trigger a batch refresh of cost data for code examples. Use after pricing data updates.",
)
async def refresh_code_examples_costs(
    cloud_provider: str | None = Query(
        None,
        description="Filter by cloud provider (aws, gcp, azure)",
    ),
    batch_size: int = Query(
        100,
        ge=1,
        le=1000,
        description="Batch size for processing",
    ),
    max_examples: int | None = Query(
        None,
        ge=1,
        description="Maximum number of examples to refresh",
    ),
    current_user: dict[str, Any] = Depends(require_admin),
) -> dict[str, Any]:
    """Refresh cost data for code examples.
    
    Args:
        cloud_provider: Optional cloud provider filter
        batch_size: Batch size for processing
        max_examples: Maximum number of examples to refresh
        current_user: Current authenticated admin user
        
    Returns:
        Dictionary with refresh statistics
        
    Raises:
        HTTPException: If user is not authorized or refresh fails
    """
    
    try:
        stats = await code_examples_cost_refresh_service.refresh_costs_batch(
            cloud_provider=cloud_provider,
            batch_size=batch_size,
            max_examples=max_examples,
        )
        
        logger.info(
            "Cost refresh triggered by user %s: refreshed=%d, failed=%d",
            current_user.get("user_id"),
            stats["refreshed"],
            stats["failed"],
        )
        
        return {
            "status": "accepted",
            "message": "Cost refresh started",
            "statistics": stats,
        }
    except Exception as e:
        logger.error("Error triggering cost refresh: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger cost refresh: {str(e)}",
        ) from e


@router.get(
    "/code-examples/cost-status",
    summary="Get cost refresh status",
    description="Check the status of cost data freshness for code examples.",
)
async def get_cost_refresh_status(
    cloud_provider: str | None = Query(
        None,
        description="Filter by cloud provider (aws, gcp, azure)",
    ),
    current_user: dict[str, Any] = Depends(require_admin),
) -> dict[str, Any]:
    """Get cost refresh status.
    
    Args:
        cloud_provider: Optional cloud provider filter
        current_user: Current authenticated admin user
        
    Returns:
        Dictionary with cost refresh status information
    """
    
    try:
        latest_pricing_timestamp = await code_examples_cost_refresh_service.get_latest_pricing_timestamp(
            cloud_provider
        )
        
        from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
        
        async with MongoDBClient() as client:
            await client.connect()
            
            if client.database is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Database not available",
                )
            
            collection = client.database.code_examples
            
            query_filter: dict[str, Any] = {
                "cost_analysis": {"$exists": True},
            }
            
            if cloud_provider:
                query_filter["cloud_provider"] = cloud_provider.lower()
            
            total_with_costs = await collection.count_documents(query_filter)
            
            stale_count = 0
            if latest_pricing_timestamp:
                stale_query = query_filter.copy()
                stale_query["cost_analysis.analysis_timestamp"] = {
                    "$lt": latest_pricing_timestamp,
                }
                stale_count = await collection.count_documents(stale_query)
        
        return {
            "latest_pricing_timestamp": latest_pricing_timestamp.isoformat() if latest_pricing_timestamp else None,
            "total_examples_with_costs": total_with_costs,
            "stale_examples": stale_count,
            "fresh_examples": total_with_costs - stale_count,
            "cloud_provider": cloud_provider,
        }
    except Exception as e:
        logger.error("Error getting cost refresh status: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get cost refresh status: {str(e)}",
        ) from e

