from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_filestate.option.abstract_file_content_option import (
    AbstractFileContentOption,
)
from wexample_filestate.option.mixin.with_docker_option_mixin import (
    WithDockerOptionMixin,
)
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    pass


@base_class
class AbstractJavascriptFileContentOption(
    WithDockerOptionMixin, AbstractFileContentOption
):
    def _get_docker_image_name(self) -> str:
        """Return the Docker image name for JavaScript options."""
        return "wex-javascript-option"

    def _get_dockerfile_path(self) -> Path:
        """Return the path to the JavaScript Dockerfile."""
        # Get the path relative to this file
        current_file = Path(__file__)
        package_root = current_file.parent.parent.parent
        return package_root / "resources" / "docker" / "Dockerfile.javascript-option"
