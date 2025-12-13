# SPDX-FileCopyrightText: 2025-present jd-35656 <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Click-based command-line interface for Lbx."""

from __future__ import annotations

import getpass
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from lbx.__version__ import __version__
from lbx.core import Lbx
from lbx.exceptions import DecryptionError, LbxError

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def build_lbx(vault: Path | None) -> Lbx:
    """Construct an Lbx instance for CLI usage.

    The CLI always uses the OS keychain for key storage.

    Args:
        vault: Optional path to the vault file.

    Returns:
        Configured Lbx instance.
    """
    return Lbx(path=vault, use_keychain=True)


def ensure_unlocked(lbx: Lbx) -> None:
    """Ensure the vault is unlocked, prompting if necessary.

    Strategy:
    * If already unlocked: do nothing.
    * Otherwise, try to unlock from keychain.
    * If still locked, ask for password and unlock.

    Args:
        lbx: Lbx instance to ensure unlocked.
    """
    if lbx.is_unlocked:
        return

    # Best-effort: try keychain
    try:
        if lbx.unlock_from_keychain():
            return
    except LbxError:
        # Ignore and fall back to password prompt
        pass

    # Fallback: ask user
    password = getpass.getpass("Vault password: ")
    lbx.unlock(password)


def retry_on_bad_key(
    lbx: Lbx,
    func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Run an operation, retrying once if the key is invalid.

    This is used for operations that decrypt data. If a DecryptionError occurs,
    it is assumed that the stored key (from keychain) is stale or invalid.
    The user is prompted for the password and the operation is retried once.

    Args:
        lbx: Lbx instance used to unlock with a fresh password.
        func: Callable to execute.
        *args: Positional arguments passed to ``func``.
        **kwargs: Keyword arguments passed to ``func``.

    Returns:
        Result of ``func(*args, **kwargs)``.

    Raises:
        DecryptionError: If decryption still fails after retry.
    """
    try:
        return func(*args, **kwargs)
    except DecryptionError:
        click.echo("Stored key is invalid. Please enter vault password again.", err=True)
        password = getpass.getpass("Vault password: ")
        lbx.unlock(password)
        return func(*args, **kwargs)


def read_secret_value(name: str, value_opt: str | None) -> str:
    """Read a secret value from --value, stdin, or a prompt.

    Priority:
    * If --value is given: use that.
    * Else if stdin is piped: read from stdin.
    * Else: prompt without echo.

    Args:
        name: Logical name of the secret (used in the prompt).
        value_opt: Optional value passed via CLI.

    Returns:
        Secret value as a string.
    """
    if value_opt is not None:
        return value_opt

    if not sys.stdin.isatty():
        # Piped input
        return sys.stdin.read().rstrip("\n")

    # Interactive prompt without echo
    return getpass.getpass(f"Enter secret for {name}: ")


# ---------------------------------------------------------------------------
# Root group
# ---------------------------------------------------------------------------


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=False,
)
@click.version_option(version=__version__, prog_name="lbx")
@click.option(
    "--vault",
    "-v",
    type=click.Path(path_type=Path),
    help="Path to the vault file. Defaults to ~/.lbx/vault.lbx",
)
@click.pass_context
def lbx(ctx: click.Context, vault: Path | None) -> None:
    """Lbx encrypted secret manager."""
    ctx.obj = {"vault_path": vault}


# ---------------------------------------------------------------------------
# Vault commands
# ---------------------------------------------------------------------------


@lbx.group(help="Vault management commands.")
@click.pass_context
def vault(ctx: click.Context) -> None:
    """Vault commands group."""
    # Context not used directly; kept for symmetry.


@vault.command("init", help="Create a new vault.")
@click.pass_context
def vault_init(ctx: click.Context) -> None:
    """Create a new vault and store its key in the OS keychain."""
    s = build_lbx(ctx.obj["vault_path"])

    pw1 = getpass.getpass("New vault password: ")
    pw2 = getpass.getpass("Repeat password: ")

    if pw1 != pw2:
        click.echo("Error: passwords do not match", err=True)
        raise SystemExit(1)

    s.create(pw1)
    click.echo(f"Vault created at {s.path}")


@vault.command("unlock", help="Unlock vault using a password.")
@click.pass_context
def vault_unlock(ctx: click.Context) -> None:
    """Unlock a vault using a password and store the key in the keychain."""
    s = build_lbx(ctx.obj["vault_path"])
    password = getpass.getpass("Vault password: ")
    s.unlock(password)
    click.echo("Vault unlocked (key stored in OS keychain).")


@vault.command("lock", help="Lock vault (clear key from memory).")
@click.pass_context
def vault_lock(ctx: click.Context) -> None:
    """Lock the vault by clearing the in-memory key."""
    s = build_lbx(ctx.obj["vault_path"])
    s.lock()
    click.echo("Vault locked.")


@vault.command("delete", help="Delete vault file and keychain entry.")
@click.pass_context
def vault_delete(ctx: click.Context) -> None:
    """Delete the vault file and any associated keychain entry."""
    s = build_lbx(ctx.obj["vault_path"])

    confirm = click.prompt(
        f"Type DELETE to delete vault at {s.path}",
        type=str,
        show_default=False,
    )
    if confirm != "DELETE":
        click.echo("Aborted.")
        raise SystemExit(1)

    s.delete_vault()
    click.echo("Vault and keychain entry deleted.")


@vault.command("status", help="Show vault status.")
@click.pass_context
def vault_status(ctx: click.Context) -> None:
    """Show basic vault status."""
    s = build_lbx(ctx.obj["vault_path"])

    if not s.exists():
        click.echo("Vault: not found")
        return

    click.echo(f"Vault: {s.path}")
    click.echo("Status: unlocked" if s.is_unlocked else "Status: locked")


# ---------------------------------------------------------------------------
# Service commands
# ---------------------------------------------------------------------------


@lbx.group(help="Service operations.")
@click.pass_context
def service(ctx: click.Context) -> None:
    """Service commands group."""


@service.command("list", help="List all services.")
@click.pass_context
def service_list(ctx: click.Context) -> None:
    """List all service names in the vault."""
    s = build_lbx(ctx.obj["vault_path"])
    services = s.list_services()  # only needs vault loaded
    for name in services:
        click.echo(name)


@service.command("rename", help="Rename a service.")
@click.argument("old")
@click.argument("new")
@click.pass_context
def service_rename(ctx: click.Context, old: str, new: str) -> None:
    """Rename an existing service.

    Args:
        old: Existing service name.
        new: New service name.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)
    s.rename_service(old, new)
    click.echo(f"{old!r} -> {new!r}")


