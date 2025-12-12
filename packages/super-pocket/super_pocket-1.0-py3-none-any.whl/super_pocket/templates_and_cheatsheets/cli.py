#!/usr/bin/env python3
"""
CLI for managing templates and cheatsheets.

Provides commands to:
- List available templates and cheatsheets
- View/display content in terminal
- Copy templates to user projects
- Validate template syntax
"""

import shutil
from pathlib import Path
from typing import Optional, Literal

from super_pocket.settings import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from . import TEMPLATES_DIR, CHEATSHEETS_DIR


console = Console()


def get_available_items(item_type: Literal["templates", "cheatsheets"]) -> list[Path]:
    """
    Get list of available templates or cheatsheets.

    Scans the appropriate directory and returns all Markdown files (.md) found,
    sorted alphabetically by filename.

    Args:
        item_type: Either "templates" or "cheatsheets" to specify which directory to scan.

    Returns:
        list[Path]: Sorted list of Path objects for available Markdown items.

    Example:
        >>> templates = get_available_items("templates")
        >>> [t.name for t in templates]
        ['agent_template.md', 'unit_tests_agent.md']
    """
    directory = TEMPLATES_DIR if item_type == "templates" else CHEATSHEETS_DIR
    return sorted(directory.glob("*.md"))


@click.group()
def templates_cli():
    """
    Manage agent templates and development cheatsheets.

    Provides commands to list, view, and copy templates/cheatsheets
    to your projects.
    """
    pass


