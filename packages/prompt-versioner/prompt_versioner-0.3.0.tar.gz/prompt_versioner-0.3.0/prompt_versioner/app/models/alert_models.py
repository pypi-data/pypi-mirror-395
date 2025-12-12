from dataclasses import dataclass
from enum import Enum


class AlertType(Enum):
    """Type of alert."""

    COST_INCREASE = "cost_increase"
    LATENCY_INCREASE = "latency_increase"
    QUALITY_DECREASE = "quality_decrease"
    ERROR_RATE_INCREASE = "error_rate_increase"


@dataclass
class Alert:
    """Performance alert."""

    alert_type: AlertType
    prompt_name: str
    current_version: str
    baseline_version: str
    metric_name: str
    baseline_value: float
    current_value: float
    change_percent: float
    threshold: float
    message: str
