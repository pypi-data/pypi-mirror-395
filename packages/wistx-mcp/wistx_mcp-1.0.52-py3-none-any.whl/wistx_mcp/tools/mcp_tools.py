"""MCP tools for compliance and knowledge research."""

import base64
import logging
import re
import sys
from datetime import datetime
from typing import Any

import httpx

from wistx_mcp.tools.lib.api_client import WISTXAPIClient, get_api_client
from wistx_mcp.tools.lib.web_search_client import WebSearchClient
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_types
from wistx_mcp.tools.lib.resource_type_validator import validate_provider_compatibility
from wistx_mcp.tools import visualize_infra_flow
from wistx_mcp.tools import generate_documentation
from wistx_mcp.config import settings
from wistx_mcp.tools import pricing

logger = logging.getLogger(__name__)

# Patch sys.exit to prevent api.config from exiting the MCP server
_original_sys_exit = sys.exit

def _mcp_safe_exit(code: int = 0) -> None:
    """MCP-safe sys.exit that raises SystemExit instead of exiting."""
    raise SystemExit(code)

api_client = WISTXAPIClient()


async def get_compliance_requirements(
    resource_types: list[str],
    standards: list[str] | None = None,
    severity: str | None = None,
    include_remediation: bool = True,
    include_verification: bool = True,
    api_key: str = "",
    generate_report: bool = True,
    cloud_provider: str | list[str] | None = None,
) -> dict[str, Any]:
    """Get compliance requirements for infrastructure resources.

    Args:
        resource_types: List of resource types (RDS, S3, EC2, etc.)
        standards: List of compliance standards (PCI-DSS, HIPAA, etc.)
        severity: Filter by severity level
        include_remediation: Include remediation guidance
        include_verification: Include verification procedures
        api_key: WISTX API key (required for authentication)
        generate_report: Whether to automatically generate and store a compliance report
        cloud_provider: Cloud provider (aws, gcp, azure) or list of providers for multi-cloud projects - used to validate resource types match provider

    Returns:
        Dictionary with compliance controls and summary.
        If generate_report=True and api_key provided, also includes:
        - report_id: Generated report ID
        - report_download_url: URL to download report
        - report_view_url: URL to view report

    Raises:
        ValueError: If input validation fails
        RuntimeError: If API call fails
        ConnectionError: If network connection fails
        TimeoutError: If request times out
    """
    if not resource_types:
        raise ValueError("At least one resource type is required")

    if not isinstance(resource_types, list):
        raise ValueError("resource_types must be a list")

    if len(resource_types) > 50:
        raise ValueError("Maximum 50 resource types allowed")

    def _detect_providers_from_resource_types(resource_types: list[str]) -> list[str]:
        """Detect cloud providers from resource types.
        
        Args:
            resource_types: List of resource types
            
        Returns:
            List of detected provider names (aws, gcp, azure)
        """
        detected_providers = set()
        
        try:
            from api.utils.resource_types import (
                VALID_AWS_RESOURCE_TYPES,
                VALID_GCP_RESOURCE_TYPES,
                VALID_AZURE_RESOURCE_TYPES,
            )
        except ImportError:
            return []
        
        aws_upper = {rt.upper() for rt in VALID_AWS_RESOURCE_TYPES}
        gcp_upper = {rt.upper() for rt in VALID_GCP_RESOURCE_TYPES}
        azure_upper = {rt.upper() for rt in VALID_AZURE_RESOURCE_TYPES}
        
        for rt in resource_types:
            if not rt or not rt.strip():
                continue
            
            rt_upper = rt.strip().upper()
            
            if rt_upper in aws_upper:
                detected_providers.add("aws")
            elif rt_upper in gcp_upper:
                detected_providers.add("gcp")
            elif rt_upper in azure_upper:
                detected_providers.add("azure")
        
        return sorted(list(detected_providers))
    
    cloud_provider_normalized = None
    detected_providers = []
    
    if cloud_provider:
        valid_providers = ["aws", "gcp", "azure"]
        
        if isinstance(cloud_provider, list):
            if len(cloud_provider) == 1:
                cloud_provider_normalized = cloud_provider[0].strip().lower() if isinstance(cloud_provider[0], str) else None
            elif len(cloud_provider) > 1:
                detected_providers = [p.strip().lower() for p in cloud_provider if isinstance(p, str)]
                logger.info("Multi-cloud project detected with providers: %s. Using first provider for normalization.", detected_providers)
                cloud_provider_normalized = detected_providers[0] if detected_providers else None
            else:
                cloud_provider_normalized = None
        elif isinstance(cloud_provider, str):
            cloud_provider_normalized = cloud_provider.strip().lower()
            
            if cloud_provider_normalized == "multi-cloud":
                detected_providers = _detect_providers_from_resource_types(resource_types)
                if detected_providers:
                    logger.info(
                        "Multi-cloud project detected. Providers inferred from resource types: %s. "
                        "Skipping provider-specific validation to allow resources from all providers.",
                        detected_providers,
                    )
                else:
                    logger.info(
                        "Multi-cloud project detected but could not infer providers from resource types. "
                        "Skipping provider-specific validation."
                    )
                cloud_provider_normalized = None
        else:
            logger.warning("Invalid cloud_provider type: %s. Expected str or list[str]", type(cloud_provider))
            cloud_provider_normalized = None
        
        if cloud_provider_normalized and cloud_provider_normalized not in valid_providers:
            logger.warning("Invalid cloud_provider: %s. Valid providers: %s", cloud_provider_normalized, valid_providers)
            cloud_provider_normalized = None
    
    normalized_resource_types = normalize_resource_types(resource_types, cloud_provider_normalized)
    
    if cloud_provider_normalized is None and cloud_provider and isinstance(cloud_provider, str) and cloud_provider.lower() == "multi-cloud":
        detected_providers = _detect_providers_from_resource_types(normalized_resource_types)
        if detected_providers:
            logger.debug(
                "Re-normalizing resource types for multi-cloud with detected providers: %s",
                detected_providers,
            )
            normalized_resource_types = normalize_resource_types(normalized_resource_types, detected_providers)
    
    if normalized_resource_types != resource_types:
        logger.debug(
            "Normalized resource types: %s -> %s",
            resource_types,
            normalized_resource_types,
        )
    
    if cloud_provider_normalized:
        valid_types, invalid_types, suggestions = validate_provider_compatibility(
            normalized_resource_types,
            cloud_provider_normalized,
        )
        
        if invalid_types:
            suggestion_msgs = []
            for invalid_type in invalid_types:
                if invalid_type in suggestions:
                    suggestion_msgs.append(f"'{invalid_type}' -> use '{suggestions[invalid_type]}'")
                else:
                    suggestion_msgs.append(f"'{invalid_type}' is not valid for {cloud_provider_normalized.upper()}")
            
            logger.warning(
                "Provider-incompatible resource types detected: %s. Suggestions: %s",
                invalid_types,
                suggestions,
            )
            
            if not valid_types:
                from wistx_mcp.tools.lib.resource_type_validator import get_provider_resource_types
                
                valid_resource_types = sorted(list(get_provider_resource_types(cloud_provider_normalized)))
                common_types = valid_resource_types[:20]  # Show first 20 common types
                
                error_msg = (
                    f"All resource types are incompatible with {cloud_provider_normalized.upper()}. "
                    f"Invalid types: {', '.join(invalid_types)}. "
                )
                if suggestions:
                    error_msg += f"Suggestions: {'; '.join(suggestion_msgs)}. "
                error_msg += (
                    f"Valid {cloud_provider_normalized.upper()} resource types include: "
                    f"{', '.join(common_types)}"
                )
                if len(valid_resource_types) > 20:
                    error_msg += f" (and {len(valid_resource_types) - 20} more)"
                raise ValueError(error_msg)
            
            normalized_resource_types = valid_types
    
    sanitized_resource_types = []
    for rt in normalized_resource_types:
        if not isinstance(rt, str):
            raise ValueError(f"Resource type must be string, got {type(rt)}")
        rt_clean = rt.strip()[:100]
        if not rt_clean or len(rt_clean) < 2:
            raise ValueError(f"Invalid resource type: {rt}")
        sanitized_resource_types.append(rt_clean)
    
    resource_types = sanitized_resource_types

    if standards is not None:
        if not isinstance(standards, list):
            raise ValueError("standards must be a list")
        if len(standards) > 20:
            raise ValueError("Maximum 20 standards allowed")

        sanitized_standards = []
        for std in standards:
            if not isinstance(std, str):
                raise ValueError(f"Standard must be string, got {type(std)}")
            std_clean = std.strip().upper()[:50]
            if not std_clean or len(std_clean) < 2:
                raise ValueError(f"Invalid standard: {std}")
            sanitized_standards.append(std_clean)

        standards = sanitized_standards

    if severity is not None:
        valid_severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        if severity not in valid_severities:
            raise ValueError(f"severity must be one of {valid_severities}")
        severity = severity.upper()

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        user_id = await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    try:
        result = await api_client.get_compliance_requirements(
            resource_types=resource_types,
            standards=standards or [],
            severity=severity,
            include_remediation=include_remediation,
            include_verification=include_verification,
        )
        
        logger.info("API client returned result type: %s", type(result))
        
        if result is None:
            logger.error("API client returned None for compliance requirements")
            raise RuntimeError("API returned null response")
        
        if not isinstance(result, dict):
            logger.error("API client returned non-dict result: %s", type(result))
            raise RuntimeError(f"Invalid response type from API: {type(result)}")
        
        logger.info("Result keys: %s", list(result.keys()) if isinstance(result, dict) else "N/A")
        logger.info("Result has 'controls': %s, Result has 'data': %s", "controls" in result, "data" in result)
        
        if not isinstance(result, dict):
            logger.error("Invalid response type from API: %s", type(result))
            raise RuntimeError("Invalid response format from API")

        if "data" not in result and "controls" not in result:
            logger.error("Response missing required fields: %s", list(result.keys()))
            raise RuntimeError("Invalid response structure: missing 'data' or 'controls'")

        if "controls" in result:
            if not isinstance(result["controls"], list):
                logger.error("Controls field is not a list: %s", type(result["controls"]))
                raise RuntimeError("Invalid controls structure: expected list")

            for i, control in enumerate(result["controls"]):
                if not isinstance(control, dict):
                    logger.error("Control %d is not a dict: %s", i, type(control))
                    raise RuntimeError(f"Invalid control structure at index {i}")

                required_fields = ["control_id", "standard"]
                missing = [f for f in required_fields if f not in control]
                if missing:
                    logger.warning("Control %d missing fields: %s", i, missing)

        if "data" in result and isinstance(result["data"], dict):
            if "controls" in result["data"]:
                if not isinstance(result["data"]["controls"], list):
                    logger.error("Data.controls field is not a list: %s", type(result["data"]["controls"]))
                    raise RuntimeError("Invalid data.controls structure: expected list")
    except ValueError as e:
        error_msg = str(e)
        if "Invalid resource types" in error_msg or "Invalid request parameters" in error_msg:
            logger.warning(
                "Failed to fetch compliance requirements due to invalid resource types: %s. "
                "Original resource types: %s, Normalized: %s. "
                "Attempting to filter out invalid types and retry.",
                error_msg,
                resource_types,
                normalized_resource_types,
            )
            invalid_types_match = re.search(r"Invalid resource types: \[(.*?)\]", error_msg)
            if invalid_types_match:
                invalid_types_str = invalid_types_match.group(1)
                invalid_types = [t.strip().strip("'\"") for t in invalid_types_str.split(",")]
                
                filtered_normalized = [
                    rt for rt in normalized_resource_types 
                    if rt not in invalid_types
                ]
                
                if filtered_normalized:
                    logger.info(
                        "Retrying with filtered normalized resource types: %s (removed: %s). "
                        "Original types: %s, Normalized types: %s",
                        filtered_normalized,
                        invalid_types,
                        resource_types,
                        normalized_resource_types,
                    )
                    normalized_filtered = filtered_normalized
                    result = await api_client.get_compliance_requirements(
                        resource_types=normalized_filtered,
                        standards=standards or [],
                        severity=severity,
                        include_remediation=include_remediation,
                        include_verification=include_verification,
                    )

                    if result is None:
                        logger.error("API client returned None after retry")
                        raise RuntimeError("API returned null response after retry")

                    if not isinstance(result, dict):
                        logger.error("API client returned non-dict result after retry: %s", type(result))
                        raise RuntimeError(f"Invalid response type from API after retry: {type(result)}")

                    if "data" not in result and "controls" not in result:
                        logger.error("Response missing required fields after retry: %s", list(result.keys()))
                        raise RuntimeError("Invalid response structure after retry: missing 'data' or 'controls'")
                else:
                    logger.error(
                        "All resource types were invalid. Cannot fetch compliance requirements."
                    )
                    raise ValueError(
                        f"All resource types are invalid: {invalid_types}. "
                        "Please check resource type names."
                    ) from e
            else:
                raise ValueError(
                    f"Invalid resource types in request: {error_msg}"
                ) from e
        else:
            raise
    except ValueError as e:
        logger.error("Validation error in get_compliance_requirements: %s", e, exc_info=True)
        raise
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code if e.response else None
        logger.error("HTTP status error: %s (status: %s)", e, status_code)
        if status_code == 401:
            raise ValueError("Invalid API key") from e
        elif status_code == 429:
            raise RuntimeError("Rate limit exceeded") from e
        elif status_code >= 500:
            raise RuntimeError(f"Server error: {status_code}") from e
        raise RuntimeError(f"HTTP error: {status_code}") from e
    except httpx.TimeoutException as e:
        logger.error("Request timeout: %s", e)
        raise TimeoutError("Request timeout") from e
    except httpx.NetworkError as e:
        logger.error("Network error: %s", e)
        raise ConnectionError("Network connection failed") from e
    except httpx.HTTPError as e:
        logger.error("HTTP error in get_compliance_requirements: %s", e, exc_info=True)
        raise RuntimeError(f"HTTP error: {e}") from e
    except (RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Error in get_compliance_requirements: %s", e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error in get_compliance_requirements: %s", e, exc_info=True)
        raise

    # Report generation and return logic - OUTSIDE except blocks
    if generate_report and api_key:
        try:
            if user_id:
                controls = result.get("controls") or result.get("data", {}).get("controls", [])
                if controls:
                    subject = f"Compliance Report: {', '.join(resource_types)}"
                    if standards:
                        subject += f" ({', '.join(standards)})"

                    logger.info("Generating compliance report for user %s", user_id)

                    report_result = await generate_documentation.generate_documentation(
                        document_type="compliance_report",
                        subject=subject,
                        resource_types=resource_types,
                        compliance_standards=standards or [],
                        format="markdown",
                        include_compliance=True,
                        include_security=True,
                        include_cost=False,
                        include_best_practices=True,
                    )

                    report_id = f"report-{datetime.now().strftime('%Y%m%d%H%M%S')}-{user_id[:8]}"

                    content = report_result.get("content", "")
                    output_format = report_result.get("format", "markdown")

                    content_type_map = {
                        "markdown": "text/markdown",
                        "html": "text/html",
                        "pdf": "application/pdf",
                        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        "json": "application/json",
                    }

                    content_type = content_type_map.get(output_format, "text/plain")

                    if isinstance(content, bytes):
                        content_b64 = base64.b64encode(content).decode("utf-8")
                    else:
                        content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")

                    try:
                        from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
                        from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS

                        async with MongoDBClient() as mongodb_client:
                            if mongodb_client.database is None:
                                raise RuntimeError("MongoDB database not available")
                            reports_collection = mongodb_client.database.reports

                            async def _insert_report() -> None:
                                await reports_collection.insert_one({
                                    "report_id": report_id,
                                    "user_id": user_id,
                                    "document_type": "compliance_report",
                                    "subject": subject,
                                    "format": output_format,
                                    "content": content_b64,
                                    "content_type": content_type,
                                    "sections": report_result.get("sections", []),
                                    "metadata": report_result.get("metadata", {}),
                                    "created_at": datetime.utcnow(),
                                })

                            await execute_mongodb_operation(
                                _insert_report,
                                timeout=API_TIMEOUT_SECONDS,
                                max_retries=3,
                            )

                            api_url_value = getattr(settings, "api_url", "")
                            base_url = api_url_value.rstrip("/") if api_url_value else ""
                            download_url = f"{base_url}/v1/reports/{report_id}/download?format={output_format}" if base_url else ""
                            view_url = f"{base_url}/v1/reports/{report_id}/view?format={output_format}" if base_url else ""

                            result["report_id"] = report_id
                            result["report_download_url"] = download_url
                            result["report_view_url"] = view_url

                            logger.info("Compliance report generated and stored: %s", report_id)
                    except Exception as e:
                        logger.warning("Error storing compliance report: %s", e)
                else:
                    logger.warning("No controls found, skipping report generation")
            else:
                logger.warning("User ID not found from API key, skipping report generation")
        except Exception as e:
            logger.warning("Failed to generate compliance report: %s", e, exc_info=True)

    if result is None:
        logger.error("CRITICAL: result is None before return statement. This should never happen.")
        logger.error("Stack trace:", exc_info=True)
        raise RuntimeError("Internal error: result is None before return")

    if not isinstance(result, dict):
        logger.error("CRITICAL: result is not a dict before return: %s", type(result))
        logger.error("Stack trace:", exc_info=True)
        raise RuntimeError(f"Internal error: result is not a dict: {type(result)}")

    logger.info("Returning result with keys: %s", list(result.keys()) if isinstance(result, dict) else "N/A")
    logger.debug("Result type: %s, Result keys: %s", type(result), list(result.keys()) if isinstance(result, dict) else "N/A")

    final_result = result
    if final_result is None:
        logger.error("CRITICAL: final_result is None at return statement")
        raise RuntimeError("Internal error: result is None at return")
    if not isinstance(final_result, dict):
        logger.error("CRITICAL: final_result is not a dict at return: %s", type(final_result))
        raise RuntimeError(f"Internal error: result is not a dict at return: {type(final_result)}")

    return final_result


