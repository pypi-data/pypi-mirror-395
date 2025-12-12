from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_filestate.option.mixin.with_docker_option_mixin import (
    WithDockerOptionMixin,
)
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class PhpOption(OptionMixin, WithDockerOptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate_php.config_value.php_config_value import (
            PhpConfigValue,
        )

        return Union[list[str], dict, PhpConfigValue]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        return self._create_child_required_operation(target=target, scopes=scopes)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        # Import all the config options for each PHP operation
        from wexample_filestate_php.option.php.phpcs_fixer_option import (
            PhpcsFixerOption,
        )

        return [
            # filestate: php-iterable-sort
            PhpcsFixerOption,
        ]

    def set_value(self, raw_value: Any) -> None:
        # Convert list form to dict form for consistency
        if isinstance(raw_value, list):
            dict_value = {}
            for option_name in raw_value:
                dict_value[option_name] = True
            raw_value = dict_value

        super().set_value(raw_value=raw_value)
