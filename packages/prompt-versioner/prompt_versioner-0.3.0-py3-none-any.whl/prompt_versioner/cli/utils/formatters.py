"""Formatting utilities for CLI output."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict, Any


console = Console()


def format_prompts_table(prompts: List[str], versioner: Any) -> Table:
    """Format prompts list as table.

    Args:
        prompts: List of prompt names
        versioner: PromptVersioner instance

    Returns:
        Rich Table
    """
    table = Table(title="Tracked Prompts")
    table.add_column("Name", style="cyan")
    table.add_column("Versions", style="magenta")
    table.add_column("Latest", style="green")

    for prompt in prompts:
        versions = versioner.list_versions(prompt)
        latest = versions[0] if versions else None

        table.add_row(
            prompt,
            str(len(versions)),
            latest["version"] if latest else "N/A",
        )

    return table


def format_versions_table(name: str, versions: List[Dict[str, Any]]) -> Table:
    """Format versions list as table.

    Args:
        name: Prompt name
        versions: List of version dicts

    Returns:
        Rich Table
    """
    table = Table(title=f"Versions of '{name}'")
    table.add_column("Version", style="cyan")
    table.add_column("Timestamp", style="green")
    table.add_column("Git Commit", style="magenta")

    for v in versions:
        table.add_row(
            v["version"],
            v["timestamp"],
            v.get("git_commit", "N/A")[:8] if v.get("git_commit") else "N/A",
        )

    return table


def format_version_detail(name: str, version: Dict[str, Any]) -> None:
    """Print version details.

    Args:
        name: Prompt name
        version: Version dict
    """
    # Metadata panel
    console.print(
        Panel(
            f"[cyan]Version:[/cyan] {version['version']}\n"
            f"[cyan]Timestamp:[/cyan] {version['timestamp']}\n"
            f"[cyan]Git Commit:[/cyan] {version.get('git_commit', 'N/A')}",
            title=f"Prompt: {name}",
            border_style="green",
        )
    )

    # System prompt
    console.print("\n[bold]System Prompt:[/bold]")
    console.print(Panel(version["system_prompt"], border_style="blue"))

    # User prompt
    console.print("\n[bold]User Prompt:[/bold]")
    console.print(Panel(version["user_prompt"], border_style="magenta"))


def format_metrics_table(metrics: Dict[str, List[float]]) -> Table:
    """Format metrics as table.

    Args:
        metrics: Dict of metric name to values

    Returns:
        Rich Table
    """
    table = Table(title="Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="yellow")
    table.add_column("Average", style="green")
    table.add_column("Min", style="blue")
    table.add_column("Max", style="magenta")

    for metric_name, values in metrics.items():
        if values:
            table.add_row(
                metric_name,
                str(len(values)),
                f"{sum(values)/len(values):.4f}",
                f"{min(values):.4f}",
                f"{max(values):.4f}",
            )

    return table


def format_comparison_table(name: str, comparison: Dict[str, Any]) -> Table:
    """Format version comparison as table.

    Args:
        name: Prompt name
        comparison: Comparison dict

    Returns:
        Rich Table
    """
    table = Table(title=f"Comparison: {name}")
    table.add_column("Version", style="cyan")
    table.add_column("Timestamp", style="green")
    table.add_column("Metrics", style="magenta")

    for v_data in comparison["versions"]:
        metrics_str = (
            ", ".join(f"{k}: {sum(v)/len(v):.2f}" for k, v in v_data["metrics"].items() if v)
            or "No metrics"
        )

        table.add_row(
            v_data["version"],
            v_data["timestamp"],
            metrics_str,
        )

    return table


def format_diff_panel(version1: str, version2: str, summary: str) -> Panel:
    """Format diff summary as panel.

    Args:
        version1: First version
        version2: Second version
        summary: Diff summary text

    Returns:
        Rich Panel
    """
    return Panel(
        summary,
        title=f"Diff: {version1} → {version2}",
        border_style="blue",
    )


def format_dashboard_info(project: str, db_path: str, port: int) -> Panel:
    """Format dashboard startup info.

    Args:
        project: Project name
        db_path: Database path
        port: Server port

    Returns:
        Rich Panel
    """
    return Panel(
        f"[cyan]Project:[/cyan] {project}\n"
        f"[cyan]Database:[/cyan] {db_path}\n"
        f"[cyan]URL:[/cyan] http://localhost:{port}",
        title="Prompt Versioner Dashboard",
        border_style="green",
    )


def print_success(message: str) -> None:
    """Print success message."""
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message."""
    console.print(f"[red]Error:[/red] {message}")


def print_warning(message: str) -> None:
    """Print warning message."""
    console.print(f"[yellow]{message}[/yellow]")


def print_info(message: str) -> None:
    """Print info message."""
    console.print(f"[blue]{message}[/blue]")
