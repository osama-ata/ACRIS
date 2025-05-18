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

## Vector Similarity Search with DuckDB

ACRIS supports semantic search over risk cases using DuckDB with the VSS (Vector Similarity Search) extension and Sentence Transformers for embedding generation.

### Setup

1. **Install dependencies** (already in `pyproject.toml`):
   - `duckdb`
   - `sentence-transformers`
   - `numpy`

2. **Environment**
   - Activate your virtual environment:

     ```bash
     source .venv/bin/activate
     ```

   - Ensure dependencies are installed:

     ```bash
     uv pip install
     ```

3. **Configuration**
   - By default, the DuckDB database is stored as `acris.duckdb` in the project root.
   - To override the path, set the `ACRIS_DUCKDB_PATH` environment variable.

### Usage

The main API is provided in `acris/vector_db.py`:

- `add_risk_case(description: str) -> int`
  - Adds a risk case and stores its embedding.
- `find_similar_cases(query: str, top_k: int = 5) -> List[Tuple[int, str, float]]`
  - Returns the most similar risk cases to the query string.
- `rebuild_vss_index() -> None`
  - Rebuilds the VSS index (call after bulk updates).
- `get_all_risk_cases() -> List[Tuple[int, str]]`
  - Returns all risk cases (id, description).

#### Example

```python
from acris import vector_db

# Add a risk case risk_id = vector_db.add_risk_case("Risk of fall from height")

# Query similar cases
results = vector_db.find_similar_cases("fall prevention", top_k=3)
for rid, desc, score in results:
    print(f"ID: {rid}, Desc: {desc}, Score: {score:.4f}")
```

#### Notes

- The embedding model used is `all-MiniLM-L6-v2` (384-dim).
- The VSS extension is loaded automatically.
- All code follows PEP 8, uses type hints, and is documented with docstrings.
- For production, ensure the database file is secured and sensitive data is handled appropriately.
