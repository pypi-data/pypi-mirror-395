# Contributing

Thank you for your interest in contributing to lbx. We welcome contributions of all kinds — bug reports, documentation improvements, feature requests, and code contributions.

## Ways to Contribute

**Reporting Issues**: [Open an issue](https://github.com/jd-35656/lbx/issues) with detailed steps to reproduce, expected behavior, and environment details.

**Documentation**: Fix typos, add examples, improve clarity, or enhance API documentation.

**Code**: Submit bug fixes, new features, performance improvements, or test coverage enhancements.

---

## Getting Started

### Prerequisites

- Git installed and configured
- Python 3.10+ installed  
- Nox for task automation: `pipx install nox`
- GitHub workflow familiarity

### Quick Start

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/lbx.git
cd lbx
nox -s devenv-3.13  # Setup environment
nox                 # Verify setup
```

See [Development Setup](development.md) for detailed instructions.

## Contribution Workflow

### 1. Fork and Clone

Fork the repository on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/lbx.git
cd lbx
```

### 2. Create a Branch

Create a descriptive branch for your changes:

```bash
git checkout -b feat/add-export-command
git checkout -b fix/memory-leak-issue-123
git checkout -b docs/improve-installation-guide
```

**Branch naming conventions:**

| Prefix      | Purpose           | Example                      |
| ----------- | ----------------- | ---------------------------- |
| `feat/`     | New features      | `feat/async-support`         |
| `fix/`      | Bug fixes         | `fix/validation-error`       |
| `docs/`     | Documentation     | `docs/api-reference`         |
| `refactor/` | Code refactoring  | `refactor/simplify-parser`   |
| `test/`     | Test improvements | `test/add-integration-tests` |
| `chore/`    | Maintenance       | `chore/update-dependencies`  |

### 3. Make Your Changes

Follow the [code standards](#code-standards) and ensure:

- Code is properly formatted and linted
- Type hints are included for public APIs
- Tests are added or updated
- Documentation is updated if needed

### 4. Add Changelog Entry

For user-facing changes, add a changelog fragment:

```bash
# Format: changelog.d/<number>.<type>.md
changelog.d/123.added.md      # New feature
changelog.d/456.fixed.md      # Bug fix
changelog.d/789.changed.md    # Behavior change
```

**Skip for**: Documentation, internal refactoring, CI updates, typos (add `no-changelog` label).

### 5. Commit Your Changes

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```bash
# Format: <type>(<scope>): <description>

git commit -m "feat(cli): add export command with JSON support"
git commit -m "fix(core): resolve memory leak in encryption module"
git commit -m "docs: update installation instructions"
git commit -m "test: add integration tests for vault operations"
```

**Commit types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks
- `ci`: CI/CD changes

### 6. Run Tests and Checks

Before pushing, verify everything passes:

```bash
# Run all checks
nox

# Or individually
nox -s tests-3.13  # Run tests
nox -s check       # Lint + type check
```

See [Testing Guide](testing.md) for details.

### 7. Push to Your Fork

```bash
git push origin feat/add-export-command
```

### 8. Open a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill out the PR template with:
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Checklist completion

## Code Standards

### Style Guide

See `pyproject.toml` for current configuration:

- Code formatting and linting rules
- Line length limits
- Import sorting preferences
- Docstring style requirements

### Type Hints

All public APIs must include type hints:

```python
def encrypt_data(data: bytes, key: str) -> bytes:
    """
    Encrypt data using the provided key.

    Args:
        data: Raw bytes to encrypt.
        key: Encryption key.

    Returns:
        Encrypted bytes.

    Raises:
        ValueError: If key is invalid.
    """
    ...
```

### Documentation & Testing

- All public APIs require Google-style docstrings
- Include examples for complex functionality  
- Maintain minimum 90% test coverage
- Write tests for new features and bug fixes

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass locally (`nox`)
- [ ] Code is formatted and linted
- [ ] Type checking passes
- [ ] Documentation updated
- [ ] Changelog fragment added (or `no-changelog` label)
- [ ] Commits follow Conventional Commits format
- [ ] Branch up to date with `main`

### PR Description

- What changed and why
- How to test the changes  
- Related issues (use "Fixes #123")
- Breaking changes (if any)

### Review Process

1. Automated checks must pass
2. Maintainer review required
3. Address feedback
4. Clean commit history
5. Maintainer merges when approved

## Code of Conduct

This project follows GitHub's community guidelines. By participating, you agree to maintain respectful and constructive interactions. Please report unacceptable behavior to the project maintainers.

## Getting Help

- **Documentation**: [Development Setup](development.md) and [Testing Guide](testing.md)
- **Discussions**: [GitHub Discussions](https://github.com/jd-35656/lbx/discussions)
- **Issues**: Search existing or open new ones
- **Questions**: Tag issues with `question`

## License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](https://github.com/jd-35656/lbx/blob/main/LICENSE).

## Recognition

Contributors are recognized in GitHub's contributor graph, release notes, and project documentation.

Thank you for making lbx better!

## See Also

**Contributing Guides:**

- [Development Setup](development.md)
- [Testing Guide](testing.md)
- [Release Process](releasing.md)

**Project Links:**

- [GitHub Repository](https://github.com/jd-35656/lbx)
- [Issue Tracker](https://github.com/jd-35656/lbx/issues)
- [Discussions](https://github.com/jd-35656/lbx/discussions)
- [PyPI Package](https://pypi.org/project/lbx/)

**External Resources:**

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Open Source Guides](https://opensource.guide/)
