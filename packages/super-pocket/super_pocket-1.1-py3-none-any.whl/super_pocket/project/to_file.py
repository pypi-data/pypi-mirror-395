#!/usr/bin/env python3
"""
Project to file converter.

This module scans a project directory and generates a single Markdown file
containing the entire codebase with syntax highlighting and file tree structure.
"""

import os
import argparse
import sys
from super_pocket.settings import click, CONTEXT_SETTINGS, add_help_argument
from rich.console import Console
from collections.abc import Generator
from pathlib import Path
from typing import Set


console = Console()


# Language mapping for syntax highlighting in Markdown code blocks
LANG_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.json': 'json',
    '.xml': 'xml',
    '.yml': 'yaml',
    '.yaml': 'yaml',
    '.md': 'markdown',
    '.sh': 'bash',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.go': 'go',
    '.rs': 'rust',
    '.php': 'php',
    '.rb': 'ruby',
    '.sql': 'sql',
    '.dockerfile': 'dockerfile',
    'Dockerfile': 'dockerfile',
}

DEFAULT_VALUES = {
    "project": ".",
    "output": None,
    "exclude": "env,.env,venv,.venv,.gitignore,.git,.vscode,.idea,.cursor,lib,bin,site-packages,node_modules,__pycache__,.DS_Store,.python-version",
    "extend_exclude": ""
}


def get_language_identifier(filename: str) -> str:
    """
    Determine the language identifier for a Markdown code block based on file extension.

    This function maps file extensions to their corresponding language identifiers
    for proper syntax highlighting in Markdown code blocks. Special files like
    'Dockerfile' are handled separately.

    Args:
        filename: The name of the file (can be basename or full path).

    Returns:
        str: Language identifier for syntax highlighting (e.g., 'python', 'javascript').
             Returns 'plaintext' if the extension is not recognized.

    Example:
        >>> get_language_identifier('script.py')
        'python'
        >>> get_language_identifier('Dockerfile')
        'dockerfile'
    """
    # Handle special cases like 'Dockerfile' without extension
    if os.path.basename(filename) in LANG_MAP:
        return LANG_MAP[os.path.basename(filename)]

    # Handle standard extensions
    _, ext = os.path.splitext(filename)
    return LANG_MAP.get(ext.lower(), 'plaintext')


