"""
Templates and cheatsheets management module.

Provides CLI commands to:
- List available templates and cheatsheets
- View/display content in terminal
- Copy templates to user projects
- Validate template syntax
"""

from pathlib import Path

# Directories for templates and cheatsheets
TEMPLATES_DIR = Path(__file__).parent / "templates"
CHEATSHEETS_DIR = Path(__file__).parent / "cheatsheets"

__all__ = ["TEMPLATES_DIR", "CHEATSHEETS_DIR"]
