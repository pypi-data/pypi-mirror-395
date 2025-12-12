from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.helpers.string import string_to_pascal_case
from wexample_helpers_git.helpers.git import (
    git_tag_exists,
    git_tag_annotated,
)
from wexample_wex_addon_app.workdir.framework_packages_suite_workdir import (
    FrameworkPackageSuiteWorkdir,
)
from wexample_wex_addon_dev_php.workdir.php_workdir import PhpWorkdir

if TYPE_CHECKING:
    from wexample_filestate.config_value.readme_content_config_value import (
        ReadmeContentConfigValue,
    )
    from wexample_filestate.utils.search_result import SearchResult


class PhpPackageWorkdir(PhpWorkdir):
    def _get_readme_content(self) -> ReadmeContentConfigValue | None:
        from wexample_wex_addon_dev_php.config_value.php_package_readme_config_value import (
            PhpPackageReadmeContentConfigValue,
        )

        return PhpPackageReadmeContentConfigValue(workdir=self)

    def _get_suite_package_workdir_class(self) -> type[FrameworkPackageSuiteWorkdir]:
        from wexample_wex_addon_dev_php.workdir.php_packages_suite_workdir import (
            PhpPackagesSuiteWorkdir,
        )

        return PhpPackagesSuiteWorkdir

    def get_package_import_name(self) -> str:
        """Get the full package import name with vendor prefix."""
        return f"{string_to_pascal_case(self.get_vendor_name())}\\{string_to_pascal_case(self.get_project_name())}"

    def search_imports_in_codebase(
        self, searched_package: PhpPackageWorkdir
    ) -> list[SearchResult]:
        """Find PHP `use`/qualified references to the given package."""
        import re

        pkg = re.escape(searched_package.get_package_import_name())
        pattern = rf"(?m)^\s*use\s+{pkg}(?:\\\\[\w]+)*\s*;|{pkg}(?:\\\\[\w]+)*"
        return self.search_in_codebase(pattern, regex=True, flags=re.MULTILINE)

    def search_in_codebase(
        self, string: str, *, regex: bool = False, flags: int = 0
    ) -> list[SearchResult]:
        from wexample_filestate.utils.search_result import SearchResult
        from wexample_filestate_php.file.php_file import PhpFile

        found: list[SearchResult] = []

        def _search(item: PhpFile) -> None:
            found.extend(
                SearchResult.create_for_all_matches(
                    string, item, regex=regex, flags=flags
                )
            )

        self.for_each_child_of_type_recursive(callback=_search, class_type=PhpFile)

        return found

    def _publish(self, force: bool = False) -> None:
        """Add a Packagist-friendly tag (vX.Y.Z) in addition to default tagging."""
        tag = f"v{self.get_project_version()}"
        cwd = self.get_path()

        if git_tag_exists(tag, cwd=cwd, inherit_stdio=False) and not force:
            self.log(
                f"Tag {tag} already exists, skipping creation (use --force to re-tag)."
            )
        else:
            git_tag_annotated(tag, f"Release {tag}", cwd=cwd, inherit_stdio=True)

        # Uses git repo to deploy packages.
        self.push_to_deployment_remote()

    def get_package_name(self) -> str:
        from wexample_helpers.helpers.string import string_to_kebab_case

        return f"{string_to_kebab_case(self.get_vendor_name())}/{string_to_kebab_case(self.get_project_name())}"
