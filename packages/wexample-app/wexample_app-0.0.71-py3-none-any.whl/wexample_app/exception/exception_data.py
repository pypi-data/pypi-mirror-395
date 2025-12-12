from __future__ import annotations

from typing import TypedDict


class CommandBuildFailedData(TypedDict):
    """Data structure for CommandBuildFailed exception."""

    command_name: str
    resolver_name: str


class CommandFunctionNameMissingData(TypedDict):
    """Data structure for CommandFunctionNameMissing exception."""

    command_name: str


class CommandFunctionNotFoundData(TypedDict):
    """Data structure for CommandFunctionNotFound exception."""

    function_name: str
    module_path: str


class CommandModuleLoadErrorData(TypedDict):
    """Data structure for CommandModuleLoadError exception."""

    file_path: str


class CommandResolverNotFoundData(TypedDict):
    """Data structure for CommandResolverNotFound exception."""

    command_type: str


class CommandRunnerMissingData(TypedDict):
    """Data structure for CommandRunnerMissing exception."""

    command_name: str


class CommandRunnerNotFoundData(TypedDict):
    """Data structure for CommandRunnerNotFound exception."""

    command_name: str


class CommandTypeNotFoundData(TypedDict):
    """Data structure for CommandTypeNotFound exception."""

    command_name: str


class ResponseInvalidContentTypeData(TypedDict):
    """Data structure for ResponseInvalidContentType exception."""

    allowed_types: list[str]
    content_type: str
    content_value: str