@service.command("delete", help="Delete a service.")
@click.argument("name")
@click.pass_context
def service_delete(ctx: click.Context, name: str) -> None:
    """Delete a service and all its secrets.

    Args:
        name: Service name.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)
    s.delete_service(name)
    click.echo(f"Deleted service {name!r}")


# ---------------------------------------------------------------------------
# Secret commands
# ---------------------------------------------------------------------------


@lbx.group(help="Secret operations.")
@click.pass_context
def secret(ctx: click.Context) -> None:
    """Secret commands group."""


@secret.command("list", help="List secrets.")
@click.option("-s", "--service", help="Filter by service")
@click.pass_context
def secret_list(ctx: click.Context, service: str | None) -> None:
    """List secrets, optionally filtered by service.

    Args:
        service: Optional service name to filter by.
    """
    s = build_lbx(ctx.obj["vault_path"])
    entries = s.list_secrets(service=service)  # names only
    for svc, name in entries:
        click.echo(name if service else f"{svc}:{name}")


@secret.command("get", help="Get decrypted secret.")
@click.argument("service")
@click.argument("name")
@click.pass_context
def secret_get(ctx: click.Context, service: str, name: str) -> None:
    """Print a decrypted secret to stdout.

    Args:
        service: Service name.
        name: Secret name.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)
    entry = retry_on_bad_key(s, s.get_secret, service, name)
    click.echo(entry.value)


@secret.command("add", help="Add a new secret.")
@click.argument("service")
@click.argument("name")
@click.option("--value", help="Secret value; if omitted, read from stdin or prompt.")
@click.pass_context
def secret_add(ctx: click.Context, service: str, name: str, value: str | None) -> None:
    """Add a new secret.

    Args:
        service: Service name.
        name: Secret name.
        value: Optional secret value. If omitted, it is read from stdin or a
            prompt.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)

    value = read_secret_value(name, value)
    s.add_secret(service, name, value)
    click.echo(f"Added {service}:{name}")


@secret.command("update", help="Update an existing secret.")
@click.argument("service")
@click.argument("name")
@click.option("--value", help="New value; if omitted, read from stdin or prompt.")
@click.pass_context
def secret_update(ctx: click.Context, service: str, name: str, value: str | None) -> None:
    """Update the value of an existing secret.

    Args:
        service: Service name.
        name: Secret name.
        value: Optional new value. If omitted, it is read from stdin or a
            prompt.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)

    value = read_secret_value(name, value)
    s.update_secret(service, name, value)
    click.echo(f"Updated {service}:{name}")


@secret.command("rename", help="Rename a secret.")
@click.argument("service")
@click.argument("old")
@click.argument("new")
@click.pass_context
def secret_rename(ctx: click.Context, service: str, old: str, new: str) -> None:
    """Rename a secret within a service.

    Args:
        service: Service name.
        old: Existing secret name.
        new: New secret name.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)
    s.rename_secret(service, old, new)
    click.echo(f"{service}:{old} -> {service}:{new}")


@secret.command("move", help="Move a secret to another service.")
@click.argument("source")
@click.argument("name")
@click.argument("target")
@click.pass_context
def secret_move(ctx: click.Context, source: str, name: str, target: str) -> None:
    """Move a secret from one service to another.

    Args:
        source: Source service name.
        name: Secret name.
        target: Target service name.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)
    s.move_secret(source, name, target)
    click.echo(f"{source}:{name} -> {target}:{name}")


@secret.command("delete", help="Delete a secret.")
@click.argument("service")
@click.argument("name")
@click.pass_context
def secret_delete(ctx: click.Context, service: str, name: str) -> None:
    """Delete a secret from a service.

    Args:
        service: Service name.
        name: Secret name.
    """
    s = build_lbx(ctx.obj["vault_path"])
    ensure_unlocked(s)
    s.delete_secret(service, name)
    click.echo(f"Deleted {service}:{name}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Console script entry point."""
    try:
        lbx()
    except LbxError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1) from e
