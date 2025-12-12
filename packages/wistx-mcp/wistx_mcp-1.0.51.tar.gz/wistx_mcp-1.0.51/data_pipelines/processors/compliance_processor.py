"""Compliance data processor - transforms raw compliance data into standardized models."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ..models.compliance import (
    CodeSnippet,
    ComplianceControl,
    Reference,
    Remediation,
)
from ..utils.config import PipelineSettings
from ..utils.logger import setup_logger
from ..utils.sanitization import sanitize_control_id, sanitize_text, sanitize_url
from .category_resource_mapper import CategoryResourceMapper
from .document_processor import DocumentProcessor

logger = setup_logger(__name__)
settings = PipelineSettings()


class ComplianceProcessor:
    """Process raw compliance data into standardized ComplianceControl models.

    Supports both streaming (production) and checkpointing (development) modes.
    """

    def __init__(self, save_intermediate: bool = False):
        """Initialize compliance processor.

        Args:
            save_intermediate: If True, save processed data to disk (checkpointing mode)
        """
        self.save_intermediate = save_intermediate
        self.data_dir = settings.data_dir / "compliance"
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.pdf_dir = Path(__file__).parent.parent / "collectors" / "pdf"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.document_processor = DocumentProcessor()
        self.resource_mapper = CategoryResourceMapper()

    def load_raw_data(self, standard: str) -> list[dict[str, Any]]:
        """Load raw compliance data for a standard (sync wrapper).

        Includes both JSON files. PDF processing should use async method.

        Args:
            standard: Compliance standard name (e.g., "PCI-DSS", "CIS")

        Returns:
            List of raw compliance control dictionaries
        """
        all_data = []

        patterns = [
            f"{standard.lower().replace('-', '_')}*.json",
            f"{standard.lower().replace('-', '_')}-raw.json",
        ]
        
        files = []
        for pattern in patterns:
            found = list(self.raw_dir.glob(pattern))
            if found:
                files.extend(found)
                break
        
        if not files:
            logger.warning("No JSON files found for standard %s in %s", standard, self.raw_dir)
            logger.info("Tried patterns: %s", patterns)
            logger.info("Directory contents: %s", list(self.raw_dir.glob("*.json")))

        if files:
            logger.info("Loading raw data from %d JSON files for standard: %s", len(files), standard)

            for file_path in files:
                try:
                    if not file_path.exists():
                        logger.error("File does not exist: %s", file_path)
                        continue
                    
                    file_size = file_path.stat().st_size
                    if file_size == 0:
                        logger.error("File is empty: %s", file_path)
                        continue
                    
                    logger.debug("Loading file: %s (size: %d bytes)", file_path, file_size)
                    
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_data.extend(data)
                            logger.info("Loaded %d items from %s", len(data), file_path)
                        else:
                            all_data.append(data)
                except json.JSONDecodeError as e:
                    logger.error("JSON decode error in file %s: %s", file_path, e)
                    continue
                except IOError as e:
                    logger.error("IO error loading file %s: %s", file_path, e)
                    continue

        logger.info("Total loaded %d raw compliance controls from JSON for standard: %s", len(all_data), standard)
        return all_data

    def process_standard(
        self, standard: str, version: str = "latest"
    ) -> tuple[list[ComplianceControl], list[dict[str, Any]]]:
        """Process raw compliance data for a standard (sync wrapper - deprecated).

        Use process_standard_async for LLM-based extraction.

        Args:
            standard: Compliance standard name
            version: Standard version

        Returns:
            Tuple of (processed_controls, failed_items)
        """
        import asyncio

        return asyncio.run(self.process_standard_async(standard, version))

    def standardize_control(
        self,
        raw: dict[str, Any],
        standard: str,
        version: str = "latest",
        user_id: str | None = None,
        organization_id: str | None = None,
        visibility: str = "global",
        is_custom: bool = False,
        source_document_id: str | None = None,
        source_document_name: str | None = None,
        extraction_method: str | None = None,
        extraction_confidence: float | None = None,
    ) -> ComplianceControl:
        """Convert raw control to ComplianceControl model.

        Args:
            raw: Raw compliance control dictionary
            standard: Compliance standard name
            version: Standard version (default: "latest")
            user_id: User ID for custom controls (optional)
            organization_id: Organization ID for custom controls (optional)
            visibility: Visibility scope (global, organization, user)
            is_custom: Whether this is a custom control
            source_document_id: Source document ID (optional)
            source_document_name: Source document name (optional)
            extraction_method: Extraction method (optional)
            extraction_confidence: Extraction confidence score (optional)

        Returns:
            Standardized ComplianceControl object

        Raises:
            ValidationError: If raw data cannot be standardized
        """
        # Get sequence number for fallback ID generation
        fallback_sequence = raw.get("sequence", raw.get("_index", 0))

        # Extract control_id from various possible field names
        raw_control_id = (
            raw.get("control_id")
            or raw.get("benchmark_id")
            or raw.get("article_id")
            or raw.get("requirement_id")
        )

        if is_custom and not raw_control_id:
            control_id = self._generate_custom_control_id(
                organization_id=organization_id,
                user_id=user_id,
                standard=standard,
                sequence=fallback_sequence,
            )
        else:
            # If no control_id found, use None to trigger fallback in _normalize_control_id
            control_id = self._normalize_control_id(
                str(raw_control_id) if raw_control_id else None,
                standard,
                fallback_sequence=fallback_sequence,
            )
            control_id = sanitize_control_id(control_id, max_length=100)

        title = raw.get("title") or raw.get("requirement") or "Untitled Control"
        title = sanitize_text(title, max_length=500)

        description = raw.get("description") or raw.get("content") or raw.get("guidance") or ""
        description = sanitize_text(description, max_length=10000)

        severity = self._extract_severity(raw, standard)
        category, subcategory = self._extract_categories(raw, standard)

        remediation = self._extract_remediation(raw)
        references = self._extract_references(raw)
        applies_to = self._extract_applies_to(raw, category, subcategory)

        source_value = sanitize_text(raw.get("source"), max_length=200) if raw.get("source") else None
        if is_custom:
            source_value = source_value or "user_upload" if user_id else "organization_upload"

        return ComplianceControl(
            control_id=str(control_id),
            standard=standard,
            version=version,
            title=title,
            description=description,
            requirement=raw.get("requirement") or raw.get("content"),
            testing_procedures=raw.get("testing_procedures", []) or [],
            severity=severity,
            category=category,
            subcategory=subcategory,
            applies_to=applies_to,
            remediation=remediation,
            verification=self._extract_verification(raw),
            references=references,
            source_url=sanitize_url(raw.get("source_url", "")),
            source=source_value,
            user_id=user_id,
            organization_id=organization_id,
            visibility=visibility,
            is_custom=is_custom,
            source_document_id=source_document_id,
            source_document_name=source_document_name,
            extraction_method=extraction_method,
            extraction_confidence=extraction_confidence,
            reviewed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    def _extract_severity(self, raw: dict[str, Any], standard: str = "") -> str:
        """Extract severity from raw data with intelligent inference.

        Args:
            raw: Raw control dictionary
            standard: Compliance standard name (for inference)

        Returns:
            Severity level (HIGH, MEDIUM, LOW, CRITICAL)
        """
        # Try direct extraction first
        severity = raw.get("severity") or raw.get("level") or raw.get("priority")

        if severity:
            severity_str = str(severity).upper()
            if severity_str in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                return severity_str

            severity_map = {
                "1": "CRITICAL",
                "2": "HIGH",
                "3": "MEDIUM",
                "4": "LOW",
                "5": "LOW",
            }
            mapped = severity_map.get(severity_str)
            if mapped:
                return mapped

        # Infer from control ID pattern (generic for all standards)
        control_id = str(raw.get("control_id", "")).upper()
        if control_id and standard:
            standard_upper = standard.upper()
            if control_id.startswith(f"{standard_upper}-"):
                try:
                    parts = control_id.split("-")
                    if len(parts) >= 3:
                        req_num_str = parts[2].split(".")[0]
                        req_num = int(req_num_str)
                        
                        if req_num <= 4:
                            return "CRITICAL"
                        elif req_num <= 8:
                            return "HIGH"
                        else:
                            return "MEDIUM"
                except (ValueError, IndexError):
                    pass

        # Infer from content keywords
        title = str(raw.get("title", "")).lower()
        description = str(raw.get("description", "")).lower()
        requirement = str(raw.get("requirement", "")).lower()

        critical_keywords = [
            "encrypt", "cardholder data", "authentication", "firewall", 
            "access control", "chd", "pan", "encryption", "key management"
        ]
        high_keywords = [
            "vulnerability", "patch", "security", "access", "permission",
            "malware", "antivirus", "penetration", "scan"
        ]

        combined_text = f"{title} {description} {requirement}"
        
        if any(keyword in combined_text for keyword in critical_keywords):
            return "CRITICAL"
        elif any(keyword in combined_text for keyword in high_keywords):
            return "HIGH"

        # Default fallback
        return "MEDIUM"

    def _extract_categories(self, raw: dict[str, Any], standard: str) -> tuple[str | None, str | None]:
        """Extract category and subcategory from raw data.

        Tries multiple sources and infers from control_id patterns if needed.

        Args:
            raw: Raw control dictionary
            standard: Compliance standard name

        Returns:
            Tuple of (category, subcategory)
        """
        category = raw.get("category") or raw.get("domain") or raw.get("section") or raw.get("level")
        subcategory = raw.get("subcategory") or raw.get("subdomain")

        if not category:
            category, subcategory = self._infer_categories_from_content(raw, standard)

        return (category, subcategory)

    def _infer_categories_from_content(self, raw: dict[str, Any], _standard: str) -> tuple[str | None, str | None]:
        """Infer category and subcategory from control content (generic for all standards).

        Uses content analysis rather than hardcoded standard-specific logic.

        Args:
            raw: Raw control dictionary
            _standard: Compliance standard name (unused, kept for API consistency)

        Returns:
            Tuple of (category, subcategory)
        """
        title = str(raw.get("title", "")).lower()
        description = str(raw.get("description", "")).lower()
        content = f"{title} {description}".lower()

        if "encrypt" in content or "encryption" in content or "cipher" in content:
            if "transit" in content or "transport" in content or "network" in content:
                return ("data_protection", "data-in-transit")
            elif "rest" in content or "storage" in content or "at-rest" in content:
                return ("data_protection", "data-at-rest")
            return ("data_protection", "encryption")
        
        elif "firewall" in content or "network segmentation" in content or "network security" in content:
            return ("network_security", "firewall" if "firewall" in content else None)
        
        elif "access" in content or "authentication" in content or "authorization" in content:
            if "restrict" in content or "limit" in content:
                return ("access_control", "access_restrictions")
            elif "identify" in content or "identity" in content:
                return ("access_control", "identification")
            return ("access_control", None)
        
        elif "log" in content or "monitor" in content or "audit" in content:
            if "test" in content or "scan" in content or "vulnerability" in content:
                return ("monitoring_testing", "security_testing")
            return ("monitoring_testing", "logging")
        
        elif "vulnerability" in content or "patch" in content or "antivirus" in content or "malware" in content:
            if "antivirus" in content or "malware" in content:
                return ("vulnerability_management", "antivirus")
            return ("vulnerability_management", "secure_systems")
        
        elif "policy" in content or "procedure" in content or "documentation" in content:
            return ("policy_procedures", "security_policies")
        
        elif "backup" in content or "recovery" in content or "disaster" in content:
            return ("data_protection", "backup_recovery")
        
        elif "incident" in content or "response" in content or "breach" in content:
            return ("incident_response", None)

        return (None, None)

    def _extract_remediation(self, raw: dict[str, Any]) -> Remediation:
        """Extract remediation information from raw data.

        Handles both dict format (from LLM) and string format (from other sources).

        Args:
            raw: Raw control dictionary

        Returns:
            Remediation object
        """
        remediation_data = raw.get("remediation") or raw.get("guidance") or ""
        steps = raw.get("remediation_steps", []) or []
        summary = "No remediation guidance available"

        if isinstance(remediation_data, dict):
            summary = remediation_data.get("summary", "") or ""
            if not steps:
                steps = remediation_data.get("steps", []) or []
            remediation_text = summary
        elif isinstance(remediation_data, str):
            remediation_text = remediation_data
            if remediation_text and not steps:
                steps = [step.strip() for step in remediation_text.split("\n") if step.strip()]
            summary = remediation_text[:500] if remediation_text else summary
        else:
            remediation_text = ""

        code_snippets = self._extract_code_snippets(raw)

        if not summary and steps:
            summary = " ".join(steps[:3])[:500] if steps else summary

        return Remediation(
            summary=summary,
            steps=steps[:20] if isinstance(steps, list) else [],
            code_snippets=code_snippets,
        )

    def _extract_code_snippets(self, raw: dict[str, Any]) -> list[CodeSnippet]:
        """Extract code snippets from raw data.

        Handles code snippets from both top-level and nested remediation structure.

        Args:
            raw: Raw control dictionary

        Returns:
            List of CodeSnippet objects
        """
        snippets = []

        remediation_data = raw.get("remediation")
        if isinstance(remediation_data, dict):
            remediation_snippets = remediation_data.get("code_snippets", []) or []
            if remediation_snippets:
                for snippet_data in remediation_snippets:
                    try:
                        snippet = CodeSnippet(
                            cloud_provider=snippet_data.get("cloud_provider"),
                            service=snippet_data.get("service"),
                            infrastructure_type=snippet_data.get("infrastructure_type", "terraform"),
                            code=snippet_data.get("code", ""),
                            language=snippet_data.get("language"),
                            description=snippet_data.get("description"),
                            resource_type=snippet_data.get("resource_type"),
                        )
                        snippets.append(snippet)
                    except ValidationError as e:
                        logger.warning("Invalid code snippet from remediation: %s", e)
                        continue

        if "code_snippets" in raw and isinstance(raw["code_snippets"], list):
            for snippet_data in raw["code_snippets"]:
                try:
                    snippet = CodeSnippet(
                        cloud_provider=snippet_data.get("cloud_provider"),
                        service=snippet_data.get("service"),
                        infrastructure_type=snippet_data.get("infrastructure_type", "terraform"),
                        code=snippet_data.get("code", ""),
                        language=snippet_data.get("language"),
                        description=snippet_data.get("description"),
                        resource_type=snippet_data.get("resource_type"),
                    )
                    snippets.append(snippet)
                except ValidationError as e:
                    logger.warning("Invalid code snippet: %s", e)
                    continue

        return snippets

    def _extract_references(self, raw: dict[str, Any]) -> list[Reference]:
        """Extract references from raw data.

        Args:
            raw: Raw control dictionary

        Returns:
            List of Reference objects
        """
        references = []

        if "references" in raw and isinstance(raw["references"], list):
            for ref_data in raw["references"]:
                try:
                    ref = Reference(
                        type=ref_data.get("type", "official"),
                        url=str(ref_data.get("url", "")),
                        title=ref_data.get("title", ""),
                    )
                    references.append(ref)
                except ValidationError as e:
                    logger.warning("Invalid reference: %s", e)
                    continue

        source_url = raw.get("source_url")
        if source_url and not any(r.url == source_url for r in references):
            references.append(
                Reference(
                    type="official",
                    url=str(source_url),
                    title=f"Official {raw.get('standard', '')} Documentation",
                )
            )

        return references

    def _extract_applies_to(self, raw: dict[str, Any], category: str | None = None, subcategory: str | None = None) -> list[str]:
        """Extract cloud resources this control applies to.

        Uses LLM-extracted resources if specific, otherwise infers from category/subcategory.

        Args:
            raw: Raw control dictionary
            category: Control category (for inference)
            subcategory: Control subcategory (for inference)

        Returns:
            List of cloud resource identifiers
        """
        applies_to = raw.get("applies_to", []) or []

        if isinstance(applies_to, str):
            applies_to = [applies_to]

        has_specific_resources = False
        for resource in applies_to:
            if not self.resource_mapper.is_generic(resource):
                has_specific_resources = True
                break

        if not has_specific_resources and (category or subcategory):
            inferred_resources = self.resource_mapper.infer_resources(category, subcategory)
            if inferred_resources:
                logger.debug(
                    "Inferred %d resources for category=%s, subcategory=%s",
                    len(inferred_resources),
                    category,
                    subcategory,
                )
                applies_to.extend(inferred_resources)

        if not applies_to:
            cloud = raw.get("cloud")
            if cloud:
                cloud_map = {
                    "aws": "AWS::*",
                    "gcp": "GCP::*",
                    "azure": "Azure::*",
                    "oci": "OCI::*",
                    "oracle": "OCI::*",
                }
                applies_to = [cloud_map.get(cloud.lower(), "Generic")]

        return list(dict.fromkeys(applies_to))

    def _extract_verification(self, raw: dict[str, Any]) -> dict[str, Any] | None:
        """Extract verification information from raw data.

        Args:
            raw: Raw control dictionary

        Returns:
            Verification dictionary or None
        """
        verification = raw.get("verification") or raw.get("audit")

        if verification:
            if isinstance(verification, dict):
                return verification
            elif isinstance(verification, str):
                return {"methods": [verification]}

        testing_procedures = raw.get("testing_procedures", [])
        if testing_procedures:
            return {"testing_procedures": testing_procedures}

        return None

    def _generate_custom_control_id(
        self,
        organization_id: str | None,
        user_id: str | None,
        standard: str,
        sequence: int,
    ) -> str:
        """Generate unique control ID for custom control.

        Args:
            organization_id: Organization ID (if org-level)
            user_id: User ID
            standard: Compliance standard name
            sequence: Sequence number within document

        Returns:
            Unique control ID
        """
        prefix = "custom"
        org_part = organization_id[:8] if organization_id else user_id[:8] if user_id else "unknown"
        standard_clean = standard.upper().replace("-", "_").replace(" ", "_")[:20]
        sequence_str = str(sequence).zfill(3)

        return sanitize_control_id(f"{prefix}_{org_part}_{standard_clean}_{sequence_str}", max_length=100)

    def _validate_control_id_format(self, control_id: str, standard: str) -> tuple[bool, str | None]:
        """Validate control ID follows the standardized format STANDARD-X.Y.Z.

        The standardized format is: {STANDARD}-N[.N[.N[.N]]]
        Where N is an integer (1-999).

        Args:
            control_id: Control ID to validate
            standard: Compliance standard name

        Returns:
            Tuple of (is_valid, corrected_id or None)
            - If valid: (True, None)
            - If correctable: (False, corrected_id)
            - If uncorrectable: (False, None)
        """
        import re

        if not control_id:
            return False, None

        standard_upper = standard.upper()
        control_upper = control_id.upper().strip()

        # Pattern: STANDARD-N[.N[.N[.N]]] where N is integer
        valid_pattern = rf"^{re.escape(standard_upper)}-\d+(\.\d+)*$"

        if re.match(valid_pattern, control_upper):
            return True, None

        # Attempt correction for common issues

        # 1. Strip trailing letter suffixes (e.g., PCI-DSS-3.4.1.C -> PCI-DSS-3.4.1)
        stripped = re.sub(r"\.([A-Z])$", "", control_upper)
        if re.match(valid_pattern, stripped):
            logger.debug("Corrected control ID '%s' -> '%s' (removed letter suffix)", control_id, stripped)
            return False, stripped

        # 2. Try to extract numeric portion after standard prefix
        # Handle cases like HIPAA-LS-001 or HIPAA-ACCT-02
        if control_upper.startswith(f"{standard_upper}-"):
            remainder = control_upper[len(standard_upper) + 1:]
            # Extract any numbers from the remainder
            numbers = re.findall(r"\d+", remainder)
            if numbers:
                # Convert to hierarchical format: first number as major, rest as minor
                if len(numbers) == 1:
                    corrected = f"{standard_upper}-0.0.{int(numbers[0])}"
                else:
                    corrected = f"{standard_upper}-{'.'.join(numbers)}"
                logger.debug("Corrected control ID '%s' -> '%s' (extracted numbers)", control_id, corrected)
                return False, corrected

        # 3. If just a number or number sequence, add the standard prefix
        number_only_pattern = r"^\d+(\.\d+)*$"
        if re.match(number_only_pattern, control_upper):
            corrected = f"{standard_upper}-{control_upper}"
            logger.debug("Corrected control ID '%s' -> '%s' (added prefix)", control_id, corrected)
            return False, corrected

        # Unable to correct
        return False, None

    def _normalize_control_id(self, control_id: str, standard: str, fallback_sequence: int | None = None) -> str:
        """Normalize control ID for consistency.

        Ensures control IDs follow the standardized format: STANDARD-X.Y.Z
        where X, Y, Z are integers.

        Args:
            control_id: Raw control ID
            standard: Compliance standard name
            fallback_sequence: Optional sequence number for fallback ID generation

        Returns:
            Normalized control ID in format STANDARD-X.Y.Z
        """
        if not control_id:
            if fallback_sequence is not None:
                return f"{standard.upper()}-0.0.{fallback_sequence}"
            return f"{standard.upper()}-0.0.0"

        normalized = str(control_id).strip()

        # Replace spaces with hyphens
        normalized = normalized.replace(" ", "-")

        # Ensure standard prefix is present and uppercase
        standard_upper = standard.upper()
        if not normalized.upper().startswith(standard_upper):
            if normalized.upper().startswith(standard.lower().upper()):
                normalized = standard_upper + normalized[len(standard):]
            else:
                normalized = f"{standard_upper}-{normalized}"

        normalized = normalized.upper()

        # Validate and correct the format
        is_valid, corrected = self._validate_control_id_format(normalized, standard)

        if is_valid:
            return normalized

        if corrected:
            return corrected

        # If unable to correct, generate a fallback ID
        if fallback_sequence is not None:
            fallback_id = f"{standard_upper}-0.0.{fallback_sequence}"
            logger.warning(
                "Control ID '%s' could not be normalized to standard format. Using fallback: %s",
                control_id,
                fallback_id,
            )
            return fallback_id

        # Last resort: keep the original normalized form but log a warning
        logger.warning(
            "Control ID '%s' does not follow standard format STANDARD-X.Y.Z. "
            "Consider reviewing the source data.",
            normalized,
        )
        return normalized

    def validate_control(self, control: ComplianceControl) -> bool:
        """Validate a compliance control.

        Args:
            control: ComplianceControl object to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            control.model_validate(control.model_dump())
            return True
        except ValidationError as e:
            logger.warning("Validation error for control %s: %s", control.control_id, e)
            return False

    async def process_standard_async(
        self, standard: str, version: str = "latest"
    ) -> tuple[list[ComplianceControl], list[dict[str, Any]]]:
        """Process raw compliance data for a standard (async with LLM extraction).

        Args:
            standard: Compliance standard name
            version: Standard version

        Returns:
            Tuple of (processed_controls, failed_items)
        """
        logger.info("Processing compliance standard: %s (version: %s)", standard, version)

        raw_data = await self._load_raw_data_async(standard)

        if not raw_data:
            logger.warning("No raw data found for standard: %s", standard)
            return [], []

        processed_controls = []
        failed_items = []

        for raw in raw_data:
            try:
                control = self.standardize_control(raw, standard, version)

                if not self.validate_control(control):
                    failed_items.append({"raw": raw, "error": "Validation failed"})
                    continue

                processed_controls.append(control)

            except (ValidationError, KeyError, ValueError, TypeError) as e:
                logger.warning("Error processing control: %s", e)
                failed_items.append({"raw": raw, "error": str(e)})
                continue

        failure_rate = len(failed_items) / len(raw_data) if raw_data else 0.0
        logger.info(
            "Processed %d controls, %d failed (%.1f%% failure rate) for standard: %s",
            len(processed_controls),
            len(failed_items),
            failure_rate * 100,
            standard,
        )

        if failure_rate > 0.3:
            logger.error("High processing failure rate detected: %.1f%% (threshold: 30%%) for standard: %s", 
                        failure_rate * 100, standard)

        if self.save_intermediate:
            self.save_processed(processed_controls, standard)

        return processed_controls, failed_items

    async def _load_raw_data_async(self, standard: str) -> list[dict[str, Any]]:
        """Load raw compliance data for a standard (async with LLM extraction).

        Includes JSON files and PDF processing with LLM extraction.

        Args:
            standard: Compliance standard name (e.g., "PCI-DSS", "CIS")

        Returns:
            List of raw compliance control dictionaries
        """
        all_data = []

        patterns = [
            f"{standard.lower().replace('-', '_')}*.json",
            f"{standard.lower().replace('-', '_')}-raw.json",
        ]
        
        files = []
        for pattern in patterns:
            found = list(self.raw_dir.glob(pattern))
            if found:
                files.extend(found)
                break
        
        if not files:
            logger.warning("No JSON files found for standard %s in %s", standard, self.raw_dir)
            logger.info("Tried patterns: %s", patterns)
            logger.info("Directory contents: %s", list(self.raw_dir.glob("*.json")))

        if files:
            logger.info("Loading raw data from %d JSON files for standard: %s", len(files), standard)

            for file_path in files:
                try:
                    if not file_path.exists():
                        logger.error("File does not exist: %s", file_path)
                        continue
                    
                    file_size = file_path.stat().st_size
                    if file_size == 0:
                        logger.error("File is empty: %s", file_path)
                        continue
                    
                    logger.debug("Loading file: %s (size: %d bytes)", file_path, file_size)
                    
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_data.extend(data)
                            logger.info("Loaded %d items from %s", len(data), file_path)
                        else:
                            all_data.append(data)
                except json.JSONDecodeError as e:
                    logger.error("JSON decode error in file %s: %s", file_path, e)
                    continue
                except IOError as e:
                    logger.error("IO error loading file %s: %s", file_path, e)
                    continue

        pdf_data = await self._load_pdf_data_async(standard)
        if pdf_data:
            all_data.extend(pdf_data)
            logger.info("Loaded %d controls from PDFs for standard: %s", len(pdf_data), standard)

        logger.info("Total loaded %d raw compliance controls for standard: %s", len(all_data), standard)
        return all_data

    async def _load_pdf_data_async(self, standard: str) -> list[dict[str, Any]]:
        """Load and process PDF files for a standard using Docling + LLM (async).

        Args:
            standard: Compliance standard name

        Returns:
            List of extracted compliance controls from PDFs
        """
        if not self.pdf_dir.exists():
            logger.debug("PDF directory does not exist: %s", self.pdf_dir)
            return []

        standard_lower = standard.lower().replace("-", "_").replace(" ", "_")
        standard_upper = standard.upper().replace("-", "_").replace(" ", "_")
        pdf_patterns = [
            f"*{standard_lower}*.pdf",
            f"*{standard_upper}*.pdf",
            f"*{standard.lower().replace('-', '')}*.pdf",
            f"*{standard.upper().replace('-', '')}*.pdf",
            f"*{standard.lower()}*.pdf",
            f"*{standard.upper()}*.pdf",
        ]

        pdf_files = []
        for pattern in pdf_patterns:
            found_files = list(self.pdf_dir.rglob(pattern))
            if found_files:
                pdf_files.extend(found_files)
        
        pdf_files = list(set(pdf_files))

        if not pdf_files:
            logger.debug("No PDF files found for standard: %s in %s", standard, self.pdf_dir)
            return []

        logger.info("Processing %d PDF files for standard: %s", len(pdf_files), standard)
        
        aws_specific_keywords = ["aws", "amazon", "compliance-on-aws"]
        official_keywords = ["v4", "v4_0", "requirements", "testing"]
        
        filtered_pdf_files = []
        skipped_pdf_files = []
        
        for pdf_file in pdf_files:
            filename_lower = pdf_file.name.lower()
            
            is_aws_specific = any(keyword in filename_lower for keyword in aws_specific_keywords)
            is_official = any(keyword in filename_lower for keyword in official_keywords)
            
            if is_aws_specific and not is_official:
                skipped_pdf_files.append(pdf_file)
                logger.info("Skipping AWS-specific PDF (will use official document instead): %s", pdf_file.name)
                continue
            
            filtered_pdf_files.append(pdf_file)
        
        if skipped_pdf_files:
            logger.info("Skipped %d AWS-specific PDF(s), processing %d official PDF(s)", len(skipped_pdf_files), len(filtered_pdf_files))
        
        pdf_files = filtered_pdf_files
        
        if not pdf_files:
            logger.warning("No PDF files to process after filtering for standard: %s", standard)
            return []

        all_controls = []

        for pdf_file in pdf_files:
            try:
                controls = await self.document_processor.extract_compliance_controls_from_pdf_async(
                    pdf_file, standard
                )
                all_controls.extend(controls)
                logger.info("Extracted %d controls from PDF: %s", len(controls), pdf_file.name)
            except (ValueError, TypeError, KeyError, IOError, RuntimeError) as e:
                error_msg = str(e).lower()
                is_quota_error = False
                
                try:
                    from google.api_core import exceptions as google_exceptions
                    if isinstance(e, (google_exceptions.ResourceExhausted, google_exceptions.PermissionDenied)):
                        is_quota_error = True
                except (ImportError, TypeError):
                    pass
                
                if not is_quota_error and ("quota" in error_msg or "permission" in error_msg or "rate limit" in error_msg):
                    is_quota_error = True
                
                if is_quota_error:
                    logger.error(
                        "Gemini quota/rate limit exceeded while processing PDF %s. Skipping PDF processing. "
                        "Pipeline will continue with web-collected controls. "
                        "Please increase Gemini quota to process PDFs.",
                        pdf_file.name,
                    )
                else:
                    logger.error("Error processing PDF %s: %s", pdf_file, e, exc_info=True)
                continue

        return all_controls

    def save_processed(self, controls: list[ComplianceControl], standard: str) -> None:
        """Save processed controls to JSON file.

        Args:
            controls: List of processed ComplianceControl objects
            standard: Compliance standard name
        """
        output_file = self.processed_dir / f"{standard.lower().replace('-', '_')}_processed.json"

        data = [control.model_dump(mode="json") for control in controls]

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        logger.info("Saved %d processed controls to %s", len(controls), output_file)

    def process_all_standards(self) -> dict[str, tuple[list[ComplianceControl], list[dict[str, Any]]]]:
        """Process all available compliance standards.

        Dynamically discovers standards from the raw data directory.

        Returns:
            Dictionary mapping standard names to (processed_controls, failed_items)
        """
        from ..config.compliance_urls import COMPLIANCE_URLS
        
        standards = list(COMPLIANCE_URLS.keys())

        results = {}

        for standard in standards:
            try:
                processed, failed = self.process_standard(standard)
                results[standard] = (processed, failed)
            except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
                logger.error("Error processing standard %s: %s", standard, e)
                results[standard] = ([], [{"error": str(e)}])

        return results
