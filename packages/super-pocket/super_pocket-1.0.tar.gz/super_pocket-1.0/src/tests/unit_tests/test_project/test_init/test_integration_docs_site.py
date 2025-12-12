"""
Integration tests for docs-site template.

Tests the complete project generation workflow for the docs-site template,
including different docs tools (Sphinx, MkDocs, Docusaurus), themes, and features.
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
    """Load docs-site manifest"""
    manifest_path = template_base_path / "docs-site.yaml"
    return parse_manifest(manifest_path)


def test_docs_site_quick_mode(temp_output_dir, template_base_path, manifest):
    """Test docs-site template in quick mode (all defaults - Sphinx)"""
    project_name = "test_docs"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    # Use default selections (quick mode - Sphinx)
    tool_selections = {
        choice_name: choice.default
        for choice_name, choice in manifest.tool_choices.items()
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Test docs site")
    results = generator.generate()

    # Verify project was created
    assert project_path.exists()
    assert (project_path / "README.md").exists()

    # Verify Sphinx structure (default)
    assert (project_path / "docs").exists()
    assert (project_path / "docs" / "source").exists()
    assert (project_path / "docs" / "source" / "conf.py").exists()
    assert (project_path / "docs" / "source" / "index.rst").exists()

    # Verify default features (api_docs, search, deploy_github)
    assert (project_path / ".github" / "workflows" / "deploy.yml").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results), f"Some file operations failed: {[r.message for r in file_results if not r.success]}"


def test_docs_site_with_sphinx(temp_output_dir, template_base_path, manifest):
    """Test docs-site template with Sphinx"""
    project_name = "test_docs_sphinx"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "sphinx",
        "theme": "alabaster",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Docs with Sphinx")
    results = generator.generate()

    # Verify Sphinx structure
    assert project_path.exists()
    assert (project_path / "docs" / "source" / "conf.py").exists()
    assert (project_path / "docs" / "source" / "index.rst").exists()
    assert (project_path / "docs" / "Makefile").exists()

    # Verify conf.py contains Sphinx configuration
    conf_content = (project_path / "docs" / "source" / "conf.py").read_text()
    assert "sphinx" in conf_content.lower() or "extensions" in conf_content

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_with_mkdocs(temp_output_dir, template_base_path, manifest):
    """Test docs-site template with MkDocs"""
    project_name = "test_docs_mkdocs"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "mkdocs",
        "theme": "material",
        "package_manager": "poetry"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Docs with MkDocs")
    results = generator.generate()

    # Verify MkDocs structure
    assert project_path.exists()
    assert (project_path / "mkdocs.yml").exists()
    assert (project_path / "docs").exists()
    assert (project_path / "docs" / "index.md").exists()

    # Verify mkdocs.yml contains MkDocs configuration
    mkdocs_content = (project_path / "mkdocs.yml").read_text()
    assert "site_name" in mkdocs_content or "theme" in mkdocs_content

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_with_docusaurus(temp_output_dir, template_base_path, manifest):
    """Test docs-site template with Docusaurus"""
    project_name = "test_docs_docusaurus"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "docusaurus",
        "theme": "classic",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Docs with Docusaurus")
    results = generator.generate()

    # Verify Docusaurus structure
    assert project_path.exists()
    assert (project_path / "docusaurus.config.js").exists()
    assert (project_path / "sidebars.js").exists()
    assert (project_path / "package.json").exists()
    assert (project_path / "docs").exists()

    # Verify docusaurus.config.js contains Docusaurus configuration
    config_content = (project_path / "docusaurus.config.js").read_text()
    assert "module.exports" in config_content or "export" in config_content

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_sphinx_with_api_docs(temp_output_dir, template_base_path, manifest):
    """Test docs-site Sphinx with API documentation"""
    project_name = "test_docs_api"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "sphinx",
        "theme": "readthedocs",
        "package_manager": "uv"
    }
    feature_selections = {
        "api_docs": True,  # Enable API docs
        "versioning": False,
        "search": True,
        "i18n": False,
        "deploy_github": False
    }

    generator.set_selections(tool_selections, feature_selections, "Docs with API")
    results = generator.generate()

    # Verify API documentation file exists
    assert project_path.exists()
    assert (project_path / "docs" / "source" / "api.rst").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_mkdocs_with_api_docs(temp_output_dir, template_base_path, manifest):
    """Test docs-site MkDocs with API documentation"""
    project_name = "test_mkdocs_api"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "mkdocs",
        "theme": "material",
        "package_manager": "uv"
    }
    feature_selections = {
        "api_docs": True,  # Enable API docs
        "versioning": False,
        "search": True,
        "i18n": False,
        "deploy_github": False
    }

    generator.set_selections(tool_selections, feature_selections, "MkDocs with API")
    results = generator.generate()

    # Verify API documentation file exists
    assert project_path.exists()
    assert (project_path / "docs" / "api.md").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_with_github_pages_deployment(temp_output_dir, template_base_path, manifest):
    """Test docs-site with GitHub Pages deployment"""
    project_name = "test_docs_github"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "sphinx",
        "theme": "readthedocs",
        "package_manager": "uv"
    }
    feature_selections = {
        "api_docs": True,
        "versioning": False,
        "search": True,
        "i18n": False,
        "deploy_github": True  # Enable GitHub Pages
    }

    generator.set_selections(tool_selections, feature_selections, "Docs with GitHub Pages")
    results = generator.generate()

    # Verify GitHub Actions workflow exists
    assert project_path.exists()
    assert (project_path / ".github" / "workflows" / "deploy.yml").exists()

    # Verify workflow contains deployment config
    workflow_content = (project_path / ".github" / "workflows" / "deploy.yml").read_text()
    assert "workflow" in workflow_content.lower() or "deploy" in workflow_content.lower() or "pages" in workflow_content.lower()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_docusaurus_with_i18n(temp_output_dir, template_base_path, manifest):
    """Test docs-site Docusaurus with internationalization"""
    project_name = "test_docs_i18n"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "docusaurus",
        "theme": "classic",
        "package_manager": "uv"
    }
    feature_selections = {
        "api_docs": False,
        "versioning": False,
        "search": True,
        "i18n": True,  # Enable i18n
        "deploy_github": False
    }

    generator.set_selections(tool_selections, feature_selections, "Docs with i18n")
    results = generator.generate()

    # Verify i18n directory exists (Docusaurus only)
    assert project_path.exists()
    assert (project_path / "i18n").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_sphinx_readthedocs_config(temp_output_dir, template_base_path, manifest):
    """Test that Sphinx generates Read the Docs config"""
    project_name = "test_docs_rtd"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "sphinx",
        "theme": "readthedocs",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Sphinx with RTD")
    results = generator.generate()

    # Verify Read the Docs config exists
    assert project_path.exists()
    assert (project_path / ".readthedocs.yml").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_mkdocs_readthedocs_config(temp_output_dir, template_base_path, manifest):
    """Test that MkDocs generates Read the Docs config"""
    project_name = "test_mkdocs_rtd"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "mkdocs",
        "theme": "material",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "MkDocs with RTD")
    results = generator.generate()

    # Verify Read the Docs config exists
    assert project_path.exists()
    assert (project_path / ".readthedocs.yml").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_full_featured_sphinx(temp_output_dir, template_base_path, manifest):
    """Test docs-site Sphinx with all features enabled"""
    project_name = "test_docs_full_sphinx"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "sphinx",
        "theme": "book",
        "package_manager": "poetry"
    }
    feature_selections = {
        feature.name: True  # Enable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Full Sphinx docs")
    results = generator.generate()

    # Verify all features
    assert project_path.exists()
    assert (project_path / "docs" / "source" / "api.rst").exists()
    assert (project_path / ".github" / "workflows" / "deploy.yml").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)


def test_docs_site_minimal_docusaurus(temp_output_dir, template_base_path, manifest):
    """Test docs-site Docusaurus with minimal features"""
    project_name = "test_docs_minimal"
    project_path = temp_output_dir / project_name

    generator = ProjectGenerator(
        manifest=manifest,
        project_name=project_name,
        output_path=project_path,
        template_base_path=template_base_path
    )

    tool_selections = {
        "docs_tool": "docusaurus",
        "theme": "classic",
        "package_manager": "uv"
    }
    feature_selections = {
        feature.name: False  # Disable all features
        for feature in manifest.features
    }

    generator.set_selections(tool_selections, feature_selections, "Minimal Docusaurus")
    results = generator.generate()

    # Verify basic structure exists
    assert project_path.exists()
    assert (project_path / "docusaurus.config.js").exists()

    # Verify optional features are NOT present
    assert not (project_path / "i18n").exists()
    assert not (project_path / ".github").exists()

    # Verify file operations succeeded
    file_results = [r for r in results if "write_file" in str(r.message).lower() or "create_directory" in str(r.message).lower()]
    assert all(result.success for result in file_results)
