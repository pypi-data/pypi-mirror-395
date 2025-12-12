"""
Project generation engine.

Orchestrates the project generation process including file creation,
template rendering, and post-generation actions.
"""
from pathlib import Path
from typing import Any

from .manifest import TemplateManifest, StructureItem
from .renderers import build_context, render_template_file, render_template_string
from .actions import ActionExecutor, ActionResult
from rich.console import Console

console = Console()


class ProjectGenerator:
    """Generates projects from templates."""

    def __init__(
        self,
        manifest: TemplateManifest,
        project_name: str,
        output_path: Path,
        template_base_path: Path | None = None
    ):
        """
        Initialize project generator.

        Args:
            manifest: Template manifest
            project_name: Name of the project to generate
            output_path: Where to generate the project
            template_base_path: Base path for template files
        """
        self.manifest = manifest
        self.project_name = project_name
        self.output_path = output_path
        self.template_base_path = template_base_path or Path(__file__).parent.parent / "templates"

        self.tool_selections: dict[str, str] = {}
        self.feature_selections: dict[str, bool] = {}
        self.description: str = ""

        self.action_executor = ActionExecutor(output_path)

    def set_selections(
        self,
        tool_selections: dict[str, str],
        feature_selections: dict[str, bool],
        description: str
    ):
        """
        Set user selections.

        Args:
            tool_selections: Selected tools for each choice category
            feature_selections: Enabled/disabled features
            description: Project description
        """
        self.tool_selections = tool_selections
        self.feature_selections = feature_selections
        self.description = description

    def generate(self) -> list[ActionResult]:
        """
        Generate the project with comprehensive error handling.

        Returns:
            List of action results
        """
        results = []

        try:
            # Build context
            context = build_context(
                project_name=self.project_name,
                description=self.description,
                tool_choices=self.tool_selections,
                features=self.feature_selections,
                python_version=self.manifest.python_version
            )

            # Create output directory
            try:
                self.output_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                results.append(ActionResult(
                    success=False,
                    message=f"Failed to create output directory: {self.output_path}",
                    error=str(e)
                ))
                return results

            # Generate structure
            for item in self.manifest.structure:
                try:
                    # Check condition if present
                    if item.condition and not self._evaluate_condition(item.condition, context):
                        continue

                    # Render path template
                    rendered_path = render_template_string(item.path, context)

                    # Skip if path is empty (from conditional template)
                    if not rendered_path or rendered_path.isspace():
                        continue

                    full_path = self.output_path / rendered_path

                    if item.type == "directory":
                        result = self.action_executor.create_directory(full_path)
                        results.append(result)
                    else:  # file
                        if item.template:
                            # Render template field name (in case it has variables)
                            rendered_template = render_template_string(item.template, context)

                            # Skip if template is empty (from conditional template)
                            if not rendered_template or rendered_template.isspace():
                                continue

                            # Render from template file
                            template_path = self.template_base_path / self.manifest.name / rendered_template
                            if template_path.exists():
                                content = render_template_file(template_path, context)
                            else:
                                # If template doesn't exist, log warning but continue
                                console.print(f"[yellow]Warning: Template not found: {template_path}[/yellow]")
                                content = ""
                        else:
                            # Create empty file
                            content = ""

                        result = self.action_executor.write_file(full_path, content)
                        results.append(result)

                    # Log error but continue with next items
                    if not result.success:
                        console.print(f"[yellow]Warning:[/yellow] {result.message}")
                        if result.error:
                            console.print(f"  Error details: {result.error}")

                except Exception as e:
                    error_result = ActionResult(
                        success=False,
                        message=f"Failed to process item {item.path}",
                        error=str(e)
                    )
                    results.append(error_result)
                    console.print(f"[yellow]Warning:[/yellow] {error_result.message}")
                    # Continue with next items

            # Execute post-generation actions
            for action in self.manifest.post_generation:
                try:
                    # Check condition
                    if action.condition and not self._evaluate_condition(action.condition, context):
                        continue

                    result = self._execute_action(action.action, action.params, context)
                    results.append(result)

                    # Log error but continue with next actions
                    if not result.success:
                        console.print(f"[yellow]Warning:[/yellow] {result.message}")
                        if result.error:
                            console.print(f"  Error details: {result.error}")

                except Exception as e:
                    error_result = ActionResult(
                        success=False,
                        message=f"Failed to execute action {action.action}",
                        error=str(e)
                    )
                    results.append(error_result)
                    console.print(f"[yellow]Warning:[/yellow] {error_result.message}")
                    # Continue with next actions

            return results

        except Exception as e:
            console.print(f"[red]Fatal error during generation:[/red] {e}")
            results.append(ActionResult(
                success=False,
                message="Fatal error during project generation",
                error=str(e)
            ))
            raise

    def _evaluate_condition(self, condition: str, context: dict) -> bool:
        """
        Evaluate a condition string.

        Args:
            condition: Condition to evaluate (e.g., "features.testing")
            context: Context dictionary

        Returns:
            True if condition is met, False otherwise
        """
        # Simple dot-notation evaluation
        parts = condition.split(".")
        value = context
        for part in parts:
            value = value.get(part, False)
            if value is False:
                return False
        return bool(value)

    def _execute_action(self, action_name: str, params: dict, context: dict) -> ActionResult:
        """
        Execute a post-generation action.

        Args:
            action_name: Name of the action
            params: Action parameters
            context: Rendering context

        Returns:
            ActionResult
        """
        if action_name == "git_init":
            return self.action_executor.execute_git_init()
        elif action_name == "create_venv":
            package_manager = params.get("package_manager", "uv")
            # Render template variables in params
            if isinstance(package_manager, str) and "{{" in package_manager:
                package_manager = render_template_string(package_manager, context)
            return self.action_executor.create_venv(package_manager)
        elif action_name == "install_dependencies":
            package_manager = params.get("package_manager", "uv")
            if isinstance(package_manager, str) and "{{" in package_manager:
                package_manager = render_template_string(package_manager, context)
            dev = params.get("dev", True)
            return self.action_executor.install_dependencies(package_manager, dev)
        elif action_name == "run_command":
            command = params.get("command", "")
            command = render_template_string(command, context)
            # Convert command string to list for safe execution
            # Split by spaces but preserve quoted strings
            import shlex
            command_list = shlex.split(command) if isinstance(command, str) else command
            return self.action_executor.run_command(command_list)
        elif action_name == "display_next_steps":
            return ActionResult(
                success=True,
                message="Project generated successfully!"
            )
        else:
            return ActionResult(
                success=False,
                message=f"Unknown action: {action_name}"
            )