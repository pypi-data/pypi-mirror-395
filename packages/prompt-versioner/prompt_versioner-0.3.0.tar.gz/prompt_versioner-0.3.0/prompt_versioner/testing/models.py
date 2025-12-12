"""Data models for testing framework."""

from dataclasses import dataclass
from typing import Callable, Dict, List, Any, Optional


@dataclass
class TestCase:
    """A single test case for a prompt."""

    name: str
    inputs: Dict[str, Any]
    expected_output: Optional[Any] = None
    validation_fn: Optional[Callable[[Any], bool]] = None


@dataclass
class TestResult:
    """Result of running a test case."""

    test_case: TestCase
    success: bool
    output: Any
    metrics: Dict[str, float]
    error: Optional[str] = None
    duration_ms: float = 0.0


@dataclass
class ABTestResult:
    """Result of an A/B test."""

    version_a: str
    version_b: str
    metric_name: str
    a_values: List[float]
    b_values: List[float]
    a_mean: float
    b_mean: float
    winner: str
    improvement: float
    confidence: float
