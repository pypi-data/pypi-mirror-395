from __future__ import annotations


def debug_handle_app_error(
    e: Exception, debug_config_file_name: str = ".env.yml"
) -> None:
    import os
    import sys

    from wexample_helpers.helpers.error import error_format
    from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read_dict

    # Load debug configuration from YAML
    debug_config = yaml_read_dict(os.path.join(os.getcwd(), debug_config_file_name))

    print(error_format(error=e, paths_map=debug_config.get("host_paths_map", {})))

    # Exit with error code to signal failure to calling process
    sys.exit(1)
