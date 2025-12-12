from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_wex_addon_dev_flutter.workdir.flutter_workdir import FlutterWorkdir

if TYPE_CHECKING:
    from wexample_filestate.config_value.readme_content_config_value import (
        ReadmeContentConfigValue,
    )
    from wexample_wex_addon_app.workdir.framework_packages_suite_workdir import (
        FrameworkPackageSuiteWorkdir,
    )


class FlutterPackageWorkdir(FlutterWorkdir):
    def _get_readme_content(self) -> ReadmeContentConfigValue | None:
        from wexample_wex_addon_dev_flutter.config_value.flutter_package_readme_config_value import (
            FlutterPackageReadmeContentConfigValue,
        )

        return FlutterPackageReadmeContentConfigValue(workdir=self)

    def _get_suite_package_workdir_class(self) -> type[FrameworkPackageSuiteWorkdir]:
        from wexample_wex_addon_dev_flutter.workdir.flutter_packages_suite_workdir import (
            FlutterPackagesSuiteWorkdir,
        )

        return FlutterPackagesSuiteWorkdir
