# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""Library errors."""

from __future__ import annotations


class MissingVarError(OSError):
    """Raise when an env var is expected to be set, but is not present."""

    def __init__(self, varname: str) -> None:
        """Raise when an env var is expected to be set but is not present."""
        super().__init__(f"Environment variable '{varname}' is not set")
