# Testing

Complete guide for running tests, ensuring code quality, and validating changes before submitting contributions.

## Overview

This project uses [Nox](https://nox.thea.codes/) to automate testing across multiple Python versions. All test sessions include code coverage reporting and enforce a minimum 90% coverage threshold.

**Supported Python Versions:** 3.10, 3.11, 3.12, 3.13

## Quick Start

```bash
# Run tests and quality checks (default)
nox

# Run tests on specific Python version
nox -s tests-3.13

# Run all quality checks
nox -s check
```

## Running Tests

### Basic Usage

=== "All Versions"
    ```bash
    nox -s tests
    ```

=== "Specific Version"
    ```bash
    nox -s tests-3.13
    nox -s tests-3.10
    ```

=== "Current Python"
    ```bash
    nox --python current -s tests
    ```

### Passing Arguments to Pytest

Pass custom arguments to pytest using `--`:

```bash
# Verbose output
nox -s tests-3.13 -- -v

# Run specific test file
nox -s tests-3.13 -- tests/test_cli.py

# Run tests matching pattern
nox -s tests-3.13 -- -k test_encryption

# Stop on first failure
nox -s tests-3.13 -- -x

# Multiple arguments
nox -s tests-3.13 -- -v -x --tb=short
```

### Common Pytest Options

| Option                   | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `-v`, `--verbose`        | Increase verbosity                               |
| `-s`                     | Disable output capturing (show print statements) |
| `-x`, `--exitfirst`      | Stop on first test failure                       |
| `-k EXPRESSION`          | Run tests matching given expression              |
| `--lf`, `--last-failed`  | Rerun only tests that failed last time           |
| `--ff`, `--failed-first` | Run failed tests first, then others              |
| `--maxfail=N`            | Stop after N failures                            |
| `--tb=short`             | Shorter traceback format                         |
| `--tb=no`                | Disable traceback                                |
| `--pdb`                  | Drop into debugger on failure                    |

---

## Code Coverage

### Viewing Coverage Reports

Test sessions automatically generate coverage reports:

```bash
nox -s tests-3.13
```

**Terminal Output:**

```txt
---------- coverage: platform darwin, python 3.13.0 -----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/lbx/__init__.py      12      0   100%
src/lbx/core.py         145      7    95%   78-82, 156
src/lbx/cli.py           89      4    96%   234-237
-----------------------------------------------------
TOTAL                     246     11    96%

Required test coverage of 90% reached. Total coverage: 96.00%
```

### HTML Coverage Reports

Generate interactive HTML coverage report:

```bash
nox -s tests-3.13 -- --cov-report=html
```

View the report:

```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html
```

### Coverage Requirements

From `pyproject.toml`:

```toml
[tool.coverage.report]
fail_under = 90
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

!!! note "Minimum Threshold"
    All code must maintain at least **90% test coverage**. Tests will fail if coverage drops below this threshold.

## Code Quality Checks

### Linting

Check code style and formatting with Ruff:

```bash
nox -s lint
```

This validates:

- Code style compliance (PEP 8)
- Import sorting and organization
- Unused imports and variables
- Security issues (via Bandit rules)
- Code complexity
- Common bugs and anti-patterns

**Configuration:** See `[tool.ruff]` section in `pyproject.toml`

### Type Checking

Run static type analysis with MyPy:

```bash
# Check all source files
nox -s typecheck

# Check specific module
nox -s typecheck -- src/lbx/core

# Check specific file
nox -s typecheck -- src/lbx/cli.py
```

**Configuration:** See `[tool.mypy]` section in `pyproject.toml`

### Combined Quality Checks

Run both linting and type checking:

```bash
nox -s check
```

This is equivalent to running:

```bash
nox -s lint
nox -s typecheck
```

## Development Environment

### Setup

Create a complete development environment:

```bash
nox -s devenv-3.13
```

This installs:

- Project in editable mode
- All test dependencies (pytest, pytest-cov)
- Type checking tools (mypy)
- Documentation dependencies
- Development tools (nox)

### Activating the Environment

```bash
# Unix/Linux/macOS
source .nox/devenv-3-13/bin/activate

# Windows
.nox\devenv-3-13\Scripts\activate
```

### IDE Configuration

Configure your IDE to use the Nox virtual environment:

```bash
# Get Python interpreter path (after activation)
which python

# Example output:
# /path/to/project/.nox/devenv-3-13/bin/python
```

Point your IDE's Python interpreter to this path.

## Test Organization

### Directory Structure

```txt
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_core.py             # Core functionality tests
├── test_cli.py              # CLI tests
└── integration/
    └── test_e2e.py          # End-to-end tests
```

### Test Discovery

Pytest automatically discovers:

- Test files: `tests/test_*.py` or `tests/*_test.py`
- Test functions: `def test_*()`
- Test classes: `class Test*`
- Test methods: `def test_*()` within test classes

Configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

## Available Nox Sessions

View all available sessions:

```bash
nox --list
```

### Testing Sessions

| Session      | Description              |
| ------------ | ------------------------ |
| `tests-3.10` | Run tests on Python 3.10 |
| `tests-3.11` | Run tests on Python 3.11 |
| `tests-3.12` | Run tests on Python 3.12 |
| `tests-3.13` | Run tests on Python 3.13 |

### Quality Sessions

| Session     | Description            |
| ----------- | ---------------------- |
| `lint`      | Run Ruff linter checks |
| `typecheck` | Run MyPy type checking |
| `check`     | Run lint + typecheck   |

### Development Sessions

| Session      | Description                    |
| ------------ | ------------------------------ |
| `devenv-3.X` | Set up development environment |
| `build`      | Build distribution packages    |

### Documentation Sessions

| Session       | Description                 |
| ------------- | --------------------------- |
| `docs_serve`  | Serve documentation locally |
| `deploy_docs` | Deploy docs to GitHub Pages |

## Continuous Integration

All pull requests must pass:

- Tests on all supported Python versions (3.10-3.13)
- Code coverage threshold (≥90%)
- Linting checks (Ruff)
- Type checking (MyPy)

### Running CI Checks Locally

Before pushing changes:

```bash
# Run default sessions (tests + check)
nox

# Run tests on all Python versions
nox -s tests

# Verify code quality
nox -s check
```

## Troubleshooting

### Common Issues

| Problem                    | Solution                                                     |
| -------------------------- | ------------------------------------------------------------ |
| Nox not found              | Install: `pip install nox` or `pipx install nox`             |
| Python version unavailable | Install missing version or use `--python current`            |
| Import errors during tests | Install project: `pip install -e .` or run `nox -s devenv`   |
| Coverage below threshold   | Add tests or mark unreachable code with `# pragma: no cover` |
| Port 8000 already in use   | Kill process: `lsof -ti :8000 \| xargs kill -9`              |

### Clearing Nox Cache

Remove all virtual environments:

```bash
nox --clean
```

Remove specific session:

```bash
rm -rf .nox/tests-3-13
```

### Verbose Output

See all commands executed by Nox:

```bash
nox -s tests-3.13 --verbose
```

## Best Practices

### Pre-Commit Checklist

- [ ] All tests pass locally
- [ ] Code coverage ≥90%
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] Changelog fragment added

### Testing Workflow

```bash
# Setup (once)
nox -s devenv-3.13
source .nox/devenv-3-13/bin/activate

# Development
pytest tests/test_core.py -v

# Pre-commit
nox -s tests-3.13 check

# Pre-push
nox
```

### Writing Tests

```python
# tests/test_example.py
import pytest


def test_basic_functionality():
    """Test basic feature behavior."""
    result = my_function(input_data)
    assert result == expected_output


def test_error_handling():
    """Test that errors are raised appropriately."""
    with pytest.raises(ValueError, match="Invalid input"):
        my_function(invalid_data)


@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiple_cases(input, expected):
    """Test function with multiple inputs."""
    assert double(input) == expected
```

## Advanced Usage

### Parallel Test Execution

Install pytest-xdist:

```bash
pip install pytest-xdist
```

Run tests in parallel:

```bash
# Use 4 workers
nox -s tests-3.13 -- -n 4

# Use auto-detection
nox -s tests-3.13 -- -n auto
```

### Test Reports

Generate JUnit XML report (for CI systems):

```bash
nox -s tests-3.13 -- --junit-xml=test-results.xml
```

### Debugging Tests

Drop into debugger on failure:

```bash
nox -s tests-3.13 -- --pdb
```

Show local variables in traceback:

```bash
nox -s tests-3.13 -- -l
```

### Rerunning Failed Tests

```bash
# Run only last failed tests
nox -s tests-3.13 -- --lf

# Run failed tests first, then remaining
nox -s tests-3.13 -- --ff
```

## Configuration Reference

All testing, coverage, and linting configurations are defined in `pyproject.toml`. See the file for:

- Test discovery paths and options
- Coverage thresholds and reporting
- Code formatting rules
- Linting and type checking settings

## See Also

**Contributing Guides:**

- [Contributing Overview](index.md)
- [Development Setup](development.md)
- [Release Process](releasing.md)

**External Resources:**

- [Nox Documentation](https://nox.thea.codes/)
- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
