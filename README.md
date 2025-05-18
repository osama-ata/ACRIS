# ACRIS

Automated Construction Risk Identifcation System

## Monolithic Modular Structure

The ACRIS system is organized as a monolithic modular Python package under the `acris/` directory. Main modules:

- `dp/`: Data Processing
- `upq/`: User & Project Query
- `qo/`: Question Organization
- `ro/`: Risk Output
- `ra/`: Risk Analysis
- `common/`: Shared utilities, config, and data models

## Development Environment

```bash
source .venv/bin/activate

uv pip install
```

Linting and formatting:

```bash
# ruff check is the primary entrypoint to the Ruff linter
ruff check                  # Lint files in the current directory.
ruff check --fix            # Lint files in the current directory and fix any fixable errors.
ruff check --watch          # Lint files in the current directory and re-lint on change.
ruff check path/to/code/    # Lint files in `path/to/code`.

# ruff format is the primary entrypoint to the formatter
ruff format                   # Format all files in the current directory.
ruff format path/to/code/     # Format all files in `path/to/code` (and any subdirectories).
ruff format path/to/file.py   # Format a single file.

```

To test the build:

```bash
source .venv/bin/activate && uv pip install dist/acris-0.1.0-py3-none-any.whl && python -c 'import acris; import acris.main'
```

The main entry point is `acris/main.py`.

See `acris/README.md` for module details.
