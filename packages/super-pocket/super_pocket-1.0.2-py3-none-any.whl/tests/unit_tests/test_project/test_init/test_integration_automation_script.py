"""
Integration tests for automation-script template.

Tests the complete project generation workflow for the automation-script template,
including different schedulers, config formats, and feature combinations.
"""
import pytest
from pathlib import Path
import shutil
import tempfile

from super_pocket.project.init.manifest import parse_manifest
from super_pocket.project.init.engine import ProjectGenerator


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test output"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def template_base_path():
    """Path to template directory"""
    return Path(__file__).parent.parent.parent.parent.parent / "super_pocket" / "project" / "templates"


@pytest.fixture
def manifest(template_base_path):
    """Load automation-script manifest"""
    manifest_path = template_base_path / "automation-script.yaml"
    return parse_manifest(manifest_path)


def test_automation_script_quick_mode(temp_output_dir, template_base_path, manifest):
    """Test automation-script template in quick mode (all defaults)"""
    project_name = "test_automation"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Use default selections (quick mode)
    tool_selections = {
        choice_name: choice.default
        for choice_name, choice in manifest.tool_choices.items()
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Test automation script")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name).exists()
    assert (project_path / "src" / project_name / "runner.py").exists()
    assert (project_path / "src" / project_name / "tasks.py").exists()
    assert (project_path / "src" / project_name / "config_loader.py").exists()

    # Verify default config format (yaml)
    assert (project_path / "config.yaml").exists()

    # Verify default features (logging + testing)
    assert (project_path / "src" / project_name / "logging_config.py").exists()
    assert (project_path / "tests").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results), f"Some file operations failed: {[r.message for r in file_results if not r.success]}"


def test_automation_script_with_cron(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with cron scheduler"""
    project_name = "test_auto_cron"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select cron
    tool_selections = {
        "scheduler": "cron",
        "config_format": "yaml",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with cron")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "runner.py").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_apscheduler(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with APScheduler"""
    project_name = "test_auto_aps"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select APScheduler
    tool_selections = {
        "scheduler": "apscheduler",
        "config_format": "toml",
        "package_manager": "poetry"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with APScheduler")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "runner.py").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_yaml_config(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with YAML config"""
    project_name = "test_auto_yaml"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "scheduler": "none",
        "config_format": "yaml",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with YAML")
    results = generator.generate()

    # Verify YAML config exists
    assert (project_path / "config.yaml").exists()

    # Verify config_loader.py exists
    config_loader_path = project_path / "src" / project_name / "config_loader.py"
    assert config_loader_path.exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_toml_config(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with TOML config"""
    project_name = "test_auto_toml"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "scheduler": "none",
        "config_format": "toml",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with TOML")
    results = generator.generate()

    # Verify TOML config exists
    assert (project_path / "config.toml").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_json_config(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with JSON config"""
    project_name = "test_auto_json"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "scheduler": "none",
        "config_format": "json",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with JSON")
    results = generator.generate()

    # Verify JSON config exists
    assert (project_path / "config.json").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_env_config(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with .env config"""
    project_name = "test_auto_env"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "scheduler": "none",
        "config_format": "env",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with .env")
    results = generator.generate()

    # Verify .env config exists
    assert (project_path / ".env").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_notifications(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with notifications enabled"""
    project_name = "test_auto_notif"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "scheduler": "none",
        "config_format": "yaml",
        "package_manager": "uv"
    }
    feature_selections = {
        "logging": True,
        "notifications": True,  # Enable notifications
        "testing": True,
        "docker": False,
        "systemd": False
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with notifications")
    results = generator.generate()

    # Verify notifications.py exists
    assert (project_path / "src" / project_name / "notifications.py").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_systemd(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with systemd service"""
    project_name = "test_auto_systemd"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "scheduler": "none",
        "config_format": "yaml",
        "package_manager": "uv"
    }
    feature_selections = {
        "logging": True,
        "notifications": False,
        "testing": True,
        "docker": False,
        "systemd": True  # Enable systemd
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with systemd")
    results = generator.generate()

    # Verify systemd service file exists
    service_file = project_path / f"{project_name}.service"
    assert service_file.exists()

    # Verify service file contains systemd config
    service_content = service_file.read_text()
    assert "[Unit]" in service_content or "Service" in service_content

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_with_docker(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with Docker"""
    project_name = "test_auto_docker"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "scheduler": "apscheduler",
        "config_format": "toml",
        "package_manager": "poetry"
    }
    feature_selections = {
        "logging": True,
        "notifications": False,
        "testing": True,
        "docker": True,  # Enable Docker
        "systemd": False
    }

    generator.set_selections(tool_selections, feature_selections, "Automation with Docker")
    results = generator.generate()

    # Verify Docker files exist
    assert (project_path / "Dockerfile").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_automation_script_full_featured(temp_output_dir, template_base_path, manifest):
    """Test automation-script template with all features enabled"""
    project_name = "test_auto_full"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable all features
    tool_selections = {
        "scheduler": "apscheduler",
        "config_format": "yaml",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: True  # Enable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Full-featured automation")
    results = generator.generate()

    # Verify all feature-specific files exist
    assert project_path.exists()
    assert (project_path / "src" / project_name / "logging_config.py").exists()
    assert (project_path / "src" / project_name / "notifications.py").exists()
    assert (project_path / "tests").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / f"{project_name}.service").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)
