"""Performance monitoring and alerting."""

from typing import Dict, List, Optional, Callable, Any
from prompt_versioner.app.models import Alert, AlertType
import logging


class PerformanceMonitor:
    """Monitor prompt performance and trigger alerts."""

    def __init__(self, versioner: Any):
        """Initialize monitor.

        Args:
            versioner: PromptVersioner instance
        """
        self.versioner = versioner
        self.alert_handlers = []  # type: List[Callable[[Alert], None]]

    def add_alert_handler(self, handler: Callable[[Alert], None]) -> None:
        """Add alert handler function.

        Args:
            handler: Function that receives Alert objects
        """
        self.alert_handlers.append(handler)

    def check_regression(
        self,
        name: str,
        current_version: str,
        baseline_version: Optional[str] = None,
        thresholds: Optional[Dict[str, float]] = None,
    ) -> List[Alert]:
        """Check for performance regressions.

        Args:
            name: Prompt name
            current_version: Current version to check
            baseline_version: Baseline version (uses previous if None)
            thresholds: Dict of metric -> threshold (e.g., {"cost": 0.20} for 20%)

        Returns:
            List of triggered alerts
        """
        thresholds = thresholds or {
            "cost": 0.20,  # 20% cost increase
            "latency": 0.30,  # 30% latency increase
            "quality": -0.10,  # 10% quality decrease
            "error_rate": 0.05,  # 5% error rate increase
        }

        current_v = self.versioner.get_version(name, current_version)
        if not current_v:
            return []

        # Get baseline version
        if baseline_version is None:
            versions = self.versioner.list_versions(name)
            if len(versions) < 2:
                return []  # No baseline to compare
            baseline_version = versions[1]["version"]  # Previous version

        baseline_v = self.versioner.get_version(name, baseline_version)
        if not baseline_v:
            return []

        current_metrics = self.versioner.storage.get_metrics_summary(current_v["id"])
        baseline_metrics = self.versioner.storage.get_metrics_summary(baseline_v["id"])

        if not current_metrics or not baseline_metrics:
            return []

        alerts = []

        # Check cost increase
        if "cost" in thresholds:
            baseline_cost = baseline_metrics.get("avg_cost", 0)
            current_cost = current_metrics.get("avg_cost", 0)

            if baseline_cost and baseline_cost > 0:
                change = (current_cost - baseline_cost) / baseline_cost

                if change > thresholds["cost"]:
                    alerts.append(
                        Alert(
                            alert_type=AlertType.COST_INCREASE,
                            prompt_name=name,
                            current_version=current_version,
                            baseline_version=baseline_version,
                            metric_name="avg_cost",
                            baseline_value=baseline_cost,
                            current_value=current_cost,
                            change_percent=change * 100,
                            threshold=thresholds["cost"] * 100,
                            message=f"Cost increased by {change*100:.1f}% (threshold: {thresholds['cost']*100:.0f}%)",
                        )
                    )

        # Check latency increase
        if "latency" in thresholds:
            baseline_latency = baseline_metrics.get("avg_latency", 0)
            current_latency = current_metrics.get("avg_latency", 0)

            if baseline_latency and baseline_latency > 0:
                change = (current_latency - baseline_latency) / baseline_latency

                if change > thresholds["latency"]:
                    alerts.append(
                        Alert(
                            alert_type=AlertType.LATENCY_INCREASE,
                            prompt_name=name,
                            current_version=current_version,
                            baseline_version=baseline_version,
                            metric_name="avg_latency",
                            baseline_value=baseline_latency,
                            current_value=current_latency,
                            change_percent=change * 100,
                            threshold=thresholds["latency"] * 100,
                            message=f"Latency increased by {change*100:.1f}% (threshold: {thresholds['latency']*100:.0f}%)",
                        )
                    )

        # Check quality decrease
        if "quality" in thresholds:
            baseline_quality = baseline_metrics.get("avg_quality", 0)
            current_quality = current_metrics.get("avg_quality", 0)

            if baseline_quality and baseline_quality > 0:
                change = (current_quality - baseline_quality) / baseline_quality

                if change < thresholds["quality"]:  # Negative threshold for decrease
                    alerts.append(
                        Alert(
                            alert_type=AlertType.QUALITY_DECREASE,
                            prompt_name=name,
                            current_version=current_version,
                            baseline_version=baseline_version,
                            metric_name="avg_quality",
                            baseline_value=baseline_quality,
                            current_value=current_quality,
                            change_percent=change * 100,
                            threshold=thresholds["quality"] * 100,
                            message=f"Quality decreased by {abs(change)*100:.1f}% (threshold: {abs(thresholds['quality'])*100:.0f}%)",
                        )
                    )

        # Check error rate increase
        if "error_rate" in thresholds:
            baseline_error_rate = 1 - baseline_metrics.get("success_rate", 1)
            current_error_rate = 1 - current_metrics.get("success_rate", 1)

            if current_error_rate - baseline_error_rate > thresholds["error_rate"]:
                alerts.append(
                    Alert(
                        alert_type=AlertType.ERROR_RATE_INCREASE,
                        prompt_name=name,
                        current_version=current_version,
                        baseline_version=baseline_version,
                        metric_name="error_rate",
                        baseline_value=baseline_error_rate,
                        current_value=current_error_rate,
                        change_percent=(current_error_rate - baseline_error_rate) * 100,
                        threshold=thresholds["error_rate"] * 100,
                        message=f"Error rate increased by {(current_error_rate - baseline_error_rate)*100:.1f}% (threshold: {thresholds['error_rate']*100:.0f}%)",
                    )
                )

        # Trigger alert handlers
        for alert in alerts:
            for handler in self.alert_handlers:
                try:
                    handler(alert)
                except Exception as e:
                    logging.warning(f"Alert handler failed: {e}")

        return alerts
