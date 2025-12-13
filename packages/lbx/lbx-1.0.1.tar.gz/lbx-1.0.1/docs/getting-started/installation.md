# Installation

Install lbx using your preferred Python package manager.

## Recommended: Using pipx

!!! tip "Why pipx?"
    [pipx](https://pypa.github.io/pipx/) installs Python CLI tools in isolated environments,
    keeping your global Python setup clean while making the command available system-wide.

### Install pipx

=== "macOS"
    ```bash
    brew install pipx
    pipx ensurepath
    ```

=== "Ubuntu / Debian"
    ```bash
    sudo apt update
    sudo apt install pipx
    pipx ensurepath
    ```

=== "Windows (Scoop)"
    ```powershell
    scoop install pipx
    pipx ensurepath
    ```

=== "Windows (pip)"
    ```powershell
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```

=== "Other Linux"
    ```bash
    python -m pip install --user pipx
    python -m pipx ensurepath
    ```

### Install lbx

```bash
pipx install lbx
```

!!! success "Installation Complete"
    lbx is now available system-wide as the `lbx` command.

### Verify Installation

```bash
lbx --version
lbx --help
```

---

## Alternative: Using pip

!!! warning "Virtual Environment Recommended"
    Installing globally with pip can cause conflicts. Use pipx or a virtual environment instead.

=== "With Virtual Environment (Recommended)"
    ```bash
    python -m venv lbx-env
    source lbx-env/bin/activate  # Windows: lbx-env\Scripts\activate
    pip install lbx
    ```

=== "Global Installation"
    ```bash
    pip install lbx
    ```

---

## Upgrading

=== "pipx"
    ```bash
    pipx upgrade lbx
    ```

=== "pip"
    ```bash
    pip install --upgrade lbx
    ```

---

## Uninstalling

=== "pipx"
    ```bash
    pipx uninstall lbx
    ```

=== "pip"
    ```bash
    pip uninstall lbx
    ```

## Development Installation

For contributing to lbx development:

```bash
git clone https://github.com/jd-35656/lbx.git
cd lbx
pipx install --editable .
```

See [Development Setup](../contributing/development.md) for detailed instructions.

## System Requirements

| Requirement          | Details                 |
| -------------------- | ----------------------- |
| **Python**           | 3.10 or higher          |
| **Operating System** | Windows, macOS, Linux   |
| **Dependencies**     | Installed automatically |

## Troubleshooting

### Command Not Found

If `lbx` command is not found after installation:

=== "pipx"
    ```bash
    pipx ensurepath
    # Restart your terminal
    ```

=== "pip (virtual environment)"
    ```bash
    # Ensure virtual environment is activated
    source lbx-env/bin/activate
    ```

### Permission Errors

On Unix systems, if you encounter permission errors:

```bash
# Use pipx instead of global pip
pipx install lbx
```

### Python Version Issues

Ensure you have Python 3.10 or higher:

```bash
python --version
```

If you need to upgrade Python, visit [python.org](https://www.python.org/downloads/).

## See Also

**Getting Started:**

- [Quick Start Guide](quickstart.md) - Start using lbx in minutes
- [CLI Reference](../user-guide/cli.md) - Complete command reference
- [API Reference](../api/index.md) - Python API documentation

**For Developers:**

- [Development Setup](../contributing/development.md) - Set up development environment
- [Contributing Guide](../contributing/index.md) - How to contribute to lbx

**External Resources:**

- [pipx Documentation](https://pypa.github.io/pipx/) - Learn more about pipx
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html) - Official Python venv guide
