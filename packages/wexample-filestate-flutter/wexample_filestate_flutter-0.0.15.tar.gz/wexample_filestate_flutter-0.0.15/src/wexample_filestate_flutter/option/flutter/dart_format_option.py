from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from .abstract_flutter_file_content_option import AbstractFlutterFileContentOption

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class DartFormatOption(AbstractFlutterFileContentOption):
    def get_description(self) -> str:
        return "Format and fix Dart/Flutter code using dart format and dart fix."

    def _apply_content_change(self, target: TargetFileOrDirectoryType) -> str:
        """Format and fix Dart/Flutter code using dart format and dart fix via Docker."""
        # Clean host caches and ensure dependencies are resolved inside the container
        self._prepare_container_environment(target)

        # Get the file path inside the container
        container_file_path = self._get_container_file_path(target)

        # First, apply dart fix to auto-fix issues
        self._run_from_container_root(
            target=target,
            shell_command=f"dart fix --apply {container_file_path}",
        )

        # Then, format the code
        self._run_from_container_root(
            target=target,
            shell_command=f"dart format {container_file_path}",
        )

        # Read the fixed and formatted content from the file (it was modified in place)
        return target.read_text()
