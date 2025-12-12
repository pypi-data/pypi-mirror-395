from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_addon_app.workdir.framework_packages_suite_workdir import (
    FrameworkPackageSuiteWorkdir,
)

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir


class FlutterPackagesSuiteWorkdir(FrameworkPackageSuiteWorkdir):
    def _child_is_package_directory(self, entry: Path) -> bool:
        return entry.is_dir() and (entry / "pubspec.yaml").is_file()

    def _get_children_package_directory_name(self) -> str:
        return "flutter"

    def _get_children_package_workdir_class(self) -> type[CodeBaseWorkdir]:
        from wexample_wex_addon_dev_flutter.workdir.flutter_package_workdir import (
            FlutterPackageWorkdir,
        )

        return FlutterPackageWorkdir
