from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.options_provider.abstract_options_provider import (
    AbstractOptionsProvider,
)
from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_filestate.option.children_file_factory_option import (
        ChildrenFileFactoryOption,
    )

    from wexample_wex_addon_dev_javascript.file.javascript_package_json_file import (
        JavascriptPackageJsonFile,
    )


class JavascriptWorkdir(CodeBaseWorkdir):
    def get_app_config_file(self, reload: bool = True) -> JavascriptPackageJsonFile:
        from wexample_wex_addon_dev_javascript.file.javascript_package_json_file import (
            JavascriptPackageJsonFile,
        )

        config_file = self.find_by_type(JavascriptPackageJsonFile)
        # Read once to populate content with file source.
        config_file.read_text(reload=reload)
        return config_file

    def get_dependencies_versions(self) -> dict[str, str]:
        return self.get_app_config_file().get_dependencies_versions()

    def get_main_code_file_extension(self) -> str:
        return "js"

    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        from wexample_filestate_javascript.options_provider.javascript_options_provider import (
            JavascriptOptionsProvider,
        )

        options = super().get_options_providers()

        options.extend(
            [
                JavascriptOptionsProvider,
            ]
        )

        return options

    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_helpers.helpers.array import array_dict_get_by

        from wexample_wex_addon_dev_javascript.file.javascript_package_json_file import (
            JavascriptPackageJsonFile,
        )

        raw_value = super().prepare_value(raw_value=raw_value)

        # Ensure a package.json file exists for any JavaScript package project
        children = raw_value["children"]

        children.append(
            {
                "class": JavascriptPackageJsonFile,
                "name": "package.json",
                "type": DiskItemType.FILE,
                "should_exist": True,
            }
        )

        # Add rules to .gitignore
        array_dict_get_by("name", ".gitignore", children).setdefault(
            "should_contain_lines", []
        ).extend(
            [
                "node_modules/",
                "dist/",
                "build/",
                ".npm",
                ".eslintcache",
            ]
        )

        children.extend(
            [
                {
                    "name": "tests",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_javascript_file_children_filter(),
                    ],
                },
                {
                    "name": "src",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_javascript_file_children_filter(),
                    ],
                },
            ]
        )

        return raw_value

    def _create_javascript_file_children_filter(self) -> ChildrenFileFactoryOption:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )
        from wexample_filestate_javascript.file.javascript_file import JavascriptFile
        from wexample_filestate_javascript.option.javascript.biome_option import (
            BiomeOption,
        )

        # Using a generic pattern since there's no specific JavascriptFile class yet
        return ChildrenFilterOption(
            pattern={
                "class": JavascriptFile,
                "type": DiskItemType.FILE,
                "javascript": [BiomeOption.get_name()],
            },
            name_pattern=r"^.*\.(js|jsx|ts|tsx)$",
            recursive=True,
        )
