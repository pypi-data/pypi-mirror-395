"""Data models for metrics."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum


@dataclass
class ModelMetrics:
    """Metrics for a single LLM call."""

    # Model info
    model_name: Optional[str] = None

    # Token usage
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    # Cost
    cost_eur: Optional[float] = None

    # Performance
    latency_ms: Optional[float] = None

    # Quality metrics
    quality_score: Optional[float] = None
    accuracy: Optional[float] = None

    # Model parameters
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None

    # Status
    success: bool = True
    error_message: Optional[str] = None

    # Additional data
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "model_name": self.model_name,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cost_eur": self.cost_eur,
            "latency_ms": self.latency_ms,
            "quality_score": self.quality_score,
            "accuracy": self.accuracy,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "success": self.success,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelMetrics":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class MetricStats:
    """Statistical summary of a metric."""

    name: str
    count: int
    mean: float
    median: float
    std_dev: float
    min_val: float
    max_val: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "count": self.count,
            "mean": self.mean,
            "median": self.median,
            "std_dev": self.std_dev,
            "min": self.min_val,
            "max": self.max_val,
        }

    def format(self) -> str:
        """Format as human-readable string."""
        return (
            f"{self.name}: "
            f"mean={self.mean:.4f}, "
            f"median={self.median:.4f}, "
            f"std={self.std_dev:.4f}, "
            f"range=[{self.min_val:.4f}, {self.max_val:.4f}], "
            f"n={self.count}"
        )


@dataclass
class MetricComparison:
    """Comparison between two metric sets."""

    metric_name: str
    baseline_mean: float
    new_mean: float
    mean_diff: float
    mean_pct_change: float
    improved: bool
    baseline_stats: Dict[str, float]
    new_stats: Dict[str, float]

    def format(self) -> str:
        """Format as human-readable string."""
        symbol = "↑" if self.improved else "↓"
        return (
            f"{self.metric_name}: "
            f"{self.baseline_mean:.4f} → {self.new_mean:.4f} "
            f"({symbol} {abs(self.mean_pct_change):.2f}%)"
        )


class MetricType(str, Enum):
    """Common metric types for LLM prompts."""

    # Token metrics
    INPUT_TOKENS = "input_tokens"
    OUTPUT_TOKENS = "output_tokens"
    TOTAL_TOKENS = "total_tokens"

    # Cost metrics
    COST = "cost_eur"
    COST_PER_TOKEN = "cost_per_token"  # nosec: B105

    # Performance metrics
    LATENCY = "latency_ms"
    THROUGHPUT = "throughput"

    # Quality metrics
    QUALITY = "quality_score"
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    COHERENCE = "coherence"
    FACTUALITY = "factuality"
    FLUENCY = "fluency"

    # Success metrics
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"


class MetricDirection(str, Enum):
    """Direction for metric optimization."""

    HIGHER_IS_BETTER = "higher"
    LOWER_IS_BETTER = "lower"
    NEUTRAL = "neutral"


# Mapping of metric types to optimization direction
METRIC_DIRECTIONS = {
    MetricType.COST: MetricDirection.LOWER_IS_BETTER,
    MetricType.COST_PER_TOKEN: MetricDirection.LOWER_IS_BETTER,
    MetricType.LATENCY: MetricDirection.LOWER_IS_BETTER,
    MetricType.ERROR_RATE: MetricDirection.LOWER_IS_BETTER,
    MetricType.QUALITY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.ACCURACY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.RELEVANCE: MetricDirection.HIGHER_IS_BETTER,
    MetricType.COHERENCE: MetricDirection.HIGHER_IS_BETTER,
    MetricType.FACTUALITY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.FLUENCY: MetricDirection.HIGHER_IS_BETTER,
    MetricType.THROUGHPUT: MetricDirection.HIGHER_IS_BETTER,
    MetricType.SUCCESS_RATE: MetricDirection.HIGHER_IS_BETTER,
}


@dataclass
class MetricThreshold:
    """Threshold configuration for a metric."""

    metric_type: MetricType
    warning_threshold: float
    critical_threshold: float
    direction: MetricDirection = MetricDirection.HIGHER_IS_BETTER

    def check(self, value: float) -> str:
        """Check if value meets thresholds.

        Returns:
            'ok', 'warning', or 'critical'
        """
        if self.direction == MetricDirection.HIGHER_IS_BETTER:
            if value < self.critical_threshold:
                return "critical"
            elif value < self.warning_threshold:
                return "warning"
            else:
                return "ok"
        else:  # LOWER_IS_BETTER
            if value > self.critical_threshold:
                return "critical"
            elif value > self.warning_threshold:
                return "warning"
            else:
                return "ok"
