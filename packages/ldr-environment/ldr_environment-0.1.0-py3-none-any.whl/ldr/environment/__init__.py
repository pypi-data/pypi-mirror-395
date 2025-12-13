# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""Interact with the runtime environment."""

from __future__ import annotations

__all__ = (
    "MissingVarError",
    "config",
    "errors",
    "get",
    "google",
    "require",
)


from ldr.environment import config, errors, google
from ldr.environment.errors import MissingVarError
from ldr.environment.var import get, require
