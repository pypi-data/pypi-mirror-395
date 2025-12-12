from __future__ import annotations

from typing import Union

from wexample_filestate.item.item_source_directory import ItemSourceDirectory
from wexample_filestate.item.item_source_file import ItemSourceFile
from wexample_filestate.item.item_target_directory import ItemTargetDirectory
from wexample_filestate.item.item_target_file import ItemTargetFile

TargetFileOrDirectory = Union[ItemTargetDirectory, ItemTargetFile]
SourceFileOrDirectory = Union[ItemSourceDirectory, ItemSourceFile]
