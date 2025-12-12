"""Commands for model pricing and cost estimation."""

import click
from typing import Optional, List, Dict, Any, cast
from prompt_versioner.cli.main_cli import cli
from prompt_versioner.cli.utils.formatters import (
    print_info,
    print_warning,
    console,
)
from prompt_versioner.metrics.pricing import PricingManager
from rich.table import Table
import json


@cli.command()
@click.option(
    "--format",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Output format (table or json)",
)
@click.option(
    "--sort-by",
    type=click.Choice(["name", "input", "output", "total"]),
    default="name",
    help="Sort models by field",
)
@click.option(
    "--filter",
    default=None,
    help="Filter models by name (case-insensitive substring match)",
)
@click.option(
    "--limit",
    type=int,
    default=None,
    help="Limit number of models displayed",
)
@click.pass_context
def models(
    ctx: click.Context,
    format: str,
    sort_by: str,
    filter: Optional[str],
    limit: Optional[int],
) -> None:
    """List available LLM models with pricing information.

    Examples:
        pv models                          # Show all models in table format
        pv models --sort-by input          # Sort by input price
        pv models --sort-by output         # Sort by output price
        pv models --filter gpt             # Filter GPT models only
        pv models --format json            # Export to JSON
        pv models --limit 10               # Show top 10 models
    """
    pricing_manager = PricingManager()

    models_list = pricing_manager.list_models()

    if not models_list:
        print_warning("No models available")
        return

    # Prepare model data
    model_data: List[Dict[str, Any]] = []
    for model_name in models_list:
        pricing = pricing_manager.get_pricing(model_name)
        if pricing:
            # Calculate average cost per 1000 tokens (500 in + 500 out)
            avg_cost = pricing_manager.calculate_cost(model_name, 500, 500)

            model_data.append(
                {
                    "name": model_name,
                    "input_price": pricing.input_price,
                    "output_price": pricing.output_price,
                    "currency": pricing.currency,
                    "avg_cost": avg_cost,
                }
            )

    # Filter if requested
    if filter:
        filter_lower: str = filter.lower()
        model_data = [m for m in model_data if filter_lower in cast(str, m["name"]).lower()]

        if not model_data:
            print_warning(f"No models found matching filter: '{filter}'")
            return

    # Sort
    sort_keys = {
        "name": lambda x: x["name"],
        "input": lambda x: x["input_price"],
        "output": lambda x: x["output_price"],
        "total": lambda x: x["avg_cost"],
    }
    model_data.sort(key=sort_keys[sort_by])

    # Limit if requested
    if limit and limit > 0:
        model_data = model_data[:limit]

    # JSON format
    if format == "json":
        output = [
            {
                "name": m["name"],
                "input_price_per_1m": m["input_price"],
                "output_price_per_1m": m["output_price"],
                "currency": m["currency"],
            }
            for m in model_data
        ]
        console.print(json.dumps(output, indent=2))
        return

    # Table format
    table = Table(title="Available LLM Models with Pricing", show_header=True, header_style="bold")
    table.add_column("Model Name", style="cyan", no_wrap=True, width=25)
    table.add_column("Input Price\n(per 1M tokens)", style="green", justify="right")
    table.add_column("Output Price\n(per 1M tokens)", style="yellow", justify="right")
    table.add_column("Avg Cost\n(500in+500out)", style="magenta", justify="right")

    for model in model_data:
        table.add_row(
            cast(str, model["name"]),
            f"€{model['input_price']:.2f}",
            f"€{model['output_price']:.2f}",
            f"€{model['avg_cost']:.6f}",
        )

    console.print(table)

    # Summary
    info_parts = [f"Total models: {len(model_data)}"]
    if filter:
        info_parts.append(f"(filtered by '{filter}')")
    if limit:
        info_parts.append(f"(showing top {limit})")

    print_info(" ".join(info_parts))

    # Show example calculation for top 3 cheapest
    if len(model_data) >= 3 and format != "json":
        console.print("\n[dim]Example: Cost for 1,000 input + 500 output tokens:[/dim]")
        example_models = sorted(model_data, key=lambda x: x["avg_cost"])[:3]

        for model in example_models:
            cost = pricing_manager.calculate_cost(cast(str, model["name"]), 1000, 500)
            console.print(f"  [cyan]{cast(str, model['name']):<25}[/cyan] €{cost:.6f}")


