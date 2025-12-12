from __future__ import annotations

import re

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.name.abstract_name_child_option import (
    AbstractNameChildOption,
)


@base_class
class CaseFormatOption(AbstractNameChildOption):
    def apply_correction(self, name: str) -> str:
        """Apply case format correction to name."""
        if self.get_value().is_none():
            return name

        case_format = self.get_value().get_str()

        if case_format == "uppercase":
            return name.upper()
        elif case_format == "lowercase":
            return name.lower()
        elif case_format == "camelCase":
            # Convert to camelCase (simple implementation)
            parts = name.replace("_", " ").replace("-", " ").split()
            if parts:
                return parts[0].lower() + "".join(
                    word.capitalize() for word in parts[1:]
                )
        elif case_format == "snake_case":
            # Convert to snake_case (simple implementation)
            # Handle camelCase to snake_case
            s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
            return (
                re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
                .lower()
                .replace("-", "_")
                .replace(" ", "_")
            )
        elif case_format == "kebab-case":
            # Convert to kebab-case (simple implementation)
            # Handle camelCase to kebab-case
            s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
            return (
                re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1)
                .lower()
                .replace("_", "-")
                .replace(" ", "-")
            )

        return name

    def get_description(self) -> str:
        return "Enforce case format (uppercase, lowercase, camelCase, snake_case, kebab-case)"

    def validate_name(self, name: str) -> bool:
        """Validate case format of the name."""
        if self.get_value().is_none():
            return True

        case_format = self.get_value().get_str()

        if case_format == "uppercase":
            return name.isupper()
        elif case_format == "lowercase":
            return name.islower()
        elif case_format == "camelCase":
            return self._is_camel_case(name)
        elif case_format == "snake_case":
            return self._is_snake_case(name)
        elif case_format == "kebab-case":
            return self._is_kebab_case(name)
        return True

    def _is_camel_case(self, name: str) -> bool:
        """Check if name is in camelCase format."""
        return re.match(r"^[a-z][a-zA-Z0-9]*$", name) is not None

    def _is_kebab_case(self, name: str) -> bool:
        """Check if name is in kebab-case format."""
        return re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name) is not None

    def _is_snake_case(self, name: str) -> bool:
        """Check if name is in snake_case format."""
        return re.match(r"^[a-z0-9]+(_[a-z0-9]+)*$", name) is not None
