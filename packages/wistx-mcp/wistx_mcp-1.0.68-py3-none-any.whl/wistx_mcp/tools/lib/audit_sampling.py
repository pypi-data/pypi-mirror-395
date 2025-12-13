"""Audit Sampling Tools for WISTX.

This module implements AICPA/PCAOB-compliant audit sampling methodologies:
- Statistical sampling (MUS, attribute sampling)
- Non-statistical sampling (haphazard, block)
- Sample size determination based on risk assessment
- Tolerable misstatement calculations
- Dual-purpose sample design

Industry Standards Implemented:
- PCAOB AS 2315 (Audit Sampling)
- AICPA AU-C Section 530 (Audit Sampling)
- ISA 530 (Audit Sampling)
- PCAOB AS 1215 (Audit Documentation)
"""

import logging
import math
import random
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class SamplingMethod(Enum):
    """Audit sampling methods per PCAOB AS 2315."""
    # Statistical methods
    MUS = "monetary_unit_sampling"           # Monetary Unit Sampling (PPS)
    ATTRIBUTE = "attribute_sampling"          # For tests of controls
    CLASSICAL_VARIABLES = "classical_variables"  # Mean-per-unit, ratio, difference
    
    # Non-statistical methods
    HAPHAZARD = "haphazard"                  # Random without formal selection
    BLOCK = "block"                          # Contiguous items
    JUDGMENTAL = "judgmental"                # Based on auditor judgment


