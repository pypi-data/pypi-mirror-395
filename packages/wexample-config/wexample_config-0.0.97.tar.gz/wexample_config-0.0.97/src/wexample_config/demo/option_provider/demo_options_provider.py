from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.options_provider.abstract_options_provider import (
    AbstractOptionsProvider,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


class DemoOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> list[type[AbstractConfigOption]]:
        from wexample_config.config_option.children_config_option import (
            ChildrenConfigOption,
        )
        from wexample_config.config_option.name_config_option import NameConfigOption
        from wexample_config.demo.config_option.demo_custom_value_config_option import (
            DemoCustomValueConfigOption,
        )
        from wexample_config.demo.config_option.demo_dict_config_option import (
            DemoDictConfigOption,
        )
        from wexample_config.demo.config_option.demo_extensible_config_option import (
            DemoExtensibleConfigOption,
        )
        from wexample_config.demo.config_option.demo_list_config_option import (
            DemoListConfigOption,
        )
        from wexample_config.demo.config_option.demo_nested_config_option import (
            DemoNestedConfigOption,
        )
        from wexample_config.demo.config_option.demo_union_config_option import (
            DemoUnionConfigOption,
        )

        return [
            ChildrenConfigOption,
            DemoCustomValueConfigOption,
            DemoDictConfigOption,
            DemoExtensibleConfigOption,
            DemoListConfigOption,
            DemoNestedConfigOption,
            DemoUnionConfigOption,
            NameConfigOption,
        ]
