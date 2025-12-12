"""Generate documentation tool - create documentation and reports."""

import base64
import logging
import re
import sys
from datetime import datetime
from typing import Any

from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.document_generator import DocumentGenerator
from wistx_mcp.tools.lib.report_template_manager import ReportTemplateManager
from wistx_mcp.tools.lib.format_converter import FormatConverter
from wistx_mcp.tools.lib.template_library import TemplateLibrary
from wistx_mcp.models.report_template import OutputFormat
from wistx_mcp.config import settings

logger = logging.getLogger(__name__)

# Patch sys.exit to prevent api.config from exiting the MCP server
_original_sys_exit = sys.exit

def _mcp_safe_exit(code: int = 0) -> None:
    """MCP-safe sys.exit that raises SystemExit instead of exiting."""
    raise SystemExit(code)


async def generate_documentation(
    document_type: str,
    subject: str,
    infrastructure_code: str | None = None,
    configuration: dict[str, Any] | None = None,
    include_compliance: bool = True,
    include_security: bool = True,
    include_cost: bool = True,
    include_best_practices: bool = True,
    resource_types: list[str] | None = None,
    resource_ids: list[str] | None = None,
    compliance_standards: list[str] | None = None,
    resources: list[dict[str, Any]] | None = None,
    api_spec: dict[str, Any] | None = None,
    format: str = "markdown",
    template_id: str | None = None,
    custom_template: dict[str, Any] | None = None,
    branding: dict[str, Any] | None = None,
    api_key: str = "",
) -> dict[str, Any]:
    """Generate documentation and reports.

    Args:
        document_type: Type of document (architecture_diagram, runbook, compliance_report,
                      cost_report, security_report, api_documentation, deployment_guide,
                      project_overview)
        subject: Subject of the document (project name, resource, topic)
        infrastructure_code: Infrastructure code to document
        configuration: Configuration to document. For project_overview, supports:
                      - include_toc: bool (default True) - Include table of contents
        include_compliance: Include compliance information
        include_security: Include security information
        include_cost: Include cost information
        include_best_practices: Include best practices
        resource_types: List of resource types (for compliance/security reports)
        resource_ids: List of specific indexed resource IDs to filter knowledge articles.
                     For project_overview, these are the repositories to include in the overview.
        compliance_standards: List of compliance standards (for compliance report)
        resources: List of resource specifications (for cost report)
        api_spec: API specification (for api_documentation)
        format: Output format (markdown, pdf, html, json)
        template_id: Custom template ID (for compliance_report)
        custom_template: Custom template dictionary (alternative to template_id)
        branding: Branding configuration (logo, colors, etc.)

    Returns:
        Dictionary with documentation:
        - content: Generated documentation content
        - format: Output format
        - document_type: Type of document
        - sections: Document sections
        - metadata: Document metadata

    Raises:
        ValueError: If invalid document_type or parameters
        Exception: If generation fails
    """
    from wistx_mcp.tools.lib.auth_context import get_api_key_from_context

    api_key = get_api_key_from_context() or api_key

    valid_types = [
        "architecture_diagram",
        "runbook",
        "compliance_report",
        "cost_report",
        "security_report",
        "api_documentation",
        "deployment_guide",
        "project_overview",
        "infrastructure_import_report",
    ]

    if document_type not in valid_types:
        raise ValueError(f"Invalid document_type: {document_type}. Must be one of {valid_types}")

    if format not in ["markdown", "pdf", "html", "json", "docx"]:
        raise ValueError(f"Invalid format: {format}. Must be one of markdown, pdf, html, json, docx")

    from wistx_mcp.tools.lib.input_sanitizer import (
        validate_input_size,
        validate_infrastructure_code_input,
    )
    from wistx_mcp.tools.lib.constants import MAX_SUBJECT_LENGTH

    validate_input_size(subject, "subject", MAX_SUBJECT_LENGTH)

    if infrastructure_code:
        validate_infrastructure_code_input(infrastructure_code)

    from wistx_mcp.tools.lib.auth_context import validate_api_key_and_get_user_id, get_auth_context

    validated_user_id = None
    try:
        validated_user_id = await validate_api_key_and_get_user_id(api_key)
    except (ValueError, RuntimeError) as e:
        raise

    logger.info(
        "Generating documentation: type=%s, subject=%s, format=%s",
        document_type,
        subject,
        format,
    )

    auth_ctx = get_auth_context()
    user_id = validated_user_id
    if not user_id and auth_ctx:
        user_id = auth_ctx.get_user_id()
    
    if auth_ctx and user_id:
            try:
                sys.exit = _mcp_safe_exit
                from api.services.quota_service import quota_service, QuotaExceededError
                sys.exit = _original_sys_exit

                plan = "professional"
                if auth_ctx.user_info:
                    plan = auth_ctx.user_info.get("plan", "professional")
                await quota_service.check_query_quota(user_id, plan)
            except ImportError:
                sys.exit = _original_sys_exit
                logger.debug("API quota service not available, skipping quota check")
            except QuotaExceededError as e:
                sys.exit = _original_sys_exit
                logger.warning("Quota exceeded for user %s: %s", user_id, e)
                raise RuntimeError(f"Quota exceeded: {e}") from e
            except Exception as e:
                sys.exit = _original_sys_exit
                logger.warning("Failed to check quota (continuing): %s", e)

    try:
        async with MongoDBClient() as mongodb_client:

            generator = DocumentGenerator(mongodb_client)

            selected_resources_info = []
            if resource_ids and mongodb_client.database:
                try:
                    resources_collection = mongodb_client.database.indexed_resources
                    resource_docs = []
                    async for doc in resources_collection.find({"resource_id": {"$in": resource_ids}}):
                        resource_docs.append(doc)
                    
                    selected_resources_info = [
                        {
                            "resource_id": doc.get("resource_id"),
                            "name": doc.get("name"),
                            "resource_type": doc.get("resource_type"),
                            "repo_url": doc.get("repo_url"),
                            "documentation_url": doc.get("documentation_url"),
                            "document_url": doc.get("document_url"),
                        }
                        for doc in resource_docs
                    ]
                except Exception as e:
                    logger.warning("Failed to fetch resource details: %s", e)

            content = ""

            if document_type == "architecture_diagram":
                content = await generator.generate_architecture_doc(
                    subject=subject,
                    infrastructure_code=infrastructure_code,
                    configuration=configuration,
                    include_compliance=include_compliance,
                    include_security=include_security,
                )

                if include_security and infrastructure_code:
                    try:
                        from wistx_mcp.tools import regex_search

                        if api_key:
                            security_templates = ["api_key", "password", "secret_key"]
                            security_issues = []
                            for template in security_templates:
                                try:
                                    regex_results = await regex_search.regex_search_codebase(
                                        template=template,
                                        api_key=api_key,
                                        include_context=True,
                                        limit=5,
                                    )
                                    matches = regex_results.get("matches", [])
                                    if matches:
                                        security_issues.append({
                                            "type": template,
                                            "count": len(matches),
                                            "matches": matches[:3],
                                        })
                                except Exception as e:
                                    logger.warning("Regex search failed for template %s: %s", template, e)

                            if security_issues:
                                security_section = "\n\n## Security Issues Found\n\n"
                                for issue in security_issues:
                                    security_section += f"- **{issue['type'].replace('_', ' ').title()}**: Found {issue['count']} instances\n"
                                content += security_section
                    except ImportError:
                        logger.warning("regex_search module not available, skipping security checks")
                    except Exception as e:
                        logger.warning("Failed to add regex security checks to documentation: %s", e)

            elif document_type == "runbook":
                operations = configuration.get("operations") if configuration else None
                troubleshooting = configuration.get("troubleshooting") if configuration else None
                content = await generator.generate_runbook(
                    subject=subject,
                    operations=operations,
                    troubleshooting=troubleshooting,
                )

            elif document_type == "compliance_report":
                if not resource_types and not resource_ids:
                    raise ValueError("resource_types or resource_ids required for compliance_report")

                template_manager = ReportTemplateManager(mongodb_client)
                format_converter = FormatConverter()

                # Auto-select default template if none provided
                if not template_id and not custom_template:
                    # Get the first compliance standard or use PCI-DSS as default
                    standard = compliance_standards[0] if compliance_standards else "PCI-DSS"
                    default_template = await template_manager.get_default_template(
                        document_type="compliance_report",
                        compliance_standard=standard,
                    )
                    if default_template:
                        template_id = default_template.template_id
                        logger.info(
                            "Auto-selected default template %s for %s",
                            template_id,
                            standard,
                        )

                if template_id or custom_template:
                    template_data = None
                    if template_id:
                        template = await template_manager.get_template(template_id)
                        if not template:
                            raise ValueError(f"Template not found: {template_id}")
                    else:
                        template_dict = custom_template or {}
                        from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_types
                        
                        cloud_provider_for_template = configuration.get("cloud_provider") if configuration else None
                        normalized_resource_types_for_template = normalize_resource_types(resource_types or [], cloud_provider_for_template)
                        
                        template = await template_manager.register_template(
                            name=template_dict.get("name", "Custom Template"),
                            template_content=template_dict.get("template_content", ""),
                            document_type="compliance_report",
                            template_engine=template_dict.get("template_engine", "jinja2"),
                            compliance_standards=compliance_standards or [],
                            resource_types=normalized_resource_types_for_template,
                            variables=template_dict.get("variables", {}),
                            visibility="private",
                            user_id=None,
                        )

                    from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_types

                    cloud_provider = configuration.get("cloud_provider") if configuration else None
                    normalized_resource_types = normalize_resource_types(resource_types or [], cloud_provider)

                    compliance_data = await generator._fetch_compliance_data(
                        resource_types=normalized_resource_types,
                        standards=compliance_standards,
                        resource_ids=resource_ids,
                        cloud_provider=cloud_provider,
                    )

                    controls = compliance_data.get("controls", [])

                    # Use shared resource-mapping logic from DocumentGenerator
                    mapping_data = await generator._map_controls_to_resources(
                        controls=controls,
                        resource_ids=resource_ids,
                        resource_types=normalized_resource_types,
                        cloud_provider=cloud_provider,
                        selected_resources_info=selected_resources_info,
                    )

                    resource_list = mapping_data["resource_list"]
                    resource_compliance_summary = mapping_data["resource_compliance_summary"]
                    requirements_with_resources = mapping_data["requirements_with_resources"]

                    template_data = {
                        "subject": subject,
                        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "compliance_status": "Assessed",
                        "total_requirements": len(controls),
                        "compliant_requirements": 0,
                        "non_compliant_requirements": 0,
                        "compliance_score": 0.0,
                        "resources": resource_list,
                        "resource_compliance_summary": resource_compliance_summary,
                        "assessment_start": datetime.now().strftime("%Y-%m-%d"),
                        "assessment_end": datetime.now().strftime("%Y-%m-%d"),
                        "requirements": requirements_with_resources,
                        "recommendations": [],
                    }

                    rendered_content = await template_manager.render_template(
                        template_id=template.template_id,
                        data=template_data,
                        output_format=OutputFormat(format.upper()),
                    )

                    if format == "pdf":
                        pdf_bytes = format_converter.markdown_to_pdf(
                            rendered_content,
                            styles=template.styles,
                            branding=branding or template.branding,
                        )
                        return {
                            "content": pdf_bytes,
                            "format": "pdf",
                            "document_type": document_type,
                            "subject": subject,
                            "sections": _extract_sections(rendered_content),
                            "metadata": {
                                "generated_at": datetime.now().isoformat(),
                                "template_id": template.template_id,
                                "template_name": template.name,
                            },
                        }
                    elif format == "html":
                        html_content = format_converter.markdown_to_html(
                            rendered_content,
                            styles=template.styles,
                        )
                        return {
                            "content": html_content,
                            "format": "html",
                            "document_type": document_type,
                            "subject": subject,
                            "sections": _extract_sections(rendered_content),
                            "metadata": {
                                "generated_at": datetime.now().isoformat(),
                                "template_id": template.template_id,
                                "template_name": template.name,
                            },
                        }
                    elif format == "docx":
                        docx_bytes = format_converter.markdown_to_docx(
                            rendered_content,
                            branding=branding or template.branding,
                        )
                        return {
                            "content": docx_bytes,
                            "format": "docx",
                            "document_type": document_type,
                            "subject": subject,
                            "sections": _extract_sections(rendered_content),
                            "metadata": {
                                "generated_at": datetime.now().isoformat(),
                                "template_id": template.template_id,
                                "template_name": template.name,
                            },
                        }
                    else:
                        content = rendered_content
                else:
                    from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_types
                    
                    cloud_provider = configuration.get("cloud_provider") if configuration else None
                    normalized_resource_types = normalize_resource_types(resource_types or [], cloud_provider)
                    
                    content = await generator.generate_compliance_report(
                        subject=subject,
                        resource_types=normalized_resource_types,
                        standards=compliance_standards,
                        resource_ids=resource_ids,
                        cloud_provider=cloud_provider,
                    )

            elif document_type == "security_report":
                from wistx_mcp.tools.lib.resource_type_normalizer import normalize_resource_types
                
                cloud_provider = configuration.get("cloud_provider") if configuration else None
                normalized_resource_types = normalize_resource_types(resource_types or [], cloud_provider)
                
                content = await generator.generate_security_report(
                    subject=subject,
                    resource_types=normalized_resource_types,
                    cloud_provider=cloud_provider,
                    resource_ids=resource_ids,
                )

                try:
                    from wistx_mcp.tools import regex_search

                    if api_key:
                        security_templates = ["api_key", "password", "secret_key", "token", "credential"]
                        security_issues = []
                        for template in security_templates:
                            try:
                                regex_results = await regex_search.regex_search_codebase(
                                    template=template,
                                    api_key=api_key,
                                    include_context=True,
                                    limit=10,
                                )
                                matches = regex_results.get("matches", [])
                                if matches:
                                    security_issues.append({
                                        "type": template,
                                        "count": len(matches),
                                        "matches": matches[:5],
                                    })
                            except Exception as e:
                                logger.warning("Regex search failed for template %s: %s", template, e)

                        if security_issues:
                            security_section = "\n\n## Security Audit Results\n\n"
                            security_section += f"**Total Issues Found**: {sum(issue['count'] for issue in security_issues)}\n\n"
                            for issue in security_issues:
                                security_section += f"### {issue['type'].replace('_', ' ').title()}\n\n"
                                security_section += f"Found {issue['count']} instances:\n\n"
                                for match in issue["matches"]:
                                    security_section += f"- File: `{match.get('file_path', 'unknown')}`\n"
                                    security_section += f"  Line {match.get('line_number', 'unknown')}: {match.get('match_text', '')[:100]}\n\n"
                            content += security_section
                except ImportError:
                    logger.warning("regex_search module not available, skipping security audit")
                except Exception as e:
                    logger.warning("Failed to add regex security checks to security report: %s", e)

            elif document_type == "cost_report":
                content = await generator.generate_cost_report(
                    subject=subject,
                    resources=resources,
                )

            elif document_type == "api_documentation":
                content = await generator.generate_api_documentation(
                    subject=subject,
                    api_spec=api_spec,
                )

            elif document_type == "deployment_guide":
                infrastructure_type = configuration.get("infrastructure_type") if configuration else None
                cloud_provider = configuration.get("cloud_provider") if configuration else None
                content = await generator.generate_deployment_guide(
                    subject=subject,
                    infrastructure_type=infrastructure_type,
                    cloud_provider=cloud_provider,
                    include_compliance=include_compliance,
                    include_security=include_security,
                    include_cost=include_cost,
                    include_best_practices=include_best_practices,
                    api_key=api_key,
                )

            elif document_type == "project_overview":
                include_toc = configuration.get("include_toc", True) if configuration else True
                content = await generator.generate_project_overview(
                    subject=subject,
                    resource_ids=resource_ids,
                    include_compliance=include_compliance,
                    include_security=include_security,
                    include_cost=include_cost,
                    include_toc=include_toc,
                    api_key=api_key,
                )

            elif document_type == "infrastructure_import_report":
                # Generate infrastructure import documentation from discovery results
                discovery_data = configuration.get("discovery_data", {}) if configuration else {}
                include_toc = configuration.get("include_toc", True) if configuration else True
                include_import_commands = configuration.get("include_import_commands", True) if configuration else True
                include_diagram = configuration.get("include_diagram", True) if configuration else True

                content = await generator.generate_infrastructure_import_report(
                    subject=subject,
                    discovery_data=discovery_data,
                    include_compliance=include_compliance,
                    include_security=include_security,
                    include_diagram=include_diagram,
                    include_import_commands=include_import_commands,
                    include_toc=include_toc,
                    api_key=api_key,
                )

            sections = _extract_sections(content)

            metadata = {
                "generated_at": datetime.now().isoformat(),
                "includes": {
                    "compliance": include_compliance,
                    "security": include_security,
                    "cost": include_cost,
                    "best_practices": include_best_practices,
                },
            }

            if resource_ids:
                metadata["resource_ids"] = resource_ids
            if selected_resources_info:
                metadata["selected_resources"] = selected_resources_info

            result = {
                "content": content,
                "format": format,
                "document_type": document_type,
                "subject": subject,
                "sections": sections,
                "metadata": metadata,
            }

            auth_ctx = get_auth_context()
            storage_user_id = validated_user_id
            if not storage_user_id and auth_ctx:
                if auth_ctx.user_info:
                    storage_user_id = auth_ctx.get_user_id()
                else:
                    try:
                        await auth_ctx.validate()
                        storage_user_id = auth_ctx.get_user_id()
                    except Exception as e:
                        logger.warning("Failed to validate auth context for report storage: %s", e)

            logger.info("Report storage check: validated_user_id=%s, storage_user_id=%s, auth_ctx=%s", validated_user_id, storage_user_id, auth_ctx is not None)

            if storage_user_id:
                try:
                    report_id = f"report-{datetime.now().strftime('%Y%m%d%H%M%S')}-{storage_user_id[:8]}"
                    output_format = format

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

                    from wistx_mcp.tools.lib.mongodb_client import execute_mongodb_operation
                    from wistx_mcp.tools.lib.constants import API_TIMEOUT_SECONDS

                    async def _insert_report() -> None:
                        logger.info("Starting report insertion: report_id=%s, user_id=%s", report_id, storage_user_id)
                        async with MongoDBClient() as mongodb_client:
                            if mongodb_client.database is None:
                                logger.error("MongoDB database is None after connection")
                                raise RuntimeError("MongoDB database not available")
                            reports_collection = mongodb_client.database.reports
                            logger.debug("Inserting report into collection: %s", reports_collection.name)

                            result = await reports_collection.insert_one({
                                "report_id": report_id,
                                "user_id": storage_user_id,
                                "document_type": document_type,
                                "subject": subject,
                                "format": output_format,
                                "content": content_b64,
                                "content_type": content_type,
                                "sections": sections,
                                "metadata": metadata,
                                "created_at": datetime.utcnow(),
                            })
                            logger.info("Report inserted successfully: inserted_id=%s", result.inserted_id)

                    await execute_mongodb_operation(
                        _insert_report,
                        timeout=API_TIMEOUT_SECONDS,
                        max_retries=3,
                    )

                    base_url = settings.api_url.rstrip("/") if hasattr(settings, "api_url") else ""
                    download_url = f"{base_url}/v1/reports/{report_id}/download?format={output_format}" if base_url else ""
                    view_url = f"{base_url}/v1/reports/{report_id}/view?format={output_format}" if base_url else ""

                    result["report_id"] = report_id
                    result["report_download_url"] = download_url
                    result["report_view_url"] = view_url

                    logger.info("Report generated and stored: %s for user %s", report_id, storage_user_id)
                except Exception as e:
                    logger.error("Error storing report in database: %s", e, exc_info=True)
                    logger.error("Report storage failed - report_id=%s, user_id=%s, error_type=%s", report_id, storage_user_id, type(e).__name__)
            else:
                logger.warning("Skipping report storage: storage_user_id is None or empty")

            return result
    except Exception as e:
        logger.error("Error in generate_documentation: %s", e, exc_info=True)
        raise


