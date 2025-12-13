"""Tests for README generator core."""

import pytest
from pathlib import Path
from super_pocket.readme.generator import ReadmeGenerator
from super_pocket.readme.models import ProjectContext, ProjectType


@pytest.fixture
def python_context():
    """Create a Python project context."""
    return ProjectContext(
        project_name="test-project",
        project_path=Path("/test"),
        language="python",
        project_type=ProjectType.CLI_TOOL,
        description="A test project",
        runtime_version=">=3.11",
        package_manager="uv"
    )


def test_generator_creates_readme(python_context):
    """Test that generator creates README content."""
    generator = ReadmeGenerator()
    content = generator.generate(python_context, selected_badges=[], selected_sections=[])

    assert "# test-project" in content
    assert "A test project" in content


def test_generator_includes_baseline_sections(python_context):
    """Test that baseline sections are always included."""
    generator = ReadmeGenerator()
    content = generator.generate(python_context, selected_badges=[], selected_sections=[])

    # Baseline sections
    assert "# test-project" in content  # Title
    assert "Prerequisites" in content
    assert "Installation" in content


def test_generator_includes_optional_sections(python_context):
    """Test that optional sections are included when requested."""
    generator = ReadmeGenerator()
    content = generator.generate(
        python_context,
        selected_badges=[],
        selected_sections=["running-tests"]
    )

    assert "Running Tests" in content or "Tests" in content
