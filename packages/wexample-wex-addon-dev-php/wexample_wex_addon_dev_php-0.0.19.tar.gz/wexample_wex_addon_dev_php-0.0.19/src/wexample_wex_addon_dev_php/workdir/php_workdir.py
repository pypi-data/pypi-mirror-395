from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate_php.option.php.phpcs_fixer_option import PhpcsFixerOption
from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_filestate.option.children_file_factory_option import (
        ChildrenFileFactoryOption,
    )

    from wexample_wex_addon_dev_php.file.php_composer_json_file import (
        PhpComposerJsonFile,
    )


class PhpWorkdir(CodeBaseWorkdir):
    def get_app_config_file(self, reload: bool = True) -> PhpComposerJsonFile:
        from wexample_wex_addon_dev_php.file.php_composer_json_file import (
            PhpComposerJsonFile,
        )

        config_file = self.find_by_type(PhpComposerJsonFile)
        # Read once to populate content with file source.
        config_file.read_text(reload=reload)
        return config_file

    def get_dependencies_versions(self) -> dict[str, str]:
        return self.get_app_config_file().get_dependencies_versions()

    def get_main_code_file_extension(self) -> str:
        from wexample_filestate_php.const.php_file import PHP_FILE_EXTENSION

        return PHP_FILE_EXTENSION

    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        from wexample_filestate_php.options_provider.php_options_provider import (
            PhpOptionsProvider,
        )

        options = super().get_options_providers()

        options.extend(
            [
                PhpOptionsProvider,
            ]
        )

        return options

    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_helpers.helpers.array import array_dict_get_by

        from wexample_wex_addon_dev_php.file.php_composer_json_file import (
            PhpComposerJsonFile,
        )

        raw_value = super().prepare_value(raw_value=raw_value)

        # Ensure a composer.json file exists for any PHP package project
        children = raw_value["children"]

        children.append(
            {
                "class": PhpComposerJsonFile,
                "name": "composer.json",
                "type": DiskItemType.FILE,
                "should_exist": True,
            }
        )

        # Add rules to .gitignore
        array_dict_get_by("name", ".gitignore", children).setdefault(
            "should_contain_lines", []
        ).extend(
            [
                ".php-cs-fixer.cache",
                ".scannerwork",
                "/vendor",
            ]
        )

        children.extend(
            [
                {
                    "name": "tests",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_php_file_children_filter(),
                    ],
                },
                {
                    "name": "src",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_php_file_children_filter(),
                    ],
                },
            ]
        )

        return raw_value

    def _create_php_file_children_filter(self) -> ChildrenFileFactoryOption:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )
        from wexample_filestate_php.file.php_file import PhpFile

        return ChildrenFilterOption(
            pattern={
                "class": PhpFile,
                "type": DiskItemType.FILE,
                "php": [PhpcsFixerOption.get_name()],
            },
            name_pattern=r"^.*\.php$",
            recursive=True,
        )
