"""Main README generator."""

from typing import List
from .models import ProjectContext
from .templates.base import (
    TitleSection,
    PrerequisitesSection,
    InstallationSection,
    ProjectStructureSection
)
from .badges import BadgeGenerator, BadgeType


class ReadmeGenerator:
    """Generate README files from project context."""

    def __init__(self):
        """Initialize generator with section templates."""
        self.badge_generator = BadgeGenerator()

        # Baseline sections (always included)
        self.baseline_sections = {
            "title": TitleSection(),
            "prerequisites": PrerequisitesSection(),
            "installation": InstallationSection(),
            "structure": ProjectStructureSection()
        }

        # Optional sections
        self.optional_sections = {
            "running-tests": self._running_tests_section,
        }

    def generate(
        self,
        context: ProjectContext,
        selected_badges: List[BadgeType],
        selected_sections: List[str]
    ) -> str:
        """
        Generate README content.

        Args:
            context: Project context
            selected_badges: List of badge types to include
            selected_sections: List of optional section IDs to include

        Returns:
            Complete README markdown content
        """
        sections = []

        # Title section
        sections.append(self.baseline_sections["title"].generate(context))
        sections.append("")

        # Badges
        if selected_badges:
            badge_lines = []
            for badge_type in selected_badges:
                badge_md = self.badge_generator.generate_badge(badge_type, context)
                if badge_md:
                    badge_lines.append(badge_md)

            if badge_lines:
                sections.append(" ".join(badge_lines))
                sections.append("")

        # Baseline sections
        sections.append(self.baseline_sections["prerequisites"].generate(context))
        sections.append("")
        sections.append(self.baseline_sections["installation"].generate(context))
        sections.append("")
        sections.append(self.baseline_sections["structure"].generate(context))
        sections.append("")

        # Optional sections
        for section_id in selected_sections:
            if section_id in self.optional_sections:
                section_func = self.optional_sections[section_id]
                sections.append(section_func(context))
                sections.append("")

        return "\n".join(sections)

    def _running_tests_section(self, context: ProjectContext) -> str:
        """Generate running tests section."""
        lines = ["## Running Tests"]
        lines.append("")
        lines.append("```bash")

        if context.language == "python":
            if context.test_framework == "pytest":
                lines.append("pytest")
            else:
                lines.append("python -m pytest")

        lines.append("```")

        return "\n".join(lines)
