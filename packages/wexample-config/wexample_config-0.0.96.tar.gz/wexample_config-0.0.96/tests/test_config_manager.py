from __future__ import annotations

from typing import Any

import pytest


class TestConfigManager:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        from wexample_config.demo.demo_config_manager import DemoConfigManager

        self.config_manager = DemoConfigManager()

    def test_configure_callback(self) -> None:
        from wexample_config.config_value.callback_render_config_value import (
            CallbackRenderConfigValue,
        )

        def _name(option: Any) -> str:
            return "yes"

        self.config_manager.set_value({"name": CallbackRenderConfigValue(raw=_name)})

        assert self.config_manager.get_option("name").get_value().is_str()

    def test_configure_custom_value_type(self) -> None:
        from wexample_helpers.exception.not_allowed_variable_type_exception import (
            NotAllowedVariableTypeException,
        )

        from wexample_config.config_value.custom_type_config_value import (
            CustomTypeConfigValue,
        )
        from wexample_config.demo.config_option.demo_custom_value_config_option import (
            DemoCustomValueConfigOption,
        )

        with pytest.raises(NotAllowedVariableTypeException):
            self.config_manager.set_value(
                {"demo_custom_value": CustomTypeConfigValue(raw=123)}
            )

        self.config_manager.set_value(
            {"demo_custom_value": CustomTypeConfigValue(raw="yeah")}
        )

        assert (
            self.config_manager.get_option(DemoCustomValueConfigOption)
            .get_value()
            .is_str()
        )
        assert (
            self.config_manager.get_option(DemoCustomValueConfigOption)
            .get_value()
            .get_str()
            == "yeah"
        )

    def test_configure_extensible(self) -> None:
        from wexample_config.demo.config_option.demo_extensible_config_option import (
            DemoExtensibleConfigOption,
        )
        from wexample_config.exception.invalid_option_exception import (
            InvalidOptionException,
        )

        # Extensible children option
        self.config_manager.set_value(
            {
                "demo_extensible": {
                    "unexpected_option": "yes",
                    "unexpected_dict": {
                        "unexpected_option": "yay",
                    },
                }
            }
        )

        assert (
            self.config_manager.get_option(DemoExtensibleConfigOption)
            .get_value()
            .is_dict()
        )

        # Unexpected option fails on current
        with pytest.raises(InvalidOptionException):
            self.config_manager.set_value({"lorem": "ipsum"})

    def test_configure_list_type(self) -> None:
        from wexample_helpers.exception.not_allowed_variable_type_exception import (
            NotAllowedVariableTypeException,
        )

        from wexample_config.demo.config_option.demo_list_config_option import (
            DemoListConfigOption,
        )

        with pytest.raises(NotAllowedVariableTypeException):
            self.config_manager.set_value({"demo_list": 123})

        self.config_manager.set_value({"demo_list": []})

        assert (
            self.config_manager.get_option(DemoListConfigOption).get_value().is_list()
        )

    def test_configure_name(self) -> None:
        from wexample_config.config_option.children_config_option import (
            ChildrenConfigOption,
        )
        from wexample_config.config_option.name_config_option import NameConfigOption

        self.config_manager.set_value({"name": "yes", "children": []})

        assert self.config_manager.get_value().is_dict()
        assert self.config_manager.get_key() == "demo_config_manager"
        assert len(self.config_manager.options)
        assert self.config_manager.get_option("name").get_value().is_str()
        assert self.config_manager.get_option_value(NameConfigOption).get_str() == "yes"
        assert self.config_manager.get_option_value(ChildrenConfigOption).is_list()

    def test_configure_nested_dict_type(self) -> None:
        from wexample_config.config_value.custom_type_config_value import (
            CustomTypeConfigValue,
        )
        from wexample_config.demo.config_option.demo_dict_config_option import (
            DemoDictConfigOption,
        )
        from wexample_config.demo.config_option.demo_nested_config_option import (
            DemoNestedConfigOption,
        )

        self.config_manager.set_value(
            {
                "demo_nested": {
                    "name": "FIRST_LEVEL_DICT",
                    "demo_dict": {
                        "lorem": {
                            "info": "As the demo_dict is typed, we should have sub dicts"
                            "the type is like: Dict[str, Dict[str, Any]]",
                            "other": 123,
                            "demo_custom_value": CustomTypeConfigValue(raw="yeah"),
                        },
                    },
                }
            }
        )

        # Main dict is saved
        assert isinstance(self.config_manager.get_value().get_dict(), dict)

        option = self.config_manager.get_option(DemoNestedConfigOption)
        assert isinstance(option, DemoNestedConfigOption)

        # Subclass has been created
        option = self.config_manager.get_option_recursive(DemoDictConfigOption)

        assert isinstance(option, DemoDictConfigOption)
        assert isinstance(option.get_value().get_dict().get("lorem"), dict)

    def test_configure_unexpected(self) -> None:
        from wexample_config.exception.invalid_option_exception import (
            InvalidOptionException,
        )

        with pytest.raises(InvalidOptionException):
            self.config_manager.set_value({"unexpected_option": "yes"})

    def test_configure_unexpected_type(self) -> None:
        from wexample_helpers.exception.not_allowed_variable_type_exception import (
            NotAllowedVariableTypeException,
        )

        with pytest.raises(NotAllowedVariableTypeException):
            self.config_manager.set_value({"name": 123})

        with pytest.raises(NotAllowedVariableTypeException):
            self.config_manager.set_value({"name": []})

    def test_configure_union_type(self) -> None:
        from wexample_helpers.exception.not_allowed_variable_type_exception import (
            NotAllowedVariableTypeException,
        )

        from wexample_config.demo.config_option.demo_union_config_option import (
            DemoUnionConfigOption,
        )

        with pytest.raises(NotAllowedVariableTypeException):
            self.config_manager.set_value({"demo_union": 123})

        self.config_manager.set_value({"demo_union": "hey"})

        assert (
            self.config_manager.get_option(DemoUnionConfigOption).get_value().is_str()
        )

        self.config_manager.set_value({"demo_union": {}})

        assert (
            self.config_manager.get_option(DemoUnionConfigOption).get_value().is_dict()
        )

    def test_setup(self) -> None:
        from wexample_config.demo.demo_config_manager import DemoConfigManager

        assert isinstance(self.config_manager, DemoConfigManager)
