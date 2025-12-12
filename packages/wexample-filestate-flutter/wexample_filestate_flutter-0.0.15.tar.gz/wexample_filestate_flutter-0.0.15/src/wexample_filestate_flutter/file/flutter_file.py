from __future__ import annotations

from typing import ClassVar

from wexample_filestate.item.item_target_file import ItemTargetFile


class FlutterFile(ItemTargetFile):
    EXTENSION_ENV: ClassVar[str] = "dart"

    def _expected_file_name_extension(self) -> str | None:
        return FlutterFile.EXTENSION_ENV
