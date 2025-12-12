from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_filestate.item.file.structured_content_file import StructuredContentFile

if TYPE_CHECKING:
    from wexample_helpers.const.types import StructuredData


class EnvFile(StructuredContentFile):
    """
    Simple .env reader/writer using python-dotenv.
    """

    EXTENSION_ENV: ClassVar[str] = "env"
    EXTENSION_DOT_ENV: ClassVar[str] = f".{EXTENSION_ENV}"

    def dumps(self, content: StructuredData | None) -> str:
        # Produce .env textual content from a dict-like mapping
        if not isinstance(content, dict):
            return ""
        return (
            "\n".join(f"{k}={'' if v is None else v}" for k, v in content.items())
            + "\n"
        )

    # ---------- Parsing / Serialization ----------
    def loads(self, text: str, strict: bool = False) -> StructuredData:
        from io import StringIO

        from dotenv import dotenv_values

        return dict(dotenv_values(stream=StringIO(text)))

    def _expected_file_name_extension(self) -> str:
        return self.EXTENSION_ENV
