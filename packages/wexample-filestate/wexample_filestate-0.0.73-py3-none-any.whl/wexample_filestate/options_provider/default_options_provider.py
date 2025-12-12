from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.options_provider.abstract_options_provider import (
    AbstractOptionsProvider,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


class DefaultOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.active_option import (
            ActiveOption,
        )
        from wexample_filestate.option.children_file_factory_option import (
            ChildrenFileFactoryOption,
        )
        from wexample_filestate.option.children_option import (
            ChildrenOption,
        )
        from wexample_filestate.option.class_option import (
            ClassOption,
        )
        from wexample_filestate.option.content_option import (
            ContentOption,
        )
        from wexample_filestate.option.default_content_option import (
            DefaultContentOption,
        )
        from wexample_filestate.option.mode_option import ModeOption
        from wexample_filestate.option.name.on_bad_format_option import (
            OnBadFormatOption,
        )
        from wexample_filestate.option.name_option import (
            NameOption,
        )
        from wexample_filestate.option.remove_backup_max_file_size_option import (
            RemoveBackupMaxFileSizeOption,
        )
        from wexample_filestate.option.shortcut_option import (
            ShortcutOption,
        )
        from wexample_filestate.option.should_contain_lines_option import (
            ShouldContainLinesOption,
        )
        from wexample_filestate.option.should_exist_option import (
            ShouldExistOption,
        )
        from wexample_filestate.option.should_have_extension_option import (
            ShouldHaveExtensionOption,
        )
        from wexample_filestate.option.should_not_contain_lines_option import (
            ShouldNotContainLinesOption,
        )
        from wexample_filestate.option.text_option import (
            TextOption,
        )
        from wexample_filestate.option.type_option import TypeOption
        from wexample_filestate.option.yaml_option import (
            YamlOption,
        )

        return [
            # filestate: python-iterable-sort
            ActiveOption,
            ChildrenFileFactoryOption,
            ChildrenOption,
            ClassOption,
            ContentOption,
            DefaultContentOption,
            ModeOption,
            NameOption,
            OnBadFormatOption,
            RemoveBackupMaxFileSizeOption,
            ShortcutOption,
            ShouldContainLinesOption,
            ShouldExistOption,
            ShouldHaveExtensionOption,
            ShouldNotContainLinesOption,
            TextOption,
            TypeOption,
            YamlOption,
        ]
