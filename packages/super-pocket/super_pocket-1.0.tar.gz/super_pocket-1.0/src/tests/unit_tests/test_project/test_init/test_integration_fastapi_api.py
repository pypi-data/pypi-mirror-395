"""
Integration tests for fastapi-api template.

Tests the complete project generation workflow for the fastapi-api template,
including different package managers and feature combinations.
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
    """Load fastapi-api manifest"""
    manifest_path = template_base_path / "fastapi-api.yaml"
    return parse_manifest(manifest_path)


def test_fastapi_quick_mode(temp_output_dir, template_base_path, manifest):
    """Test fastapi-api template in quick mode (all defaults)"""
    project_name = "test_api"
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

    generator.set_selections(tool_selections, feature_selections, "Test FastAPI project")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name).exists()
    assert (project_path / "src" / project_name / "main.py").exists()
    assert (project_path / "src" / project_name / "schemas.py").exists()
    assert (project_path / "src" / project_name / "routers").exists()
    assert (project_path / "pyproject.toml").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / ".env.example").exists()

    # Verify default features (database + migrations + testing)
    assert (project_path / "src" / project_name / "models.py").exists()
    assert (project_path / "src" / project_name / "database.py").exists()
    assert (project_path / "alembic").exists()
    assert (project_path / "tests").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results), f"Some file operations failed: {[r.message for r in file_results if not r.success]}"


def test_fastapi_with_auth(temp_output_dir, template_base_path, manifest):
    """Test fastapi-api template with authentication enabled"""
    project_name = "test_api_auth"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable auth
    tool_selections = {
        "package_manager": "uv"
    }
    feature_selections = {
        "database": True,
        "migrations": True,
        "auth": True,  # Enable auth
        "docker": False,
        "testing": True,
        "github_actions": False,
        "pip_requirements": False
    }

    generator.set_selections(tool_selections, feature_selections, "API with auth")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()

    # Verify auth.py exists
    assert (project_path / "src" / project_name / "auth.py").exists()

    # Verify auth.py contains JWT-related code
    auth_content = (project_path / "src" / project_name / "auth.py").read_text()
    assert "jwt" in auth_content.lower() or "token" in auth_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_fastapi_with_docker(temp_output_dir, template_base_path, manifest):
    """Test fastapi-api template with Docker enabled"""
    project_name = "test_api_docker"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable docker
    tool_selections = {
        "package_manager": "poetry"
    }
    feature_selections = {
        "database": True,
        "migrations": False,
        "auth": False,
        "docker": True,  # Enable docker
        "testing": True,
        "github_actions": False,
        "pip_requirements": False
    }

    generator.set_selections(tool_selections, feature_selections, "API with Docker")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()

    # Verify Docker files exist
    assert (project_path / "Dockerfile").exists()
    assert (project_path / "docker-compose.yml").exists()

    # Verify Docker content
    dockerfile_content = (project_path / "Dockerfile").read_text()
    assert "python" in dockerfile_content.lower()

    compose_content = (project_path / "docker-compose.yml").read_text()
    assert "version" in compose_content or "services" in compose_content

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_fastapi_minimal(temp_output_dir, template_base_path, manifest):
    """Test fastapi-api template with minimal features"""
    project_name = "test_api_minimal"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Disable most features
    tool_selections = {
        "package_manager": "pip"
    }
    feature_selections = {
        "database": False,
        "migrations": False,
        "auth": False,
        "docker": False,
        "testing": False,
        "github_actions": False,
        "pip_requirements": True  # Enable only pip requirements
    }

    generator.set_selections(tool_selections, feature_selections, "Minimal API")
    results = generator.generate()

    # Verify basic structure exists
    assert project_path.exists()
    assert (project_path / "src" / project_name / "main.py").exists()
    assert (project_path / "requirements.txt").exists()

    # Verify optional files do NOT exist
    assert not (project_path / "src" / project_name / "models.py").exists()
    assert not (project_path / "src" / project_name / "database.py").exists()
    assert not (project_path / "src" / project_name / "auth.py").exists()
    assert not (project_path / "alembic").exists()
    assert not (project_path / "tests").exists()
    assert not (project_path / "Dockerfile").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_fastapi_full_featured(temp_output_dir, template_base_path, manifest):
    """Test fastapi-api template with all features enabled"""
    project_name = "test_api_full"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable all features
    tool_selections = {
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: True  # Enable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Full-featured API")
    results = generator.generate()

    # Verify all feature-specific files exist
    assert project_path.exists()
    assert (project_path / "src" / project_name / "models.py").exists()
    assert (project_path / "src" / project_name / "database.py").exists()
    assert (project_path / "src" / project_name / "auth.py").exists()
    assert (project_path / "alembic").exists()
    assert (project_path / "tests").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / ".github" / "workflows" / "ci.yml").exists()
    assert (project_path / "requirements.txt").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_fastapi_routers_structure(temp_output_dir, template_base_path, manifest):
    """Test that FastAPI routers directory is properly structured"""
    project_name = "test_api_routers"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        choice_name: choice.default
        for choice_name, choice in manifest.tool_choices.items()
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Test routers")
    results = generator.generate()

    # Verify routers structure
    routers_path = project_path / "src" / project_name / "routers"
    assert routers_path.exists()
    assert (routers_path / "__init__.py").exists()
    assert (routers_path / "items.py").exists()

    # Verify router file contains FastAPI router code
    router_content = (routers_path / "items.py").read_text()
    assert "APIRouter" in router_content or "router" in router_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_fastapi_with_poetry_package_manager(temp_output_dir, template_base_path, manifest):
    """Test fastapi-api with Poetry package manager"""
    project_name = "test_api_poetry"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "package_manager": "poetry"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "API with Poetry")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "pyproject.toml").exists()

    # Verify pyproject.toml contains poetry config
    pyproject_content = (project_path / "pyproject.toml").read_text()
    assert "poetry" in pyproject_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)
