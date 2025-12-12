from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoCustomValueConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_config.config_value.custom_type_config_value import (
            CustomTypeConfigValue,
        )

        return CustomTypeConfigValue
