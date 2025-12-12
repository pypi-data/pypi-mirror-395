"""Tests for interactive UI."""
import pytest
from super_pocket.project.init.interactive import get_default_selections
from super_pocket.project.init.manifest import (
    TemplateManifest,
    ToolChoice,
    ToolOption,
    Feature
)


def test_get_default_selections():
    """Test getting default selections from manifest."""
    manifest = TemplateManifest(
        name="test",
        display_name="Test",
        description="Test",
        python_version=">=3.11",
        tool_choices={
            "framework": ToolChoice(
                prompt="Choose framework",
                default="click",
                options=[
                    ToolOption(name="click", description="Click"),
                    ToolOption(name="typer", description="Typer"),
                ]
            )
        },
        features=[
            Feature(name="testing", description="Testing", default=True),
            Feature(name="docker", description="Docker", default=False),
        ],
        structure=[],
        post_generation=[]
    )

    tool_sel, feat_sel = get_default_selections(manifest)

    assert tool_sel["framework"] == "click"
    assert feat_sel["testing"] is True
    assert feat_sel["docker"] is False
