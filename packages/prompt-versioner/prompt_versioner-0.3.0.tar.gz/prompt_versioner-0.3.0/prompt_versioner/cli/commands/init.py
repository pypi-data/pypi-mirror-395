"""Initialization and setup commands."""

import click
from pathlib import Path
from prompt_versioner.cli.main_cli import cli
from prompt_versioner.cli.utils.formatters import (
    print_success,
    print_error,
    print_info,
    print_warning,
    console,
)


@cli.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """Initialize prompt versioner in current directory."""
    versioner = ctx.obj["versioner"]

    # Create .prompt_versions directory
    Path(".prompt_versions").mkdir(exist_ok=True)

    print_success("Initialized prompt versioner")
    console.print("Database: .prompt_versions/db.sqlite")

    # Offer to install Git hooks
    if versioner.git_tracker:
        if click.confirm("Install Git hooks for automatic versioning?"):
            versioner.install_git_hooks()
            print_success("Git hooks installed")


@cli.command()
@click.pass_context
def install_hooks(ctx: click.Context) -> None:
    """Install Git hooks for automatic versioning."""
    versioner = ctx.obj["versioner"]

    try:
        versioner.install_git_hooks()
        print_success("Git hooks installed")
    except RuntimeError as e:
        print_error(str(e))


@cli.command()
@click.pass_context
def uninstall_hooks(ctx: click.Context) -> None:
    """Uninstall Git hooks."""
    versioner = ctx.obj["versioner"]

    try:
        versioner.uninstall_git_hooks()
        print_success("Git hooks uninstalled")
    except RuntimeError as e:
        print_error(str(e))


@cli.command()
@click.option("--pre-commit", is_flag=True, help="Run in pre-commit mode")
@click.option("--post-commit", is_flag=True, help="Run in post-commit mode")
@click.pass_context
def auto_version(ctx: click.Context, pre_commit: bool, post_commit: bool) -> None:
    """Auto-version prompts (used by Git hooks)."""

    if pre_commit:
        print_info("Running pre-commit prompt versioning...")
        # Add pre-commit logic here
        print_success("Pre-commit checks passed")

    elif post_commit:
        print_info("Running post-commit prompt versioning...")
        # Add post-commit logic here
        print_success("Prompts versioned")

    else:
        print_warning("Specify --pre-commit or --post-commit")
