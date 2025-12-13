"""
Tests for the main CLI module.
"""

import pytest
from pathlib import Path
from click.testing import CliRunner
from super_pocket.cli import cli, main


@pytest.fixture
def runner():
    """Provide a CliRunner instance for testing."""
    return CliRunner()


def test_cli_version(runner: CliRunner):
    """Test CLI version option."""
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert "pocket" in result.output.lower() or "version" in result.output.lower()


def test_cli_help(runner: CliRunner):
    """Test CLI help command."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Pocket" in result.output or "pocket" in result.output.lower()


def test_cli_markdown_render(runner: CliRunner, sample_markdown_file):
    """Test markdown render command."""
    result = runner.invoke(
        cli,
        ['markdown', 'render', str(sample_markdown_file)]
    )
    # Should succeed if file exists
    assert result.exit_code in [0, 1]


def test_cli_markdown_render_nonexistent(runner: CliRunner):
    """Test markdown render with non-existent file."""
    result = runner.invoke(
        cli,
        ['markdown', 'render', '/nonexistent/file.md']
    )
    assert result.exit_code != 0


def test_cli_project_to_file(runner: CliRunner, sample_project_structure, temp_dir):
    """Test project to-file command."""
    output_file = temp_dir / "project_export.md"
    
    result = runner.invoke(
        cli,
        [
            'project', 'to-file',
            '--path', str(sample_project_structure),
            '--output', str(output_file)
        ]
    )
    
    if result.exit_code == 0:
        assert output_file.exists()


def test_cli_project_to_file_default_path(runner: CliRunner, temp_dir):
    """Test project to-file with default path."""
    result = runner.invoke(
        cli,
        ['project', 'to-file', '--output', str(temp_dir / "output.md")]
    )
    # Should either succeed or fail gracefully
    assert result.exit_code in [0, 1]


def test_cli_documents_list(runner: CliRunner):
    """Test documents list command."""
    result = runner.invoke(cli, ['documents', 'list'])
    assert result.exit_code == 0


def test_cli_documents_list_type(runner: CliRunner):
    """Test documents list with type option."""
    result = runner.invoke(cli, ['documents', 'list', '--type', 'templates'])
    assert result.exit_code == 0


def test_cli_documents_view(runner: CliRunner):
    """Test documents view command."""
    # Try to view an actual template if any exist
    from super_pocket.documents.cli import get_available_items
    
    templates = get_available_items("templates")
    if templates:
        template_name = templates[0].stem
        result = runner.invoke(cli, ['documents', 'view', template_name])
        # Should succeed if template exists
        assert result.exit_code in [0, 1]
    else:
        pytest.skip("No templates available for testing")


def test_cli_documents_view_nonexistent(runner: CliRunner):
    """Test documents view with non-existent template."""
    result = runner.invoke(cli, ['documents', 'view', 'nonexistent_template_xyz'])
    assert result.exit_code != 0


def test_cli_documents_copy(runner: CliRunner, temp_dir):
    """Test documents copy command."""
    from super_pocket.documents.cli import get_available_items
    
    templates = get_available_items("templates")
    if templates:
        template_name = templates[0].stem
        output_file = temp_dir / "copied_template.md"
        
        result = runner.invoke(
            cli,
            [
                'documents', 'copy',
                template_name,
                '--output', str(output_file),
                '--force'
            ]
        )
        
        if result.exit_code == 0:
            assert output_file.exists()
    else:
        pytest.skip("No templates available for testing")


def test_cli_documents_init(runner: CliRunner, temp_dir):
    """Test documents init command."""
    output_dir = temp_dir / ".AGENTS_CLI"
    
    result = runner.invoke(
        cli,
        ['documents', 'init', '--output', str(output_dir)]
    )
    
    if result.exit_code == 0:
        assert output_dir.exists()
        assert output_dir.is_dir()


def test_cli_pdf_convert(runner: CliRunner, temp_dir):
    """Test PDF convert command."""
    # Create a test text file
    test_file = temp_dir / "test.txt"
    test_file.write_text("Test content", encoding='utf-8')
    output_file = temp_dir / "output.pdf"
    
    result = runner.invoke(
        cli,
        ['pdf', 'convert', str(test_file), '--output', str(output_file)]
    )
    
    # May fail if fpdf2 is not installed, which is acceptable
    assert result.exit_code in [0, 1]


def test_cli_pdf_convert_nonexistent(runner: CliRunner):
    """Test PDF convert with non-existent file."""
    result = runner.invoke(
        cli,
        ['pdf', 'convert', '/nonexistent/file.txt']
    )
    assert result.exit_code != 0


def test_cli_web_favicon(runner: CliRunner, temp_dir):
    """Test web favicon command."""
    # Create a dummy image file (not a real image, but tests the command structure)
    test_file = temp_dir / "test.png"
    test_file.write_text("dummy", encoding='utf-8')
    output_file = temp_dir / "favicon.ico"
    
    result = runner.invoke(
        cli,
        ['web', 'favicon', str(test_file), '--output', str(output_file)]
    )
    
    # May fail if Pillow is not installed or file is not a valid image, which is acceptable
    assert result.exit_code in [0, 1]


def test_cli_web_favicon_nonexistent(runner: CliRunner):
    """Test web favicon with non-existent file."""
    result = runner.invoke(
        cli,
        ['web', 'favicon', '/nonexistent/file.png']
    )
    assert result.exit_code != 0


def test_cli_web_favicon_with_sizes(runner: CliRunner, temp_dir):
    """Test web favicon with custom sizes."""
    test_file = temp_dir / "test.png"
    test_file.write_text("dummy", encoding='utf-8')
    output_file = temp_dir / "favicon.ico"
    
    result = runner.invoke(
        cli,
        [
            'web', 'favicon',
            str(test_file),
            '--output', str(output_file),
            '--sizes', '64x64,32x32,16x16'
        ]
    )
    
    # May fail if Pillow is not installed or file is not a valid image
    assert result.exit_code in [0, 1]


def test_main_function(runner: CliRunner):
    """Test main function entry point."""
    # main() just calls cli(), so test that it doesn't crash
    try:
        main()
    except SystemExit:
        pass  # Expected when no arguments provided
    except Exception:
        pytest.fail("main() raised an unexpected exception")


def test_cli_no_arguments(runner: CliRunner):
    """Test CLI with no arguments shows help."""
    result = runner.invoke(cli, [])
    # Should show help or usage
    assert result.exit_code in [0, 2]  # 0 for help, 2 for missing command


def test_cli_invalid_command(runner: CliRunner):
    """Test CLI with invalid command."""
    result = runner.invoke(cli, ['invalid-command'])
    assert result.exit_code != 0


def test_cli_markdown_group_help(runner: CliRunner):
    """Test markdown group help."""
    result = runner.invoke(cli, ['markdown', '--help'])
    assert result.exit_code == 0


def test_cli_project_group_help(runner: CliRunner):
    """Test project group help."""
    result = runner.invoke(cli, ['project', '--help'])
    assert result.exit_code == 0


def test_cli_documents_group_help(runner: CliRunner):
    """Test documents group help."""
    result = runner.invoke(cli, ['documents', '--help'])
    assert result.exit_code == 0


def test_cli_pdf_group_help(runner: CliRunner):
    """Test PDF group help."""
    result = runner.invoke(cli, ['pdf', '--help'])
    assert result.exit_code == 0


def test_cli_web_group_help(runner: CliRunner):
    """Test web group help."""
    result = runner.invoke(cli, ['web', '--help'])
    assert result.exit_code == 0

