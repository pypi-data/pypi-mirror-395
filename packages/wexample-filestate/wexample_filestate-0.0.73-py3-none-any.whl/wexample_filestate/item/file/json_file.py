from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.const.types import StructuredData

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from wexample_helpers.const.types import JsonContent, StructuredData


class JsonFile(StructuredContentFile):
    EXTENSION_JSON: ClassVar[str] = "json"

    def dumps(self, content: StructuredData | None) -> str:
        import json

        return json.dumps(content or {}, ensure_ascii=False, indent=2)

    def loads(self, text: str, strict: bool = False) -> JsonContent:  # type: ignore[name-defined]
        import json

        return json.loads(text)

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_JSON
