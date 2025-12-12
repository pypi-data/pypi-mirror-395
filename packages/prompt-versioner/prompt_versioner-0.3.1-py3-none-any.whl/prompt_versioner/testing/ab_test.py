"""A/B testing framework for prompt versions."""

from typing import Any, List
import statistics

from prompt_versioner.testing.models import ABTestResult
from prompt_versioner.testing.formatters import format_ab_test_result


class ABTest:
    """A/B test framework for comparing prompt versions."""

    def __init__(
        self,
        versioner: Any,
        prompt_name: str,
        version_a: str,
        version_b: str,
        metric_name: str = "quality_score",
    ):
        """Initialize A/B test.

        Args:
            versioner: PromptVersioner instance
            prompt_name: Name of prompt to test
            version_a: First version (baseline)
            version_b: Second version (challenger)
            metric_name: Metric to compare
        """
        self.versioner = versioner
        self.prompt_name = prompt_name
        self.version_a = version_a
        self.version_b = version_b
        self.metric_name = metric_name

        self.results_a: List[float] = []
        self.results_b: List[float] = []

    def log_result(self, version: str, metric_value: float) -> None:
        """Log a test result.

        Args:
            version: Which version (a or b)
            metric_value: Metric value
        """
        if version == "a":
            self.results_a.append(metric_value)
        elif version == "b":
            self.results_b.append(metric_value)
        else:
            raise ValueError(f"Invalid version: {version}. Must be 'a' or 'b'")

    def log_batch_results(self, version: str, metric_values: List[float]) -> None:
        """Log multiple test results at once.

        Args:
            version: Which version (a or b)
            metric_values: List of metric values
        """
        for value in metric_values:
            self.log_result(version, value)

    def get_result(self) -> ABTestResult:
        """Get A/B test result.

        Returns:
            ABTestResult with winner and statistics
        """
        if not self.results_a or not self.results_b:
            raise ValueError("Not enough data for A/B test. Both versions need results.")

        mean_a = statistics.mean(self.results_a)
        mean_b = statistics.mean(self.results_b)

        # Determine winner
        winner = "b" if mean_b > mean_a else "a"
        improvement = abs(mean_b - mean_a) / mean_a * 100 if mean_a != 0 else 0

        # Calculate confidence (simplified - would use t-test in production)
        confidence = self._calculate_confidence()

        return ABTestResult(
            version_a=self.version_a,
            version_b=self.version_b,
            metric_name=self.metric_name,
            a_values=self.results_a,
            b_values=self.results_b,
            a_mean=mean_a,
            b_mean=mean_b,
            winner=self.version_b if winner == "b" else self.version_a,
            improvement=improvement,
            confidence=confidence,
        )

    def print_result(self) -> None:
        """Print formatted A/B test result."""

        result = self.get_result()
        output = format_ab_test_result(self.prompt_name, result)
        print(output)

    def clear_results(self) -> None:
        """Clear all logged results."""
        self.results_a.clear()
        self.results_b.clear()

    def get_sample_counts(self) -> tuple[int, int]:
        """Get number of samples for each version.

        Returns:
            Tuple of (count_a, count_b)
        """
        return len(self.results_a), len(self.results_b)

    def is_ready(self, min_samples: int = 30) -> bool:
        """Check if enough samples collected for reliable results.

        Args:
            min_samples: Minimum samples per version

        Returns:
            True if both versions have enough samples
        """
        return len(self.results_a) >= min_samples and len(self.results_b) >= min_samples

    # Private methods

    def _calculate_confidence(self) -> float:
        """Calculate confidence level (simplified).

        Returns:
            Confidence score between 0 and 1
        """
        # Simplified confidence based on sample size
        # In production, use proper statistical tests (t-test, etc.)
        min_samples = min(len(self.results_a), len(self.results_b))
        confidence = min(min_samples / 30.0, 1.0)

        # Adjust for variance
        if len(self.results_a) > 1 and len(self.results_b) > 1:
            std_a = statistics.stdev(self.results_a)
            std_b = statistics.stdev(self.results_b)
            avg_std = (std_a + std_b) / 2

            # Lower confidence if high variance
            if avg_std > 0:
                variance_penalty = 1.0 / (1.0 + avg_std)
                confidence *= variance_penalty

        return confidence