def _extract_sections(content: str) -> list[str]:
    """Extract section headers from markdown content.

    Args:
        content: Markdown content

    Returns:
        List of section headers
    """
    sections = re.findall(r"^#+\s+(.+)$", content, re.MULTILINE)
    return sections


def generate_toc(content: str, max_depth: int = 3) -> str:
    """Generate a table of contents from markdown content.

    Args:
        content: Markdown content
        max_depth: Maximum header depth to include (1-6)

    Returns:
        Markdown table of contents string
    """
    toc_lines = ["## Table of Contents\n"]
    header_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

    for match in header_pattern.finditer(content):
        level = len(match.group(1))
        title = match.group(2).strip()

        if level > max_depth:
            continue

        if title.lower() == "table of contents":
            continue

        anchor = title.lower()
        anchor = re.sub(r"[^\w\s-]", "", anchor)
        anchor = re.sub(r"\s+", "-", anchor)

        indent = "  " * (level - 1)
        toc_lines.append(f"{indent}- [{title}](#{anchor})")

    return "\n".join(toc_lines) + "\n"


def insert_toc_into_content(content: str, max_depth: int = 3) -> str:
    """Insert table of contents into markdown content after the first header.

    Args:
        content: Markdown content
        max_depth: Maximum header depth to include

    Returns:
        Content with TOC inserted
    """
    if "## Table of Contents" in content:
        return content

    toc = generate_toc(content, max_depth)

    first_header_match = re.search(r"^#\s+.+$", content, re.MULTILINE)
    if first_header_match:
        insert_pos = first_header_match.end()
        next_content = content[insert_pos:].lstrip()

        if next_content.startswith("**Generated**") or next_content.startswith("*Generated*"):
            gen_line_end = content.find("\n\n", insert_pos)
            if gen_line_end != -1:
                insert_pos = gen_line_end + 2

        return content[:insert_pos] + "\n\n" + toc + "\n" + content[insert_pos:]

    return toc + "\n" + content

