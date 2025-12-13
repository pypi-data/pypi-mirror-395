"""Agent improvement metrics service."""

import logging
from datetime import datetime, timedelta
from typing import Any, Optional

try:
    from scipy import stats

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    stats = None

from api.database.mongodb import mongodb_manager
from api.models.task_tracking import AgentImprovementReport, TaskComparison
from api.services.task_tracker import task_tracker

logger = logging.getLogger(__name__)


class AgentMetricsService:
    """Service for calculating agent improvement metrics."""

    async def calculate_task_success_rate(
        self,
        start_date: datetime,
        end_date: datetime,
        wistx_enabled: Optional[bool] = None,
        task_type: Optional[str] = None,
    ) -> dict[str, Any]:
        """Calculate task success rate.

        Args:
            start_date: Start date
            end_date: End date
            wistx_enabled: Filter by WISTX enabled status
            task_type: Filter by task type

        Returns:
            Dictionary with success rate metrics
        """
        tasks = await task_tracker.get_tasks(
            task_type=task_type,
            wistx_enabled=wistx_enabled,
            start_date=start_date,
            end_date=end_date,
            limit=10000,
        )

        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.get("status") == "completed")
        failed_tasks = sum(1 for t in tasks if t.get("status") == "failed")

        success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": round(success_rate, 2),
        }

    async def calculate_average_duration(
        self,
        start_date: datetime,
        end_date: datetime,
        wistx_enabled: Optional[bool] = None,
        task_type: Optional[str] = None,
    ) -> dict[str, Any]:
        """Calculate average task duration.

        Args:
            start_date: Start date
            end_date: End date
            wistx_enabled: Filter by WISTX enabled status
            task_type: Filter by task type

        Returns:
            Dictionary with duration metrics
        """
        tasks = await task_tracker.get_tasks(
            task_type=task_type,
            wistx_enabled=wistx_enabled,
            start_date=start_date,
            end_date=end_date,
            limit=10000,
        )

        durations = [
            t.get("duration_seconds")
            for t in tasks
            if t.get("duration_seconds") is not None and t.get("status") == "completed"
        ]

        if not durations:
            return {
                "average_duration": None,
                "median_duration": None,
                "min_duration": None,
                "max_duration": None,
                "sample_size": 0,
            }

        return {
            "average_duration": round(sum(durations) / len(durations), 2),
            "median_duration": round(sorted(durations)[len(durations) // 2], 2),
            "min_duration": round(min(durations), 2),
            "max_duration": round(max(durations), 2),
            "sample_size": len(durations),
        }

    async def calculate_compliance_score(
        self,
        start_date: datetime,
        end_date: datetime,
        wistx_enabled: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Calculate average compliance score.

        Args:
            start_date: Start date
            end_date: End date
            wistx_enabled: Filter by WISTX enabled status

        Returns:
            Dictionary with compliance metrics
        """
        tasks = await task_tracker.get_tasks(
            wistx_enabled=wistx_enabled,
            start_date=start_date,
            end_date=end_date,
            limit=10000,
        )

        compliance_scores = [
            t.get("metrics", {}).get("compliance_score")
            for t in tasks
            if t.get("metrics", {}).get("compliance_score") is not None
        ]

        if not compliance_scores:
            return {
                "average_score": None,
                "median_score": None,
                "sample_size": 0,
            }

        return {
            "average_score": round(sum(compliance_scores) / len(compliance_scores), 2),
            "median_score": round(sorted(compliance_scores)[len(compliance_scores) // 2], 2),
            "sample_size": len(compliance_scores),
        }

    async def calculate_cost_accuracy(
        self,
        start_date: datetime,
        end_date: datetime,
        wistx_enabled: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Calculate cost estimation accuracy.

        Args:
            start_date: Start date
            end_date: End date
            wistx_enabled: Filter by WISTX enabled status

        Returns:
            Dictionary with cost accuracy metrics
        """
        tasks = await task_tracker.get_tasks(
            wistx_enabled=wistx_enabled,
            start_date=start_date,
            end_date=end_date,
            limit=10000,
        )

        accuracies = []
        for task in tasks:
            metrics = task.get("metrics", {})
            estimated = metrics.get("estimated_cost")
            actual = metrics.get("actual_cost")

            if estimated is not None and actual is not None and actual > 0:
                error_percentage = abs(estimated - actual) / actual * 100
                accuracy = max(0, 100 - error_percentage)
                accuracies.append(accuracy)

        if not accuracies:
            return {
                "average_accuracy": None,
                "within_10_percent": None,
                "sample_size": 0,
            }

        within_10_percent = sum(1 for a in accuracies if a >= 90) / len(accuracies) * 100

        return {
            "average_accuracy": round(sum(accuracies) / len(accuracies), 2),
            "within_10_percent": round(within_10_percent, 2),
            "sample_size": len(accuracies),
        }

    async def calculate_hallucination_rate(
        self,
        start_date: datetime,
        end_date: datetime,
        wistx_enabled: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Calculate hallucination rate.

        Args:
            start_date: Start date
            end_date: End date
            wistx_enabled: Filter by WISTX enabled status

        Returns:
            Dictionary with hallucination metrics
        """
        tasks = await task_tracker.get_tasks(
            wistx_enabled=wistx_enabled,
            start_date=start_date,
            end_date=end_date,
            limit=10000,
        )

        total_tasks = len(tasks)
        hallucinations = sum(
            t.get("metrics", {}).get("hallucinations_detected", 0) for t in tasks
        )

        hallucination_rate = (hallucinations / total_tasks * 100) if total_tasks > 0 else 0.0

        return {
            "total_tasks": total_tasks,
            "total_hallucinations": hallucinations,
            "hallucination_rate": round(hallucination_rate, 2),
        }

    async def calculate_user_satisfaction(
        self,
        start_date: datetime,
        end_date: datetime,
        wistx_enabled: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Calculate user satisfaction score.

        Args:
            start_date: Start date
            end_date: End date
            wistx_enabled: Filter by WISTX enabled status

        Returns:
            Dictionary with satisfaction metrics
        """
        tasks = await task_tracker.get_tasks(
            wistx_enabled=wistx_enabled,
            start_date=start_date,
            end_date=end_date,
            limit=10000,
        )

        ratings = [
            t.get("user_feedback", {}).get("rating")
            for t in tasks
            if t.get("user_feedback", {}).get("rating") is not None
        ]

        if not ratings:
            return {
                "average_rating": None,
                "sample_size": 0,
            }

        return {
            "average_rating": round(sum(ratings) / len(ratings), 2),
            "sample_size": len(ratings),
        }

    def _calculate_improvement(
        self,
        without_value: float,
        with_value: float,
    ) -> tuple[float, float]:
        """Calculate improvement percentage and absolute value.

        Args:
            without_value: Value without WISTX
            with_value: Value with WISTX

        Returns:
            Tuple of (improvement_percentage, improvement_absolute)
        """
        if without_value == 0:
            return (0.0, 0.0)

        improvement_absolute = with_value - without_value
        improvement_percentage = (improvement_absolute / without_value) * 100

        return (improvement_percentage, improvement_absolute)

    def _calculate_statistical_significance(
        self,
        without_values: list[float],
        with_values: list[float],
    ) -> Optional[float]:
        """Calculate statistical significance (p-value) using t-test.

        Args:
            without_values: List of values without WISTX
            with_values: List of values with WISTX

        Returns:
            P-value or None if insufficient data or scipy not available
        """
        if not SCIPY_AVAILABLE:
            logger.debug("scipy not available, skipping statistical significance calculation")
            return None

        if len(without_values) < 2 or len(with_values) < 2:
            return None

        try:
            _, p_value = stats.ttest_ind(without_values, with_values)
            return float(p_value)
        except Exception as e:
            logger.warning("Failed to calculate statistical significance: %s", e)
            return None

    async def compare_with_baseline(
        self,
        start_date: datetime,
        end_date: datetime,
        task_type: Optional[str] = None,
    ) -> list[TaskComparison]:
        """Compare metrics with and without WISTX.

        Args:
            start_date: Start date
            end_date: End date
            task_type: Filter by task type

        Returns:
            List of task comparisons
        """
        comparisons: list[TaskComparison] = []

        success_without = await self.calculate_task_success_rate(
            start_date, end_date, wistx_enabled=False, task_type=task_type
        )
        success_with = await self.calculate_task_success_rate(
            start_date, end_date, wistx_enabled=True, task_type=task_type
        )

        if success_without["total_tasks"] > 0 and success_with["total_tasks"] > 0:
            without_rate = success_without["success_rate"]
            with_rate = success_with["success_rate"]
            improvement_pct, improvement_abs = self._calculate_improvement(without_rate, with_rate)

            tasks_without = await task_tracker.get_tasks(
                wistx_enabled=False,
                start_date=start_date,
                end_date=end_date,
                task_type=task_type,
                limit=10000,
            )
            tasks_with = await task_tracker.get_tasks(
                wistx_enabled=True,
                start_date=start_date,
                end_date=end_date,
                task_type=task_type,
                limit=10000,
            )

            without_successes = [
                1 if t.get("status") == "completed" else 0 for t in tasks_without
            ]
            with_successes = [1 if t.get("status") == "completed" else 0 for t in tasks_with]

            p_value = self._calculate_statistical_significance(without_successes, with_successes)

            comparisons.append(
                TaskComparison(
                    metric_name="task_success_rate",
                    without_wistx=without_rate,
                    with_wistx=with_rate,
                    improvement_percentage=improvement_pct,
                    improvement_absolute=improvement_abs,
                    statistical_significance=p_value,
                )
            )

        duration_without = await self.calculate_average_duration(
            start_date, end_date, wistx_enabled=False, task_type=task_type
        )
        duration_with = await self.calculate_average_duration(
            start_date, end_date, wistx_enabled=True, task_type=task_type
        )

        if (
            duration_without.get("average_duration") is not None
            and duration_with.get("average_duration") is not None
        ):
            without_duration = duration_without["average_duration"]
            with_duration = duration_with["average_duration"]
            improvement_pct, improvement_abs = self._calculate_improvement(without_duration, with_duration)

            tasks_without = await task_tracker.get_tasks(
                wistx_enabled=False,
                start_date=start_date,
                end_date=end_date,
                task_type=task_type,
                limit=10000,
            )
            tasks_with = await task_tracker.get_tasks(
                wistx_enabled=True,
                start_date=start_date,
                end_date=end_date,
                task_type=task_type,
                limit=10000,
            )

            without_durations = [
                t.get("duration_seconds", 0)
                for t in tasks_without
                if t.get("duration_seconds") is not None
            ]
            with_durations = [
                t.get("duration_seconds", 0)
                for t in tasks_with
                if t.get("duration_seconds") is not None
            ]

            p_value = self._calculate_statistical_significance(without_durations, with_durations)

            comparisons.append(
                TaskComparison(
                    metric_name="time_to_completion",
                    without_wistx=without_duration,
                    with_wistx=with_duration,
                    improvement_percentage=-improvement_pct,
                    improvement_absolute=-improvement_abs,
                    statistical_significance=p_value,
                )
            )

        compliance_without = await self.calculate_compliance_score(
            start_date, end_date, wistx_enabled=False
        )
        compliance_with = await self.calculate_compliance_score(
            start_date, end_date, wistx_enabled=True
        )

        if (
            compliance_without.get("average_score") is not None
            and compliance_with.get("average_score") is not None
        ):
            without_score = compliance_without["average_score"]
            with_score = compliance_with["average_score"]
            improvement_pct, improvement_abs = self._calculate_improvement(without_score, with_score)

            comparisons.append(
                TaskComparison(
                    metric_name="compliance_adherence",
                    without_wistx=without_score,
                    with_wistx=with_score,
                    improvement_percentage=improvement_pct,
                    improvement_absolute=improvement_abs,
                    statistical_significance=None,
                )
            )

        cost_without = await self.calculate_cost_accuracy(
            start_date, end_date, wistx_enabled=False
        )
        cost_with = await self.calculate_cost_accuracy(
            start_date, end_date, wistx_enabled=True
        )

        if (
            cost_without.get("average_accuracy") is not None
            and cost_with.get("average_accuracy") is not None
        ):
            without_accuracy = cost_without["average_accuracy"]
            with_accuracy = cost_with["average_accuracy"]
            improvement_pct, improvement_abs = self._calculate_improvement(
                without_accuracy, with_accuracy
            )

            comparisons.append(
                TaskComparison(
                    metric_name="cost_accuracy",
                    without_wistx=without_accuracy,
                    with_wistx=with_accuracy,
                    improvement_percentage=improvement_pct,
                    improvement_absolute=improvement_abs,
                    statistical_significance=None,
                )
            )

        hallucination_without = await self.calculate_hallucination_rate(
            start_date, end_date, wistx_enabled=False
        )
        hallucination_with = await self.calculate_hallucination_rate(
            start_date, end_date, wistx_enabled=True
        )

        if (
            hallucination_without.get("hallucination_rate") is not None
            and hallucination_with.get("hallucination_rate") is not None
        ):
            without_rate = hallucination_without["hallucination_rate"]
            with_rate = hallucination_with["hallucination_rate"]
            improvement_pct, improvement_abs = self._calculate_improvement(without_rate, with_rate)

            comparisons.append(
                TaskComparison(
                    metric_name="hallucination_rate",
                    without_wistx=without_rate,
                    with_wistx=with_rate,
                    improvement_percentage=-improvement_pct,
                    improvement_absolute=-improvement_abs,
                    statistical_significance=None,
                )
            )

        satisfaction_without = await self.calculate_user_satisfaction(
            start_date, end_date, wistx_enabled=False
        )
        satisfaction_with = await self.calculate_user_satisfaction(
            start_date, end_date, wistx_enabled=True
        )

        if (
            satisfaction_without.get("average_rating") is not None
            and satisfaction_with.get("average_rating") is not None
        ):
            without_rating = satisfaction_without["average_rating"]
            with_rating = satisfaction_with["average_rating"]
            improvement_pct, improvement_abs = self._calculate_improvement(without_rating, with_rating)

            comparisons.append(
                TaskComparison(
                    metric_name="user_satisfaction",
                    without_wistx=without_rating,
                    with_wistx=with_rating,
                    improvement_percentage=improvement_pct,
                    improvement_absolute=improvement_abs,
                    statistical_significance=None,
                )
            )

        return comparisons

    async def generate_improvement_report(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> AgentImprovementReport:
        """Generate comprehensive improvement report.

        Args:
            start_date: Report period start date
            end_date: Report period end date

        Returns:
            Agent improvement report
        """
        comparisons = await self.compare_with_baseline(start_date, end_date)

        tasks_without = await task_tracker.get_tasks(
            wistx_enabled=False, start_date=start_date, end_date=end_date, limit=10000
        )
        tasks_with = await task_tracker.get_tasks(
            wistx_enabled=True, start_date=start_date, end_date=end_date, limit=10000
        )

        overall_improvement = 0.0
        if comparisons:
            positive_improvements = [
                c.improvement_percentage
                for c in comparisons
                if c.metric_name != "hallucination_rate" and c.metric_name != "time_to_completion"
            ]
            negative_improvements = [
                abs(c.improvement_percentage)
                for c in comparisons
                if c.metric_name == "hallucination_rate" or c.metric_name == "time_to_completion"
            ]

            all_improvements = positive_improvements + negative_improvements
            if all_improvements:
                overall_improvement = sum(all_improvements) / len(all_improvements)

        task_type_breakdown: dict[str, TaskComparison] = {}
        task_types = ["compliance", "pricing", "code_generation", "best_practices"]

        for task_type in task_types:
            type_comparisons = await self.compare_with_baseline(start_date, end_date, task_type=task_type)
            if type_comparisons:
                task_type_breakdown[task_type] = type_comparisons[0]

        return AgentImprovementReport(
            period_start=start_date,
            period_end=end_date,
            sample_size_without=len(tasks_without),
            sample_size_with=len(tasks_with),
            overall_improvement=round(overall_improvement, 2),
            metrics=comparisons,
            task_type_breakdown=task_type_breakdown,
        )


agent_metrics_service = AgentMetricsService()