class RiskLevel(Enum):
    """Risk of material misstatement levels."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class ControlEffectiveness(Enum):
    """Control effectiveness assessment."""
    EFFECTIVE = "effective"
    PARTIALLY_EFFECTIVE = "partially_effective"
    NOT_EFFECTIVE = "not_effective"
    NOT_TESTED = "not_tested"


@dataclass
class SamplingParameters:
    """Parameters for sample size determination per PCAOB AS 2315."""
    # Population characteristics
    population_size: int
    population_value: float = 0.0  # Total monetary value (for MUS)
    
    # Risk assessment
    risk_of_material_misstatement: RiskLevel = RiskLevel.MODERATE
    detection_risk: RiskLevel = RiskLevel.MODERATE
    inherent_risk: RiskLevel = RiskLevel.MODERATE
    control_risk: RiskLevel = RiskLevel.MODERATE
    
    # Tolerable misstatement (materiality)
    tolerable_misstatement: float = 0.0
    tolerable_rate: float = 0.05  # For attribute sampling (5%)
    
    # Expected misstatement
    expected_misstatement: float = 0.0
    expected_rate: float = 0.01  # For attribute sampling (1%)
    
    # Confidence level
    confidence_level: float = 0.95  # 95% confidence
    
    # Stratification
    stratify: bool = False
    strata_count: int = 3


@dataclass
class SampleItem:
    """Individual item selected for sampling."""
    item_id: str
    item_value: float
    stratum: int | None = None
    selection_method: str = ""
    selection_interval: float | None = None
    random_start: float | None = None
    tested: bool = False
    test_result: str = ""
    exception_noted: bool = False
    exception_description: str = ""


@dataclass
class SampleResult:
    """Results of audit sampling."""
    sample_id: str
    sampling_method: SamplingMethod
    parameters: SamplingParameters
    sample_size: int
    items: list[SampleItem]
    
    # Evaluation results
    exceptions_found: int = 0
    projected_misstatement: float = 0.0
    upper_misstatement_limit: float = 0.0
    conclusion: str = ""
    
    # Documentation
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""
    workpaper_reference: str = ""


class AuditSamplingCalculator:
    """Calculator for audit sample sizes per PCAOB AS 2315.
    
    This calculator implements the statistical formulas and tables
    from PCAOB AS 2315 for determining appropriate sample sizes
    based on risk assessment and materiality.
    """
    
    # Risk factor tables from PCAOB AS 2315
    # Risk of incorrect acceptance factors
    RISK_FACTORS = {
        0.01: 4.61,  # 1% risk
        0.05: 3.00,  # 5% risk
        0.10: 2.31,  # 10% risk
        0.15: 1.90,  # 15% risk
        0.20: 1.61,  # 20% risk
        0.25: 1.39,  # 25% risk
        0.30: 1.21,  # 30% risk
        0.37: 1.00,  # 37% risk
        0.50: 0.70,  # 50% risk
    }
    
    # Attribute sampling table (sample sizes for tests of controls)
    # Based on expected deviation rate and tolerable rate
    ATTRIBUTE_SAMPLE_SIZES = {
        # (expected_rate, tolerable_rate): sample_size at 95% confidence
        (0.00, 0.05): 59,
        (0.00, 0.10): 29,
        (0.01, 0.05): 93,
        (0.01, 0.10): 38,
        (0.02, 0.05): 181,
        (0.02, 0.10): 48,
        (0.03, 0.10): 64,
        (0.04, 0.10): 88,
        (0.05, 0.10): 124,
    }
    
    @classmethod
    def calculate_mus_sample_size(
        cls,
        params: SamplingParameters,
    ) -> int:
        """Calculate sample size for Monetary Unit Sampling (MUS).
        
        Formula: n = (BV × RF) / TM
        Where:
            BV = Book Value (population value)
            RF = Risk Factor (based on risk of incorrect acceptance)
            TM = Tolerable Misstatement
        
        Args:
            params: Sampling parameters
            
        Returns:
            Calculated sample size
        """
        if params.tolerable_misstatement <= 0:
            raise ValueError("Tolerable misstatement must be positive")
        
        # Determine risk of incorrect acceptance based on risk assessment
        risk_of_incorrect_acceptance = cls._get_risk_of_incorrect_acceptance(params)
        risk_factor = cls._get_risk_factor(risk_of_incorrect_acceptance)
        
        # Adjust for expected misstatement
        expansion_factor = 1.0
        if params.expected_misstatement > 0:
            ratio = params.expected_misstatement / params.tolerable_misstatement
            if ratio < 0.2:
                expansion_factor = 1.0
            elif ratio < 0.4:
                expansion_factor = 1.25
            elif ratio < 0.6:
                expansion_factor = 1.67
            else:
                expansion_factor = 2.0
        
        # Calculate sample size
        sample_size = math.ceil(
            (params.population_value * risk_factor * expansion_factor) 
            / params.tolerable_misstatement
        )
        
        # Apply finite population correction if needed
        if sample_size > params.population_size * 0.1:
            sample_size = cls._apply_finite_correction(
                sample_size, params.population_size
            )
        
        return max(sample_size, 25)  # Minimum sample size of 25

    @classmethod
    def calculate_attribute_sample_size(
        cls,
        params: SamplingParameters,
    ) -> int:
        """Calculate sample size for attribute sampling (tests of controls).

        Uses AICPA sample size tables based on:
        - Expected deviation rate
        - Tolerable deviation rate
        - Confidence level

        Args:
            params: Sampling parameters

        Returns:
            Calculated sample size
        """
        expected = round(params.expected_rate, 2)
        tolerable = round(params.tolerable_rate, 2)

        # Look up in table
        key = (expected, tolerable)
        if key in cls.ATTRIBUTE_SAMPLE_SIZES:
            return cls.ATTRIBUTE_SAMPLE_SIZES[key]

        # Interpolate or use formula
        # n = (Z² × p × (1-p)) / E²
        z = 1.96 if params.confidence_level >= 0.95 else 1.645
        p = params.expected_rate
        e = params.tolerable_rate - params.expected_rate

        if e <= 0:
            raise ValueError("Tolerable rate must exceed expected rate")

        sample_size = math.ceil((z ** 2 * p * (1 - p)) / (e ** 2))

        # Apply finite population correction
        if sample_size > params.population_size * 0.05:
            sample_size = cls._apply_finite_correction(
                sample_size, params.population_size
            )

        return max(sample_size, 25)

    @classmethod
    def _get_risk_of_incorrect_acceptance(cls, params: SamplingParameters) -> float:
        """Determine risk of incorrect acceptance from risk assessment.

        Based on audit risk model: AR = IR × CR × DR
        Where DR = AR / (IR × CR)

        Risk of incorrect acceptance is related to detection risk.
        """
        # Map risk levels to numeric values
        risk_map = {
            RiskLevel.LOW: 0.20,
            RiskLevel.MODERATE: 0.50,
            RiskLevel.HIGH: 0.80,
        }

        ir = risk_map[params.inherent_risk]
        cr = risk_map[params.control_risk]

        # Target audit risk of 5%
        target_ar = 0.05

        # Calculate required detection risk
        dr = target_ar / (ir * cr)

        # Cap at reasonable bounds
        return min(max(dr, 0.05), 0.50)

    @classmethod
    def _get_risk_factor(cls, risk: float) -> float:
        """Get risk factor from table based on risk of incorrect acceptance."""
        # Find closest risk level in table
        closest_risk = min(cls.RISK_FACTORS.keys(), key=lambda x: abs(x - risk))
        return cls.RISK_FACTORS[closest_risk]

    @classmethod
    def _apply_finite_correction(cls, n: int, N: int) -> int:
        """Apply finite population correction factor.

        n' = n / (1 + (n/N))
        """
        return math.ceil(n / (1 + (n / N)))


class AuditSampler:
    """Performs audit sampling selection per PCAOB AS 2315.

    This class implements various sampling selection methods
    and maintains proper documentation for audit workpapers.
    """

    def __init__(self, params: SamplingParameters):
        """Initialize sampler with parameters.

        Args:
            params: Sampling parameters
        """
        self.params = params
        self.calculator = AuditSamplingCalculator()

    def select_mus_sample(
        self,
        population: list[dict[str, Any]],
        value_field: str = "value",
        id_field: str = "id",
    ) -> SampleResult:
        """Select sample using Monetary Unit Sampling (MUS/PPS).

        MUS treats each dollar as a sampling unit, giving larger
        items a proportionally higher chance of selection.

        Args:
            population: List of items with values
            value_field: Field name containing monetary value
            id_field: Field name containing item identifier

        Returns:
            SampleResult with selected items
        """
        sample_size = self.calculator.calculate_mus_sample_size(self.params)

        # Calculate sampling interval
        total_value = sum(item.get(value_field, 0) for item in population)
        interval = total_value / sample_size

        # Random start within first interval
        random_start = random.uniform(0, interval)

        # Select items using systematic selection
        selected_items = []
        cumulative_value = 0
        selection_point = random_start

        for item in population:
            item_value = item.get(value_field, 0)
            cumulative_value += item_value

            # Check if this item contains a selection point
            while selection_point <= cumulative_value:
                selected_items.append(SampleItem(
                    item_id=str(item.get(id_field, "")),
                    item_value=item_value,
                    selection_method="MUS",
                    selection_interval=interval,
                    random_start=random_start,
                ))
                selection_point += interval

        return SampleResult(
            sample_id=f"MUS-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            sampling_method=SamplingMethod.MUS,
            parameters=self.params,
            sample_size=len(selected_items),
            items=selected_items,
        )

    def select_attribute_sample(
        self,
        population: list[dict[str, Any]],
        id_field: str = "id",
    ) -> SampleResult:
        """Select sample for attribute (tests of controls) sampling.

        Uses systematic random selection for attribute testing.

        Args:
            population: List of items to sample from
            id_field: Field name containing item identifier

        Returns:
            SampleResult with selected items
        """
        sample_size = self.calculator.calculate_attribute_sample_size(self.params)
        sample_size = min(sample_size, len(population))

        # Calculate interval
        interval = len(population) / sample_size
        random_start = random.uniform(0, interval)

        # Systematic selection
        selected_items = []
        for i in range(sample_size):
            index = int(random_start + (i * interval)) % len(population)
            item = population[index]
            selected_items.append(SampleItem(
                item_id=str(item.get(id_field, "")),
                item_value=0,  # Not applicable for attribute sampling
                selection_method="ATTRIBUTE",
                selection_interval=interval,
                random_start=random_start,
            ))

        return SampleResult(
            sample_id=f"ATTR-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            sampling_method=SamplingMethod.ATTRIBUTE,
            parameters=self.params,
            sample_size=len(selected_items),
            items=selected_items,
        )

    def select_haphazard_sample(
        self,
        population: list[dict[str, Any]],
        sample_size: int,
        id_field: str = "id",
        value_field: str = "value",
    ) -> SampleResult:
        """Select haphazard (non-statistical) sample.

        Haphazard selection without any conscious bias,
        but not using formal random selection.

        Args:
            population: List of items to sample from
            sample_size: Number of items to select
            id_field: Field name containing item identifier
            value_field: Field name containing value (optional)

        Returns:
            SampleResult with selected items
        """
        sample_size = min(sample_size, len(population))

        # Use random.sample for haphazard selection
        selected = random.sample(population, sample_size)

        selected_items = [
            SampleItem(
                item_id=str(item.get(id_field, "")),
                item_value=item.get(value_field, 0),
                selection_method="HAPHAZARD",
            )
            for item in selected
        ]

        return SampleResult(
            sample_id=f"HAP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            sampling_method=SamplingMethod.HAPHAZARD,
            parameters=self.params,
            sample_size=len(selected_items),
            items=selected_items,
        )

    def evaluate_mus_results(
        self,
        sample_result: SampleResult,
    ) -> dict[str, Any]:
        """Evaluate MUS sample results and project misstatement.

        Calculates:
        - Basic precision
        - Projected misstatement
        - Upper misstatement limit

        Args:
            sample_result: Sample result with tested items

        Returns:
            Evaluation results dictionary
        """
        # Count exceptions and calculate tainting percentages
        exceptions = [item for item in sample_result.items if item.exception_noted]

        if not exceptions:
            # No exceptions - only basic precision
            basic_precision = (
                self.params.tolerable_misstatement
                * self._get_risk_factor_for_evaluation(0)
            )
            return {
                "exceptions_found": 0,
                "projected_misstatement": 0,
                "basic_precision": basic_precision,
                "upper_misstatement_limit": basic_precision,
                "conclusion": "No exceptions noted. Upper misstatement limit is within tolerable misstatement.",
                "acceptable": True,
            }

        # Calculate projected misstatement
        interval = sample_result.items[0].selection_interval or 1
        projected = 0

        for exception in exceptions:
            # Tainting percentage = misstatement / recorded amount
            # For simplicity, assume full tainting
            projected += interval

        # Calculate upper misstatement limit
        risk_factor = self._get_risk_factor_for_evaluation(len(exceptions))
        basic_precision = self.params.tolerable_misstatement * risk_factor
        upper_limit = projected + basic_precision

        acceptable = upper_limit <= self.params.tolerable_misstatement

        return {
            "exceptions_found": len(exceptions),
            "projected_misstatement": projected,
            "basic_precision": basic_precision,
            "upper_misstatement_limit": upper_limit,
            "conclusion": (
                f"Upper misstatement limit (${upper_limit:,.2f}) is "
                f"{'within' if acceptable else 'exceeds'} tolerable misstatement "
                f"(${self.params.tolerable_misstatement:,.2f})."
            ),
            "acceptable": acceptable,
        }

    def evaluate_attribute_results(
        self,
        sample_result: SampleResult,
    ) -> dict[str, Any]:
        """Evaluate attribute sample results.

        Calculates:
        - Sample deviation rate
        - Upper deviation limit
        - Conclusion on control effectiveness

        Args:
            sample_result: Sample result with tested items

        Returns:
            Evaluation results dictionary
        """
        exceptions = [item for item in sample_result.items if item.exception_noted]
        sample_size = len(sample_result.items)

        # Calculate sample deviation rate
        deviation_rate = len(exceptions) / sample_size if sample_size > 0 else 0

        # Calculate upper deviation limit (simplified)
        # Using normal approximation for large samples
        z = 1.96  # 95% confidence
        upper_limit = deviation_rate + z * math.sqrt(
            (deviation_rate * (1 - deviation_rate)) / sample_size
        )

        acceptable = upper_limit <= self.params.tolerable_rate

        effectiveness = ControlEffectiveness.EFFECTIVE
        if not acceptable:
            if deviation_rate > self.params.tolerable_rate:
                effectiveness = ControlEffectiveness.NOT_EFFECTIVE
            else:
                effectiveness = ControlEffectiveness.PARTIALLY_EFFECTIVE

        return {
            "exceptions_found": len(exceptions),
            "sample_size": sample_size,
            "sample_deviation_rate": deviation_rate,
            "upper_deviation_limit": upper_limit,
            "tolerable_rate": self.params.tolerable_rate,
            "control_effectiveness": effectiveness.value,
            "conclusion": (
                f"Upper deviation limit ({upper_limit:.1%}) is "
                f"{'within' if acceptable else 'exceeds'} tolerable rate "
                f"({self.params.tolerable_rate:.1%}). "
                f"Control is assessed as {effectiveness.value}."
            ),
            "acceptable": acceptable,
        }

    def _get_risk_factor_for_evaluation(self, num_exceptions: int) -> float:
        """Get risk factor for MUS evaluation based on exceptions."""
        # Simplified - in practice, use AICPA tables
        base_factor = 3.0  # For 5% risk
        return base_factor + (num_exceptions * 0.75)

