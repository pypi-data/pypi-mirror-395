from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.dict import DICT_PATH_SEPARATOR_DEFAULT

from wexample_config.config_value.config_value import ConfigValue


@base_class
class NestedConfigValue(ConfigValue):
    def __attrs_post_init__(self) -> None:
        # If this ConfigValue holds a dict,
        # replace all nested dict values with NestedConfigValue.
        if self.is_dict():
            value_dict = self.raw
            # Iterate over a copy of items so we can safely modify in place
            for key, val in list(value_dict.items()):
                self.raw[key] = self._wrap(val)
        # If this ConfigValue holds a list/tuple,
        # wrap each element consistently as ConfigValue/NestedConfigValue.
        elif self.is_list() or self.is_tuple():
            seq = self.raw
            wrapped = [self._wrap(v) for v in seq]
            # Preserve tuple/list type
            self.raw = tuple(wrapped) if self.is_tuple() else wrapped

    @classmethod
    def _wrap(cls, val: Any) -> ConfigValue:
        """
        Recursively wrap:
        - any dict into NestedConfigValue(raw=dict)
        - lists/tuples into the same type with wrapped elements
        - everything else unchanged
        """
        from collections.abc import Mapping, Sequence

        # Case 1: dict / Mapping → wrap in NestedConfigValue
        if isinstance(val, Mapping):
            return cls(raw=dict(val))

        # Case 2: sequences (list/tuple), but not str/bytes
        # Return a NestedConfigValue so traversal always hits a node
        # capable of get_config_item. Element wrapping is handled in initialization fields.
        if isinstance(val, Sequence) and not isinstance(val, (str, bytes, bytearray)):
            return cls(raw=val)

        # Case 3: primitive / other types → unchanged
        return ConfigValue(raw=val)

    def get_config_item(self, key: Any, default: Any = None) -> ConfigValue | None:
        # Dict access by string key
        if self.is_dict() and isinstance(key, str) and key in self.raw:
            return self.raw[key]

        # List/Tuple access by integer index (also accept str indices like "0")
        if self.is_list() or self.is_tuple():
            idx: int | None = None
            if isinstance(key, int):
                idx = key
            elif isinstance(key, str) and (
                key.isdigit() or (key.startswith("-") and key[1:].isdigit())
            ):
                try:
                    idx = int(key)
                except ValueError:
                    idx = None
            if idx is not None:
                seq = self.raw
                if -len(seq) <= idx < len(seq):
                    return seq[idx]
        return ConfigValue(raw=default)

    def search(
        self,
        path: str,
        separator: str = DICT_PATH_SEPARATOR_DEFAULT,
        default: Any = None,
    ) -> ConfigValue:
        """
        Traverse nested dict/list/tuple values by a separated path.
        Example: search("first.second.0.third").
        Returns a ConfigValue/NestedConfigValue if found, else None.
        Assumes nested containers are wrapped as NestedConfigValue.
        """
        if not path:
            return self

        current: ConfigValue | None = self
        for part in path.split(separator):
            if not isinstance(current, NestedConfigValue):
                return ConfigValue(raw=default if default is not None else None)
            current = current.get_config_item(part)
            if current is None:
                return ConfigValue(raw=default if default is not None else None)

        return current

    def set_by_path(
        self,
        path: str,
        value: Any,
        separator: str = DICT_PATH_SEPARATOR_DEFAULT,
        create_missing: bool = True,
    ) -> None:
        """
        Set a value at a nested path.
        Example: set_by_path("global.version", "0.1.0")

        Args:
            path: Dot-separated path to the value (e.g., "global.version")
            value: The value to set
            separator: Path separator (default: ".")
            create_missing: If True, creates missing intermediate dicts

        Raises:
            ValueError: If the path is invalid or intermediate values are not dicts
        """
        if not path:
            raise ValueError("Path cannot be empty")

        if not self.is_dict():
            raise ValueError("Can only set values on dict-based NestedConfigValue")

        parts = path.split(separator)
        current = self.raw

        # Navigate to the parent of the target
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                if create_missing:
                    current[part] = self._wrap({})
                else:
                    raise ValueError(
                        f"Path '{separator.join(parts[:i+1])}' does not exist"
                    )

            next_item = current[part]
            if not isinstance(next_item, NestedConfigValue) or not next_item.is_dict():
                raise ValueError(
                    f"Cannot traverse path at '{separator.join(parts[:i+1])}': "
                    f"not a dict"
                )
            current = next_item.raw

        # Set the final value
        final_key = parts[-1]
        current[final_key] = self._wrap(value)

    def to_dict(self) -> dict[str, Any]:
        """Recursively dump to a native dict.

        If the underlying value isn't a dict, fallback to the base conversion.
        """
        if not self.is_dict():
            # Fallback – may still contain wrapped values; ensure we unwrap keys
            raw = super().to_dict()
            return {k: self._unwrap(v) for k, v in raw.items()}
        return {k: self._unwrap(v) for k, v in self.raw.items()}

    def to_list(self) -> list[Any]:
        """Recursively dump to a native list (tuples become lists)."""
        if self.is_list() or self.is_tuple():
            return [self._unwrap(v) for v in self.raw]
        # Fallback to base, then unwrap any items just in case
        base_list = super().to_list()
        return [self._unwrap(v) for v in base_list]

    def update_nested(self, data: dict[str, Any]) -> None:
        """
        Update the nested structure with values from a dict.
        Example: update_nested({"global": {"version": "0.1.0"}})

        This method recursively merges the provided dict into the existing structure.

        Args:
            data: Dictionary with nested structure to merge

        Raises:
            ValueError: If this ConfigValue is not a dict
        """
        if not self.is_dict():
            raise ValueError("Can only update dict-based NestedConfigValue")

        self._update_nested_recursive(self.raw, data)

    def _unwrap(self, value: Any) -> Any:
        """Return a native Python object from any ConfigValue/NestedConfigValue.

        - NestedConfigValue(dict)  -> dict with unwrapped children
        - NestedConfigValue(list/tuple) -> list with unwrapped children
        - ConfigValue(primitives) -> primitive raw value
        - Bare Mapping/Sequence (shouldn't happen after wrapping) -> recurse best-effort
        """
        from collections.abc import Mapping, Sequence

        if isinstance(value, NestedConfigValue):
            if value.is_dict():
                return value.to_dict()
            if value.is_list() or value.is_tuple():
                return value.to_list()
            return value._get_nested_raw()
        if isinstance(value, ConfigValue):
            return value._get_nested_raw()
        # Best-effort for unexpected raw containers
        if isinstance(value, Mapping):
            return {k: self._unwrap(v) for k, v in value.items()}
        if isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        ):
            return [self._unwrap(v) for v in value]
        return value

    def _update_nested_recursive(
        self, target: dict[str, ConfigValue], source: dict[str, Any]
    ) -> None:
        """
        Recursively merge source dict into target dict.

        Args:
            target: Target dict (with ConfigValue values)
            source: Source dict (with raw Python values)
        """
        for key, value in source.items():
            if key in target:
                existing = target[key]
                # If both are dicts, merge recursively
                if (
                    isinstance(existing, NestedConfigValue)
                    and existing.is_dict()
                    and isinstance(value, dict)
                ):
                    self._update_nested_recursive(existing.raw, value)
                else:
                    # Otherwise, replace with new wrapped value
                    target[key] = self._wrap(value)
            else:
                # Key doesn't exist, add it
                target[key] = self._wrap(value)
