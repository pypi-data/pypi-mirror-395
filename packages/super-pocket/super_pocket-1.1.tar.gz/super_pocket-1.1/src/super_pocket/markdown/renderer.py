#!/usr/bin/env python3
"""
Markdown renderer using Rich library.

This module provides functionality to read and render Markdown files
beautifully in the terminal using the Rich library for enhanced formatting
and syntax highlighting.

Combines functionality from both fancy_md.py and markd.py.
"""

from pathlib import Path
from typing import Optional

from super_pocket.settings import click
from rich.console import Console
from rich.markdown import Markdown
from rich import errors
from rich.prompt import Prompt
from super_pocket.utils import print_error




def read_markdown_file(file_path: Path) -> str:
    """
    Read the contents of a Markdown file.

    Args:
        file_path: Path to the Markdown file to read.

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the path is not a file.
        PermissionError: If the file cannot be read.
        IOError: If there's an error reading the file.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    try:
        return file_path.read_text(encoding='utf-8')
    except PermissionError:
        raise
    except Exception as e:
        print_error(e, custom=True, message=f"Error reading file {file_path}")
        raise


def render_markdown(content: str, console: Optional[Console] = None) -> None:
    """
    Render Markdown content to the terminal using Rich.

    Args:
        content: The Markdown content to render.
        console: Optional Console instance. If not provided, a new one is created.

    Raises:
        errors.MarkdownError: If there's an error rendering the markdown.
    """
    if not console:
        console = Console()

    try:
        md = Markdown(content)
        console.print(md)
    except errors.MarkdownError as e:
        print_error(e, custom=True, message="Error rendering Markdown")
        raise


@click.command()
@click.argument(
    'file',
    type=click.Path(exists=True, path_type=Path),
    required=False
)
def markd(file: Path) -> None:
    """
    Render Markdown files in the terminal.

    This command-line tool reads a Markdown file and displays it with enhanced
    formatting, syntax highlighting, and beautiful terminal rendering using the
    Rich library. Supports multiple input methods for flexibility.

    Args:
        file: Positional argument for the file path (preferred method).

    Note:
        If no file is specified, the user will be prompted interactively.

    Examples:
        markd README.md
    """
    console = Console()

    # Determine which file path to use (priority: file)
    file_path = file

    # If no file specified, prompt the user
    if not file_path:
        file_path_str = Prompt.ask('Enter the path to the Markdown file')
        file_path = Path(file_path_str.strip())

    try:
        # Read the Markdown file
        content = read_markdown_file(file_path)

        # Render the Markdown
        render_markdown(content, console)

    except (FileNotFoundError, ValueError, PermissionError, IOError) as e:
        print_error(e)
        raise

    except Exception as e:
        print_error(e, custom=True, message="Unexpected error")
        raise


if __name__ == '__main__':
    markd()
