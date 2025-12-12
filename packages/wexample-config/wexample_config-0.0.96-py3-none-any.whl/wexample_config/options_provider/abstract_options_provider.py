from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


@base_class
class AbstractOptionsProvider(BaseClass):
    @classmethod
    @abstract_method
    def get_options(cls) -> list[type[AbstractConfigOption]]:
        pass

    @classmethod
    def get_options_registry(cls) -> dict[str, type[AbstractConfigOption]]:
        return {option.get_name(): option for option in cls.get_options()}
