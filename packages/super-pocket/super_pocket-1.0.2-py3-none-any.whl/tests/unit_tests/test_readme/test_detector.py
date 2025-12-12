"""Tests for main project detector."""

import pytest
from pathlib import Path
from super_pocket.readme.detector import ProjectDetector
from super_pocket.readme.models import ProjectType


@pytest.fixture
def python_project(tmp_path):
    """Create a temporary Python project."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-project"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = ["click>=8.0.0"]

[project.scripts]
test = "test.main:cli"
""")
    return tmp_path


def test_detector_finds_python_project(python_project):
    """Test detector successfully identifies Python project."""
    detector = ProjectDetector()
    context = detector.detect(python_project)

    assert context is not None
    assert context.language == "python"
    assert context.project_type == ProjectType.CLI_TOOL


def test_detector_returns_none_for_unknown(tmp_path):
    """Test detector returns None for unrecognized projects."""
    detector = ProjectDetector()
    context = detector.detect(tmp_path)

    assert context is None


def test_detector_uses_multiple_analyzers(python_project):
    """Test that detector tries multiple analyzers."""
    detector = ProjectDetector()
    # Should try all analyzers but find Python
    context = detector.detect(python_project)

    assert context.language == "python"
