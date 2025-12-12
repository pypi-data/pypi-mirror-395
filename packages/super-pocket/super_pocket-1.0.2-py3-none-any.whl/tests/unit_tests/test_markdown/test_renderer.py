"""
Tests for markdown renderer module.
"""

import pytest
from pathlib import Path
from super_pocket.markdown.renderer import read_markdown_file, render_markdown
from rich.console import Console


def test_read_markdown_file_success(sample_markdown_file):
    """Test reading a valid markdown file."""
    content = read_markdown_file(sample_markdown_file)
    assert isinstance(content, str)
    assert "Test Document" in content
    assert "Hello, world!" in content


def test_read_markdown_file_not_found():
    """Test reading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_markdown_file(Path("/nonexistent/file.md"))


def test_read_markdown_file_not_a_file(temp_dir):
    """Test reading a directory raises ValueError."""
    with pytest.raises(ValueError):
        read_markdown_file(temp_dir)


def test_render_markdown_success(sample_markdown_content):
    """Test rendering markdown content."""
    console = Console()
    # Should not raise any exception
    render_markdown(sample_markdown_content, console)


def test_render_markdown_with_default_console(sample_markdown_content):
    """Test rendering markdown with default console."""
    # Should not raise any exception
    render_markdown(sample_markdown_content)


def test_render_markdown_empty_content():
    """Test rendering empty markdown content."""
    console = Console()
    # Should not raise any exception
    render_markdown("", console)


def test_read_markdown_file_permission_error(temp_dir):
    """Test reading a file with permission errors."""
    # Create a file and then make it unreadable (if possible)
    test_file = temp_dir / "test.md"
    test_file.write_text("# Test", encoding='utf-8')
    
    # On Unix systems, we can test permission errors
    import os
    import stat
    try:
        # Make file unreadable
        test_file.chmod(0o000)
        with pytest.raises((PermissionError, IOError)):
            read_markdown_file(test_file)
    except (OSError, NotImplementedError):
        # Permission changes not supported on this system
        pytest.skip("Permission testing not supported on this system")
    finally:
        # Restore permissions
        try:
            test_file.chmod(0o644)
        except (OSError, NotImplementedError):
            pass


def test_render_markdown_various_formats():
    """Test rendering markdown with various formatting."""
    console = Console()
    
    # Test with different markdown elements
    complex_markdown = """# Heading 1
## Heading 2
### Heading 3

**Bold text** and *italic text*

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2

`inline code`

```python
def hello():
    print("Hello")
```

> Blockquote

[Link](https://example.com)
"""
    # Should not raise any exception
    render_markdown(complex_markdown, console)
