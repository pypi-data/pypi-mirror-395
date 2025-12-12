from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)


@base_class
class AbstractConfigManager(AbstractNestedConfigOption):
    pass
