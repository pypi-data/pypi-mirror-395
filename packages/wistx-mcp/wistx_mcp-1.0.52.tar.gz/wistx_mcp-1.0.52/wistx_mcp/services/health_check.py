"""Health check service for MCP server."""

import asyncio
import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)


class MCPHealthCheck:
    """Health check service for MCP server components."""

    def __init__(self):
        """Initialize health check service."""
        self.mongodb_client = MongoDBClient()

    async def check_mongodb(self) -> dict[str, Any]:
        """Check MongoDB connection health.

        Returns:
            Dictionary with MongoDB health status
        """
        try:
            await asyncio.wait_for(
                self.mongodb_client.connect(),
                timeout=5.0,
            )
            is_healthy = await asyncio.wait_for(
                self.mongodb_client.health_check(),
                timeout=2.0,
            )
            if is_healthy:
                return {
                    "status": "healthy",
                    "database": settings.mongodb_database,
                }
            return {
                "status": "unhealthy",
                "database": settings.mongodb_database,
                "error": "Health check failed",
            }
        except asyncio.TimeoutError:
            return {
                "status": "unhealthy",
                "database": settings.mongodb_database,
                "error": "Connection timeout",
            }
        except (RuntimeError, ConnectionError, ValueError) as e:
            logger.warning("MongoDB health check failed: %s", e)
            return {
                "status": "unhealthy",
                "database": settings.mongodb_database,
                "error": str(e),
            }
        except Exception as e:
            logger.warning("Unexpected error in MongoDB health check: %s", e)
            return {
                "status": "unhealthy",
                "database": settings.mongodb_database,
                "error": "Unexpected error",
            }

    async def check_pinecone(self) -> dict[str, Any]:
        """Check Pinecone connection health.

        Returns:
            Dictionary with Pinecone health status
        """
        if not settings.pinecone_api_key:
            return {
                "status": "not_configured",
            }

        try:
            from pinecone import Pinecone  # type: ignore[import-untyped]
            from pinecone.exceptions import NotFoundException  # type: ignore[import-untyped]

            pc = Pinecone(api_key=settings.pinecone_api_key)
            index = await asyncio.wait_for(
                asyncio.to_thread(pc.Index, settings.pinecone_index_name),
                timeout=5.0,
            )
            stats = await asyncio.wait_for(
                asyncio.to_thread(index.describe_index_stats),
                timeout=5.0,
            )
            return {
                "status": "healthy",
                "index": settings.pinecone_index_name,
                "vector_count": stats.get("total_vector_count", 0),
            }
        except NotFoundException:
            return {
                "status": "index_not_found",
                "index": settings.pinecone_index_name,
                "error": f"Index '{settings.pinecone_index_name}' does not exist",
            }
        except (ImportError, ModuleNotFoundError):
            return {
                "status": "unavailable",
                "error": "Pinecone client not installed",
            }
        except asyncio.TimeoutError:
            return {
                "status": "unhealthy",
                "error": "Connection timeout",
            }
        except (RuntimeError, ConnectionError, ValueError, AttributeError) as e:
            logger.warning("Pinecone health check failed: %s", e)
            return {
                "status": "unhealthy",
                "error": str(e),
            }
        except Exception as e:
            logger.warning("Unexpected error in Pinecone health check: %s", e)
            return {
                "status": "unhealthy",
                "error": "Unexpected error",
            }

    async def check_api_client(self) -> dict[str, Any]:
        """Check WISTX API client health.

        Returns:
            Dictionary with API client health status
        """
        if not settings.api_key or not settings.api_url:
            return {
                "status": "not_configured",
            }

        try:
            from wistx_mcp.tools.lib.api_client import WISTXAPIClient

            client = WISTXAPIClient(api_key=settings.api_key, api_url=settings.api_url)
            response = await asyncio.wait_for(
                client.client.get(f"{settings.api_url}/health"),
                timeout=5.0,
            )
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "api_url": settings.api_url,
                }
            return {
                "status": "unhealthy",
                "api_url": settings.api_url,
                "error": f"API returned status {response.status_code}",
            }
        except asyncio.TimeoutError:
            return {
                "status": "unhealthy",
                "error": "API connection timeout",
            }
        except (RuntimeError, ConnectionError, ValueError) as e:
            logger.warning("API client health check failed: %s", e)
            return {
                "status": "unhealthy",
                "error": str(e),
            }
        except Exception as e:
            logger.warning("Unexpected error in API client health check: %s", e)
            return {
                "status": "unhealthy",
                "error": "Unexpected error",
            }

    async def check_all(self) -> dict[str, Any]:
        """Check all components health.

        Returns:
            Dictionary with overall health status
        """
        mongodb_health, pinecone_health, api_health = await asyncio.gather(
            self.check_mongodb(),
            self.check_pinecone(),
            self.check_api_client(),
            return_exceptions=True,
        )

        if isinstance(mongodb_health, Exception):
            mongodb_health = {"status": "error", "error": str(mongodb_health)}
        if isinstance(pinecone_health, Exception):
            pinecone_health = {"status": "error", "error": str(pinecone_health)}
        if isinstance(api_health, Exception):
            api_health = {"status": "error", "error": str(api_health)}

        overall_status = "healthy"
        if mongodb_health.get("status") != "healthy":
            overall_status = "degraded"
        if any(
            health.get("status") == "unhealthy"
            for health in [mongodb_health, pinecone_health, api_health]
        ):
            overall_status = "unhealthy"

        return {
            "status": overall_status,
            "mongodb": mongodb_health,
            "pinecone": pinecone_health,
            "api_client": api_health,
        }


mcp_health_check = MCPHealthCheck()

