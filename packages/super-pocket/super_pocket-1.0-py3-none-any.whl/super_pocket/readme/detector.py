"""Main project detector that orchestrates all analyzers."""

from pathlib import Path
from typing import Optional
from .models import ProjectContext
from .analyzers import PythonAnalyzer


class ProjectDetector:
    """Detect project language and type using multiple analyzers."""

    def __init__(self):
        """Initialize detector with all available analyzers."""
        self.analyzers = [
            PythonAnalyzer(),
            # Future: JavaScriptAnalyzer(), GoAnalyzer(), etc.
        ]

    def detect(self, project_path: Path) -> Optional[ProjectContext]:
        """
        Detect project context by trying all analyzers.

        Args:
            project_path: Path to the project directory

        Returns:
            ProjectContext if detected, None otherwise
        """
        if not project_path.exists() or not project_path.is_dir():
            return None

        # Try each analyzer in order
        for analyzer in self.analyzers:
            context = analyzer.analyze(project_path)
            if context is not None:
                return context

        return None
