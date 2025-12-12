from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class AbstractYamlChildOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool

    def _dump_yaml_content(self, data) -> str:
        """Dump YAML data to string content."""
        import yaml

        return yaml.safe_dump(data, sort_keys=False)

    def _read_yaml_data(self, target: TargetFileOrDirectoryType):
        """Read YAML data from target file."""
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read

        return yaml_read(target.get_path())
