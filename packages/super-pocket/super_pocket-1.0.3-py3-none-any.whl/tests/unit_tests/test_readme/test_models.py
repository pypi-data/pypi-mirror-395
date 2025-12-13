"""Tests for README generator data models."""

import pytest
from pathlib import Path
from super_pocket.readme.models import ProjectContext, ProjectType


def test_project_context_creation():
    """Test creating a ProjectContext with basic data."""
    context = ProjectContext(
        project_name="test-project",
        project_path=Path("/test/path"),
        language="python",
        project_type=ProjectType.CLI_TOOL
    )

    assert context.project_name == "test-project"
    assert context.language == "python"
    assert context.project_type == ProjectType.CLI_TOOL


def test_project_context_with_optional_fields():
    """Test ProjectContext with optional fields."""
    context = ProjectContext(
        project_name="test-project",
        project_path=Path("/test/path"),
        language="python",
        project_type=ProjectType.WEB_APP,
        framework="fastapi",
        package_manager="uv",
        license_type="MIT"
    )

    assert context.framework == "fastapi"
    assert context.package_manager == "uv"
    assert context.license_type == "MIT"


def test_project_type_enum_values():
    """Test ProjectType enum has expected values."""
    assert ProjectType.CLI_TOOL.value == "cli"
    assert ProjectType.WEB_APP.value == "web_app"
    assert ProjectType.LIBRARY.value == "library"
    assert ProjectType.API.value == "api"
