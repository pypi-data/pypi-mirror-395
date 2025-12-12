from __future__ import annotations

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class


@base_class
class BiomeConfigOption(AbstractConfigOption):
    @staticmethod
    def get_name() -> str:
        return "biome"
