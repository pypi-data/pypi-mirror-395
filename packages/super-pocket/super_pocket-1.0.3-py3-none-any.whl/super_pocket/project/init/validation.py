"""
Input validation for project initialization.

Provides comprehensive validation for project names, paths, template names,
and manifest files to ensure safe and correct project generation.
"""

import os
import re
from pathlib import Path
from typing import Optional


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_project_name(name: str) -> None:
    """
    Validate project name is suitable for a Python project.

    Project names should:
    - Not be empty
    - Start with a letter
    - Contain only letters, numbers, underscores, and hyphens
    - Not be a Python reserved keyword

    Args:
        name: Project name to validate

    Raises:
        ValidationError: If name is invalid
    """
    if not name:
        raise ValidationError("Project name cannot be empty")

    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name):
        raise ValidationError(
            f"Project name '{name}' must start with a letter and contain only "
            "letters, numbers, underscores, and hyphens"
        )

    if name.startswith('_'):
        raise ValidationError("Project name cannot start with underscore")

    # Check for Python reserved keywords
    reserved = [
        'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
        'def', 'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
        'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
        'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try',
        'while', 'with', 'yield'
    ]
    if name.lower() in reserved:
        raise ValidationError(f"Project name '{name}' is a Python reserved keyword")


def validate_output_path(path: Path, allow_existing: bool = False) -> None:
    """
    Validate output path for project creation.

    Checks that:
    - If path exists, it must be a directory and empty (if allow_existing=True)
    - First existing parent directory is writable
    - Path is not a file

    Args:
        path: Path to validate
        allow_existing: If True, allow path to exist (will fail if not empty)

    Raises:
        ValidationError: If path is invalid
    """
    if path.exists():
        if not allow_existing:
            raise ValidationError(f"Path already exists: {path}")

        if not path.is_dir():
            raise ValidationError(f"Path exists but is not a directory: {path}")

        # Check if directory is empty
        if list(path.iterdir()):
            raise ValidationError(f"Directory is not empty: {path}")

    # Find the first existing parent directory
    # We walk up the tree until we find a directory that exists
    # Start by resolving to absolute path to handle relative paths correctly
    parent = path.absolute().parent

    while True:
        if parent.exists():
            if not parent.is_dir():
                raise ValidationError(f"Parent path is not a directory: {parent}")

            # Check write permissions on the first existing parent
            if not os.access(parent, os.W_OK):
                raise ValidationError(f"No write permission for parent directory: {parent}")

            # Found a valid parent, we're good
            return

        # Move up to the next parent
        new_parent = parent.parent
        if new_parent == parent:  # We've reached the root
            break
        parent = new_parent

    # If we get here, we've reached the root without finding an existing directory
    raise ValidationError(f"Cannot find a valid parent directory for: {path}")


def validate_template_name(name: str, available_templates: list[str]) -> None:
    """
    Validate template name exists in available templates.

    Args:
        name: Template name to validate
        available_templates: List of available template names

    Raises:
        ValidationError: If template doesn't exist
    """
    if name not in available_templates:
        raise ValidationError(
            f"Template '{name}' not found. Available templates: "
            f"{', '.join(available_templates)}"
        )


def validate_manifest(manifest_path: Path) -> None:
    """
    Validate manifest file exists and is accessible.

    Args:
        manifest_path: Path to manifest YAML file

    Raises:
        ValidationError: If manifest is invalid
    """
    if not manifest_path.exists():
        raise ValidationError(f"Manifest file not found: {manifest_path}")

    if not manifest_path.is_file():
        raise ValidationError(f"Manifest path is not a file: {manifest_path}")

    # Check read permissions
    if not os.access(manifest_path, os.R_OK):
        raise ValidationError(f"No read permission for manifest file: {manifest_path}")
