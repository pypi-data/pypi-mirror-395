"""CLI commands for README generator."""

from super_pocket.settings import click, CONTEXT_SETTINGS, add_help_command
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .detector import ProjectDetector
from .generator import ReadmeGenerator

console = Console()


@click.group(context_settings=CONTEXT_SETTINGS)
def readme_cli():
    """README generator commands."""
    pass


@readme_cli.command("analyze", context_settings=CONTEXT_SETTINGS)
@click.argument("path", type=click.Path(exists=True), default=".")
def analyze_command(path: str):
    """
    Analyze a project and show detection results.

    Args:
        path: Project directory path (default: current directory)
    """
    project_path = Path(path).resolve()

    detector = ProjectDetector()
    context = detector.detect(project_path)

    if context is None:
        console.print("[red]Could not detect project type.[/red]")
        console.print("No recognized project files found (pyproject.toml, package.json, etc.)")
        raise click.Abort()

    # Display detection results
    table = Table(title="Project Analysis")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Name", context.project_name)
    table.add_row("Language", context.language.title())
    table.add_row("Project Type", context.project_type.value.replace("_", " ").title())

    if context.framework:
        table.add_row("Framework", context.framework)
    if context.runtime_version:
        table.add_row("Runtime Version", context.runtime_version)
    if context.package_manager:
        table.add_row("Package Manager", context.package_manager)

    console.print(table)

    if context.dependencies:
        console.print(f"\n[cyan]Dependencies:[/cyan] {len(context.dependencies)} found")


@readme_cli.command("generate", context_settings=CONTEXT_SETTINGS)
@click.option("--output", "-o", default="README.md", help="Output file path")
@click.option("--path", "-p", type=click.Path(exists=True), default=".", help="Project directory")
def generate_command(output: str, path: str):
    """
    Generate a README file for the project.

    Args:
        output: Output file path
        path: Project directory path
    """
    project_path = Path(path).resolve()
    output_path = Path(output)

    # Detect project
    detector = ProjectDetector()
    context = detector.detect(project_path)

    if context is None:
        console.print("[red]Could not detect project type.[/red]")
        raise click.Abort()

    console.print(f"[cyan]Detected:[/cyan] {context.language.title()} {context.project_type.value}")

    # Generate README (minimal for now - no interactivity yet)
    generator = ReadmeGenerator()
    content = generator.generate(context, selected_badges=[], selected_sections=[])

    # Write to file
    output_path.write_text(content)
    console.print(f"[green]✓[/green] README generated: {output_path}")


# Add 'help' subcommand to the group
add_help_command(readme_cli)


if __name__ == "__main__":
    readme_cli()
