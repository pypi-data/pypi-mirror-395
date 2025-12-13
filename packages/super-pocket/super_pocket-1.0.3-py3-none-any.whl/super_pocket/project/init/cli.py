"""
CLI commands for project initialization.

Provides Click commands for listing, showing, and initializing projects
from templates.
"""
from super_pocket.settings import (
    click,
    CONTEXT_SETTINGS,
    add_help_command,
    centered_spinner,
    display_logo
)
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.live import Live
from super_pocket.utils import print_error
from .manifest import parse_manifest
from .engine import ProjectGenerator
from .interactive import customize_interactively
from .validation import (
    validate_project_name,
    validate_output_path,
    validate_template_name,
    ValidationError
)


console = Console()


def list_templates(templates_dir: Path) -> list[dict]:
    """
    List all available templates.

    Args:
        templates_dir: Directory containing template manifests

    Returns:
        List of template info dicts
    """
    display_logo()
    with Live(centered_spinner("Loading templates..."), refresh_per_second=20, transient=True):
        templates = []
        for manifest_file in templates_dir.glob("*.yaml"):
            try:
                manifest = parse_manifest(manifest_file)
                templates.append({
                    "name": manifest.name,
                    "display_name": manifest.display_name,
                    "description": manifest.description
                })
            except Exception as e:
                print_error(e, custom=True, message=f"Error loading {manifest_file.name}")

    display_logo()
    return templates


@click.group(name="init", context_settings=CONTEXT_SETTINGS)
def init_group():
    """Initialize new projects from templates."""
    pass


@init_group.command(name="list", context_settings=CONTEXT_SETTINGS)
def list_cmd():
    """List available project templates."""
    templates_dir = Path(__file__).parent.parent / "templates"
    templates = list_templates(templates_dir)

    if not templates:
        display_logo()
        console.print("[yellow]No templates found[/yellow]", justify="center")
        return

    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Display Name", style="green")
    table.add_column("Description")

    for template in templates:
        table.add_row(
            template["name"],
            template["display_name"],
            template["description"]
        )

    console.print(table)


@init_group.command(name="show", context_settings=CONTEXT_SETTINGS)
@click.argument("template_name")
def show_cmd(template_name: str):
    """Show details of a specific template."""
    templates_dir = Path(__file__).parent.parent / "templates"
    manifest_path = templates_dir / f"{template_name}.yaml"

    if not manifest_path.exists():
        console.print(f"[red]Template not found: {template_name}[/red]")
        return

    try:
        manifest = parse_manifest(manifest_path)

        console.print(f"\n[bold cyan]{manifest.display_name}[/bold cyan]")
        console.print(f"{manifest.description}\n")
        console.print(f"Python version: {manifest.python_version}")

        if manifest.tool_choices:
            console.print("\n[bold]Tool Choices:[/bold]")
            for key, choice in manifest.tool_choices.items():
                console.print(f"  {choice.prompt}")
                for option in choice.options:
                    default = " (default)" if option.name == choice.default else ""
                    console.print(f"    - {option.name}: {option.description}{default}")

        if manifest.features:
            console.print("\n[bold]Features:[/bold]")
            for feature in manifest.features:
                default = "✓" if feature.default else "✗"
                console.print(f"  [{default}] {feature.description}")

    except Exception as e:
        print_error(e, custom=True, message="Error loading template")
        raise


@init_group.command(context_settings=CONTEXT_SETTINGS)
@click.argument("template_name")
@click.option("--path", "-p", type=click.Path(), help="Output directory")
@click.option("--quick", "-q", is_flag=True, help="Use defaults without prompting")
def new(template_name: str, path: str | None, quick: bool):
    """
    Initialize a new project from a template.

    Args:
        template_name: Name of the template to use
        path: Output directory (defaults to ./<project_name>)
        quick: Use default selections without prompting
    """
    templates_dir = Path(__file__).parent.parent / "templates"
    manifest_path = templates_dir / f"{template_name}.yaml"

    try:
        # Validate template name
        available_templates = list_templates(templates_dir)
        available_names = [t['name'] for t in available_templates]
        validate_template_name(template_name, available_names)

        # Load manifest
        manifest = parse_manifest(manifest_path)

        # Get user customization
        project_name, description, tool_sel, feat_sel = customize_interactively(
            manifest, quick=quick
        )

        # Validate project name
        try:
            validate_project_name(project_name)
        except ValidationError as e:
            print_error(e, custom=True, message="Invalid project name")
            raise click.Abort()

        # Determine output path
        if path:
            output_path = Path(path)
        else:
            output_path = Path.cwd() / project_name

        # Validate output path
        try:
            validate_output_path(output_path, allow_existing=False)
        except ValidationError as e:
            print_error(e, custom=True, message="Invalid output path")
            raise click.Abort()

        # Generate project
        with Live(centered_spinner("Generating project..."), refresh_per_second=20, transient=True):

            generator = ProjectGenerator(
                manifest=manifest,
                project_name=project_name,
                output_path=output_path
            )
            generator.set_selections(tool_sel, feat_sel, description)

            results = generator.generate()

        # Display results
        success_count = sum(1 for r in results if r.success)
        console.print(f"\n[green]✓ Generated {success_count} items successfully[/green]")

        # Show any errors
        errors = [r for r in results if not r.success]
        if errors:
            console.print(f"\n[yellow]Warnings/Errors:[/yellow]")
            for error in errors:
                console.print(f"  [red]✗[/red] {error.message}")
                if error.error:
                    console.print(f"    {error.error}")

        console.print(f"\n[bold green]Project created successfully![/bold green]")
        console.print(f"Location: {output_path}")

    except ValidationError as e:
        print_error(e, custom=True, message="Validation Error")
        raise
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
    except Exception as e:
        print_error(e, custom=True, message="Error")
        raise


# Add 'help' subcommand to the group
add_help_command(init_group)