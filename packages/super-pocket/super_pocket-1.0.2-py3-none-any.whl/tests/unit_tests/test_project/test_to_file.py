"""
Tests for project to_file module.
"""

import pytest
from pathlib import Path
from super_pocket.project.to_file import (
    get_language_identifier,
    generate_tree,
    create_codebase_markdown
)


def test_get_language_identifier_python():
    """Test language identifier for Python files."""
    assert get_language_identifier("test.py") == "python"
    assert get_language_identifier("TEST.PY") == "python"


def test_get_language_identifier_javascript():
    """Test language identifier for JavaScript files."""
    assert get_language_identifier("app.js") == "javascript"
    assert get_language_identifier("component.ts") == "typescript"


def test_get_language_identifier_dockerfile():
    """Test language identifier for Dockerfile."""
    assert get_language_identifier("Dockerfile") == "dockerfile"


def test_get_language_identifier_unknown():
    """Test language identifier for unknown file types."""
    assert get_language_identifier("unknown.xyz") == "plaintext"


def test_generate_tree(sample_project_structure):
    """Test generating project tree."""
    tree_lines = list(generate_tree(str(sample_project_structure), set()))
    tree_output = '\n'.join(tree_lines)

    assert "src/" in tree_output
    assert "main.py" in tree_output
    assert "README.md" in tree_output


def test_generate_tree_with_exclusions(sample_project_structure):
    """Test generating project tree with exclusions."""
    tree_lines = list(generate_tree(str(sample_project_structure), {"tests"}))
    tree_output = '\n'.join(tree_lines)

    assert "src/" in tree_output
    assert "tests" not in tree_output


def test_create_codebase_markdown(sample_project_structure, temp_dir):
    """Test creating codebase markdown file."""
    output_file = temp_dir / "output.md"

    create_codebase_markdown(
        str(sample_project_structure),
        str(output_file),
        "__pycache__,.git"
    )

    assert output_file.exists()
    content = output_file.read_text(encoding='utf-8')

    # Check that file contains expected content
    assert "test_project" in content
    assert "```bash" in content  # Tree structure
    assert "```python" in content  # Python code blocks
    assert "main.py" in content


def test_get_language_identifier_various_extensions():
    """Test language identifier for various file extensions."""
    assert get_language_identifier("file.html") == "html"
    assert get_language_identifier("file.css") == "css"
    assert get_language_identifier("file.json") == "json"
    assert get_language_identifier("file.yaml") == "yaml"
    assert get_language_identifier("file.yml") == "yaml"
    assert get_language_identifier("file.sh") == "bash"
    assert get_language_identifier("file.go") == "go"
    assert get_language_identifier("file.rs") == "rust"
    assert get_language_identifier("file.php") == "php"
    assert get_language_identifier("file.rb") == "ruby"
    assert get_language_identifier("file.sql") == "sql"


def test_get_language_identifier_case_insensitive():
    """Test that language identifier is case insensitive."""
    assert get_language_identifier("file.PY") == "python"
    assert get_language_identifier("file.JS") == "javascript"
    assert get_language_identifier("file.MD") == "markdown"


def test_generate_tree_empty_directory(temp_dir):
    """Test generating tree for empty directory."""
    empty_dir = temp_dir / "empty"
    empty_dir.mkdir()
    
    tree_lines = list(generate_tree(str(empty_dir), set()))
    # Should return empty or minimal tree
    assert isinstance(tree_lines, list)


def test_generate_tree_multiple_exclusions(sample_project_structure):
    """Test generating tree with multiple exclusions."""
    exclusions = {"tests", "src", "README.md"}
    tree_lines = list(generate_tree(str(sample_project_structure), exclusions))
    tree_output = '\n'.join(tree_lines)
    
    assert "tests" not in tree_output
    assert "src" not in tree_output
    assert "README.md" not in tree_output


def test_create_codebase_markdown_with_binary_file(sample_project_structure, temp_dir):
    """Test creating markdown with binary files (should skip them)."""
    # Add a binary-like file to the project
    binary_file = sample_project_structure / "binary.bin"
    binary_file.write_bytes(b'\x00\x01\x02\x03')
    
    output_file = temp_dir / "output.md"
    
    create_codebase_markdown(
        str(sample_project_structure),
        str(output_file),
        "__pycache__,.git"
    )
    
    assert output_file.exists()
    # Binary file should be skipped or handled gracefully
    content = output_file.read_text(encoding='utf-8')
    # Should still contain other files
    assert "main.py" in content or "test_project" in content
