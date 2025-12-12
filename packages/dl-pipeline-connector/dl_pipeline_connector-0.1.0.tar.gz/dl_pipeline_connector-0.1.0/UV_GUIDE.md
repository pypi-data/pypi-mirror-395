# UV Package Manager Guide

Quick reference for using `uv` with this project.

## Quick Start (TL;DR)

```bash
# Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Set up project
uv sync                          # Creates venv + installs all deps

# Add packages
uv add package-name              # Production dependency
uv add --dev package-name        # Dev dependency

# Remove packages
uv remove package-name           # Auto-updates pyproject.toml

# Run commands (no activation needed!)
uv run python script.py
uv run pytest
```

**Key Point:** Use `uv add` instead of `uv pip install` - it automatically updates `pyproject.toml`!

## Why UV?

- **Fast**: 10-100x faster than pip
- **No manual version management**: Automatically updates `pyproject.toml`
- **Better dependency resolution**: Resolves conflicts more reliably
- **Modern**: Built with Rust for performance

## Common Commands

### Initial Setup

```bash
# Install uv (first time only)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Sync project (creates venv and installs all dependencies)
uv sync

# This automatically:
# - Creates .venv if it doesn't exist
# - Installs all dependencies from pyproject.toml
# - Installs the project in editable mode
```

### Adding Dependencies (Recommended: Use `uv add`)

```bash
# Add a package (production dependency)
# Automatically installs AND updates pyproject.toml
uv add dagster

# Add a package (dev dependency)
uv add --dev pytest

# Add specific version
uv add pandas==2.0.0

# Add with extras
uv add "dlt[bigquery]"

# Add multiple packages at once
uv add dagster dagster-webserver dagster-slack
```

### Alternative: Using `uv pip` (Legacy approach)

```bash
# Install packages (doesn't auto-update pyproject.toml)
uv pip install dagster

# You'll need to manually add to pyproject.toml:
# [project.dependencies]
# dagster = ">=1.5.0"
```

### Managing Dependencies

```bash
# Sync all dependencies from pyproject.toml
uv sync

# Sync including dev dependencies
uv sync --all-extras

# Remove a package
uv remove <package-name>

# Update all packages to latest compatible versions
uv lock --upgrade

# Show installed packages
uv pip list

# Show dependency tree
uv pip tree
```

### Common Workflows

#### Starting Fresh

```bash
# Clone the repo
cd dl-pipeline-connector

# Sync everything (creates venv + installs deps)
uv sync

# Copy environment template
cp .env.example .env

# Edit .env with your settings
```

#### Adding a New Package

```bash
# Add production dependency (auto-updates pyproject.toml)
uv add requests

# Add dev dependency
uv add --dev pytest-asyncio

# That's it! No manual editing needed.
```

#### Removing a Package

```bash
# Remove a package (auto-updates pyproject.toml)
uv remove requests
```

#### Running Tests

```bash
# Make sure dev dependencies are installed
uv sync

# Run tests
pytest
```

## UV vs PIP Comparison

| Task | pip + requirements.txt | uv (modern) |
|------|----------------------|-------------|
| Add package | `pip install package` + manual edit | `uv add package` |
| Remove package | `pip uninstall package` + manual edit | `uv remove package` |
| Install all deps | `pip install -r requirements.txt` | `uv sync` |
| Create venv | `python -m venv .venv` | `uv venv` (or auto with `uv sync`) |
| Install editable | `pip install -e .` | Auto with `uv sync` |
| Speed | Slow | 10-100x faster |
| Lock file | requirements.txt (manual) | uv.lock (automatic) |

## Best Practices

1. **Use `uv add`** instead of `uv pip install` - it auto-updates `pyproject.toml`
2. **Use `uv sync`** for initial setup - creates venv and installs everything
3. **No requirements.txt needed** - `pyproject.toml` is the modern standard
4. **Dev dependencies**: Use `uv add --dev` for test/lint tools
5. **Lock versions**: `uv` automatically creates `uv.lock` for reproducible builds

## Troubleshooting

### "uv: command not found"

Make sure uv is installed and in your PATH:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then restart your terminal
```

### Virtual Environment Not Activating

```bash
# Make sure you created it first
uv venv

# Then activate
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Package Import Errors

```bash
# Make sure everything is synced
uv sync

# Check if venv is activated (optional with uv run)
# You can run commands without activating:
uv run python script.py
uv run pytest
```

## Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [Python Packaging Guide](https://packaging.python.org/)
