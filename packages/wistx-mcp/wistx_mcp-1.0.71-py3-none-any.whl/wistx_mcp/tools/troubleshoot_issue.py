"""Troubleshoot issue tool - diagnose and fix infrastructure/code issues."""

import logging
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.vector_search import VectorSearch
from wistx_mcp.tools.lib.web_search_client import WebSearchClient
from wistx_mcp.tools.lib.issue_analyzer import IssueAnalyzer
from wistx_mcp.tools.lib.incident_tracker import IncidentTracker
from wistx_mcp.tools.lib.solution_builder import SolutionKnowledgeBuilder
from wistx_mcp.tools.lib.pattern_recognizer import PatternRecognizer
from wistx_mcp.tools.lib.api_client import WISTXAPIClient
from wistx_mcp.tools.lib.plan_enforcement import require_query_quota
from wistx_mcp.tools.lib.github_tree_fetcher import GitHubTreeFetcher
from wistx_mcp.tools import visualize_infra_flow
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)

api_client = WISTXAPIClient()


@require_query_quota
async def troubleshoot_issue(
    issue_description: str,
    infrastructure_type: str | None = None,
    cloud_provider: str | None = None,
    error_messages: list[str] | None = None,
    configuration_code: str | None = None,
    logs: str | None = None,
    resource_type: str | None = None,
    api_key: str = "",
) -> dict[str, Any]:
    """Troubleshoot infrastructure and code issues.

    Args:
        issue_description: Description of the issue
        infrastructure_type: Type of infrastructure (terraform, kubernetes, docker, etc.)
        cloud_provider: Cloud provider (aws, gcp, azure)
        error_messages: List of error messages
        configuration_code: Relevant configuration code
        logs: Log output
        resource_type: Resource type (RDS, S3, EKS, etc.)
        api_key: WISTX API key (for searching user's codebase)

    Returns:
        Dictionary with troubleshooting results:
        - diagnosis: Root cause analysis
        - issues: List of identified issues
        - fixes: Recommended fixes with code examples
        - prevention: How to prevent similar issues
        - related_knowledge: Related knowledge base articles
        - similar_issues: Similar issues from user's codebase (if api_key provided)

    Raises:
        ValueError: If invalid parameters
        Exception: If troubleshooting fails
    """
    if not issue_description:
        raise ValueError("issue_description is required")

    from wistx_mcp.tools.lib.input_sanitizer import validate_input_size
    from wistx_mcp.tools.lib.constants import MAX_ISSUE_DESCRIPTION_LENGTH

    validate_input_size(issue_description, "issue_description", MAX_ISSUE_DESCRIPTION_LENGTH)

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id

    try:
        await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    logger.info(
        "Troubleshooting issue: description='%s', type=%s, provider=%s",
        issue_description[:100],
        infrastructure_type,
        cloud_provider,
    )

    web_search_client = None

    try:
        async with MongoDBClient() as mongodb_client:
            vector_search = VectorSearch(
                mongodb_client,
                gemini_api_key=settings.gemini_api_key,
            )

            analyzer = IssueAnalyzer(mongodb_client)
            incident_tracker = IncidentTracker(mongodb_client)
            solution_builder = SolutionKnowledgeBuilder(
                mongodb_client,
                vector_search=vector_search,
            )
            pattern_recognizer = PatternRecognizer(mongodb_client)

            diagnosis = {
                "root_cause": "",
                "confidence": "medium",
                "issues": [],
            }

            if error_messages:
                error_text = " ".join(error_messages)
                error_analysis = await analyzer.analyze_error(
                    error_message=error_text,
                    infrastructure_type=infrastructure_type,
                    cloud_provider=cloud_provider,
                )
                diagnosis["issues"].extend(error_analysis.get("likely_causes", []))
                diagnosis["error_patterns"] = error_analysis.get("error_patterns", [])

            if logs:
                log_analysis = analyzer.analyze_logs(logs)
                diagnosis["log_analysis"] = log_analysis
                if log_analysis.get("error_count", 0) > 0:
                    diagnosis["issues"].extend(log_analysis.get("error_lines", [])[:3])

        if configuration_code:
            config_analysis = await analyzer.analyze_configuration(
                configuration_code,
                infrastructure_type,
                api_key=api_key,
            )
            diagnosis["configuration_issues"] = config_analysis.get("issues", [])
            diagnosis["configuration_warnings"] = config_analysis.get("warnings", [])
            diagnosis["issues"].extend(config_analysis.get("issues", []))
            if config_analysis.get("regex_issues"):
                diagnosis["regex_security_issues"] = config_analysis["regex_issues"]

            try:
                visualization_result = await visualize_infra_flow.visualize_infra_flow(
                    infrastructure_code=configuration_code,
                    infrastructure_type=infrastructure_type,
                    visualization_type="flow",
                    format="mermaid",
                    include_resources=True,
                    include_networking=True,
                    depth=3,
                )
                diagnosis["visualization"] = visualization_result.get("visualization", "")
                diagnosis["visualization_components"] = visualization_result.get("components", [])
                diagnosis["visualization_connections"] = visualization_result.get("connections", [])
                logger.info("Generated infrastructure visualization for troubleshooting")
            except Exception as e:
                logger.warning("Failed to generate visualization for troubleshooting: %s", e)

        github_url = None
        if configuration_code:
            import re
            github_match = re.search(r"github\.com[/:]([\w\-]+)/([\w\-]+)", configuration_code)
            if github_match:
                github_url = f"https://github.com/{github_match.group(1)}/{github_match.group(2)}"

        repository_structure = None
        if github_url:
            try:
                fetcher = GitHubTreeFetcher(github_token=None)
                tree_data = await fetcher.fetch_tree(
                    repo_url=github_url,
                    include_patterns=["**/*.tf", "**/*.yaml", "**/*.yml", "**/Dockerfile"],
                    max_depth=5,
                )
                repository_structure = tree_data.get("structure", {})
                diagnosis["repository_structure"] = repository_structure
                logger.info("Fetched repository structure for troubleshooting context")
            except Exception as e:
                logger.warning("Failed to fetch repository structure: %s", e)

        import asyncio

        query = f"{issue_description} {infrastructure_type} {cloud_provider} {resource_type}"

        async def gather_similar_solutions() -> list[dict[str, Any]]:
            """Gather similar solutions."""
            try:
                return await solution_builder.search_solutions(
                    query=query,
                    infrastructure_type=infrastructure_type,
                    cloud_provider=cloud_provider,
                    limit=5,
                )
            except Exception as e:
                logger.warning("Failed to gather similar solutions: %s", e)
                return []

        async def gather_similar_incidents() -> list[dict[str, Any]]:
            """Gather similar incidents."""
            try:
                return await incident_tracker.find_similar_incidents(
                    issue_description=issue_description,
                    infrastructure_type=infrastructure_type,
                    cloud_provider=cloud_provider,
                    limit=5,
                )
            except Exception as e:
                logger.warning("Failed to gather similar incidents: %s", e)
                return []

        async def gather_knowledge_results() -> list[dict[str, Any]]:
            """Gather knowledge base results."""
            try:
                return await vector_search.search_knowledge_articles(
                    query=query,
                    domains=["devops", "infrastructure", "security", "sre"],
                    limit=10,
                )
            except Exception as e:
                logger.warning("Failed to gather knowledge results: %s", e)
                return []

        async def gather_web_results() -> dict[str, Any] | None:
            """Gather web search results."""
            if not settings.tavily_api_key:
                return None
            try:
                web_search_client = WebSearchClient(api_key=settings.tavily_api_key)
                return await web_search_client.search_by_domain(
                    query=f"{issue_description} troubleshooting fix solution",
                    domains=["devops", "infrastructure"],
                    max_results=5,
                    max_age_days=90,
                )
            except Exception as e:
                logger.warning("Failed to search web for troubleshooting: %s", e)
                return None

        user_id = None

        async def gather_user_issues() -> tuple[list[dict[str, Any]], str | None]:
            """Gather user-specific issues and return user_id."""
            if not api_key or not configuration_code:
                return [], None
            try:
                user_info = await api_client.get_current_user(api_key=api_key)
                found_user_id = user_info.get("user_id")

                if found_user_id:
                    user_results = await vector_search.search_knowledge_articles(
                        query=query,
                        user_id=str(found_user_id),
                        include_global=False,
                        limit=5,
                    )
                    return user_results, str(found_user_id)
                return [], None
            except Exception as e:
                logger.warning("Failed to search user codebase: %s", e)
                return [], None

        results = await asyncio.gather(
            gather_similar_solutions(),
            gather_similar_incidents(),
            gather_knowledge_results(),
            gather_web_results(),
            gather_user_issues(),
            return_exceptions=True,
        )

        similar_solutions, similar_incidents, knowledge_results, web_results, user_issues_result = results

        if isinstance(similar_solutions, Exception):
            similar_solutions = []
        if isinstance(similar_incidents, Exception):
            similar_incidents = []
        if isinstance(knowledge_results, Exception):
            knowledge_results = []
        if isinstance(web_results, Exception):
            web_results = None
        if isinstance(user_issues_result, Exception):
            similar_user_issues = []
            user_id = None
        else:
            similar_user_issues, user_id = user_issues_result

        fixes = await _generate_fixes(
            issue_description=issue_description,
            error_messages=error_messages,
            configuration_code=configuration_code,
            knowledge_results=knowledge_results,
            web_results=web_results,
            diagnosis=diagnosis,
        )

        prevention = await _generate_prevention_strategies(
            issue_description=issue_description,
            infrastructure_type=infrastructure_type,
            knowledge_results=knowledge_results,
            diagnosis=diagnosis,
        )

        if web_results and web_results.get("results"):
            try:
                from api.services.web_search_storage_service import web_search_storage_service

                storage_stats = await web_search_storage_service.store_web_search_results(
                    web_results=web_results,
                    query=f"{issue_description} troubleshooting fix solution",
                    domains_searched=["devops", "infrastructure"],
                    store_in_background=True,
                )
                logger.info(
                    "Web search results storage initiated for troubleshooting: %d results, %d will be stored",
                    storage_stats["total_results"],
                    storage_stats.get("stored", 0) + storage_stats.get("converted", 0),
                )
            except Exception as e:
                logger.warning("Failed to store web search results from troubleshooting: %s", e, exc_info=True)

        if diagnosis["issues"]:
            diagnosis["root_cause"] = diagnosis["issues"][0] if diagnosis["issues"] else "Unable to determine root cause"
            diagnosis["confidence"] = "high" if len(diagnosis["issues"]) > 2 else "medium"

        incident = await incident_tracker.create_incident(
            issue_description=issue_description,
            diagnosis=diagnosis,
            fixes=fixes,
            infrastructure_type=infrastructure_type,
            cloud_provider=cloud_provider,
            resource_type=resource_type,
            error_messages=error_messages,
            configuration_code=configuration_code,
            logs=logs,
            user_id=user_id,
        )

        similar_incident_ids = [inc.incident_id for inc in similar_incidents]
        incident.similar_incidents = similar_incident_ids
        await incident_tracker._save_incident(incident)

        return {
            "incident_id": incident.incident_id,
            "diagnosis": diagnosis,
            "issues": diagnosis["issues"],
            "fixes": fixes,
            "prevention": prevention,
            "related_knowledge": knowledge_results,
            "similar_issues": similar_user_issues,
            "similar_incidents": [
                {
                    "incident_id": inc.incident_id,
                    "issue_description": inc.issue_description,
                    "status": inc.status.value,
                    "solution_applied": inc.solution_applied,
                }
                for inc in similar_incidents
            ],
            "similar_solutions": [
                {
                    "solution_id": sol.solution_id,
                    "problem_summary": sol.problem_summary,
                    "solution_description": sol.solution_description,
                    "success_rate": sol.success_rate,
                }
                for sol in similar_solutions
            ],
                "web_sources": web_results.get("results", []) if web_results else [],
            }

    except ValueError as e:
        logger.error("Validation error in troubleshoot_issue: %s", e)
        from wistx_mcp.tools.lib.error_handler import ErrorHandler

        error_info = ErrorHandler.format_error_with_remediation(
            e,
            context={"tool_name": "wistx_troubleshoot_issue"},
        )
        raise ValueError(
            f"{error_info['error_message']}\n"
            f"Remediation: {'; '.join(error_info['remediation_steps'][:3])}"
        ) from e
    except Exception as e:
        logger.error("Error in troubleshoot_issue: %s", e, exc_info=True)
        from wistx_mcp.tools.lib.error_handler import ErrorHandler

        error_info = ErrorHandler.format_error_with_remediation(
            e,
            context={"tool_name": "wistx_troubleshoot_issue"},
        )
        raise RuntimeError(
            f"Error in troubleshoot_issue: {error_info['error_message']}\n"
            f"Remediation: {'; '.join(error_info['remediation_steps'][:3])}"
        ) from e
    finally:
        if web_search_client:
            try:
                await web_search_client.close()
            except Exception as e:
                logger.warning("Error cleaning up web search client: %s", e)


