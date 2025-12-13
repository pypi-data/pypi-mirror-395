# Contributing to django-rewind

Thank you for your interest in contributing to django-rewind! This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. It's recommended for development.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/HartBrook/django-rewind.git
cd django-rewind

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in editable mode with dev dependencies
uv pip install -e ".[dev]"

# Or use uv sync (creates venv and installs automatically)
uv sync --extra dev
```

### Using pip (Alternative)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Running Tests

Tests are located in the `django_rewind/tests/` directory and use a minimal Django settings configuration for fast execution.

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=django_rewind --cov-report=html

# Using uv
uv run pytest

# Run specific test file
pytest django_rewind/tests/test_recorder.py

# Run specific test
pytest django_rewind/tests/test_recorder.py::test_specific_function
```

**Note:** Tests use `django_rewind.tests.settings` for Django configuration, which provides a minimal setup for unit testing without requiring the full test project structure.

## Code Quality

We use several tools to maintain code quality:

- **black**: Code formatting
- **flake8**: Linting
- **isort**: Import sorting
- **mypy**: Type checking
- **pytest**: Testing
- **pre-commit**: Automated checks before commits

### Pre-commit Hooks (Recommended)

We use pre-commit hooks to automatically check code quality before commits. This ensures consistent code style and catches issues early.

```bash
# Install pre-commit hooks (one-time setup)
uv run pre-commit install

# Run hooks on all files
uv run pre-commit run --all-files

# Run hooks on staged files (automatic on commit)
uv run pre-commit run
```

The hooks will automatically:
- Format code with black
- Sort imports with isort
- Check linting with flake8
- Verify file formatting (trailing whitespace, end of files, etc.)
- Check for merge conflicts and other issues

### Manual Checks

You can also run checks manually:

```bash
# Format code
uv run black .

# Sort imports
uv run isort .

# Check linting
uv run flake8 django_rewind django_rewind/tests

# Type checking
uv run mypy django_rewind

# Run all checks
uv run black .
uv run isort .
uv run flake8 django_rewind django_rewind/tests
uv run mypy django_rewind
```

## Building the Package

```bash
# Build distributions
python -m build

# Or using uv
uv build

# Check the built package
twine check dist/*
```

## Testing Across Multiple Environments

[tox](https://tox.wiki/) is included in the dev dependencies for testing across multiple Python and Django versions. Note that a tox configuration file is not currently included in the repository, but you can set one up if you want to test across multiple environments locally.

```bash
# Install tox (included in dev dependencies)
uv pip install tox

# If you set up a tox.ini configuration file:
# Run tests across all configured environments
tox

# Run tests for a specific environment
tox -e py312-django51

# List all available environments
tox list
```

## Submitting Changes

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** following the code style guidelines below
4. **Ensure tests pass**:
   ```bash
   pytest
   ```
5. **Ensure code quality checks pass**:
   ```bash
   uv run pre-commit run --all-files
   ```
   Or run checks manually as described in the Code Quality section
6. **Commit your changes** with a clear, descriptive message:
   ```bash
   git commit -m 'Add amazing feature'
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
8. **Open a Pull Request** on GitHub with a clear description of your changes

### Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Include tests for new functionality
- Update documentation if needed
- Ensure all CI checks pass
- Reference any related issues

## Code Style

- **Follow PEP 8** - Python style guide
- **Use black for formatting** - Line length: 88 characters
- **Sort imports with isort** - Configured to work with black
- **Type hints** - Encouraged but not required for all code
- **Docstrings** - Required for public functions and classes
- **Naming conventions** - Follow Django and Python conventions

## Testing Guidelines

- **Write tests for new features** - Aim for comprehensive coverage
- **Ensure all tests pass** - Run `pytest` before submitting
- **Test edge cases** - Consider error conditions and boundary cases
- **Use descriptive test names** - Test names should clearly describe what they test
- **Keep tests isolated** - Each test should be independent and not rely on others
- **Use fixtures** - Leverage pytest fixtures for common setup

## Project Structure

```
django-rewind/
├── django_rewind/          # Main package
│   ├── management/         # Django management commands
│   ├── migrations/         # Package migrations
│   ├── tests/              # Test suite
│   └── ...                 # Core modules
├── test_project/           # Test Django project (for integration testing)
├── pytest.ini              # Pytest configuration
├── pyproject.toml          # Project metadata and tool configs
└── ...
```

## Additional Resources

- **Test Project**: The `test_project/` directory contains a full Django project for integration testing. See `test_project/README.md` for details.
  - To reset the database and run migrations fresh: `cd test_project && make reset && make up`
- **Pre-commit Hooks**: Configured in `.pre-commit-config.yaml` to automatically check code quality
- **Type Checking**: Uses mypy with django-stubs for Django type hints

## Questions?

Feel free to open an [issue](https://github.com/HartBrook/django-rewind/issues) for any questions or concerns. We're happy to help!
