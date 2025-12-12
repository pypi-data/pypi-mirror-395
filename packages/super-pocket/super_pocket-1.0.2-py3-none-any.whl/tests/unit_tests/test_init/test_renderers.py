"""Tests for template rendering."""
import pytest
import tempfile
from pathlib import Path
from super_pocket.project.init.renderers import build_context


def test_build_context():
    """Test building Jinja2 context from selections."""
    tool_choices = {
        "cli_framework": "click",
        "package_manager": "uv"
    }
    features = {
        "testing": True,
        "docker": False
    }

    context = build_context(
        project_name="my_awesome_cli",
        description="A CLI tool",
        tool_choices=tool_choices,
        features=features,
        python_version=">=3.11"
    )

    assert context["project_name"] == "my_awesome_cli"
    assert context["project_display_name"] == "My Awesome CLI"
    assert context["description"] == "A CLI tool"
    assert context["tool_choices"]["cli_framework"] == "click"
    assert context["features"]["testing"] is True
    assert context["features"]["docker"] is False


def test_render_template_string():
    """Test rendering a template string."""
    from super_pocket.project.init.renderers import render_template_string

    template = "Hello {{ name }}!"
    context = {"name": "World"}
    result = render_template_string(template, context)
    assert result == "Hello World!"


def test_render_template_with_conditionals():
    """Test rendering with conditional logic."""
    from super_pocket.project.init.renderers import render_template_string

    template = """
{% if features.testing %}
import pytest
{% endif %}

def main():
    pass
"""
    context = {"features": {"testing": True}}
    result = render_template_string(template, context)
    assert "import pytest" in result


def test_render_template_file():
    """Test rendering a template file."""
    from super_pocket.project.init.renderers import render_template_file

    # Create a temporary template file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.j2', delete=False) as f:
        f.write("Project: {{ project_name }}\nVersion: {{ version }}")
        template_path = Path(f.name)

    try:
        context = {"project_name": "test_project", "version": "1.0.0"}
        result = render_template_file(template_path, context)
        assert "Project: test_project" in result
        assert "Version: 1.0.0" in result
    finally:
        template_path.unlink()  # Clean up temp file
