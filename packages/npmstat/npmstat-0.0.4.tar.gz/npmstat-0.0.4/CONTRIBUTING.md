# Contributing

- [Setup](#Setup)
- [Build](#Build)
- [UV](#UV)

This is more of a development guide.

## Setup

Clone the project and change into the directory.

```shell
# Install Project
uv sync
# Activate (Windows)
.\.venv\Scripts\activate
# Activate (Unix)
source .venv/venv/activate
# Deactivate
deactivate
```

Note: uv `sync` installs all dependencies and the project as an editable.

- Environments: https://docs.astral.sh/uv/pip/environments/

## Build

This project is using Hatchling and GitHub actions.

```shell
uv run hatch build
```

The version is set from the release tag in the [release.yaml](.github/workflows/release.yaml).

- Hatch: https://hatch.pypa.io/latest/

## UV

### Manage UV

```shell
# Add Package
uv add requests
# Add Dev Package
uv add --dev black
# Remove Package
uv remove requests
# Update uv.lock (with project)
uv lock
# Upgrade uv.lock (pip upgrade)
uv lock --upgrade
```

- Lock and sync: https://docs.astral.sh/uv/concepts/projects/sync/
- Managing dependencies: https://docs.astral.sh/uv/guides/projects/#managing-dependencies

### Using UV

```shell
# Run Something
uv run black .
# Run Without Installing
uvx ruff check
```

- Tools: https://docs.astral.sh/uv/guides/tools/
