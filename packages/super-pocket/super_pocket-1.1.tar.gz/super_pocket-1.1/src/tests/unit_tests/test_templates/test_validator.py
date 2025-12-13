"""
Tests for template validator module.
"""

import pytest
from pathlib import Path
from super_pocket.documents.validator import (
    validate_markdown_syntax,
    validate_agent_template,
    validate_template_file,
    TemplateValidationError
)


def test_validate_markdown_syntax_valid():
    """Test validating valid markdown content."""
    content = """# Test Document

This is a **test** document.

## Section

Some content here.
"""
    issues = validate_markdown_syntax(content)
    assert isinstance(issues, list)
    assert len(issues) == 0


def test_validate_markdown_syntax_no_heading():
    """Test validating markdown without headings generates warning."""
    content = "This is plain text without headings."
    issues = validate_markdown_syntax(content)
    assert len(issues) > 0
    assert any("No headings found" in issue for issue in issues)


def test_validate_markdown_syntax_unclosed_code_block():
    """Test validating markdown with unclosed code block generates error."""
    # Content with only one opening ``` (unclosed)
    content = """# Test

```python
def hello():
    print("Hello")
# Missing closing code block
"""
    issues = validate_markdown_syntax(content)
    assert len(issues) > 0
    assert any("Unclosed code block" in issue for issue in issues)


def test_validate_markdown_syntax_closed_code_block():
    """Test validating markdown with properly closed code blocks."""
    content = """# Test

```python
def hello():
    print("Hello")
```
"""
    issues = validate_markdown_syntax(content)
    # Should not have unclosed code block error
    assert not any("Unclosed code block" in issue for issue in issues)


def test_validate_agent_template_valid_file(sample_markdown_file):
    """Test validating a valid agent template file."""
    result = validate_agent_template(sample_markdown_file)
    
    assert isinstance(result, dict)
    assert 'valid' in result
    assert 'issues' in result
    assert 'warnings' in result
    assert result['valid'] is True
    assert isinstance(result['issues'], list)
    assert isinstance(result['warnings'], list)


def test_validate_agent_template_nonexistent_file():
    """Test validating a non-existent file."""
    nonexistent = Path("/nonexistent/path/file.md")
    result = validate_agent_template(nonexistent)
    
    assert result['valid'] is False
    assert len(result['issues']) > 0
    assert any("Error reading file" in issue for issue in result['issues'])


def test_validate_agent_template_large_file(temp_dir):
    """Test validating a large file generates warning."""
    large_content = "# Test\n" + "x" * 150000  # ~150KB
    large_file = temp_dir / "large.md"
    large_file.write_text(large_content, encoding='utf-8')
    
    result = validate_agent_template(large_file)
    
    assert len(result['warnings']) > 0
    assert any("large" in warning.lower() for warning in result['warnings'])


def test_validate_agent_template_with_errors(temp_dir):
    """Test validating a template with markdown errors."""
    invalid_content = """# Test

```python
def hello():
    print("Hello")
# Missing closing code block
"""
    invalid_file = temp_dir / "invalid.md"
    invalid_file.write_text(invalid_content, encoding='utf-8')
    
    result = validate_agent_template(invalid_file)
    
    assert result['valid'] is False
    assert len(result['issues']) > 0
    assert any("Unclosed code block" in issue for issue in result['issues'])


def test_validate_template_file_success(sample_markdown_file, capsys):
    """Test validate_template_file with valid file."""
    result = validate_template_file(sample_markdown_file, verbose=True)
    
    assert result is True
    captured = capsys.readouterr()
    assert "Validating" in captured.out or "Valid" in captured.out


def test_validate_template_file_nonexistent():
    """Test validate_template_file with non-existent file."""
    nonexistent = Path("/nonexistent/file.md")
    result = validate_template_file(nonexistent, verbose=False)
    
    assert result is False


def test_validate_template_file_verbose_false(sample_markdown_file):
    """Test validate_template_file with verbose=False doesn't print."""
    result = validate_template_file(sample_markdown_file, verbose=False)
    
    assert isinstance(result, bool)


def test_validate_markdown_syntax_empty_content():
    """Test validating empty markdown content."""
    issues = validate_markdown_syntax("")
    assert isinstance(issues, list)
    # Empty content should have no heading warning
    assert any("No headings found" in issue for issue in issues)


def test_validate_markdown_syntax_multiple_code_blocks():
    """Test validating markdown with multiple code blocks."""
    content = """# Test

```python
def hello():
    pass
```

```javascript
function hello() {
    console.log("Hello");
}
```
"""
    issues = validate_markdown_syntax(content)
    # Should not have unclosed code block error
    assert not any("Unclosed code block" in issue for issue in issues)

