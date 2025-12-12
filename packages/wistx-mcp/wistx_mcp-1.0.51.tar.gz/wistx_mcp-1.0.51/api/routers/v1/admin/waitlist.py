"""Admin waitlist management endpoints."""

import logging
from datetime import datetime
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from api.dependencies.auth import require_admin
from api.database.mongodb import mongodb_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/waitlist", tags=["admin"])


class WaitlistEntryResponse(BaseModel):
    """Waitlist entry response model."""

    id: str = Field(..., description="Entry ID")
    email: str = Field(..., description="Email address")
    name: str | None = Field(None, description="User name")
    created_at: datetime = Field(..., description="Signup timestamp")
    status: str = Field(..., description="Status (pending, approved, rejected)")
    position: int | None = Field(None, description="Position in waitlist")


class WaitlistListResponse(BaseModel):
    """Waitlist list response model."""

    entries: list[WaitlistEntryResponse] = Field(..., description="Waitlist entries")
    total: int = Field(..., description="Total count")
    pending_count: int = Field(..., description="Pending count")
    approved_count: int = Field(..., description="Approved count")


class WaitlistUpdateRequest(BaseModel):
    """Waitlist update request model."""

    status: str = Field(..., description="New status (pending, approved, rejected)")


class BulkApproveRequest(BaseModel):
    """Bulk approve request model."""

    entry_ids: list[str] = Field(..., description="List of entry IDs to approve")


@router.get("/", response_model=WaitlistListResponse, summary="List waitlist entries")
async def list_waitlist(
    status_filter: str | None = Query(None, alias="status", description="Filter by status"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    current_user: dict[str, Any] = Depends(require_admin),
) -> WaitlistListResponse:
    """List waitlist entries with filters and pagination.

    Args:
        status_filter: Status filter (pending, approved, rejected)
        limit: Result limit
        offset: Result offset
        current_user: Current admin user

    Returns:
        Waitlist list response
    """
    try:
        db = mongodb_manager.get_database()
        waitlist_collection = db.waitlist

        query = {}
        if status_filter:
            query["status"] = status_filter

        total = waitlist_collection.count_documents(query)
        pending_count = waitlist_collection.count_documents({"status": "pending"})
        approved_count = waitlist_collection.count_documents({"status": "approved"})

        cursor = waitlist_collection.find(query).sort("created_at", 1).skip(offset).limit(limit)
        entries_data = list(cursor)

        entries = []
        for idx, entry in enumerate(entries_data):
            entries.append(
                WaitlistEntryResponse(
                    id=str(entry["_id"]),
                    email=entry.get("email", ""),
                    name=entry.get("name"),
                    created_at=entry.get("created_at", datetime.utcnow()),
                    status=entry.get("status", "pending"),
                    position=offset + idx + 1,
                )
            )

        return WaitlistListResponse(
            entries=entries,
            total=total,
            pending_count=pending_count,
            approved_count=approved_count,
        )

    except Exception as e:
        logger.error("Error listing waitlist: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list waitlist entries",
        ) from e


@router.patch(
    "/{entry_id}",
    response_model=WaitlistEntryResponse,
    summary="Update waitlist entry status",
)
async def update_waitlist_entry(
    entry_id: str,
    request: WaitlistUpdateRequest,
    current_user: dict[str, Any] = Depends(require_admin),
) -> WaitlistEntryResponse:
    """Update waitlist entry status.

    Args:
        entry_id: Waitlist entry ID
        request: Update request
        current_user: Current admin user

    Returns:
        Updated waitlist entry

    Raises:
        HTTPException: If entry not found or invalid status
    """
    if request.status not in ["pending", "approved", "rejected"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Must be one of: pending, approved, rejected",
        )

    try:
        db = mongodb_manager.get_database()
        waitlist_collection = db.waitlist

        entry = waitlist_collection.find_one({"_id": ObjectId(entry_id)})
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Waitlist entry not found",
            )

        waitlist_collection.update_one(
            {"_id": ObjectId(entry_id)},
            {"$set": {"status": request.status, "updated_at": datetime.utcnow()}},
        )

        updated_entry = waitlist_collection.find_one({"_id": ObjectId(entry_id)})

        logger.info(
            "Waitlist entry %s updated to status: %s by admin %s",
            entry_id,
            request.status,
            current_user.get("user_id"),
        )

        return WaitlistEntryResponse(
            id=str(updated_entry["_id"]),
            email=updated_entry.get("email", ""),
            name=updated_entry.get("name"),
            created_at=updated_entry.get("created_at", datetime.utcnow()),
            status=updated_entry.get("status", "pending"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating waitlist entry: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update waitlist entry",
        ) from e


@router.post(
    "/bulk-approve",
    response_model=dict[str, Any],
    summary="Bulk approve waitlist entries",
)
async def bulk_approve_waitlist(
    request: BulkApproveRequest,
    current_user: dict[str, Any] = Depends(require_admin),
) -> dict[str, Any]:
    """Bulk approve waitlist entries.

    Args:
        request: Bulk approve request
        current_user: Current admin user

    Returns:
        Bulk approve result
    """
    try:
        db = mongodb_manager.get_database()
        waitlist_collection = db.waitlist

        entry_ids = [ObjectId(eid) for eid in request.entry_ids]

        result = waitlist_collection.update_many(
            {"_id": {"$in": entry_ids}},
            {"$set": {"status": "approved", "updated_at": datetime.utcnow()}},
        )

        logger.info(
            "Bulk approved %d waitlist entries by admin %s",
            result.modified_count,
            current_user.get("user_id"),
        )

        return {
            "approved_count": result.modified_count,
            "total_requested": len(request.entry_ids),
        }

    except Exception as e:
        logger.error("Error bulk approving waitlist: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to bulk approve waitlist entries",
        ) from e

