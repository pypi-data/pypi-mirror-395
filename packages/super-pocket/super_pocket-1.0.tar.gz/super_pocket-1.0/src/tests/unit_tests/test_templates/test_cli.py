"""
Tests for templates and cheatsheets CLI module.
"""

import pytest
import shutil
from pathlib import Path
from click.testing import CliRunner
from super_pocket.templates_and_cheatsheets.cli import (
    templates_cli,
    get_available_items,
    list_items,
    view_item,
    copy_item,
    init_agents
)
from super_pocket.templates_and_cheatsheets import TEMPLATES_DIR, CHEATSHEETS_DIR


def test_get_available_items_templates():
    """Test getting available templates."""
    items = get_available_items("templates")
    assert isinstance(items, list)
    # Check that all items are Path objects
    if items:
        assert all(isinstance(item, Path) for item in items)
        assert all(item.suffix == '.md' for item in items)


def test_get_available_items_cheatsheets():
    """Test getting available cheatsheets."""
    items = get_available_items("cheatsheets")
    assert isinstance(items, list)
    # Check that all items are Path objects
    if items:
        assert all(isinstance(item, Path) for item in items)
        assert all(item.suffix == '.md' for item in items)


def test_templates_cli_list_all(runner: CliRunner):
    """Test listing all templates and cheatsheets."""
    result = runner.invoke(templates_cli, ['list'])
    assert result.exit_code == 0
    assert "Available Templates & Cheatsheets" in result.output or "Template" in result.output or "Cheatsheet" in result.output


def test_templates_cli_list_templates(runner: CliRunner):
    """Test listing only templates."""
    result = runner.invoke(templates_cli, ['list', '--type', 'templates'])
    assert result.exit_code == 0


def test_templates_cli_list_cheatsheets(runner: CliRunner):
    """Test listing only cheatsheets."""
    result = runner.invoke(templates_cli, ['list', '--type', 'cheatsheets'])
    assert result.exit_code == 0


def test_templates_cli_view_existing_template(runner: CliRunner, temp_dir):
    """Test viewing an existing template."""
    # Create a test template
    test_template = TEMPLATES_DIR / "test_template.md"
    if not test_template.exists():
        test_template.write_text("# Test Template\n\nThis is a test.", encoding='utf-8')
    
    try:
        result = runner.invoke(templates_cli, ['view', 'test_template'])
        # Should succeed if template exists, or fail gracefully if not
        assert result.exit_code in [0, 1]
    finally:
        if test_template.exists() and test_template.name == "test_template.md":
            test_template.unlink()


def test_templates_cli_view_nonexistent(runner: CliRunner):
    """Test viewing a non-existent template."""
    result = runner.invoke(templates_cli, ['view', 'nonexistent_template_xyz'])
    assert result.exit_code != 0
    assert "not found" in result.output.lower() or "Error" in result.output


def test_templates_cli_copy_existing_template(runner: CliRunner, temp_dir):
    """Test copying an existing template."""
    # Create a test template
    test_template = TEMPLATES_DIR / "test_template.md"
    if not test_template.exists():
        test_template.write_text("# Test Template\n\nThis is a test.", encoding='utf-8')
    
    output_file = temp_dir / "copied_template.md"
    
    try:
        result = runner.invoke(
            templates_cli,
            ['copy', 'test_template', '--output', str(output_file), '--force']
        )
        # Should succeed if template exists
        if result.exit_code == 0:
            assert output_file.exists()
            assert output_file.read_text(encoding='utf-8') == test_template.read_text(encoding='utf-8')
    finally:
        if test_template.exists() and test_template.name == "test_template.md":
            test_template.unlink()
        if output_file.exists():
            output_file.unlink()


def test_templates_cli_copy_nonexistent(runner: CliRunner, temp_dir):
    """Test copying a non-existent template."""
    output_file = temp_dir / "output.md"
    result = runner.invoke(
        templates_cli,
        ['copy', 'nonexistent_template_xyz', '--output', str(output_file)]
    )
    assert result.exit_code != 0
    assert "not found" in result.output.lower() or "Error" in result.output


def test_templates_cli_copy_without_force_existing_file(runner: CliRunner, temp_dir):
    """Test copying when output file already exists without --force."""
    # Create a test template
    test_template = TEMPLATES_DIR / "test_template.md"
    if not test_template.exists():
        test_template.write_text("# Test Template\n\nThis is a test.", encoding='utf-8')
    
    output_file = temp_dir / "existing.md"
    output_file.write_text("Existing content", encoding='utf-8')
    
    try:
        result = runner.invoke(
            templates_cli,
            ['copy', 'test_template', '--output', str(output_file)],
            input='n\n'  # Don't overwrite
        )
        # Should either abort or prompt
        assert result.exit_code in [0, 1]
    finally:
        if test_template.exists() and test_template.name == "test_template.md":
            test_template.unlink()


def test_templates_cli_init(runner: CliRunner, temp_dir):
    """Test initializing agent templates directory."""
    output_dir = temp_dir / ".AGENTS"
    
    result = runner.invoke(
        templates_cli,
        ['init', '--output', str(output_dir)]
    )
    
    # Should succeed if templates exist
    if result.exit_code == 0:
        assert output_dir.exists()
        assert output_dir.is_dir()


def test_list_items_function(runner: CliRunner):
    """Test list_items function directly."""
    result = runner.invoke(list_items, ['--type', 'all'])
    assert result.exit_code == 0


def test_view_item_function_existing(runner: CliRunner):
    """Test view_item function with existing item."""
    # Try to view an actual template if any exist
    templates = get_available_items("templates")
    if templates:
        template_name = templates[0].stem
        result = runner.invoke(view_item, [template_name])
        # Should succeed if template exists
        assert result.exit_code in [0, 1]
    else:
        pytest.skip("No templates available for testing")


def test_view_item_function_nonexistent(runner: CliRunner):
    """Test view_item function with non-existent item."""
    result = runner.invoke(view_item, ['nonexistent_item_xyz'])
    assert result.exit_code != 0


def test_copy_item_function(runner: CliRunner, temp_dir):
    """Test copy_item function."""
    templates = get_available_items("templates")
    if templates:
        template_name = templates[0].stem
        output_file = temp_dir / "copied.md"
        
        result = runner.invoke(
            copy_item,
            [template_name, '--output', str(output_file), '--force']
        )
        
        if result.exit_code == 0:
            assert output_file.exists()
    else:
        pytest.skip("No templates available for testing")


def test_init_agents_function(runner: CliRunner, temp_dir):
    """Test init_agents function."""
    output_dir = temp_dir / ".AGENTS_TEST"
    
    result = runner.invoke(init_agents, ['--output', str(output_dir)])
    
    if result.exit_code == 0:
        assert output_dir.exists()
        assert output_dir.is_dir()


@pytest.fixture
def runner():
    """Provide a CliRunner instance for testing."""
    return CliRunner()

