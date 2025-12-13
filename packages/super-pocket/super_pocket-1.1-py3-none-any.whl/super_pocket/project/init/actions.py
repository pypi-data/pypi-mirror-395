"""
Post-generation actions execution.

Handles git initialization, virtual environment creation,
dependency installation, and other post-generation tasks.
"""
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ActionResult:
    """Result of an action execution."""
    success: bool
    message: str
    error: str | None = None


class ActionExecutor:
    """Executes post-generation actions."""

    def __init__(self, project_path: Path):
        """
        Initialize action executor.

        Args:
            project_path: Path to the generated project
        """
        self.project_path = project_path

    def execute_git_init(self) -> ActionResult:
        """
        Initialize git repository.

        Returns:
            ActionResult with execution status
        """
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            return ActionResult(
                success=True,
                message="Initialized git repository"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message="Failed to initialize git repository",
                error=str(e)
            )

    def create_directory(self, path: Path) -> ActionResult:
        """
        Create a directory and all parent directories.

        Args:
            path: Directory path to create

        Returns:
            ActionResult with execution status
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return ActionResult(
                success=True,
                message=f"Created directory: {path}"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to create directory: {path}",
                error=str(e)
            )

    def write_file(self, path: Path, content: str) -> ActionResult:
        """
        Write content to a file.

        Args:
            path: File path
            content: File content

        Returns:
            ActionResult with execution status
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return ActionResult(
                success=True,
                message=f"Created file: {path}"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to write file: {path}",
                error=str(e)
            )

    def create_venv(self, package_manager: str = "uv") -> ActionResult:
        """
        Create virtual environment.

        Args:
            package_manager: Package manager to use (uv, poetry, pip)

        Returns:
            ActionResult with execution status
        """
        try:
            if package_manager == "uv":
                cmd = ["uv", "venv"]
            elif package_manager == "poetry":
                cmd = ["poetry", "env", "use", "python"]
            else:  # pip
                cmd = ["python", "-m", "venv", ".venv"]

            subprocess.run(
                cmd,
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            return ActionResult(
                success=True,
                message=f"Created virtual environment with {package_manager}"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message=f"Failed to create virtual environment",
                error=str(e)
            )

    def install_dependencies(self, package_manager: str = "uv", dev: bool = True) -> ActionResult:
        """
        Install project dependencies.

        Args:
            package_manager: Package manager to use
            dev: Whether to install dev dependencies

        Returns:
            ActionResult with execution status
        """
        try:
            if package_manager == "uv":
                cmd = ["uv", "sync"]
            elif package_manager == "poetry":
                cmd = ["poetry", "install"]
                if not dev:
                    cmd.append("--no-dev")
            else:  # pip
                cmd = ["pip", "install", "-r", "requirements.txt"]

            subprocess.run(
                cmd,
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            return ActionResult(
                success=True,
                message=f"Installed dependencies with {package_manager}"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message="Failed to install dependencies",
                error=str(e)
            )

    def run_command(self, command: list[str]) -> ActionResult:
        """
        Run a command safely without shell injection risk.

        Args:
            command: Command as list of strings (e.g., ["git", "init"])

        Returns:
            ActionResult with execution status
        """
        try:
            subprocess.run(
                command,
                cwd=self.project_path,
                check=True,
                capture_output=True,
                text=True
            )
            return ActionResult(
                success=True,
                message=f"Executed: {' '.join(command)}"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message=f"Command failed: {' '.join(command)}",
                error=str(e)
            )
