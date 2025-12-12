"""REST API endpoints for documentation and report generation."""

import base64
import logging
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from api.dependencies import get_current_user
from api.dependencies.plan_enforcement import require_query_quota
from api.models.v1_responses import APIResponse, ErrorResponse
from wistx_mcp.tools.generate_documentation import generate_documentation
from wistx_mcp.tools.lib.mongodb_client import MongoDBClient
from wistx_mcp.tools.lib.report_template_manager import ReportTemplateManager
from wistx_mcp.tools.lib.format_converter import FormatConverter
from wistx_mcp.models.report_template import OutputFormat

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reports", tags=["reports"])


class GenerateReportRequest(BaseModel):
    """Request model for generating a report."""

    document_type: str = Field(
        ...,
        description="Type of document (compliance_report, security_report, cost_report, etc.)",
    )
    subject: str = Field(..., description="Subject of the document")
    resource_ids: list[str] | None = Field(
        default=None,
        description="List of specific indexed resource IDs to include in report (filters to user's resources)",
    )
    resource_types: list[str] | None = Field(default=None, description="List of resource types")
    compliance_standards: list[str] | None = Field(default=None, description="List of compliance standards")
    format: str = Field(default="markdown", description="Output format (markdown, html, pdf, docx)")
    template_id: str | None = Field(default=None, description="Custom template ID")
    custom_template: dict[str, Any] | None = Field(default=None, description="Custom template dictionary")
    branding: dict[str, Any] | None = Field(default=None, description="Branding configuration")
    include_compliance: bool = Field(default=True, description="Include compliance information")
    include_security: bool = Field(default=True, description="Include security information")
    include_cost: bool = Field(default=True, description="Include cost information")
    include_best_practices: bool = Field(default=True, description="Include best practices")


class ReportResponse(BaseModel):
    """Response model for report generation."""

    report_id: str = Field(..., description="Report identifier")
    document_type: str = Field(..., description="Document type")
    subject: str = Field(..., description="Subject")
    format: str = Field(..., description="Output format")
    content: str | bytes = Field(..., description="Report content (base64 for binary formats)")
    content_type: str = Field(..., description="Content type (text/markdown, application/pdf, etc.)")
    sections: list[str] = Field(default_factory=list, description="Document sections")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Report metadata")
    download_url: str = Field(..., description="URL to download the report")
    view_url: str = Field(..., description="URL to view the report")


class ReportListItem(BaseModel):
    """Response model for report list item (without content)."""

    report_id: str = Field(..., description="Report identifier")
    document_type: str = Field(..., description="Document type")
    subject: str = Field(..., description="Subject")
    format: str = Field(..., description="Output format")
    sections: list[str] = Field(default_factory=list, description="Document sections")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Report metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    download_url: str = Field(..., description="URL to download the report")
    view_url: str = Field(..., description="URL to view the report")


