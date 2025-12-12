#!/usr/bin/env python3
"""
Pocket - Unified CLI entry point.

This module provides a unified command-line interface for all Pocket
functionalities, organized into logical subcommands.
"""
import asyncio
import sys
from super_pocket.settings import click

from rich.console import Console
from pathlib import Path

from super_pocket import __version__
from super_pocket.web.job_search import main as job_search
from super_pocket.markdown.renderer import markd
from super_pocket.project.to_file import create_codebase_markdown
# from super_pocket.project.readme import run_readme_wizard  # Module moved
from super_pocket.templates_and_cheatsheets.cli import (
    list_items, view_item, copy_item, init_agents
)
from super_pocket.pdf.converter import pdf_convert
from super_pocket.web.favicon import convert_to_favicon as favicon_convert
from super_pocket.project.req_to_date import run_req_to_date
from super_pocket.readme.cli import readme_cli
from super_pocket.web.favicon import favicon
from super_pocket.project.req_to_date import run_req_to_date, print_req_to_date_results
from super_pocket.project.init.cli import init_group
from super_pocket.interactive import pocket_cmd
from super_pocket.xml.cli import xml as xml_cmd



console = Console()


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="pocket")
@click.pass_context
def cli(ctx):
    """
    A collection of tools.

    Available commands:
    - markdown: Render markdown files in terminal
    - project: Project management tools (export to file, etc.)
    - templates: Manage agent templates and cheatsheets
    - pdf: PDF conversion tools
    - web: Web utilities (favicon conversion, etc.)
    - readme: Generate README.md files or analyze your project
    - req-to-date: Check for outdated dependencies
    - xml: Convert custom tag syntax into formatted XML

    Examples:
        pocket markdown render README.md
        pocket project to-file . -o project-to-file.md
        pocket templates list
        pocket readme generate README.md
        pocket project req-to-date pyproject.toml
    """
    if ctx.invoked_subcommand is None and not ctx.args:
        if sys.stdin is None or not sys.stdin.isatty():
            click.echo(ctx.get_help())
            return

        pocket_cmd()
        return


# ==================== Markdown Commands ====================
@cli.group(name="markdown")
def markdown_group():
    """Markdown rendering and conversion tools."""
    pass


@markdown_group.command(name="render")
@click.argument('file', type=click.Path(exists=True))
@click.option('--width', '-w', type=int, help='Output width in characters.')
def markdown_render(file: str, width: int):
    """
    Render a Markdown file beautifully in the terminal.

    This command reads a Markdown file and displays it with enhanced formatting,
    syntax highlighting, and beautiful terminal rendering using the Rich library.

    Args:
        file: Path to the Markdown file to render.
        width: Optional output width in characters for wrapping.

    Examples:
        pocket markdown render README.md
        pocket markdown render docs/guide.md -w 100
    """

    # Call the markd function with the file
    ctx = click.Context(markd)
    ctx.invoke(markd, file=Path(file), output=None, input=None)


# ==================== Project Commands ====================
@cli.group(name="project")
def project_group():
    """Project management and export tools."""
    pass


@project_group.command(name="to-file")
@click.option(
    '-p', '--path',
    default='.',
    help='Root directory of the project to scan.'
)
@click.option(
    '-o', '--output',
    default=None,
    help='Output Markdown file name.'
)
@click.option(
    '-e', '--exclude',
    default=".AGENTS,Agents,AGENTS.md,.claude,.cursor,WORKFLOWS.md,RULES.md,env,.env,venv,.venv,.gitignore,.git,.vscode,.idea,lib,bin,site-packages,node_modules,__pycache__,.DS_Store",
    help='Comma-separated list of files/directories to exclude.'
)
def project_to_file(path: str, output: str, exclude: str):
    """
    Export entire project to a single Markdown file.

    This command scans a project directory and generates a single Markdown
    file containing the file tree structure and all source code with syntax
    highlighting. Useful for documentation, code reviews, or AI analysis.

    Args:
        path: Root directory of the project to scan (default: current directory).
        output: Name of the output Markdown file (default: <project_name>-1-file.md).
        exclude: Comma-separated list of files/directories to exclude from export.

    Examples:
        pocket project to-file
        pocket project to-file -p ./my-project -o export.md
        pocket project to-file -e "node_modules,dist,build"
    """

    create_codebase_markdown(path, output, exclude)


