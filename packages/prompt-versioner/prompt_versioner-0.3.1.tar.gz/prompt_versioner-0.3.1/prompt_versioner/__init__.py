"""Prompt Versioner - Intelligent versioning for LLM prompts."""

# Import relativi corretti per quando è installato come package
from prompt_versioner.core import PromptVersioner, TestContext, VersionBump, PreReleaseLabel
from prompt_versioner.storage import PromptStorage
from prompt_versioner.app import (
    DiffEngine,
    PromptDiff,
    ChangeType,
    PerformanceMonitor,
    Alert,
    AlertType,
)
from prompt_versioner.tracker import GitTracker, AutoTracker, PromptHasher
from prompt_versioner.metrics import (
    MetricsTracker,
    MetricType,
    MetricAggregator,
    ModelMetrics,
    MetricsCalculator,
)
from prompt_versioner.testing import (
    PromptTestRunner,
    TestCase,
    TestResult,
    TestDataset,
    ABTest,
    ABTestResult,
)

__version__ = "0.1.0"

__all__ = [
    "PromptVersioner",
    "TestContext",
    "VersionBump",
    "PreReleaseLabel",
    "PromptStorage",
    "DiffEngine",
    "PromptDiff",
    "ChangeType",
    "GitTracker",
    "AutoTracker",
    "PromptHasher",
    "MetricsTracker",
    "MetricType",
    "MetricAggregator",
    "ModelMetrics",
    "MetricsCalculator",
    "PromptTestRunner",
    "TestCase",
    "TestResult",
    "TestDataset",
    "ABTest",
    "ABTestResult",
    "PerformanceMonitor",
    "Alert",
    "AlertType",
]