@router.post(
    "/generate",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate documentation or report",
    description="Generate comprehensive documentation and reports in various formats (Markdown, HTML, PDF, DOCX).",
)
async def generate_report(
    request: GenerateReportRequest,
    http_request: Request,
    current_user: dict[str, Any] = Depends(require_query_quota),
) -> APIResponse:
    """Generate a documentation or report.

    Args:
        request: Generate report request
        http_request: HTTP request object
        current_user: Current authenticated user

    Returns:
        API response with report data

    Raises:
        HTTPException: If generation fails
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    resource_ids = request.resource_ids
    if resource_ids:
        from api.services.indexing_service import indexing_service

        user_resources = await indexing_service.list_resources(
            user_id=str(user_id),
            organization_id=current_user.get("organization_id"),
        )
        user_resource_ids = {r.resource_id for r in user_resources}

        invalid_ids = set(resource_ids) - user_resource_ids
        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied to resources: {', '.join(invalid_ids)}",
            )

    try:
        api_key = current_user.get("api_key", "")
        result = await generate_documentation(
            document_type=request.document_type,
            subject=request.subject,
            resource_types=request.resource_types,
            resource_ids=resource_ids,
            compliance_standards=request.compliance_standards,
            format=request.format,
            template_id=request.template_id,
            custom_template=request.custom_template,
            branding=request.branding,
            include_compliance=request.include_compliance,
            include_security=request.include_security,
            include_cost=request.include_cost,
            include_best_practices=request.include_best_practices,
            api_key=api_key,
        )

        report_id = f"report-{datetime.now().strftime('%Y%m%d%H%M%S')}-{user_id[:8]}"

        content = result.get("content", "")
        output_format = result.get("format", "markdown")

        content_type_map = {
            "markdown": "text/markdown",
            "html": "text/html",
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "json": "application/json",
            "xml": "application/xml",
        }

        content_type = content_type_map.get(output_format, "text/plain")

        if isinstance(content, bytes):
            content_b64 = base64.b64encode(content).decode("utf-8")
        else:
            content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")

        mongodb_client = MongoDBClient()
        await mongodb_client.connect()
        if mongodb_client.database is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed",
            )
        reports_collection = mongodb_client.database.reports

        from bson import ObjectId

        try:
            user_id_obj = ObjectId(user_id)
        except Exception:
            user_id_obj = user_id

        await reports_collection.insert_one({
            "report_id": report_id,
            "user_id": user_id_obj,
            "document_type": result.get("document_type", request.document_type),
            "subject": result.get("subject", request.subject),
            "format": output_format,
            "content": content_b64,
            "content_type": content_type,
            "sections": result.get("sections", []),
            "metadata": result.get("metadata", {}),
            "created_at": datetime.utcnow(),
        })

        base_url = str(http_request.base_url).rstrip("/")
        download_url = f"{base_url}/v1/reports/{report_id}/download?format={output_format}"
        view_url = f"{base_url}/v1/reports/{report_id}/view?format={output_format}"

        response_data = ReportResponse(
            report_id=report_id,
            document_type=result.get("document_type", request.document_type),
            subject=result.get("subject", request.subject),
            format=output_format,
            content=content_b64,
            content_type=content_type,
            sections=result.get("sections", []),
            metadata=result.get("metadata", {}),
            download_url=download_url,
            view_url=view_url,
        )

        return APIResponse(
            data=response_data.model_dump(),
            metadata={
                "message": "Report generated successfully",
            },
        )

    except ValueError as e:
        logger.warning("Invalid request for report generation: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "INVALID_REQUEST",
                "message": str(e),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e

    except Exception as e:
        logger.error("Error generating report: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "REPORT_GENERATION_FAILED",
                "message": "Failed to generate report",
                "details": {"error": str(e)},
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/{report_id}/download",
    summary="Download report",
    description="Download a generated report in the specified format.",
)
async def download_report(
    report_id: str,
    format: str = Query(default="markdown", description="Output format (markdown, html, pdf, docx, xlsx, csv, xml)"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> StreamingResponse:
    """Download a report in the specified format.

    Args:
        report_id: Report identifier
        format: Output format (markdown, html, pdf, docx)
        current_user: Current authenticated user

    Returns:
        StreamingResponse with report content

    Raises:
        HTTPException: If report not found or download fails
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        mongodb_client = MongoDBClient()
        await mongodb_client.connect()

        if mongodb_client.database is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed",
            )
        reports_collection = mongodb_client.database.reports

        from bson import ObjectId

        query_conditions = [{"report_id": report_id, "user_id": user_id}]
        try:
            query_conditions.append({"report_id": report_id, "user_id": ObjectId(user_id)})
        except Exception:
            pass
        
        report_doc = await reports_collection.find_one({"$or": query_conditions})
        
        if not report_doc:
            logger.warning("Report not found for download: report_id=%s, user_id=%s", report_id, user_id)
            all_reports = await reports_collection.find({"report_id": report_id}).to_list(length=5)
            if all_reports:
                logger.debug("Found %d reports with report_id=%s (without user filter). User IDs: %s", len(all_reports), report_id, [str(r.get("user_id")) for r in all_reports])
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report not found: {report_id}",
            )

        content = report_doc.get("content")
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report content not found",
            )

        if isinstance(content, str):
            content_bytes = base64.b64decode(content)
        else:
            content_bytes = content

        stored_format = report_doc.get("format", "markdown")
        content_type_map = {
            "markdown": "text/markdown",
            "html": "text/html",
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "csv": "text/csv",
            "xml": "application/xml",
        }

        if format != stored_format:
            try:
                format_converter = FormatConverter()
                if stored_format in ("pdf", "docx", "xlsx"):
                    raise ValueError(f"Cannot convert from binary format {stored_format}")

                content_str = content_bytes.decode("utf-8") if isinstance(content_bytes, bytes) else str(content_bytes)
                content_bytes = format_converter.convert_format(
                    content=content_str,
                    source_format=stored_format,
                    target_format=format,
                    branding=report_doc.get("metadata", {}).get("branding"),
                )
                logger.info("Converted report from %s to %s", stored_format, format)
            except ValueError as e:
                logger.warning("Format conversion not supported: %s", e)
                # Return proper error instead of silently falling back to wrong format
                # This prevents corrupted files (e.g., markdown content with PDF mime type)
                error_msg = str(e)
                if "WeasyPrint" in error_msg:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="PDF generation is not available. WeasyPrint system dependencies are missing. Please download in another format (HTML, Markdown, or DOCX).",
                    ) from e
                elif "openpyxl" in error_msg:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Excel generation is not available. Please download in another format (CSV, HTML, or Markdown).",
                    ) from e
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Format conversion not supported: {error_msg}",
                    ) from e
            except Exception as e:
                logger.error("Format conversion failed: %s", e, exc_info=True)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to convert report format: {str(e)}",
                ) from e

        content_type = content_type_map.get(format, "application/octet-stream")
        filename = f"{report_doc.get('subject', 'report')}.{format}"

        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": content_type,
        }
        
        if format.lower() in ("pdf", "docx", "xlsx"):
            headers["Content-Length"] = str(len(content_bytes))
        
        return StreamingResponse(
            iter([content_bytes]),
            media_type=content_type,
            headers=headers,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error downloading report: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to download report",
        ) from e


