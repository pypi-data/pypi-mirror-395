"""Commands for listing and viewing prompts."""

from typing import Dict, List
import click
from prompt_versioner.cli.main_cli import cli
from prompt_versioner.cli.utils.formatters import (
    format_prompts_table,
    format_versions_table,
    format_version_detail,
    format_metrics_table,
    print_warning,
    print_error,
    console,
)


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List all tracked prompts."""
    versioner = ctx.obj["versioner"]
    prompts = versioner.list_prompts()

    if not prompts:
        print_warning("No prompts tracked yet")
        return

    table = format_prompts_table(prompts, versioner)
    console.print(table)


@cli.command()
@click.argument("name")
@click.pass_context
def versions(ctx: click.Context, name: str) -> None:
    """List all versions of a prompt."""
    versioner = ctx.obj["versioner"]
    versions_list = versioner.list_versions(name)

    if not versions_list:
        print_warning(f"No versions found for prompt '{name}'")
        return

    table = format_versions_table(name, versions_list)
    console.print(table)


@cli.command()
@click.argument("name")
@click.argument("version")
@click.pass_context
def show(ctx: click.Context, name: str, version: str) -> None:
    """Show details of a specific version."""
    versioner = ctx.obj["versioner"]
    v = versioner.get_version(name, version)

    if not v:
        print_error(f"Version '{version}' not found for prompt '{name}'")
        return

    # Show version details
    format_version_detail(name, v)

    # Show metrics if available
    metrics = versioner.storage.get_metrics(v["id"])
    if metrics:
        console.print("\n[bold]Metrics:[/bold]")

        # Aggregate metrics for display
        aggregated: Dict[str, List[float]] = {}
        for metric in metrics:
            for key, value in metric.items():
                if (
                    key not in ["id", "version_id", "timestamp", "metadata", "error_message"]
                    and value is not None
                ):
                    if isinstance(value, (int, float)):
                        if key not in aggregated:
                            aggregated[key] = []
                        aggregated[key].append(float(value))

        if aggregated:
            table = format_metrics_table(aggregated)
            console.print(table)
        else:
            console.print("No numeric metrics available for this version.")
    else:
        console.print("\n[dim]No metrics recorded for this version.[/dim]")
