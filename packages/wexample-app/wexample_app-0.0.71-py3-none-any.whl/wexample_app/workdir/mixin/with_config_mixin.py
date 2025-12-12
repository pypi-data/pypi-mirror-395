from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_app.const.globals import APP_FILE_APP_CONFIG_NAME
from wexample_app.workdir.mixin.with_yaml_files import WithYamlFiles

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue
    from wexample_filestate.item.file.yaml_file import YamlFile
    from wexample_helpers.const.types import FileStringOrPath


@base_class
class WithConfigMixin(WithYamlFiles):
    @classmethod
    def get_config_from_path(cls, path: FileStringOrPath) -> YamlFile | None:
        from pathlib import Path

        from wexample_filestate.item.file.yaml_file import YamlFile

        from wexample_app.const.globals import APP_FILE_APP_CONFIG, WORKDIR_SETUP_DIR

        setup_config_path = Path(path) / WORKDIR_SETUP_DIR / APP_FILE_APP_CONFIG

        if setup_config_path.exists():
            return YamlFile.create_from_path(
                path=setup_config_path,
            )

        return None

    def get_config(self, env_name: None | str = None) -> NestedConfigValue:
        from wexample_config.config_value.nested_config_value import NestedConfigValue

        config_file = self.get_config_file(env_name=env_name)
        if config_file.get_path().exists():
            return config_file.read_config()

        return NestedConfigValue(raw={})

    def get_config_file(self, env_name: None | str = None) -> YamlFile:
        from wexample_app.const.globals import APP_FILE_APP_CONFIG, WORKDIR_SETUP_DIR

        file_name = APP_FILE_APP_CONFIG
        if env_name:
            file_name = f"{APP_FILE_APP_CONFIG_NAME}.{env_name}.yml"

        # We don't search into the target item tree as this is a low level information.
        return self.get_yaml_file_from_path(
            path=self.get_path() / WORKDIR_SETUP_DIR / file_name
        )
