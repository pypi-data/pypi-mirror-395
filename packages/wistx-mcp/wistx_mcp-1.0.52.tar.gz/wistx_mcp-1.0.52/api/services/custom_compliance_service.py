"""Service for managing custom compliance controls."""

import asyncio
import hashlib
import logging
import tempfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from bson import ObjectId
from fastapi import UploadFile

from api.database.mongodb import mongodb_manager
from api.exceptions import ValidationError, NotFoundError, AuthorizationError, DatabaseError
from api.models.compliance_custom import (
    CustomComplianceControlResponse,
    CustomControlsListResponse,
    DeleteCustomControlResponse,
    ReviewCustomControlResponse,
    UpdateCustomControlRequest,
    UploadComplianceDocumentResponse,
    UploadStatusResponse,
)
from api.services.exceptions import QuotaExceededError
from api.services.quota_service import quota_service
from api.utils.file_handler import file_handler
from data_pipelines.loaders.mongodb_loader import MongoDBLoader
from data_pipelines.loaders.pinecone_loader import PineconeLoader
from data_pipelines.models.compliance import ComplianceControl
from data_pipelines.processors.compliance_processor import ComplianceProcessor


def _safe_serialize(data: Any) -> dict | list | Any | None:
    """Safely serialize data that might be a dict, Pydantic model, or other type.

    Args:
        data: Data to serialize

    Returns:
        Serialized data (dict, list, or the original value if primitive)
    """
    if data is None:
        return None
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        return [_safe_serialize(item) for item in data]
    if hasattr(data, "model_dump"):
        return data.model_dump()
    if hasattr(data, "__dict__"):
        return data.__dict__
    return data
from data_pipelines.processors.document_processor import DocumentProcessor
from data_pipelines.processors.embedding_generator import EmbeddingGenerator
from data_pipelines.processors.llm_extractor import LLMControlExtractor

logger = logging.getLogger(__name__)


