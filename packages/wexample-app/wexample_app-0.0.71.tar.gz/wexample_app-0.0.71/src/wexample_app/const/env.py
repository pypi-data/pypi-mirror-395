from __future__ import annotations

# filestate: python-constant-sort
ENV_NAME_DEV: str = "dev"
ENV_NAME_LOCAL: str = "local"
ENV_NAME_PROD: str = "prod"
ENV_NAME_TEST: str = "test"

ENV_COLORS = {
    ENV_NAME_LOCAL: "green",
    ENV_NAME_DEV: "yellow",
    ENV_NAME_TEST: "magenta",
    ENV_NAME_PROD: "red",
}
