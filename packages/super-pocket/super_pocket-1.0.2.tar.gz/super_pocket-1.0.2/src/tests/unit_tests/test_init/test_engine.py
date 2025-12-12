"""Tests for project generation engine."""
import pytest
import tempfile
from pathlib import Path
from super_pocket.project.init.engine import ProjectGenerator
from super_pocket.project.init.manifest import (
    TemplateManifest,
    ToolChoice,
    ToolOption,
    Feature,
    StructureItem,
    PostGenAction
)


def test_project_generator_initialization(tmp_path):
    """Test ProjectGenerator initialization."""
    manifest = TemplateManifest(
        name="test-template",
        display_name="Test Template",
        description="A test template",
        python_version=">=3.11",
        tool_choices={},
        features=[],
        structure=[],
        post_generation=[]
    )

    generator = ProjectGenerator(
        manifest=manifest,
        project_name="test_project",
        output_path=tmp_path
    )

    assert generator.manifest == manifest
    assert generator.project_name == "test_project"
    assert generator.output_path == tmp_path


def test_generate_simple_structure(tmp_path):
    """Test generating a simple project structure."""
    manifest = TemplateManifest(
        name="test-template",
        display_name="Test Template",
        description="A test template",
        python_version=">=3.11",
        tool_choices={},
        features=[],
        structure=[
            StructureItem(path="src/{{ project_name }}", type="directory"),
            StructureItem(path="README.md", type="file", template=None),
        ],
        post_generation=[]
    )

    generator = ProjectGenerator(
        manifest=manifest,
        project_name="test_project",
        output_path=tmp_path
    )

    generator.set_selections({}, {}, "Test description")

    # Generate the project
    results = generator.generate()

    # Verify directory was created
    assert (tmp_path / "src" / "test_project").exists()
    assert (tmp_path / "src" / "test_project").is_dir()

    # Verify file was created
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "README.md").is_file()

    # Verify results
    assert len(results) == 2  # 1 directory + 1 file
    assert all(r.success for r in results)