@project_group.command(name="readme")
@click.option(
    '-p', '--path',
    default='.',
    help='Root directory of the project to scan.'
)
@click.option(
    '-o', '--output',
    default=None,
    help='Output README file path (defaults to <project_root>/README.md).'
)
def project_readme(path: str, output: str | None):
    """Interactively generate a README.md for a project.

    This command scans the target project to infer its languages, dependencies,
    frameworks and a likely project type. It then runs an interactive wizard
    to build a relevant README.md, asking the user a few questions to
    customize the final content.

    Args:
        path: Root directory of the project to scan (default: current directory).
        output: Optional explicit README path; default is README.md in project root.

    Examples:
        pocket project readme
        pocket project readme -p ./my-project
        pocket project readme -p ./my-project -o ./docs/README.md
    """

    run_readme_wizard(path, output)

@project_group.command(name="req-to-date")
@click.argument("packages", nargs=-1)
def req_to_date(packages: tuple[str, ...]):
    """Accepte `nom==version`, une liste séparée par des virgules ou un fichier requirements."""

    if not packages:
        raise click.BadParameter(
            "Fournissez au moins un package, une liste séparée par des virgules ou un fichier requirements.txt.",
            ctx=click.get_current_context(),
            param_hint="packages"
        )

    try:
        results = run_req_to_date(packages)
    except ValueError as exc:
        raise click.BadParameter(str(exc))

    outdated_count = 0
    for result in results:
        if result.latest_overall and result.current_version != result.latest_overall:
            console.print(
                f"[red]{result.package} ({result.current_version})[/red] -> "
                f"[green]{result.latest_overall}[/green]"
            )
            outdated_count += 1

    if outdated_count == 0:
        console.print("[green]All packages are up to date[/green]")
    print_req_to_date_results(
        results,
        lambda result: console.print(
            f"{result.package} [red]{result.current_version}[/red] -> "
            f"[green]{result.latest_overall}[/green]",
            style="bold",
            justify="center",
        ),
    )

project_group.add_command(init_group)
# ==================== Templates Commands ====================
@cli.group(name="templates")
def templates_group():
    """Manage agent templates and development cheatsheets."""
    pass


@templates_group.command(name="list")
@click.option(
    '--type', '-t',
    type=click.Choice(['templates', 'cheatsheets', 'all'], case_sensitive=False),
    default='all',
    help='Type of items to list.'
)
def templates_list(type: str):
    """
    List available templates and cheatsheets.

    Displays a formatted table showing all available templates and/or cheatsheets
    with their names and descriptions.

    Args:
        type: Filter by type - 'templates', 'cheatsheets', or 'all' (default: all).

    Examples:
        pocket templates list
        pocket templates list --type templates
        pocket templates list -t cheatsheets
    """

    ctx = click.Context(list_items)
    ctx.invoke(list_items, type=type)


@templates_group.command(name="view")
@click.argument('name', type=str)
@click.option(
    '--type', '-t',
    type=click.Choice(['template', 'cheatsheet'], case_sensitive=False),
    help='Type of item to view.'
)
def templates_view(name: str, type: str):
    """
    View a template or cheatsheet in the terminal.

    Renders the template or cheatsheet content with Markdown formatting
    directly in the terminal for quick reference.

    Args:
        name: Name of the template or cheatsheet (without .md extension).
        type: Type of item to view - 'template' or 'cheatsheet' (auto-detected if omitted).

    Examples:
        pocket templates view unit_tests_agent
        pocket templates view SQL -t cheatsheet
    """

    ctx = click.Context(view_item)
    ctx.invoke(view_item, name=name, type=type)


@templates_group.command(name="copy")
@click.argument('name', type=str)
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output path for the copied file.'
)
@click.option(
    '--type', '-t',
    type=click.Choice(['template', 'cheatsheet'], case_sensitive=False),
    help='Type of item to copy.'
)
@click.option(
    '--force', '-f',
    is_flag=True,
    help='Overwrite existing file.'
)
def templates_copy(name: str, output: str, type: str, force: bool):
    """
    Copy a template or cheatsheet to your project.

    Copies the specified template or cheatsheet file to a destination in your
    project. Creates parent directories if they don't exist.

    Args:
        name: Name of the template or cheatsheet (without .md extension).
        output: Output path (file or directory) for the copied file.
        type: Type of item to copy - 'template' or 'cheatsheet' (auto-detected if omitted).
        force: If True, overwrite existing file without confirmation.

    Examples:
        pocket templates copy unit_tests_agent -o .agents/
        pocket templates copy SQL -o docs/cheatsheets/
    """
    output_path = Path(output) if output else None

    ctx = click.Context(copy_item)
    ctx.invoke(copy_item, name=name, output=output_path, type=type, force=force)


@templates_group.command(name="init")
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Directory for agent templates.'
)
def templates_init(output: str):
    """
    Initialize agent configuration directory with all templates.

    Creates a directory and copies all available agent templates into it.
    Useful for quickly setting up agent configurations in a new project.

    Args:
        output: Directory where agent templates will be copied (default: .AGENTS).

    Examples:
        pocket templates init
        pocket templates init -o ./agents/
    """     
    output_path = Path(output) if output else Path.cwd() / ".AGENTS"

    ctx = click.Context(init_agents)
    ctx.invoke(init_agents, output=output_path)


