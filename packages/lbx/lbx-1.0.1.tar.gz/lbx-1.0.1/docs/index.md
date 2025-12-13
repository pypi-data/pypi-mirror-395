<!-- markdownlint-disable MD033 -->
# lbx - Lock Box

A lightweight secret storage vault with CLI and Python API. Stores secrets in encrypted files with master password secured via OS keychain.

## What is lbx?

lbx provides secure, encrypted storage for sensitive data like API keys, passwords, and configuration secrets. It features both a command-line interface and Python API for seamless integration into your workflow.

## Key Features

- **Secure Encryption**: AES-256 encryption with master password protection
- **Cross-Platform**: Works on Windows, macOS, and Linux  
- **Dual Interface**: Both CLI and Python API available
- **Keychain Integration**: Master password stored securely in OS keychain
- **Simple Workflow**: Intuitive commands for daily use
- **Minimal Dependencies**: Lightweight and secure

## Getting Started

<div class="grid cards" markdown>

- :material-download:{ .lg .middle } **Installation**

    ---

    Install lbx using pipx, pip, or from source

    [:octicons-arrow-right-24: Install lbx](getting-started/installation.md)

- :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Get up and running with lbx in minutes

    [:octicons-arrow-right-24: Quick start guide](getting-started/quickstart.md)

- :material-console:{ .lg .middle } **CLI Reference**

    ---

    Complete command-line interface documentation

    [:octicons-arrow-right-24: CLI commands](user-guide/cli.md)

- :material-code-braces:{ .lg .middle } **API Reference**

    ---

    Python API for programmatic access

    [:octicons-arrow-right-24: Python API](api/index.md)

</div>

## Use Cases

**Development Teams**
: Store API keys, database credentials, and service tokens securely across team members

**DevOps & CI/CD**
: Manage secrets in deployment pipelines and infrastructure automation

**Personal Projects**
: Keep sensitive configuration data encrypted and organized

**Security-Conscious Users**
: Replace plain-text config files with encrypted secret storage

## Why lbx?

| Feature                  | lbx                 | Environment Variables | Config Files      |
| ------------------------ | ------------------- | --------------------- | ----------------- |
| **Encryption**           | ✅ AES-256           | ❌ Plain text          | ❌ Plain text      |
| **Cross-platform**       | ✅ Windows/Mac/Linux | ✅ All platforms       | ✅ All platforms   |
| **Keychain integration** | ✅ OS keychain       | ❌ Manual              | ❌ Manual          |
| **Programmatic access**  | ✅ CLI + Python API  | ✅ Environment         | ✅ File parsing    |
| **Version control safe** | ✅ Encrypted files   | ❌ Exposed secrets     | ❌ Exposed secrets |

## Requirements

- Python 3.10 or higher
- Windows, macOS, or Linux
- OS keychain support (automatic)

## Community & Support

- **Documentation**: [https://jd-35656.github.io/lbx/](https://jd-35656.github.io/lbx/)
- **Source Code**: [GitHub Repository](https://github.com/jd-35656/lbx)
- **Bug Reports**: [GitHub Issues](https://github.com/jd-35656/lbx/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jd-35656/lbx/discussions)
- **PyPI Package**: [pypi.org/project/lbx](https://pypi.org/project/lbx/)

## License

lbx is released under the [MIT License](https://github.com/jd-35656/lbx/blob/main/LICENSE).

---

**Ready to secure your secrets?** Start with the [Installation Guide](getting-started/installation.md) or jump to the [Quick Start](getting-started/quickstart.md).

---

© 2025 Jitesh Sahani (JD)  
📧 [jitesh.sahani@outlook.com](mailto:jitesh.sahani@outlook.com)

*"Your secrets are safe, your mind at peace."*  
🐺 Crafted by a dreamer, for dreamers 🐺