def generate_tree(root_dir: str, exclude: Set[str]) -> Generator[str, None, None]:
    """
    Generate a text representation of the project tree structure.

    Creates an ASCII tree visualization of the directory structure, similar to
    the Unix 'tree' command. Excludes specified files and directories from the
    output. Uses box-drawing characters (│, ├, └) for visual hierarchy.

    Args:
        root_dir: Root directory to scan.
        exclude: Set of file/directory names to exclude from the tree.

    Yields:
        str: Lines representing the tree structure with proper indentation.

    Example:
        >>> for line in generate_tree('/path/to/project', {'node_modules', '.git'}):
        ...     print(line)
        ├── src/
        │   ├── main.py
        │   └── utils.py
    """
    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Modify in-place to prevent os.walk from exploring excluded directories
        dirs[:] = [d for d in dirs if d not in exclude]
        files = [f for f in files if f not in exclude]

        level = root.replace(root_dir, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''

        # Display current directory name (relative)
        if level > 0:
            yield f"{indent}{os.path.basename(root)}/"

        # Display files in current directory
        sub_indent = '│   ' * level + '├── '
        for i, f in enumerate(sorted(files)):
            # Use different prefix for last element
            prefix = '└── ' if i == len(files) - 1 else '├── '
            yield f"{'│   ' * level}{prefix}{f}"


def create_codebase_markdown(
    project_path: str,
    output_file: str,
    exclude_str: str
) -> None:
    """
    Scan a project and generate a comprehensive Markdown documentation file.

    This function walks through a project directory, generates a file tree
    visualization, and includes the content of all text-based files in a single
    Markdown document with proper syntax highlighting. Perfect for documentation,
    code reviews, or feeding entire codebases to AI tools.

    The generated Markdown file includes:
    1. Project title (based on directory name)
    2. ASCII tree structure of the project
    3. Content of each file with syntax highlighting

    Args:
        project_path: Path to the project root directory.
        output_file: Path to the output Markdown file. If None, defaults to
                    '<project_name>-1-file.md'.
        exclude_str: Comma-separated string of files/directories to exclude
                    (e.g., "node_modules,.git,__pycache__").

    Raises:
        IOError: If there's an error writing to the output file.
        SystemExit: If the project path doesn't exist or an error occurs during processing.

    Example:
        >>> create_codebase_markdown(
        ...     project_path='/path/to/my-app',
        ...     output_file='my-app.md',
        ...     exclude_str='node_modules,.git,dist'
        ... )
        || Starting project scan: 'my-app'
        ...
        || Success! Codebase compiled into 'my-app.md'
    """
    # Clean up paths and exclusions
    project_path = os.path.abspath(project_path)
    project_name = os.path.basename(project_path)
    exclude_set = set(exclude_str.split(','))

    # Set default output filename if not provided
    if output_file is None:
        output_file = f"{project_name}-1-file.md"

    console.print(f"|| Starting project scan: '{project_name}'", style="bold")
    console.print(f"|| Source directory: {project_path}", style="bold")
    console.print(f"|| Output file: {output_file}", style="bold")
    console.print(f"|| Excluded items: {exclude_set}", style="bold")

    try:
        with open(output_file, 'w', encoding='utf-8') as md_file:
            # 1. Write main title
            md_file.write(f"# {project_name}\n\n")

            # 2. Generate and write project tree
            console.print("|| Generating file tree...", style="bold")
            md_file.write("```bash\n")
            md_file.write(f"{project_name}/\n")
            for line in generate_tree(project_path, exclude_set):
                md_file.write(f"{line}\n")
            md_file.write("```\n\n")
            console.print("|| File tree generated.", style="bold")

            # 3. Walk through files and write their content
            console.print("|| Reading and writing file contents...", style="bold")
            for root, dirs, files in os.walk(project_path, topdown=True):
                # Ensure we don't descend into excluded directories
                dirs[:] = [d for d in dirs if d not in exclude_set]

                for filename in sorted(files):
                    if filename in exclude_set:
                        continue

                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, project_path)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as file_content:
                            content = file_content.read()
                            lang = get_language_identifier(filename)

                            md_file.write("---\n\n")  # Horizontal separator
                            md_file.write(f"**`{relative_path}`**:\n")
                            md_file.write(f"```{lang}\n")
                            md_file.write(content)
                            md_file.write("\n```\n\n")

                    except UnicodeDecodeError:
                        console.print(f"[red]|| Warning: Cannot read file [/red]'{relative_path}'[red] (probably binary). Skipping.[/]", style="bold")
                    except Exception as e:
                        console.print(f"[red]❌ Error reading file [/red]'{relative_path}'[red]: {e}[/]", style="bold")

            console.print("|| File contents written.", style="bold")

    except IOError as e:
        console.print(f"[red]❌ Error writing to file [/red]'{output_file}'[red]: {e}[/]", style="bold")
    except Exception as e:
        console.print(f"[red]❌ An unexpected error occurred: {e}[/]", style="bold")

    console.print(f"\n|| Success! Codebase compiled into '{output_file}'")

@click.command(name="proj-to-file", context_settings=CONTEXT_SETTINGS)
@click.option('-p', '--project', default='.', help='Root directory of the project to scan.')
@click.option('-o', '--output', default=None, help='Output Markdown file name.')
@click.option('-e', '--exclude', default=DEFAULT_VALUES["exclude"], help='Comma-separated list of files/directories to exclude.')
@click.option('-ee', '--extend-exclude', default="", help='Comma-separated list of files/directories to extend the exclude list.')
def proj_to_file(project: str, output: str, exclude: str, extend_exclude: str):
    """
    Export an entire project directory to a single Markdown file.

    This command scans a project directory and generates a single Markdown
    file containing the file tree structure and all source code with syntax
    highlighting. Useful for documentation, code reviews, or AI analysis.
    """
    exclude_pattern = DEFAULT_VALUES["exclude"]
    project_dir = DEFAULT_VALUES["project"]
    output_path = DEFAULT_VALUES["output"]

    if project:
        project_dir = project
    
    if output:
        output_path = output
    
    if exclude:
        exclude_pattern = exclude
    
    if extend_exclude:
        exclude_pattern += f",{extend_exclude}"

    create_codebase_markdown(project_dir, output_path, exclude_pattern)

add_help_argument(proj_to_file)
