from __future__ import annotations

from typing import Any

from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class PhpConfigValue(ConfigValue):
    phpcs_fixer: bool | None = public_field(
        default=None,
        description="Fix PHP code style using PHP-CS-Fixer",
    )
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )

    def to_option_raw_value(self) -> Any:
        from wexample_filestate_php.config_option.phpcs_fixer_config_option import (
            PhpcsFixerConfigOption,
        )

        return {
            PhpcsFixerConfigOption.get_name(): self.phpcs_fixer,
        }
