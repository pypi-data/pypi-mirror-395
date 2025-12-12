from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_addon_app.workdir.framework_packages_suite_workdir import (
    FrameworkPackageSuiteWorkdir,
)

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir


class JavascriptPackagesSuiteWorkdir(FrameworkPackageSuiteWorkdir):
    def _child_is_package_directory(self, entry: Path) -> bool:
        return entry.is_dir() and (entry / "package.json").is_file()

    def _get_children_package_directory_name(self) -> str:
        return "npm"

    def _get_children_package_workdir_class(self) -> type[CodeBaseWorkdir]:
        from wexample_wex_addon_dev_javascript.workdir.javascript_package_workdir import (
            JavascriptPackageWorkdir,
        )

        return JavascriptPackageWorkdir
