from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.classes.abstract_config_manager import AbstractConfigManager

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )


class DemoConfigManager(AbstractConfigManager):
    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        from wexample_config.demo.option_provider.demo_options_provider import (
            DemoOptionsProvider,
        )

        return [
            DemoOptionsProvider,
        ]
