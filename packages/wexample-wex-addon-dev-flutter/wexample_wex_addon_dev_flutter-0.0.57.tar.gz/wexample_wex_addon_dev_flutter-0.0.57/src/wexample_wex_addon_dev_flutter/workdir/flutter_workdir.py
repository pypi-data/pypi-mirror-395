from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.options_provider.abstract_options_provider import (
    AbstractOptionsProvider,
)
from wexample_helpers.decorator.base_class import base_class
from wexample_wex_addon_app.workdir.code_base_workdir import CodeBaseWorkdir
from wexample_wex_addon_app.workdir.mixin.with_license_workdir_mixin import WithLicenseWorkdirMixin

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_filestate.option.children_file_factory_option import (
        ChildrenFileFactoryOption,
    )

    from wexample_wex_addon_dev_flutter.file.flutter_pubspec_yaml_file import (
        FlutterPubspecYamlFile,
    )


@base_class
class FlutterWorkdir(WithLicenseWorkdirMixin, CodeBaseWorkdir):
    def get_app_config_file(self, reload: bool = True) -> FlutterPubspecYamlFile:
        from wexample_wex_addon_dev_flutter.file.flutter_pubspec_yaml_file import (
            FlutterPubspecYamlFile,
        )

        config_file = self.find_by_type(FlutterPubspecYamlFile)
        # Read once to populate content with file source.
        config_file.read_text(reload=reload)
        return config_file

    def get_dependencies_versions(self) -> dict[str, str]:
        return self.get_app_config_file().get_dependencies_versions()

    def get_main_code_file_extension(self) -> str:
        return "dart"

    def get_options_providers(self) -> list[type[AbstractOptionsProvider]]:
        from wexample_filestate_flutter.options_provider.flutter_options_provider import (
            FlutterOptionsProvider,
        )

        options = super().get_options_providers()

        options.extend(
            [
                FlutterOptionsProvider,
            ]
        )

        return options

    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_helpers.helpers.array import array_dict_get_by

        from wexample_wex_addon_dev_flutter.file.flutter_pubspec_yaml_file import (
            FlutterPubspecYamlFile,
        )

        raw_value = super().prepare_value(raw_value=raw_value)

        children = raw_value["children"]

        children.append(
            {
                "class": FlutterPubspecYamlFile,
                "name": "pubspec.yaml",
                "type": DiskItemType.FILE,
                "should_exist": True,
            }
        )

        # Add common Flutter ignores
        array_dict_get_by("name", ".gitignore", children).setdefault(
            "should_contain_lines", []
        ).extend(
            [
                ".dart_tool/",
                "build/",
                ".packages",
                ".flutter-plugins",
                ".flutter-plugins-dependencies",
                ".flutter-plugins-android",
                ".flutter-plugins-ios",
            ]
        )

        children.extend(
            [
                {
                    "name": "lib",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_flutter_file_children_filter(),
                    ],
                },
                {
                    "name": "test",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True,
                    "children": [
                        self._create_flutter_file_children_filter(),
                    ],
                },
                {
                    "name": ".publignore",
                    "type": DiskItemType.FILE,
                    "should_exist": True,
                },
            ]
        )

        self.append_license(raw_value)

        return raw_value

    def _create_flutter_file_children_filter(self) -> ChildrenFileFactoryOption:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.option.children_filter_option import (
            ChildrenFilterOption,
        )
        from wexample_filestate_flutter.file.flutter_file import FlutterFile
        from wexample_filestate_flutter.option.flutter.dart_format_option import (
            DartFormatOption,
        )

        return ChildrenFilterOption(
            pattern={
                "class": FlutterFile,
                "type": DiskItemType.FILE,
                "flutter": [
                    DartFormatOption.get_name(),
                ],
            },
            name_pattern=r"^.*\.dart$",
            recursive=True,
        )

    def _safe_shell(self, cmd, cwd) -> None:
        import subprocess
        from wexample_helpers.helpers.shell import shell_run
        try:
            shell_run(cmd, inherit_stdio=True, cwd=cwd)
        except subprocess.CalledProcessError as e:
            if e.returncode != 65:
                raise
            self.warning(f"Command {cmd} returned warnings (exit code 65).")

    def _publish(self, force=False) -> None:
        cwd = self.get_path()

        self._safe_shell(["flutter", "pub", "publish", "--dry-run"], cwd)

        publish_cmd = ["flutter", "pub", "publish"] + (["--force"] if force else [])
        self._safe_shell(publish_cmd, cwd)
