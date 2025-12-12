"""Template validator for validating architecture templates before use."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class TemplateValidator:
    """Validator for architecture templates."""

    def validate_template(self, template: dict[str, Any]) -> dict[str, Any]:
        """Validate template structure and content.

        Args:
            template: Template dictionary to validate

        Returns:
            Validation results dictionary with:
            - valid: Whether template is valid
            - errors: List of error messages
            - warnings: List of warning messages
        """
        errors = []
        warnings = []

        if not isinstance(template, dict):
            errors.append("Template must be a dictionary")
            return {"valid": False, "errors": errors, "warnings": warnings}

        if "structure" not in template:
            errors.append("Template must have 'structure' field")
        else:
            structure = template.get("structure")
            if not isinstance(structure, dict):
                errors.append("Template 'structure' must be a dictionary")

        if "name" not in template:
            warnings.append("Template missing 'name' field")

        if "description" not in template:
            warnings.append("Template missing 'description' field")

        structure = template.get("structure", {})
        if structure:
            self._validate_structure(structure, errors, warnings, path="structure")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def _validate_structure(
        self,
        structure: dict[str, Any],
        errors: list[str],
        warnings: list[str],
        path: str = "",
    ) -> None:
        """Recursively validate structure.

        Args:
            structure: Structure dictionary
            errors: Errors list to append to
            warnings: Warnings list to append to
            path: Current path in structure
        """
        if not isinstance(structure, dict):
            errors.append(f"Structure at '{path}' must be a dictionary")
            return

        for key, value in structure.items():
            current_path = f"{path}.{key}" if path else key

            if isinstance(value, dict):
                if not value:
                    warnings.append(f"Empty directory at '{current_path}'")
                else:
                    self._validate_structure(value, errors, warnings, current_path)
            elif isinstance(value, str):
                if not value.strip():
                    warnings.append(f"Empty file content at '{current_path}'")
            else:
                errors.append(f"Invalid value type at '{current_path}': expected dict or str, got {type(value).__name__}")

    def validate_template_fields(self, template: dict[str, Any], required_fields: list[str]) -> dict[str, Any]:
        """Validate that template has required fields.

        Args:
            template: Template dictionary
            required_fields: List of required field names

        Returns:
            Validation results dictionary
        """
        errors = []
        warnings = []

        for field in required_fields:
            if field not in template:
                errors.append(f"Missing required field: {field}")
            elif not template[field]:
                warnings.append(f"Field '{field}' is empty")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

