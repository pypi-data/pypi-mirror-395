"""Tests for post-generation actions."""
import pytest
import tempfile
from pathlib import Path
from super_pocket.project.init.actions import ActionExecutor


def test_git_init_action(tmp_path):
    """Test git init action."""
    executor = ActionExecutor(project_path=tmp_path)

    result = executor.execute_git_init()

    assert result.success is True
    assert (tmp_path / ".git").exists()


def test_create_directory_action(tmp_path):
    """Test directory creation action."""
    executor = ActionExecutor(project_path=tmp_path)

    test_dir = tmp_path / "src" / "my_package"
    executor.create_directory(test_dir)

    assert test_dir.exists()
    assert test_dir.is_dir()
