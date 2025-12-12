from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from wexample_helpers.const.types import AnyList

    from wexample_config.config_value.config_value import ConfigValue

T = TypeVar("T")


@base_class
class ConfigValueCollection(BaseClass, Generic[T]):
    """A collection of ConfigValue objects that provides utility methods for working with collections."""

    items: list[ConfigValue] = public_field(
        factory=list,
        description="List of ConfigValue objects in the collection.",
    )

    def __len__(self) -> int:
        """Return the number of items in the collection."""
        return len(self.items)

    def __iter__(self) -> Iterator[ConfigValue]:
        """Allow iteration over the collection items."""
        return iter(self.items)

    def __getitem__(self, index: int) -> ConfigValue:
        """Allow indexing to access items directly."""
        return self.items[index]

    def __attrs_post_init__(self) -> None:
        pass

    # Factory methods
    @classmethod
    def from_config_values(cls, values: list[ConfigValue]) -> ConfigValueCollection:
        """Create a ConfigValueCollection from a list of ConfigValue objects."""
        collection = cls()
        collection.extend(values)
        return collection

    @classmethod
    def from_raw_values(cls, values: list[Any]) -> ConfigValueCollection:
        """Create a ConfigValueCollection from a list of raw values."""
        from wexample_config.config_value.config_value import ConfigValue

        return cls.from_config_values([ConfigValue(raw=value) for value in values])

    def append(self, value: ConfigValue) -> None:
        """Add a ConfigValue to the collection."""
        self.items.append(value)

    def extend(self, values: list[ConfigValue]) -> None:
        """Add multiple ConfigValue objects to the collection."""
        self.items.extend(values)

    def get_bool_collection(self) -> list[bool]:
        """Convert all items in the collection to booleans."""
        return self.map(lambda item: item.get_bool())

    def get_bool_or_none_collection(self) -> list[bool | None]:
        """Convert all items in the collection to booleans or None."""
        return self.map(lambda item: item.get_bool_or_none())

    def get_dict_collection(self) -> list[dict]:
        """Convert all items in the collection to dictionaries."""
        return self.map(lambda item: item.get_dict())

    def get_dict_or_none_collection(self) -> list[dict | None]:
        """Convert all items in the collection to dictionaries or None."""
        return self.map(lambda item: item.get_dict_or_none())

    def get_float_collection(self) -> list[float]:
        """Convert all items in the collection to floats."""
        return self.map(lambda item: item.get_float())

    def get_float_or_none_collection(self) -> list[float | None]:
        """Convert all items in the collection to floats or None."""
        return self.map(lambda item: item.get_float_or_none())

    def get_int_collection(self) -> list[int]:
        """Convert all items in the collection to integers."""
        return self.map(lambda item: item.get_int())

    def get_int_or_none_collection(self) -> list[int | None]:
        """Convert all items in the collection to integers or None."""
        return self.map(lambda item: item.get_int_or_none())

    def get_list_collection(self) -> list[AnyList]:
        """Convert all items in the collection to lists."""
        return self.map(lambda item: item.get_list())

    def get_list_or_none_collection(self) -> list[AnyList | None]:
        """Convert all items in the collection to lists or None."""
        return self.map(lambda item: item.get_list_or_none())

    # Collection conversion methods
    def get_str_collection(self) -> list[str]:
        """Convert all items in the collection to strings."""
        return self.map(lambda item: item.get_str())

    # Non-strict collection conversion methods
    def get_str_or_none_collection(self) -> list[str | None]:
        """Convert all items in the collection to strings or None."""
        return self.map(lambda item: item.get_str_or_none())

    def map(self, func: Callable[[ConfigValue], T]) -> list[T]:
        """Apply a function to each ConfigValue in the collection and return the results."""
        return [func(item) for item in self.items]

    def to_bool_collection(self) -> list[bool]:
        """Convert all items in the collection to booleans using to_bool()."""
        return self.map(lambda item: item.to_bool())

    def to_dict_collection(self) -> list[dict]:
        """Convert all items in the collection to dictionaries using to_dict()."""
        return self.map(lambda item: item.to_dict())

    def to_float_collection(self) -> list[float]:
        """Convert all items in the collection to floats using to_float()."""
        return self.map(lambda item: item.to_float())

    def to_int_collection(self) -> list[int]:
        """Convert all items in the collection to integers using to_int()."""
        return self.map(lambda item: item.to_int())

    def to_list_collection(self) -> list[AnyList]:
        """Convert all items in the collection to lists using to_list()."""
        return self.map(lambda item: item.to_list())

    # Compatibility methods for to_* methods
    def to_str_collection(self) -> list[str]:
        """Convert all items in the collection to strings using to_str()."""
        return self.map(lambda item: item.to_str())
