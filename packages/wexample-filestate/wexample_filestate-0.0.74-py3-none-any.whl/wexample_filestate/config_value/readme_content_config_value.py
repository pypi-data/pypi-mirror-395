from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.config_value.aggregated_templates_config_value import (
    AggregatedTemplatesConfigValue,
)

if TYPE_CHECKING:
    from pathlib import Path

    from jinja2 import Environment


@base_class
class ReadmeContentConfigValue(AggregatedTemplatesConfigValue):
    """Base class for README content generation.

    Handles pure template rendering logic without any knowledge of workdir or suite.
    Subclasses must implement template search paths and context building.
    """

    @staticmethod
    def _format_dependencies_list(dependencies: list[str]) -> str:
        """Format dependencies as a Markdown list.

        Args:
            dependencies: List of dependency strings

        Returns:
            Formatted Markdown list
        """
        return "\n".join([f"- {dep}" for dep in dependencies])

    def get_templates(self) -> list[str] | None:
        """Generate README content from templates.

        This method orchestrates the entire README generation process.
        """
        context = self._get_template_context()
        section_names = self._get_section_names()

        # Collect available sections
        available_sections = []
        for section_name in section_names:
            # Exclude these sections from table of content.
            if section_name not in ["title", "table-of-contents"]:
                if self._section_exists(section_name):
                    available_sections.append(
                        {
                            "name": section_name,
                            "title": self._section_name_to_title(section_name),
                            "anchor": section_name.replace("_", "-"),
                        }
                    )

        context["available_sections"] = available_sections

        # Render in order
        rendered_content = ""
        for section_name in section_names:
            section_content = self._render_readme_section(section_name, context)
            if section_content:
                rendered_content += f"{section_content}\n\n"

        return [rendered_content]

    def _get_readme_search_paths(self) -> list[Path]:
        """Return list of paths to search for README templates.

        Must be implemented by subclasses.

        Returns:
            List of paths to search for templates
        """
        return []

    def _get_section_names(self) -> list[str]:
        """Return the list of section names to include in the README.

        Must be implemented by subclasses.

        Returns:
            List of section names in order
        """
        return [
            "title",
            "table-of-contents",
        ]

    def _get_template_context(self) -> dict:
        """Build the template context with all variables.

        Must be implemented by subclasses.

        Returns:
            Dictionary of template variables
        """
        return {}

    def _register_jinja_filters(self, env: Environment) -> None:
        from wexample_helpers.helpers.string import string_convert_case_map

        filters = string_convert_case_map()

        # Register each filter into Jinja
        for key, func in filters.items():
            env.filters[f"to_{key}"] = func

    def _render_readme_section(self, section_name: str, context: dict) -> str | None:
        """Render a README section from template files.

        Searches for section_name.md.j2 (Jinja2 template) first,
        then falls back to section_name.md (plain Markdown with Jinja2 variables).

        Args:
            section_name: Name of the section to render
            context: Template context variables

        Returns:
            Rendered section content or None if not found
        """
        from jinja2 import Environment, FileSystemLoader, TemplateNotFound

        search_paths = self._get_readme_search_paths()

        # Try .md.j2 first
        for search_path in search_paths:
            if not search_path.exists():
                continue

            env = Environment(loader=FileSystemLoader(str(search_path)))
            self._register_jinja_filters(env)
            try:
                template = env.get_template(f"{section_name}.md.j2")
                return template.render(context)
            except TemplateNotFound:
                pass

        # Then try .md
        for search_path in search_paths:
            md_path = search_path / f"{section_name}.md"
            if md_path.exists():
                content = md_path.read_text(encoding="utf-8")
                env = Environment(loader=FileSystemLoader(str(search_path)))
                self._register_jinja_filters(env)
                template = env.from_string(content)
                return template.render(context)

        return None

    def _section_exists(self, section_name: str) -> bool:
        """Check if a README section template exists.

        Args:
            section_name: Name of the section to check

        Returns:
            True if section template exists, False otherwise
        """
        for search_path in self._get_readme_search_paths():
            if (search_path / f"{section_name}.md.j2").exists():
                return True
            if (search_path / f"{section_name}.md").exists():
                return True
        return False

    def _section_name_to_title(self, section_name: str) -> str:
        """Convert a section name to a human-readable title.

        Args:
            section_name: Section name with dashes or underscores

        Returns:
            Title-cased string with spaces
        """
        return section_name.replace("-", " ").replace("_", " ").title()