@cli.command()
@click.argument("model_name")
@click.argument("input_tokens", type=int)
@click.argument("output_tokens", type=int)
@click.option("--calls", type=int, default=1, help="Number of API calls to estimate")
@click.pass_context
def estimate_cost(
    ctx: click.Context, model_name: str, input_tokens: int, output_tokens: int, calls: int
) -> None:
    """Estimate cost for a specific model and token usage.

    Examples:
        pv estimate-cost gpt-4o 1000 500           # Single call
        pv estimate-cost gpt-4o-mini 1000 500 --calls 100  # 100 calls
    """
    pricing_manager = PricingManager()

    # Check if model exists
    if model_name not in pricing_manager.list_models():
        print_warning(f"Model '{model_name}' not found in pricing database")
        console.print("\n[dim]Available models:[/dim]")
        for model in sorted(pricing_manager.list_models())[:5]:
            console.print(f"  • {model}")
        console.print(
            f"\n[dim]Use 'pv models' to see all {len(pricing_manager.list_models())} models[/dim]"
        )
        return

    # Calculate estimate
    estimate = pricing_manager.estimate_cost(model_name, input_tokens, output_tokens, calls)

    # Display results
    table = Table(title=f"Cost Estimate: {model_name}", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")

    table.add_row("Input tokens per call", f"{input_tokens:,}")
    table.add_row("Output tokens per call", f"{output_tokens:,}")
    table.add_row("Number of calls", f"{calls:,}")
    table.add_row("Total input tokens", f"{estimate['total_input_tokens']:,}")
    table.add_row("Total output tokens", f"{estimate['total_output_tokens']:,}")
    table.add_row("", "")  # Separator
    table.add_row("[bold]Cost per call[/bold]", f"[bold]€{estimate['cost_per_call']:.6f}[/bold]")
    table.add_row(
        "[bold]Total cost[/bold]", f"[bold green]€{estimate['total_cost']:.4f}[/bold green]"
    )

    console.print(table)


@cli.command()
@click.argument("input_tokens", type=int)
@click.argument("output_tokens", type=int)
@click.option("--top", type=int, default=5, help="Show top N cheapest models")
@click.pass_context
def compare_costs(ctx: click.Context, input_tokens: int, output_tokens: int, top: int) -> None:
    """Compare costs across all models for given token usage.

    Examples:
        pv compare-costs 1000 500              # Compare all models
        pv compare-costs 1000 500 --top 10     # Show top 10 cheapest
    """
    pricing_manager = PricingManager()

    # Get all costs
    costs = pricing_manager.compare_models(input_tokens, output_tokens)

    if not costs:
        print_warning("No models available for comparison")
        return

    # Create table
    table = Table(
        title=f"Cost Comparison ({input_tokens:,} input + {output_tokens:,} output tokens)",
        show_header=True,
    )
    table.add_column("Rank", style="dim", justify="right", width=5)
    table.add_column("Model Name", style="cyan", width=25)
    table.add_column("Cost", style="green", justify="right")
    table.add_column("Relative", style="yellow", justify="right")

    # Get cheapest cost for relative calculation
    cheapest_cost = min(costs.values())

    # Add rows (limited to top N)
    items = list(costs.items())[:top] if top else list(costs.items())

    for idx, (model, cost) in enumerate(items, 1):
        relative = f"{(cost / cheapest_cost):.1f}x" if cheapest_cost > 0 else "N/A"

        # Highlight top 3
        if idx == 1:
            style = "bold green"
        elif idx == 2:
            style = "bold yellow"
        elif idx == 3:
            style = "bold"
        else:
            style = ""

        table.add_row(f"{idx}", f"[{style}]{model}[/{style}]", f"€{cost:.6f}", relative)

    console.print(table)

    # Summary
    total_models = len(costs)
    if top and top < total_models:
        print_info(f"Showing top {top} of {total_models} models")
        console.print(f"[dim]Use --top {total_models} to see all models[/dim]")
    else:
        print_info(f"Total models compared: {total_models}")
