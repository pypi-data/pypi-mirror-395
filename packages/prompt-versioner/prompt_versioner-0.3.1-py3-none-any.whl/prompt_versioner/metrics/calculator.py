"""Metrics calculation utilities."""

from typing import Optional
from prompt_versioner.metrics.models import ModelMetrics
from prompt_versioner.metrics.pricing import PricingManager


class MetricsCalculator:
    """Calculate various metrics for LLM calls."""

    def __init__(self, pricing_manager: Optional[PricingManager] = None):
        """Initialize calculator.

        Args:
            pricing_manager: Optional custom pricing manager
        """
        self.pricing_manager = pricing_manager or PricingManager()

    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in EUR for a model call.

        Args:
            model_name: Name of the model
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in EUR
        """
        return self.pricing_manager.calculate_cost(model_name, input_tokens, output_tokens)

    def enrich_metrics(self, metrics: ModelMetrics) -> ModelMetrics:
        """Enrich metrics with calculated values.

        Calculates cost if not provided and calculates derived metrics.

        Args:
            metrics: ModelMetrics object

        Returns:
            Enriched ModelMetrics object
        """
        # Calculate total tokens if not provided
        if metrics.total_tokens is None:
            if metrics.input_tokens and metrics.output_tokens:
                metrics.total_tokens = metrics.input_tokens + metrics.output_tokens

        # Calculate cost if not provided
        if metrics.cost_eur is None:
            if (
                metrics.model_name is not None
                and metrics.input_tokens is not None
                and metrics.output_tokens is not None
            ):
                metrics.cost_eur = self.calculate_cost(
                    metrics.model_name, metrics.input_tokens, metrics.output_tokens
                )

        # Add derived metrics to metadata
        if metrics.metadata is None:
            metrics.metadata = {}

        # Cost per token
        if metrics.cost_eur and metrics.total_tokens:
            metrics.metadata["cost_per_token"] = metrics.cost_eur / metrics.total_tokens

        # Tokens per second
        if metrics.total_tokens and metrics.latency_ms:
            metrics.metadata["tokens_per_second"] = metrics.total_tokens / (
                metrics.latency_ms / 1000
            )

        # Cost per second
        if metrics.cost_eur and metrics.latency_ms:
            metrics.metadata["cost_per_second"] = metrics.cost_eur / (metrics.latency_ms / 1000)

        return metrics

    def calculate_efficiency_score(self, metrics: ModelMetrics) -> float:
        """Calculate efficiency score (quality per cost).

        Args:
            metrics: ModelMetrics object

        Returns:
            Efficiency score (0-100)
        """
        if not metrics.quality_score or not metrics.cost_eur:
            return 0.0

        if metrics.cost_eur == 0:
            return 100.0

        # Quality (0-1) divided by cost, normalized to 0-100
        raw_score = metrics.quality_score / metrics.cost_eur

        # Normalize (assuming typical costs are 0.001 to 0.1 EUR)
        normalized = min(raw_score * 10, 100.0)

        return normalized

    def calculate_value_score(
        self,
        metrics: ModelMetrics,
        quality_weight: float = 0.5,
        cost_weight: float = 0.3,
        latency_weight: float = 0.2,
    ) -> float:
        """Calculate overall value score.

        Combines quality, cost, and latency into single score.

        Args:
            metrics: ModelMetrics object
            quality_weight: Weight for quality (0-1)
            cost_weight: Weight for cost (0-1)
            latency_weight: Weight for latency (0-1)

        Returns:
            Value score (0-100)
        """
        score = 0.0
        total_weight = 0.0

        # Quality component (higher is better)
        if metrics.quality_score is not None:
            score += metrics.quality_score * 100 * quality_weight
            total_weight += quality_weight

        # Cost component (lower is better, normalize to 0-100)
        if metrics.cost_eur is not None:
            # Assume costs range from 0.0001 to 1.0 EUR
            cost_score = max(0, 100 - (metrics.cost_eur * 100))
            score += cost_score * cost_weight
            total_weight += cost_weight

        # Latency component (lower is better, normalize to 0-100)
        if metrics.latency_ms is not None:
            # Assume latency ranges from 100ms to 10000ms
            latency_score = max(0, 100 - (metrics.latency_ms / 100))
            score += latency_score * latency_weight
            total_weight += latency_weight

        return score / total_weight if total_weight > 0 else 0.0
