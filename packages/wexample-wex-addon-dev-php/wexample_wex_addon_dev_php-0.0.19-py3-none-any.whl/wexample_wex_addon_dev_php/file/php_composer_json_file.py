from __future__ import annotations

from wexample_filestate.item.file.json_file import JsonFile
from wexample_helpers.decorator.base_class import base_class


@base_class
class PhpComposerJsonFile(JsonFile):
    def add_dependency(
        self,
        package_name: str,
        version: str,
        operator: str = "",
        optional: bool = False,
        group: None | str = None,
    ) -> bool:
        """
        Add or update a Composer dependency.
        Returns True if the dependency list changed.
        """
        # Composer group
        group_key = "require-dev" if group == "dev" else "require"

        # Composer does not use operators like pip (==, >=, etc.)
        # So operator is simply prepended if provided.
        constraint = f"{operator}{version}".strip()

        config = self.read_config()

        # Extract or create dependency dictionary
        deps_node = config.search(path=group_key, default={})
        deps = deps_node.to_dict() if deps_node else {}

        old = deps.get(package_name)

        # Nothing changes
        if old == constraint:
            return False

        # Apply change
        deps[package_name] = constraint

        config_updated = {}
        config_updated[group_key] = deps
        config.update_nested(data=config_updated)

        self.write_config(config)

        return True

    def get_dependencies_versions(
        self, optional: bool = False, group: str = "dev"
    ) -> dict[str, str]:
        # Default values is not well managed in nested config value, for now.
        require = self.read_config().search(path="require")

        if not require:
            return {}

        return require.to_dict()

    def dumps(self, content: dict | None = None) -> str:
        content = content or self.read_parsed()
        content["version"] = self.get_parent_item().get_project_version()

        return super().dumps(content or {})
