"""Command-line interface for prompt-versioner."""

from prompt_versioner.cli.main_cli import cli, main
from prompt_versioner.cli.commands.dashboard import dashboard_standalone

__all__ = ["cli", "main", "dashboard_standalone"]
