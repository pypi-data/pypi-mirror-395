# Development Guide

This guide covers how to set up and work on the `social-links` project locally.

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - A fast Python package installer and resolver

## Installation

### Installing uv

If you don't have `uv` installed, you can install it using [UV Getting Started](https://docs.astral.sh/uv/getting-started/installation/)

### Setting Up the Development Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/ysskrishna/social-links.git
   cd social-links
   ```

2. Install the project and development dependencies using `uv`:

   ```bash
   uv sync --dev
   ```

   This will:

   - Create a virtual environment (if it doesn't exist)
   - Install the project in editable mode
   - Install all development dependencies (including `pytest`)

## Local Testing

### Running Tests

Run all tests using pytest:

```bash
uv run pytest
```

### Running Specific Test Files

```bash
uv run pytest tests/test_core.py
uv run pytest tests/test_platforms.py
uv run pytest tests/test_platform_management.py
uv run pytest tests/test_edge_cases.py
```

### Building the Package

To build the package locally:

```bash
uv build
```

This will create distribution files in the `dist/` directory:

- `social-links-<version>-py3-none-any.whl` (wheel)
- `social-links-<version>.tar.gz` (source distribution)

### Installing the Local Package

To test the package installation locally:

```bash
# Install from the built wheel
uv pip install dist/social-links-*.whl

# Or install in editable mode for development
uv pip install -e .
```

## Project Structure

```
social-links/
├── sociallinks/          # Main package code
│   ├── __init__.py       # Package initialization
│   ├── core.py           # Core SocialLinks class
│   ├── exceptions.py     # Custom exceptions
│   └── platforms.py      # Predefined platform configurations
├── tests/                # Test suite
│   ├── __init__.py
│   ├── test_core.py      # Core functionality tests
│   ├── test_platforms.py # Platform-specific tests
│   ├── test_platform_management.py # Platform CRUD tests
│   └── test_edge_cases.py # Edge case tests
├── pyproject.toml        # Project configuration and dependencies
├── uv.lock              # Locked dependency versions
└── README.md            # User-facing documentation
```

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Packaging Guide](https://packaging.python.org/)
