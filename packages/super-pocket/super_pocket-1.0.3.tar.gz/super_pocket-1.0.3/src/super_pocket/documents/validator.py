"""
Template validator module.

Provides functionality to validate the syntax and structure
of agent configuration templates.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any

from rich.console import Console


console = Console()


class TemplateValidationError(Exception):
    """Exception raised when template validation fails."""
    pass


def validate_markdown_syntax(content: str) -> List[str]:
    """
    Validate basic Markdown syntax.

    Args:
        content: Markdown content to validate.

    Returns:
        List of warning/error messages (empty if valid).
    """
    issues = []

    lines = content.split('\n')

    # Check for basic structure
    has_heading = any(line.strip().startswith('#') for line in lines)
    if not has_heading:
        issues.append("Warning: No headings found in template")

    # Check for unclosed code blocks
    code_block_count = content.count('```')
    if code_block_count % 2 != 0:
        issues.append("Error: Unclosed code block detected")

    return issues


def validate_agent_template(file_path: Path) -> Dict[str, Any]:
    """
    Validate an agent configuration template.

    Args:
        file_path: Path to the template file.

    Returns:
        Dictionary with validation results:
        - 'valid': bool
        - 'issues': list of issues found
        - 'warnings': list of warnings
    """
    result = {
        'valid': True,
        'issues': [],
        'warnings': []
    }

    try:
        content = file_path.read_text(encoding='utf-8')

        # Basic Markdown validation
        syntax_issues = validate_markdown_syntax(content)
        for issue in syntax_issues:
            if issue.startswith('Error'):
                result['valid'] = False
                result['issues'].append(issue)
            else:
                result['warnings'].append(issue)

        # Check file size (warn if too large)
        file_size_kb = len(content) / 1024
        if file_size_kb > 100:
            result['warnings'].append(f"Warning: Template is large ({file_size_kb:.1f} KB)")

    except Exception as e:
        result['valid'] = False
        result['issues'].append(f"Error reading file: {e}")

    return result


def validate_template_file(file_path: Path, verbose: bool = True) -> bool:
    """
    Validate a template file and optionally print results.

    Args:
        file_path: Path to the template file.
        verbose: If True, print validation results.

    Returns:
        True if valid, False otherwise.
    """
    if not file_path.exists():
        if verbose:
            console.print(f"[red]Error:[/red] File not found: {file_path}", style="bold")
        return False

    if verbose:
        console.print(f"Validating: [cyan]{file_path.name}[/cyan]")

    result = validate_agent_template(file_path)

    if verbose:
        if result['valid']:
            console.print("[green]✓ Valid[/green]")
        else:
            console.print("[red]✗ Invalid[/red]")

        for issue in result['issues']:
            console.print(f"  [red]•[/red] {issue}")

        for warning in result['warnings']:
            console.print(f"  [yellow]•[/yellow] {warning}")

    return result['valid']
