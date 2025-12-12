"""Indexing endpoints for user-provided resources."""

import json
import logging
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status

from api.dependencies import get_current_user
from api.models.indexing import ResourceStatus, ResourceType
from api.models.indexing_requests import (
    IndexDocumentRequest,
    IndexDocumentationRequest,
    IndexRepositoryRequest,
    ReindexDocumentRequest,
    ReplaceDocumentContentRequest,
    UpdateDocumentRequest,
)
from api.models.indexing_responses import (
    ActivitiesListResponse,
    ActivityResponse,
    IndexResourceResponse,
    ResourceDetailResponse,
    ResourceListResponse,
)
from api.models.v1_responses import ErrorResponse
from api.services.indexing_service import indexing_service
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.services.usage_tracker import usage_tracker

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/indexing", tags=["indexing"])


@router.post(
    "/repositories",
    response_model=IndexResourceResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Index GitHub repository",
    description="Index a GitHub repository for user-specific search. Supports both public and private repositories.",
)
async def index_repository(
    request: IndexRepositoryRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> IndexResourceResponse:
    """Index a GitHub repository.

    Args:
        request: Index repository request
        current_user: Current authenticated user

    Returns:
        Index resource response with resource_id and status

    Raises:
        HTTPException: If quota exceeded or validation fails
    """
    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    organization_id = current_user.get("organization_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        await quota_service.check_indexing_quota(
            user_id=user_id,
            plan=plan,
            estimated_storage_mb=0.0,
        )
    except QuotaExceededError as e:
        logger.warning("Indexing quota exceeded for user %s: %s", user_id, e)
        error_response = ErrorResponse(
            error={
                "code": "QUOTA_EXCEEDED",
                "message": str(e),
                "details": {
                    "limit_type": e.limit_type,
                    "current": e.current,
                    "limit": e.limit,
                },
            },
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_response.model_dump(),
        ) from e

    try:
        from api.services.github_service import github_service

        repo_url_str = str(request.repo_url)

        access_info = await github_service.validate_repository_access(
            repo_url=repo_url_str,
            github_token=request.github_token,
            user_id=user_id,
        )

        if not access_info["accessible"]:
            if access_info.get("requires_oauth"):
                from api.services.oauth_service import oauth_service
                has_token = await oauth_service.has_github_token(user_id)
                
                if not has_token:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "error": "GITHUB_OAUTH_REQUIRED",
                            "message": "GitHub connection is required. Please connect your GitHub account in settings.",
                            "repository_info": access_info.get("repository_info"),
                            "authorization_url": "/v1/oauth/github/authorize",
                            "settings_url": "/settings/integrations",
                        },
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "error": "REPOSITORY_ACCESS_DENIED",
                            "message": "Access denied to this private repository. Check repository permissions.",
                            "repository_info": access_info.get("repository_info"),
                        },
                    )
            else:
                error_msg = access_info.get("error", "Repository access denied")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "error": "REPOSITORY_ACCESS_DENIED",
                        "message": error_msg,
                        "repository_info": access_info.get("repository_info"),
                    },
                )

        logger.info(
            "Repository access validated: %s (private: %s, token_source: %s)",
            repo_url_str,
            access_info["is_private"],
            access_info.get("token_source", "unknown"),
        )

        name = request.name or repo_url_str.split("/")[-1].replace(".git", "")

        resource = await indexing_service.create_resource(
            user_id=user_id,
            organization_id=organization_id,
            resource_type=ResourceType.REPOSITORY,
            name=name,
            description=request.description,
            tags=request.tags,
            repo_url=repo_url_str,
            branch=request.branch,
            github_token=request.github_token,
            include_patterns=request.include_patterns,
            exclude_patterns=request.exclude_patterns,
            compliance_standards=request.compliance_standards,
            environment_name=request.environment_name,
        )

        job_id = await indexing_service.start_indexing_job(
            resource_id=resource.resource_id,
            user_id=user_id,
            plan=plan,
            organization_id=organization_id,
        )

        await usage_tracker.track_indexing_operation(
            user_id=user_id,
            api_key_id=current_user.get("api_key_id", ""),
            index_type="repository",
            resource_id=resource.resource_id,
            documents_count=0,
            storage_mb=0.0,
            organization_id=organization_id,
            plan=plan,
        )

        return IndexResourceResponse(
            resource_id=resource.resource_id,
            status=resource.status,
            progress=resource.progress,
            message="Repository indexing started",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error indexing repository: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "INDEXING_ERROR",
                "message": "Failed to start repository indexing",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.post(
    "/documentation",
    response_model=IndexResourceResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Index documentation website",
    description="Index a documentation website for user-specific search.",
)
async def index_documentation(
    request: IndexDocumentationRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> IndexResourceResponse:
    """Index a documentation website.

    Args:
        request: Index documentation request
        current_user: Current authenticated user

    Returns:
        Index resource response with resource_id and status

    Raises:
        HTTPException: If quota exceeded or validation fails
    """
    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    organization_id = current_user.get("organization_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        await quota_service.check_indexing_quota(
            user_id=user_id,
            plan=plan,
            estimated_storage_mb=0.0,
        )
    except QuotaExceededError as e:
        logger.warning("Indexing quota exceeded for user %s: %s", user_id, e)
        error_response = ErrorResponse(
            error={
                "code": "QUOTA_EXCEEDED",
                "message": str(e),
                "details": {
                    "limit_type": e.limit_type,
                    "current": e.current,
                    "limit": e.limit,
                },
            },
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_response.model_dump(),
        ) from e

    try:
        doc_url_str = str(request.documentation_url)
        name = request.name or doc_url_str

        resource = await indexing_service.create_resource(
            user_id=user_id,
            organization_id=organization_id,
            resource_type=ResourceType.DOCUMENTATION,
            name=name,
            description=request.description,
            tags=request.tags,
            documentation_url=doc_url_str,
            include_patterns=request.include_patterns,
            exclude_patterns=request.exclude_patterns,
            max_pages=request.max_pages,
            max_depth=request.max_depth,
            incremental_update=request.incremental_update,
            compliance_standards=request.compliance_standards,
            environment_name=request.environment_name,
        )

        await indexing_service.start_indexing_job(
            resource_id=resource.resource_id,
            user_id=user_id,
            plan=plan,
        )

        await usage_tracker.track_indexing_operation(
            user_id=user_id,
            api_key_id=current_user.get("api_key_id", ""),
            index_type="documentation",
            resource_id=resource.resource_id,
            documents_count=0,
            storage_mb=0.0,
            organization_id=organization_id,
            plan=plan,
        )

        return IndexResourceResponse(
            resource_id=resource.resource_id,
            status=resource.status,
            progress=resource.progress,
            message="Documentation indexing started",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error indexing documentation: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "INDEXING_ERROR",
                "message": "Failed to start documentation indexing",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.post(
    "/documents",
    response_model=IndexResourceResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Index document",
    description="Upload and index a document (PDF, DOCX, Markdown, etc.) for user-specific search. "
                "Supports both file upload (multipart/form-data) and URL download (multipart/form-data).",
)
async def index_document(
    file: Optional[UploadFile] = File(default=None, description="Uploaded file (PDF, DOCX, Markdown, TXT)"),
    document_url: Optional[str] = Form(default=None, description="Document URL (http/https) or local file path"),
    document_type: Optional[str] = Form(default=None, description="Document type (auto-detected if not provided)"),
    name: Optional[str] = Form(default=None, description="Custom name for the resource"),
    description: Optional[str] = Form(default=None, description="Resource description"),
    tags: Optional[str] = Form(default=None, description="JSON array string of tags"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> IndexResourceResponse:
    """Index a document.

    Supports two modes:
    1. File upload (multipart/form-data): Provide 'file' parameter
    2. URL download (multipart/form-data): Provide 'document_url' parameter

    Args:
        file: Uploaded file (optional)
        document_url: Document URL or local path (optional)
        document_type: Document type (auto-detected if not provided)
        name: Custom name for the resource
        description: Resource description
        tags: JSON array string of tags
        current_user: Current authenticated user

    Returns:
        Index resource response with resource_id and status

    Raises:
        HTTPException: If validation fails, quota exceeded, or processing fails
    """
    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")
    organization_id = current_user.get("organization_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    if not file and not document_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'file' or 'document_url' must be provided",
        )

    if file and document_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot provide both 'file' and 'document_url'. Choose one.",
        )

    tag_list = []
    if tags:
        try:
            tag_list = json.loads(tags) if isinstance(tags, str) else tags
            if not isinstance(tag_list, list):
                tag_list = []
        except Exception:
            tag_list = []

    tmp_file_path: Optional[Path] = None
    detected_document_type: Optional[str] = None
    file_name: Optional[str] = None

    try:
        from api.utils.file_handler import file_handler

        if file:
            tmp_file_path, detected_document_type = await file_handler.save_uploaded_file(
                file=file,
                plan=plan,
            )
            file_name = file.filename or "uploaded_file"

        elif document_url:
            if document_url.startswith(("http://", "https://")):
                tmp_file_path, detected_document_type = await file_handler.download_file_from_url(
                    url=document_url,
                    plan=plan,
                )
                file_name = Path(document_url).name or "downloaded_file"
            else:
                tmp_file_path = Path(document_url)
                
                try:
                    validated_path = file_handler.validate_file_path(tmp_file_path)
                    tmp_file_path = validated_path
                except ValueError as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid file path: {str(e)}",
                    ) from e
                
                if not tmp_file_path.exists():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"File not found: {document_url}",
                    )
                
                if not file_handler.is_temporary_file(tmp_file_path):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="File must be in temporary directory",
                    )
                
                file_name = tmp_file_path.name
                detected_document_type = document_type or file_handler.validate_file_type(
                    file_name,
                    None,
                )

        final_document_type = document_type or detected_document_type

        if not final_document_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not determine document type. Please provide 'document_type' parameter.",
            )

        valid_document_types = {"pdf", "docx", "markdown", "md", "txt", "xml", "excel", "xlsx", "xls", "csv"}
        if final_document_type.lower() not in valid_document_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid document type: {final_document_type}. "
                       f"Supported types: {', '.join(valid_document_types)}",
            )

        file_size_mb = 0.0
        if tmp_file_path and tmp_file_path.exists():
            file_size_mb = tmp_file_path.stat().st_size / (1024 * 1024)

        try:
            await quota_service.check_indexing_quota(
                user_id=user_id,
                plan=plan,
                estimated_storage_mb=file_size_mb,
            )
        except QuotaExceededError as e:
            if tmp_file_path and tmp_file_path.exists():
                if document_url and document_url.startswith(("http://", "https://")) or file:
                    file_handler.cleanup_file(tmp_file_path)

            logger.warning("Indexing quota exceeded for user %s: %s", user_id, e)
            error_response = ErrorResponse(
                error={
                    "code": "QUOTA_EXCEEDED",
                    "message": str(e),
                    "details": {
                        "limit_type": e.limit_type,
                        "current": e.current,
                        "limit": e.limit,
                    },
                },
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_response.model_dump(),
            ) from e

        document_path_str = str(tmp_file_path) if tmp_file_path else document_url

        resource = await indexing_service.create_resource(
            user_id=user_id,
            organization_id=organization_id,
            resource_type=ResourceType.DOCUMENT,
            name=name or file_name or "Document",
            description=description,
            tags=tag_list,
            document_url=document_path_str,
            document_type=final_document_type.lower(),
        )

        await indexing_service.start_indexing_job(
            resource_id=resource.resource_id,
            user_id=user_id,
            plan=plan,
        )

        await usage_tracker.track_indexing_operation(
            user_id=user_id,
            api_key_id=current_user.get("api_key_id", ""),
            index_type="document",
            resource_id=resource.resource_id,
            documents_count=1,
            storage_mb=file_size_mb,
            organization_id=organization_id,
            plan=plan,
        )

        return IndexResourceResponse(
            resource_id=resource.resource_id,
            status=resource.status,
            progress=resource.progress,
            message="Document indexing started",
        )

    except HTTPException:
        raise
    except ValueError as e:
        logger.warning("Validation error indexing document: %s", e)
        if tmp_file_path and tmp_file_path.exists():
            if document_url and document_url.startswith(("http://", "https://")) or file:
                file_handler.cleanup_file(tmp_file_path)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except Exception as e:
        logger.error("Error indexing document: %s", e, exc_info=True)

        if tmp_file_path and tmp_file_path.exists():
            if document_url and document_url.startswith(("http://", "https://")) or file:
                from api.utils.file_handler import file_handler
                file_handler.cleanup_file(tmp_file_path)

        error_response = ErrorResponse(
            error={
                "code": "INDEXING_ERROR",
                "message": "Failed to start document indexing",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/resources",
    response_model=ResourceListResponse,
    summary="List indexed resources",
    description="List all indexed resources for the current user.",
)
async def list_resources(
    resource_type: ResourceType | None = Query(default=None, description="Filter by resource type"),
    status: ResourceStatus | None = Query(default=None, description="Filter by status"),
    deduplicate: bool = Query(default=True, description="Show only latest completed resource per repo"),
    show_duplicates: bool = Query(default=False, description="Include duplicate information"),
    include_ai_analysis: bool = Query(default=False, description="Include AI-analyzed insights (disabled by default for performance)"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResourceListResponse:
    """List indexed resources for user with enhanced options.

    Args:
        resource_type: Filter by resource type
        status: Filter by status
        deduplicate: Show only latest completed resource per repo
        show_duplicates: Include duplicate information
        include_ai_analysis: Include AI-analyzed insights
        current_user: Current authenticated user

    Returns:
        Resource list response with summary and deletion hints
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        resources = await indexing_service.list_resources(
            user_id=user_id,
            organization_id=organization_id,
            resource_type=resource_type,
            status=status,
        )

        resource_responses = [
            ResourceDetailResponse(
                resource_id=r.resource_id,
                user_id=r.user_id,
                organization_id=r.organization_id,
                resource_type=r.resource_type,
                status=r.status,
                progress=r.progress,
                name=r.name,
                description=r.description,
                tags=r.tags,
                repo_url=r.repo_url,
                branch=r.branch,
                documentation_url=r.documentation_url,
                document_url=r.document_url,
                articles_indexed=r.articles_indexed,
                files_processed=r.files_processed,
                total_files=r.total_files,
                storage_mb=r.storage_mb,
                error_message=r.error_message,
                error_details=r.error_details,
                created_at=r.created_at,
                updated_at=r.updated_at,
                indexed_at=r.indexed_at,
            )
            for r in resources
        ]

        response = ResourceListResponse(resources=resource_responses, total=len(resource_responses))

        if deduplicate or show_duplicates or include_ai_analysis:
            from api.utils.repo_normalizer import normalize_repo_url

            if deduplicate:
                grouped = {}
                duplicates = []

                for resource in resource_responses:
                    if resource.resource_type == ResourceType.REPOSITORY:
                        normalized_url = normalize_repo_url(resource.repo_url or "")
                        key = (user_id, normalized_url, resource.branch or "main")

                        if key in grouped:
                            existing = grouped[key]
                            existing_indexed_at = existing.indexed_at
                            resource_indexed_at = resource.indexed_at

                            if (
                                resource.status == ResourceStatus.COMPLETED
                                and existing.status != ResourceStatus.COMPLETED
                            ) or (
                                resource.status == ResourceStatus.COMPLETED
                                and existing.status == ResourceStatus.COMPLETED
                                and resource_indexed_at
                                and existing_indexed_at
                                and resource_indexed_at > existing_indexed_at
                            ):
                                duplicates.append(existing)
                                grouped[key] = resource
                            else:
                                duplicates.append(resource)
                        else:
                            grouped[key] = resource
                    else:
                        grouped[id(resource)] = resource

                resource_responses = list(grouped.values())
                response.resources = resource_responses
                response.total = len(resource_responses)

            response.summary = {
                "total": len(resource_responses),
                "by_type": {},
                "by_status": {},
                "deletion_info": (
                    "To delete a resource, use wistx_delete_resource with the resource_id. "
                    "Each resource in the list includes its resource_id field."
                ),
            }

            for resource in resource_responses:
                res_type = resource.resource_type.value if hasattr(resource.resource_type, "value") else str(resource.resource_type)
                res_status = resource.status.value if hasattr(resource.status, "value") else str(resource.status)
                response.summary["by_type"][res_type] = response.summary["by_type"].get(res_type, 0) + 1
                response.summary["by_status"][res_status] = response.summary["by_status"].get(res_status, 0) + 1

            if show_duplicates and deduplicate:
                response.summary["duplicate_count"] = len(duplicates)

            if include_ai_analysis and resource_responses:
                try:
                    from wistx_mcp.tools.lib.ai_analyzer import ai_analyzer
                    resources_dict = [r.model_dump() for r in resource_responses]
                    ai_analysis = await ai_analyzer.analyze_resource_collection(resources=resources_dict)
                    if ai_analysis:
                        response.ai_analysis = ai_analysis
                    else:
                        response.ai_analysis = {
                            "error": "AI analysis unavailable",
                            "reason": "service_unavailable",
                            "message": "AI analysis service is temporarily unavailable",
                        }
                except RuntimeError as e:
                    error_msg = str(e)
                    is_rate_limit = "rate limit" in error_msg.lower() or "quota" in error_msg.lower() or "temporarily unavailable" in error_msg.lower()
                    logger.warning("AI analysis failed: %s", e)
                    response.ai_analysis = {
                        "error": "AI analysis unavailable",
                        "reason": "rate_limit_exceeded" if is_rate_limit else "service_error",
                        "message": error_msg,
                    }
                except Exception as e:
                    logger.warning("AI analysis failed, continuing without analysis: %s", e)
                    response.ai_analysis = {
                        "error": "AI analysis unavailable",
                        "reason": "service_error",
                        "message": "AI analysis service encountered an error",
                    }

        for resource in response.resources:
            resource.deletion_hint = (
                f"Use wistx_delete_resource with resource_id='{resource.resource_id}' to delete this resource"
            )

        if not response.summary:
            response.summary = {
                "total": len(response.resources),
                "by_type": {},
                "by_status": {},
                "deletion_info": (
                    "To delete a resource, use wistx_delete_resource with the resource_id. "
                    "Each resource in the list includes its resource_id field."
                ),
            }
            for resource in response.resources:
                res_type = resource.resource_type.value if hasattr(resource.resource_type, "value") else str(resource.resource_type)
                res_status = resource.status.value if hasattr(resource.status, "value") else str(resource.status)
                response.summary["by_type"][res_type] = response.summary["by_type"].get(res_type, 0) + 1
                response.summary["by_status"][res_status] = response.summary["by_status"].get(res_status, 0) + 1

        return response

    except Exception as e:
        logger.error("Error listing resources: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list resources",
        ) from e


@router.get(
    "/resources/{resource_id}",
    response_model=ResourceDetailResponse,
    summary="Get resource details",
    description="Get detailed information about a specific indexed resource.",
)
async def get_resource(
    resource_id: str,
    include_sections: bool = Query(default=True, description="Include documentation sections"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResourceDetailResponse:
    """Get resource details with optional sections.

    Args:
        resource_id: Resource ID
        include_sections: Include documentation sections in response
        current_user: Current authenticated user

    Returns:
        Resource detail response with optional sections

    Raises:
        HTTPException: If resource not found or access denied
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        resource = await indexing_service.get_resource(resource_id, user_id)

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

        sections_data = None
        section_count = None

        if include_sections:
            try:
                from api.services.section_organizer import section_organizer
                from api.models.indexing_responses import SectionSummary

                sections = await section_organizer.get_sections_for_resource(
                    resource_id=resource_id,
                    user_id=user_id,
                )

                if sections:
                    sections_data = [
                        SectionSummary(
                            section_id=s.section_id,
                            title=s.title,
                            summary=s.summary,
                            section_type=s.section_type.value,
                            component_count=len(s.component_article_ids),
                        )
                        for s in sections
                    ]
                    section_count = len(sections)
            except Exception as e:
                logger.debug("Failed to load sections for resource %s: %s", resource_id, e)

        return ResourceDetailResponse(
            resource_id=resource.resource_id,
            user_id=resource.user_id,
            organization_id=resource.organization_id,
            resource_type=resource.resource_type,
            status=resource.status,
            progress=resource.progress,
            name=resource.name,
            description=resource.description,
            tags=resource.tags,
            repo_url=resource.repo_url,
            branch=resource.branch,
            documentation_url=resource.documentation_url,
            document_url=resource.document_url,
            articles_indexed=resource.articles_indexed,
            files_processed=resource.files_processed,
            total_files=resource.total_files,
            storage_mb=resource.storage_mb,
            error_message=resource.error_message,
            error_details=resource.error_details,
            created_at=resource.created_at,
            updated_at=resource.updated_at,
            indexed_at=resource.indexed_at,
            sections=sections_data,
            section_count=section_count,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting resource: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get resource",
        ) from e


@router.get(
    "/resources/{resource_id}/activities",
    response_model=ActivitiesListResponse,
    summary="Get indexing activities for a resource",
    description="Get detailed activity log for an indexing operation. Useful for real-time progress tracking.",
)
async def get_resource_activities(
    resource_id: str,
    limit: int = Query(default=100, ge=1, le=500, description="Maximum number of activities to return"),
    after_timestamp: Optional[str] = Query(default=None, description="Only return activities after this ISO timestamp"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ActivitiesListResponse:
    """Get indexing activities for a resource.

    Args:
        resource_id: Resource ID
        limit: Maximum number of activities to return
        after_timestamp: Only return activities after this timestamp (for polling)
        current_user: Current authenticated user

    Returns:
        List of indexing activities

    Raises:
        HTTPException: If resource not found or access denied
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        # Verify resource access
        resource = await indexing_service.get_resource(resource_id, user_id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

        # Parse after_timestamp if provided
        from datetime import datetime

        after_dt = None
        if after_timestamp:
            try:
                after_dt = datetime.fromisoformat(after_timestamp.replace("Z", "+00:00"))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid timestamp format. Use ISO 8601 format.",
                )

        # Get activities
        activities = await indexing_service.get_activities(
            resource_id=resource_id,
            limit=limit + 1,  # Fetch one extra to check if there are more
            after_timestamp=after_dt,
        )

        has_more = len(activities) > limit
        if has_more:
            activities = activities[:limit]

        # Convert to response models
        activity_responses = [
            ActivityResponse(
                activity_id=a.activity_id,
                activity_type=a.activity_type.value if hasattr(a.activity_type, "value") else str(a.activity_type),
                message=a.message,
                file_path=a.file_path,
                details=a.details,
                progress=a.progress,
                files_processed=a.files_processed,
                total_files=a.total_files,
                elapsed_seconds=a.elapsed_seconds,
                created_at=a.created_at,
            )
            for a in activities
        ]

        return ActivitiesListResponse(
            resource_id=resource_id,
            activities=activity_responses,
            total=len(activity_responses),
            has_more=has_more,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to get activities for resource %s: %s", resource_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get activities",
        ) from e


@router.get(
    "/resources/{resource_id}/articles",
    summary="Get knowledge articles for a resource",
    description="Get all knowledge articles indexed from a resource. Supports filtering by domain, content type, and search.",
)
async def get_resource_articles(
    resource_id: str,
    domain: Optional[str] = Query(default=None, description="Filter by domain (devops, compliance, finops, etc.)"),
    content_type: Optional[str] = Query(default=None, description="Filter by content type (guide, reference, tutorial, etc.)"),
    search: Optional[str] = Query(default=None, description="Search in title, summary, and content"),
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=20, ge=1, le=100, description="Items per page"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get knowledge articles for a resource.

    Args:
        resource_id: Resource ID
        domain: Filter by knowledge domain
        content_type: Filter by content type
        search: Search query
        page: Page number (1-based)
        limit: Items per page
        current_user: Current authenticated user

    Returns:
        Paginated list of knowledge articles with metadata

    Raises:
        HTTPException: If resource not found or access denied
    """
    from api.database.mongodb import mongodb_manager
    import re

    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        # Verify resource access
        resource = await indexing_service.get_resource(resource_id, user_id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

        db = mongodb_manager.get_database()
        collection = db.knowledge_articles

        # Build query
        query: dict[str, Any] = {"resource_id": resource_id}

        if domain:
            query["domain"] = domain
        if content_type:
            query["content_type"] = content_type
        if search:
            # Case-insensitive search in title, summary, and content
            search_regex = re.compile(re.escape(search), re.IGNORECASE)
            query["$or"] = [
                {"title": {"$regex": search_regex}},
                {"summary": {"$regex": search_regex}},
                {"content": {"$regex": search_regex}},
            ]

        # Get total count
        total = collection.count_documents(query)

        # Get paginated articles
        skip = (page - 1) * limit
        cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)

        articles = []
        domains_found: set[str] = set()
        content_types_found: set[str] = set()

        for doc in cursor:
            article_domain = doc.get("domain", "")
            article_content_type = doc.get("content_type", "")
            domains_found.add(article_domain)
            content_types_found.add(article_content_type)

            articles.append({
                "article_id": doc.get("article_id", doc.get("_id", "")),
                "title": doc.get("title", "Untitled"),
                "summary": doc.get("summary", ""),
                "content": doc.get("content", ""),
                "domain": article_domain,
                "subdomain": doc.get("subdomain", ""),
                "content_type": article_content_type,
                "tags": doc.get("tags", []),
                "categories": doc.get("categories", []),
                "source_url": doc.get("source_url", ""),
                "source_urls": doc.get("source_urls"),
                "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
                "updated_at": doc.get("updated_at").isoformat() if doc.get("updated_at") else None,
                "quality_score": doc.get("quality_score"),
                "structured_data": doc.get("structured_data", {}),
                "compliance_impact": doc.get("compliance_impact"),
                "cost_impact": doc.get("cost_impact"),
                "security_impact": doc.get("security_impact"),
                "cloud_providers": doc.get("cloud_providers", []),
                "services": doc.get("services", []),
            })

        # Get all unique domains and content types for filters (without pagination)
        all_domains = collection.distinct("domain", {"resource_id": resource_id})
        all_content_types = collection.distinct("content_type", {"resource_id": resource_id})

        return {
            "articles": articles,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit,
            "has_more": page * limit < total,
            "filters": {
                "domains": sorted([d for d in all_domains if d]),
                "content_types": sorted([ct for ct in all_content_types if ct]),
            },
            "resource": {
                "resource_id": resource.resource_id,
                "name": resource.name,
                "status": resource.status.value if resource.status else None,
                "articles_indexed": resource.articles_indexed,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to get articles for resource %s: %s", resource_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get articles",
        ) from e


@router.get(
    "/resources/{resource_id}/articles/{article_id}",
    summary="Get a specific knowledge article",
    description="Get full details of a specific knowledge article by ID.",
)
async def get_article_detail(
    resource_id: str,
    article_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get a specific knowledge article.

    Args:
        resource_id: Resource ID
        article_id: Article ID
        current_user: Current authenticated user

    Returns:
        Full article details

    Raises:
        HTTPException: If resource or article not found
    """
    from api.database.mongodb import mongodb_manager

    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        # Verify resource access
        resource = await indexing_service.get_resource(resource_id, user_id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

        db = mongodb_manager.get_database()
        collection = db.knowledge_articles

        # Find article
        doc = collection.find_one({
            "resource_id": resource_id,
            "$or": [
                {"article_id": article_id},
                {"_id": article_id},
            ],
        })

        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found",
            )

        return {
            "article_id": doc.get("article_id", doc.get("_id", "")),
            "title": doc.get("title", "Untitled"),
            "summary": doc.get("summary", ""),
            "content": doc.get("content", ""),
            "domain": doc.get("domain", ""),
            "subdomain": doc.get("subdomain", ""),
            "content_type": doc.get("content_type", ""),
            "tags": doc.get("tags", []),
            "categories": doc.get("categories", []),
            "industries": doc.get("industries", []),
            "cloud_providers": doc.get("cloud_providers", []),
            "services": doc.get("services", []),
            "source_url": doc.get("source_url", ""),
            "source_urls": doc.get("source_urls"),
            "references": doc.get("references", []),
            "related_articles": doc.get("related_articles", []),
            "related_controls": doc.get("related_controls", []),
            "structured_data": doc.get("structured_data", {}),
            "compliance_impact": doc.get("compliance_impact"),
            "cost_impact": doc.get("cost_impact"),
            "security_impact": doc.get("security_impact"),
            "quality_score": doc.get("quality_score"),
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
            "updated_at": doc.get("updated_at").isoformat() if doc.get("updated_at") else None,
            "commit_sha": doc.get("commit_sha"),
            "branch": doc.get("branch"),
            "resource": {
                "resource_id": resource.resource_id,
                "name": resource.name,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Failed to get article %s for resource %s: %s", article_id, resource_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get article",
        ) from e


@router.post(
    "/resources/{resource_id}/cancel",
    summary="Cancel indexing job",
    description="Cancel an active indexing job for the specified resource.",
)
async def cancel_indexing(
    resource_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Cancel an active indexing job.

    Args:
        resource_id: Resource ID of the job to cancel
        current_user: Current authenticated user

    Returns:
        Cancellation status information
    """
    user_id = current_user["sub"]

    try:
        result = await indexing_service.cancel_indexing(resource_id, user_id)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to cancel indexing"),
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error cancelling indexing for %s: %s", resource_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel indexing",
        ) from e


@router.post(
    "/resources/{resource_id}/retry",
    summary="Retry indexing job",
    description="Retry indexing for a failed resource.",
)
async def retry_indexing(
    resource_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Retry indexing for a failed resource.

    Args:
        resource_id: Resource ID of the failed job to retry
        current_user: Current authenticated user

    Returns:
        Retry status information
    """
    user_id = current_user["sub"]
    plan = current_user.get("plan", "professional")

    try:
        result = await indexing_service.retry_indexing(resource_id, user_id, plan)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to retry indexing"),
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error retrying indexing for %s: %s", resource_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retry indexing",
        ) from e


@router.delete(
    "/resources/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete indexed resource by ID",
    description="Delete an indexed resource and all associated knowledge articles by resource_id.",
)
async def delete_resource_by_id(
    resource_id: str,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> None:
    """Delete indexed resource by resource_id (legacy endpoint).

    Args:
        resource_id: Resource ID
        current_user: Current authenticated user

    Raises:
        HTTPException: If resource not found or access denied
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        success = await indexing_service.delete_resource(resource_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting resource: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete resource",
        ) from e


@router.delete(
    "/resources",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete indexed resource by identifier",
    description="Delete an indexed resource and all associated knowledge articles by resource_type and identifier.",
)
async def delete_resource(
    resource_type: ResourceType = Query(..., description="Type of resource"),
    identifier: str = Query(..., description="Resource identifier (repo URL, doc URL, or resource_id)"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> None:
    """Delete indexed resource by type and identifier.

    Args:
        resource_type: Type of resource
        identifier: Resource identifier (repository URL, documentation URL, document URL, or resource_id)
        current_user: Current authenticated user

    Raises:
        HTTPException: If resource not found or access denied
    """
    user_id = current_user.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    try:
        resource = await indexing_service.find_resource_by_identifier(
            identifier=identifier,
            resource_type=resource_type,
            user_id=user_id,
        )

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

        success = await indexing_service.delete_resource(resource.resource_id, user_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting resource: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete resource",
        ) from e



@router.get(
    "/resources/{resource_id}/cost-analysis",
    summary="Get cost analysis for indexed repository",
    description="Get aggregated cost analysis from knowledge articles for an indexed repository.",
)
async def get_cost_analysis(
    resource_id: str,
    refresh: bool = Query(default=False, description="Force recalculation"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get cost analysis for indexed repository.

    Args:
        resource_id: Resource ID
        refresh: Force recalculation
        current_user: Current authenticated user

    Returns:
        Cost analysis dictionary

    Raises:
        HTTPException: If resource not found or access denied
    """
    from api.services.repository_analysis_service import repository_analysis_service

    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    resource = await indexing_service.get_resource(resource_id, str(user_id))
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied",
        )

    try:
        analysis = await repository_analysis_service.get_cost_analysis(
            resource_id=resource_id,
            user_id=str(user_id),
            refresh=refresh,
        )

        return {
            "resource_id": resource_id,
            "repository_url": resource.repo_url,
            "environment_name": resource.environment_name,
            "cost_analysis": analysis,
        }
    except Exception as e:
        logger.error("Error getting cost analysis: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get cost analysis",
        ) from e


@router.get(
    "/resources/{resource_id}/compliance-analysis",
    summary="Get compliance analysis for indexed repository",
    description="Get aggregated compliance analysis from knowledge articles for an indexed repository.",
)
async def get_compliance_analysis(
    resource_id: str,
    standards: Optional[list[str]] = Query(default=None, description="Filter by compliance standards"),
    refresh: bool = Query(default=False, description="Force recalculation"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    """Get compliance analysis for indexed repository.

    Args:
        resource_id: Resource ID
        standards: Filter by compliance standards
        refresh: Force recalculation
        current_user: Current authenticated user

    Returns:
        Compliance analysis dictionary

    Raises:
        HTTPException: If resource not found or access denied
    """
    from api.services.repository_analysis_service import repository_analysis_service

    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found",
        )

    resource = await indexing_service.get_resource(resource_id, str(user_id))
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found or access denied",
        )

    try:
        analysis = await repository_analysis_service.get_compliance_analysis(
            resource_id=resource_id,
            user_id=str(user_id),
            standards=standards,
            refresh=refresh,
        )

        return {
            "resource_id": resource_id,
            "repository_url": resource.repo_url,
            "environment_name": resource.environment_name,
            "compliance_analysis": analysis,
        }
    except Exception as e:
        logger.error("Error getting compliance analysis: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get compliance analysis",
        ) from e
