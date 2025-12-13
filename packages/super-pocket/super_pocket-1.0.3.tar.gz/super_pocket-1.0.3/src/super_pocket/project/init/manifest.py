"""
Manifest parsing and validation for project templates.

This module defines the data models for template manifests and
provides parsing/validation functionality.
"""
from dataclasses import dataclass, field
from typing import Any
import yaml
from pathlib import Path


@dataclass
class ToolOption:
    """Represents a single option in a tool choice."""
    name: str
    description: str


@dataclass
class ToolChoice:
    """Represents a category of tool choices (e.g., CLI framework)."""
    prompt: str
    default: str
    options: list[ToolOption]


@dataclass
class Feature:
    """Represents a toggleable feature in a template."""
    name: str
    description: str
    default: bool = False


@dataclass
class StructureItem:
    """Represents a file or directory in the project structure."""
    path: str
    type: str = "file"  # "file" or "directory"
    template: str | None = None
    condition: str | None = None


@dataclass
class PostGenAction:
    """Represents a post-generation action to execute."""
    action: str
    condition: str | None = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class TemplateManifest:
    """Complete template manifest with all metadata and configuration."""
    name: str
    display_name: str
    description: str
    python_version: str
    tool_choices: dict[str, ToolChoice]
    features: list[Feature]
    structure: list[StructureItem]
    post_generation: list[PostGenAction]


def parse_manifest(manifest_path: Path) -> TemplateManifest:
    """
    Parse a template manifest from a YAML file.

    Args:
        manifest_path: Path to the YAML manifest file

    Returns:
        Parsed TemplateManifest object

    Raises:
        FileNotFoundError: If manifest file doesn't exist
        ValueError: If manifest is invalid
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, 'r') as f:
        data = yaml.safe_load(f)

    # Parse tool choices
    tool_choices = {}
    for key, choice_data in data.get("tool_choices", {}).items():
        options = [
            ToolOption(**opt) for opt in choice_data["options"]
        ]
        tool_choices[key] = ToolChoice(
            prompt=choice_data["prompt"],
            default=choice_data["default"],
            options=options
        )

    # Parse features
    features = [Feature(**feat) for feat in data.get("features", [])]

    # Parse structure
    structure = []
    for item in data.get("structure", []):
        structure.append(StructureItem(**item))

    # Parse post-generation actions
    post_gen = []
    for action in data.get("post_generation", []):
        if isinstance(action, str):
            # Simple action name only
            post_gen.append(PostGenAction(action=action))
        elif isinstance(action, dict):
            # Action with params - create a copy to avoid mutating input
            action_copy = action.copy()
            action_name = action_copy.pop("action")
            condition = action_copy.pop("condition", None)
            post_gen.append(PostGenAction(
                action=action_name,
                condition=condition,
                params=action_copy
            ))

    return TemplateManifest(
        name=data["name"],
        display_name=data["display_name"],
        description=data["description"],
        python_version=data["python_version"],
        tool_choices=tool_choices,
        features=features,
        structure=structure,
        post_generation=post_gen
    )
