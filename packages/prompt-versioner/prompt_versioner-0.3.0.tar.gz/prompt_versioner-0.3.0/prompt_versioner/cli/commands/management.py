"""Commands for managing versions (rollback, delete)."""

import click
from prompt_versioner.cli.main_cli import cli
from prompt_versioner.cli.utils.formatters import print_success, print_error, print_warning, console


@cli.command()
@click.argument("name")
@click.argument("to_version")
@click.pass_context
def rollback(ctx: click.Context, name: str, to_version: str) -> None:
    """Rollback to a previous version."""
    versioner = ctx.obj["versioner"]

    if not click.confirm(f"Rollback '{name}' to version '{to_version}'?"):
        return

    try:
        new_version_id = versioner.rollback(name, to_version)
        print_success(f"Rolled back to {to_version}")
        console.print(f"Created new version with ID: {new_version_id}")
    except ValueError as e:
        print_error(str(e))


@cli.command()
@click.argument("name")
@click.option("--delete-all", is_flag=True, help="Delete all versions")
@click.argument("version", required=False)
@click.pass_context
def delete(ctx: click.Context, name: str, version: str, delete_all: bool) -> None:
    """Delete a specific version or all versions of a prompt."""
    versioner = ctx.obj["versioner"]

    if delete_all:
        if not click.confirm(f"Delete ALL versions of '{name}'?", abort=True):
            return

        versions = versioner.list_versions(name)
        for v in versions:
            versioner.storage.delete_version(name, v["version"])

        print_success(f"Deleted {len(versions)} versions of '{name}'")

    elif version:
        if not click.confirm(f"Delete version '{version}' of '{name}'?", abort=True):
            return

        if versioner.storage.delete_version(name, version):
            print_success(f"Deleted version '{version}'")
        else:
            print_error(f"Version '{version}' not found")

    else:
        print_warning("Specify a version or use --delete-all")


@cli.command("clear-db")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def clear_db(ctx: click.Context, force: bool) -> None:
    """Clear all prompts and data from the database."""
    versioner = ctx.obj["versioner"]

    # Get all prompts
    prompts = versioner.list_prompts()

    if not prompts:
        console.print("✨ [green]Database is already empty![/green]")
        return

    # Show what will be deleted
    console.print(f"\n📊 [yellow]Found {len(prompts)} prompt(s):[/yellow]")
    total_versions = 0
    for prompt in prompts:
        versions = versioner.list_versions(prompt)
        total_versions += len(versions)
        console.print(f"   • {prompt} ({len(versions)} versions)")

    console.print(f"\n📈 [red]Total: {total_versions} versions across {len(prompts)} prompts[/red]")

    # Confirmation
    if not force:
        console.print(
            "\n⚠️  [bold red]This will permanently delete ALL prompts and their data![/bold red]"
        )
        console.print("   - All prompt versions")
        console.print("   - All metrics and logs")
        console.print("   - All annotations and metadata")

        if not click.confirm("\nAre you sure you want to continue?", abort=True):
            return

    # Delete all prompts
    console.print("\n🗑️  [yellow]Deleting all prompts...[/yellow]")
    deleted_count = 0

    with console.status("[spinner] Deleting prompts...") as status:
        for prompt in prompts:
            status.update(f"[spinner] Deleting {prompt}...")
            versions = versioner.list_versions(prompt)
            for version in versions:
                versioner.storage.delete_version(prompt, version["version"])
                deleted_count += 1

    # Clean up database
    console.print("🧹 [yellow]Cleaning up database...[/yellow]")
    versioner.storage.db.vacuum()

    print_success(f"Deleted {deleted_count} versions across {len(prompts)} prompts")
    console.print("✨ [green]Database is now empty![/green]")

    # Show database stats
    db_size = versioner.storage.db.get_db_size()
    console.print(f"📊 Database size: {db_size / 1024:.1f} KB")


# Standalone command for direct execution
@click.command()
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.option("--project", default=None, help="Project name")
@click.option("--db-path", type=click.Path(), default=None, help="Database path")
def clear_db_standalone(force: bool, project: str, db_path: str) -> None:
    """Clear all prompts and data from the database (standalone)."""
    from prompt_versioner.core import PromptVersioner
    from pathlib import Path

    # Auto-detect database
    default_db_dir = Path.cwd() / ".prompt_versions"
    default_db_path = default_db_dir / "db.sqlite"

    if db_path:
        db_path_obj = Path(db_path)
    elif default_db_path.exists():
        db_path_obj = default_db_path
    else:
        console.print("[red]❌ No database found![/red]")
        console.print("   Expected: .prompt_versions/db.sqlite")
        console.print("   Use --db-path to specify custom location")
        return

    if not project:
        project = Path.cwd().name

    console.print(f"[cyan]Database:[/cyan] {db_path_obj}")
    console.print(f"[cyan]Project:[/cyan] {project}")

    # Create versioner
    versioner = PromptVersioner(project_name=project, db_path=db_path_obj, enable_git=False)

    # Get all prompts
    prompts = versioner.list_prompts()

    if not prompts:
        console.print("✨ [green]Database is already empty![/green]")
        return

    # Show what will be deleted
    console.print(f"\n📊 [yellow]Found {len(prompts)} prompt(s):[/yellow]")
    total_versions = 0
    for prompt in prompts:
        versions = versioner.list_versions(prompt)
        total_versions += len(versions)
        console.print(f"   • {prompt} ({len(versions)} versions)")

    console.print(f"\n📈 [red]Total: {total_versions} versions across {len(prompts)} prompts[/red]")

    # Confirmation
    if not force:
        console.print(
            "\n⚠️  [bold red]This will permanently delete ALL prompts and their data![/bold red]"
        )
        console.print("   - All prompt versions")
        console.print("   - All metrics and logs")
        console.print("   - All annotations and metadata")

        if not click.confirm("\nAre you sure you want to continue?", abort=True):
            return

    # Delete all prompts
    console.print("\n🗑️  [yellow]Deleting all prompts...[/yellow]")
    deleted_count = 0

    with console.status("[spinner] Deleting prompts...") as status:
        for prompt in prompts:
            status.update(f"[spinner] Deleting {prompt}...")
            versions = versioner.list_versions(prompt)
            for version in versions:
                versioner.storage.delete_version(prompt, version["version"])
                deleted_count += 1

    # Clean up database
    console.print("🧹 [yellow]Cleaning up database...[/yellow]")
    versioner.storage.db.vacuum()

    console.print(
        f"✅ [green]Deleted {deleted_count} versions across {len(prompts)} prompts[/green]"
    )
    console.print("✨ [green]Database is now empty![/green]")

    # Show database stats
    db_size = versioner.storage.db.get_db_size()
    console.print(f"📊 Database size: {db_size / 1024:.1f} KB")
