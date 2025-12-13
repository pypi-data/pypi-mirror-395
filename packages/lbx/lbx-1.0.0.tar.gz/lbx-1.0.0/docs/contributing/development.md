# Development Setup

Complete guide for setting up a local development environment.

## Prerequisites

Before starting, ensure you have:

- **Git**: Version control ([Download](https://git-scm.com/downloads))
- **Python**: Version 3.10 or higher ([Download](https://www.python.org/downloads/))
- **Nox**: Task automation tool

Install Nox:

=== "pipx (Recommended)"
    ```bash
    python -m pip install --user pipx
    python -m pipx ensurepath
    pipx install nox
    ```

=== "pip"
    ```bash
    pip install nox
    ```

## Initial Setup

### 1. Fork and Clone

Fork the repository on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/lbx.git
cd lbx
```

### 2. Add Upstream Remote

Add the original repository as upstream:

```bash
git remote add upstream https://github.com/jd-35656/lbx.git
git fetch upstream
```

### 3. Create Development Environment

Use Nox to set up a complete development environment:

```bash
nox -s devenv-3.13
```

This creates a virtual environment in `.nox/devenv-3-13/` with:

- Project installed in editable mode
- All test dependencies
- Type checking tools
- Documentation tools
- Development utilities

### 4. Activate Virtual Environment

=== "Unix/Linux/macOS"
    ```bash
    source .nox/devenv-3-13/bin/activate
    ```

=== "Windows"
    ```bash
    .nox\devenv-3-13\Scripts\activate
    ```

### 5. Verify Installation

```bash
lbx --version         # Check command availability
nox -s tests-3.13       # Run tests
nox                     # Run all checks
```

## Python Version Management

### Switching Python Versions

The project supports Python 3.10 through 3.13. Use different environments for each version:

```bash
# List available sessions
nox --list

# Create environment for Python 3.12
nox -s devenv-3.12
source .nox/devenv-3-12/bin/activate
```

### Using pyenv (Recommended)

Manage multiple Python versions with [pyenv](https://github.com/pyenv/pyenv):

```bash
# Install pyenv (macOS)
brew install pyenv

# Install Python versions
pyenv install 3.10.13
pyenv install 3.11.7
pyenv install 3.12.1
pyenv install 3.13.0

# Set local Python versions for project
pyenv local 3.13.0 3.12.1 3.11.7 3.10.13
```

## IDE Configuration

### Visual Studio Code

#### 1. Select Interpreter

- Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
- Type "Python: Select Interpreter"
- Choose `.nox/devenv-3-13/bin/python`

#### 2. Recommended Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "tamasfe.even-better-toml"
  ]
}
```

#### 3. Workspace Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".nox/devenv-3-13/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests"],
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    }
  },
  "ruff.importStrategy": "fromEnvironment"
}
```

### PyCharm

#### 1. Set Project Interpreter

- File → Settings → Project → Python Interpreter
- Click gear icon → Add
- Select "Existing environment"
- Choose `.nox/devenv-3-13/bin/python`
- Apply changes

#### 2. Configure Pytest

- Settings → Tools → Python Integrated Tools
- Default test runner: pytest
- Apply

#### 3. Enable Ruff

- Settings → Tools → External Tools
- Add new tool:
  - Name: Ruff Format
  - Program: `$ProjectFileDir$/.nox/devenv-3-13/bin/ruff`
  - Arguments: `format $FilePath$`
  - Working directory: `$ProjectFileDir$`

## Project Structure

Understanding the project layout:

```txt
lbx/
├── .github/
│   └── workflows/          # CI/CD automation
├── docs/                   # MkDocs documentation
│   ├── contributing/       # Contribution guides
│   ├── changelog.md        # Release history
│   └── ...
├── src/lbx/              # Main package source
│   ├── __init__.py
│   ├── __main__.py         # CLI entry point
│   ├── __version__.py      # Auto-generated version
│   ├── cli/                # Command-line interface
│   └── core/               # Core functionality
├── tests/                  # Test suite
│   ├── conftest.py         # Pytest fixtures
│   ├── test_cli.py
│   └── ...
├── changelog.d/            # Changelog fragments
├── noxfile.py              # Task automation
├── pyproject.toml          # Project metadata & config
├── README.md
└── LICENSE
```

## Common Development Tasks

| Task             | Command                                |
| ---------------- | -------------------------------------- |
| Run application  | `lbx --help` or `python -m lbx --help` |
| Run tests        | `nox -s tests-3.13`                    |
| Check formatting | `nox -s lint`                          |
| Type checking    | `nox -s typecheck`                     |
| Serve docs       | `nox -s docs_serve`                    |
| Build package    | `hatch build`                          |

See [Testing Guide](testing.md) for detailed testing instructions.

## Working with Dependencies

### Adding Dependencies

Edit `pyproject.toml`:

```toml
[project]
dependencies = [
    "click>=8.3",
    "cryptography>=44.0",
    # Add new dependency here
]
```

Then reinstall:

```bash
pip install -e .
```

### Adding Development Dependencies

```toml
[project.optional-dependencies]
tests = [
    "pytest>=8.3.5",
    # Add test dependency
]
types = [
    "mypy>=1.15",
    # Add type stub
]
docs = [
    "mkdocs>=1.6",
    # Add docs dependency
]
```

Recreate environment:

```bash
nox -s devenv-3.13 --force
```

## Keeping Your Fork Updated

Regularly sync with the upstream repository:

```bash
# Fetch latest changes
git fetch upstream

# Update your main branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

## Troubleshooting

| Problem                | Solution                                  |
| ---------------------- | ----------------------------------------- |
| Nox not found          | `pipx install nox`                        |
| Python version missing | Install version or use `--python current` |
| Import errors          | `pip install -e .`                        |
| Tests fail after pull  | `nox -s devenv --force`                   |
| Port 8000 in use       | `lsof -ti :8000 \| xargs kill -9`         |

**Reset environment:**

```bash
nox --clean
nox -s devenv-3.13
```

## Next Steps

Now that your environment is set up:

1. Read the [Contributing Guide](index.md) for workflow details
2. Review the [Testing Guide](testing.md) for testing practices
3. Check [open issues](https://github.com/jd-35656/lbx/issues) for contribution ideas
4. Join [GitHub Discussions](https://github.com/jd-35656/lbx/discussions) for questions

## See Also

**Contributing Guides:**

- [Contributing Overview](index.md)
- [Testing Guide](testing.md)
- [Release Process](releasing.md)

**External Resources:**

- [Nox Documentation](https://nox.thea.codes/)
- [Hatch Documentation](https://hatch.pypa.io/)
- [pyenv](https://github.com/pyenv/pyenv)
- [pipx](https://pypa.github.io/pipx/)
- [VS Code Python](https://code.visualstudio.com/docs/python/python-tutorial)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Git Workflow](https://docs.github.com/en/get-started/quickstart/github-flow)
