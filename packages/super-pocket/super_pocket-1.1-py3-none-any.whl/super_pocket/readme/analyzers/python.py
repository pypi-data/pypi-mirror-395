"""Python project analyzer."""

import tomllib
from pathlib import Path
from typing import Optional
from ..models import ProjectContext, ProjectType


class PythonAnalyzer:
    """Analyze Python projects to extract context."""

    def analyze(self, project_path: Path) -> Optional[ProjectContext]:
        """
        Analyze a Python project.

        Args:
            project_path: Path to the project directory

        Returns:
            ProjectContext if Python project detected, None otherwise
        """
        pyproject_path = project_path / "pyproject.toml"

        if not pyproject_path.exists():
            return None

        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
        except (OSError, tomllib.TOMLDecodeError):
            return None

        project_data = data.get("project", {})

        # Extract basic info
        project_name = project_data.get("name", project_path.name)
        description = project_data.get("description")
        version = project_data.get("version")
        runtime_version = project_data.get("requires-python")

        # Detect project type
        project_type = self._detect_project_type(project_data, data)

        # Extract dependencies
        dependencies = project_data.get("dependencies", [])

        return ProjectContext(
            project_name=project_name,
            project_path=project_path,
            language="python",
            project_type=project_type,
            description=description,
            version=version,
            runtime_version=runtime_version,
            dependencies=dependencies
        )

    def _detect_project_type(
        self,
        project_data: dict,
        full_data: dict
    ) -> ProjectType:
        """Detect the type of Python project."""
        # Check for CLI tool indicators
        if "scripts" in project_data or "entry_points" in project_data:
            return ProjectType.CLI_TOOL

        # Check for web framework dependencies
        deps = project_data.get("dependencies", [])
        deps_str = " ".join(deps).lower()

        if any(fw in deps_str for fw in ["fastapi", "flask", "django"]):
            return ProjectType.WEB_APP

        # Default to library
        return ProjectType.LIBRARY
