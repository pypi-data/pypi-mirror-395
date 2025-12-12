"""Output formatting for test results."""

from typing import Dict, Any
from prompt_versioner.testing.models import ABTestResult


def format_test_summary(summary: Dict[str, Any]) -> str:
    """Format test summary as human-readable text.

    Args:
        summary: Summary dict from PromptTestRunner.get_summary

    Returns:
        Formatted string
    """
    lines = ["=" * 80, "TEST SUMMARY", "=" * 80]

    lines.append(f"\nTests Run: {summary['total']}")
    lines.append(f"Passed:    {summary['passed']} ({summary['pass_rate']:.1%})")
    lines.append(f"Failed:    {summary['failed']}")

    if summary["metrics"]:
        lines.append("\nMETRICS:")
        for name, stats in summary["metrics"].items():
            lines.append(f"\n  {name}:")
            lines.append(f"    Mean:   {stats['mean']:.4f}")
            lines.append(f"    Median: {stats['median']:.4f}")
            lines.append(f"    Std:    {stats['std_dev']:.4f}")
            lines.append(f"    Range:  [{stats['min']:.4f}, {stats['max']:.4f}]")

    lines.append("\n" + "=" * 80)
    return "\n".join(lines)


def format_ab_test_result(prompt_name: str, result: ABTestResult) -> str:
    """Format A/B test result.

    Args:
        prompt_name: Name of the prompt
        result: ABTestResult object

    Returns:
        Formatted string
    """
    lines = [
        "=" * 60,
        f"A/B Test Results: {prompt_name}",
        "=" * 60,
        f"Metric: {result.metric_name}",
        f"\nVersion A ({result.version_a}):",
        f"  Mean: {result.a_mean:.4f}",
        f"  Samples: {len(result.a_values)}",
        f"\nVersion B ({result.version_b}):",
        f"  Mean: {result.b_mean:.4f}",
        f"  Samples: {len(result.b_values)}",
        f"\n🏆 Winner: {result.winner}",
        f"📈 Improvement: {result.improvement:.2f}%",
        f"🎯 Confidence: {result.confidence:.1%}",
        "=" * 60,
    ]

    return "\n".join(lines)


def format_test_result_table(results: list) -> str:
    """Format test results as ASCII table.

    Args:
        results: List of TestResult objects

    Returns:
        Formatted table string
    """
    lines = []
    lines.append("=" * 100)
    lines.append(f"{'Test Name':<40} {'Status':<10} {'Duration (ms)':<15} {'Error':<35}")
    lines.append("=" * 100)

    for result in results:
        status = "✓ PASS" if result.success else "✗ FAIL"
        error = (
            result.error[:32] + "..."
            if result.error and len(result.error) > 32
            else (result.error or "")
        )

        lines.append(
            f"{result.test_case.name:<40} "
            f"{status:<10} "
            f"{result.duration_ms:<15.2f} "
            f"{error:<35}"
        )

    lines.append("=" * 100)
    return "\n".join(lines)
