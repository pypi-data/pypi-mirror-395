# Development Guide

This project uses `uv` as the Python package manager and build tool. Here are the key development commands:

## Setup

```bash
# Install dependencies and create virtual environment
$ uv sync
```

## Testing

```bash
# Run all tests
$ uv run pytest tests
$ make test

# Run single test
$ uv run pytest tests/test_<module>.py::<test_function>

# Run specific test module
$ uv run pytest tests/test_<module>.py

# Run tests with coverage
$ uv run pytest --cov=src/ipsdk --cov-report=term --cov-report=html tests/
$ make coverage

# Run tests with coverage check (enforces 95% minimum coverage)
$ make coverage-check
```

### Multi-Version Testing with Tox

The SDK supports Python 3.10, 3.11, 3.12, and 3.13. Use tox to test across all versions:

```bash
# Run tests across all Python versions
$ uv run tox
$ make tox

# Run tests in parallel (faster)
$ uv run tox -p auto

# Run tests on specific Python version
$ uv run tox -e py310    # Python 3.10
$ make tox-py310

$ uv run tox -e py311    # Python 3.11
$ make tox-py311

$ uv run tox -e py312    # Python 3.12
$ make tox-py312

$ uv run tox -e py313    # Python 3.13
$ make tox-py313

# Run quick tests (no lint/security)
$ uv run tox -e quick

# Run coverage report on Python 3.13
$ uv run tox -e coverage
```

## Code Quality

```bash
# Lint code
$ uv run ruff check src/ipsdk
$ uv run ruff check tests
$ make lint

# Format code (automatic code formatting)
$ uv run ruff format src/ipsdk tests
$ make format

# Auto-fix linting issues (where possible)
$ uv run ruff check --fix src/ipsdk tests
$ make ruff-fix

# Type checking
$ uv run mypy src/ipsdk

# Security analysis (scans for vulnerabilities)
$ uv run bandit -r src/ipsdk --configfile pyproject.toml
$ make security
```

### Pre-commit Hooks

The project uses pre-commit hooks for automatic code quality checks:

```bash
# Install git hooks
$ uv run pre-commit install

# Run on all files
$ uv run pre-commit run --all-files
```

Pre-commit hooks include:
- Basic file checks (trailing whitespace, EOF fixer, YAML/TOML validation)
- Ruff linting and formatting
- MyPy type checking

## Build and Maintenance

```bash
# Clean build artifacts
$ make clean

# Run premerge checks (clean, lint, security, and test with coverage check)
$ make premerge

# Generate changelog (uses git-cliff with conventional commits)
$ make changelog              # Generate full CHANGELOG.md
$ make changelog-unreleased   # Show unreleased changes only
```

### Version Management

The project uses **dynamic versioning** from git tags:
- Build system: **Hatchling** with **uv-dynamic-versioning**
- Version format: **PEP440** style
- Tags automatically generate versions
- Fallback version: `0.0.0` when no tags exist

## Development Workflow

1. **Setup**: Run `uv sync` to install dependencies and create a virtual environment
2. **Install hooks**: Run `uv run pre-commit install` to set up git hooks (optional but recommended)
3. **Development**: Make your changes to the codebase
4. **Format**: Run `make format` to auto-format code
5. **Testing**: Run tests with `make test` or `uv run pytest tests`
6. **Quality Checks**: Run `make lint` and `make security` to check code quality
7. **Coverage**: Ensure test coverage meets 95% threshold with `make coverage-check`
8. **Pre-merge**: Run `make premerge` before submitting changes (runs all checks)
9. **Multi-version**: Optionally test across Python versions with `make tox`

## Additional Tools

The project uses the following development tools:

- **uv**: Package manager and virtual environment management
- **pytest**: Testing framework with async support (`pytest-asyncio`)
- **pytest-cov**: Code coverage reporting plugin
- **ruff**: Fast Python linter and formatter (30+ rule sets)
- **mypy**: Static type checker
- **bandit**: Security vulnerability scanner
- **tox**: Multi-version Python testing (3.10, 3.11, 3.12, 3.13)
- **tox-uv**: Tox integration with uv for fast environments
- **pre-commit**: Git hooks for automated quality checks
- **git-cliff**: Changelog generator using conventional commits
- **q**: Debugging utility

All tools are configured in `pyproject.toml` and can be run through `uv` or the provided Makefile targets.

### Ruff Configuration

