from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from wexample_filestate.option.abstract_file_content_option import (
    AbstractFileContentOption,
)
from wexample_filestate.option.mixin.with_docker_option_mixin import (
    WithDockerOptionMixin,
)
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class AbstractFlutterFileContentOption(
    WithDockerOptionMixin, AbstractFileContentOption
):
    _CONTAINER_ROOT: ClassVar[str] = "/var/www/html"
    # Avoid re-running flutter pub get for every file during the same Python process
    _prepared_roots: ClassVar[set[str]] = set()

    def _cleanup_host_cache(self, target: TargetFileOrDirectoryType) -> None:
        """Remove host-generated Dart cache files that contain absolute paths.

        These caches often point to the host's pub cache (e.g., /home/<user>/.pub-cache)
        and break inside the container, so we wipe them before running commands there.
        """
        import shutil

        root_path = target.get_root().get_path()

        dart_tool = root_path / ".dart_tool"
        if dart_tool.exists():
            shutil.rmtree(dart_tool, ignore_errors=True)

        packages_file = root_path / ".packages"
        if packages_file.exists():
            packages_file.unlink(missing_ok=True)

    def _get_docker_image_name(self) -> str:
        """Return the Docker image name for Flutter options."""
        return "wex-flutter-option"

    def _get_dockerfile_path(self) -> Path:
        """Return the path to the Flutter Dockerfile."""
        # Get the path relative to this file
        current_file = Path(__file__)
        package_root = current_file.parent.parent.parent
        return package_root / "resources" / "docker" / "Dockerfile.flutter-option"

    def _prepare_container_environment(self, target: TargetFileOrDirectoryType) -> None:
        """Ensure caches are clean and dependencies are resolved inside the container."""
        root_key = str(target.get_root().get_path().resolve())
        if root_key in self._prepared_roots:
            return

        # Remove host-specific cache artifacts first
        self._cleanup_host_cache(target)

        # Make sure the container exists before running pub get
        self._ensure_docker_container(target)

        # Re-install dependencies inside the container to regenerate package_config with container paths.
        # Prefer flutter pub when available (flutter SDK projects), otherwise fall back to dart pub.
        self._execute_in_docker(
            target=target,
            command=[
                "bash",
                "-lc",
                "export PATH=/sdks/flutter/bin:$PATH && "
                f"cd {self._CONTAINER_ROOT} && "
                "if command -v flutter >/dev/null 2>&1; then "
                "flutter pub get; "
                "else "
                "dart pub get; "
                "fi",
            ],
        )
        self._prepared_roots.add(root_key)

    def _run_from_container_root(
        self, target: TargetFileOrDirectoryType, shell_command: str
    ) -> str:
        """Helper to run a shell command from the project root inside the container."""
        return self._execute_in_docker(
            target=target,
            command=[
                "bash",
                "-lc",
                f"export PATH=/usr/local/flutter/bin:/usr/lib/dart/bin:$PATH && cd {self._CONTAINER_ROOT} && {shell_command}",
            ],
        )
