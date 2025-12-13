# Quick Start

Get up and running with lbx in minutes.

## Installation

```bash
pipx install lbx
```

See [Installation Guide](installation.md) for other installation options.

## CLI Usage

### Create a new vault

```bash
lbx vault init
```

You'll be prompted for a password.
The derived encryption key is stored in your OS keychain.

### Add a secret

```bash
lbx secret add github token --value ghp_xxxxxx
```

Or pipe it for better security:

```bash
printf "ghp_xxxxxx" | lbx secret add github token
```

### Retrieve a secret

```bash
lbx secret get github token
```

If the keychain key is missing or outdated, you'll be prompted for the password.

### Update a secret

```bash
printf "new-value" | lbx secret update github token
```

### List services and secrets

```bash
lbx service list
lbx secret list
lbx secret list --service github
```

### Rename or move secrets

```bash
lbx secret rename github token api_key
lbx secret move github api_key gitlab
```

### Lock the vault

```bash
lbx vault lock
```

### Delete the vault

```bash
lbx vault delete
```

## Python API

```python
from lbx import Lbx

# Load vault (auto-load key from keychain when available)
vault = Lbx()

vault.get_secret("github", "token")  # returns SecretEntry
vault.add_secret("github", "token", "new-value")
vault.list_services()
vault.list_secrets()
```

## Next Steps

- **CLI Users**: See [CLI Reference](../user-guide/cli.md) for all commands
- **Python Developers**: See [API Reference](../api/index.md) for complete documentation
- **Need Help?**: Check [Installation Guide](installation.md) for troubleshooting

## See Also

**Documentation:**

- [Installation Guide](installation.md) - Detailed installation instructions
- [CLI Reference](../user-guide/cli.md) - Complete command reference
- [API Reference](../api/index.md) - Python API documentation

**Support:**

- [GitHub Issues](https://github.com/jd-35656/lbx/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/jd-35656/lbx/discussions) - Questions and community support
