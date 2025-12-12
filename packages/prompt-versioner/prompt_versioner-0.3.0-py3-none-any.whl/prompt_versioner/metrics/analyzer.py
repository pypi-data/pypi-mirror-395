"""Metrics analysis and comparison."""

from typing import Dict, List
from prompt_versioner.metrics.models import (
    MetricComparison,
    METRIC_DIRECTIONS,
    MetricDirection,
    MetricType,
)
from prompt_versioner.metrics.tracker import MetricsTracker


class MetricsAnalyzer:
    """Analyzes and compares metrics between versions."""

    @staticmethod
    def compare_metrics(
        baseline_metrics: Dict[str, List[float]],
        new_metrics: Dict[str, List[float]],
    ) -> List[MetricComparison]:
        """Compare metrics between two versions.

        Args:
            baseline_metrics: Metrics from baseline version
            new_metrics: Metrics from new version

        Returns:
            List of MetricComparison objects
        """
        comparisons = []

        # Find common metrics
        common_metrics = set(baseline_metrics.keys()) & set(new_metrics.keys())

        for metric_name in common_metrics:
            baseline_vals = baseline_metrics[metric_name]
            new_vals = new_metrics[metric_name]

            baseline_stats = MetricsTracker.compute_stats(baseline_vals)
            new_stats = MetricsTracker.compute_stats(new_vals)

            # Compute differences
            mean_diff = new_stats["mean"] - baseline_stats["mean"]
            mean_pct_change = (
                (mean_diff / baseline_stats["mean"] * 100) if baseline_stats["mean"] != 0 else 0.0
            )

            # Determine if improved based on metric type

            metric_type = MetricType(metric_name)
            direction = METRIC_DIRECTIONS.get(metric_type, MetricDirection.HIGHER_IS_BETTER)

            if direction == MetricDirection.HIGHER_IS_BETTER:
                improved = mean_diff > 0
            else:  # LOWER_IS_BETTER
                improved = mean_diff < 0

            comparisons.append(
                MetricComparison(
                    metric_name=metric_name,
                    baseline_mean=baseline_stats["mean"],
                    new_mean=new_stats["mean"],
                    mean_diff=mean_diff,
                    mean_pct_change=mean_pct_change,
                    improved=improved,
                    baseline_stats=baseline_stats,
                    new_stats=new_stats,
                )
            )

        return comparisons

    @staticmethod
    def format_comparison(comparisons: List[MetricComparison]) -> str:
        """Format metric comparisons as human-readable text.

        Args:
            comparisons: List of MetricComparison objects

        Returns:
            Formatted string
        """
        lines = ["=" * 80, "METRICS COMPARISON", "=" * 80]

        for comp in comparisons:
            lines.append(f"\n{comp.metric_name.upper()}:")
            lines.append(
                f"  Baseline: {comp.baseline_mean:.4f} (±{comp.baseline_stats['std_dev']:.4f})"
            )
            lines.append(f"  New:      {comp.new_mean:.4f} (±{comp.new_stats['std_dev']:.4f})")

            symbol = "↑" if comp.improved else "↓"
            status = "✓ IMPROVED" if comp.improved else "✗ REGRESSED"

            lines.append(
                f"  Change:   {symbol} {abs(comp.mean_diff):.4f} ({comp.mean_pct_change:+.2f}%) {status}"
            )

        return "\n".join(lines)

    @staticmethod
    def detect_regressions(
        comparisons: List[MetricComparison],
        threshold: float = 0.05,
    ) -> List[MetricComparison]:
        """Detect regressions in metrics.

        Args:
            comparisons: List of MetricComparison objects
            threshold: Relative threshold for regression (default 5%)

        Returns:
            List of MetricComparison objects that regressed
        """
        regressions = []

        for comp in comparisons:
            # Check if metric regressed by more than threshold
            if not comp.improved and abs(comp.mean_pct_change) > threshold * 100:
                regressions.append(comp)

        return regressions

    @staticmethod
    def get_best_version(
        versions_metrics: Dict[str, Dict[str, List[float]]],
        metric_name: str,
        higher_is_better: bool = True,
    ) -> tuple[str, float]:
        """Find the best version for a specific metric.

        Args:
            versions_metrics: Dict of version -> metrics dict
            metric_name: Name of metric to compare
            higher_is_better: Whether higher values are better

        Returns:
            Tuple of (best_version_name, best_value)
        """
        best_version = None
        best_value = None

        for version_name, metrics in versions_metrics.items():
            if metric_name not in metrics:
                continue

            values = metrics[metric_name]
            if not values:
                continue

            mean_value = sum(values) / len(values)

            if best_value is None:
                best_version = version_name
                best_value = mean_value
            else:
                if higher_is_better and mean_value > best_value:
                    best_version = version_name
                    best_value = mean_value
                elif not higher_is_better and mean_value < best_value:
                    best_version = version_name
                    best_value = mean_value

        return (best_version or "unknown", best_value or 0.0)

    @staticmethod
    def rank_versions(
        versions_metrics: Dict[str, Dict[str, List[float]]],
        metric_name: str,
        higher_is_better: bool = True,
    ) -> List[tuple[str, float]]:
        """Rank all versions by a specific metric.

        Args:
            versions_metrics: Dict of version -> metrics dict
            metric_name: Name of metric to rank by
            higher_is_better: Whether higher values are better

        Returns:
            List of (version_name, mean_value) tuples, sorted by rank
        """
        rankings = []

        for version_name, metrics in versions_metrics.items():
            if metric_name not in metrics:
                continue

            values = metrics[metric_name]
            if not values:
                continue

            mean_value = sum(values) / len(values)
            rankings.append((version_name, mean_value))

        # Sort by value
        rankings.sort(key=lambda x: x[1], reverse=higher_is_better)

        return rankings

    @staticmethod
    def calculate_improvement_score(
        comparisons: List[MetricComparison], weights: Dict[str, float] | None = None
    ) -> float:
        """Calculate overall improvement score from comparisons.

        Args:
            comparisons: List of MetricComparison objects
            weights: Optional weights for each metric (default: equal weights)

        Returns:
            Overall improvement score (-100 to +100)
        """
        if not comparisons:
            return 0.0

        if weights is None:
            # Equal weights
            weights = {comp.metric_name: 1.0 for comp in comparisons}

        total_score = 0.0
        total_weight = 0.0

        for comp in comparisons:
            weight = weights.get(comp.metric_name, 1.0)

            # Score is percentage change, capped at ±100
            score = max(-100, min(100, comp.mean_pct_change))

            total_score += score * weight
            total_weight += weight

        return total_score / total_weight if total_weight > 0 else 0.0
