"""Tests for README CLI commands."""

from click.testing import CliRunner
from super_pocket.readme.cli import readme_cli


def test_readme_cli_help():
    """Test readme CLI help message."""
    runner = CliRunner()
    result = runner.invoke(readme_cli, ["--help"])

    assert result.exit_code == 0
    assert "readme" in result.output.lower()


def test_readme_analyze_command(tmp_path):
    """Test readme analyze command."""
    # Create a Python project
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-project"
version = "1.0.0"
requires-python = ">=3.11"
""")

    runner = CliRunner()
    result = runner.invoke(readme_cli, ["analyze", str(tmp_path)])

    assert result.exit_code == 0
    assert "python" in result.output.lower()


def test_readme_analyze_no_project(tmp_path):
    """Test analyze command on non-project directory."""
    runner = CliRunner()
    result = runner.invoke(readme_cli, ["analyze", str(tmp_path)])

    assert result.exit_code != 0
    assert "not detect" in result.output.lower() or "no project" in result.output.lower()


def test_readme_generate_command(tmp_path):
    """Test readme generate command creates README file."""
    # Create a Python project
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-project"
version = "1.0.0"
requires-python = ">=3.11"
""")

    runner = CliRunner()
    output_file = tmp_path / "README.md"
    result = runner.invoke(readme_cli, ["generate", "-p", str(tmp_path), "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()
    assert "# test-project" in output_file.read_text()
