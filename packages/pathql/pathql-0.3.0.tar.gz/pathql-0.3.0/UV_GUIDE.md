# TPath Development with uv

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management and building.

## Quick Start with uv

### Install uv
```bash
# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Development Setup
```bash
# Create virtual environment and install dependencies
uv sync --dev

# Activate the environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install in development mode
uv pip install -e .
```

### Building the Package
```bash
# Build wheel and source distribution
uv build

# Build only wheel
uv build --wheel

# Build only source distribution  
uv build --sdist
```

### Running Tests
```bash
# Install test dependencies
uv sync --group test

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=tpath --cov-report=html
```

### Code Quality
```bash
# Install lint dependencies
uv sync --group lint

# Format code with ruff
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/tpath
```

### Publishing
```bash
# Build and upload to PyPI
uv build
uv publish

# Or upload to Test PyPI
uv publish --repository testpypi
```

## Project Structure

The project uses:
- **hatchling** as the build backend (fast and modern)
- **ruff** for formatting and linting (replaces black, isort, flake8)
- **pytest** for testing
- **mypy** for type checking

## uv.lock

The `uv.lock` file (when generated) ensures reproducible builds across environments. This file should be committed to version control.

## Development Workflow

1. Make changes to code
2. Format: `uv run ruff format .`
3. Lint: `uv run ruff check .`
4. Test: `uv run pytest`
5. Build: `uv build`
6. Commit and push

## Benefits of uv

- **Fast**: 10-100x faster than pip
- **Reliable**: Deterministic dependency resolution
- **Modern**: Built for modern Python packaging standards
- **Simple**: Single tool for dependency management, building, and publishing