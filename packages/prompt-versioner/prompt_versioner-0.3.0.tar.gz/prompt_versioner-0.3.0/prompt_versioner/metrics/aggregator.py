"""Metrics aggregation across multiple runs."""

from typing import List, Dict, Any, Optional
from prompt_versioner.metrics.models import ModelMetrics


class MetricAggregator:
    """Aggregates metrics across multiple test runs."""

    def __init__(self) -> None:
        """Initialize aggregator."""
        self.metrics: List[ModelMetrics] = []

    def add(self, metric: ModelMetrics) -> None:
        """Add a metric.

        Args:
            metric: ModelMetrics object
        """
        self.metrics.append(metric)

    def add_dict(self, **kwargs: Any) -> None:
        """Add metrics from keyword arguments.

        Args:
            **kwargs: Metric fields
        """
        self.metrics.append(ModelMetrics(**kwargs))

    def add_batch(self, metrics: List[ModelMetrics]) -> None:
        """Add multiple metrics at once.

        Args:
            metrics: List of ModelMetrics objects
        """
        self.metrics.extend(metrics)

    def get_summary(self) -> Dict[str, Any]:
        """Get statistical summary of all metrics.

        Returns:
            Dict with aggregated statistics
        """
        if not self.metrics:
            return {
                "call_count": 0,
                "has_data": False,
            }

        return {
            "call_count": len(self.metrics),
            "has_data": True,
            # Token statistics
            "total_tokens": sum(m.total_tokens or 0 for m in self.metrics),
            "avg_input_tokens": self._avg([m.input_tokens for m in self.metrics if m.input_tokens]),
            "avg_output_tokens": self._avg(
                [m.output_tokens for m in self.metrics if m.output_tokens]
            ),
            "avg_total_tokens": self._avg([m.total_tokens for m in self.metrics if m.total_tokens]),
            # Cost statistics
            "total_cost": sum(m.cost_eur or 0 for m in self.metrics),
            "avg_cost": self._avg([m.cost_eur for m in self.metrics if m.cost_eur]),
            "min_cost": min([m.cost_eur for m in self.metrics if m.cost_eur], default=0),
            "max_cost": max([m.cost_eur for m in self.metrics if m.cost_eur], default=0),
            # Latency statistics
            "avg_latency": self._avg([m.latency_ms for m in self.metrics if m.latency_ms]),
            "min_latency": min([m.latency_ms for m in self.metrics if m.latency_ms], default=0),
            "max_latency": max([m.latency_ms for m in self.metrics if m.latency_ms], default=0),
            "median_latency": self._median([m.latency_ms for m in self.metrics if m.latency_ms]),
            # Quality statistics
            "avg_quality": self._avg([m.quality_score for m in self.metrics if m.quality_score]),
            "min_quality": min(
                [m.quality_score for m in self.metrics if m.quality_score], default=0
            ),
            "max_quality": max(
                [m.quality_score for m in self.metrics if m.quality_score], default=0
            ),
            # Accuracy statistics
            "avg_accuracy": self._avg([m.accuracy for m in self.metrics if m.accuracy]),
            # Success metrics
            "success_count": sum(1 for m in self.metrics if m.success),
            "failure_count": sum(1 for m in self.metrics if not m.success),
            "success_rate": sum(1 for m in self.metrics if m.success) / len(self.metrics),
            # Model usage
            "models_used": list(set(m.model_name for m in self.metrics if m.model_name)),
            "primary_model": self._most_common(
                [m.model_name for m in self.metrics if m.model_name]
            ),
        }

    def get_summary_by_model(self) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics grouped by model.

        Returns:
            Dict of model_name -> summary stats
        """
        by_model: Dict[str, List[ModelMetrics]] = {}

        for metric in self.metrics:
            if metric.model_name:
                if metric.model_name not in by_model:
                    by_model[metric.model_name] = []
                by_model[metric.model_name].append(metric)

        result = {}
        for model_name, model_metrics in by_model.items():
            temp_aggregator = MetricAggregator()
            temp_aggregator.metrics = model_metrics
            result[model_name] = temp_aggregator.get_summary()

        return result

    def get_failures(self) -> List[ModelMetrics]:
        """Get all failed metrics.

        Returns:
            List of failed ModelMetrics
        """
        return [m for m in self.metrics if not m.success]

    def filter_by_model(self, model_name: str) -> List[ModelMetrics]:
        """Filter metrics by model name.

        Args:
            model_name: Name of model to filter by

        Returns:
            List of ModelMetrics for specified model
        """
        return [m for m in self.metrics if m.model_name == model_name]

    @staticmethod
    def _avg(values: List[Optional[float]]) -> float:
        """Calculate average of values."""
        valid_values = [v for v in values if v is not None]
        return sum(valid_values) / len(valid_values) if valid_values else 0.0

    @staticmethod
    def _median(values: List[Optional[float]]) -> float:
        """Calculate median of values."""
        valid_values = sorted([v for v in values if v is not None])
        if not valid_values:
            return 0.0
        n = len(valid_values)
        if n % 2 == 0:
            return (valid_values[n // 2 - 1] + valid_values[n // 2]) / 2
        else:
            return valid_values[n // 2]

    @staticmethod
    def _most_common(values: List[Optional[str]]) -> Optional[str]:
        """Find most common value."""
        if not values:
            return None

        from collections import Counter

        counter = Counter(values)
        most_common = counter.most_common(1)
        return most_common[0][0] if most_common else None

    def clear(self) -> None:
        """Clear all metrics."""
        self.metrics.clear()

    def to_list(self) -> List[Dict[str, Any]]:
        """Export metrics as list of dicts.

        Returns:
            List of metric dicts
        """
        return [m.to_dict() for m in self.metrics]

    def __len__(self) -> int:
        """Get number of metrics."""
        return len(self.metrics)

    def __iter__(self) -> Any:
        """Iterate over metrics."""
        return iter(self.metrics)
