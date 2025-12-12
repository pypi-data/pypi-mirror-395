"""
Template rendering with Jinja2.

Provides context building and template rendering functionality.
"""
from pathlib import Path
from jinja2 import Template


def build_context(
    project_name: str,
    description: str,
    tool_choices: dict[str, str],
    features: dict[str, bool],
    python_version: str
) -> dict:
    """
    Build Jinja2 context from user selections.

    Args:
        project_name: Project name in snake_case
        description: Project description
        tool_choices: Dict mapping choice category to selected option
        features: Dict mapping feature name to enabled/disabled
        python_version: Python version requirement

    Returns:
        Context dictionary for Jinja2 rendering
    """
    # Convert snake_case to Title Case for display name
    # Special handling for common abbreviations
    words = []
    for word in project_name.split("_"):
        # Keep common abbreviations uppercase
        if word.upper() in ["CLI", "API", "HTTP", "HTTPS", "SQL", "DB", "ID", "URL", "UI", "UX"]:
            words.append(word.upper())
        else:
            words.append(word.capitalize())
    display_name = " ".join(words)

    return {
        "project_name": project_name,
        "project_display_name": display_name,
        "description": description,
        "tool_choices": tool_choices,
        "features": features,
        "python_version": python_version,
    }


def render_template_string(template_str: str, context: dict) -> str:
    """
    Render a Jinja2 template string with context.

    Args:
        template_str: Jinja2 template as string
        context: Context dictionary

    Returns:
        Rendered string
    """
    template = Template(template_str)
    return template.render(**context)


def render_template_file(template_path: Path, context: dict) -> str:
    """
    Render a Jinja2 template file with context.

    Args:
        template_path: Path to template file
        context: Context dictionary

    Returns:
        Rendered string

    Raises:
        FileNotFoundError: If template file doesn't exist
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, 'r') as f:
        template_str = f.read()

    return render_template_string(template_str, context)
