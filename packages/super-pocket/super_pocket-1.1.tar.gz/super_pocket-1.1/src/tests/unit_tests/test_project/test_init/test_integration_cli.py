"""
Integration tests for project init CLI commands.

Tests the complete CLI workflow using Click's CliRunner, including:
- pocket project init list
- pocket project init show <template>
- pocket project init new <template>
"""
import pytest
from pathlib import Path
import shutil
import tempfile
from click.testing import CliRunner

from super_pocket.cli import cli


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test output"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def runner():
    """Create Click CLI runner"""
    return CliRunner()


def test_cli_list_templates(runner):
    """Test 'pocket project init list' command"""
    result = runner.invoke(cli, ["project", "init", "list"])

    # Verify command succeeded
    assert result.exit_code == 0

    # Verify output contains template names
    output = result.output
    assert "python-cli" in output.lower() or "Python CLI" in output
    assert "fastapi" in output.lower() or "FastAPI" in output
    assert "python-package" in output.lower() or "Python Package" in output
    assert "ml-project" in output.lower() or "ML" in output
    assert "automation-script" in output.lower() or "Automation" in output
    assert "docs-site" in output.lower() or "Documentation" in output


def test_cli_show_template_python_cli(runner):
    """Test 'pocket project init show python-cli' command"""
    result = runner.invoke(cli, ["project", "init", "show", "python-cli"])

    # Verify command succeeded
    assert result.exit_code == 0

    # Verify output contains template details
    output = result.output
    assert "Python CLI" in output or "python-cli" in output
    assert "click" in output.lower() or "typer" in output.lower()


def test_cli_show_template_fastapi(runner):
    """Test 'pocket project init show fastapi-api' command"""
    result = runner.invoke(cli, ["project", "init", "show", "fastapi-api"])

    # Verify command succeeded
    assert result.exit_code == 0

    # Verify output contains template details
    output = result.output
    assert "FastAPI" in output or "fastapi" in output.lower()


def test_cli_show_invalid_template(runner):
    """Test 'pocket project init show' with invalid template name"""
    result = runner.invoke(cli, ["project", "init", "show", "nonexistent-template"])

    # Verify command indicates error
    # Exit code might be 0 with error message, so check output
    output = result.output
    assert "not found" in output.lower() or "error" in output.lower()


def test_cli_new_python_cli_quick_mode(runner, temp_output_dir):
    """Test 'pocket project init new python-cli --quick' command"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        result = runner.invoke(cli, [
            "project", "init", "new", "python-cli",
            "--path", "test_cli_project",
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created
        project_path = Path("test_cli_project")
        assert project_path.exists()
        assert (project_path / "README.md").exists()
        assert (project_path / "pyproject.toml").exists()

        # Verify src structure
        assert (project_path / "src").exists()


def test_cli_new_fastapi_quick_mode(runner, temp_output_dir):
    """Test 'pocket project init new fastapi-api --quick' command"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        result = runner.invoke(cli, [
            "project", "init", "new", "fastapi-api",
            "--path", "test_api_project",
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created
        project_path = Path("test_api_project")
        assert project_path.exists()
        assert (project_path / "README.md").exists()
        assert (project_path / "src").exists()


def test_cli_new_python_package_quick_mode(runner, temp_output_dir):
    """Test 'pocket project init new python-package --quick' command"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        result = runner.invoke(cli, [
            "project", "init", "new", "python-package",
            "--path", "test_package_project",
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created
        project_path = Path("test_package_project")
        assert project_path.exists()
        assert (project_path / "src").exists()


def test_cli_new_ml_project_quick_mode(runner, temp_output_dir):
    """Test 'pocket project init new ml-project --quick' command"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        result = runner.invoke(cli, [
            "project", "init", "new", "ml-project",
            "--path", "test_ml_project",
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created
        project_path = Path("test_ml_project")
        assert project_path.exists()
        assert (project_path / "notebooks").exists()
        assert (project_path / "data").exists()


