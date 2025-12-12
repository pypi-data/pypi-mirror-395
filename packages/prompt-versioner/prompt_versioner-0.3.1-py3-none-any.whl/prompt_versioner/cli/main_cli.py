"""Main CLI group and entry point."""

import click
from prompt_versioner.core import PromptVersioner


@click.group()
@click.option("--project", default="default", help="Project name")
@click.pass_context
def cli(ctx: click.Context, project: str) -> None:
    """Prompt Versioner - Intelligent versioning for LLM prompts."""
    ctx.ensure_object(dict)
    ctx.obj["versioner"] = PromptVersioner(project_name=project)
    ctx.obj["project"] = project


def main() -> None:
    """Entry point for CLI."""
    # Import commands to register them

    cli()


if __name__ == "__main__":
    main()
