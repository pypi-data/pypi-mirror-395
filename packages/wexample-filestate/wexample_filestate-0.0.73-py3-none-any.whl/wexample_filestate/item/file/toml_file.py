from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from tomlkit import TOMLDocument


@base_class
class TomlFile(StructuredContentFile):
    EXTENSION_TOML: ClassVar[str] = "toml"

    def dumps(self, content: TOMLDocument | dict | None) -> str:  # type: ignore[name-defined]
        # from tomlkit import dumps as toml_dumps
        from tomlkit import TOMLDocument, document, dumps

        if content is None:
            return dumps(document())

        # If it's already a TOMLDocument, dump as-is to preserve formatting
        try:
            if isinstance(content, TOMLDocument):
                return dumps(content)
        except Exception:
            pass

        # Otherwise, attempt to create a TOMLDocument from a dict-like value
        if isinstance(content, dict):
            doc = document()
            for k, v in content.items():
                doc[k] = v
            return dumps(doc)

        # Fallback: stringify
        return str(content)

    # ---------- Parsing / Serialization ----------
    def loads(self, text: str, strict: bool = False) -> TOMLDocument:  # type: ignore[name-defined]
        from tomlkit import document, parse

        if text is None or text == "":
            # Return an empty TOMLDocument to keep types consistent
            return document()
        return parse(text)

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_TOML
