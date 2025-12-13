# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""Test the ldr.env.config module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ldr.environment import config as env_config

if TYPE_CHECKING:
    import pytest


def test_use_pretty_exceptions_unset_local(monkeypatch: pytest.MonkeyPatch) -> None:
    """Return True when the PRETTY_EXCEPTIONS var is unset and running locally."""
    monkeypatch.delenv("PRETTY_EXCEPTIONS", raising=False)
    assert env_config.use_pretty_exceptions() is True


def test_use_pretty_exceptions_unset_cloud_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """Return False when the PRETTY_EXCEPTIONS var is unset and running in cloud run."""
    monkeypatch.delenv("PRETTY_EXCEPTIONS", raising=False)
    monkeypatch.setenv("CLOUD_RUN_JOB", "my-job")
    assert env_config.use_pretty_exceptions() is False


def test_use_pretty_exceptions_in_cloud_run_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Return False when a Cloud Run container contract var is set and using auto."""
    monkeypatch.setenv("PRETTY_EXCEPTIONS", "auto")
    monkeypatch.setenv("CLOUD_RUN_JOB", "abc")
    assert env_config.use_pretty_exceptions() is False


def test_use_pretty_exceptions_in_local_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Return True when no Cloud Run container contract vars are set."""
    cloud_vars = {"CLOUD_RUN_JOB", "CLOUD_RUN_WORKER_POOL", "K_SERVICE"}

    for var in cloud_vars:
        monkeypatch.delenv(var, raising=False)

    assert env_config.use_pretty_exceptions() is True


def test_use_pretty_exceptions(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure True is returned when PRETTY_EXCEPTIONS is set to a yes-like value."""
    yes_values = {"y", "yes", "true", "enable"}

    for value in yes_values:
        monkeypatch.setenv("PRETTY_EXCEPTIONS", value)
        assert env_config.use_pretty_exceptions() is True
