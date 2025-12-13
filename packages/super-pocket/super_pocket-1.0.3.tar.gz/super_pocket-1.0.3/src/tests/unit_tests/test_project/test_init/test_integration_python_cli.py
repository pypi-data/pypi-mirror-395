"""
Integration tests for python-cli template.

Tests the complete project generation workflow for the python-cli template,
including different tool choices and feature combinations.
"""
import pytest
from pathlib import Path
import shutil
import tempfile

from super_pocket.project.init.manifest import parse_manifest
from super_pocket.project.init.engine import ProjectGenerator


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test output"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def template_base_path():
    """Path to template directory"""
    return Path(__file__).parent.parent.parent.parent.parent / "super_pocket" / "project" / "templates"


@pytest.fixture
def manifest(template_base_path):
    """Load python-cli manifest"""
    manifest_path = template_base_path / "python-cli.yaml"
    return parse_manifest(manifest_path)


def test_python_cli_quick_mode(temp_output_dir, template_base_path, manifest):
    """Test python-cli template in quick mode (all defaults)"""
    project_name = "test_cli"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Use default selections (quick mode)
    tool_selections = {
        choice_name: choice.default
        for choice_name, choice in manifest.tool_choices.items()
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Test CLI project")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name).exists()
    assert (project_path / "src" / project_name / "cli.py").exists()
    assert (project_path / "src" / project_name / "__init__.py").exists()
    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / ".gitignore").exists()

    # Verify default selections (click + uv + rich_output + testing)
    cli_content = (project_path / "src" / project_name / "cli.py").read_text()
    assert "click" in cli_content  # Default is click

    # Verify tests directory exists (default testing=true)
    assert (project_path / "tests").exists()
    assert (project_path / "tests" / "test_cli.py").exists()

    # Verify all critical results succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results), f"Some file operations failed: {[r.message for r in file_results if not r.success]}"


def test_python_cli_with_typer(temp_output_dir, template_base_path, manifest):
    """Test python-cli template with Typer framework"""
    project_name = "test_typer_cli"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select typer
    tool_selections = {
        "cli_framework": "typer",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Test Typer CLI")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "cli.py").exists()

    # Verify typer is used
    cli_content = (project_path / "src" / project_name / "cli.py").read_text()
    assert "typer" in cli_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_python_cli_with_argparse(temp_output_dir, template_base_path, manifest):
    """Test python-cli template with argparse framework"""
    project_name = "test_argparse_cli"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select argparse
    tool_selections = {
        "cli_framework": "argparse",
        "package_manager": "pip"
    }
    feature_selections = {
        feature.name: False  # Disable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Test argparse CLI")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "cli.py").exists()

    # Verify argparse is used
    cli_content = (project_path / "src" / project_name / "cli.py").read_text()
    assert "argparse" in cli_content.lower()

    # Verify tests directory does NOT exist (testing disabled)
    assert not (project_path / "tests").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_python_cli_with_poetry(temp_output_dir, template_base_path, manifest):
    """Test python-cli template with Poetry package manager"""
    project_name = "test_poetry_cli"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select poetry
    tool_selections = {
        "cli_framework": "click",
        "package_manager": "poetry"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Test Poetry CLI")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "pyproject.toml").exists()

    # Verify pyproject.toml contains poetry config
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert "poetry" in pyproject_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_python_cli_with_all_features(temp_output_dir, template_base_path, manifest):
    """Test python-cli template with all features enabled"""
    project_name = "test_full_cli"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable all features
    tool_selections = {
        "cli_framework": "click",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: True  # Enable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Full-featured CLI")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()

    # Verify all feature-specific files exist
    assert (project_path / "tests").exists()  # testing
    assert (project_path / ".github" / "workflows" / "ci.yml").exists()  # github_actions
    assert (project_path / "Dockerfile").exists()  # docker

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_python_cli_readme_content(temp_output_dir, template_base_path, manifest):
    """Test that README contains expected content"""
    project_name = "test_readme_cli"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    description = "My awesome CLI tool"
    tool_selections = {
        choice_name: choice.default
        for choice_name, choice in manifest.tool_choices.items()
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, description)
    results = generator.generate()

    # Verify README exists and contains project info
    readme_path = project_path / "README.md"
    assert readme_path.exists()

    readme_content = readme_path.read_text()
    assert project_name in readme_content or project_name.replace("_", " ") in readme_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_python_cli_no_features(temp_output_dir, template_base_path, manifest):
    """Test python-cli template with no features enabled"""
    project_name = "test_minimal_cli"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Disable all features
    tool_selections = {
        "cli_framework": "argparse",
        "package_manager": "pip"
    }
    feature_selections = {
        feature.name: False  # Disable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Minimal CLI")
    results = generator.generate()

    # Verify basic structure exists
    assert project_path.exists()
    assert (project_path / "src" / project_name / "cli.py").exists()

    # Verify optional files do NOT exist
    assert not (project_path / "tests").exists()
    assert not (project_path / ".github").exists()
    assert not (project_path / "Dockerfile").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)
