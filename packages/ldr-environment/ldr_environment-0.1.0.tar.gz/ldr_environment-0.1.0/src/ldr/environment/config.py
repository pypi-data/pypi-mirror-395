# Copyright 2025 Louder Digital Pty Ltd.
# All Rights Reserved.
"""Environment based configuration used across louder projects."""

from __future__ import annotations

from ldr import environment


def use_pretty_exceptions() -> bool:
    """
    Determine if pretty exceptions should be used based on the environment.

    Listens to the `PRETTY_EXCEPTIONS` environment variable:

    - When set to `y`, `yes`, `enable`, or `true`, this method will return True.

    - If unset, or set to `auto` and running locally, it will return True.

    - If unset, or set to `auto` and running in a Google Cloud Run environment,
    it will return False.

    - If set to anything other than `y`, `yes`, `enable`, `true`, or `auto`,
    it will return False.

    Returns
    -------
    Whether pretty exceptions should be used.

    """
    cloud_vars = {
        "CLOUD_RUN_JOB",
        "CLOUD_RUN_WORKER_POOL",
        "K_SERVICE",
    }

    mode = environment.get("PRETTY_EXCEPTIONS", "auto").lower()

    if mode == "auto":
        is_cloud_run = any(environment.get(v) for v in cloud_vars)
        return not is_cloud_run

    return mode in {"y", "yes", "enable", "true"}
