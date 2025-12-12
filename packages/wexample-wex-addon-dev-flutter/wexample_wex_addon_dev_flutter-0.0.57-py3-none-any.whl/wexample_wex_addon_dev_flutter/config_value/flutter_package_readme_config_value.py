from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class
from wexample_wex_addon_app.config_value.app_readme_config_value import (
    AppReadmeConfigValue,
)


@base_class
class FlutterPackageReadmeContentConfigValue(AppReadmeConfigValue):
    """README generation for Flutter packages."""

    def _get_app_description(self) -> str:
        return self.workdir.get_app_config().get("description", "")
