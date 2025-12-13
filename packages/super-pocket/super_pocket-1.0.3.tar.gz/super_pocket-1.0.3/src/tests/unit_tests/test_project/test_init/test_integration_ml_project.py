"""
Integration tests for ml-project template.

Tests the complete project generation workflow for the ml-project template,
including different ML frameworks, experiment trackers, and feature combinations.
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
    """Load ml-project manifest"""
    manifest_path = template_base_path / "ml-project.yaml"
    return parse_manifest(manifest_path)


def test_ml_project_quick_mode(temp_output_dir, template_base_path, manifest):
    """Test ml-project template in quick mode (all defaults)"""
    project_name = "test_ml"
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

    generator.set_selections(tool_selections, feature_selections, "Test ML project")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name).exists()
    assert (project_path / "src" / project_name / "train.py").exists()
    assert (project_path / "src" / project_name / "config.py").exists()

    # Verify ML-specific directories
    assert (project_path / "notebooks").exists()
    assert (project_path / "notebooks" / "01_exploration.ipynb").exists()
    assert (project_path / "data").exists()
    assert (project_path / "models").exists()

    # Verify default testing
    assert (project_path / "tests").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results), f"Some file operations failed: {[r.message for r in file_results if not r.success]}"


def test_ml_project_with_pytorch(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with PyTorch framework"""
    project_name = "test_ml_pytorch"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select PyTorch
    tool_selections = {
        "framework": "pytorch",
        "notebook_type": "jupyter",
        "package_manager": "uv",
        "experiment_tracking": "none"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "ML with PyTorch")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()

    # Verify train.py exists (framework-specific)
    train_path = project_path / "src" / project_name / "train.py"
    assert train_path.exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_with_tensorflow(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with TensorFlow framework"""
    project_name = "test_ml_tf"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select TensorFlow
    tool_selections = {
        "framework": "tensorflow",
        "notebook_type": "jupyterlab",
        "package_manager": "poetry",
        "experiment_tracking": "none"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "ML with TensorFlow")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "train.py").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_with_sklearn(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with scikit-learn framework"""
    project_name = "test_ml_sklearn"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Select sklearn
    tool_selections = {
        "framework": "sklearn",
        "notebook_type": "jupyter",
        "package_manager": "pip",
        "experiment_tracking": "none"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "ML with sklearn")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "train.py").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_with_mlflow(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with MLflow experiment tracking"""
    project_name = "test_ml_mlflow"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable MLflow
    tool_selections = {
        "framework": "pytorch",
        "notebook_type": "jupyter",
        "package_manager": "uv",
        "experiment_tracking": "mlflow"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "ML with MLflow")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "train.py").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_with_wandb(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with Weights & Biases tracking"""
    project_name = "test_ml_wandb"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable wandb
    tool_selections = {
        "framework": "tensorflow",
        "notebook_type": "jupyterlab",
        "package_manager": "poetry",
        "experiment_tracking": "wandb"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "ML with wandb")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "src" / project_name / "train.py").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_with_dvc(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with DVC enabled"""
    project_name = "test_ml_dvc"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable DVC
    tool_selections = {
        "framework": "none",
        "notebook_type": "jupyter",
        "package_manager": "uv",
        "experiment_tracking": "none"
    }
    feature_selections = {
        "dvc": True,  # Enable DVC
        "docker": False,
        "testing": True
    }

    generator.set_selections(tool_selections, feature_selections, "ML with DVC")
    results = generator.generate()

    # Verify DVC setup
    assert project_path.exists()
    assert (project_path / ".dvc").exists()
    assert (project_path / ".dvcignore").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_with_docker(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with Docker enabled"""
    project_name = "test_ml_docker"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable Docker
    tool_selections = {
        "framework": "pytorch",
        "notebook_type": "jupyter",
        "package_manager": "pip",
        "experiment_tracking": "none"
    }
    feature_selections = {
        "dvc": False,
        "docker": True,  # Enable Docker
        "testing": True
    }

    generator.set_selections(tool_selections, feature_selections, "ML with Docker")
    results = generator.generate()

    # Verify Docker setup
    assert project_path.exists()
    assert (project_path / "Dockerfile").exists()

    # Verify Dockerfile contains GPU support hints
    dockerfile_content = (project_path / "Dockerfile").read_text()
    assert "python" in dockerfile_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_notebooks_directory(temp_output_dir, template_base_path, manifest):
    """Test that notebooks directory is created properly"""
    project_name = "test_ml_notebooks"
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

    generator.set_selections(tool_selections, feature_selections, "Test notebooks")
    results = generator.generate()

    # Verify notebooks directory
    notebooks_path = project_path / "notebooks"
    assert notebooks_path.exists()
    assert (notebooks_path / "01_exploration.ipynb").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_data_structure(temp_output_dir, template_base_path, manifest):
    """Test that data and models directories are created"""
    project_name = "test_ml_data"
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

    generator.set_selections(tool_selections, feature_selections, "Test data structure")
    results = generator.generate()

    # Verify data and models directories
    assert (project_path / "data").exists()
    assert (project_path / "data" / ".gitkeep").exists()
    assert (project_path / "models").exists()
    assert (project_path / "models" / ".gitkeep").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_ml_project_full_featured(temp_output_dir, template_base_path, manifest):
    """Test ml-project template with all features enabled"""
    project_name = "test_ml_full"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Enable all features
    tool_selections = {
        "framework": "pytorch",
        "notebook_type": "jupyterlab",
        "package_manager": "uv",
        "experiment_tracking": "mlflow"
    }
    feature_selections = {
        feature.name: True  # Enable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Full-featured ML")
    results = generator.generate()

    # Verify all features
    assert project_path.exists()
    assert (project_path / ".dvc").exists()
    assert (project_path / "Dockerfile").exists()
    assert (project_path / "tests").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)
