# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""Test the ldr.env.var module."""

from __future__ import annotations

import pytest
from ldr.environment import errors, var

ENV_VAR = "_LDR_ENV_TEST_VAR"


def test_var_get(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure a variable is loaded correctly."""
    monkeypatch.setenv(ENV_VAR, "test")
    assert var.get(ENV_VAR) == "test"


def test_var_get_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure None is returned when no var is set."""
    monkeypatch.delenv(ENV_VAR, raising=False)
    assert var.get(ENV_VAR) is None


def test_var_require(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure a requried variable is loaded correctly."""
    monkeypatch.setenv(ENV_VAR, "test")
    assert var.require(ENV_VAR) == "test"


def test_var_require_unset_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure a requried variable is loaded correctly."""
    monkeypatch.delenv(ENV_VAR, raising=False)
    with pytest.raises(errors.MissingVarError):
        assert var.require(ENV_VAR)
