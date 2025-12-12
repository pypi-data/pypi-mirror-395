from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wexample_app.command.option import Option

ParsedArgs = dict[str, Any]


def argument_filter_core_options(
    arguments: list[str],
    core_options: list[Option],
) -> list[str]:
    """Filter out core options from arguments list without modifying the original.

    Args:
        arguments: List of command line arguments
        core_options: List of core Option objects to filter out

    Returns:
        New list with core options and their values removed
    """

    # Helper functions to find options
    def find_option_by_kebab_name(kebab_name: str) -> Option | None:
        for option in core_options:
            if option.kebab_name == kebab_name:
                return option
        return None

    def find_option_by_short_name(short_name: str) -> Option | None:
        for option in core_options:
            if option.short_name == short_name:
                return option
        return None

    filtered = []
    skip_next = False

    for i, arg in enumerate(arguments):
        if skip_next:
            skip_next = False
            continue

        is_core_option = False

        # Check for long option (--option)
        if arg.startswith("--"):
            option_name = arg[2:]
            option = find_option_by_kebab_name(option_name)
            if option:
                is_core_option = True
                # If not a flag, skip the next argument (the value)
                if (
                    not option.is_flag
                    and i + 1 < len(arguments)
                    and not arguments[i + 1].startswith("-")
                ):
                    skip_next = True

        # Check for short option (-o)
        elif arg.startswith("-") and len(arg) > 1:
            short_name = arg[1:]
            option = find_option_by_short_name(short_name)
            if option:
                is_core_option = True
                # If not a flag, skip the next argument (the value)
                if (
                    not option.is_flag
                    and i + 1 < len(arguments)
                    and not arguments[i + 1].startswith("-")
                ):
                    skip_next = True

        if not is_core_option:
            filtered.append(arg)

    return filtered


def argument_parse_options(
    arguments: list[str],
    options: list[Option],
    allowed_option_names: list[str] | None = None,
    strict: bool = True,
) -> ParsedArgs:
    """Parse raw command line arguments into a dictionary of option name to value.

    Args:
        arguments: List of command line arguments to parse
        options: List of Option objects defining the available options
        allowed_option_names: Optional list of allowed option names for error messages
        strict: If True, raise exception on unknown options. If False, ignore them.

    Returns:
        Dictionary mapping option names to their parsed values

    Raises:
        CommandUnexpectedArgumentException: If an unknown argument is encountered (strict mode only)
        CommandArgumentConversionException: If argument value conversion fails
    """
    from wexample_helpers.helpers.cli import cli_argument_convert_value

    from wexample_app.exception.command_argument_conversion_exception import (
        CommandArgumentConversionException,
    )
    from wexample_app.exception.command_unexpected_argument_exception import (
        CommandUnexpectedArgumentException,
    )

    # Helper functions to find options
    def find_option_by_kebab_name(kebab_name: str) -> Option | None:
        for option in options:
            if option.kebab_name == kebab_name:
                return option
        return None

    def find_option_by_short_name(short_name: str) -> Option | None:
        for option in options:
            if option.short_name == short_name:
                return option
        return None

    def is_valid_option(arg: str) -> bool:
        """Check if an argument is a valid option (not just any string starting with -)."""
        if arg.startswith("--"):
            return find_option_by_kebab_name(arg[2:]) is not None
        elif arg.startswith("-") and len(arg) > 1:
            return find_option_by_short_name(arg[1:]) is not None
        return False

    def process_option_value(option: Option, i: int) -> tuple[Any, bool]:
        """Process the value for a given option.

        Returns:
            Tuple of (value, should_skip_next)
        """
        if option.is_flag:
            return True, False

        # Check if there's a next argument
        if i + 1 >= len(arguments):
            return option.default if option.default is not None else None, False

        next_arg = arguments[i + 1]

        # Accept the next argument as value if:
        # 1. It doesn't start with "-", OR
        # 2. It starts with "-" but is NOT a valid option
        if not next_arg.startswith("-") or not is_valid_option(next_arg):
            try:
                value = cli_argument_convert_value(next_arg, option.type)
                return value, True
            except Exception as e:
                raise CommandArgumentConversionException(
                    argument_name=option.name,
                    value=next_arg,
                    target_type=option.type,
                    cause=e,
                )
        else:
            # Next arg is a valid option, use default
            return option.default if option.default is not None else None, False

    result: dict[str, Any] = {}
    skip_next = False

    for i, arg in enumerate(arguments):
        # Skip this iteration if we've already processed this argument as a value
        if skip_next:
            skip_next = False
            continue

        option = None

        # Check if the argument is an option (starts with - or --)
        if arg.startswith("--"):
            # Long option name (e.g., --version)
            option_name = arg[2:]
            option = find_option_by_kebab_name(option_name)
        elif arg.startswith("-") and len(arg) > 1:
            # Short option name (e.g., -v)
            short_name = arg[1:]
            option = find_option_by_short_name(short_name)

        if option:
            # Process the option value
            value, skip_next = process_option_value(option, i)

            # Handle multiple values
            if option.multiple:
                if option.name not in result:
                    result[option.name] = []
                result[option.name].append(value)
            else:
                result[option.name] = value
        elif arg.startswith("-"):
            # Unknown option
            if strict:
                raise CommandUnexpectedArgumentException(
                    argument=arg,
                    allowed_arguments=allowed_option_names or [],
                )
            # In non-strict mode, skip unknown options

    return result
