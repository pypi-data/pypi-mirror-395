from __future__ import annotations

import os
import subprocess
from typing import TYPE_CHECKING

from wexample_helpers.helpers.string import string_to_kebab_case

from wexample_wex_addon_dev_javascript.workdir.javascript_workdir import (
    JavascriptWorkdir,
)

if TYPE_CHECKING:
    from wexample_filestate.config_value.readme_content_config_value import (
        ReadmeContentConfigValue,
    )
    from wexample_wex_addon_app.workdir.framework_packages_suite_workdir import (
        FrameworkPackageSuiteWorkdir,
    )


class JavascriptPackageWorkdir(JavascriptWorkdir):
    def get_package_import_name(self) -> str:
        """Get the full package import name with vendor prefix."""
        return (
            f"@{self.get_vendor_name()}/{string_to_kebab_case(self.get_project_name())}"
        )

    def _get_readme_content(self) -> ReadmeContentConfigValue | None:
        from wexample_wex_addon_dev_javascript.config_value.javascript_package_readme_config_value import (
            JavascriptPackageReadmeContentConfigValue,
        )

        return JavascriptPackageReadmeContentConfigValue(workdir=self)

    def _get_suite_package_workdir_class(self) -> type[FrameworkPackageSuiteWorkdir]:
        from wexample_wex_addon_dev_javascript.workdir.javascript_packages_suite_workdir import (
            JavascriptPackagesSuiteWorkdir,
        )

        return JavascriptPackagesSuiteWorkdir

    def _publish(self, force: bool = False) -> None:
        """Publish the package to npm, skipping if the version already exists."""
        from wexample_helpers.helpers.shell import shell_run

        package_name = self.get_package_name()
        version = self.get_project_version()
        registry = self.get_env_parameter_or_suite_fallback(
            key="NPM_REGISTRY", default="https://registry.npmjs.org"
        )

        # Detect if the version already exists on the registry
        release_exists = False
        try:
            shell_run(
                [
                    "npm",
                    "view",
                    f"{package_name}@{version}",
                    "version",
                    "--registry",
                    registry,
                ],
                cwd=self.get_path(),
                inherit_stdio=False,
            )
            release_exists = True
        except subprocess.CalledProcessError:
            release_exists = False

        if release_exists and not force:
            self.warning(
                f'Trying to publish an existing release for package "{package_name}" version {version}'
            )
            return

        token = self.get_env_parameter_or_suite_fallback("NPM_TOKEN")
        env = os.environ.copy()
        host = registry.rstrip("/").split("://")[-1]

        if registry:
            env["npm_config_registry"] = registry
        if token:
            env["NPM_TOKEN"] = token
            env[f"npm_config_//{host}/:_authToken"] = token

        shell_run(
            ["npm", "publish", "--registry", registry],
            cwd=self.get_path(),
            env=env,
            inherit_stdio=True,
        )
