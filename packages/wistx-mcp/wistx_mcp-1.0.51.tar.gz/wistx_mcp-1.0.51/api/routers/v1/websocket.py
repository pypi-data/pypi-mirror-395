"""WebSocket endpoints for real-time indexing updates.

This module provides WebSocket connections for streaming real-time progress
updates and activity events during indexing operations.
"""

import asyncio
import logging
from typing import Any
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from api.services.indexing_service import indexing_service
from api.models.indexing import ActivityType

logger = logging.getLogger(__name__)

router = APIRouter()


class IndexingConnectionManager:
    """Manages WebSocket connections for indexing updates."""

    def __init__(self) -> None:
        # Map of resource_id -> set of WebSocket connections
        self.active_connections: dict[str, set[WebSocket]] = {}
        # Map of user_id -> set of WebSocket connections (for global updates)
        self.user_connections: dict[str, set[WebSocket]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        resource_id: str | None = None,
        user_id: str | None = None,
    ) -> None:
        """Accept a new WebSocket connection.
        
        Args:
            websocket: The WebSocket connection
            resource_id: Optional resource ID for specific resource updates
            user_id: Optional user ID for all user's resource updates
        """
        await websocket.accept()
        
        if resource_id:
            if resource_id not in self.active_connections:
                self.active_connections[resource_id] = set()
            self.active_connections[resource_id].add(websocket)
            logger.info("WebSocket connected for resource: %s", resource_id)
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(websocket)
            logger.info("WebSocket connected for user: %s", user_id)

    def disconnect(
        self,
        websocket: WebSocket,
        resource_id: str | None = None,
        user_id: str | None = None,
    ) -> None:
        """Remove a WebSocket connection.
        
        Args:
            websocket: The WebSocket connection to remove
            resource_id: Optional resource ID
            user_id: Optional user ID
        """
        if resource_id and resource_id in self.active_connections:
            self.active_connections[resource_id].discard(websocket)
            if not self.active_connections[resource_id]:
                del self.active_connections[resource_id]
            logger.info("WebSocket disconnected for resource: %s", resource_id)
        
        if user_id and user_id in self.user_connections:
            self.user_connections[user_id].discard(websocket)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]
            logger.info("WebSocket disconnected for user: %s", user_id)

    async def send_resource_update(
        self,
        resource_id: str,
        data: dict[str, Any],
    ) -> None:
        """Send update to all connections subscribed to a resource.
        
        Args:
            resource_id: Resource ID to send update for
            data: Update data to send
        """
        if resource_id in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[resource_id]:
                try:
                    await connection.send_json(data)
                except Exception:
                    dead_connections.add(connection)
            
            # Clean up dead connections
            for conn in dead_connections:
                self.active_connections[resource_id].discard(conn)

    async def send_user_update(
        self,
        user_id: str,
        data: dict[str, Any],
    ) -> None:
        """Send update to all connections for a user.
        
        Args:
            user_id: User ID to send update for
            data: Update data to send
        """
        if user_id in self.user_connections:
            dead_connections = set()
            for connection in self.user_connections[user_id]:
                try:
                    await connection.send_json(data)
                except Exception:
                    dead_connections.add(connection)
            
            # Clean up dead connections
            for conn in dead_connections:
                self.user_connections[user_id].discard(conn)

    async def broadcast_activity(
        self,
        resource_id: str,
        user_id: str,
        activity: dict[str, Any],
    ) -> None:
        """Broadcast an activity to both resource and user subscribers.
        
        Args:
            resource_id: Resource ID
            user_id: User ID
            activity: Activity data
        """
        message = {
            "type": "activity",
            "resource_id": resource_id,
            "activity": activity,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self.send_resource_update(resource_id, message)
        await self.send_user_update(user_id, message)

    async def broadcast_progress(
        self,
        resource_id: str,
        user_id: str,
        progress: float,
        status: str,
        files_processed: int | None = None,
        total_files: int | None = None,
        articles_indexed: int | None = None,
    ) -> None:
        """Broadcast progress update to subscribers.
        
        Args:
            resource_id: Resource ID
            user_id: User ID
            progress: Progress percentage (0-100)
            status: Current status
            files_processed: Number of files processed
            total_files: Total number of files
            articles_indexed: Number of articles indexed
        """
        message = {
            "type": "progress",
            "resource_id": resource_id,
            "progress": progress,
            "status": status,
            "files_processed": files_processed,
            "total_files": total_files,
            "articles_indexed": articles_indexed,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self.send_resource_update(resource_id, message)
        await self.send_user_update(user_id, message)


# Global connection manager instance
connection_manager = IndexingConnectionManager()


@router.websocket("/ws/indexing/{resource_id}")
async def websocket_indexing_resource(
    websocket: WebSocket,
    resource_id: str,
    token: str = Query(default=""),
) -> None:
    """WebSocket endpoint for real-time updates on a specific resource.

    Connects to receive real-time progress and activity updates for a specific
    indexing resource.

    Args:
        websocket: WebSocket connection
        resource_id: Resource ID to subscribe to
        token: Optional authentication token (for future use)
    """
    # Note: For now, we don't authenticate WebSocket connections
    # In production, you'd validate the token and extract user_id
    user_id = None  # Would be extracted from token validation

    await connection_manager.connect(websocket, resource_id=resource_id, user_id=user_id)

    try:
        # Send initial state
        resource = await indexing_service.get_resource_by_id_internal(resource_id)
        if resource:
            await websocket.send_json({
                "type": "initial",
                "resource_id": resource_id,
                "status": resource.status.value,
                "progress": resource.progress or 0,
                "files_processed": resource.files_processed,
                "total_files": resource.total_files,
                "articles_indexed": resource.articles_indexed,
                "timestamp": datetime.utcnow().isoformat(),
            })

        # Keep connection alive and listen for client messages
        while True:
            try:
                # Wait for any message (ping/pong or client commands)
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0  # 30 second timeout for keepalive
                )

                # Handle ping/pong
                if data == "ping":
                    await websocket.send_text("pong")

            except asyncio.TimeoutError:
                # Send keepalive ping
                try:
                    await websocket.send_text("ping")
                except Exception:
                    break

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected for resource: %s", resource_id)
    except Exception as e:
        logger.error("WebSocket error for resource %s: %s", resource_id, e)
    finally:
        connection_manager.disconnect(websocket, resource_id=resource_id, user_id=user_id)


@router.websocket("/ws/indexing/user/{user_id}")
async def websocket_indexing_user(
    websocket: WebSocket,
    user_id: str,
    token: str = Query(default=""),
) -> None:
    """WebSocket endpoint for real-time updates on all user's resources.

    Connects to receive real-time progress and activity updates for all
    indexing resources belonging to a user.

    Args:
        websocket: WebSocket connection
        user_id: User ID to subscribe to
        token: Optional authentication token (for future use)
    """
    await connection_manager.connect(websocket, user_id=user_id)

    try:
        # Send initial state of all active indexing jobs
        resources = await indexing_service.list_resources(user_id=user_id)
        active_resources = [
            r for r in resources
            if r.status.value in ['pending', 'indexing']
        ]

        await websocket.send_json({
            "type": "initial",
            "active_jobs": [
                {
                    "resource_id": r.resource_id,
                    "name": r.name,
                    "resource_type": r.resource_type.value,
                    "status": r.status.value,
                    "progress": r.progress or 0,
                    "files_processed": r.files_processed,
                    "total_files": r.total_files,
                    "articles_indexed": r.articles_indexed,
                }
                for r in active_resources
            ],
            "timestamp": datetime.utcnow().isoformat(),
        })

        # Keep connection alive
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )

                if data == "ping":
                    await websocket.send_text("pong")

            except asyncio.TimeoutError:
                try:
                    await websocket.send_text("ping")
                except Exception:
                    break

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected for user: %s", user_id)
    except Exception as e:
        logger.error("WebSocket error for user %s: %s", user_id, e)
    finally:
        connection_manager.disconnect(websocket, user_id=user_id)

