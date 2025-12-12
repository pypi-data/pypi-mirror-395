"""Custom compliance controls endpoints for v1 API."""

import logging
from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status

from api.dependencies import get_current_user
from api.dependencies.plan_enforcement import require_custom_compliance_access
from api.models.compliance_custom import (
    CustomComplianceControlResponse,
    CustomControlsListResponse,
    DeleteCustomControlResponse,
    ReviewCustomControlRequest,
    ReviewCustomControlResponse,
    UpdateCustomControlRequest,
    UploadComplianceDocumentResponse,
    UploadStatusResponse,
)
from api.models.v1_responses import APIResponse, ErrorResponse
from api.services.custom_compliance_service import custom_compliance_service
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/compliance/custom-controls", tags=["compliance", "custom-controls"])


@router.post(
    "/upload",
    response_model=APIResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload compliance document",
    description="Upload a compliance document (PDF, DOCX, XML, Excel, CSV, TXT, Markdown) for custom control extraction",
)
async def upload_compliance_document(
    file: UploadFile = File(...),
    standard: str = Form(...),
    version: str = Form(default="1.0"),
    visibility: str = Form(
        default="organization",
        pattern="^(organization|user|global)$",
    ),
    name: Optional[str] = Form(default=None),
    description: Optional[str] = Form(default=None),
    auto_approve: bool = Form(default=False),
    extraction_method: str = Form(
        default="llm",
        pattern="^(llm|structured|manual)$",
    ),
    current_user: Annotated[dict[str, Any], Depends(require_custom_compliance_access)] = None,
) -> APIResponse:
    """Upload compliance document for custom control extraction.

    Args:
        file: Uploaded file
        standard: Compliance standard name
        version: Standard version
        visibility: Visibility scope
        name: Document name
        description: Document description
        auto_approve: Auto-approve extracted controls
        extraction_method: Extraction method
        current_user: Current authenticated user

    Returns:
        Upload response with upload_id
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")
    plan = current_user.get("plan", "professional")

    try:
        await quota_service.check_custom_controls_quota(user_id, plan, controls_count=1)
    except QuotaExceededError as e:
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
        response = await custom_compliance_service.upload_and_process_document(
            file=file,
            user_id=user_id,
            organization_id=organization_id,
            standard=standard,
            version=version,
            visibility=visibility,
            name=name,
            description=description,
            auto_approve=auto_approve,
            extraction_method=extraction_method,
        )

        return APIResponse(
            data=response.model_dump(),
            metadata={"message": "Document uploaded successfully. Processing started."},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to upload compliance document: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "UPLOAD_FAILED",
                "message": "Failed to upload document",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/upload/{upload_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get upload status",
    description="Get status of compliance document upload and processing",
)
async def get_upload_status(
    upload_id: str,
    current_user: Annotated[dict[str, Any], Depends(require_custom_compliance_access)] = None,
) -> APIResponse:
    """Get upload status.

    Args:
        upload_id: Upload ID
        current_user: Current authenticated user

    Returns:
        Upload status response
    """
    user_id = current_user.get("user_id")

    try:
        response = await custom_compliance_service.get_upload_status(upload_id, user_id)
        return APIResponse(data=response.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get upload status: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "STATUS_FAILED",
                "message": "Failed to get upload status",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="List custom compliance controls",
    description="List custom compliance controls with filtering and pagination",
)
async def list_custom_controls(
    standard: Optional[str] = Query(default=None, description="Filter by standard"),
    visibility: Optional[str] = Query(default=None, description="Filter by visibility"),
    reviewed: Optional[bool] = Query(default=None, description="Filter by review status"),
    limit: int = Query(default=100, ge=1, le=1000, description="Pagination limit"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    current_user: Annotated[dict[str, Any], Depends(require_custom_compliance_access)] = None,
) -> APIResponse:
    """List custom compliance controls.

    Args:
        standard: Filter by standard
        visibility: Filter by visibility
        reviewed: Filter by review status
        limit: Pagination limit
        offset: Pagination offset
        current_user: Current authenticated user

    Returns:
        List of custom controls
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")

    try:
        response = await custom_compliance_service.list_custom_controls(
            user_id=user_id,
            organization_id=organization_id,
            standard=standard,
            visibility=visibility,
            reviewed=reviewed,
            limit=limit,
            offset=offset,
        )
        return APIResponse(data=response.model_dump())
    except Exception as e:
        logger.error("Failed to list custom controls: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "LIST_FAILED",
                "message": "Failed to list custom controls",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.get(
    "/{control_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Get custom compliance control",
    description="Get a specific custom compliance control by ID",
)
async def get_custom_control(
    control_id: str,
    current_user: Annotated[dict[str, Any], Depends(require_custom_compliance_access)] = None,
) -> APIResponse:
    """Get custom compliance control by ID.

    Args:
        control_id: Control ID
        current_user: Current authenticated user

    Returns:
        Compliance control
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")

    try:
        response = await custom_compliance_service.get_custom_control(
            control_id=control_id,
            user_id=user_id,
            organization_id=organization_id,
        )
        return APIResponse(data=response.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get custom control: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "GET_FAILED",
                "message": "Failed to get custom control",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.put(
    "/{control_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Update custom compliance control",
    description="Update a custom compliance control",
)
async def update_custom_control(
    control_id: str,
    updates: UpdateCustomControlRequest,
    current_user: Annotated[dict[str, Any], Depends(require_custom_compliance_access)] = None,
) -> APIResponse:
    """Update custom compliance control.

    Args:
        control_id: Control ID
        updates: Update fields
        current_user: Current authenticated user

    Returns:
        Updated compliance control
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")

    try:
        response = await custom_compliance_service.update_custom_control(
            control_id=control_id,
            user_id=user_id,
            organization_id=organization_id,
            updates=updates,
        )
        return APIResponse(data=response.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update custom control: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "UPDATE_FAILED",
                "message": "Failed to update custom control",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.delete(
    "/{control_id}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete custom compliance control",
    description="Delete a custom compliance control",
)
async def delete_custom_control(
    control_id: str,
    current_user: Annotated[dict[str, Any], Depends(require_custom_compliance_access)] = None,
) -> APIResponse:
    """Delete custom compliance control.

    Args:
        control_id: Control ID
        current_user: Current authenticated user

    Returns:
        Deletion response
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")

    try:
        response = await custom_compliance_service.delete_custom_control(
            control_id=control_id,
            user_id=user_id,
            organization_id=organization_id,
        )
        return APIResponse(data=response.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete custom control: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "DELETE_FAILED",
                "message": "Failed to delete custom control",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e


@router.post(
    "/{control_id}/review",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Review custom compliance control",
    description="Review and approve/reject a custom compliance control",
)
async def review_custom_control(
    control_id: str,
    review: ReviewCustomControlRequest,
    current_user: Annotated[dict[str, Any], Depends(require_custom_compliance_access)] = None,
) -> APIResponse:
    """Review custom compliance control.

    Args:
        control_id: Control ID
        review: Review request
        current_user: Current authenticated user

    Returns:
        Review response
    """
    user_id = current_user.get("user_id")
    organization_id = current_user.get("organization_id")

    try:
        response = await custom_compliance_service.review_custom_control(
            control_id=control_id,
            user_id=user_id,
            organization_id=organization_id,
            approved=review.approved,
            notes=review.notes,
        )
        return APIResponse(data=response.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to review custom control: %s", e, exc_info=True)
        error_response = ErrorResponse(
            error={
                "code": "REVIEW_FAILED",
                "message": "Failed to review custom control",
                "details": str(e) if logger.isEnabledFor(logging.DEBUG) else None,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response.model_dump(),
        ) from e

