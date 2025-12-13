"""Cost Forecaster.

Provides intelligent cost forecasting with confidence intervals.
Uses multiple forecasting methods and combines them for better accuracy.

Industry Comparison:
- AWS Cost Explorer: Basic linear forecasting
- CloudZero: ML-based but dashboard-only
- WISTX: Real-time forecasting integrated into code generation context
"""

import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any
from statistics import mean, stdev

from wistx_mcp.tools.lib.cost_intelligence.models import (
    CostForecast,
    DailyForecast,
    CostRecord,
)

logger = logging.getLogger(__name__)


class CostForecaster:
    """Forecast future costs using statistical methods.
    
    Uses multiple forecasting approaches:
    1. Simple moving average for stable costs
    2. Exponential smoothing for trending costs
    3. Linear regression for growth patterns
    
    Combines forecasts with confidence intervals.
    """
    
    # Configuration
    MIN_DATA_POINTS = 14  # Minimum days for reliable forecasting
    DEFAULT_FORECAST_DAYS = 30
    CONFIDENCE_LEVEL = 0.80  # 80% confidence interval
    
    def __init__(
        self,
        smoothing_factor: float = 0.3,
        confidence_level: float = CONFIDENCE_LEVEL,
    ):
        """Initialize the forecaster.
        
        Args:
            smoothing_factor: Alpha for exponential smoothing (0-1)
            confidence_level: Confidence level for intervals (0-1)
        """
        self.smoothing_factor = smoothing_factor
        self.confidence_level = confidence_level
    
    def forecast(
        self,
        cost_records: list[CostRecord],
        forecast_days: int = DEFAULT_FORECAST_DAYS,
        planned_changes: list[dict[str, Any]] | None = None,
    ) -> CostForecast:
        """Generate cost forecast with confidence intervals.
        
        Args:
            cost_records: Historical cost records
            forecast_days: Number of days to forecast
            planned_changes: List of planned infrastructure changes
            
        Returns:
            CostForecast with daily predictions and confidence intervals
        """
        now = datetime.now(timezone.utc)
        
        # Aggregate to daily costs
        daily_costs = self._aggregate_daily_costs(cost_records)
        
        if len(daily_costs) < self.MIN_DATA_POINTS:
            logger.warning(
                "Insufficient data for forecasting (%d days, need %d)",
                len(daily_costs),
                self.MIN_DATA_POINTS,
            )
            # Return a basic forecast based on average
            return self._create_basic_forecast(daily_costs, forecast_days, now)
        
        # Generate forecasts using multiple methods
        ma_forecast = self._moving_average_forecast(daily_costs, forecast_days)
        es_forecast = self._exponential_smoothing_forecast(daily_costs, forecast_days)
        lr_forecast = self._linear_regression_forecast(daily_costs, forecast_days)
        
        # Combine forecasts (ensemble)
        combined = self._combine_forecasts(
            [ma_forecast, es_forecast, lr_forecast],
            weights=[0.3, 0.4, 0.3],  # Weight ES slightly higher
        )
        
        # Calculate confidence intervals
        historical_std = stdev([c for _, c in daily_costs]) if len(daily_costs) > 1 else 0
        daily_forecasts = self._create_daily_forecasts(
            combined, now, historical_std
        )
        
        # Calculate totals
        total_predicted = sum(f.predicted_cost for f in daily_forecasts)
        lower_total = sum(f.lower_bound for f in daily_forecasts)
        upper_total = sum(f.upper_bound for f in daily_forecasts)
        
        # Account for planned changes
        planned_impact = 0.0
        if planned_changes:
            planned_impact = self._calculate_planned_impact(planned_changes)
        
        return CostForecast(
            forecast_id=str(uuid.uuid4()),
            generated_at=now,
            forecast_start=now,
            forecast_end=now + timedelta(days=forecast_days),
            daily_forecasts=daily_forecasts,
            predicted_monthly_total=total_predicted,
            confidence_level=self.confidence_level,
            lower_bound_monthly=lower_total,
            upper_bound_monthly=upper_total,
            planned_changes_impact=planned_impact,
            forecast_with_changes=total_predicted + planned_impact if planned_impact else None,
            source="wistx_ensemble",
        )
    
    def _aggregate_daily_costs(
        self, cost_records: list[CostRecord]
    ) -> list[tuple[datetime, float]]:
        """Aggregate costs by day."""
        daily_totals: dict[str, float] = {}
        
        for record in cost_records:
            date_key = record.billing_period_start.strftime("%Y-%m-%d")
            daily_totals[date_key] = daily_totals.get(date_key, 0) + record.billed_cost
        
        sorted_days = sorted(daily_totals.items())
        return [
            (datetime.strptime(d, "%Y-%m-%d"), cost)
            for d, cost in sorted_days
        ]
    
    def _create_basic_forecast(
        self,
        daily_costs: list[tuple[datetime, float]],
        forecast_days: int,
        start_date: datetime,
    ) -> CostForecast:
        """Create a basic forecast when insufficient data."""
        if not daily_costs:
            avg_cost = 0.0
        else:
            avg_cost = mean([c for _, c in daily_costs])
        
        daily_forecasts = []
        for i in range(forecast_days):
            date = start_date + timedelta(days=i + 1)
            daily_forecasts.append(DailyForecast(
                date=date,
                predicted_cost=avg_cost,
                lower_bound=avg_cost * 0.7,
                upper_bound=avg_cost * 1.3,
                confidence=0.5,  # Low confidence due to insufficient data
            ))
        
        total = avg_cost * forecast_days
        
        return CostForecast(
            forecast_id=str(uuid.uuid4()),
            generated_at=start_date,
            forecast_start=start_date,
            forecast_end=start_date + timedelta(days=forecast_days),
            daily_forecasts=daily_forecasts,
            predicted_monthly_total=total,
            confidence_level=0.5,
            lower_bound_monthly=total * 0.7,
            upper_bound_monthly=total * 1.3,
            source="wistx_basic",
        )

    def _moving_average_forecast(
        self,
        daily_costs: list[tuple[datetime, float]],
        forecast_days: int,
        window: int = 7,
    ) -> list[float]:
        """Forecast using simple moving average."""
        costs = [c for _, c in daily_costs]

        # Calculate moving average of last 'window' days
        if len(costs) >= window:
            ma = mean(costs[-window:])
        else:
            ma = mean(costs)

        # Simple MA forecast is constant
        return [ma] * forecast_days

    def _exponential_smoothing_forecast(
        self,
        daily_costs: list[tuple[datetime, float]],
        forecast_days: int,
    ) -> list[float]:
        """Forecast using exponential smoothing (Holt's method)."""
        costs = [c for _, c in daily_costs]
        alpha = self.smoothing_factor

        # Initialize
        level = costs[0]
        trend = (costs[-1] - costs[0]) / len(costs) if len(costs) > 1 else 0

        # Apply exponential smoothing
        for cost in costs[1:]:
            prev_level = level
            level = alpha * cost + (1 - alpha) * (level + trend)
            trend = alpha * (level - prev_level) + (1 - alpha) * trend

        # Generate forecast
        forecast = []
        for i in range(forecast_days):
            forecast.append(max(0, level + (i + 1) * trend))

        return forecast

    def _linear_regression_forecast(
        self,
        daily_costs: list[tuple[datetime, float]],
        forecast_days: int,
    ) -> list[float]:
        """Forecast using simple linear regression."""
        costs = [c for _, c in daily_costs]
        n = len(costs)

        # Calculate slope and intercept
        x_mean = (n - 1) / 2
        y_mean = mean(costs)

        numerator = sum((i - x_mean) * (costs[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator

        intercept = y_mean - slope * x_mean

        # Generate forecast
        forecast = []
        for i in range(forecast_days):
            predicted = intercept + slope * (n + i)
            forecast.append(max(0, predicted))

        return forecast

    def _combine_forecasts(
        self,
        forecasts: list[list[float]],
        weights: list[float],
    ) -> list[float]:
        """Combine multiple forecasts using weighted average."""
        if not forecasts:
            return []

        forecast_days = len(forecasts[0])
        combined = []

        for i in range(forecast_days):
            weighted_sum = sum(
                f[i] * w for f, w in zip(forecasts, weights)
            )
            combined.append(weighted_sum)

        return combined

    def _create_daily_forecasts(
        self,
        predictions: list[float],
        start_date: datetime,
        historical_std: float,
    ) -> list[DailyForecast]:
        """Create DailyForecast objects with confidence intervals."""
        daily_forecasts = []

        # Z-score for 80% confidence interval
        z_score = 1.28  # 80% CI

        for i, predicted in enumerate(predictions):
            date = start_date + timedelta(days=i + 1)

            # Widen confidence interval as we forecast further
            uncertainty_factor = 1 + (i * 0.02)  # 2% wider per day
            margin = z_score * historical_std * uncertainty_factor

            daily_forecasts.append(DailyForecast(
                date=date,
                predicted_cost=predicted,
                lower_bound=max(0, predicted - margin),
                upper_bound=predicted + margin,
                confidence=self.confidence_level / uncertainty_factor,
            ))

        return daily_forecasts

    def _calculate_planned_impact(
        self, planned_changes: list[dict[str, Any]]
    ) -> float:
        """Calculate cost impact of planned infrastructure changes."""
        total_impact = 0.0

        for change in planned_changes:
            change_type = change.get("type", "add")
            monthly_cost = change.get("monthly_cost", 0)

            if change_type == "add":
                total_impact += monthly_cost
            elif change_type == "remove":
                total_impact -= monthly_cost
            elif change_type == "modify":
                old_cost = change.get("old_monthly_cost", 0)
                total_impact += monthly_cost - old_cost

        return total_impact

    def forecast_budget_exceedance(
        self,
        forecast: CostForecast,
        budget_amount: float,
        current_spent: float,
    ) -> dict[str, Any]:
        """Predict when budget will be exceeded.

        Args:
            forecast: Cost forecast
            budget_amount: Total budget amount
            current_spent: Amount already spent

        Returns:
            Dictionary with exceedance prediction
        """
        remaining = budget_amount - current_spent
        cumulative = 0.0

        for daily in forecast.daily_forecasts:
            cumulative += daily.predicted_cost

            if cumulative > remaining:
                days_until = (daily.date - forecast.generated_at).days
                return {
                    "will_exceed": True,
                    "exceedance_date": daily.date,
                    "days_until_exceeded": days_until,
                    "predicted_overage": cumulative - remaining,
                    "confidence": daily.confidence,
                }

        return {
            "will_exceed": False,
            "exceedance_date": None,
            "days_until_exceeded": None,
            "predicted_remaining": remaining - cumulative,
            "confidence": self.confidence_level,
        }
