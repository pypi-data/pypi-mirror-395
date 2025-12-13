"""Badge generation for README files."""

from enum import Enum
from typing import List, Optional
from .models import ProjectContext


class BadgeType(Enum):
    """Types of badges that can be generated."""
    PYTHON_VERSION = "python_version"
    NODE_VERSION = "node_version"
    LICENSE = "license"
    BUILD_STATUS = "build_status"
    COVERAGE = "coverage"
    DOCS = "docs"
    PACKAGE_VERSION = "package_version"


class BadgeGenerator:
    """Generate badge markdown for README files."""

    def get_available_badges(self, context: ProjectContext) -> List[BadgeType]:
        """
        Get list of badges that can be generated for this project.

        Args:
            context: Project context

        Returns:
            List of available badge types
        """
        badges = []

        # Language version badges
        if context.language == "python" and context.runtime_version:
            badges.append(BadgeType.PYTHON_VERSION)
        elif context.language == "javascript" and context.runtime_version:
            badges.append(BadgeType.NODE_VERSION)

        # License badge
        if context.license_type:
            badges.append(BadgeType.LICENSE)

        # CI/CD badge
        if context.has_ci:
            badges.append(BadgeType.BUILD_STATUS)

        # Coverage badge
        if context.has_tests:
            badges.append(BadgeType.COVERAGE)

        # Documentation badge
        if context.has_docs:
            badges.append(BadgeType.DOCS)

        return badges

    def generate_badge(
        self,
        badge_type: BadgeType,
        context: ProjectContext
    ) -> Optional[str]:
        """
        Generate markdown for a specific badge.

        Args:
            badge_type: Type of badge to generate
            context: Project context

        Returns:
            Badge markdown or None if not available
        """
        if badge_type == BadgeType.PYTHON_VERSION:
            return self._python_version_badge(context)
        elif badge_type == BadgeType.LICENSE:
            return self._license_badge(context)
        elif badge_type == BadgeType.BUILD_STATUS:
            return self._build_status_badge(context)

        return None

    def _python_version_badge(self, context: ProjectContext) -> str:
        """Generate Python version badge."""
        version = context.runtime_version or "3.11+"
        # Extract major.minor from version string like ">=3.11"
        version_num = version.replace(">=", "").replace(">", "").strip()

        return (
            f"[![Python Version](https://img.shields.io/badge/"
            f"python-{version_num}%2B-blue.svg)]"
            f"(https://www.python.org/downloads/)"
        )

    def _license_badge(self, context: ProjectContext) -> str:
        """Generate license badge."""
        license_type = context.license_type or "MIT"

        return (
            f"[![License: {license_type}]"
            f"(https://img.shields.io/badge/License-{license_type}-green.svg)]"
            f"(https://opensource.org/licenses/{license_type})"
        )

    def _build_status_badge(self, context: ProjectContext) -> str:
        """Generate build status badge."""
        # Placeholder - would need repo info
        return (
            f"[![Build Status](https://img.shields.io/github/actions/"
            f"workflow/status/USER/REPO/ci.yml?branch=main)]"
            f"(https://github.com/USER/REPO/actions)"
        )
