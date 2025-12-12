"""Document update endpoints."""

import logging
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from api.dependencies import get_current_user
from api.models.indexing_requests import ReindexDocumentRequest, UpdateDocumentRequest
from api.models.indexing_responses import ResourceDetailResponse
from api.models.v1_responses import ErrorResponse
from api.services.indexing_service import indexing_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/indexing/documents", tags=["document-updates"])


@router.put(
    "/{resource_id}",
    response_model=ResourceDetailResponse,
    summary="Update document metadata",
    description="Update document metadata (name, description, tags) without re-indexing.",
)
async def update_document_metadata(
    resource_id: str,
    request: UpdateDocumentRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResourceDetailResponse:
    """Update document metadata.

    Args:
        resource_id: Resource ID
        request: Update request
        current_user: Current authenticated user

    Returns:
        Updated resource details

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
        resource = await indexing_service.update_document_metadata(
            resource_id=resource_id,
            user_id=user_id,
            name=request.name,
            description=request.description,
            tags=request.tags,
        )

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

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
        )

    except ValueError as e:
        logger.warning("Invalid update request: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating document metadata: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "UPDATE_ERROR",
                "message": "Failed to update document metadata",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.put(
    "/{resource_id}/content",
    response_model=ResourceDetailResponse,
    summary="Replace document content",
    description="Replace document content and optionally re-index.",
)
async def replace_document_content(
    resource_id: str,
    file: Optional[UploadFile] = File(default=None),
    document_url: Optional[str] = Form(default=None),
    re_index: bool = Form(default=True),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResourceDetailResponse:
    """Replace document content.

    Args:
        resource_id: Resource ID
        file: New file to upload
        document_url: New document URL
        re_index: Whether to re-index after replacement
        current_user: Current authenticated user

    Returns:
        Updated resource details

    Raises:
        HTTPException: If validation fails or resource not found
    """
    user_id = current_user.get("user_id")
    plan = current_user.get("plan", "professional")

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
            detail="Cannot provide both 'file' and 'document_url'",
        )

    tmp_file_path: Optional[Path] = None

    try:
        from api.utils.file_handler import file_handler

        if file:
            tmp_file_path, _ = await file_handler.save_uploaded_file(file=file, plan=plan)
        elif document_url:
            if document_url.startswith(("http://", "https://")):
                tmp_file_path, _ = await file_handler.download_file_from_url(
                    url=document_url,
                    plan=plan,
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="document_url must be an HTTP/HTTPS URL",
                )

        resource = await indexing_service.replace_document_content(
            resource_id=resource_id,
            user_id=user_id,
            file_path=tmp_file_path,
            re_index=re_index,
        )

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

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
        )

    except FileNotFoundError as e:
        logger.warning("File not found: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "FILE_NOT_FOUND",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.model_dump(),
        ) from e
    except ValueError as e:
        logger.warning("Invalid replacement request: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error replacing document content: %s", e, exc_info=True)
        if tmp_file_path and tmp_file_path.exists():
            from api.utils.file_handler import file_handler
            file_handler.cleanup_file(tmp_file_path)
        error_response = ErrorResponse(
            error={
                "code": "REPLACE_ERROR",
                "message": "Failed to replace document content",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.post(
    "/{resource_id}/reindex",
    response_model=ResourceDetailResponse,
    summary="Re-index document",
    description="Re-index an existing document with latest processing logic.",
)
async def reindex_document(
    resource_id: str,
    request: ReindexDocumentRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ResourceDetailResponse:
    """Re-index document.

    Args:
        resource_id: Resource ID
        request: Re-index request
        current_user: Current authenticated user

    Returns:
        Updated resource details

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
        resource = await indexing_service.reindex_document(
            resource_id=resource_id,
            user_id=user_id,
            force=request.force,
        )

        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found or access denied",
            )

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
        )

    except ValueError as e:
        logger.warning("Invalid re-index request: %s", e)
        error_response = ErrorResponse(
            error={
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "details": None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.model_dump(),
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error re-indexing document: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "REINDEX_ERROR",
                "message": "Failed to re-index document",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e

