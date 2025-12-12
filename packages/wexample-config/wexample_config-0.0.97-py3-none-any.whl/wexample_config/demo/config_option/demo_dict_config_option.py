from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class DemoDictConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return dict[str, dict[str, Any]]
