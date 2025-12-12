from __future__ import annotations

from types import UnionType
from typing import TYPE_CHECKING, Any

from wexample_helpers.decorator.base_class import base_class

from wexample_config.config_option.abstract_list_config_option import (
    AbstractListConfigOption,
)

if TYPE_CHECKING:
    from types import UnionType


@base_class
class ChildrenConfigOption(AbstractListConfigOption):
    def dump(self) -> Any:
        output = []

        for child in self.children:
            output.append(child.dump())

        return output

    def get_item_class_type(self) -> type | UnionType:
        from wexample_config.config_option.abstract_nested_config_option import (
            AbstractNestedConfigOption,
        )

        return AbstractNestedConfigOption
