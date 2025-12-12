from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from wexample_helpers.const.types import StructuredData


class XmlFile(StructuredContentFile):
    EXTENSION_XML: ClassVar[str] = "xml"

    def dumps(self, content: StructuredData | None) -> str:
        import xmltodict

        if isinstance(content, str):
            # Already XML string
            return content
        try:
            return xmltodict.unparse(content or {}, pretty=True)
        except Exception:
            return str(content)

    # ---------- Parsing / Serialization ----------
    def loads(self, text: str, strict: bool = False) -> StructuredData:
        import xmltodict

        parsed = xmltodict.parse(text)
        return parsed or {}

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_XML
