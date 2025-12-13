# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""Test the ldr.env.google module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ldr.environment import google

if TYPE_CHECKING:
    import pytest


def test_google_cloud_run_job_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check Cloud Run Job container contract env vars are loaded correctly."""
    envvars = {
        "CLOUD_RUN_JOB": "test-job",
        "CLOUD_RUN_EXECUTION": "test-job-abcdef",
        "CLOUD_RUN_TASK_INDEX": "0",
        "CLOUD_RUN_TASK_ATTEMPT": "0",
        "CLOUD_RUN_TASK_COUNT": "1",
    }
    for k, v in envvars.items():
        monkeypatch.setenv(k, v)

    container_vars = google.CloudRunJob()
    assert container_vars.job == "test-job"
    assert container_vars.execution == "test-job-abcdef"
    assert container_vars.task_index == 0
    assert container_vars.task_attempt == 0
    assert container_vars.task_count == 1


def test_google_cloud_run_job_from_local_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure None is set for all vars when running locally."""
    envvars = {
        "CLOUD_RUN_JOB",
        "CLOUD_RUN_EXECUTION",
        "CLOUD_RUN_TASK_INDEX",
        "CLOUD_RUN_TASK_ATTEMPT",
        "CLOUD_RUN_TASK_COUNT",
    }
    for k in envvars:
        monkeypatch.delenv(k, raising=False)

    container_vars = google.CloudRunJob()
    assert container_vars.job is None
    assert container_vars.execution is None
    assert container_vars.task_index is None
    assert container_vars.task_attempt is None
    assert container_vars.task_count is None


def test_google_cloud_run_service_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check Cloud Run Service container contract env vars are loaded correctly."""
    port = 8080
    envvars = {
        "PORT": str(port),
        "K_SERVICE": "test-service",
        "K_REVISION": "test-service-abcdef",
        "K_CONFIGURATION": "test",
    }
    for k, v in envvars.items():
        monkeypatch.setenv(k, v)

    container_vars = google.CloudRunService()
    assert container_vars.port == port
    assert container_vars.k_service == "test-service"
    assert container_vars.k_revision == "test-service-abcdef"
    assert container_vars.k_configuration == "test"


def test_google_cloud_run_service_from_local_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensure None is set for all vars when running locally."""
    envvars = {
        "PORT",
        "K_SERVICE",
        "K_REVISION",
        "K_CONFIGURATION",
    }
    for k in envvars:
        monkeypatch.delenv(k, raising=False)

    container_vars = google.CloudRunService()
    assert container_vars.port is None
    assert container_vars.k_service is None
    assert container_vars.k_revision is None
    assert container_vars.k_configuration is None


def test_google_cloud_run_worker_pool_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check Cloud Run Service container contract env vars are loaded correctly."""
    envvars = {
        "CLOUD_RUN_WORKER_POOL": "test-worker-pool",
        "CLOUD_RUN_WORKER_POOL_REVISION": "test-worker-pool-abcdef",
    }
    for k, v in envvars.items():
        monkeypatch.setenv(k, v)

    container_vars = google.CloudRunWorkerPool()
    assert container_vars.worker_pool == "test-worker-pool"
    assert container_vars.worker_pool_revision == "test-worker-pool-abcdef"


def test_google_cloud_run_worker_pool_from_local_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensure None is set for all vars when running locally."""
    envvars = {
        "CLOUD_RUN_WORKER_POOL",
        "CLOUD_RUN_WORKER_POOL_REVISION",
    }
    for k in envvars:
        monkeypatch.delenv(k, raising=False)

    container_vars = google.CloudRunWorkerPool()
    assert container_vars.worker_pool is None
    assert container_vars.worker_pool_revision is None
