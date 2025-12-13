# Contributing to Itential Python SDK

Thank you for your interest in contributing to the Itential Python SDK! This guide will help you get started with contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a code of conduct that promotes a welcoming and inclusive environment. Please be respectful and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.8 or higher (we test on 3.10, 3.11, 3.12, 3.13)
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/ipsdk.git
   cd ipsdk
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/itential/ipsdk.git
   ```

## Development Setup

### Install Dependencies

```bash
# Install all dependencies including development tools
uv sync

# Verify installation
uv run python --version
uv run pytest --version
```

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
uv run pre-commit install
```

This will run linting, formatting, and security checks before each commit.

## Development Workflow

### Branch Strategy

- `devel` - Main development branch
- `feature/your-feature` - Feature branches
- `fix/issue-description` - Bug fix branches
- `security/security-improvement` - Security-related changes

### Creating a Feature Branch

```bash
git checkout devel
git pull upstream devel
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in small, logical commits
2. Follow the [code standards](#code-standards)
3. Add or update tests as needed
4. Update documentation if required
5. Run the development checks frequently

### Development Commands

```bash
# Run all linting checks
make lint
uv run ruff check src/ipsdk tests

# Auto-format code
make format
uv run ruff format src/ipsdk tests

# Auto-fix linting issues where possible
make ruff-fix
uv run ruff check --fix src/ipsdk tests

# Run tests
make test
uv run pytest tests

# Run tests with coverage
make coverage
uv run pytest --cov=src/ipsdk --cov-report=term --cov-report=html tests/

# Run security analysis
make security
uv run bandit -r src/ipsdk --configfile pyproject.toml

# Run type checking
uv run mypy src/ipsdk

# Run all premerge checks (recommended before pushing)
make premerge
```

### Testing Different Python Versions

```bash
# Test specific Python version
uv run --python 3.10 pytest tests
uv run --python 3.11 pytest tests
uv run --python 3.12 pytest tests
uv run --python 3.13 pytest tests

# Test all supported versions
for version in 3.10 3.11 3.12 3.13; do
    echo "Testing Python $version"
    uv run --python $version pytest tests
done
```

## Code Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) for Python code style
- Use [Black](https://black.readthedocs.io/)-compatible formatting (88 character line length)
- Code is automatically formatted using Ruff

### Code Quality

- **Linting**: We use Ruff with comprehensive rule sets (30+ categories)
- **Type Hints**: All public APIs must include type hints
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Security**: All code is scanned with Bandit and Ruff security rules

### Docstring Format

```python
def example_function(param1: str, param2: int = 10) -> bool:
    """Brief description of what the function does.

    Longer description if needed, explaining the function's behavior,
    usage patterns, or important considerations.

    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter with default value.

    Returns:
        Description of the return value and its type.

    Raises:
        ValueError: When param1 is invalid.
        ConnectionError: When unable to connect to the server.

    Example:
        >>> result = example_function("test", 20)
        >>> print(result)
        True
    """
```

### Import Organization

- Follow the import order: standard library, third-party, local
- Use absolute imports
- One import per line

```python
# Standard library
import os
from typing import Optional

# Third-party
import httpx

# Local
from ipsdk.connection import Connection
from ipsdk.exceptions import ConnectionError
```

## Testing

### Test Structure

- Tests are located in the `tests/` directory
- Test files follow the pattern `test_<module>.py`
- Each module should have comprehensive test coverage

### Writing Tests

```python
import pytest
from ipsdk import platform_factory


def test_platform_factory_basic():
    """Test basic platform factory functionality."""
    client = platform_factory(
        host="https://test.example.com",
        username="test_user",
        password="test_pass"
    )
    assert client is not None


@pytest.mark.asyncio
async def test_async_connection():
    """Test async connection functionality."""
    async with platform_factory(
        host="https://test.example.com",
        username="test_user",
        password="test_pass",
        want_async=True
    ) as client:
        assert client is not None
```

### Coverage Requirements

- Minimum 95% test coverage is required
- All new code must include tests
- Tests should cover both success and failure scenarios
- Use `make coverage-check` to verify coverage meets requirements

### Running Tests

```bash
# Run all tests
uv run pytest tests

# Run specific test file
uv run pytest tests/test_connection.py

# Run specific test function
uv run pytest tests/test_connection.py::test_basic_connection

# Run with verbose output
uv run pytest -v tests

# Run with coverage reporting
uv run pytest --cov=src/ipsdk --cov-report=term tests
```

## Documentation

### Code Documentation

- All public APIs must have docstrings
- Use Google-style docstrings
- Include examples in docstrings where helpful
- Document all parameters, return values, and exceptions

### README Updates

- Update README.md if your changes affect:
  - Installation instructions
  - Usage examples
  - API changes
  - New features

### Changelog

- The project uses [conventional commits](https://www.conventionalcommits.org/) for automatic changelog generation
- Changelog is generated automatically using git-cliff
- Use descriptive commit messages following the conventional format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `test:` for test improvements
  - `ci:` for CI/CD changes
  - `refactor:` for code refactoring

## Submitting Changes

### Before Submitting

1. Ensure all tests pass: `make test`
2. Run the full premerge pipeline: `make premerge`
3. Update documentation if needed
4. Write descriptive commit messages

### Pull Request Process

1. Push your feature branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a pull request against the `devel` branch

3. Fill out the pull request template with:
   - Clear description of changes
   - Testing performed
   - Any breaking changes
   - Related issues

### Pull Request Requirements

- All CI checks must pass
- Code coverage must be ≥95%
- At least one maintainer approval required
- All conversations must be resolved

### Commit Message Format

Use conventional commit format:

```
type(scope): description

Longer explanation if needed.

- List any breaking changes
- Reference related issues

```

## Release Process

### Versioning

- Uses [Semantic Versioning](https://semver.org/)
- Version is automatically determined from git tags
- Format: `v<major>.<minor>.<patch>` (e.g., `v1.0.0`)

### Release Types

- **Production Release**: `v1.0.0` → PyPI + GitHub release
- **Pre-release**: `v1.0.0-alpha.1` → TestPyPI + GitHub pre-release

### Creating a Release

Releases are automated via GitHub Actions:

1. Create and push a version tag:
   ```bash
   git tag v1.0.0
   git push upstream v1.0.0
   ```

2. GitHub Actions will:
   - Run all tests and checks
   - Build wheel and source distributions
   - Publish to PyPI
   - Create GitHub release with changelog
   - Generate release notes

### GoReleaser

The project uses GoReleaser for release automation:

```bash
# Test release configuration
goreleaser check

# Test build locally
goreleaser build --snapshot --clean

# Test full release locally (no publishing)
goreleaser release --snapshot --clean
```

## Getting Help

### Resources

- [Python SDK Documentation](https://github.com/itential/ipsdk)
- [Itential Platform Documentation](https://docs.itential.com/)
- [Project Issues](https://github.com/itential/ipsdk/issues)

### Contact

- Create an issue for bugs or feature requests
- Use discussions for questions and community interaction
- Follow the security policy for security-related issues

### Development Environment Issues

If you encounter issues with the development environment:

1. Ensure you have the latest version of uv
2. Try cleaning and reinstalling dependencies:
   ```bash
   make clean
   uv sync
   ```
3. Check that all required Python versions are available
4. Verify pre-commit hooks are installed

## Thank You

Thank you for contributing to the Itential Python zRK! Your contributions help make the project better for everyone.
