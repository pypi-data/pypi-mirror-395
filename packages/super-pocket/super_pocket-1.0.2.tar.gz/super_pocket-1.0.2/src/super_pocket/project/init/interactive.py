"""
Interactive UI for project customization.

Provides interactive prompts for tool choices and feature selection
using Rich for beautiful terminal output.
"""
from typing import Tuple
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from .manifest import TemplateManifest
from .validation import validate_project_name, ValidationError


console = Console()


def get_default_selections(manifest: TemplateManifest) -> Tuple[dict[str, str], dict[str, bool]]:
    """
    Get default selections from manifest.

    Args:
        manifest: Template manifest

    Returns:
        Tuple of (tool_selections, feature_selections)
    """
    tool_selections = {
        key: choice.default
        for key, choice in manifest.tool_choices.items()
    }

    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    return tool_selections, feature_selections


def prompt_project_info() -> Tuple[str, str]:
    """
    Prompt for project name and description with validation.

    Returns:
        Tuple of (project_name, description)
    """
    console.print("\n[bold cyan]Project Information[/bold cyan]")

    # Prompt for project name with validation loop
    while True:
        project_name = Prompt.ask(
            "Project name (letters, numbers, underscores, hyphens)",
            default="my_project"
        )

        # Try to validate the project name
        try:
            validate_project_name(project_name)
            break  # Valid name, exit loop
        except ValidationError as e:
            console.print(f"[red]{e}[/red]")
            console.print("Please try again with a valid project name.")

    description = Prompt.ask(
        "Project description",
        default="A new project"
    )

    return project_name, description


def prompt_tool_choices(manifest: TemplateManifest) -> dict[str, str]:
    """
    Prompt user to select tools for each choice category.

    Args:
        manifest: Template manifest

    Returns:
        Dict mapping choice category to selected option
    """
    selections = {}

    if not manifest.tool_choices:
        return selections

    console.print("\n[bold cyan]Tool Choices[/bold cyan]")

    for key, choice in manifest.tool_choices.items():
        console.print(f"\n[yellow]{choice.prompt}[/yellow]")

        # Create options display
        for i, option in enumerate(choice.options, 1):
            default_marker = " [dim](default)[/dim]" if option.name == choice.default else ""
            console.print(f"  {i}. {option.name} - {option.description}{default_marker}")

        # Prompt for selection
        selection = Prompt.ask(
            "Select option",
            choices=[str(i) for i in range(1, len(choice.options) + 1)],
            default="1"
        )
        idx = int(selection) - 1
        selected = choice.options[idx].name

        selections[key] = selected

    return selections


def prompt_features(manifest: TemplateManifest) -> dict[str, bool]:
    """
    Prompt user to enable/disable features.

    Args:
        manifest: Template manifest

    Returns:
        Dict mapping feature name to enabled/disabled
    """
    selections = {}

    if not manifest.features:
        return selections

    console.print("\n[bold cyan]Features[/bold cyan]")

    for feature in manifest.features:
        default = "Y" if feature.default else "n"
        response = Confirm.ask(
            f"{feature.description}",
            default=feature.default
        )
        selections[feature.name] = response

    return selections


def customize_interactively(
    manifest: TemplateManifest,
    quick: bool = False
) -> Tuple[str, str, dict[str, str], dict[str, bool]]:
    """
    Run interactive customization flow.

    Args:
        manifest: Template manifest
        quick: If True, use defaults without prompting

    Returns:
        Tuple of (project_name, description, tool_selections, feature_selections)
    """
    # Display header
    panel = Panel(
        f"[bold]{manifest.display_name}[/bold]\n{manifest.description}",
        title="Template",
        border_style="cyan"
    )
    console.print(panel)

    if quick:
        # Use defaults
        project_name = "my_project"
        description = manifest.description
        tool_selections, feature_selections = get_default_selections(manifest)
    else:
        # Interactive prompts
        project_name, description = prompt_project_info()
        tool_selections = prompt_tool_choices(manifest)
        feature_selections = prompt_features(manifest)

    # Display summary
    console.print("\n[bold green]Configuration Summary[/bold green]")
    console.print(f"Project: {project_name}")
    console.print(f"Description: {description}")

    if tool_selections:
        console.print("\nTool Choices:")
        for key, value in tool_selections.items():
            console.print(f"  {key}: {value}")

    if feature_selections:
        console.print("\nFeatures:")
        for key, value in feature_selections.items():
            status = "[green]✓[/green]" if value else "[red]✗[/red]"
            console.print(f"  {status} {key}")

    if not quick:
        proceed = Confirm.ask("\nProceed with generation?", default=True)
        if not proceed:
            console.print("[yellow]Cancelled[/yellow]")
            raise KeyboardInterrupt("User cancelled")

    return project_name, description, tool_selections, feature_selections
