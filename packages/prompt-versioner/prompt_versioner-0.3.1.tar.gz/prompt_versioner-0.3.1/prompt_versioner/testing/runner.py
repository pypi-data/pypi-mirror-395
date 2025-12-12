"""Test runner for executing prompt tests."""

from typing import Callable, Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from prompt_versioner.metrics import MetricAggregator
from prompt_versioner.testing.models import TestCase, TestResult
from prompt_versioner.testing.formatters import format_test_summary


class PromptTestRunner:
    """Test runner for prompt versions."""

    def __init__(self, max_workers: int = 4):
        """Initialize test runner.

        Args:
            max_workers: Maximum number of parallel test workers
        """
        self.max_workers = max_workers
        self.aggregator = MetricAggregator()

    def run_test(
        self,
        test_case: TestCase,
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]] = None,
    ) -> TestResult:
        """Run a single test case.

        Args:
            test_case: TestCase to run
            prompt_fn: Function that takes inputs and returns LLM output
            metric_fn: Optional function to compute metrics from output

        Returns:
            TestResult object
        """
        start_time = time.time()

        try:
            # Run the prompt function
            output = prompt_fn(test_case.inputs)

            # Validate output
            success = self._validate_output(test_case, output)

            # Compute metrics
            metrics = self._compute_metrics(output, metric_fn, start_time)

            # Aggregate metrics
            self.aggregator.add_dict(**metrics)

            return TestResult(
                test_case=test_case,
                success=success,
                output=output,
                metrics=metrics,
                duration_ms=metrics["duration_ms"],
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return TestResult(
                test_case=test_case,
                success=False,
                output=None,
                metrics={"duration_ms": duration_ms},
                error=str(e),
                duration_ms=duration_ms,
            )

    def run_tests(
        self,
        test_cases: List[TestCase],
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]] = None,
        parallel: bool = True,
    ) -> List[TestResult]:
        """Run multiple test cases.

        Args:
            test_cases: List of TestCase objects
            prompt_fn: Function that takes inputs and returns LLM output
            metric_fn: Optional function to compute metrics from output
            parallel: Whether to run tests in parallel

        Returns:
            List of TestResult objects
        """
        self.aggregator.clear()

        if parallel and len(test_cases) > 1:
            return self._run_parallel(test_cases, prompt_fn, metric_fn)
        else:
            return self._run_sequential(test_cases, prompt_fn, metric_fn)

    def get_summary(self, results: List[TestResult]) -> Dict[str, Any]:
        """Generate summary of test results.

        Args:
            results: List of TestResult objects

        Returns:
            Summary dict with statistics
        """
        total = len(results)
        passed = sum(1 for r in results if r.success)
        failed = total - passed

        # Get aggregated metrics
        stats = self.aggregator.get_summary()

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0.0,
            "metrics": stats,
        }

    def format_summary(self, summary: Dict[str, Any]) -> str:
        """Format test summary as human-readable text.

        Args:
            summary: Summary dict from get_summary

        Returns:
            Formatted string
        """
        return format_test_summary(summary)

    # Private methods

    def _validate_output(self, test_case: TestCase, output: Any) -> bool:
        """Validate test output.

        Args:
            test_case: TestCase with validation rules
            output: Output to validate

        Returns:
            True if validation passes
        """
        if test_case.validation_fn:
            return test_case.validation_fn(output)
        elif test_case.expected_output is not None:
            return output == test_case.expected_output
        return True

    def _compute_metrics(
        self, output: Any, metric_fn: Optional[Callable[[Any], Dict[str, float]]], start_time: float
    ) -> Dict[str, float]:
        """Compute metrics for test output.

        Args:
            output: Test output
            metric_fn: Optional metric computation function
            start_time: Test start time

        Returns:
            Dictionary of metrics
        """
        metrics = {}
        if metric_fn:
            metrics = metric_fn(output)

        duration_ms = (time.time() - start_time) * 1000
        metrics["duration_ms"] = duration_ms

        return metrics

    def _run_sequential(
        self,
        test_cases: List[TestCase],
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]],
    ) -> List[TestResult]:
        """Run tests sequentially."""
        results = []
        for test_case in test_cases:
            result = self.run_test(test_case, prompt_fn, metric_fn)
            results.append(result)
        return results

    def _run_parallel(
        self,
        test_cases: List[TestCase],
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]],
    ) -> List[TestResult]:
        """Run tests in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.run_test, tc, prompt_fn, metric_fn): tc for tc in test_cases
            }

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

        return results
