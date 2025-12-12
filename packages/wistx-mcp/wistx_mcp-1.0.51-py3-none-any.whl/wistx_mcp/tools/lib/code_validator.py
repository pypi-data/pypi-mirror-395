"""Code validator for infrastructure code validation."""

import logging
import subprocess
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class CodeValidator:
    """Validator for infrastructure code."""

    async def validate_terraform(
        self,
        code: str,
        check_syntax: bool = True,
        check_format: bool = True,
        check_validate: bool = False,
    ) -> dict[str, Any]:
        """Validate Terraform code.

        Args:
            code: Terraform code to validate
            check_syntax: Check syntax
            check_format: Check formatting
            check_validate: Run terraform validate (requires terraform binary)

        Returns:
            Validation results dictionary with:
            - valid: Whether code is valid
            - errors: List of error messages
            - warnings: List of warning messages
        """
        errors = []
        warnings = []

        if check_syntax:
            try:
                import hcl2

                parsed = hcl2.loads(code)
                if not parsed:
                    warnings.append("Parsed code is empty")
            except ImportError:
                warnings.append("hcl2 library not available, skipping syntax check")
            except Exception as e:
                errors.append(f"Syntax error: {str(e)}")

        if check_format:
            if code.count("\n") > 0:
                lines = code.split("\n")
                for i, line in enumerate(lines, 1):
                    if line.strip() and not line.startswith("#"):
                        if line.endswith(" "):
                            warnings.append(f"Line {i}: Trailing whitespace")

        if check_validate:
            warnings.append(
                "Terraform validation via subprocess is disabled for security. "
                "Use syntax and format checking instead. "
                "For full validation, use terraform validate in your local environment."
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    async def validate_kubernetes(
        self,
        code: str,
        check_syntax: bool = True,
        check_schema: bool = False,
    ) -> dict[str, Any]:
        """Validate Kubernetes manifests.

        Args:
            code: Kubernetes YAML to validate
            check_syntax: Check YAML syntax
            check_schema: Check against Kubernetes schema (requires kubectl)

        Returns:
            Validation results dictionary with:
            - valid: Whether code is valid
            - errors: List of error messages
            - warnings: List of warning messages
        """
        errors = []
        warnings = []

        if check_syntax:
            try:
                import yaml

                documents = list(yaml.safe_load_all(code))

                if not documents:
                    errors.append("No YAML documents found")

                for i, doc in enumerate(documents):
                    if doc:
                        if "kind" not in doc:
                            errors.append(f"Document {i+1}: Missing 'kind' field")
                        if "metadata" not in doc:
                            errors.append(f"Document {i+1}: Missing 'metadata' field")
                        elif "name" not in doc.get("metadata", {}):
                            warnings.append(f"Document {i+1}: Missing 'metadata.name'")
            except ImportError:
                warnings.append("yaml library not available, skipping syntax check")
            except Exception as e:
                errors.append(f"YAML syntax error: {str(e)}")

        if check_schema:
            warnings.append(
                "Kubernetes schema validation via kubectl is disabled for security. "
                "Use syntax checking instead. "
                "For full validation, use kubectl apply --dry-run=client in your local environment."
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    async def validate_dockerfile(
        self,
        code: str,
        check_syntax: bool = True,
    ) -> dict[str, Any]:
        """Validate Dockerfile.

        Args:
            code: Dockerfile content to validate
            check_syntax: Check Dockerfile syntax

        Returns:
            Validation results dictionary
        """
        errors = []
        warnings = []

        if check_syntax:
            lines = code.split("\n")
            valid_instructions = [
                "FROM",
                "RUN",
                "CMD",
                "LABEL",
                "MAINTAINER",
                "EXPOSE",
                "ENV",
                "ADD",
                "COPY",
                "ENTRYPOINT",
                "VOLUME",
                "USER",
                "WORKDIR",
                "ARG",
                "ONBUILD",
                "STOPSIGNAL",
                "HEALTHCHECK",
                "SHELL",
            ]

            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    instruction = stripped.split()[0] if stripped.split() else ""
                    if instruction not in valid_instructions:
                        errors.append(f"Line {i}: Invalid instruction '{instruction}'")

            if not any(line.strip().startswith("FROM") for line in lines):
                errors.append("Dockerfile must start with FROM instruction")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