The project uses comprehensive Ruff configuration with 30+ rule sets:
- pycodestyle (E, W), Pyflakes (F), pyupgrade (UP)
- flake8-bugbear (B), isort (I), pylint (PL)
- Security checks (S), annotations (ANN), async (ASYNC)
- Line length: 88 characters (Black-compatible)
- Target: Python 3.8+ compatibility
- Per-file ignores configured for different modules

### Coverage Requirements

The SDK enforces strict test coverage:
- **Minimum coverage**: 95%
- Coverage check runs in `make premerge` and CI/CD pipeline
- Pipeline fails if coverage drops below threshold
- Generate HTML reports with `make coverage`

## Python Version Support

The SDK officially supports Python >=3.8 and is tested on:
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

Testing across versions is automated in CI/CD using GitHub Actions matrix testing.

## Logging

By default all logging is turned off for `ipsdk`. To enable logging, use the `ipsdk.logging.set_level` function.

The SDK provides logging level constants that you can use instead of importing the standard library logging module:

```python
>>> import ipsdk

# Using ipsdk logging constants (recommended)
>>> ipsdk.logging.set_level(ipsdk.logging.DEBUG)
```

### Logging Features

The SDK includes a comprehensive logging system:
- Custom FATAL level (90) in addition to standard levels
- Convenience functions: `debug()`, `info()`, `warning()`, `error()`, `critical()`, `fatal()`, `exception()`
- File logging with automatic directory creation
- Console output control (stdout/stderr switching)
- httpx/httpcore logging control via `propagate` parameter
- Centralized configuration via `set_level()` and `configure_file_logging()`

### Available Logging Levels

The SDK provides the following logging level constants:

- `ipsdk.logging.NOTSET` - No logging threshold (0)
- `ipsdk.logging.DEBUG` - Debug messages (10)
- `ipsdk.logging.INFO` - Informational messages (20)
- `ipsdk.logging.WARNING` - Warning messages (30)
- `ipsdk.logging.ERROR` - Error messages (40)
- `ipsdk.logging.CRITICAL` - Critical error messages (50)
- `ipsdk.logging.FATAL` - Fatal error messages (90)

### File Logging

The SDK supports optional file logging in addition to console logging. You can configure file logging using several approaches:

#### Quick Setup with `configure_file_logging`

The easiest way to enable both console and file logging:

```python
>>> import ipsdk

# Enable both console and file logging
>>> ipsdk.logging.configure_file_logging("/path/to/app.log", level=ipsdk.logging.DEBUG)
```

#### Manual File Handler Management

For more control, you can add and remove file handlers manually:

```python
>>> import ipsdk

# First set the console logging level
>>> ipsdk.logging.set_level(ipsdk.logging.INFO)

# Add a file handler
>>> ipsdk.logging.add_file_handler("/path/to/app.log")

# Add multiple file handlers with different levels
>>> ipsdk.logging.add_file_handler("/path/to/debug.log", level=ipsdk.logging.DEBUG)
>>> ipsdk.logging.add_file_handler("/path/to/errors.log", level=ipsdk.logging.ERROR)

# Remove all file handlers when done
>>> ipsdk.logging.remove_file_handlers()
```

#### Custom Log Formatting

You can specify custom format strings for file handlers:

```python
>>> custom_format = "%(asctime)s [%(levelname)s] %(message)s"
>>> ipsdk.logging.add_file_handler("/path/to/app.log", format_string=custom_format)

# Or with configure_file_logging
>>> ipsdk.logging.configure_file_logging("/path/to/app.log", format_string=custom_format)
```

**Note:** File logging automatically creates parent directories if they don't exist.

## Documentation Standards

All code in the SDK follows strict documentation standards:

### Docstring Requirements

- **Style**: Google-style docstrings
- **Required sections**:
  - `Args:` - All function/method parameters
  - `Returns:` - Return value description
  - `Raises:` - Only exceptions raised by the function/method itself
- **Format**: Verbose documentation for all public methods and functions

### Example

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """
    Brief description of what the function does.

    Longer description with additional details about the function's
    behavior, edge cases, or important notes.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter with default value

    Returns:
        Description of the return value

    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string
    """
    pass
```

### Project Documentation

Project documentation is maintained in:
- `docs/` - Detailed documentation files
- `CLAUDE.md` - Project guidance and architecture
- `README.md` - Quick start and overview
- Code docstrings - API documentation
