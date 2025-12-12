from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_helpers.decorator.base_class import base_class

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


@base_class
class NameConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from collections.abc import Callable

        from wexample_config.config_value.callback_render_config_value import (
            CallbackRenderConfigValue,
        )

        return Union[str, CallbackRenderConfigValue, Callable[..., Any]]

    @staticmethod
    def resolve_config(config: DictConfig) -> DictConfig:
        from wexample_config.config_value.callback_render_config_value import (
            CallbackRenderConfigValue,
        )

        key = NameConfigOption.get_name()

        if key in config:
            value = config.get(key)

            if callable(value):
                config[key] = CallbackRenderConfigValue(raw=value)

        return config
