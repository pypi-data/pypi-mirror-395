"""Code examples service - business logic for code examples search operations."""

import logging
import time
from typing import Any

from api.models.v1_requests import CodeExamplesSearchRequest
from api.models.v1_responses import CodeExampleResponse, CodeExamplesSearchResponse
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from api.config import settings
from api.services.code_examples_cost_refresh_service import code_examples_cost_refresh_service
from api.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class CodeExamplesService:
    """Service for code examples search operations."""

    def __init__(self):
        """Initialize code examples service."""
        self.mongodb_client = MongoDBClient()
        self.vector_search = VectorSearch(
            self.mongodb_client,
            gemini_api_key=settings.gemini_api_key,
            pinecone_api_key=settings.pinecone_api_key,
            pinecone_index_name=settings.pinecone_index_name,
        )

    async def search_code_examples(
        self,
        request: CodeExamplesSearchRequest,
        user_id: str,
        request_id: str | None = None,
    ) -> CodeExamplesSearchResponse:
        """Search infrastructure code examples.

        Args:
            request: Code examples search request
            user_id: User ID for quota tracking
            request_id: Optional request ID for tracing

        Returns:
            Code examples search response with results

        Raises:
            RuntimeError: If search operation fails
            ValueError: If request is invalid
        """
        start_time = time.time()

        try:
            async with MongoDBClient() as client:
                vector_search = VectorSearch(
                    client,
                    gemini_api_key=settings.gemini_api_key,
                    pinecone_api_key=settings.pinecone_api_key,
                    pinecone_index_name=settings.pinecone_index_name,
                )

                results = await vector_search.search_code_examples(
                    query=request.query,
                    code_types=request.code_types,
                    cloud_provider=request.cloud_provider,
                    services=request.services,
                    min_quality_score=request.min_quality_score,
                    compliance_standard=request.compliance_standard,
                    limit=request.limit,
                )

                formatted_examples = []
                for result in results:
                    cost_analysis = result.get("cost_analysis")
                    
                    if cost_analysis:
                        cloud_provider = result.get("cloud_provider")
                        is_stale = await code_examples_cost_refresh_service.is_cost_stale(
                            cost_analysis,
                            cloud_provider,
                        )
                        
                        if is_stale:
                            try:
                                refreshed_cost = await code_examples_cost_refresh_service.refresh_cost_for_example(result)
                                cost_analysis = refreshed_cost
                                
                                async with MongoDBClient() as update_client:
                                    await update_client.connect()
                                    if update_client.database:
                                        await update_client.database.code_examples.update_one(
                                            {"example_id": result.get("example_id")},
                                            {
                                                "$set": {
                                                    "cost_analysis": refreshed_cost,
                                                },
                                            },
                                        )
                                
                                logger.debug(
                                    "Refreshed stale cost for example %s",
                                    result.get("example_id"),
                                )
                            except Exception as e:
                                logger.warning(
                                    "Failed to refresh stale cost for example %s: %s",
                                    result.get("example_id"),
                                    e,
                                )
                    
                    formatted_example = CodeExampleResponse(
                        example_id=result.get("example_id", ""),
                        title=result.get("title", "Untitled"),
                        description=result.get("description", ""),
                        contextual_description=result.get("contextual_description"),
                        code_type=result.get("code_type", ""),
                        cloud_provider=result.get("cloud_provider", ""),
                        services=result.get("services", []),
                        resources=result.get("resources", []),
                        code=result.get("code", ""),
                        github_url=result.get("github_url", ""),
                        file_path=result.get("file_path", ""),
                        stars=result.get("stars", 0),
                        quality_score=result.get("quality_score", 0),
                        best_practices=result.get("best_practices", []),
                        hybrid_score=result.get("hybrid_score", 0.0),
                        vector_score=result.get("vector_score", 0.0),
                        bm25_score=result.get("bm25_score", 0.0),
                        compliance_analysis=result.get("compliance_analysis"),
                        cost_analysis=cost_analysis,
                    )
                    formatted_examples.append(formatted_example)

                query_time_ms = int((time.time() - start_time) * 1000)

                response = CodeExamplesSearchResponse(
                    examples=formatted_examples,
                    total=len(formatted_examples),
                    query=request.query,
                )

                logger.info(
                    "Code examples search completed: query=%s, results=%d, query_time_ms=%d [request_id=%s]",
                    request.query[:50],
                    len(formatted_examples),
                    query_time_ms,
                    request_id or "unknown",
                )

                return response

        except ValueError as e:
            logger.warning(
                "Invalid request for code examples search: %s [request_id=%s]",
                e,
                request_id or "unknown",
            )
            raise
        except Exception as e:
            logger.error(
                "Error searching code examples: %s [request_id=%s]",
                e,
                request_id or "unknown",
                exc_info=True,
            )
            raise ExternalServiceError(
                message=f"Failed to search code examples: {e}",
                user_message="Failed to search code examples. Please try again later.",
                error_code="CODE_EXAMPLES_SEARCH_ERROR",
                details={"request_id": request_id, "error": str(e)}
            ) from e


code_examples_service = CodeExamplesService()

