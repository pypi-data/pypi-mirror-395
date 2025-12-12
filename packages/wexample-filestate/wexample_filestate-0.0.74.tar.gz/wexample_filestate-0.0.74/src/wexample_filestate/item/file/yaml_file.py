from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.const.types import StructuredData

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from wexample_helpers.const.types import StructuredData
    from wexample_helpers_yaml.const.types import YamlContent


class YamlFile(StructuredContentFile):
    EXTENSION_YAML: ClassVar[str] = "yaml"
    EXTENSION_YML: ClassVar[str] = "yml"

    def dumps(self, content: StructuredData | None) -> str:
        import yaml

        # Unwrap ConfigValue objects to their raw primitive values
        def _normalize(v):
            from wexample_config.config_value.config_value import ConfigValue

            if isinstance(v, ConfigValue):
                # Extract the raw value instead of converting to string representation
                return _normalize(v._get_nested_raw())
            if isinstance(v, dict):
                return {k: _normalize(x) for k, x in v.items()}
            if isinstance(v, list):
                return [_normalize(x) for x in v]
            return v

        normalized = _normalize(content or {})
        return yaml.safe_dump(normalized)

    def loads(self, text: str, strict: bool = False) -> YamlContent:
        import yaml

        value = yaml.safe_load(text)
        # Normalize None to empty dict for convenience
        return value if value is not None else {}

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_YML
