"""MCP HTTP endpoint for remote MCP server access."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from api.dependencies.auth import get_current_user
from api.services.mcp_http_service import MCPHTTPService
from api.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.post("/request")
async def mcp_request(
    request: Request,
    mcp_request: dict[str, Any],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> JSONResponse:
    """Handle MCP protocol request over HTTP.

    This endpoint implements the MCP protocol over HTTP, allowing
    IDEs to connect to WISTX MCP server without local installation.

    Args:
        request: FastAPI request object
        mcp_request: MCP protocol request (JSON-RPC format)
        current_user: Authenticated user (from API key)

    Returns:
        MCP protocol response (JSON-RPC format)

    Example request:
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
    """
    if not mcp_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body is required",
        )

    if mcp_request.get("jsonrpc") != "2.0":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON-RPC version. Expected '2.0'",
        )

    try:
        service = MCPHTTPService()
        
        user_info_with_api_key = current_user.copy()
        api_key = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        if api_key:
            user_info_with_api_key["api_key"] = api_key
        
        response = await service.handle_request(
            mcp_request=mcp_request,
            user_info=user_info_with_api_key,
        )
        
        headers = _get_cors_headers(request)
        return JSONResponse(content=response, headers=headers)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("MCP request failed: %s", e, exc_info=True)
        request_id = mcp_request.get("id")
        headers = _get_cors_headers(request)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e),
                },
            },
            headers=headers,
        )


def _get_cors_headers(request: Request) -> dict[str, str]:
    """Get CORS headers for the request origin.
    
    Args:
        request: FastAPI request
        
    Returns:
        Dictionary of CORS headers
    """
    origin = request.headers.get("origin")
    if not origin:
        return {}
    
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
        "https://app.wistx.ai",
        "https://wistx.ai",
        "https://www.wistx.ai",
    ]
    
    if settings.debug:
        allowed_origins.extend([
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:8000",
        ])
    
    if origin in allowed_origins:
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Expose-Headers": "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Window, X-Correlation-ID",
        }
    
    return {}

