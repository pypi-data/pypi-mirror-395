"""Data models for README generator."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any


class ProjectType(Enum):
    """Types of projects."""
    CLI_TOOL = "cli"
    WEB_APP = "web_app"
    LIBRARY = "library"
    API = "api"


@dataclass
class ProjectContext:
    """Context information about a project for README generation."""

    # Required fields
    project_name: str
    project_path: Path
    language: str
    project_type: ProjectType

    # Optional detection results
    framework: Optional[str] = None
    package_manager: Optional[str] = None
    license_type: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None

    # Environment info
    runtime_version: Optional[str] = None
    has_tests: bool = False
    test_framework: Optional[str] = None
    has_ci: bool = False
    ci_platform: Optional[str] = None
    has_docs: bool = False

    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    system_dependencies: List[str] = field(default_factory=list)

    # Detection confidence (0.0 to 1.0)
    confidence: float = 1.0

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
