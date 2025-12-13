# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""Methods to interact with environment variables."""

from __future__ import annotations

import os
from typing import overload

from ldr.environment.errors import MissingVarError


@overload
def get(key: str, /, default: str) -> str:
    ...


@overload
def get(key: str, /, default: str | None = None) -> str | None:
    ...


def get(key: str, /, default: str | None = None) -> str | None:
    """
    Load an environment variable, if it is present.

    Params
    ------
    key: The env var name to load.
    default: The default value to use when not set.

    Returns
    -------
    The value, default, or None if no value is set and no default provided.

    """
    return os.getenv(key, default)


def require(key: str, /, default: str | None = None) -> str:
    """
    Load an environment variable.

    Params
    ------
    key: The env var name to load.
    default: The default value to use when not set.

    Returns
    -------
    The value, or default if unset.

    Raises
    ------
    MissingVarError: If the env var is not set and no default is provided.

    """
    if val := os.getenv(key, default):
        return val

    raise MissingVarError(key)
