# Environment utilities

This library is for the most part a wrapper on the `os` stdlib module.

## `ldr.environment.get`

Loads an environment variable, a default, or None if no default is provided and the var is unset.

## `ldr.environment.require`

Loads an environment, a default, or raises a `ldr.environment.MissingVarError` if no default is provided and the var is unset.

## `ldr.environment.google`

This module contains pydantic models that will load [Google Cloud Run container contract variables](https://docs.cloud.google.com/run/docs/container-contract) into a model.

```python
from ldr.environment.google import CloudRunJob

# When in a Cloud Run Job environment.
job_vars = CloudRunJob()
assert job_vars.job == "my-job-name"
assert job_vars.task_index == 1

# Or locally

job_vars = CloudRunJob()
assert job_vars.job is None
```

## `ldr.environment.config`

Load configuration from the environment.

### `ldr.environment.config.use_pretty_exceptions`

Check whether to use pretty exceptions.

Reads from the `PRETTY_EXCEPTIONS` env var. Valid values are:

- `y` | `yes` | `enable` | `true`: Enable pretty exceptions
- `auto`: Check for Cloud Run container env vars and disable if any are present.
- Any other value: Disable pretty exceptions

Defaults to `auto` if unset.
