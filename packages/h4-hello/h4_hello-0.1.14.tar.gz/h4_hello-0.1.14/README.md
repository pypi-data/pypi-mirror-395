# h4-hello

[![PyPI - Version](https://img.shields.io/pypi/v/h4-hello.svg)](https://pypi.org/project/h4-hello)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/h4-hello.svg)
![Last Commit](https://img.shields.io/github/last-commit/heiwa4126/h4-hello)
[![PyPI - License](https://img.shields.io/pypi/l/h4-hello.svg)](https://opensource.org/licenses/MIT)

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
  - [CLI](#cli)
  - [As a Library](#as-a-library)
- [Development](#development)
  - [Setup](#setup)
  - [Available Tasks](#available-tasks)
  - [Publishing](#publishing)
- [License](#license)
- [Note](#note)

A practice project for publishing Python packages to PyPI with PEP740 digital signatures using **uv** as the build backend and package manager. Contains only a simple `hello()` function that returns "Hello!".

## Installation

```console
pip install h4-hello
```

## Usage

### CLI

```console
$ h4-hello
Hello!

$ h4-hello --version
h4-hello v0.1.12b2
```

### As a Library

```python
from h4_hello import hello

print(hello())  # -> Hello!
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for package management and [poethepoet](https://poethepoet.natn.io/) for task running.

### Setup

```console
# Install dependencies
uv sync

# Run tests
poe test

# Lint and type check
poe lint

# Format code
poe format

# Build package
poe build
```

### Available Tasks

Run `poe` to see all available tasks defined in `poe_tasks.toml`:

- `poe test` - Run pytest tests
- `poe check` - Run ruff linting
- `poe mypy` - Run type checking
- `poe format` - Auto-format code
- `poe build` - Full build with checks and smoke tests
- `poe smoke-test` - Test built packages in isolation
- `poe lint` - Run all linters (ruff, mypy, pep440check, pyproject validation)

### Publishing

This project uses GitHub Actions with Trusted Publishing:

- **TestPyPI**: Tag with `test-*` (e.g., `test-0.1.11`)
- **PyPI**: Tag with `v*` semver (e.g., `v0.1.11`)

Both deployments use OIDC authentication with Sigstore attestations (PEP740).

## License

`h4-hello` is distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license.

## Note

詳細な日本語ドキュメントは [NOTE-ja.md](https://github.com/heiwa4126/h4-hello/blob/main/NOTE-ja.md) を参照してください。
