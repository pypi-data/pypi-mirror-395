"""Transparent rate limiting headers for MCP responses."""

import logging
import time
from typing import Any

from wistx_mcp.tools.lib.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class RateLimitHeaders:
    """Generate and manage rate limit headers for responses."""

    def __init__(self, rate_limiter: RateLimiter | None = None):
        """Initialize rate limit headers manager.
        
        Args:
            rate_limiter: Optional RateLimiter instance
        """
        self.rate_limiter = rate_limiter or RateLimiter()

    def get_headers_for_user(self, user_id: str) -> dict[str, str]:
        """Get rate limit headers for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary of rate limit headers
        """
        try:
            # Get current rate limit status
            status = self.rate_limiter.get_status(user_id)
            
            headers = {
                "X-RateLimit-Limit": str(status.get("limit", 1000)),
                "X-RateLimit-Remaining": str(status.get("remaining", 1000)),
                "X-RateLimit-Reset": str(int(status.get("reset_time", time.time()))),
            }
            
            # Add Retry-After if rate limited
            if status.get("is_limited", False):
                retry_after = status.get("retry_after", 60)
                headers["Retry-After"] = str(int(retry_after))
                headers["X-RateLimit-Status"] = "limited"
            else:
                headers["X-RateLimit-Status"] = "ok"
            
            return headers
        except Exception as e:
            logger.error(f"Error getting rate limit headers: {e}", exc_info=True)
            return {
                "X-RateLimit-Status": "error",
                "X-RateLimit-Limit": "1000",
                "X-RateLimit-Remaining": "1000",
            }

    def get_headers_for_tool(self, tool_name: str, user_id: str) -> dict[str, str]:
        """Get rate limit headers for a specific tool.
        
        Args:
            tool_name: Name of the tool
            user_id: User identifier
            
        Returns:
            Dictionary of rate limit headers
        """
        try:
            # Get tool-specific rate limit status
            key = f"{user_id}:tool:{tool_name}"
            status = self.rate_limiter.get_status(key)
            
            headers = {
                "X-RateLimit-Tool": tool_name,
                "X-RateLimit-Limit": str(status.get("limit", 100)),
                "X-RateLimit-Remaining": str(status.get("remaining", 100)),
                "X-RateLimit-Reset": str(int(status.get("reset_time", time.time()))),
            }
            
            if status.get("is_limited", False):
                retry_after = status.get("retry_after", 60)
                headers["Retry-After"] = str(int(retry_after))
                headers["X-RateLimit-Status"] = "limited"
            else:
                headers["X-RateLimit-Status"] = "ok"
            
            return headers
        except Exception as e:
            logger.error(f"Error getting tool rate limit headers: {e}", exc_info=True)
            return {
                "X-RateLimit-Tool": tool_name,
                "X-RateLimit-Status": "error",
            }

    def format_headers_for_response(self, headers: dict[str, str]) -> str:
        """Format headers for display in response.
        
        Args:
            headers: Dictionary of headers
            
        Returns:
            Formatted string representation
        """
        lines = []
        for key, value in headers.items():
            lines.append(f"{key}: {value}")
        return "\n".join(lines)

    def get_rate_limit_info(self, user_id: str) -> dict[str, Any]:
        """Get detailed rate limit information for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with rate limit details
        """
        try:
            status = self.rate_limiter.get_status(user_id)
            
            return {
                "user_id": user_id,
                "limit": status.get("limit", 1000),
                "remaining": status.get("remaining", 1000),
                "reset_time": status.get("reset_time", time.time()),
                "is_limited": status.get("is_limited", False),
                "retry_after": status.get("retry_after", 0),
                "usage_percentage": (
                    (status.get("limit", 1000) - status.get("remaining", 1000)) 
                    / status.get("limit", 1000) * 100
                ),
            }
        except Exception as e:
            logger.error(f"Error getting rate limit info: {e}", exc_info=True)
            return {
                "user_id": user_id,
                "error": str(e),
            }

    def should_rate_limit(self, user_id: str) -> bool:
        """Check if user should be rate limited.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if user is rate limited
        """
        try:
            status = self.rate_limiter.get_status(user_id)
            return status.get("is_limited", False)
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}", exc_info=True)
            return False

    def get_retry_after(self, user_id: str) -> int:
        """Get retry-after value in seconds.
        
        Args:
            user_id: User identifier
            
        Returns:
            Seconds to wait before retrying
        """
        try:
            status = self.rate_limiter.get_status(user_id)
            return int(status.get("retry_after", 60))
        except Exception as e:
            logger.error(f"Error getting retry-after: {e}", exc_info=True)
            return 60