@templates_cli.command(name="list")
@click.option(
    '--type', '-t',
    type=click.Choice(['templates', 'cheatsheets', 'all'], case_sensitive=False),
    default='all',
    help='Type of items to list.'
)
def list_items(type: str):
    """
    List available templates and cheatsheets.

    Displays a formatted table showing all available templates and/or cheatsheets
    with their names and descriptions (extracted from the first line of each file).

    Args:
        type: Filter by type - 'templates', 'cheatsheets', or 'all' (default: all).

    Examples:
        pocket templates list
        pocket templates list --type templates
        pocket templates list -t cheatsheets
    """
    table = Table(title="Available Templates & Cheatsheets", show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan", width=15)
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")

    if type in ['templates', 'all']:
        templates = get_available_items("templates")
        for template in templates:
            # Extract description from first line if available
            try:
                first_line = template.read_text(encoding='utf-8').split('\n')[0]
                description = first_line.replace('#', '').strip()[:60]
            except Exception:
                description = "N/A"

            table.add_row("Template", template.stem, description)

    if type in ['cheatsheets', 'all']:
        cheatsheets = get_available_items("cheatsheets")
        for cheatsheet in cheatsheets:
            try:
                first_line = cheatsheet.read_text(encoding='utf-8').split('\n')[0]
                description = first_line.replace('#', '').strip()[:60]
            except Exception:
                description = "N/A"

            table.add_row("Cheatsheet", cheatsheet.stem, description)

    console.print(table)


@templates_cli.command(name="view")
@click.argument('name', type=str)
@click.option(
    '--type', '-t',
    type=click.Choice(['template', 'cheatsheet'], case_sensitive=False),
    help='Type of item to view (auto-detected if not specified).'
)
def view_item(name: str, type: Optional[str]):
    """
    View/display a template or cheatsheet in the terminal.

    Renders the template or cheatsheet content with Markdown formatting
    directly in the terminal using Rich. If type is not specified, the
    function will attempt to auto-detect by searching templates first,
    then cheatsheets.

    Args:
        name: Name of the template or cheatsheet (without .md extension).
        type: Optional type specification - 'template' or 'cheatsheet'.
              Auto-detected if not provided.

    Raises:
        click.Abort: If the item is not found or cannot be read.

    Examples:
        pocket templates view unit_tests_agent
        pocket templates view SQL -t cheatsheet
    """
    # Try to find the item
    item_path = None

    if type == 'template' or type is None:
        potential_path = TEMPLATES_DIR / f"{name}.md"
        if potential_path.exists():
            item_path = potential_path

    if type == 'cheatsheet' or (type is None and item_path is None):
        potential_path = CHEATSHEETS_DIR / f"{name}.md"
        if potential_path.exists():
            item_path = potential_path

    if item_path is None:
        console.print(f"[red]Error:[/red] Item '{name}' not found.", style="bold")
        console.print("\nUse 'pocket templates list' to see available items.")
        raise click.Abort()

    try:
        content = item_path.read_text(encoding='utf-8')
        md = Markdown(content)
        console.print(md)
    except Exception as e:
        console.print(f"[red]Error reading file:[/red] {e}", style="bold")
        raise click.Abort()


@templates_cli.command(name="copy")
@click.argument('name', type=str)
@click.option(
    '--output', '-o',
    type=click.Path(path_type=Path),
    help='Output path for the copied file. If directory, file will be copied there with original name.'
)
@click.option(
    '--type', '-t',
    type=click.Choice(['template', 'cheatsheet'], case_sensitive=False),
    help='Type of item to copy (auto-detected if not specified).'
)
@click.option(
    '--force', '-f',
    is_flag=True,
    help='Overwrite existing file if it exists.'
)
def copy_item(name: str, output: Optional[Path], type: Optional[str], force: bool):
    """
    Copy a template or cheatsheet to your project.

    Copies the specified template or cheatsheet file to a destination in your
    project. Creates parent directories if they don't exist. If the output path
    is a directory, the file is copied there with its original name.

    Args:
        name: Name of the template or cheatsheet (without .md extension).
        output: Output path (file or directory) for the copied file.
                Defaults to current directory if not specified.
        type: Optional type specification - 'template' or 'cheatsheet'.
              Auto-detected if not provided.
        force: If True, overwrite existing file without confirmation.

    Raises:
        click.Abort: If the item is not found or copy operation fails.

    Examples:
        pocket templates copy unit_tests_agent -o .agents/
        pocket templates copy SQL -o docs/cheatsheets/ -t cheatsheet
        pocket templates copy my_agent -o ./custom.md -f
    """
    # Find the source item
    source_path = None

    if type == 'template' or type is None:
        potential_path = TEMPLATES_DIR / f"{name}.md"
        if potential_path.exists():
            source_path = potential_path

    if type == 'cheatsheet' or (type is None and source_path is None):
        potential_path = CHEATSHEETS_DIR / f"{name}.md"
        if potential_path.exists():
            source_path = potential_path

    if source_path is None:
        console.print(f"[red]Error:[/red] Item '{name}' not found.", style="bold")
        console.print("\nUse 'pocket templates list' to see available items.")
        raise click.Abort()

    # Determine output path
    if output is None:
        output = Path.cwd() / source_path.name
    elif output.is_dir():
        output = output / source_path.name

    # Check if file exists
    if output.exists() and not force:
        console.print(f"[yellow]Warning:[/yellow] File '{output}' already exists.", style="bold")
        if not click.confirm("Overwrite?"):
            console.print("Operation cancelled.")
            return

    try:
        # Create parent directories if needed
        output.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(source_path, output)

        console.print(f"[green]✓[/green] Successfully copied '{source_path.name}' to '{output}'", style="bold")

    except Exception as e:
        console.print(f"[red]Error copying file:[/red] {e}", style="bold")
        raise click.Abort()


@templates_cli.command(name="init")
@click.option(
    '--output', '-o',
    type=click.Path(path_type=Path),
    default=Path.cwd() / ".AGENTS",
    help='Directory where agent templates will be initialized.'
)
def init_agents(output: Path):
    """
    Initialize agent configuration directory with all templates.

    Creates a directory and copies all available agent templates into it.
    This is useful for quickly setting up agent configurations in a new project.
    The directory is created if it doesn't exist.

    Args:
        output: Directory where agent templates will be copied.
                Defaults to '.AGENTS' in the current working directory.

    Raises:
        click.Abort: If an error occurs during directory creation or file copying.

    Examples:
        pocket templates init
        pocket templates init -o ./agents/
        pocket templates init -o /path/to/my-project/.agents
    """
    try:
        # Create output directory
        output.mkdir(parents=True, exist_ok=True)

        templates = get_available_items("templates")

        if not templates:
            console.print("[yellow]Warning:[/yellow] No templates found to copy.", style="bold")
            return

        console.print(f"Initializing agent templates in: [cyan]{output}[/cyan]")

        copied_count = 0
        for template in templates:
            dest = output / template.name
            shutil.copy2(template, dest)
            console.print(f"  [green]✓[/green] {template.name}")
            copied_count += 1

        console.print(f"\n[green]Success![/green] Copied {copied_count} template(s) to '{output}'", style="bold")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        raise click.Abort()


if __name__ == '__main__':
    templates_cli()
