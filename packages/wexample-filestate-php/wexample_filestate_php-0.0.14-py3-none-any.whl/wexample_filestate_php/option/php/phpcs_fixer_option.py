from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from .abstract_php_file_content_option import AbstractPhpFileContentOption

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class PhpcsFixerOption(AbstractPhpFileContentOption):
    def get_description(self) -> str:
        return "Fix PHP code style using PHP-CS-Fixer."

    def _apply_content_change(self, target: TargetFileOrDirectoryType) -> str:
        """Fix PHP code style using PHP-CS-Fixer via Docker."""
        # Get the file path inside the container
        container_file_path = self._get_container_file_path(target)

        # Execute php-cs-fixer in Docker with centralized config
        self._execute_in_docker(
            target=target,
            command=[
                "php-cs-fixer",
                "fix",
                "--config=/root/.php-cs-fixer.dist.php",
                container_file_path,
            ],
        )

        # Read the fixed content from the file (it was modified in place)
        return target.read_text()
