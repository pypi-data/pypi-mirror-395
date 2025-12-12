from __future__ import annotations

from types import UnionType
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)

if TYPE_CHECKING:
    from types import UnionType

    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


@base_class
class AbstractListConfigOption(AbstractNestedConfigOption):
    children: list[AbstractConfigOption] = public_field(
        factory=list, description="The list of children"
    )

    @staticmethod
    def get_allowed_types() -> type | UnionType:
        return list[dict[str, Any]]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return list[dict[str, Any]]

    def get_item_class_type(self) -> type | UnionType:
        from wexample_config.config_option.abstract_config_option import (
            AbstractConfigOption,
        )

        return AbstractConfigOption

    def set_value(self, raw_value: Any) -> None:
        from wexample_config.config_option.abstract_config_option import (
            AbstractConfigOption,
        )

        # Skip direct parent which creates only one item.
        AbstractConfigOption.set_value(self, raw_value)

        if raw_value is None:
            return

        for child_config in raw_value:
            self.children.append(
                self.get_item_class_type()(value=child_config, parent=self)
            )
