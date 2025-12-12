from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.item.file.yaml_file import YamlFile
    from wexample_helpers.const.types import PathOrString


@base_class
class WithYamlFiles(BaseClass):
    def get_yaml_file_from_path(self, path: PathOrString) -> YamlFile:
        from wexample_filestate.item.file.yaml_file import YamlFile

        return YamlFile.create_from_path(path=path, io=self.io)
