"""User notifications endpoints."""

import logging
from datetime import datetime
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from api.database.mongodb import mongodb_manager
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationResponse(BaseModel):
    """Notification response model."""

    notification_id: str
    type: str
    title: str
    message: str
    resource_id: str | None = None
    read: bool
    created_at: str


class NotificationListResponse(BaseModel):
    """List of notifications response."""

    notifications: list[NotificationResponse]
    unread_count: int
    total: int


@router.get("", response_model=NotificationListResponse)
async def get_notifications(
    limit: int = 20,
    unread_only: bool = False,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> NotificationListResponse:
    """Get user notifications.

    Args:
        limit: Maximum notifications to return
        unread_only: Only return unread notifications
        current_user: Current authenticated user

    Returns:
        List of notifications with counts
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    db = mongodb_manager.get_database()
    collection = db.user_notifications

    query: dict[str, Any] = {"user_id": ObjectId(user_id)}
    if unread_only:
        query["read"] = False

    notifications = list(
        collection.find(query).sort("created_at", -1).limit(limit)
    )

    unread_count = collection.count_documents(
        {"user_id": ObjectId(user_id), "read": False}
    )
    total = collection.count_documents({"user_id": ObjectId(user_id)})

    return NotificationListResponse(
        notifications=[
            NotificationResponse(
                notification_id=str(n["_id"]),
                type=n.get("type", "general"),
                title=n.get("title", ""),
                message=n.get("message", ""),
                resource_id=n.get("resource_id"),
                read=n.get("read", False),
                created_at=n.get("created_at", datetime.utcnow()).isoformat(),
            )
            for n in notifications
        ],
        unread_count=unread_count,
        total=total,
    )


@router.post("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, bool]:
    """Mark a notification as read."""
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found")

    db = mongodb_manager.get_database()
    collection = db.user_notifications

    result = collection.update_one(
        {"_id": ObjectId(notification_id), "user_id": ObjectId(user_id)},
        {"$set": {"read": True, "read_at": datetime.utcnow()}},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    return {"success": True}


@router.post("/read-all")
async def mark_all_as_read(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, int]:
    """Mark all notifications as read."""
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found")

    db = mongodb_manager.get_database()
    collection = db.user_notifications

    result = collection.update_many(
        {"user_id": ObjectId(user_id), "read": False},
        {"$set": {"read": True, "read_at": datetime.utcnow()}},
    )

    return {"marked_count": result.modified_count}