async def _generate_fixes(
    issue_description: str,
    error_messages: list[str] | None,
    configuration_code: str | None,
    knowledge_results: list[dict[str, Any]],
    web_results: dict[str, Any] | None,
    diagnosis: dict[str, Any],
) -> list[dict[str, Any]]:
    """Generate fix recommendations with AI-powered synthesis.

    Args:
        issue_description: Issue description
        error_messages: Error messages
        configuration_code: Configuration code
        knowledge_results: Knowledge base results
        web_results: Web search results
        diagnosis: Diagnosis results

    Returns:
        List of fix recommendations
    """
    fixes = []

    try:
        from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer

        analyzer = AIAnalyzer()

        if analyzer.client and (knowledge_results or web_results or diagnosis.get("configuration_issues")):
            context_parts = []

            if knowledge_results:
                knowledge_context = "\n".join([
                    f"**{article.get('title', 'Article')}**: {article.get('summary', '')[:200]}"
                    for article in knowledge_results[:5]
                ])
                context_parts.append(f"Knowledge Base:\n{knowledge_context}")

            if web_results and web_results.get("results"):
                web_context = "\n".join([
                    f"**{result.get('title', 'Result')}**: {result.get('content', '')[:200]}"
                    for result in web_results["results"][:3]
                ])
                context_parts.append(f"Web Sources:\n{web_context}")

            if diagnosis.get("configuration_issues"):
                config_context = "\n".join(diagnosis["configuration_issues"])
                context_parts.append(f"Configuration Issues:\n{config_context}")

            context = "\n\n".join(context_parts)

            prompt = f"""
            Generate specific, actionable fixes for this infrastructure issue:

            **Issue**: {issue_description}

            **Error Messages**: {', '.join(error_messages or [])}

            **Configuration Code**:
            {configuration_code[:1000] if configuration_code else "Not provided"}

            **Root Cause**: {diagnosis.get('root_cause', 'Unknown')}

            **Context from Knowledge Base and Web**:
            {context}

            Generate 3-5 specific fixes. For each fix, provide:
            1. title: Clear, actionable title
            2. description: Detailed explanation of the fix
            3. code_example: Code snippet showing the fix (if applicable)
            4. steps: Step-by-step instructions
            5. confidence: "high", "medium", or "low"

            Return as JSON array of fix objects. Focus on practical, implementable solutions.
            """

            ai_response = await analyzer._call_llm(prompt)

            if ai_response:
                import json
                import re

                json_match = re.search(r"\[.*\]", ai_response, re.DOTALL)
                if json_match:
                    try:
                        ai_fixes = json.loads(json_match.group())
                        for fix in ai_fixes[:5]:
                            fixes.append({
                                "title": fix.get("title", "Fix"),
                                "description": fix.get("description", ""),
                                "code_example": fix.get("code_example", ""),
                                "steps": fix.get("steps", []),
                                "source": "ai_analysis",
                                "confidence": fix.get("confidence", "medium"),
                            })
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse AI fixes JSON, using fallback")
                        fixes.extend(_generate_fallback_fixes(
                            issue_description,
                            error_messages,
                            configuration_code,
                            knowledge_results,
                            web_results,
                            diagnosis,
                        ))
                else:
                    fixes.extend(_generate_fallback_fixes(
                        issue_description,
                        error_messages,
                        configuration_code,
                        knowledge_results,
                        web_results,
                        diagnosis,
                    ))
            else:
                fixes.extend(_generate_fallback_fixes(
                    issue_description,
                    error_messages,
                    configuration_code,
                    knowledge_results,
                    web_results,
                    diagnosis,
                ))
        else:
            fixes.extend(_generate_fallback_fixes(
                issue_description,
                error_messages,
                configuration_code,
                knowledge_results,
                web_results,
                diagnosis,
            ))
    except Exception as e:
        logger.warning("AI fix generation failed, using fallback: %s", e)
        fixes.extend(_generate_fallback_fixes(
            issue_description,
            error_messages,
            configuration_code,
            knowledge_results,
            web_results,
            diagnosis,
        ))

    return fixes[:10]