# ==================== PDF Commands ====================
@cli.group(name="pdf")
def pdf_group():
    """PDF conversion tools."""
    pass


@pdf_group.command(name="convert")
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '-o', '--output',
    type=click.Path(),
    help='Output PDF file path.'
)
def pdf_convert_cmd(input_file: str, output: str):
    """
    Convert text or Markdown files to PDF.

    Converts plain text (.txt) or Markdown (.md) files to PDF format.
    Output file defaults to input filename with .pdf extension.

    Args:
        input_file: Path to the input file (.txt or .md).
        output: Optional output PDF file path (default: <input_file>.pdf).

    Examples:
        pocket pdf convert document.txt
        pocket pdf convert README.md -o output.pdf
    """
    output_path = Path(output) if output else None

    ctx = click.Context(pdf_convert)
    ctx.invoke(pdf_convert, input_file=Path(input_file), output=output_path)


# ==================== Web Commands ====================
@cli.group(name="web")
def web_group():
    """Web utilities."""
    pass


@web_group.command(name="job-search")
@click.argument("query")
@click.option("-p", "--page", type=int, default=1, help="Page number to start from")
@click.option("-n", "--num_pages", type=int, default=10, help="Number of pages to scrape")
@click.option("-c", "--country", type=str, default="fr", help="Country to search in")
@click.option("-l", "--language", type=str, default="fr", help="Language to search in")
@click.option("-d", "--date_posted", type=str, default="month", help="Date posted to search for. Possible values: all, today, 3days, week, month")
@click.option("-t", "--employment_types", type=str, default="FULLTIME", help="Employment types to search for. Possible values: FULLTIME, CONTRACTOR, PARTTIME, INTERN")
@click.option("-r", "--job_requirements", type=str, default="no_experience", help="Job requirements to search for")
@click.option("--work_from_home", is_flag=True, default=False, help="Search for jobs that allow working from home")
@click.option("-o", "--output", type=str, default="jobs.json", help="Output file name")
def web_job_search_cmd(query: str, page: int, num_pages: int, country: str, language: str, date_posted: str, employment_types: str, job_requirements: str, work_from_home: bool, output: str):
    """
    Search for jobs using the JSearch API.

    Searches for jobs based on query and saves results to a JSON file.
    Requires RAPIDAPI_API_KEY environment variable to be set.

    Args:
        query: Search query for jobs (e.g., "Python developer").
        page: Page number to start from (default: 1).
        num_pages: Number of pages to scrape (default: 10).
        country: Country to search in (default: fr).
        language: Language to search in (default: fr).
        date_posted: Date posted filter (default: month).
        employment_types: Employment types (default: FULLTIME).
        job_requirements: Job requirements (default: no_experience).
        output: Output JSON file name (default: jobs.json).

    Examples:
        pocket web job-search "Python developer"
        pocket web job-search "Data scientist" -c us -l en -o data_jobs.json
    """
    ctx = click.Context(job_search)
    ctx.invoke(job_search, query=query, page=page, num_pages=num_pages,
               country=country, language=language, date_posted=date_posted,
               employment_types=employment_types, job_requirements=job_requirements,
               work_from_home=work_from_home, output=output)


@web_group.command(name="favicon")
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '-o', '--output',
    type=click.Path(),
    help='Output favicon file path.'
)
@click.option(
    '--sizes',
    type=str,
    help='Custom sizes (e.g., "64x64,32x32,16x16")'
)
def web_favicon_cmd(input_file: str, output: str, sizes: str):
    """
    Convert an image to a favicon (.ico) file.

    Generates a multi-size .ico favicon file from any image format.
    Includes standard sizes for optimal browser compatibility.

    Args:
        input_file: Path to the input image file (PNG, JPG, etc.).
        output: Optional output .ico file path (default: favicon.ico).
        sizes: Custom sizes as comma-separated WxH values (e.g., "64x64,32x32").

    Examples:
        pocket web favicon logo.png
        pocket web favicon logo.png -o custom-favicon.ico
        pocket web favicon logo.png --sizes "64x64,32x32"
    """
    output_path = Path(output) if output else None

    ctx = click.Context(favicon_convert)
    ctx.invoke(favicon_convert, input_file=Path(input_file), output=output_path, sizes=sizes)


# ==================== README Commands ====================
cli.add_command(readme_cli, name="readme")

# ==================== XML Commands ====================
cli.add_command(xml_cmd, name="xml")


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
