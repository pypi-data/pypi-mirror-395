"""Model pricing and cost calculation."""

from typing import Dict, Optional


# Model pricing per 1M tokens (input/output) in EUR
DEFAULT_MODEL_PRICING = {
    # Claude models
    "claude-opus-4-1": {"input": 12.80, "output": 64.89},
    "claude-opus-4": {"input": 12.80, "output": 64.89},
    "claude-sonnet-4-5": {"input": 2.60, "output": 12.98},
    "claude-sonnet-4": {"input": 2.60, "output": 12.98},
    "claude-haiku-4-5": {"input": 0.87, "output": 4.33},
    # Mistral models
    "mistral-large-2411": {"input": 1.84, "output": 5.52},
    "mistral-medium-2595": {"input": 0.35, "output": 1.73},
    "mistral-small": {"input": 0.09, "output": 0.28},
    "mistral-nemo": {"input": 0.14, "output": 0.14},
    # OpenAI models
    "gpt-5": {"input": 1.08, "output": 8.58},
    "gpt-5-mini": {"input": 0.22, "output": 1.72},
    "gpt-5-nano": {"input": 0.05, "output": 0.35},
    "gpt-4-1": {"input": 1.72, "output": 6.86},
    "gpt-4-1-mini": {"input": 0.35, "output": 1.38},
    "gpt-4o": {"input": 2.15, "output": 8.57},
    "gpt-4o-mini": {"input": 0.13, "output": 0.52},
}


class ModelPricing:
    """Model pricing information."""

    def __init__(self, input_price: float, output_price: float, currency: str = "EUR"):
        """Initialize pricing.

        Args:
            input_price: Price per 1M input tokens
            output_price: Price per 1M output tokens
            currency: Currency code
        """
        self.input_price = input_price
        self.output_price = output_price
        self.currency = currency

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Total cost in specified currency
        """
        input_cost = (input_tokens / 1_000_000) * self.input_price
        output_cost = (output_tokens / 1_000_000) * self.output_price
        return input_cost + output_cost

    def to_dict(self) -> Dict[str, float | str]:
        """Convert to dictionary."""
        return {
            "input_price": self.input_price,
            "output_price": self.output_price,
            "currency": self.currency,
        }


class PricingManager:
    """Manages model pricing information."""

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None):
        """Initialize pricing manager.

        Args:
            custom_pricing: Optional custom pricing dictionary
        """
        self.pricing = DEFAULT_MODEL_PRICING.copy()
        if custom_pricing:
            self.pricing.update(custom_pricing)

    def get_pricing(self, model_name: str) -> Optional[ModelPricing]:
        """Get pricing for a model.

        Args:
            model_name: Name of the model

        Returns:
            ModelPricing object or None if not found
        """
        if model_name not in self.pricing:
            return None

        prices = self.pricing[model_name]
        return ModelPricing(input_price=prices["input"], output_price=prices["output"])

    def add_model(self, model_name: str, input_price: float, output_price: float) -> None:
        """Add or update pricing for a model.

        Args:
            model_name: Name of the model
            input_price: Price per 1M input tokens
            output_price: Price per 1M output tokens
        """
        self.pricing[model_name] = {"input": input_price, "output": output_price}

    def remove_model(self, model_name: str) -> bool:
        """Remove a model from pricing.

        Args:
            model_name: Name of the model

        Returns:
            True if removed, False if not found
        """
        if model_name in self.pricing:
            del self.pricing[model_name]
            return True
        return False

    def list_models(self) -> list[str]:
        """Get list of all models with pricing.

        Returns:
            List of model names
        """
        return list(self.pricing.keys())

    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a model call.

        Args:
            model_name: Name of the model
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in EUR, or 0.0 if model not found
        """
        pricing = self.get_pricing(model_name)
        if pricing is None:
            return 0.0

        return pricing.calculate_cost(input_tokens, output_tokens)

    def estimate_cost(
        self, model_name: str, input_tokens: int, output_tokens: int, num_calls: int = 1
    ) -> Dict[str, float]:
        """Estimate costs for multiple calls.

        Args:
            model_name: Name of the model
            input_tokens: Number of input tokens per call
            output_tokens: Number of output tokens per call
            num_calls: Number of calls

        Returns:
            Dict with cost breakdown
        """
        cost_per_call = self.calculate_cost(model_name, input_tokens, output_tokens)
        total_cost = cost_per_call * num_calls

        return {
            "cost_per_call": cost_per_call,
            "total_cost": total_cost,
            "num_calls": num_calls,
            "total_input_tokens": input_tokens * num_calls,
            "total_output_tokens": output_tokens * num_calls,
        }

    def compare_models(self, input_tokens: int, output_tokens: int) -> Dict[str, float]:
        """Compare costs across all models.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Dict of model_name -> cost
        """
        costs = {}
        for model_name in self.list_models():
            costs[model_name] = self.calculate_cost(model_name, input_tokens, output_tokens)

        return dict(sorted(costs.items(), key=lambda x: x[1]))

    def get_cheapest_model(self, input_tokens: int, output_tokens: int) -> tuple[str, float]:
        """Find the cheapest model for given token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Tuple of (model_name, cost)
        """
        costs = self.compare_models(input_tokens, output_tokens)
        if not costs:
            return ("unknown", 0.0)

        cheapest = min(costs.items(), key=lambda x: x[1])
        return cheapest