def _generate_fallback_fixes(
    issue_description: str,
    error_messages: list[str] | None,
    configuration_code: str | None,
    knowledge_results: list[dict[str, Any]],
    web_results: dict[str, Any] | None,
    diagnosis: dict[str, Any],
) -> list[dict[str, Any]]:
    """Generate fixes using fallback method (original implementation).

    Args:
        issue_description: Issue description
        error_messages: Error messages
        configuration_code: Configuration code
        knowledge_results: Knowledge base results
        web_results: Web search results
        diagnosis: Diagnosis results

    Returns:
        List of fix recommendations
    """
    fixes = []

    for article in knowledge_results[:5]:
        if article.get("content") or article.get("summary"):
            fixes.append({
                "title": article.get("title", ""),
                "description": article.get("summary", ""),
                "code_example": article.get("content", "")[:500] if article.get("content") else "",
                "source": "knowledge_base",
                "article_id": article.get("article_id", ""),
            })

    if web_results and web_results.get("results"):
        for result in web_results["results"][:3]:
            fixes.append({
                "title": result.get("title", ""),
                "description": result.get("content", "")[:300],
                "url": result.get("url", ""),
                "source": "web",
            })

    if diagnosis.get("configuration_issues"):
        for issue in diagnosis["configuration_issues"]:
            fixes.append({
                "title": f"Fix: {issue}",
                "description": "Address configuration issue",
                "source": "configuration_analysis",
            })

    return fixes


