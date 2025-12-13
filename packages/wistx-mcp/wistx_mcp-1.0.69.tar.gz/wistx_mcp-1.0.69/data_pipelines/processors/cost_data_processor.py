"""Cost data processor - transforms raw cost data into FOCUS-compliant models."""

from typing import Any

from pydantic import ValidationError

from ..collectors.aws_cost_collector import AWSCostCollector
from ..collectors.azure_cost_collector import AzureCostCollector
from ..collectors.gcp_cost_collector import GCPCostCollector
from ..collectors.oracle_cost_collector import OracleCostCollector
from ..collectors.alibaba_cost_collector import AlibabaCostCollector
from ..models.cost_data import FOCUSCostData
from ..validators.focus_validator import FOCUSValidator
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class CostDataProcessor:
    """Process raw cost data into FOCUS-compliant models.

    Supports provider-specific mapping and FOCUS validation.
    """

    def __init__(self):
        """Initialize cost data processor."""
        self.validator = FOCUSValidator()
        self.mappers = {
            "aws": AWSCostCollector(),
            "gcp": GCPCostCollector(),
            "azure": AzureCostCollector(),
            "oracle": OracleCostCollector(),
            "alibaba": AlibabaCostCollector(),
        }

    def process_raw_data(
        self, raw_data: dict[str, Any], provider: str
    ) -> FOCUSCostData | None:
        """Process raw cost data into FOCUS model.

        Args:
            raw_data: Raw cost data dictionary
            provider: Cloud provider name

        Returns:
            FOCUSCostData model or None if validation fails
        """
        if provider not in self.mappers:
            logger.error("Unknown provider: %s", provider)
            return None

        try:
            mapper = self.mappers[provider]
            focus_data = mapper.map_to_focus(raw_data)

            source_hash = self.validator.generate_source_hash(focus_data)
            lookup_key = self.validator.generate_lookup_key(focus_data)

            focus_data["source_hash"] = source_hash
            focus_data["lookup_key"] = lookup_key

            is_valid, errors = self.validator.validate(focus_data)
            if not is_valid:
                logger.warning(
                    "FOCUS validation failed for %s: %s",
                    lookup_key,
                    errors,
                )
                return None

            cost_record = FOCUSCostData(**focus_data)
            return cost_record

        except ValidationError as e:
            logger.error("Validation error processing cost data: %s", e)
            return None
        except Exception as e:
            logger.error("Error processing cost data: %s", e, exc_info=True)
            return None

    def process_batch(
        self, raw_data_list: list[dict[str, Any]], provider: str
    ) -> list[FOCUSCostData]:
        """Process a batch of raw cost data.

        Args:
            raw_data_list: List of raw cost data dictionaries
            provider: Cloud provider name

        Returns:
            List of FOCUSCostData models
        """
        processed = []

        for raw_data in raw_data_list:
            cost_record = self.process_raw_data(raw_data, provider)
            if cost_record:
                processed.append(cost_record)

        logger.info(
            "Processed %d/%d cost records for %s",
            len(processed),
            len(raw_data_list),
            provider,
        )

        return processed

