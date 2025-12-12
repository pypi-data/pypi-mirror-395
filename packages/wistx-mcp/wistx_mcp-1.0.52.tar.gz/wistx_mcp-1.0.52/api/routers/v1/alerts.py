"""Alert management endpoints."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from api.models.alert_preferences import AlertPreferences
from api.services.alert_service import alert_service
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get(
    "/budgets/{budget_id}",
    response_model=list[dict[str, Any]],
    summary="Get budget alerts",
    description="Get all alerts for a specific budget.",
)
async def get_budget_alerts(
    budget_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    """Get alerts for a budget.

    Args:
        budget_id: Budget ID
        current_user: Current authenticated user

    Returns:
        List of alerts

    Raises:
        HTTPException: If user ID not found or database error occurs
    """
    try:
        user_id = current_user.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in authentication token",
            )

        from api.database.mongodb import mongodb_manager

        db = mongodb_manager.get_database()
        collection = db.budget_alerts

        alerts = list(
            collection.find({"budget_id": budget_id, "user_id": ObjectId(user_id)})
            .sort("created_at", -1)
            .limit(100)
        )

        for alert in alerts:
            if "_id" in alert:
                alert["alert_id"] = str(alert["_id"])
                del alert["_id"]
            if "user_id" in alert:
                alert["user_id"] = str(alert["user_id"])

        return alerts
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error fetching budget alerts: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch alerts: {str(e)}",
        ) from e


@router.post("/preferences")
async def update_alert_preferences(
    preferences: AlertPreferences,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AlertPreferences:
    """Update user alert preferences.

    Args:
        preferences: Alert preferences
        current_user: Current authenticated user

    Returns:
        Updated preferences
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token",
        )

    if preferences.user_id != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update preferences for another user",
        )

    from api.database.mongodb import mongodb_manager

    db = mongodb_manager.get_database()
    collection = db.alert_preferences

    preferences_dict = preferences.model_dump()
    preferences_dict["user_id"] = ObjectId(user_id)

    collection.replace_one(
        {"user_id": ObjectId(user_id), "budget_id": preferences.budget_id},
        preferences_dict,
        upsert=True,
    )

    return preferences


@router.get("/preferences")
async def get_alert_preferences(
    budget_id: str | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> AlertPreferences:
    """Get user alert preferences.

    Args:
        budget_id: Budget ID (optional, for budget-specific preferences)
        current_user: Current authenticated user

    Returns:
        Alert preferences
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in authentication token",
        )

    from api.database.mongodb import mongodb_manager

    db = mongodb_manager.get_database()
    collection = db.alert_preferences

    query = {"user_id": ObjectId(user_id)}
    if budget_id:
        query["budget_id"] = budget_id
    else:
        query["budget_id"] = None

    preferences = collection.find_one(query)

    if not preferences:
        return AlertPreferences(user_id=str(user_id), budget_id=budget_id)

    preferences["user_id"] = str(preferences["user_id"])
    return AlertPreferences(**preferences)