async def research_knowledge_base(
    query: str,
    domains: list[str] | None = None,
    content_types: list[str] | None = None,
    include_cross_domain: bool = True,
    include_web_search: bool = True,
    format: str = "structured",
    max_results: int = 1000,
    api_key: str = "",
    research_url: str | None = None,
    enable_deep_research: bool = False,
) -> dict[str, Any]:
    """Research knowledge base across all domains with optional web search.

    Deep research tool that searches internal knowledge base and optionally
    includes real-time web search results for comprehensive coverage.

    When enable_deep_research=True, performs on-demand research using
    Anthropic's contextual retrieval approach:
    - Analyzes intent to discover relevant documentation sources
    - Fetches and chunks content with LLM-generated context
    - Indexes with hybrid search (semantic + BM25)
    - Stores in user-scoped knowledge base for future queries

    Args:
        query: Research query in natural language
        domains: Filter by domains (compliance, finops, devops, infrastructure, security, etc.)
        content_types: Filter by content types (guide, pattern, strategy, etc.)
        include_cross_domain: Include cross-domain relationships
        include_web_search: Include web search results (Tavily) for real-time information
        format: Response format (structured, markdown, executive_summary)
        max_results: Maximum number of results
        api_key: WISTX API key (required for authentication)
        research_url: Optional URL to research directly (fetches, chunks, indexes)
        enable_deep_research: Enable on-demand research with contextual retrieval

    Returns:
        Dictionary with research results and summary:
        - results: Knowledge articles from internal database
        - web_results: Web search results (if include_web_search=True)
        - research_summary: Summary of findings
        - research_session: Session info (if enable_deep_research=True)

    Raises:
        ValueError: If query validation fails
        RuntimeError: If API call fails
        ConnectionError: If network connection fails
        TimeoutError: If request times out
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    query = query.strip()
    if len(query) < 10:
        raise ValueError("Query must be at least 10 characters")
    
    if len(query) > 10000:
        raise ValueError("Query must be less than 10000 characters")
    
    if max_results < 1 or max_results > 50000:
        raise ValueError("max_results must be between 1 and 50000")
    
    if format not in ["structured", "markdown", "executive_summary"]:
        raise ValueError(f"Invalid format: {format}. Must be one of: structured, markdown, executive_summary")

    from wistx_mcp.tools.lib.input_sanitizer import validate_query_input

    validate_query_input(query)

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        user_id = await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    # Handle deep research mode (on-demand contextual retrieval)
    research_session_info = None
    if enable_deep_research or research_url:
        try:
            from api.services.research_orchestrator import ResearchOrchestrator

            orchestrator = ResearchOrchestrator()
            research_result = await orchestrator.research(
                query=query,
                user_id=user_id,
                url=research_url,
                max_sources=5,
                generate_context=True,
            )

            research_session_info = {
                "session_id": research_result.session.session_id,
                "status": research_result.session.status,
                "sources_processed": research_result.sources_processed,
                "chunks_indexed": research_result.chunks_indexed,
                "sources": research_result.session.sources,
                "errors": research_result.errors if research_result.errors else None,
            }

            if research_result.intent_analysis:
                research_session_info["intent_analysis"] = {
                    "technologies": research_result.intent_analysis.technologies,
                    "task_type": research_result.intent_analysis.task_type,
                }

            logger.info(
                "Deep research completed: %d chunks from %d sources",
                research_result.chunks_indexed,
                research_result.sources_processed,
            )
        except Exception as e:
            logger.error("Deep research failed (continuing with standard search): %s", e)
            research_session_info = {
                "status": "failed",
                "error": str(e),
            }

    web_search_client = None
    web_results = None
    result = None

    try:
        result = await api_client.research_knowledge_base(
            query=query,
            domains=domains or [],
            content_types=content_types or [],
            include_cross_domain=include_cross_domain,
            include_global=True,
            response_format=format,
            max_results=max_results,
        )
    except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Error in knowledge base research API call: %s", e, exc_info=True)
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            logger.error("Knowledge base research timed out: %s", e, exc_info=True)
            raise RuntimeError(
                f"Knowledge base research timed out after 90 seconds. "
                f"This may occur with large result sets or slow network conditions. "
                f"Try reducing max_results or retry the query."
            ) from e
        raise
    finally:
        if web_search_client:
            try:
                await web_search_client.close()
            except Exception as e:
                logger.debug("Error closing web search client: %s", e)

    if result and include_web_search and settings.tavily_api_key:
        try:
            from wistx_mcp.tools.lib.retry_utils import with_timeout
            from wistx_mcp.tools.lib.constants import WEB_SEARCH_TIMEOUT_SECONDS
            
            web_search_client = WebSearchClient(api_key=settings.tavily_api_key)
            
            async def fetch_web_search() -> dict[str, Any]:
                if domains:
                    return await web_search_client.search_by_domain(
                        query=query,
                        domains=domains,
                        max_results=min(max_results, 50),
                        max_age_days=None,
                    )
                else:
                    return await web_search_client.search_devops(
                        query=query,
                        max_results=min(max_results, 50),
                        max_age_days=90,
                    )
            
            web_search_timeout = min(WEB_SEARCH_TIMEOUT_SECONDS, 20.0)
            web_search_data = await with_timeout(
                fetch_web_search,
                timeout_seconds=web_search_timeout,
            )

            web_results = {
                "answer": web_search_data.get("answer"),
                "results": web_search_data.get("results", []),
                "domains_searched": domains if domains else ["devops", "infrastructure"],
                "freshness_info": web_search_data.get("freshness_info", {}),
            }

            logger.info(
                "Added web search results to knowledge research: %d web results for domains %s",
                len(web_search_data.get("results", [])),
                domains if domains else ["devops", "infrastructure"],
            )

            try:
                sys.exit = _mcp_safe_exit
                from api.services.web_search_storage_service import web_search_storage_service
                sys.exit = _original_sys_exit

                storage_stats = await web_search_storage_service.store_web_search_results(
                    web_results=web_results,
                    query=query,
                    domains_searched=domains if domains else ["devops", "infrastructure"],
                    store_in_background=True,
                )
                logger.info(
                    "Web search results storage initiated: %d results, %d will be stored",
                    storage_stats["total_results"],
                    storage_stats.get("stored", 0) + storage_stats.get("converted", 0),
                )
            except Exception as e:
                sys.exit = _original_sys_exit
                logger.warning("Failed to store web search results: %s", e, exc_info=True)
        except (ValueError, RuntimeError, ConnectionError, TimeoutError) as e:
            logger.warning("Failed to include web search in research (non-critical): %s", e)
            if result:
                logger.info("Returning knowledge base results without web search due to timeout/failure")
        except Exception as e:
            logger.warning("Unexpected error in web search (non-critical): %s", e, exc_info=True)
            if result:
                logger.info("Returning knowledge base results without web search due to error")

    if web_results:
        result["web_results"] = web_results
    elif result and include_web_search:
        result["web_results"] = {
            "answer": None,
            "results": [],
            "domains_searched": domains if domains else ["devops", "infrastructure"],
            "freshness_info": {},
            "note": "Web search timed out or failed, but knowledge base results are available",
        }

    if not result:
        raise RuntimeError("Knowledge base research failed: No results returned from API")

    # Add research session info if deep research was performed
    if research_session_info:
        result["research_session"] = research_session_info

    return result


async def calculate_infrastructure_cost(
    resources: list[dict[str, Any]],
    api_key: str = "",
) -> dict[str, Any]:
    """Calculate infrastructure costs.

    Args:
        resources: List of resource specifications
            Example: [{"cloud": "aws", "service": "rds", "instance_type": "db.t3.medium", "quantity": 1}]
        api_key: WISTX API key (required for authentication, can be provided via context)

    Returns:
        Dictionary with cost breakdown and optimizations

    Raises:
        ValueError: If api_key is missing or invalid
    """
    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        user_id = await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    try:
        environment_name = None
        for resource in resources:
            env_name = resource.get("environment") or resource.get("environment_name")
            if env_name:
                environment_name = env_name
                break

        result = await pricing.calculate_infrastructure_cost(
            resources,
            user_id=str(user_id),
            check_budgets=True,
            environment_name=environment_name,
        )
        return result
    except ValueError as e:
        if "Budget exceeded" in str(e):
            raise
        logger.error("Error in calculate_infrastructure_cost: %s", e, exc_info=True)
        raise
    except (RuntimeError, ConnectionError, TimeoutError) as e:
        logger.error("Error in calculate_infrastructure_cost: %s", e, exc_info=True)
        raise
    except Exception as e:
        logger.error("Unexpected error in calculate_infrastructure_cost: %s", e, exc_info=True)
        raise