async def _generate_prevention_strategies(
    issue_description: str,
    infrastructure_type: str | None,
    knowledge_results: list[dict[str, Any]],
    diagnosis: dict[str, Any],
) -> list[str]:
    """Generate prevention strategies with AI analysis.

    Args:
        issue_description: Issue description
        infrastructure_type: Infrastructure type
        knowledge_results: Knowledge base results
        diagnosis: Diagnosis results

    Returns:
        List of prevention strategies
    """
    strategies = []

    try:
        from wistx_mcp.tools.lib.ai_analyzer import AIAnalyzer

        analyzer = AIAnalyzer()

        if analyzer.client and knowledge_results:
            knowledge_context = "\n".join([
                f"- {article.get('title', 'Article')}: {article.get('summary', '')[:150]}"
                for article in knowledge_results[:5]
            ])

            prompt = f"""
            Based on this infrastructure issue, generate prevention strategies:

            **Issue**: {issue_description}
            **Infrastructure Type**: {infrastructure_type or "unknown"}
            **Root Cause**: {diagnosis.get('root_cause', 'Unknown')}

            **Related Knowledge**:
            {knowledge_context}

            Generate 5 specific prevention strategies to avoid this issue in the future.
            Focus on:
            1. Proactive monitoring and alerting
            2. Infrastructure as code best practices
            3. Configuration validation
            4. Security measures
            5. Operational procedures

            Return as a JSON array of strategy strings. Be specific and actionable.
            """

            ai_response = await analyzer._call_llm(prompt)

            if ai_response:
                import json
                import re

                json_match = re.search(r"\[.*\]", ai_response, re.DOTALL)
                if json_match:
                    try:
                        ai_strategies = json.loads(json_match.group())
                        strategies.extend(ai_strategies[:5])
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse AI strategies JSON")
                        strategies.extend(_generate_fallback_prevention(
                            issue_description,
                            infrastructure_type,
                            knowledge_results,
                            diagnosis,
                        ))
                else:
                    strategies.extend(_generate_fallback_prevention(
                        issue_description,
                        infrastructure_type,
                        knowledge_results,
                        diagnosis,
                    ))
            else:
                strategies.extend(_generate_fallback_prevention(
                    issue_description,
                    infrastructure_type,
                    knowledge_results,
                    diagnosis,
                ))
        else:
            strategies.extend(_generate_fallback_prevention(
                issue_description,
                infrastructure_type,
                knowledge_results,
                diagnosis,
            ))
    except Exception as e:
        logger.warning("AI prevention generation failed, using fallback: %s", e)
        strategies.extend(_generate_fallback_prevention(
            issue_description,
            infrastructure_type,
            knowledge_results,
            diagnosis,
        ))

    return strategies[:5]


def _generate_fallback_prevention(
    issue_description: str,
    infrastructure_type: str | None,
    knowledge_results: list[dict[str, Any]],
    diagnosis: dict[str, Any],
) -> list[str]:
    """Generate prevention strategies using fallback method.

    Args:
        issue_description: Issue description
        infrastructure_type: Infrastructure type
        knowledge_results: Knowledge base results
        diagnosis: Diagnosis results

    Returns:
        List of prevention strategies
    """
    strategies = []

    for article in knowledge_results[:3]:
        content = (article.get("content", "") + " " + article.get("summary", "")).lower()
        if "prevent" in content or "best practice" in content:
            strategies.append(article.get("summary", ""))

    if not strategies:
        strategies = [
            "Implement proper error handling and logging",
            "Use infrastructure as code with validation",
            "Set up monitoring and alerting",
            "Follow best practices for the infrastructure type",
            "Regular security audits and compliance checks",
        ]

    if diagnosis.get("configuration_warnings"):
        strategies.append("Review configuration warnings and address them proactively")

    return strategies

