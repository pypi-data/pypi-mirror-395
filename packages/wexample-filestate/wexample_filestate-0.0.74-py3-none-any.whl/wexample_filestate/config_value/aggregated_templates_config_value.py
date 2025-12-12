from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.config_value.content_config_value import ContentConfigValue

if TYPE_CHECKING:
    from wexample_helpers.const.types import BasicValue


@base_class
class AggregatedTemplatesConfigValue(ContentConfigValue):
    parameters: dict[str, BasicValue] | None = public_field(
        factory=dict, description="The parameters to replace into the template"
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this field."
    )
    templates: list[str] | None = public_field(
        factory=list, description="List of templates contents to aggregate"
    )

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Any

    def get_str(self, type_check: bool = True) -> str | None:
        from wexample_helpers.helpers.string import string_replace_params

        output = []
        templates = self.get_templates()

        if len(templates) == 0:
            return None
        for template_content in templates:
            output.append(string_replace_params(template_content, self.parameters))

        output_str = os.linesep.join(output)

        return output_str

    def get_templates(self) -> list[str] | None:
        return self.templates

    def to_option_raw_value(self) -> Any:
        return self
