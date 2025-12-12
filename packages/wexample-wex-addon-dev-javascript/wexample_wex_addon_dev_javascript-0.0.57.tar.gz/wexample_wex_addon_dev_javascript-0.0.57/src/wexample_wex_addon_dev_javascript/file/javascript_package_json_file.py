from __future__ import annotations

from wexample_filestate.item.file.json_file import JsonFile
from wexample_helpers.decorator.base_class import base_class


@base_class
class JavascriptPackageJsonFile(JsonFile):
    def dumps(self, content: dict | None = None) -> str:
        content = content or self.read_parsed()

        workdir = self.get_parent_item()
        content["name"] = workdir.get_package_import_name()
        content["version"] = workdir.get_project_version()

        if not content.get("type"):
            content["type"] = "module"

        return super().dumps(content or {})

    def get_dependencies_versions(
        self, optional: bool = False, group: str = "dev"
    ) -> dict[str, str]:
        return (
            self.read_config()
            .search(path="dependencies")
            .get_dict_or_default(default={})
        )
