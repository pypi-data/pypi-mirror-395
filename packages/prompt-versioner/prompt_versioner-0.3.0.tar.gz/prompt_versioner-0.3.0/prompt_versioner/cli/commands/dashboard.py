"""Dashboard command for launching web interface."""

import click
from pathlib import Path
from rich.table import Table
from prompt_versioner.cli.main_cli import cli
from prompt_versioner.cli.utils import format_dashboard_info, print_success, print_warning, console


@cli.command()
@click.option("--port", "-p", default=5000, help="Port to run dashboard on")
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to (default: localhost)")
@click.option("--db-path", type=click.Path(), default=None, help="Custom database path")
@click.pass_context
def dashboard(ctx: click.Context, port: int, host: str, db_path: str) -> None:
    """Launch web dashboard (auto-detects database in current directory)."""
    from prompt_versioner.core import PromptVersioner
    from prompt_versioner.app import create_app

    project = ctx.obj.get("project", "default")

    # Auto-detect database in current directory
    default_db_dir = Path.cwd() / ".prompt_versions"
    default_db_path = default_db_dir / "db.sqlite"

    if db_path:
        db_path_obj = Path(db_path)
        console.print(f"[cyan]Using database:[/cyan] {db_path_obj}")
    elif default_db_path.exists():
        db_path_obj = default_db_path
        print_success(f"Found database: {db_path_obj}")
    else:
        db_path_obj = None
        print_warning("No database found, will create new one")
        if not project or project == "default":
            project = click.prompt("Enter project name", default=Path.cwd().name)

    # Display startup info
    panel = format_dashboard_info(
        project=project, db_path=str(db_path_obj or default_db_path), port=port
    )
    console.print(panel)

    # Create versioner
    pv = PromptVersioner(project_name=project, db_path=db_path_obj, enable_git=False)

    # Show current stats
    prompts = pv.list_prompts()
    if prompts:
        table = Table(title="Current Prompts")
        table.add_column("Name", style="cyan")
        table.add_column("Versions", style="magenta")
        table.add_column("Latest", style="green")

        for prompt_name in prompts[:10]:
            versions = pv.list_versions(prompt_name)
            latest = versions[0] if versions else None
            table.add_row(
                prompt_name, str(len(versions)), latest["version"][:20] if latest else "N/A"
            )

        console.print(table)

        if len(prompts) > 10:
            console.print(f"\n[dim]... and {len(prompts) - 10} more prompts[/dim]")
    else:
        print_warning("No prompts tracked yet")
        console.print("[dim]Start using PromptVersioner in your code to see data here[/dim]\n")

    console.print(f"\n[bold green]Dashboard: http://localhost:{port}[/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    try:
        app = create_app(pv)
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        print_warning("\nDashboard stopped")


# Standalone command (can be called directly without CLI group)
@click.command()
@click.option("--port", "-p", default=5000, help="Port to run dashboard on")
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind to (default: localhost)")
@click.option("--project", default=None, help="Project name")
@click.option("--db-path", type=click.Path(), default=None, help="Database path")
def dashboard_standalone(port: int, host: str, project: str, db_path: str) -> None:
    """Launch Prompt Versioner Dashboard (standalone).

    Auto-detects database in current directory (.prompt_versions/db.sqlite)
    or creates new one if not found.
    """
    from prompt_versioner.core import PromptVersioner
    from prompt_versioner.app import create_app
    from rich.console import Console
    from rich.table import Table

    console = Console()

    # Auto-detect database
    default_db_dir = Path.cwd() / ".prompt_versions"
    default_db_path = default_db_dir / "db.sqlite"

    if db_path:
        db_path_obj = Path(db_path)
        console.print(f"[cyan]Using database:[/cyan] {db_path_obj}")
    elif default_db_path.exists():
        db_path_obj = default_db_path
        console.print(f"[green]✓ Found database:[/green] {db_path_obj}")
    else:
        db_path_obj = None
        console.print("[yellow]No database found, will create new one[/yellow]")

    if not project:
        project = Path.cwd().name

    panel = format_dashboard_info(
        project=project, db_path=str(db_path_obj or default_db_path), port=port
    )
    console.print(panel)

    # Create versioner
    pv = PromptVersioner(project_name=project, db_path=db_path_obj, enable_git=False)

    # Show stats
    prompts = pv.list_prompts()
    if prompts:
        table = Table(title="Current Prompts")
        table.add_column("Name", style="cyan")
        table.add_column("Versions", style="magenta")
        table.add_column("Latest", style="green")

        for prompt_name in prompts[:10]:
            versions = pv.list_versions(prompt_name)
            latest = versions[0] if versions else None
            table.add_row(
                prompt_name, str(len(versions)), latest["version"][:20] if latest else "N/A"
            )

        console.print(table)

        if len(prompts) > 10:
            console.print(f"\n[dim]... and {len(prompts) - 10} more prompts[/dim]")
    else:
        console.print("\n[yellow]No prompts tracked yet[/yellow]")
        console.print("[dim]Start using PromptVersioner in your code to see data here[/dim]\n")

    console.print(f"\n[bold green]Dashboard: http://localhost:{port}[/bold green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]\n")

    try:
        app = create_app(pv)
        app.run(host=host, port=port, debug=False)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Dashboard stopped[/yellow]")
