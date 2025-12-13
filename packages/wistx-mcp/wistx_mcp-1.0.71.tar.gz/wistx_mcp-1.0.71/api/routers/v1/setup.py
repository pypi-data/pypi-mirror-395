"""Setup script endpoint for automated IDE configuration."""

import logging
from typing import Optional

from fastapi import APIRouter, Query
from fastapi.responses import Response

from api.services.setup_script_service import SetupScriptService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/setup", tags=["setup"])


@router.get("/script")
async def get_setup_script(
    api_key: Optional[str] = Query(None, description="API key (optional, can be provided via script parameter)"),
    ide: Optional[str] = Query(None, description="IDE name (optional, script will auto-detect)"),
    remote: bool = Query(False, description="Use remote server (default: False)"),
) -> Response:
    """Return automated setup script.

    This endpoint generates a bash script that automatically configures
    WISTX MCP server for the user's IDE(s).

    Usage:
        curl -fsSL https://api.wistx.ai/v1/setup/script | bash -s -- YOUR_API_KEY cursor --remote

    Args:
        api_key: Optional API key (can also be passed as script argument)
        ide: Optional IDE name (can also be passed as script argument)
        remote: Use remote server instead of local

    Returns:
        Bash script content

    Example:
        ```bash
        # Remote server (recommended)
        curl -fsSL https://api.wistx.ai/v1/setup/script?remote=true | bash -s -- YOUR_API_KEY cursor

        # Local server
        curl -fsSL https://api.wistx.ai/v1/setup/script | bash -s -- YOUR_API_KEY cursor
        ```
    """
    service = SetupScriptService()
    script_content = service.generate_script(
        api_key=api_key,
        ide=ide,
        remote=remote,
    )

    return Response(
        content=script_content,
        media_type="text/x-shellscript",
        headers={
            "Content-Disposition": "attachment; filename=wistx-setup.sh",
        },
    )

