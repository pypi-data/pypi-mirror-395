from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.has_simple_repr_mixin import HasSimpleReprMixin
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_config.config_value.config_value import ConfigValue
    from wexample_config.const.types import DictConfig


@base_class
class AbstractConfigOption(
    HasSnakeShortClassNameClassMixin, HasSimpleReprMixin, BaseClass
):
    config_value: ConfigValue | None = public_field(
        description="The value object associated with this config option",
        default=None,
    )
    key: str | None = public_field(
        description="The option key",
        default=None,
    )
    parent: AbstractConfigOption | None = public_field(
        description="Parent config option if nested",
        default=None,
    )
    value: Any = public_field(
        description="The raw value of this config option",
        default=None,
    )
    _root: AbstractConfigOption | None | False = private_field(
        description="The root parent",
        default=None,
    )

    def __attrs_post_init__(self) -> None:
        self.key = self.key or self.get_name()
        self.set_value(self.value)
        if self.parent:
            self.parent.add_child(self)

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "ConfigOption"

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Any

    @staticmethod
    def resolve_config(config: DictConfig) -> DictConfig:
        return config

    def add_child(self, child: AbstractConfigOption) -> None:
        """Do stuff with this new child"""

    def dump(self) -> Any:
        return self.get_value().raw

    @abstract_method
    def get_description(self) -> str:
        pass

    def get_key(self) -> str:
        assert self.key is not None
        return self.key

    def get_parent(self) -> AbstractConfigOption:
        assert self.parent is not None
        return self.parent

    def get_root(self) -> AbstractConfigOption:
        if self.parent is not None:
            return self.parent.get_root()
        return self

    def get_value(self) -> ConfigValue:
        from wexample_config.config_value.config_value import ConfigValue

        return self.config_value or ConfigValue(raw=None)

    def get_value_class_type(self) -> type[ConfigValue]:
        from wexample_config.config_value.config_value import ConfigValue

        return ConfigValue

    def prepare_value(self, raw_value: Any) -> Any:
        from wexample_config.config_value.config_value import ConfigValue

        # Allow config option
        if isinstance(raw_value, ConfigValue):
            return raw_value.to_option_raw_value()

        return raw_value

    def set_value(self, raw_value: Any) -> Any:
        from wexample_helpers.exception.not_allowed_variable_type_exception import (
            NotAllowedVariableTypeException,
        )

        from wexample_config.config_value.config_value import ConfigValue

        if raw_value is None:
            return

        config_value_class = self.get_value_class_type()

        try:
            # Check if value is valid for the config option,
            # reuse same method to validate types.
            config_value_class.validate_value_type(
                raw_value=raw_value, allowed_type=self.get_raw_value_allowed_type()
            )
        except NotAllowedVariableTypeException as e:
            # Add context about the option class that caused the error
            # Create a new exception with enhanced context
            enhanced_exception = NotAllowedVariableTypeException(
                variable_type=e.data.get("item_type"),
                variable_value=e.data.get("item_value"),
                message=f"[{self.get_name()}] ",
                allowed_types=e.data.get("allowed_values"),
            )

            # Raise the enhanced exception with the original as cause
            raise enhanced_exception from e

        raw_value = self.prepare_value(raw_value)

        self.config_value = (
            config_value_class(raw=raw_value)
            if not isinstance(raw_value, ConfigValue)
            else raw_value
        )

        return raw_value
