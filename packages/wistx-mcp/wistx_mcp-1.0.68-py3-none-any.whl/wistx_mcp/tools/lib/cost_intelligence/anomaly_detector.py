"""Cost Anomaly Detector.

Provides intelligent anomaly detection for cloud costs using statistical
methods. Detects cost spikes, drops, and trend changes.

Industry Comparison:
- AWS Cost Anomaly Detection: Requires setup, delayed detection
- CloudZero: Dashboard-based alerts
- WISTX: Real-time detection integrated into code generation context
"""

import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Any
from statistics import mean, stdev

from wistx_mcp.tools.lib.cost_intelligence.models import (
    CostAnomaly,
    CostRecord,
    AnomalySeverity,
)

logger = logging.getLogger(__name__)


class CostAnomalyDetector:
    """Detect cost anomalies using statistical methods.
    
    Uses multiple detection strategies:
    1. Z-score based detection for sudden spikes/drops
    2. Moving average deviation for trend changes
    3. Percentage change thresholds for significant changes
    """
    
    # Thresholds for anomaly detection
    Z_SCORE_THRESHOLD = 2.5  # Standard deviations from mean
    PERCENTAGE_CHANGE_THRESHOLD = 50.0  # 50% change triggers anomaly
    MIN_DATA_POINTS = 7  # Minimum days of data for reliable detection
    
    def __init__(
        self,
        z_score_threshold: float = Z_SCORE_THRESHOLD,
        percentage_threshold: float = PERCENTAGE_CHANGE_THRESHOLD,
    ):
        """Initialize the anomaly detector.
        
        Args:
            z_score_threshold: Number of standard deviations for anomaly
            percentage_threshold: Percentage change threshold for anomaly
        """
        self.z_score_threshold = z_score_threshold
        self.percentage_threshold = percentage_threshold
    
    def detect_anomalies(
        self,
        cost_records: list[CostRecord],
        lookback_days: int = 30,
    ) -> list[CostAnomaly]:
        """Detect anomalies in cost data.
        
        Args:
            cost_records: Historical cost records
            lookback_days: Number of days to analyze
            
        Returns:
            List of detected anomalies
        """
        if len(cost_records) < self.MIN_DATA_POINTS:
            logger.debug(
                "Insufficient data for anomaly detection (%d records, need %d)",
                len(cost_records),
                self.MIN_DATA_POINTS,
            )
            return []
        
        anomalies = []
        
        # Group costs by day
        daily_costs = self._aggregate_daily_costs(cost_records)
        
        if len(daily_costs) < self.MIN_DATA_POINTS:
            return []
        
        # Detect using multiple methods
        z_score_anomalies = self._detect_z_score_anomalies(daily_costs)
        percentage_anomalies = self._detect_percentage_anomalies(daily_costs)
        trend_anomalies = self._detect_trend_anomalies(daily_costs)
        
        # Combine and deduplicate
        all_anomalies = z_score_anomalies + percentage_anomalies + trend_anomalies
        anomalies = self._deduplicate_anomalies(all_anomalies)
        
        return anomalies
    
    def _aggregate_daily_costs(
        self, cost_records: list[CostRecord]
    ) -> list[tuple[datetime, float]]:
        """Aggregate costs by day."""
        daily_totals: dict[str, float] = {}
        
        for record in cost_records:
            date_key = record.billing_period_start.strftime("%Y-%m-%d")
            daily_totals[date_key] = daily_totals.get(date_key, 0) + record.billed_cost
        
        # Sort by date
        sorted_days = sorted(daily_totals.items())
        return [
            (datetime.strptime(d, "%Y-%m-%d"), cost)
            for d, cost in sorted_days
        ]
    
    def _detect_z_score_anomalies(
        self, daily_costs: list[tuple[datetime, float]]
    ) -> list[CostAnomaly]:
        """Detect anomalies using Z-score method."""
        anomalies = []
        costs = [c for _, c in daily_costs]
        
        if len(costs) < 3:
            return []
        
        avg = mean(costs)
        std = stdev(costs) if len(costs) > 1 else 0
        
        if std == 0:
            return []
        
        for date, cost in daily_costs:
            z_score = (cost - avg) / std
            
            if abs(z_score) > self.z_score_threshold:
                severity = self._calculate_severity(abs(z_score), "z_score")
                anomaly_type = "spike" if z_score > 0 else "drop"
                
                anomalies.append(CostAnomaly(
                    anomaly_id=str(uuid.uuid4()),
                    detected_at=datetime.now(timezone.utc),
                    anomaly_type=anomaly_type,
                    severity=severity,
                    expected_spend=avg,
                    actual_spend=cost,
                    deviation_amount=abs(cost - avg),
                    deviation_percent=abs((cost - avg) / avg * 100) if avg > 0 else 0,
                    root_cause_analysis=f"Cost {anomaly_type} detected: {z_score:.1f} standard deviations from mean",
                    contributing_factors=[
                        f"Z-score: {z_score:.2f}",
                        f"Expected: ${avg:.2f}",
                        f"Actual: ${cost:.2f}",
                    ],
                    source="wistx_z_score",
                ))

        return anomalies

    def _detect_percentage_anomalies(
        self, daily_costs: list[tuple[datetime, float]]
    ) -> list[CostAnomaly]:
        """Detect anomalies based on day-over-day percentage change."""
        anomalies = []

        for i in range(1, len(daily_costs)):
            prev_date, prev_cost = daily_costs[i - 1]
            curr_date, curr_cost = daily_costs[i]

            if prev_cost == 0:
                continue

            pct_change = ((curr_cost - prev_cost) / prev_cost) * 100

            if abs(pct_change) > self.percentage_threshold:
                severity = self._calculate_severity(abs(pct_change), "percentage")
                anomaly_type = "spike" if pct_change > 0 else "drop"

                anomalies.append(CostAnomaly(
                    anomaly_id=str(uuid.uuid4()),
                    detected_at=datetime.now(timezone.utc),
                    anomaly_type=anomaly_type,
                    severity=severity,
                    expected_spend=prev_cost,
                    actual_spend=curr_cost,
                    deviation_amount=abs(curr_cost - prev_cost),
                    deviation_percent=abs(pct_change),
                    root_cause_analysis=f"Day-over-day {anomaly_type}: {pct_change:.1f}% change",
                    contributing_factors=[
                        f"Previous day: ${prev_cost:.2f}",
                        f"Current day: ${curr_cost:.2f}",
                        f"Change: {pct_change:+.1f}%",
                    ],
                    source="wistx_percentage",
                ))

        return anomalies

    def _detect_trend_anomalies(
        self, daily_costs: list[tuple[datetime, float]]
    ) -> list[CostAnomaly]:
        """Detect trend changes using moving average comparison."""
        anomalies = []

        if len(daily_costs) < 14:  # Need at least 2 weeks
            return []

        # Calculate 7-day moving averages
        costs = [c for _, c in daily_costs]

        # Start from day 14 to ensure we have two full 7-day windows
        for i in range(14, len(costs)):
            recent_avg = mean(costs[i-7:i])
            older_avg = mean(costs[i-14:i-7])

            if older_avg == 0:
                continue

            trend_change = ((recent_avg - older_avg) / older_avg) * 100

            # Only flag significant trend changes (>30%)
            if abs(trend_change) > 30:
                date = daily_costs[i][0]
                severity = self._calculate_severity(abs(trend_change), "trend")
                anomaly_type = "trend_change"

                anomalies.append(CostAnomaly(
                    anomaly_id=str(uuid.uuid4()),
                    detected_at=datetime.now(timezone.utc),
                    anomaly_type=anomaly_type,
                    severity=severity,
                    expected_spend=older_avg,
                    actual_spend=recent_avg,
                    deviation_amount=abs(recent_avg - older_avg),
                    deviation_percent=abs(trend_change),
                    root_cause_analysis=f"Cost trend change: {trend_change:+.1f}% over 7 days",
                    contributing_factors=[
                        f"Previous 7-day avg: ${older_avg:.2f}",
                        f"Recent 7-day avg: ${recent_avg:.2f}",
                        f"Trend: {'increasing' if trend_change > 0 else 'decreasing'}",
                    ],
                    source="wistx_trend",
                ))

        return anomalies

    def _calculate_severity(
        self, value: float, detection_type: str
    ) -> AnomalySeverity:
        """Calculate anomaly severity based on detection type and value."""
        if detection_type == "z_score":
            if value > 4.0:
                return AnomalySeverity.CRITICAL
            elif value > 3.5:
                return AnomalySeverity.HIGH
            elif value > 3.0:
                return AnomalySeverity.MEDIUM
            else:
                return AnomalySeverity.LOW

        elif detection_type == "percentage":
            if value > 200:
                return AnomalySeverity.CRITICAL
            elif value > 100:
                return AnomalySeverity.HIGH
            elif value > 75:
                return AnomalySeverity.MEDIUM
            else:
                return AnomalySeverity.LOW

        elif detection_type == "trend":
            if value > 100:
                return AnomalySeverity.HIGH
            elif value > 50:
                return AnomalySeverity.MEDIUM
            else:
                return AnomalySeverity.LOW

        return AnomalySeverity.LOW

    def _deduplicate_anomalies(
        self, anomalies: list[CostAnomaly]
    ) -> list[CostAnomaly]:
        """Remove duplicate anomalies detected by multiple methods."""
        # Keep the highest severity anomaly for each date
        by_date: dict[str, CostAnomaly] = {}
        severity_order = {
            AnomalySeverity.CRITICAL: 4,
            AnomalySeverity.HIGH: 3,
            AnomalySeverity.MEDIUM: 2,
            AnomalySeverity.LOW: 1,
        }

        for anomaly in anomalies:
            date_key = anomaly.detected_at.strftime("%Y-%m-%d")

            if date_key not in by_date:
                by_date[date_key] = anomaly
            else:
                existing = by_date[date_key]
                if severity_order[anomaly.severity] > severity_order[existing.severity]:
                    by_date[date_key] = anomaly

        return list(by_date.values())

    async def get_anomaly_risk_level(
        self, recent_anomalies: list[CostAnomaly]
    ) -> str:
        """Calculate overall anomaly risk level.

        Args:
            recent_anomalies: List of recent anomalies

        Returns:
            Risk level: "low", "medium", "high"
        """
        if not recent_anomalies:
            return "low"

        # Count by severity
        critical_count = sum(
            1 for a in recent_anomalies if a.severity == AnomalySeverity.CRITICAL
        )
        high_count = sum(
            1 for a in recent_anomalies if a.severity == AnomalySeverity.HIGH
        )

        if critical_count > 0:
            return "high"
        elif high_count >= 2:
            return "high"
        elif high_count >= 1 or len(recent_anomalies) >= 3:
            return "medium"
        else:
            return "low"
