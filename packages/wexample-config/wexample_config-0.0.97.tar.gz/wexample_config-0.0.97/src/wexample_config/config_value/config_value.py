from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import UnionType

    from wexample_helpers.const.types import AnyList, StringKeysDict


@base_class
class ConfigValue(BaseClass):
    """
    Wraps a raw configuration value (with optional filters) and provides a consistent API for:

      1. Type checks:
         - is_int(), is_str(), is_list(), is_dict(), is_callable(), etc.
           → Return True if the (nested) raw value is of the given type, else False.

      2. Typed getters:
         - get_int(), get_str(), get_list(), etc.
           → Return the value as the requested type or raise TypeError if the type doesn’t match
             (unless called with type_check=False).

      3. Safe getters:
         - get_int_or_none(), get_str_or_none(), …
           → Return the value as the requested type if it matches, else None.
         - get_int_or_default(default), get_str_or_default(default), …
           → Return the value if it matches the type, else return the provided default.

      4. Type-checked setters:
         - set_int(value), set_str(value), …
           → Verify the type before assigning to self.raw, else raise TypeError.

      5. Conversions:
         - to_int(), to_str(), to_list(), etc.
           → Attempt to convert the raw value via the built-in constructor (e.g. int("123")),
             raising ValueError/TypeError on failure.
         - to_int_or_none(), to_str_or_none(), …
           → Same as to_<type>(), but return None if the raw value is None.

    Advanced utilities:
      - validate_value_type(raw_value, allowed_type): generic type validation at init.

    Examples:
        cv = ConfigValue(raw="123")
        cv.is_str()                # True
        cv.get_str()               # "123"
        cv.to_int()                # 123
        cv.get_int_or_default(0)   # 0 (no exception)
    """

    raw: Any = public_field(description="The raw value of the configuration.")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(type={type(self.raw).__name__}, value={self.raw})>"

    def __str__(self) -> str:
        return self.__repr__()

    def __attrs_post_init__(self) -> None:
        self.validate_value_type(
            raw_value=self.raw, allowed_type=self.get_allowed_types()
        )
        # Allow class to generate raw value by itself.
        self.raw = self._create_default_raw(self.raw)

    @classmethod
    def validate_value_type(
        cls, raw_value: Any, allowed_type: type | UnionType
    ) -> None:
        from wexample_helpers.helpers.type import type_validate_or_fail

        type_validate_or_fail(
            value=raw_value,
            allowed_type=allowed_type,
        )

    @staticmethod
    def get_allowed_types() -> Any:
        return Any

    def get_bool(self, type_check: bool = True) -> bool:
        return self._get_value_from_callback(bool, self.get_bool, type_check)

    def get_bool_or_default(
        self, default: bool | None = None, type_check: bool = True
    ) -> bool:
        return self._get_or_default(self.get_bool, default, type_check)

    def get_bool_or_none(self) -> bool | None:
        if self.is_bool():
            return self.get_bool()
        return None

    def get_bytes(self, type_check: bool = True) -> bytes:
        return self._get_value_from_callback(bytes, self.get_bytes, type_check)

    def get_bytes_or_default(
        self, default: bytes | None = None, type_check: bool = True
    ) -> bytes:
        return self._get_or_default(self.get_bytes, default, type_check)

    def get_bytes_or_none(self) -> bytes | None:
        if self.is_bytes():
            return self.get_bytes()
        return None

    def get_callable(self, type_check: bool = True) -> Callable:
        """Return the stored value as a callable, checking recursively if needed."""
        value = self._get_nested_raw()

        if type_check and not callable(value):
            raise TypeError(f"Expected a callable, got {type(value)}")

        return value

    # Getters or None
    def get_callable_or_none(self) -> Callable | None:
        if self.is_callable():
            return self.get_callable()
        return None

    def get_class(self, type_check: bool = True) -> type[Any]:
        if type_check:
            assert self.is_class()
        return self._get_nested_raw()

    def get_class_or_none(self) -> type[Any] | None:
        if self.is_class():
            return self.get_class()
        return None

    def get_complex(self, type_check: bool = True) -> complex:
        return self._get_value_from_callback(complex, self.get_complex, type_check)

    def get_complex_or_default(
        self, default: complex | None = None, type_check: bool = True
    ) -> complex:
        return self._get_or_default(self.get_complex, default, type_check)

    def get_complex_or_none(self) -> complex | None:
        if self.is_complex():
            return self.get_complex()
        return None

    def get_dict(self, type_check: bool = True) -> StringKeysDict:
        return self._get_value_from_callback(dict, self.get_dict, type_check)

    def get_dict_or_default(
        self, default: StringKeysDict | None = None, type_check: bool = True
    ) -> StringKeysDict:
        return self._get_or_default(self.get_dict, default, type_check)

    def get_dict_or_empty(self) -> StringKeysDict:
        return self.get_dict_or_default(default={})

    def get_dict_or_none(self) -> StringKeysDict | None:
        if self.is_dict():
            return self.get_dict()
        return None

    def get_float(self, type_check: bool = True) -> float:
        return self._get_value_from_callback(float, self.get_float, type_check)

    def get_float_or_default(
        self, default: float | None = None, type_check: bool = True
    ) -> float:
        return self._get_or_default(self.get_float, default, type_check)

    def get_float_or_none(self) -> float | None:
        if self.is_float():
            return self.get_float()
        return None

    def get_int(self, type_check: bool = True) -> int:
        return self._get_value_from_callback(int, self.get_int, type_check)

    def get_int_or_default(
        self, default: int | None = None, type_check: bool = True
    ) -> int:
        return self._get_or_default(self.get_int, default, type_check)

    def get_int_or_none(self) -> int | None:
        if self.is_int():
            return self.get_int()
        return None

    def get_list(self, type_check: bool = True) -> AnyList:
        return self._get_value_from_callback(list, self.get_list, type_check)

    def get_list_or_default(
        self, default: AnyList | None = None, type_check: bool = True
    ) -> AnyList:
        return self._get_or_default(self.get_list, default, type_check)

    def get_list_or_empty(self) -> AnyList:
        return self.get_list_or_default(default=[])

    def get_list_or_none(self) -> AnyList | None:
        if self.is_list():
            return self.get_list()
        return None

    def get_set(self, type_check: bool = True) -> set:
        return self._get_value_from_callback(set, self.get_set, type_check)

    def get_set_or_default(
        self, default: set | None = None, type_check: bool = True
    ) -> set:
        default_set = default if default is not None else set()
        return self._get_or_default(self.get_set, default_set, type_check)

    def get_set_or_none(self) -> set | None:
        if self.is_set():
            return self.get_set()
        return None

    def get_str(self, type_check: bool = True) -> str:
        return self._get_value_from_callback(str, self.get_str, type_check)

    def get_str_or_default(
        self, default: str | None = None, type_check: bool = True
    ) -> str:
        return self._get_or_default(self.get_str, default, type_check)

    def get_str_or_none(self) -> str | None:
        if self.is_str():
            return self.get_str()
        return None

    def get_tuple(self, type_check: bool = True) -> tuple:
        return self._get_value_from_callback(tuple, self.get_tuple, type_check)

    def get_tuple_or_default(
        self, default: tuple | None = None, type_check: bool = True
    ) -> tuple:
        default_tuple = default if default is not None else ()
        return self._get_or_default(self.get_tuple, default_tuple, type_check)

    def get_tuple_or_none(self) -> tuple | None:
        if self.is_tuple():
            return self.get_tuple()
        return None

    def has_item_in_list(self, value: Any) -> bool:
        return self.is_list() and value in self.get_list()

    def has_key_in_dict(self, key: str) -> bool:
        # Separate type check to gracefully return false if not dict.
        return self.is_dict() and key in self.get_dict()

    def is_bool(self) -> bool:
        return self.is_of_type(bool, self._get_nested_raw())

    def is_bytes(self) -> bool:
        return self.is_of_type(bytes, self._get_nested_raw())

    # Type checking methods
    def is_callable(self) -> bool:
        return callable(self._get_nested_raw())

    # Type checking methods
    def is_class(self) -> bool:
        import inspect

        return inspect.isclass(self.raw)

    def is_complex(self) -> bool:
        return self.is_of_type(complex, self._get_nested_raw())

    def is_dict(self) -> bool:
        return self.is_of_type(dict, self._get_nested_raw())

    def is_empty(self) -> bool:
        raw = self._get_nested_raw()
        return (
            raw is None
            or (self.is_of_type(list, raw) and len(raw) == 0)
            or (self.is_of_type(str, raw) and raw == "")
            or (self.is_of_type(dict, raw) and len(raw) == 0)
            or (self.is_of_type(tuple, raw) and len(raw) == 0)
            or (self.is_of_type(set, raw) and len(raw) == 0)
            or raw == 0
            or raw is False
            or (hasattr(raw, "__len__") and len(raw) == 0)
        )

    def is_false(self) -> bool:
        return self.get_bool() == False

    def is_float(self) -> bool:
        return self.is_of_type(float, self._get_nested_raw())

    def is_int(self) -> bool:
        return self.is_of_type(int, self._get_nested_raw())

    def is_list(self) -> bool:
        return self.is_of_type(list, self._get_nested_raw())

    def is_none(self) -> bool:
        return self.raw is None

    def is_of_type(self, value_type: Any, value: Any) -> bool:
        from collections.abc import Callable

        if value_type is Callable:
            return callable(value)
        if isinstance(value_type, type):
            return isinstance(value, value_type)
        return False

    def is_set(self) -> bool:
        return self.is_of_type(set, self._get_nested_raw())

    def is_str(self) -> bool:
        return self.is_of_type(str, self._get_nested_raw())

    def is_true(self) -> bool:
        return self.to_bool_or_none() == True

    def is_tuple(self) -> bool:
        return self.is_of_type(tuple, self._get_nested_raw())

    def set_bool(self, value: bool, type_check: bool = True) -> None:
        self._assert_type(bool, value, type_check)
        self.raw = value

    def set_bytes(self, value: bytes, type_check: bool = True) -> None:
        self._assert_type(bytes, value, type_check)
        self.raw = value

    def set_callable(self, value: Callable, type_check: bool = True) -> None:
        from collections.abc import Callable

        self._assert_type(Callable, value, type_check)
        self.raw = value

    # Setters
    def set_class(self, value: type[Any], type_check: bool = True) -> None:
        from collections.abc import Callable

        self._assert_type(Callable, value, type_check)
        self.raw = value

    def set_complex(self, value: complex, type_check: bool = True) -> None:
        self._assert_type(complex, value, type_check)
        self.raw = value

    def set_dict(self, value: StringKeysDict, type_check: bool = True) -> None:
        self._assert_type(dict, value, type_check)
        self.raw = value

    def set_float(self, value: float, type_check: bool = True) -> None:
        self._assert_type(float, value, type_check)
        self.raw = value

    def set_int(self, value: int, type_check: bool = True) -> None:
        self._assert_type(int, value, type_check)
        self.raw = value

    def set_list(self, value: AnyList, type_check: bool = True) -> None:
        self._assert_type(list, value, type_check)
        self.raw = value

    def set_set(self, value: set, type_check: bool = True) -> None:
        self._assert_type(set, value, type_check)
        self.raw = value

    def set_str(self, value: str, type_check: bool = True) -> None:
        self._assert_type(str, value, type_check)
        self.raw = value

    def set_tuple(self, value: tuple, type_check: bool = True) -> None:
        self._assert_type(tuple, value, type_check)
        self.raw = value

    def to_bool(self) -> bool:
        return bool(self._execute_nested_method(self.get_bool))

    def to_bool_or_none(self) -> bool | None:
        if self.is_none():
            return None
        return self.to_bool()

    def to_bytes(self) -> bytes:
        return bytes(self._execute_nested_method(self.get_bytes))

    def to_bytes_or_none(self) -> bytes | None:
        if self.is_none():
            return None
        return self.to_bytes()

    def to_complex(self) -> complex:
        return complex(self._execute_nested_method(self.get_complex))

    def to_complex_or_none(self) -> complex | None:
        if self.is_none():
            return None
        return self.to_complex()

    def to_dict(self) -> StringKeysDict:
        return dict(self._execute_nested_method(self.get_dict))

    def to_dict_or_none(self) -> StringKeysDict | None:
        if self.is_none():
            return None
        return self.to_dict()

    def to_float(self) -> float:
        return float(self._execute_nested_method(self.get_float))

    def to_float_or_none(self) -> float | None:
        if self.is_none():
            return None
        return self.to_float()

    def to_int(self) -> int:
        return int(self._execute_nested_method(self.get_int))

    def to_int_or_none(self) -> int | None:
        if self.is_none():
            return None
        return self.to_int()

    def to_list(self) -> AnyList:
        return list(self._execute_nested_method(self.get_list))

    def to_list_or_none(self) -> AnyList | None:
        if self.is_none():
            return None
        return self.to_list()

    def to_option_raw_value(self) -> Any:
        return self.raw

    def to_set(self) -> set:
        return set(self._execute_nested_method(self.get_set))

    def to_set_or_none(self) -> set | None:
        if self.is_none():
            return None
        return self.to_set()

    # Conversion methods
    def to_str(self) -> str:
        return str(self._execute_nested_method(self.get_str))

    # Conversion methods or None
    def to_str_or_none(self) -> str | None:
        if self.is_none():
            return None
        return self.to_str()

    def to_tuple(self) -> tuple:
        return tuple(self._execute_nested_method(self.get_tuple))

    def to_tuple_or_none(self) -> tuple | None:
        if self.is_none():
            return None
        return self.to_tuple()

    def _assert_type(
        self, expected_type: Any, value: Any, type_check: bool = True
    ) -> None:
        if type_check and not self.is_of_type(expected_type, value):
            raise TypeError(f"Expected {expected_type} but got {type(value)}")

    def _create_default_raw(self, raw: Any) -> Any:
        return raw

    def _execute_nested_method(self, method: Callable[[], Any]) -> Any:
        if isinstance(self.raw, ConfigValue):
            return getattr(self.raw, method.__name__)(type_check=False)
        return self.raw

    def _get_nested_raw(self) -> Any:
        return self._resolve_nested().raw

    def _get_or_default(
        self, getter: Callable[[bool], Any], default: Any, type_check: bool = True
    ) -> Any:
        try:
            return getter(type_check=type_check)
        except TypeError:
            return default

    # Getter methods
    def _get_value_from_callback(
        self, expected_type: Any, method: Callable[..., Any], type_check: bool = True
    ) -> Any:
        value = self._execute_nested_method(method)
        self._assert_type(expected_type, value, type_check)
        return value

    def _resolve_nested(self) -> ConfigValue:
        if isinstance(self.raw, ConfigValue):
            return self.raw._resolve_nested()
        return self
