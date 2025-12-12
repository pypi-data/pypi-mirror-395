from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.dict import dict_interpolate

from wexample_app.const.path import APP_DIR_NAME_TMP
from wexample_app.workdir.mixin.with_config_mixin import WithConfigMixin
from wexample_app.workdir.mixin.with_env_parameters_mixin import WithEnvParametersMixin

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue
    from wexample_filestate.item.file.yaml_file import YamlFile


@base_class
class WithRuntimeConfigMixin(WithEnvParametersMixin, WithConfigMixin):
    def build_runtime_config_value(self) -> NestedConfigValue:
        from wexample_config.config_value.nested_config_value import NestedConfigValue
        from wexample_helpers.helpers.dict import dict_merge

        return NestedConfigValue(
            raw=dict_interpolate(
                dict_merge(
                    self.get_config().to_dict(),
                    self.get_config(env_name=self.get_app_env()).to_dict_or_none()
                    or {},
                ),
                self.get_env_parameters().to_dict(),
            )
        )

    def get_runtime_config(self, rebuild: bool = False) -> NestedConfigValue:
        runtime_config_file = self.get_runtime_config_file()
        if rebuild or not runtime_config_file.get_path().exists():
            runtime_config_file.write_config(self.build_runtime_config_value())

        return runtime_config_file.read_config()

    def get_runtime_config_file(self) -> YamlFile:
        from wexample_app.const.globals import (
            APP_FILE_APP_RUNTIME_CONFIG,
            WORKDIR_SETUP_DIR,
        )

        # We don't search into the target item tree as this is a low level information.
        return self.get_yaml_file_from_path(
            path=self.get_path()
            / WORKDIR_SETUP_DIR
            / APP_DIR_NAME_TMP
            / APP_FILE_APP_RUNTIME_CONFIG,
        )

    def write_config_value(self, *args, **kwargs) -> None:
        self.get_config_file().write_config_value(*args, **kwargs)
        self.get_runtime_config(rebuild=True)
