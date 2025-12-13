"""AWS Cost Provider.

Fetches real AWS cost and usage data using the existing AssumeRole
infrastructure. This integrates with AWS Cost Explorer API.

Security:
- Uses the same temporary credentials from STS AssumeRole as resource discovery
- Read-only cost operations only
- No data modification

Required IAM Permissions (add to customer's discovery role):
- ce:GetCostAndUsage
- ce:GetCostForecast
- ce:GetDimensionValues
- ce:GetReservationUtilization
- ce:GetSavingsPlansUtilization
- ce:GetRightsizingRecommendation
- ce:GetAnomalies
- ce:GetAnomalyMonitors
"""

import asyncio
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from typing import Any

from wistx_mcp.tools.lib.cloud_discovery.base_provider import CloudCredentials
from wistx_mcp.tools.lib.cost_intelligence.models import (
    CostRecord,
    CostAnomaly,
    CostForecast,
    DailyForecast,
    ReservationUtilization,
    RightsizingRecommendation,
    AnomalySeverity,
)

logger = logging.getLogger(__name__)


class AWSCostProvider:
    """Fetch real AWS costs using existing AssumeRole credentials.
    
    Leverages the same AWSAssumedRoleCredentialProvider used for
    resource discovery, so no additional authentication is needed.
    """
    
    # Thread pool for running boto3 calls asynchronously
    _executor = ThreadPoolExecutor(max_workers=5)
    
    def _create_cost_explorer_client(
        self, credentials: CloudCredentials, region: str = "us-east-1"
    ) -> Any:
        """Create a boto3 Cost Explorer client from credentials.
        
        Note: Cost Explorer is only available in us-east-1 region.
        """
        import boto3
        
        creds = credentials.credentials
        session = boto3.Session(
            aws_access_key_id=creds["access_key_id"],
            aws_secret_access_key=creds["secret_access_key"],
            aws_session_token=creds["session_token"],
        )
        return session.client("ce", region_name=region)
    
    async def get_cost_and_usage(
        self,
        credentials: CloudCredentials,
        start_date: datetime,
        end_date: datetime,
        granularity: str = "DAILY",
        group_by: list[str] | None = None,
        filter_by: dict[str, Any] | None = None,
    ) -> list[CostRecord]:
        """Fetch actual cost data from AWS Cost Explorer.
        
        Args:
            credentials: Temporary AWS credentials from STS AssumeRole
            start_date: Start of billing period
            end_date: End of billing period
            granularity: DAILY, MONTHLY, or HOURLY
            group_by: Dimensions to group by (SERVICE, REGION, USAGE_TYPE, etc.)
            filter_by: Filter expression
            
        Returns:
            List of FOCUS-compliant CostRecord objects
        """
        client = self._create_cost_explorer_client(credentials)
        loop = asyncio.get_event_loop()
        
        # Default grouping
        if group_by is None:
            group_by = ["SERVICE", "REGION"]
        
        def fetch_costs():
            params: dict[str, Any] = {
                "TimePeriod": {
                    "Start": start_date.strftime("%Y-%m-%d"),
                    "End": end_date.strftime("%Y-%m-%d"),
                },
                "Granularity": granularity,
                "Metrics": ["UnblendedCost", "BlendedCost", "UsageQuantity"],
                "GroupBy": [
                    {"Type": "DIMENSION", "Key": dim} for dim in group_by
                ],
            }
            
            if filter_by:
                params["Filter"] = filter_by
            
            all_results = []
            next_token = None
            
            while True:
                if next_token:
                    params["NextPageToken"] = next_token
                
                response = client.get_cost_and_usage(**params)
                all_results.extend(response.get("ResultsByTime", []))
                
                next_token = response.get("NextPageToken")
                if not next_token:
                    break
            
            return all_results
        
        try:
            raw_results = await loop.run_in_executor(self._executor, fetch_costs)
            return self._convert_to_cost_records(raw_results)
        except Exception as e:
            logger.error("Failed to fetch AWS costs: %s", e, exc_info=True)
            raise

    def _convert_to_cost_records(
        self, raw_results: list[dict[str, Any]]
    ) -> list[CostRecord]:
        """Convert AWS Cost Explorer results to FOCUS-compliant CostRecords."""
        records = []

        for time_result in raw_results:
            period = time_result.get("TimePeriod", {})
            period_start = datetime.strptime(period.get("Start", ""), "%Y-%m-%d")
            period_end = datetime.strptime(period.get("End", ""), "%Y-%m-%d")

            for group in time_result.get("Groups", []):
                keys = group.get("Keys", [])
                metrics = group.get("Metrics", {})

                # Parse keys based on grouping
                service_name = keys[0] if len(keys) > 0 else None
                region = keys[1] if len(keys) > 1 else None

                # Get costs
                unblended = metrics.get("UnblendedCost", {})
                blended = metrics.get("BlendedCost", {})
                usage = metrics.get("UsageQuantity", {})

                records.append(CostRecord(
                    billing_account_id="",  # Will be set from connection
                    billing_period_start=period_start,
                    billing_period_end=period_end,
                    resource_id=f"{service_name}:{region}",
                    resource_name=service_name,
                    provider_name="aws",
                    service_name=service_name,
                    service_category=self._categorize_service(service_name),
                    region=region,
                    billed_cost=float(unblended.get("Amount", 0)),
                    effective_cost=float(blended.get("Amount", 0)),
                    usage_quantity=float(usage.get("Amount", 0)),
                    usage_unit=usage.get("Unit"),
                ))

        return records

    def _categorize_service(self, service_name: str | None) -> str | None:
        """Categorize AWS service into compute, storage, database, network, etc."""
        if not service_name:
            return None

        service_lower = service_name.lower()

        compute_services = [
            "ec2", "lambda", "ecs", "eks", "fargate", "batch", "lightsail"
        ]
        storage_services = [
            "s3", "ebs", "efs", "fsx", "glacier", "storage gateway"
        ]
        database_services = [
            "rds", "dynamodb", "elasticache", "redshift", "documentdb",
            "neptune", "aurora"
        ]
        network_services = [
            "vpc", "cloudfront", "route 53", "api gateway", "elb",
            "direct connect", "transit gateway"
        ]

        for s in compute_services:
            if s in service_lower:
                return "compute"
        for s in storage_services:
            if s in service_lower:
                return "storage"
        for s in database_services:
            if s in service_lower:
                return "database"
        for s in network_services:
            if s in service_lower:
                return "network"

        return "other"

    async def get_cost_forecast(
        self,
        credentials: CloudCredentials,
        forecast_days: int = 30,
    ) -> CostForecast:
        """Get AWS's native cost forecast.

        Args:
            credentials: Temporary AWS credentials
            forecast_days: Number of days to forecast (max 365)

        Returns:
            CostForecast with daily predictions and confidence intervals
        """
        client = self._create_cost_explorer_client(credentials)
        loop = asyncio.get_event_loop()

        start_date = datetime.now(timezone.utc)
        end_date = start_date + timedelta(days=min(forecast_days, 365))

        def fetch_forecast():
            response = client.get_cost_forecast(
                TimePeriod={
                    "Start": start_date.strftime("%Y-%m-%d"),
                    "End": end_date.strftime("%Y-%m-%d"),
                },
                Metric="UNBLENDED_COST",
                Granularity="DAILY",
                PredictionIntervalLevel=80,  # 80% confidence interval
            )
            return response

        try:
            raw_forecast = await loop.run_in_executor(self._executor, fetch_forecast)
            return self._convert_to_cost_forecast(raw_forecast, start_date, end_date)
        except Exception as e:
            logger.error("Failed to fetch AWS forecast: %s", e, exc_info=True)
            raise

    def _convert_to_cost_forecast(
        self,
        raw_forecast: dict[str, Any],
        start_date: datetime,
        end_date: datetime,
    ) -> CostForecast:
        """Convert AWS forecast response to CostForecast model."""
        daily_forecasts = []
        total = 0.0

        for item in raw_forecast.get("ForecastResultsByTime", []):
            period = item.get("TimePeriod", {})
            date = datetime.strptime(period.get("Start", ""), "%Y-%m-%d")

            mean_value = float(item.get("MeanValue", 0))
            total += mean_value

            # Get prediction intervals
            intervals = item.get("PredictionIntervalLowerBound", mean_value * 0.8)
            lower = float(intervals) if intervals else mean_value * 0.8

            intervals = item.get("PredictionIntervalUpperBound", mean_value * 1.2)
            upper = float(intervals) if intervals else mean_value * 1.2

            daily_forecasts.append(DailyForecast(
                date=date,
                predicted_cost=mean_value,
                lower_bound=lower,
                upper_bound=upper,
                confidence=0.8,
            ))

        # Calculate monthly bounds
        lower_sum = sum(f.lower_bound for f in daily_forecasts)
        upper_sum = sum(f.upper_bound for f in daily_forecasts)

        return CostForecast(
            forecast_id=str(uuid.uuid4()),
            generated_at=datetime.now(timezone.utc),
            forecast_start=start_date,
            forecast_end=end_date,
            daily_forecasts=daily_forecasts,
            predicted_monthly_total=total,
            confidence_level=0.8,
            lower_bound_monthly=lower_sum,
            upper_bound_monthly=upper_sum,
            source="aws_cost_explorer",
        )

    async def get_anomalies(
        self,
        credentials: CloudCredentials,
        days_back: int = 30,
    ) -> list[CostAnomaly]:
        """Get detected cost anomalies from AWS Cost Anomaly Detection.

        Args:
            credentials: Temporary AWS credentials
            days_back: Number of days to look back

        Returns:
            List of detected anomalies
        """
        client = self._create_cost_explorer_client(credentials)
        loop = asyncio.get_event_loop()

        start_date = datetime.now(timezone.utc) - timedelta(days=days_back)

        def fetch_anomalies():
            try:
                response = client.get_anomalies(
                    DateInterval={
                        "StartDate": start_date.strftime("%Y-%m-%d"),
                        "EndDate": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    },
                    MaxResults=100,
                )
                return response.get("Anomalies", [])
            except Exception as e:
                # Cost Anomaly Detection might not be enabled
                logger.warning("AWS Cost Anomaly Detection not available: %s", e)
                return []

        raw_anomalies = await loop.run_in_executor(self._executor, fetch_anomalies)
        return self._convert_to_anomalies(raw_anomalies)

    def _convert_to_anomalies(
        self, raw_anomalies: list[dict[str, Any]]
    ) -> list[CostAnomaly]:
        """Convert AWS anomalies to CostAnomaly models."""
        anomalies = []

        for raw in raw_anomalies:
            impact = raw.get("Impact", {})
            expected = float(impact.get("ExpectedSpend", 0))
            actual = float(impact.get("ActualSpend", 0))
            deviation = actual - expected
            deviation_pct = (deviation / expected * 100) if expected > 0 else 0

            # Determine severity
            if abs(deviation_pct) > 100:
                severity = AnomalySeverity.CRITICAL
            elif abs(deviation_pct) > 50:
                severity = AnomalySeverity.HIGH
            elif abs(deviation_pct) > 25:
                severity = AnomalySeverity.MEDIUM
            else:
                severity = AnomalySeverity.LOW

            root_causes = raw.get("RootCauses", [])
            root_cause_str = None
            service = None
            region = None

            if root_causes:
                first_cause = root_causes[0]
                service = first_cause.get("Service")
                region = first_cause.get("Region")
                root_cause_str = (
                    f"Primary driver: {service or 'Unknown'} "
                    f"in {region or 'Unknown region'}"
                )

            anomalies.append(CostAnomaly(
                anomaly_id=raw.get("AnomalyId", str(uuid.uuid4())),
                detected_at=datetime.fromisoformat(
                    raw.get("AnomalyStartDate", datetime.now(timezone.utc).isoformat())
                ),
                anomaly_type="spike" if deviation > 0 else "drop",
                severity=severity,
                expected_spend=expected,
                actual_spend=actual,
                deviation_amount=abs(deviation),
                deviation_percent=abs(deviation_pct),
                service_name=service,
                region=region,
                root_cause_analysis=root_cause_str,
                source="aws_anomaly_detection",
            ))

        return anomalies

    async def get_reservation_utilization(
        self,
        credentials: CloudCredentials,
        days_back: int = 30,
    ) -> ReservationUtilization:
        """Get Reserved Instance utilization data.

        Args:
            credentials: Temporary AWS credentials
            days_back: Period to analyze

        Returns:
            ReservationUtilization with usage metrics
        """
        client = self._create_cost_explorer_client(credentials)
        loop = asyncio.get_event_loop()

        start_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        end_date = datetime.now(timezone.utc)

        def fetch_utilization():
            try:
                response = client.get_reservation_utilization(
                    TimePeriod={
                        "Start": start_date.strftime("%Y-%m-%d"),
                        "End": end_date.strftime("%Y-%m-%d"),
                    },
                    Granularity="MONTHLY",
                )
                return response
            except Exception as e:
                logger.warning("Failed to get RI utilization: %s", e)
                return None

        raw_util = await loop.run_in_executor(self._executor, fetch_utilization)

        if not raw_util:
            return ReservationUtilization(
                utilization_percentage=0.0,
                coverage_percentage=0.0,
            )

        # Aggregate utilization
        total_util = raw_util.get("Total", {}).get("UtilizationPercentage", "0")

        utilization_by_time = raw_util.get("UtilizationsByTime", [])
        total_hours = 0.0
        used_hours = 0.0

        for period in utilization_by_time:
            groups = period.get("Groups", [])
            for group in groups:
                util = group.get("Utilization", {})
                total_hours += float(util.get("TotalActualHours", 0))
                used_hours += float(util.get("UsedHours", 0))

        return ReservationUtilization(
            utilization_percentage=float(total_util),
            coverage_percentage=0.0,  # Requires separate API call
            total_reserved_hours=total_hours,
            used_hours=used_hours,
            unused_hours=total_hours - used_hours,
        )

    async def get_rightsizing_recommendations(
        self,
        credentials: CloudCredentials,
        service: str = "AmazonEC2",
    ) -> list[RightsizingRecommendation]:
        """Get AWS rightsizing recommendations.

        Args:
            credentials: Temporary AWS credentials
            service: Service to get recommendations for

        Returns:
            List of rightsizing recommendations
        """
        client = self._create_cost_explorer_client(credentials)
        loop = asyncio.get_event_loop()

        def fetch_recommendations():
            try:
                response = client.get_rightsizing_recommendation(
                    Service=service,
                    Configuration={
                        "RecommendationTarget": "SAME_INSTANCE_FAMILY",
                        "BenefitsConsidered": True,
                    },
                )
                return response.get("RightsizingRecommendations", [])
            except Exception as e:
                logger.warning("Failed to get rightsizing recommendations: %s", e)
                return []

        raw_recs = await loop.run_in_executor(self._executor, fetch_recommendations)
        return self._convert_to_rightsizing(raw_recs)

    def _convert_to_rightsizing(
        self, raw_recommendations: list[dict[str, Any]]
    ) -> list[RightsizingRecommendation]:
        """Convert AWS rightsizing recommendations to our model."""
        recommendations = []

        for raw in raw_recommendations:
            current = raw.get("CurrentInstance", {})

            # Get recommended action
            modify_rec = raw.get("ModifyRecommendationDetail", {})
            target_instances = modify_rec.get("TargetInstances", [{}])
            target = target_instances[0] if target_instances else {}

            current_type = current.get("ResourceDetails", {}).get(
                "EC2ResourceDetails", {}
            ).get("InstanceType", "unknown")

            target_type = target.get("ResourceDetails", {}).get(
                "EC2ResourceDetails", {}
            ).get("InstanceType", current_type)

            current_cost = float(
                current.get("MonthlyCost", "0").replace(",", "")
            )
            target_cost = float(
                target.get("EstimatedMonthlyCost", "0").replace(",", "")
            )
            savings = current_cost - target_cost

            utilization = current.get("ResourceUtilization", {}).get(
                "EC2ResourceUtilization", {}
            )

            recommendations.append(RightsizingRecommendation(
                resource_id=current.get("ResourceId", ""),
                resource_type="EC2",
                region=current.get("ResourceDetails", {}).get(
                    "EC2ResourceDetails", {}
                ).get("Region", ""),
                current_instance_type=current_type,
                current_monthly_cost=current_cost,
                recommended_instance_type=target_type,
                recommended_monthly_cost=target_cost,
                savings_amount=savings,
                savings_percentage=(savings / current_cost * 100) if current_cost > 0 else 0,
                cpu_utilization_avg=float(
                    utilization.get("MaxCpuUtilizationPercentage", 0)
                ),
                memory_utilization_avg=float(
                    utilization.get("MaxMemoryUtilizationPercentage", 0)
                ),
            ))

        return recommendations