class CustomComplianceService:
    """Service for managing custom compliance controls."""

    def __init__(self):
        """Initialize custom compliance service."""
        self.document_processor = DocumentProcessor()
        self.llm_extractor = LLMControlExtractor()
        self.compliance_processor = ComplianceProcessor()
        self.embedding_generator = EmbeddingGenerator()
        self.mongodb_loader = MongoDBLoader()
        try:
            self.pinecone_loader = PineconeLoader()
        except Exception as e:
            logger.warning(
                "Failed to initialize Pinecone loader: %s. Vector search features will be disabled.",
                e,
            )
            self.pinecone_loader = None

    async def upload_and_process_document(
        self,
        file: UploadFile,
        user_id: str,
        organization_id: Optional[str],
        standard: str,
        version: str,
        visibility: str,
        name: Optional[str],
        description: Optional[str],
        auto_approve: bool,
        extraction_method: str,
    ) -> UploadComplianceDocumentResponse:
        """Upload and process compliance document.

        Args:
            file: Uploaded file
            user_id: User ID
            organization_id: Organization ID (optional)
            standard: Compliance standard name
            version: Standard version
            visibility: Visibility scope
            name: Document name
            description: Document description
            auto_approve: Auto-approve extracted controls
            extraction_method: Extraction method

        Returns:
            Upload response with upload_id
        """
        upload_id = str(uuid.uuid4())
        document_id = str(uuid.uuid4())

        file_content = await file.read()
        file_size = len(file_content)

        max_size = file_handler.get_max_file_size("professional")
        if file_size > max_size:
            raise ValidationError(
                message=f"File too large: {file_size} bytes (max: {max_size} bytes)",
                user_message=f"File is too large ({file_size} bytes). Maximum file size: {max_size} bytes.",
                error_code="FILE_TOO_LARGE",
                details={"file_size": file_size, "max_size": max_size, "filename": file.filename}
            )

        file_type = file_handler.validate_file_type(file.filename, file.content_type)

        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            tmp_path = Path(tmp_file.name)
            tmp_path.write_bytes(file_content)

        try:
            db = mongodb_manager.get_database()
            uploads_collection = db.compliance_uploads

            upload_doc = {
                "_id": upload_id,
                "upload_id": upload_id,
                "document_id": document_id,
                "user_id": ObjectId(user_id),
                "organization_id": ObjectId(organization_id) if organization_id else None,
                "file_name": file.filename,
                "file_size": file_size,
                "file_type": file_type,
                "file_path": str(tmp_path),
                "standard": standard,
                "version": version,
                "visibility": visibility,
                "name": name,
                "description": description,
                "auto_approve": auto_approve,
                "extraction_method": extraction_method,
                "status": "pending",
                "progress": 0.0,
                "controls_extracted": 0,
                "controls_pending_review": 0,
                "controls_approved": 0,
                "controls_rejected": 0,
                "error_message": None,
                "started_at": datetime.utcnow(),
                "completed_at": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }

            uploads_collection.insert_one(upload_doc)

            asyncio.create_task(
                self.process_document_async(
                    upload_id=upload_id,
                    document_path=tmp_path,
                    user_id=user_id,
                    organization_id=organization_id,
                    standard=standard,
                    version=version,
                    visibility=visibility,
                    auto_approve=auto_approve,
                    extraction_method=extraction_method,
                )
            )

            return UploadComplianceDocumentResponse(
                upload_id=upload_id,
                document_id=document_id,
                status="pending",
                controls_extracted=0,
                controls_pending_review=0,
                message="Document uploaded successfully. Processing started.",
            )

        except Exception as e:
            logger.error("Failed to upload document: %s", e, exc_info=True)
            if tmp_path.exists():
                tmp_path.unlink()
            raise DatabaseError(
                message=f"Failed to upload document: {str(e)}",
                user_message="Failed to upload document. Please try again later.",
                error_code="DOCUMENT_UPLOAD_ERROR",
                details={"filename": file.filename, "error": str(e)}
            ) from e

    async def process_document_async(
        self,
        upload_id: str,
        document_path: Path,
        user_id: str,
        organization_id: Optional[str],
        standard: str,
        version: str,
        visibility: str,
        auto_approve: bool,
        extraction_method: str,
    ) -> None:
        """Process document and extract controls (background job).

        Args:
            upload_id: Upload job ID
            document_path: Path to document file
            user_id: User ID
            organization_id: Organization ID
            standard: Compliance standard name
            version: Standard version
            visibility: Visibility scope
            auto_approve: Auto-approve extracted controls
            extraction_method: Extraction method
        """
        db = mongodb_manager.get_database()
        uploads_collection = db.compliance_uploads

        try:
            uploads_collection.update_one(
                {"upload_id": upload_id},
                {
                    "$set": {
                        "status": "processing",
                        "progress": 10.0,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            loop = asyncio.get_event_loop()
            doc_content = await loop.run_in_executor(
                None,
                lambda: self.document_processor.process_document(
                    content=document_path,
                    source_url=str(document_path),
                    content_type="auto",
                ),
            )

            uploads_collection.update_one(
                {"upload_id": upload_id},
                {
                    "$set": {
                        "progress": 30.0,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            text_content = doc_content.get("text", "") or doc_content.get("markdown", "")
            markdown_content = doc_content.get("markdown")

            raw_controls = await self.llm_extractor.extract_controls(
                content=text_content,
                standard=standard,
                source_url=str(document_path),
                prefer_markdown=True,
                markdown_content=markdown_content,
                user_id=user_id,
                organization_id=organization_id,
            )

            uploads_collection.update_one(
                {"upload_id": upload_id},
                {
                    "$set": {
                        "progress": 60.0,
                        "controls_extracted": len(raw_controls),
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            standardized_controls = []
            for idx, raw_control in enumerate(raw_controls):
                try:
                    control = self.compliance_processor.standardize_control(
                        raw=raw_control,
                        standard=standard,
                        version=version,
                        user_id=user_id,
                        organization_id=organization_id,
                        visibility=visibility,
                        is_custom=True,
                        source_document_id=upload_id,
                        source_document_name=document_path.name,
                        extraction_method=extraction_method,
                        extraction_confidence=raw_control.get("confidence"),
                    )

                    if auto_approve:
                        control.reviewed = True
                        control.reviewed_at = datetime.utcnow()
                        control.reviewed_by = user_id

                    standardized_controls.append(control)
                except Exception as e:
                    logger.error("Failed to standardize control %d: %s", idx, e, exc_info=True)
                    continue

            uploads_collection.update_one(
                {"upload_id": upload_id},
                {
                    "$set": {
                        "progress": 80.0,
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            searchable_texts = [control.to_searchable_text() for control in standardized_controls]
            embeddings = await self.embedding_generator.generate_embeddings_batch(searchable_texts)

            for control, embedding in zip(standardized_controls, embeddings):
                control.embedding = embedding

            controls_pending_review = len([c for c in standardized_controls if not c.reviewed])
            controls_approved = len([c for c in standardized_controls if c.reviewed])

            for control in standardized_controls:
                control_dict = control.model_dump(mode="json")
                control_dict["_id"] = control.control_id
                if user_id:
                    control_dict["user_id"] = ObjectId(user_id)
                if organization_id:
                    control_dict["organization_id"] = ObjectId(organization_id)

                self.mongodb_loader.save_single_control(control_dict)
                if self.pinecone_loader:
                    try:
                        self.pinecone_loader.upsert_single_control(control_dict)
                    except Exception as e:
                        logger.warning("Failed to upsert control to Pinecone: %s", e)

            uploads_collection.update_one(
                {"upload_id": upload_id},
                {
                    "$set": {
                        "status": "completed",
                        "progress": 100.0,
                        "controls_extracted": len(standardized_controls),
                        "controls_pending_review": controls_pending_review,
                        "controls_approved": controls_approved,
                        "completed_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    }
                },
            )

            logger.info(
                "Completed processing upload %s: %d controls extracted",
                upload_id,
                len(standardized_controls),
            )

        except Exception as e:
            logger.error("Failed to process document %s: %s", upload_id, e, exc_info=True)
            uploads_collection.update_one(
                {"upload_id": upload_id},
                {
                    "$set": {
                        "status": "failed",
                        "error_message": str(e),
                        "completed_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    }
                },
            )
        finally:
            if document_path.exists():
                document_path.unlink()

    async def get_upload_status(self, upload_id: str, user_id: str) -> UploadStatusResponse:
        """Get upload status.

        Args:
            upload_id: Upload ID
            user_id: User ID

        Returns:
            Upload status response
        """
        db = mongodb_manager.get_database()
        uploads_collection = db.compliance_uploads

        upload_doc = uploads_collection.find_one({"upload_id": upload_id, "user_id": ObjectId(user_id)})

        if not upload_doc:
            raise NotFoundError(
                message=f"Upload not found: {upload_id}",
                user_message="Upload not found",
                error_code="UPLOAD_NOT_FOUND",
                details={"upload_id": upload_id, "user_id": user_id}
            )

        return UploadStatusResponse(
            upload_id=upload_doc["upload_id"],
            document_id=upload_doc["document_id"],
            status=upload_doc["status"],
            progress=upload_doc.get("progress", 0.0),
            controls_extracted=upload_doc.get("controls_extracted", 0),
            controls_pending_review=upload_doc.get("controls_pending_review", 0),
            controls_approved=upload_doc.get("controls_approved", 0),
            controls_rejected=upload_doc.get("controls_rejected", 0),
            error_message=upload_doc.get("error_message"),
            started_at=upload_doc["started_at"],
            completed_at=upload_doc.get("completed_at"),
            estimated_completion_time=None,
        )

    async def list_custom_controls(
        self,
        user_id: str,
        organization_id: Optional[str],
        standard: Optional[str],
        visibility: Optional[str],
        reviewed: Optional[bool],
        limit: int,
        offset: int,
    ) -> CustomControlsListResponse:
        """List custom compliance controls.

        Args:
            user_id: User ID
            organization_id: Organization ID
            standard: Filter by standard
            visibility: Filter by visibility
            reviewed: Filter by review status
            limit: Pagination limit
            offset: Pagination offset

        Returns:
            List of custom controls
        """
        db = mongodb_manager.get_database()
        controls_collection = db.compliance_controls

        query: dict[str, Any] = {"is_custom": True}

        visibility_filters = []
        if organization_id:
            visibility_filters.append({
                "organization_id": ObjectId(organization_id),
                "visibility": {"$in": ["organization", "global"]},
            })
        visibility_filters.append({
            "user_id": ObjectId(user_id),
            "visibility": {"$in": ["user", "global"]},
        })
        if visibility_filters:
            query["$or"] = visibility_filters

        if standard:
            query["standard"] = standard

        if visibility:
            if "$or" in query:
                for filter_item in query["$or"]:
                    filter_item["visibility"] = visibility
            else:
                query["visibility"] = visibility

        if reviewed is not None:
            query["reviewed"] = reviewed

        total = controls_collection.count_documents(query)

        cursor = controls_collection.find(query).skip(offset).limit(limit).sort("created_at", -1)

        controls = []
        for doc in cursor:
            control = self._doc_to_control_response(doc)
            controls.append(control)

        return CustomControlsListResponse(
            controls=controls,
            total=total,
            limit=limit,
            offset=offset,
            has_more=(offset + limit) < total,
        )

    def _doc_to_control_response(self, doc: dict[str, Any]) -> CustomComplianceControlResponse:
        """Convert MongoDB document to control response.

        Args:
            doc: MongoDB document

        Returns:
            Control response
        """
        return CustomComplianceControlResponse(
            control_id=doc["control_id"],
            standard=doc["standard"],
            version=doc.get("version", "1.0"),
            title=doc["title"],
            description=doc["description"],
            requirement=doc.get("requirement"),
            severity=doc["severity"],
            category=doc.get("category"),
            subcategory=doc.get("subcategory"),
            applies_to=doc.get("applies_to", []),
            remediation=_safe_serialize(doc.get("remediation")),
            verification=_safe_serialize(doc.get("verification")),
            references=_safe_serialize(doc.get("references", [])),
            visibility=doc.get("visibility", "global"),
            is_custom=doc.get("is_custom", False),
            source=doc.get("source", "wistx"),
            source_document_id=doc.get("source_document_id"),
            source_document_name=doc.get("source_document_name"),
            extraction_method=doc.get("extraction_method"),
            extraction_confidence=doc.get("extraction_confidence"),
            reviewed=doc.get("reviewed", False),
            reviewed_at=doc.get("reviewed_at"),
            reviewed_by=doc.get("reviewed_by"),
            created_at=doc.get("created_at", datetime.utcnow()),
            updated_at=doc.get("updated_at", datetime.utcnow()),
        )

    async def get_custom_control(
        self,
        control_id: str,
        user_id: str,
        organization_id: Optional[str],
    ) -> CustomComplianceControlResponse:
        """Get custom compliance control by ID.

        Args:
            control_id: Control ID
            user_id: User ID
            organization_id: Organization ID

        Returns:
            Compliance control

        Raises:
            HTTPException: If control not found or access denied
        """
        db = mongodb_manager.get_database()
        controls_collection = db.compliance_controls

        doc = controls_collection.find_one({"control_id": control_id, "is_custom": True})

        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control not found",
            )

        if not self._check_control_access(doc, user_id, organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        return self._doc_to_control_response(doc)

    def _check_control_access(
        self,
        control_doc: dict[str, Any],
        user_id: str,
        organization_id: Optional[str],
    ) -> bool:
        """Check if user can access control.

        Args:
            control_doc: Control document
            user_id: User ID
            organization_id: Organization ID

        Returns:
            True if user can access, False otherwise
        """
        control_user_id = str(control_doc.get("user_id", ""))
        control_org_id = str(control_doc.get("organization_id", ""))
        visibility = control_doc.get("visibility", "global")

        if not control_doc.get("is_custom", False):
            return True

        if control_user_id == user_id and visibility == "user":
            return True

        if control_org_id == organization_id and visibility == "organization":
            return True

        if visibility == "global":
            return True

        return False

    async def update_custom_control(
        self,
        control_id: str,
        user_id: str,
        organization_id: Optional[str],
        updates: UpdateCustomControlRequest,
    ) -> CustomComplianceControlResponse:
        """Update custom compliance control.

        Args:
            control_id: Control ID
            user_id: User ID
            organization_id: Organization ID
            updates: Update fields

        Returns:
            Updated compliance control

        Raises:
            HTTPException: If control not found or access denied
        """
        db = mongodb_manager.get_database()
        controls_collection = db.compliance_controls

        doc = controls_collection.find_one({"control_id": control_id, "is_custom": True})

        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control not found",
            )

        if not self._check_control_access(doc, user_id, organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        update_dict: dict[str, Any] = {"updated_at": datetime.utcnow()}

        if updates.title is not None:
            update_dict["title"] = updates.title
        if updates.description is not None:
            update_dict["description"] = updates.description
        if updates.requirement is not None:
            update_dict["requirement"] = updates.requirement
        if updates.severity is not None:
            update_dict["severity"] = updates.severity
        if updates.category is not None:
            update_dict["category"] = updates.category
        if updates.subcategory is not None:
            update_dict["subcategory"] = updates.subcategory
        if updates.applies_to is not None:
            update_dict["applies_to"] = updates.applies_to
        if updates.remediation is not None:
            update_dict["remediation"] = updates.remediation
        if updates.verification is not None:
            update_dict["verification"] = updates.verification
        if updates.references is not None:
            update_dict["references"] = updates.references
        if updates.visibility is not None:
            update_dict["visibility"] = updates.visibility
        if updates.reviewed is not None:
            update_dict["reviewed"] = updates.reviewed
            if updates.reviewed:
                update_dict["reviewed_at"] = datetime.utcnow()
                update_dict["reviewed_by"] = user_id

        controls_collection.update_one({"control_id": control_id}, {"$set": update_dict})

        if updates.title or updates.description or updates.requirement:
            control_doc = controls_collection.find_one({"control_id": control_id})
            if control_doc:
                control = ComplianceControl.model_validate(control_doc)
                searchable_text = control.to_searchable_text()
                embedding = await self.embedding_generator.generate_embeddings_batch([searchable_text])
                if embedding:
                    controls_collection.update_one(
                        {"control_id": control_id},
                        {"$set": {"embedding": embedding[0]}},
                    )
                    control_dict = control_doc.copy()
                    control_dict["embedding"] = embedding[0]
                    if self.pinecone_loader:
                        try:
                            self.pinecone_loader.upsert_single_control(control_dict)
                        except Exception as e:
                            logger.warning("Failed to upsert control to Pinecone: %s", e)

        updated_doc = controls_collection.find_one({"control_id": control_id})
        return self._doc_to_control_response(updated_doc)

    async def delete_custom_control(
        self,
        control_id: str,
        user_id: str,
        organization_id: Optional[str],
    ) -> DeleteCustomControlResponse:
        """Delete custom compliance control.

        Args:
            control_id: Control ID
            user_id: User ID
            organization_id: Organization ID

        Returns:
            Deletion response

        Raises:
            HTTPException: If control not found or access denied
        """
        db = mongodb_manager.get_database()
        controls_collection = db.compliance_controls

        doc = controls_collection.find_one({"control_id": control_id, "is_custom": True})

        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control not found",
            )

        if not self._check_control_access(doc, user_id, organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        controls_collection.delete_one({"control_id": control_id})

        if self.pinecone_loader:
            try:
                self.pinecone_loader.delete_single_control(control_id)
            except Exception as e:
                logger.warning("Failed to delete control from Pinecone: %s", e)

        return DeleteCustomControlResponse(
            control_id=control_id,
            deleted=True,
            message="Control deleted successfully",
        )

    async def review_custom_control(
        self,
        control_id: str,
        user_id: str,
        organization_id: Optional[str],
        approved: bool,
        notes: Optional[str],
    ) -> ReviewCustomControlResponse:
        """Review/approve custom compliance control.

        Args:
            control_id: Control ID
            user_id: User ID
            organization_id: Organization ID
            approved: Whether approved
            notes: Review notes

        Returns:
            Review response
        """
        db = mongodb_manager.get_database()
        controls_collection = db.compliance_controls

        doc = controls_collection.find_one({"control_id": control_id, "is_custom": True})

        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control not found",
            )

        if not self._check_control_access(doc, user_id, organization_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        update_dict = {
            "reviewed": True,
            "reviewed_at": datetime.utcnow(),
            "reviewed_by": user_id,
            "updated_at": datetime.utcnow(),
        }

        if notes:
            update_dict["review_notes"] = notes

        controls_collection.update_one({"control_id": control_id}, {"$set": update_dict})

        return ReviewCustomControlResponse(
            control_id=control_id,
            reviewed=True,
            reviewed_at=datetime.utcnow(),
            reviewed_by=user_id,
            notes=notes,
        )


custom_compliance_service = CustomComplianceService()

