"""Test context manager for prompt versions."""

from typing import Any, Dict, Optional


class TestContext:
    """Context manager for testing prompt versions."""

    def __init__(self, versioner: Any, name: str, version: str):
        """Initialize test context.

        Args:
            versioner: PromptVersioner instance
            name: Prompt name
            version: Version string
        """
        self.versioner = versioner
        self.name = name
        self.version = version
        self.metrics: Dict[str, Any] = {}

    def __enter__(self) -> "TestContext":
        """Enter context."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context and save metrics."""
        if self.metrics:
            self.versioner.log_metrics(self.name, self.version, **self.metrics)

    def log(
        self,
        model_name: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        cost_eur: Optional[float] = None,
        latency_ms: Optional[float] = None,
        quality_score: Optional[float] = None,
        accuracy: Optional[float] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        **extra: Any,
    ) -> None:
        """Log metrics during test.

        Args:
            model_name: Model name
            input_tokens: Input tokens
            output_tokens: Output tokens
            cost_eur: Cost in EUR
            latency_ms: Latency in ms
            quality_score: Quality score
            accuracy: Accuracy
            temperature: Temperature
            max_tokens: Max tokens
            success: Success flag
            error_message: Error message
            **extra: Extra metadata
        """
        self.metrics.update(
            {
                "model_name": model_name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_eur": cost_eur,
                "latency_ms": latency_ms,
                "quality_score": quality_score,
                "accuracy": accuracy,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "success": success,
                "error_message": error_message,
                "metadata": extra if extra else None,
            }
        )
