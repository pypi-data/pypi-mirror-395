from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_value.config_value import ConfigValue

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_nested_config_option import (
        AbstractNestedConfigOption,
    )


class CallbackRenderConfigValue(ConfigValue):
    @staticmethod
    def get_allowed_types() -> Any:
        from collections.abc import Callable

        return Callable[..., Any]

    def render(self, option: AbstractNestedConfigOption) -> str:
        return self.raw(option)
