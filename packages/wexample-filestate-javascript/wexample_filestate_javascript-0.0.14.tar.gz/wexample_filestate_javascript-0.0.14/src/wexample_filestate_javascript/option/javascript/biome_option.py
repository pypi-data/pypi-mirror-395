from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from .abstract_javascript_file_content_option import AbstractJavascriptFileContentOption

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class BiomeOption(AbstractJavascriptFileContentOption):
    def get_description(self) -> str:
        return "Format and lint JavaScript/TypeScript code using Biome."

    def _apply_content_change(self, target: TargetFileOrDirectoryType) -> str:
        """Format and lint JavaScript/TypeScript code using Biome via Docker."""
        # Get the file path inside the container
        container_file_path = self._get_container_file_path(target)

        # Execute biome in Docker with centralized config
        self._execute_in_docker(
            target=target,
            command=[
                "biome",
                "check",
                "--write",
                "--config-path=/root/biome.json",
                container_file_path,
            ],
        )

        # Read the fixed content from the file (it was modified in place)
        return target.read_text()
