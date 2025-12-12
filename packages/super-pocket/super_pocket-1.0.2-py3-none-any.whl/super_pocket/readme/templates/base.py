"""Base README sections that are included in all READMEs."""

from abc import ABC, abstractmethod
from ..models import ProjectContext


class Section(ABC):
    """Base class for README sections."""

    @abstractmethod
    def generate(self, context: ProjectContext) -> str:
        """Generate the section content."""
        pass


class TitleSection(Section):
    """Generate project title and description section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate title section."""
        lines = [f"# {context.project_name}"]

        if context.description:
            lines.append("")
            lines.append(context.description)

        return "\n".join(lines)


class PrerequisitesSection(Section):
    """Generate prerequisites section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate prerequisites section."""
        lines = ["## Prerequisites"]
        lines.append("")

        # Runtime version
        if context.runtime_version:
            if context.language == "python":
                version = context.runtime_version.replace(">=", "")
                lines.append(f"- Python {version}+")
            elif context.language == "javascript":
                lines.append(f"- Node.js {context.runtime_version}+")

        # Package manager
        if context.package_manager:
            lines.append(f"- {context.package_manager}")

        # System dependencies
        for dep in context.system_dependencies:
            lines.append(f"- {dep}")

        return "\n".join(lines)


class InstallationSection(Section):
    """Generate installation instructions section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate installation section."""
        lines = ["## Installation"]
        lines.append("")
        lines.append("```bash")
        lines.append("# Clone the repository")
        lines.append(f"git clone <repository-url>")
        lines.append(f"cd {context.project_name}")
        lines.append("")

        # Language-specific installation
        if context.language == "python":
            if context.package_manager == "uv":
                lines.append("# Install dependencies with uv")
                lines.append("uv sync")
            else:
                lines.append("# Create virtual environment")
                lines.append("python -m venv .venv")
                lines.append("source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
                lines.append("")
                lines.append("# Install package")
                lines.append("pip install -e .")

        lines.append("```")

        return "\n".join(lines)


class ProjectStructureSection(Section):
    """Generate project structure section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate project structure section."""
        lines = ["## Project Structure"]
        lines.append("")
        lines.append("```")
        lines.append(f"{context.project_name}/")

        # Basic structure based on language
        if context.language == "python":
            pkg_name = context.project_name.replace("-", "_")
            lines.append(f"├── {pkg_name}/        # Source code")
            lines.append(f"├── tests/            # Test suite")
            if context.has_docs:
                lines.append(f"├── docs/             # Documentation")
            lines.append(f"└── pyproject.toml    # Project configuration")

        lines.append("```")

        return "\n".join(lines)
