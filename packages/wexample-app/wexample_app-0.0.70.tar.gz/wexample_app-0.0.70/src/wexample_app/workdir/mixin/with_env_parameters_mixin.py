from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.mixin.has_env_keys import HasEnvKeys
from wexample_helpers.decorator.base_class import base_class

from wexample_app.const.globals import WORKDIR_SETUP_DIR

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue


@base_class
class WithEnvParametersMixin(HasEnvKeys):
    @classmethod
    def get_env_parameters_from_path(cls, path: Path) -> NestedConfigValue:
        from wexample_config.config_value.nested_config_value import NestedConfigValue
        from wexample_filestate.item.file.env_file import EnvFile

        env_path = path / WORKDIR_SETUP_DIR / EnvFile.EXTENSION_DOT_ENV

        if env_path.exists():
            dot_env = EnvFile.create_from_path(path=env_path)
            return dot_env.read_config()

        return NestedConfigValue(raw={})

    def get_env_parameter(self, key: str, default: str | None = None) -> str | None:
        # Search in .env.
        value = (
            self.get_env_parameters()
            .get_config_item(key=key, default=default)
            .get_str_or_none()
        )

        if value is None:
            return super().get_env_parameter(
                key=key,
                default=default,
            )

        return value

    def get_env_parameters(self) -> NestedConfigValue:
        return self.get_env_parameters_from_path(
            path=self.get_path(),
        )

    def set_env_parameter(self, key: str, value: str) -> None:
        """
        Save a single environment parameter to the .env file and update env_config.

        Args:
            key: The environment variable key
            value: The value to set
        """
        self.set_env_parameters({key: value})

    def set_env_parameters(self, parameters: dict[str, str]) -> None:
        """
        Save multiple environment parameters to the .env file in batch and update env_config.

        Args:
            parameters: Dictionary of key-value pairs to save
        """
        from wexample_filestate.item.file.env_file import EnvFile

        # Update env_config in memory via parent class
        super().set_env_parameters(parameters)

        # Get env file path and ensure directory exists
        env_path = self._get_env_file_path()
        env_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing config and update with new parameters
        config = self.get_env_parameters()
        config.update_nested(parameters)

        # Write back to file
        dot_env = EnvFile.create_from_path(path=env_path)
        dot_env.write_config(value=config)

    def _get_env_file_path(self) -> Path:
        """Get the path to the .env file."""
        from wexample_filestate.item.file.env_file import EnvFile

        return self.get_path() / WORKDIR_SETUP_DIR / EnvFile.EXTENSION_DOT_ENV
