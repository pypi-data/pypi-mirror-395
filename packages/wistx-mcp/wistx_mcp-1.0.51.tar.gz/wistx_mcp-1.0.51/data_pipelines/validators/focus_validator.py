"""FOCUS compliance validator."""

import hashlib
from datetime import datetime
from decimal import Decimal
from typing import Any

from data_pipelines.models.cost_data import FOCUSCostData
from data_pipelines.utils.logger import setup_logger

logger = setup_logger(__name__)


class FOCUSValidationError(Exception):
    """Raised when FOCUS validation fails."""

    pass


class FOCUSValidator:
    """Validates cost data against FOCUS specification.

    Reference: https://focus.finops.org/
    """

    REQUIRED_COLUMNS = {
        "billing_account_id",
        "billing_account_name",
        "billing_currency",
        "billing_period_start",
        "billing_period_end",
        "provider",
        "invoice_issuer",
        "region_id",
        "region_name",
        "resource_id",
        "resource_name",
        "resource_type",
        "service_category",
        "service_name",
        "sku_id",
        "sku_description",
        "sku_price_id",
        "pricing_category",
        "pricing_quantity",
        "pricing_unit",
        "list_cost",
        "list_unit_price",
        "effective_cost",
        "billed_cost",
        "consumed_quantity",
        "consumed_unit",
        "charge_category",
        "charge_description",
        "charge_frequency",
        "charge_period_start",
        "charge_period_end",
    }

    VALID_CURRENCIES = {
        "USD",
        "EUR",
        "GBP",
        "JPY",
        "CNY",
        "AUD",
        "CAD",
        "CHF",
        "INR",
        "BRL",
    }

    VALID_CHARGE_CATEGORIES = {"Usage", "Tax", "Discount", "Credit", "Refund"}

    VALID_PRICING_CATEGORIES = {"OnDemand", "Reserved", "Spot", "Committed", "SavingsPlan"}

    VALID_SERVICE_CATEGORIES = {
        "Compute",
        "Storage",
        "Network",
        "Database",
        "Analytics",
        "Security",
        "Management",
        "Integration",
    }

    def validate(self, data: dict[str, Any] | FOCUSCostData) -> tuple[bool, list[str]]:
        """Validate data against FOCUS specification.

        Args:
            data: Cost data dictionary or FOCUSCostData model

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if isinstance(data, FOCUSCostData):
            data_dict = data.model_dump()
        else:
            data_dict = data

        errors.extend(self._validate_required_columns(data_dict))
        errors.extend(self._validate_data_types(data_dict))
        errors.extend(self._validate_enumerated_values(data_dict))
        errors.extend(self._validate_date_formats(data_dict))
        errors.extend(self._validate_currency_codes(data_dict))
        errors.extend(self._validate_decimal_precision(data_dict))

        return len(errors) == 0, errors

    def _validate_required_columns(self, data: dict[str, Any]) -> list[str]:
        """Validate all required columns are present.

        Args:
            data: Data dictionary

        Returns:
            List of error messages
        """
        errors = []
        missing = self.REQUIRED_COLUMNS - set(data.keys())

        if missing:
            errors.append(f"Missing required columns: {', '.join(sorted(missing))}")

        return errors

    def _validate_data_types(self, data: dict[str, Any]) -> list[str]:
        """Validate data types match FOCUS spec.

        Args:
            data: Data dictionary

        Returns:
            List of error messages
        """
        errors = []

        if "billing_period_start" in data and not isinstance(data["billing_period_start"], (datetime, str)):
            errors.append("billing_period_start must be datetime or ISO 8601 string")

        if "billing_period_end" in data and not isinstance(data["billing_period_end"], (datetime, str)):
            errors.append("billing_period_end must be datetime or ISO 8601 string")

        if "list_cost" in data and not isinstance(data["list_cost"], (Decimal, float, int)):
            errors.append("list_cost must be Decimal, float, or int")

        if "list_unit_price" in data and not isinstance(data["list_unit_price"], (Decimal, float, int)):
            errors.append("list_unit_price must be Decimal, float, or int")

        return errors

    def _validate_enumerated_values(self, data: dict[str, Any]) -> list[str]:
        """Validate enumerated values are valid.

        Args:
            data: Data dictionary

        Returns:
            List of error messages
        """
        errors = []

        if "charge_category" in data:
            if data["charge_category"] not in self.VALID_CHARGE_CATEGORIES:
                errors.append(
                    f"charge_category must be one of {self.VALID_CHARGE_CATEGORIES}, "
                    f"got {data['charge_category']}"
                )

        if "pricing_category" in data:
            if data["pricing_category"] not in self.VALID_PRICING_CATEGORIES:
                errors.append(
                    f"pricing_category must be one of {self.VALID_PRICING_CATEGORIES}, "
                    f"got {data['pricing_category']}"
                )

        if "service_category" in data:
            if data["service_category"] not in self.VALID_SERVICE_CATEGORIES:
                errors.append(
                    f"service_category must be one of {self.VALID_SERVICE_CATEGORIES}, "
                    f"got {data['service_category']}"
                )

        return errors

    def _validate_date_formats(self, data: dict[str, Any]) -> list[str]:
        """Validate date formats are ISO 8601 compliant.

        Args:
            data: Data dictionary

        Returns:
            List of error messages
        """
        errors = []
        date_fields = [
            "billing_period_start",
            "billing_period_end",
            "charge_period_start",
            "charge_period_end",
        ]

        for field in date_fields:
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    try:
                        datetime.fromisoformat(value.replace("Z", "+00:00"))
                    except (ValueError, AttributeError):
                        errors.append(f"{field} must be ISO 8601 format, got {value}")

        return errors

    def _validate_currency_codes(self, data: dict[str, Any]) -> list[str]:
        """Validate currency codes are ISO 4217 compliant.

        Args:
            data: Data dictionary

        Returns:
            List of error messages
        """
        errors = []

        if "billing_currency" in data:
            currency = data["billing_currency"]
            if currency not in self.VALID_CURRENCIES:
                errors.append(
                    f"billing_currency must be valid ISO 4217 code, "
                    f"got {currency}. Valid: {self.VALID_CURRENCIES}"
                )

        return errors

    def _validate_decimal_precision(self, data: dict[str, Any]) -> list[str]:
        """Validate decimal precision is appropriate.

        Args:
            data: Data dictionary

        Returns:
            List of error messages
        """
        errors = []

        cost_fields = ["list_cost", "list_unit_price", "effective_cost", "billed_cost"]

        for field in cost_fields:
            if field in data:
                value = data[field]
                if isinstance(value, (float, Decimal)):
                    if value < 0:
                        errors.append(f"{field} cannot be negative, got {value}")

        return errors

    def generate_source_hash(self, data: dict[str, Any]) -> str:
        """Generate source hash for change detection.

        Args:
            data: Cost data dictionary

        Returns:
            SHA256 hash string
        """
        hash_fields = [
            "provider",
            "sku_id",
            "region_id",
            "pricing_category",
            "list_unit_price",
            "billing_period_start",
        ]

        hash_string = "|".join(str(data.get(field, "")) for field in hash_fields)
        return hashlib.sha256(hash_string.encode()).hexdigest()

    def generate_lookup_key(self, data: dict[str, Any]) -> str:
        """Generate unique lookup key for deduplication.

        Args:
            data: Cost data dictionary

        Returns:
            Lookup key string
        """
        key_fields = [
            data.get("provider", ""),
            data.get("sku_id", ""),
            data.get("region_id", ""),
            data.get("pricing_category", ""),
            str(data.get("billing_period_start", "")),
        ]

        return "_".join(str(field) for field in key_fields)

