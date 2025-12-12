from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue


class CustomTypeConfigValue(ConfigValue):
    @staticmethod
    def get_allowed_types() -> Any:
        return str
