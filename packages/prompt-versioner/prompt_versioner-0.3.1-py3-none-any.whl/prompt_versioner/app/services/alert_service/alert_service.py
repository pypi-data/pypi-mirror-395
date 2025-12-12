"""Service for handling performance alerts."""

from typing import Any, Dict, List, Optional
from prompt_versioner.app.services.alert_service.monitoring import PerformanceMonitor

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertService:
    """Service for performance monitoring and alerts."""

    def __init__(self, versioner: Any, config: Any):
        """Initialize service.

        Args:
            versioner: PromptVersioner instance
            config: Configuration object
        """
        self.versioner = versioner
        self.config = config

    def get_all_alerts(self, thresholds: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        """Get all performance alerts across all prompts.

        Args:
            thresholds: Custom alert thresholds

        Returns:
            List of alert dictionaries
        """
        if thresholds is None:
            thresholds = self.config["DEFAULT_ALERT_THRESHOLDS"]

        all_alerts = []
        prompts = self.versioner.list_prompts()
        monitor = PerformanceMonitor(self.versioner)

        for prompt_name in prompts:
            try:
                versions = self.versioner.list_versions(prompt_name)
                if len(versions) < 2:
                    continue

                latest = versions[0]
                previous = versions[1]

                alerts = monitor.check_regression(
                    name=prompt_name,
                    current_version=latest["version"],
                    baseline_version=previous["version"],
                    thresholds=thresholds,
                )

                for alert in alerts:
                    all_alerts.append(
                        {
                            "prompt_name": prompt_name,
                            "type": alert.alert_type.value,
                            "message": alert.message,
                            "metric_name": alert.metric_name,
                            "baseline_value": alert.baseline_value,
                            "current_value": alert.current_value,
                            "change_percent": alert.change_percent,
                            "threshold": alert.threshold,
                            "current_version": alert.current_version,
                            "baseline_version": alert.baseline_version,
                        }
                    )
            except Exception as e:
                logging.warning(f"Error checking alerts for prompt '{prompt_name}': {e}")
                continue

        return all_alerts

    def get_prompt_alerts(
        self, name: str, thresholds: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """Get alerts for a specific prompt.

        Args:
            name: Prompt name
            thresholds: Custom alert thresholds

        Returns:
            List of alert dictionaries
        """
        if thresholds is None:
            thresholds = self.config["DEFAULT_ALERT_THRESHOLDS"]

        versions = self.versioner.list_versions(name)
        if len(versions) < 2:
            return []

        monitor = PerformanceMonitor(self.versioner)

        latest = versions[0]
        previous = versions[1]

        alerts = monitor.check_regression(
            name=name,
            current_version=latest["version"],
            baseline_version=previous["version"],
            thresholds=thresholds,
        )

        alerts_data = []
        for alert in alerts:
            alerts_data.append(
                {
                    "type": alert.alert_type.value,
                    "message": alert.message,
                    "metric_name": alert.metric_name,
                    "baseline_value": alert.baseline_value,
                    "current_value": alert.current_value,
                    "change_percent": alert.change_percent,
                    "threshold": alert.threshold,
                    "current_version": alert.current_version,
                    "baseline_version": alert.baseline_version,
                }
            )

        return alerts_data
