from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.const.types import StructuredData

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from wexample_helpers.const.types import StructuredData


class HtmlFile(StructuredContentFile):
    EXTENSION_HTML: ClassVar[str] = "html"
    EXTENSION_HTM: ClassVar[str] = "htm"

    def dumps(self, content: StructuredData | None) -> str:
        # Accept string content or any object convertible to string (e.g., BeautifulSoup)
        if isinstance(content, str):
            return content
        return str(content or "")

    # ---------- Parsing / Serialization ----------
    def loads(self, text: str, strict: bool = False) -> str:
        # Keep HTML as raw string. If callers need a parsed tree, they can
        # operate on the returned text externally.
        return text

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_HTML
