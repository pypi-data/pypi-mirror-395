from __future__ import annotations

from wexample_file.mixin.with_local_file_mixin import WithLocalFileMixin
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.config_value.content_config_value import ContentConfigValue


@base_class
class FileContentConfigValue(WithLocalFileMixin, ContentConfigValue):
    path: str | None = public_field(
        default=None,
        description="Filesystem path to the content file",
    )
    raw: str | None = public_field(
        default=None,
        description="Raw value provided, used to populate 'path'",
    )

    def __attrs_post_init__(self) -> None:
        # Continue normal initialization chain
        super().__attrs_post_init__()

        # Ensure path is set from raw if not provided explicitly
        if self.path is None and self.raw is not None:
            self.path = self.raw

    def build_content(self) -> str | None:
        if self.get_path().exists():
            return self.get_local_file().read()
        return None
