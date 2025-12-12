# Contributing to SysMap

First off, thank you for considering contributing to SysMap! It's people like you that make SysMap such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and what you expected
- **Include screenshots** if relevant
- **Include your environment details** (OS, Python version, SysMap version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Provide specific examples** to demonstrate how it would work
- **Explain why this enhancement would be useful**

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Follow the coding style** (we use `black` for formatting and `ruff` for linting)
3. **Add tests** if you're adding functionality
4. **Update documentation** if needed
5. **Ensure the test suite passes** (`pytest`)
6. **Make sure your code lints** (`black src/ && ruff check src/`)
7. **Write a clear commit message**

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/sysmap.git
   cd sysmap
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Coding Style

We follow these conventions:

- **Python version**: Support Python 3.8+
- **Formatting**: Use `black` with line length of 100
- **Linting**: Use `ruff` for style checking
- **Type hints**: Use type hints for all function signatures
- **Docstrings**: Use Google-style docstrings for all public functions/classes

Example:
```python
def scan_packages(package_manager: str) -> List[Dict[str, str]]:
    """Scan packages from a specific package manager.

    Args:
        package_manager: Name of the package manager to scan.

    Returns:
        List of dictionaries containing package information.

    Raises:
        ValueError: If package_manager is not supported.
    """
    pass
```

## Testing

Run tests with:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=sysmap --cov-report=html
```

## Adding a New Package Manager

To add support for a new package manager:

1. Create a new scanner class in `src/sysmap/core/scanner.py`:
   ```python
   class MyPackageManagerScanner(Scanner):
       def __init__(self) -> None:
           super().__init__()
           self.name = "mypm"

       def is_available(self) -> bool:
           """Check if package manager is available."""
           return bool(self.run_command(["mypm", "--version"]))

       def scan(self) -> List[Dict[str, str]]:
           """Scan installed packages."""
           # Implementation here
           pass
   ```

2. Add it to `SystemScanner` in the `__init__` method

3. Add tests in `tests/test_scanner.py`

4. Update documentation

## Adding a New Exporter

To add a new export format:

1. Create a new file in `src/sysmap/exporters/`:
   ```python
   from .base import BaseExporter

   class MyFormatExporter(BaseExporter):
       def export(self) -> str:
           """Export data to my format."""
           # Implementation here
           pass
   ```

2. Register it in `src/sysmap/exporters/__init__.py`

3. Add it to CLI options in `src/sysmap/cli.py`

4. Add tests

## Project Structure

```
sysmap/
├── src/sysmap/           # Source code
│   ├── core/             # Core scanning logic
│   ├── exporters/        # Export format handlers
│   ├── utils/            # Utility functions
│   └── cli.py            # CLI interface
├── tests/                # Test files
├── docs/                 # Documentation
├── examples/             # Example configurations
└── .github/              # GitHub Actions workflows
```

## Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` A new feature
- `fix:` A bug fix
- `docs:` Documentation only changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
- `feat: add Homebrew package manager support`
- `fix: handle timeout in npm scanner`
- `docs: update installation instructions`

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing!