@router.get(
    "/{report_id}/view",
    summary="View report",
    description="View a generated report in the browser (HTML format).",
)
async def view_report(
    report_id: str,
    format: str = Query(default="html", description="Output format (html or markdown)"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> Response:
    """View a report in the browser.

    Args:
        report_id: Report identifier
        format: Output format (html or markdown)
        current_user: Current authenticated user

    Returns:
        Response with report content

    Raises:
        HTTPException: If report not found or view fails
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        mongodb_client = MongoDBClient()
        await mongodb_client.connect()

        if mongodb_client.database is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed",
            )
        reports_collection = mongodb_client.database.reports

        from bson import ObjectId

        query_conditions = [{"report_id": report_id, "user_id": user_id}]
        try:
            query_conditions.append({"report_id": report_id, "user_id": ObjectId(user_id)})
        except Exception:
            pass
        
        report_doc = await reports_collection.find_one({"$or": query_conditions})
        
        if not report_doc:
            logger.warning("Report not found for view: report_id=%s, user_id=%s", report_id, user_id)
            all_reports = await reports_collection.find({"report_id": report_id}).to_list(length=5)
            if all_reports:
                logger.debug("Found %d reports with report_id=%s (without user filter). User IDs: %s", len(all_reports), report_id, [str(r.get("user_id")) for r in all_reports])
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report not found: {report_id}",
            )

        content = report_doc.get("content")
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report content not found",
            )

        if isinstance(content, str):
            content_bytes = base64.b64decode(content)
        else:
            content_bytes = content

        stored_format = report_doc.get("format", "markdown")
        
        if format == "html" and stored_format != "html":
            try:
                format_converter = FormatConverter()
                if stored_format in ("pdf", "docx", "xlsx"):
                    raise ValueError(f"Cannot convert from binary format {stored_format}")
                content_str = content_bytes.decode("utf-8") if isinstance(content_bytes, bytes) else str(content_bytes)
                html_content = format_converter.convert_format(
                    content=content_str,
                    source_format=stored_format,
                    target_format="html",
                )
                content_str = html_content.decode("utf-8") if isinstance(html_content, bytes) else html_content
            except Exception as e:
                logger.warning("Format conversion failed for view: %s", e, exc_info=True)
                content_str = content_bytes.decode("utf-8") if isinstance(content_bytes, bytes) else str(content_bytes)
            return Response(content=content_str, media_type="text/html")
        elif format == "markdown":
            content_str = content_bytes.decode("utf-8") if isinstance(content_bytes, bytes) else str(content_bytes)
            return Response(content=content_str, media_type="text/markdown")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Format {format} not supported for viewing. Use 'html' or 'markdown'.",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error viewing report: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to view report",
        ) from e


@router.get(
    "/formats",
    response_model=APIResponse,
    summary="Get available report formats",
    description="Get list of available report formats and their capabilities.",
)
async def get_available_formats(
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """Get available report formats.

    Returns:
        List of formats with metadata (name, mime_type, available, description)
    """
    from wistx_mcp.tools.lib.format_converter import (
        WEASYPRINT_AVAILABLE,
        OPENPYXL_AVAILABLE,
    )

    formats = [
        {
            "name": "markdown",
            "mime_type": "text/markdown",
            "available": True,
            "description": "Markdown format (.md)",
            "category": "text",
        },
        {
            "name": "html",
            "mime_type": "text/html",
            "available": True,
            "description": "HTML format (.html)",
            "category": "web",
        },
        {
            "name": "pdf",
            "mime_type": "application/pdf",
            "available": WEASYPRINT_AVAILABLE,
            "description": "PDF document (.pdf)",
            "category": "document",
        },
        {
            "name": "docx",
            "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "available": True,
            "description": "Microsoft Word document (.docx)",
            "category": "document",
        },
        {
            "name": "xlsx",
            "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "available": OPENPYXL_AVAILABLE,
            "description": "Microsoft Excel spreadsheet (.xlsx)",
            "category": "spreadsheet",
        },
        {
            "name": "csv",
            "mime_type": "text/csv",
            "available": True,
            "description": "Comma-separated values (.csv)",
            "category": "spreadsheet",
        },
        {
            "name": "xml",
            "mime_type": "application/xml",
            "available": True,
            "description": "XML format (.xml)",
            "category": "data",
        },
    ]

    return APIResponse(
        success=True,
        data={"formats": formats},
        message="Available formats retrieved successfully",
    )


@router.get(
    "",
    response_model=APIResponse,
    summary="List reports",
    description="List all reports generated by the current user.",
)
async def list_reports(
    document_type: str | None = Query(default=None, description="Filter by document type"),
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of reports to return"),
    offset: int = Query(default=0, ge=0, description="Number of reports to skip"),
    http_request: Request = None,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """List all reports for the current user.

    Args:
        document_type: Filter by document type (optional)
        limit: Maximum number of reports to return (default: 50, max: 100)
        offset: Number of reports to skip for pagination (default: 0)
        current_user: Current authenticated user
        http_request: HTTP request object for building URLs

    Returns:
        API response with list of reports
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        mongodb_client = MongoDBClient()
        await mongodb_client.connect()

        if mongodb_client.database is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed",
            )
        reports_collection = mongodb_client.database.reports

        from bson import ObjectId

        query_conditions = [{"user_id": user_id}]
        try:
            query_conditions.append({"user_id": ObjectId(user_id)})
        except Exception:
            pass
        
        query: dict[str, Any] = {"$or": query_conditions}
        if document_type:
            query["document_type"] = document_type

        cursor = reports_collection.find(query).sort("created_at", -1).skip(offset).limit(limit)
        total_count = await reports_collection.count_documents(query)
        total_count = await reports_collection.count_documents(query)

        reports = []
        base_url = str(http_request.base_url).rstrip("/") if http_request else ""

        async for doc in cursor:
            report_format = doc.get("format", "markdown")
            report_id = doc.get("report_id", "")

            download_url = f"{base_url}/v1/reports/{report_id}/download?format={report_format}" if base_url else ""
            view_url = f"{base_url}/v1/reports/{report_id}/view?format={report_format}" if base_url else ""

            report_item = ReportListItem(
                report_id=report_id,
                document_type=doc.get("document_type", ""),
                subject=doc.get("subject", ""),
                format=report_format,
                sections=doc.get("sections", []),
                metadata=doc.get("metadata", {}),
                created_at=doc.get("created_at", datetime.utcnow()),
                download_url=download_url,
                view_url=view_url,
            )
            reports.append(report_item)

        return APIResponse(
            data={
                "reports": [r.model_dump() for r in reports],
                "total": total_count,
                "limit": limit,
                "offset": offset,
            },
            metadata={
                "message": "Reports retrieved successfully",
            },
        )

    except Exception as e:
        logger.error("Error listing reports: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "REPORT_LIST_FAILED",
                "message": "Failed to list reports",
                "details": {"error": str(e)},
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete report",
    description="Delete a generated report by report ID.",
)
async def delete_report(
    report_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> None:
    """Delete a report.

    Args:
        report_id: Report identifier
        current_user: Current authenticated user

    Raises:
        HTTPException: If report not found or deletion fails
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        mongodb_client = MongoDBClient()
        await mongodb_client.connect()

        if mongodb_client.database is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed",
            )
        reports_collection = mongodb_client.database.reports

        result = await reports_collection.delete_one({"report_id": report_id, "user_id": user_id})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report not found: {report_id}",
            )

        logger.info("Report deleted: %s by user: %s", report_id, user_id)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting report: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "REPORT_DELETE_FAILED",
                "message": "Failed to delete report",
                "details": {"error": str(e)},
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/templates",
    response_model=APIResponse,
    summary="List report templates",
    description="List available report templates.",
)
async def list_templates(
    document_type: str | None = Query(default=None, description="Filter by document type"),
    compliance_standard: str | None = Query(default=None, description="Filter by compliance standard"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> APIResponse:
    """List available report templates.

    Args:
        document_type: Filter by document type
        compliance_standard: Filter by compliance standard
        current_user: Current authenticated user

    Returns:
        API response with list of templates
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")

    try:
        mongodb_client = MongoDBClient()
        await mongodb_client.connect()

        template_manager = ReportTemplateManager(mongodb_client)

        templates = await template_manager.search_templates(
            document_type=document_type,
            compliance_standard=compliance_standard,
            visibility="public",
            user_id=user_id,
            organization_id=organization_id,
            limit=50,
        )

        templates_data = [
            {
                "template_id": t.template_id,
                "name": t.name,
                "description": t.description,
                "version": t.version,
                "document_type": t.document_type,
                "compliance_standards": t.compliance_standards,
                "output_formats": [f.value for f in t.output_formats],
                "template_engine": t.template_engine.value,
            }
            for t in templates
        ]

        return APIResponse(
            data={"templates": templates_data, "total": len(templates_data)},
            metadata={
                "message": "Templates retrieved successfully",
            },
        )

    except Exception as e:
        logger.error("Error listing templates: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "TEMPLATE_LIST_FAILED",
                "message": "Failed to list templates",
                "details": {"error": str(e)},
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e

