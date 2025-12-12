"""Commands for diffing and comparing versions."""

import click
from prompt_versioner.app.services.diff_service import DiffEngine
from prompt_versioner.cli.main_cli import cli
from prompt_versioner.cli.utils.formatters import (
    format_diff_panel,
    format_comparison_table,
    print_error,
    console,
)


@cli.command()
@click.argument("name")
@click.argument("version1")
@click.argument("version2")
@click.pass_context
def diff(ctx: click.Context, name: str, version1: str, version2: str) -> None:
    """Show diff between two versions."""
    versioner = ctx.obj["versioner"]

    try:
        diff_result = versioner.diff(name, version1, version2)

        # Print summary panel
        panel = format_diff_panel(version1, version2, diff_result.summary)
        console.print(panel)

        # Print formatted diff
        diff_text = DiffEngine.format_diff_text(diff_result)
        console.print(diff_text)

    except ValueError as e:
        print_error(str(e))


@cli.command()
@click.argument("name")
@click.argument("versions", nargs=-1)
@click.pass_context
def compare(ctx: click.Context, name: str, versions: tuple) -> None:
    """Compare multiple versions with metrics."""
    versioner = ctx.obj["versioner"]

    if len(versions) < 2:
        print_error("Need at least 2 versions to compare")
        return

    try:
        comparison = versioner.compare_versions(name, list(versions))
        table = format_comparison_table(name, comparison)
        console.print(table)
    except ValueError as e:
        print_error(str(e))
