from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from wexample_filestate.testing.abstract_state_manager_test import (
    AbstractStateManagerTest,
)

if TYPE_CHECKING:
    from wexample_filestate.config_option.mixin.item_config_option_mixin import (
        ItemTreeConfigOptionMixin,
    )


class TestFileStateManager(AbstractStateManagerTest):
    def test_configure_class_unexpected(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)

        from wexample_filestate.exception.bad_configuration_class_type_exception import (
            BadConfigurationClassTypeException,
        )

        class BadClass:
            pass

        with pytest.raises(BadConfigurationClassTypeException):
            self.state_manager.configure(config={"children": [{"class": BadClass}]})

    def test_configure_from_callback(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)

        def _name(option: ItemTreeConfigOptionMixin) -> str:
            return "yes"

        self.state_manager.configure(config={"name": _name})

        assert self.state_manager.get_name() == "file_state_manager"
        assert self.state_manager.get_item_name() == "yes"

    def test_configure_from_callback_class(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)
        from wexample_config.config_value.callback_render_config_value import (
            CallbackRenderConfigValue,
        )

        def _name(option: ItemTreeConfigOptionMixin) -> str:
            return "yow"

        self.state_manager.configure(
            config={
                "name": CallbackRenderConfigValue(raw=_name),
            }
        )

        assert self.state_manager.get_item_name() == "yow"

    def test_configure_from_file(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)
        self.state_manager.configure_from_file(
            self._get_test_state_manager_path() / "config-test-one.yml"
        )

    def test_configure_name(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)
        self.state_manager.configure({"name": "yes"})

    def test_configure_unexpected(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)
        from wexample_config.exception.invalid_option_exception import (
            InvalidOptionException,
        )

        with pytest.raises(InvalidOptionException):
            self.state_manager.configure(config={"unexpected_option": "yes"})

    def test_dump(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        self.state_manager.configure(
            config={
                "children": [
                    {
                        "name": TEST_FILE_NAME_SIMPLE_TEXT,
                        "type": "file",
                    }
                ]
            }
        )

        dump = self.state_manager.dump()

        assert dump == {
            "name": self._get_parent_dir(),
            "children": [{"name": "simple-text.txt", "type": "file"}],
        }
        assert isinstance(dump, dict)

    def test_setup(self, tmp_path) -> None:
        self._setup_with_tmp_path(tmp_path)
        assert self.state_manager is not None

    def _get_parent_dir(self) -> str:
        return self.state_manager.get_path().name
