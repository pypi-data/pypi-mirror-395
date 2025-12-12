from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)


class DemoNestedConfigOption(AbstractNestedConfigOption):
    nested: bool = True

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Any