def test_cli_new_automation_script_quick_mode(runner, temp_output_dir):
    """Test 'pocket project init new automation-script --quick' command"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        result = runner.invoke(cli, [
            "project", "init", "new", "automation-script",
            "--path", "test_automation_project",
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created
        project_path = Path("test_automation_project")
        assert project_path.exists()
        assert (project_path / "src").exists()


def test_cli_new_docs_site_quick_mode(runner, temp_output_dir):
    """Test 'pocket project init new docs-site --quick' command"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        result = runner.invoke(cli, [
            "project", "init", "new", "docs-site",
            "--path", "test_docs_project",
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created
        project_path = Path("test_docs_project")
        assert project_path.exists()
        assert (project_path / "docs").exists()


def test_cli_new_invalid_template(runner, temp_output_dir):
    """Test 'pocket project init new' with invalid template name"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        result = runner.invoke(cli, [
            "project", "init", "new", "nonexistent-template",
            "--path", "test_project",
            "--quick"
        ])

        # Verify command indicates error
        output = result.output
        assert "not found" in output.lower() or "error" in output.lower()


def test_cli_new_existing_directory(runner, temp_output_dir):
    """Test 'pocket project init new' with existing non-empty directory"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        # Create directory with a file
        test_dir = Path("existing_project")
        test_dir.mkdir()
        (test_dir / "existing_file.txt").write_text("test")

        result = runner.invoke(cli, [
            "project", "init", "new", "python-cli",
            "--path", "existing_project",
            "--quick"
        ])

        # Verify command indicates error
        output = result.output
        assert "exists" in output.lower() or "not empty" in output.lower()


def test_cli_new_with_custom_path(runner, temp_output_dir):
    """Test 'pocket project init new' with custom output path"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        custom_path = "custom/nested/path/my_project"

        result = runner.invoke(cli, [
            "project", "init", "new", "python-cli",
            "--path", custom_path,
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created at custom path
        project_path = Path(custom_path)
        assert project_path.exists()
        assert (project_path / "README.md").exists()


def test_cli_new_without_path_option(runner, temp_output_dir):
    """Test 'pocket project init new' without --path option (should use default)"""
    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        # Without --path, project name will be used as directory name
        # Quick mode uses default project name "my_project"
        result = runner.invoke(cli, [
            "project", "init", "new", "python-cli",
            "--quick"
        ])

        # Verify command succeeded
        assert result.exit_code == 0

        # Verify project was created with default name
        default_path = Path("my_project")
        assert default_path.exists()
        assert (default_path / "README.md").exists()


def test_cli_new_all_templates_quick_mode(runner, temp_output_dir):
    """Test that all 6 templates can be created via CLI in quick mode"""
    templates = [
        "python-cli",
        "fastapi-api",
        "python-package",
        "ml-project",
        "automation-script",
        "docs-site"
    ]

    with runner.isolated_filesystem(temp_dir=temp_output_dir):
        for i, template in enumerate(templates):
            project_name = f"test_project_{i}"

            result = runner.invoke(cli, [
                "project", "init", "new", template,
                "--path", project_name,
                "--quick"
            ])

            # Verify each template creates successfully
            assert result.exit_code == 0, f"Failed to create {template}: {result.output}"

            # Verify project was created
            project_path = Path(project_name)
            assert project_path.exists(), f"Project path not created for {template}"
            assert (project_path / "README.md").exists(), f"README not created for {template}"


def test_cli_help_commands(runner):
    """Test that all help commands work"""
    # Test main init help
    result = runner.invoke(cli, ["project", "init", "--help"])
    assert result.exit_code == 0
    assert "list" in result.output
    assert "show" in result.output
    assert "new" in result.output

    # Test list help
    result = runner.invoke(cli, ["project", "init", "list", "--help"])
    assert result.exit_code == 0

    # Test show help
    result = runner.invoke(cli, ["project", "init", "show", "--help"])
    assert result.exit_code == 0

    # Test new help
    result = runner.invoke(cli, ["project", "init", "new", "--help"])
    assert result.exit_code == 0
    assert "--quick" in result.output
    assert "--path" in result.output
