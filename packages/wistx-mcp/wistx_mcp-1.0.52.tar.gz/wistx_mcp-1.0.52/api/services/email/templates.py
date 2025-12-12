"""Email template rendering."""

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path(__file__).parent / "templates"


async def render_template(template_name: str, context: dict[str, Any]) -> str:
    """Render email template with context variables.

    Args:
        template_name: Template name (without .html extension)
        context: Template context variables

    Returns:
        Rendered HTML content

    Raises:
        FileNotFoundError: If template file not found
        ValueError: If template rendering fails
    """
    template_path = _TEMPLATE_DIR / f"{template_name}.html"

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_name}")

    try:
        content = template_path.read_text(encoding="utf-8")

        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))

        return content

    except Exception as e:
        from api.exceptions import ExternalServiceError
        raise ExternalServiceError(
            message=f"Failed to render template {template_name}: {str(e)}",
            user_message="Failed to render email template. Please contact support.",
            error_code="TEMPLATE_RENDER_ERROR",
            details={"template_name": template_name, "error": str(e)}
        ) from e

