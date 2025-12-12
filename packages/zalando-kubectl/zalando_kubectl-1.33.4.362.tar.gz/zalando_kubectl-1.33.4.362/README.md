# Zalando Kubectl

## Description

[![PyPI Downloads](https://img.shields.io/pypi/dw/zalando-kubectl.svg)](https://pypi.python.org/pypi/zalando-kubectl/)

[![Latest PyPI version](https://img.shields.io/pypi/v/zalando-kubectl.svg)](https://pypi.python.org/pypi/zalando-kubectl/)
[![License](https://img.shields.io/pypi/l/zalando-kubectl.svg)](https://pypi.python.org/pypi/zalando-kubectl/)

Kubernetes CLI (kubectl) wrapper in Python with OAuth token authentication.

This wrapper script `zkubectl` serves as a drop-in replacement for the
`kubectl` binary:

-   it downloads the current `kubectl` binary from Google
-   it generates a new `~/.kube/config` with an OAuth Bearer token
    acquired via [zign](https://pypi.python.org/pypi/stups-zign).
-   it passes through commands to the `kubectl` binary

## User Facing documentation

- https://cloud.docs.zalando.net/reference/zkubectl/
- https://cloud.docs.zalando.net/howtos/install-tools/

## Contribute

### Setup project

- It's recommended to use [uv](https://github.com/astral-sh/uv) for the project.

Go to the project dir and install dependencies with uv

``` bash
$ cd <project-path>
$ uv sync
```

- [Optional] install pre-commit hooks

```bash
$ pre-commit install
```

- [Optional] The project uses [ruff](https://docs.astral.sh/ruff/) for
code formatting, configure your editor to use it.


### Unit Tests

Run unit tests with Docker:

``` bash
docker build --build-arg PYTHON_VERSION=3.10 --build-arg PACKAGE_NAME=zalando_kubectl -f Dockerfile.test .
docker build --build-arg PYTHON_VERSION=3.11 --build-arg PACKAGE_NAME=zalando_kubectl -f Dockerfile.test .
docker build --build-arg PYTHON_VERSION=3.12 --build-arg PACKAGE_NAME=zalando_kubectl --build-arg DEBIAN_DISTRO=bullseye -f Dockerfile.test .
docker build --build-arg PYTHON_VERSION=3.13 --build-arg PACKAGE_NAME=zalando_kubectl --build-arg DEBIAN_DISTRO=bullseye -f Dockerfile.test .
```

### Run Locally

via uv

``` bash
$ uv run zkubectl
```

Or first activate the virtualenv

```bash
$ source .venv/bin/activate
$ zkubectl login playground
```

### Use as `kubectl` plugin

The project exposes scripts that use the `kubectl` plugin format

You can see which ones are available in the scripts section of [pyproject.toml](pyproject.toml)

In order for `kubectl` to detect the subcommands provided by the script, they must be in the PATH, so you need first to activate the virtualenv

```bash
$ source .venv/bin/activate
$ kubectl login playground
```
