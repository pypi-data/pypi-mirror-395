from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoExtensibleConfigOption(AbstractConfigOption):
    @staticmethod
    def get_allowed_types() -> Any:
        return list
