from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class JavascriptConfigValue(ConfigValue):
    biome: bool | None = public_field(
        default=None,
        description="Format and lint JavaScript/TypeScript code using Biome",
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate_javascript.config_option.biome_config_option import (
            BiomeConfigOption,
        )

        return {
            BiomeConfigOption.get_name(): self.biome,
        }
