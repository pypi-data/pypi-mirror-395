"""CLI commands modules."""

# Import all command modules to register them with the CLI group
from prompt_versioner.cli.commands import init
from prompt_versioner.cli.commands import prompts
from prompt_versioner.cli.commands import diff
from prompt_versioner.cli.commands import management
from prompt_versioner.cli.commands import dashboard
from prompt_versioner.cli.commands import pricing

__all__ = ["init", "prompts", "diff", "management", "dashboard", "pricing"]
