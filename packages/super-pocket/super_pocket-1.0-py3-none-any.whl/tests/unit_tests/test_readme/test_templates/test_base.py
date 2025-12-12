"""Tests for base README templates."""

import pytest
from pathlib import Path
from super_pocket.readme.templates.base import (
    TitleSection,
    PrerequisitesSection,
    InstallationSection
)
from super_pocket.readme.models import ProjectContext, ProjectType


@pytest.fixture
def python_cli_context():
    """Create a Python CLI project context."""
    return ProjectContext(
        project_name="test-cli",
        project_path=Path("/test"),
        language="python",
        project_type=ProjectType.CLI_TOOL,
        description="A test CLI tool",
        runtime_version=">=3.11",
        package_manager="uv",
        dependencies=["click>=8.0.0"]
    )


def test_title_section_generation(python_cli_context):
    """Test title section generation."""
    section = TitleSection()
    content = section.generate(python_cli_context)

    assert "# test-cli" in content
    assert "A test CLI tool" in content


def test_prerequisites_section(python_cli_context):
    """Test prerequisites section generation."""
    section = PrerequisitesSection()
    content = section.generate(python_cli_context)

    assert "## Prerequisites" in content
    assert "Python 3.11" in content or ">=3.11" in content


def test_installation_section(python_cli_context):
    """Test installation section generation."""
    section = InstallationSection()
    content = section.generate(python_cli_context)

    assert "## Installation" in content
    assert "uv sync" in content or "pip install" in content
    assert "```bash" in content
