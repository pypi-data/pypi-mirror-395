"""Tests for badge generator."""

import pytest
from pathlib import Path
from super_pocket.readme.badges import BadgeGenerator, BadgeType
from super_pocket.readme.models import ProjectContext, ProjectType


@pytest.fixture
def python_context():
    """Create a Python project context."""
    return ProjectContext(
        project_name="test-project",
        project_path=Path("/test"),
        language="python",
        project_type=ProjectType.CLI_TOOL,
        runtime_version=">=3.11",
        license_type="MIT"
    )


def test_badge_generator_available_badges(python_context):
    """Test getting available badges for a project."""
    generator = BadgeGenerator()
    badges = generator.get_available_badges(python_context)

    assert BadgeType.PYTHON_VERSION in badges
    assert BadgeType.LICENSE in badges


def test_badge_generator_python_version(python_context):
    """Test generating Python version badge."""
    generator = BadgeGenerator()
    markdown = generator.generate_badge(BadgeType.PYTHON_VERSION, python_context)

    assert "python-3.11" in markdown
    assert "badge" in markdown
    assert "shields.io" in markdown


def test_badge_generator_license_badge(python_context):
    """Test generating license badge."""
    generator = BadgeGenerator()
    markdown = generator.generate_badge(BadgeType.LICENSE, python_context)

    assert "MIT" in markdown
    assert "badge" in markdown


def test_badge_generator_skips_unavailable(python_context):
    """Test that unavailable badges return None."""
    python_context.has_ci = False
    generator = BadgeGenerator()

    # CI badge should not be available
    badges = generator.get_available_badges(python_context)
    assert BadgeType.BUILD_STATUS not in badges
