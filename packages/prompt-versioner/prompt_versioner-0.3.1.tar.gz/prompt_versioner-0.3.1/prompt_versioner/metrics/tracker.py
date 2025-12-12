"""Metrics tracking and statistical analysis."""

import statistics
from typing import Dict, List, Any
from prompt_versioner.metrics.models import MetricStats


class MetricsTracker:
    """Tracks and analyzes metrics for prompt versions."""

    @staticmethod
    def compute_stats(values: List[float]) -> Dict[str, float]:
        """Compute statistical summary of metric values.

        Args:
            values: List of metric values

        Returns:
            Dict with statistical measures
        """
        if not values:
            return {
                "count": 0,
                "mean": 0.0,
                "median": 0.0,
                "std_dev": 0.0,
                "min": 0.0,
                "max": 0.0,
                "sum": 0.0,
            }

        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "min": min(values),
            "max": max(values),
            "sum": sum(values),
        }

    @staticmethod
    def compute_percentiles(
        values: List[float], percentiles: List[int] = [25, 50, 75, 90, 95, 99]
    ) -> Dict[int, float]:
        """Compute percentiles of metric values.

        Args:
            values: List of metric values
            percentiles: List of percentiles to compute

        Returns:
            Dict of percentile -> value
        """
        if not values:
            return {p: 0.0 for p in percentiles}

        sorted_values = sorted(values)
        result = {}

        for p in percentiles:
            index = int(len(sorted_values) * p / 100)
            index = min(index, len(sorted_values) - 1)
            result[p] = sorted_values[index]

        return result

    @staticmethod
    def analyze_metrics(metrics: Dict[str, List[float]]) -> List[MetricStats]:
        """Analyze metrics and return statistical summaries.

        Args:
            metrics: Dict of metric name -> list of values

        Returns:
            List of MetricStats objects
        """
        results = []

        for name, values in metrics.items():
            if not values:
                continue

            stats = MetricsTracker.compute_stats(values)
            results.append(
                MetricStats(
                    name=name,
                    count=int(stats["count"]),
                    mean=stats["mean"],
                    median=stats["median"],
                    std_dev=stats["std_dev"],
                    min_val=stats["min"],
                    max_val=stats["max"],
                )
            )

        return results

    @staticmethod
    def detect_outliers(
        values: List[float], method: str = "iqr", threshold: float = 1.5
    ) -> List[int]:
        """Detect outliers in metric values.

        Args:
            values: List of metric values
            method: Method to use ('iqr' or 'zscore')
            threshold: Threshold for outlier detection

        Returns:
            List of indices of outlier values
        """
        if len(values) < 4:
            return []

        outliers = []

        if method == "iqr":
            # Interquartile range method
            sorted_vals = sorted(values)
            q1_idx = len(sorted_vals) // 4
            q3_idx = 3 * len(sorted_vals) // 4

            q1 = sorted_vals[q1_idx]
            q3 = sorted_vals[q3_idx]
            iqr = q3 - q1

            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr

            for i, val in enumerate(values):
                if val < lower_bound or val > upper_bound:
                    outliers.append(i)

        elif method == "zscore":
            # Z-score method
            mean = statistics.mean(values)
            std_dev = statistics.stdev(values)

            for i, val in enumerate(values):
                z_score = abs((val - mean) / std_dev) if std_dev > 0 else 0
                if z_score > threshold:
                    outliers.append(i)

        return outliers

    @staticmethod
    def calculate_trend(values: List[float]) -> Dict[str, Any]:
        """Calculate trend in metric values over time.

        Args:
            values: List of metric values in chronological order

        Returns:
            Dict with trend information
        """
        if len(values) < 2:
            return {
                "trend": "insufficient_data",
                "direction": None,
                "slope": 0.0,
            }

        # Simple linear regression
        n = len(values)
        x = list(range(n))

        x_mean = sum(x) / n
        y_mean = sum(values) / n

        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0.0

        # Determine trend direction
        if abs(slope) < 0.01:
            trend = "stable"
            direction = None
        elif slope > 0:
            trend = "increasing"
            direction = "up"
        else:
            trend = "decreasing"
            direction = "down"

        return {
            "trend": trend,
            "direction": direction,
            "slope": slope,
            "start_value": values[0],
            "end_value": values[-1],
            "change": values[-1] - values[0],
            "pct_change": ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0.0,
        }
