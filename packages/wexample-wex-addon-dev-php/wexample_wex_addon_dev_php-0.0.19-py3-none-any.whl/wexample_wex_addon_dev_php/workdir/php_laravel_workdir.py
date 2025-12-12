from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_addon_dev_php.workdir.php_workdir import PhpWorkdir

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class PhpLaravelWorkdir(PhpWorkdir):
    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        from wexample_filestate.const.disk import DiskItemType

        raw_value = super().prepare_value(raw_value)

        children = raw_value["children"]

        children.extend(
            [
                {
                    "name": "tests",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_python_file_children_filter(),
                    ],
                },
            ]
        )

        return raw_value
