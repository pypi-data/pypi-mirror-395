"""Research sessions endpoints for v1 API.

Manages user research sessions for on-demand knowledge research.
"""

import logging
import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from api.models.v1_responses import APIResponse, ErrorResponse
from api.services.research_orchestrator import ResearchOrchestrator
from api.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/research-sessions", tags=["research-sessions"])


class ResearchRequest(BaseModel):
    """Request model for initiating research."""
    query: str = Field(..., min_length=10, max_length=5000, description="Research query")
    url: str | None = Field(None, description="Optional URL to research directly")
    max_sources: int = Field(5, ge=1, le=10, description="Maximum sources to process")
    generate_context: bool = Field(True, description="Generate LLM context for chunks")


class DeleteSessionRequest(BaseModel):
    """Request model for deleting a session."""
    session_id: str = Field(..., description="Session ID to delete")


@router.post(
    "/research",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Initiate on-demand research",
    description="Research documentation using contextual retrieval approach",
)
async def initiate_research(
    request: ResearchRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Initiate on-demand research.
    
    Uses Anthropic's contextual retrieval approach to:
    1. Analyze intent and discover sources
    2. Fetch and chunk content with LLM context
    3. Index for hybrid retrieval
    4. Store in user-scoped knowledge base
    """
    request_id = getattr(http_request.state, "request_id", "")
    start_time = time.time()
    user_id = current_user.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
        )
    
    try:
        orchestrator = ResearchOrchestrator()
        result = await orchestrator.research(
            query=request.query,
            user_id=user_id,
            url=request.url,
            max_sources=request.max_sources,
            generate_context=request.generate_context,
        )
        
        query_time_ms = int((time.time() - start_time) * 1000)
        
        return APIResponse(
            data={
                "session_id": result.session.session_id,
                "status": result.session.status,
                "sources_processed": result.sources_processed,
                "chunks_indexed": result.chunks_indexed,
                "sources": result.session.sources,
                "errors": result.errors if result.errors else None,
                "intent_analysis": {
                    "technologies": result.intent_analysis.technologies,
                    "task_type": result.intent_analysis.task_type,
                } if result.intent_analysis else None,
            },
            metadata={
                "request_id": request_id,
                "timestamp": time.time(),
                "query_time_ms": query_time_ms,
            },
        )
    except Exception as e:
        logger.error("Research failed: %s | Request-ID: %s", e, request_id, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Research failed: {str(e)}",
        )


@router.get(
    "/",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="List research sessions",
    description="Get user's research sessions",
)
async def list_sessions(
    http_request: Request,
    limit: int = 20,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """List user's research sessions."""
    request_id = getattr(http_request.state, "request_id", "")
    user_id = current_user.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
        )
    
    try:
        orchestrator = ResearchOrchestrator()
        sessions = await orchestrator.get_user_sessions(user_id, limit=limit)
        
        # Convert ObjectId to string for JSON serialization
        for session in sessions:
            if "_id" in session:
                session["_id"] = str(session["_id"])
        
        return APIResponse(
            data={"sessions": sessions, "total": len(sessions)},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
    except Exception as e:
        logger.error("Failed to list sessions: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}",
        )


@router.get(
    "/{session_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get research session",
    description="Get status and details of a research session",
)
async def get_session(
    session_id: str,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Get a research session by ID."""
    request_id = getattr(http_request.state, "request_id", "")
    user_id = current_user.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
        )
    
    try:
        orchestrator = ResearchOrchestrator()
        sessions = await orchestrator.get_user_sessions(user_id, limit=1000)
        
        session = next(
            (s for s in sessions if s.get("session_id") == session_id),
            None
        )
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Research session not found",
            )
        
        if "_id" in session:
            session["_id"] = str(session["_id"])
        
        return APIResponse(
            data={"session": session},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get session: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session: {str(e)}",
        )


@router.delete(
    "/{session_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete research session",
    description="Delete a research session and its indexed chunks",
)
async def delete_session(
    session_id: str,
    http_request: Request,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Delete a research session and its chunks."""
    request_id = getattr(http_request.state, "request_id", "")
    user_id = current_user.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
        )
    
    try:
        orchestrator = ResearchOrchestrator()
        deleted = await orchestrator.delete_session(user_id, session_id)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or already deleted",
            )
        
        return APIResponse(
            data={"deleted": True, "session_id": session_id},
            metadata={"request_id": request_id, "timestamp": time.time()},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete session: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}",
        )

