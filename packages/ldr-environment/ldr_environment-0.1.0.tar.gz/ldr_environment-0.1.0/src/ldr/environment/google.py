# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""
Typed mappings for Cloud Run container runtime contracts.

See https://docs.cloud.google.com/run/docs/container-contract.
"""

from __future__ import annotations

import pydantic
import pydantic_settings


class CloudRunJob(pydantic_settings.BaseSettings, env_prefix="CLOUD_RUN_"):
    """A Google Cloud Run V2 Job's runtime contract env vars."""

    job: str | None = pydantic.Field(
        default=None,
        description="The name of the Cloud Run job being run.",
    )
    execution: str | None = pydantic.Field(
        default=None,
        description="The name of the Cloud Run execution being run.",
    )
    task_index: int | None = pydantic.Field(
        default=None,
        description="The index of this task. Starts at 0 for the first task and "
        "increments by 1 for every successive task, up to the maximum number of "
        "tasks minus 1. If you set --parallelism to greater than 1, tasks might "
        "not follow the index order. For example, it would be possible for task "
        "2 to start before task 1.",
    )
    task_attempt: int | None = pydantic.Field(
        default=None,
        description="The number of times this task has been retried. Starts at 0 for "
        "the first attempt and increments by 1 for every successive retry, up to the "
        "maximum retries value.",
    )
    task_count: int | None = pydantic.Field(
        default=None,
        description="The number of tasks defined in the --tasks parameter.",
    )


class CloudRunService(pydantic_settings.BaseSettings):
    """A Google Cloud Run V2 Service's runtime contract env vars."""

    port: int | None = pydantic.Field(
        default=None,
        description="The port your HTTP server should listen on.",
    )
    k_service: str | None = pydantic.Field(
        default=None,
        description="The name of the Cloud Run service being run.",
    )
    k_revision: str | None = pydantic.Field(
        default=None,
        description="The name of the Cloud Run revision being run.",
    )
    k_configuration: str | None = pydantic.Field(
        default=None,
        description="The name of the Cloud Run configuration "
        "that created the revision.",
    )


class CloudRunWorkerPool(pydantic_settings.BaseSettings, env_prefix="CLOUD_RUN_"):
    """A Google Cloud Run V2 Worker Pool's runtime contract env vars."""

    worker_pool: str | None = pydantic.Field(
        default=None,
        description="The name of the running Cloud Run worker pool.",
    )
    worker_pool_revision: str | None = pydantic.Field(
        default=None,
        description="The name of the running Cloud Run worker pool revision.",
    )
