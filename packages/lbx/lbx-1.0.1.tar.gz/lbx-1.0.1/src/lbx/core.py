# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT
"""Core vault operations for Lbx.

This module provides the Lbx class, which acts as the high-level vault
manager. It coordinates:

* BinaryService for (de)serialization.
* CryptoService for encryption and key derivation.
* FileService for vault file I/O.
* KeyringService for storing the encryption key in the OS keychain.

By default, the derived encryption key is stored in the OS keychain whenever
a vault is created or unlocked. This can be disabled via the ``use_keychain``
flag for programmatic or test use.
"""

from __future__ import annotations

from pathlib import Path

from lbx.exceptions import (
    SecretExistsError,
    SecretNotFoundError,
    ServiceExistsError,
    ServiceNotFoundError,
    VaultExistsError,
    VaultLockedError,
    VaultNotFoundError,
)
from lbx.models import Secret as SecretModel
from lbx.models import SecretEntry, Service, Vault
from lbx.services import BinaryService, CryptoService, FileService, KeyringService


class Lbx:
    """High-level vault manager.

    This class provides the main API for working with an Lbx vault:
    creating, unlocking, locking, deleting, and managing services and
    secrets. It composes the service layer into a single cohesive interface.

    By default, the derived encryption key is stored in the OS keychain
    whenever a vault is created or unlocked. This can be controlled via the
    ``use_keychain`` flag.
    """

    __slots__ = (
        "_binary",
        "_crypto",
        "_file",
        "_keyring",
        "_use_keychain",
        "_vault",
    )

    def __init__(  # noqa: PLR0913
        self,
        path: Path | str | None = None,
        *,
        use_keychain: bool = True,
        binary_service: BinaryService | None = None,
        file_service: FileService | None = None,
        keyring_service: KeyringService | None = None,
        crypto_service: CryptoService | None = None,
    ) -> None:
        """Initialize the Lbx vault manager.

        Args:
            path (Path | str | None): Optional path to the vault file. If
                None, the default vault path (as determined by FileService)
                is used.
            use_keychain (bool): Whether to store the derived encryption key
                in the OS keychain when creating or unlocking the vault.
            binary_service (BinaryService | None): Optional preconfigured
                BinaryService instance.
            file_service (FileService | None): Optional preconfigured
                FileService instance.
            keyring_service (KeyringService | None): Optional preconfigured
                KeyringService instance.
            crypto_service (CryptoService | None): Optional preconfigured
                CryptoService instance.
        """
        self._binary: BinaryService = binary_service or BinaryService()
        self._file: FileService = file_service or FileService(path)
        self._keyring: KeyringService = keyring_service or KeyringService()
        self._crypto: CryptoService = crypto_service or CryptoService()
        self._vault: Vault | None = None
        self._use_keychain: bool = use_keychain

    # ----------------------------------------------------------------------
    # Properties
    # ----------------------------------------------------------------------

    @property
    def is_unlocked(self) -> bool:
        """Whether the vault is currently unlocked.

        Returns:
            bool: True if an encryption key is loaded in memory, False
            otherwise.
        """
        return self._crypto.key is not None

    @property
    def path(self) -> Path:
        """Path to the vault file on disk.

        Returns:
            Path: Vault file path.
        """
        return self._file.path

    # ----------------------------------------------------------------------
    # Vault lifecycle
    # ----------------------------------------------------------------------

    def exists(self) -> bool:
        """Check whether the vault file exists.

        Returns:
            bool: True if the vault file exists, False otherwise.
        """
        return self._file.exists()

    def create(self, password: str) -> None:
        """Create a new vault.

        This method:

        * Fails if a vault file already exists.
        * Derives a master key and encryption key from the password.
        * Persists the vault to disk.
        * Stores the encryption key in the OS keychain if ``use_keychain``
          is True.

        Args:
            password (str): Password to derive the master and encryption keys.

        Raises:
            VaultExistsError: If a vault file already exists at the
                configured path.
            InvalidPasswordError: If the password is empty (raised by
                CryptoService).
            EncryptionError: If key derivation or encryption fails.
        """
        if self._file.exists():
            raise VaultExistsError("Vault already exists")

        master_key, key = CryptoService.create_master_key(password)
        self._vault = Vault(master_key=master_key)
        self._crypto.set_key(key)
        self._save()

        if self._use_keychain:
            self._keyring.store(key)

    def unlock(self, password: str) -> None:
        """Unlock an existing vault using a password.

        This method:

        * Loads the vault from disk.
        * Verifies the password against the stored master key.
        * Derives and sets the encryption key.
        * Stores the encryption key in the OS keychain if ``use_keychain``
          is True.

        Args:
            password (str): Password to verify and derive the encryption key.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
            InvalidPasswordError: If the password is empty or incorrect.
            EncryptionError: If key derivation fails.
        """
        self._load()

        vault = self._require_vault()
        key = CryptoService.verify_password(password, vault.master_key)
        self._crypto.set_key(key)

        if self._use_keychain:
            self._keyring.store(key)

    def unlock_from_keychain(self) -> bool:
        """Unlock the vault using the OS keychain.

        This method attempts to:

        * Load the vault from disk.
        * Retrieve the encryption key from the OS keychain.
        * Set the encryption key in memory.

        Returns:
            bool: True if the key was found and the vault was unlocked,
            False if no key exists in the keychain for this service/account.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
            KeychainNotAvailableError: If the OS keychain is not available.
            KeychainAccessError: If the keychain is locked or access is
                denied.
            KeychainDataError: If the stored key data is invalid.
        """
        if not self._keyring.exists():
            return False

        self._load()
        key = self._keyring.retrieve()
        self._crypto.set_key(key)
        return True

    def lock(self) -> None:
        """Lock the vault and clear the encryption key from memory."""
        self._crypto.clear_key()

    def lock_and_forget(self) -> None:
        """Lock the vault and remove the key from the OS keychain.

        This clears the in-memory key and deletes the key from the keychain.
        """
        self._crypto.clear_key()
        self._keyring.delete()

    def delete_vault(self) -> None:
        """Delete the vault file and any stored keychain entry.

        After this operation, the in-memory vault is also cleared.
        """
        self._file.delete()
        self._keyring.delete()
        self._vault = None
        self._crypto.clear_key()

    # ----------------------------------------------------------------------
    # Services
    # ----------------------------------------------------------------------

    def list_services(self) -> list[str]:
        """List all service names in the vault.

        Returns:
            list[str]: List of service names.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
        """
        self._ensure_loaded()
        vault = self._require_vault()
        return list(vault.services.keys())

    def has_service(self, service: str) -> bool:
        """Check whether a service exists.

        Args:
            service (str): Service name to check.

        Returns:
            bool: True if the service exists, False otherwise.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
        """
        self._ensure_loaded()
        vault = self._require_vault()
        return service in vault.services

    def delete_service(self, service: str) -> None:
        """Delete a service and all its secrets.

        Args:
            service (str): Name of the service to delete.

        Raises:
            ServiceNotFoundError: If the service does not exist.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        if service not in vault.services:
            raise ServiceNotFoundError(f"Service not found: {service}")

        del vault.services[service]
        self._save()

    def rename_service(self, old_name: str, new_name: str) -> None:
        """Rename a service.

        Args:
            old_name (str): Existing service name.
            new_name (str): New service name.

        Raises:
            ServiceNotFoundError: If ``old_name`` does not exist.
            ServiceExistsError: If ``new_name`` already exists.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        svc = vault.services.get(old_name)
        if svc is None:
            raise ServiceNotFoundError(f"Service not found: {old_name}")

        if new_name in vault.services:
            raise ServiceExistsError(f"Service already exists: {new_name}")

        del vault.services[old_name]
        svc.name = new_name
        vault.services[new_name] = svc
        self._save()

    # ----------------------------------------------------------------------
    # Secrets
    # ----------------------------------------------------------------------

    def list_secrets(self, service: str | None = None) -> list[tuple[str, str]]:
        """List secrets, optionally filtered by service.

        Args:
            service (str | None): Optional service name. If provided,
                only secrets for that service are listed. If None, all
                secrets in the vault are listed.

        Returns:
            list[tuple[str, str]]: List of (service_name, secret_name)
            tuples.

        Raises:
            ServiceNotFoundError: If a specific service is requested but
                does not exist.
            VaultNotFoundError: If the vault file does not exist.
        """
        self._ensure_loaded()
        vault = self._require_vault()

        if service is not None:
            svc = vault.services.get(service)
            if svc is None:
                raise ServiceNotFoundError(f"Service not found: {service}")
            return [(service, name) for name in svc.secrets]

        return [(svc.name, name) for svc in vault.services.values() for name in svc.secrets]

    def has_secret(self, service: str, name: str) -> bool:
        """Check whether a secret exists.

        Args:
            service (str): Service name.
            name (str): Secret name.

        Returns:
            bool: True if the secret exists, False otherwise.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
        """
        self._ensure_loaded()
        vault = self._require_vault()

        svc = vault.services.get(service)
        if svc is None:
            return False

        return name in svc.secrets

    def get_secret(self, service: str, name: str) -> SecretEntry:
        """Get a decrypted secret.

        Args:
            service (str): Service name.
            name (str): Secret name.

        Returns:
            SecretEntry: Decrypted secret entry.

        Raises:
            ServiceNotFoundError: If the service does not exist.
            SecretNotFoundError: If the secret does not exist.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        svc = vault.services.get(service)
        if svc is None:
            raise ServiceNotFoundError(f"Service not found: {service}")

        secret = svc.secrets.get(name)
        if secret is None:
            raise SecretNotFoundError(f"Secret not found: {name}")

        value = self._crypto.decrypt(secret)
        return SecretEntry(service=service, name=name, value=value)

    def add_secret(self, service: str, name: str, value: str) -> None:
        """Add a new secret.

        If the service does not exist, it is created. If the secret already
        exists in that service, a SecretExistsError is raised.

        Args:
            service (str): Service name.
            name (str): Secret name.
            value (str): Secret plaintext value.

        Raises:
            SecretExistsError: If the secret already exists in the service.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        svc = vault.services.get(service)
        if svc is None:
            svc = Service(name=service)
            vault.services[service] = svc

        if name in svc.secrets:
            raise SecretExistsError(f"Secret already exists: service={service!r}, name={name!r}")

        secret = self._crypto.encrypt(name, value)
        svc.secrets[name] = secret
        self._save()

    def update_secret(self, service: str, name: str, value: str) -> None:
        """Update an existing secret.

        Args:
            service (str): Service name.
            name (str): Secret name.
            value (str): New plaintext value.

        Raises:
            ServiceNotFoundError: If the service does not exist.
            SecretNotFoundError: If the secret does not exist.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        svc = vault.services.get(service)
        if svc is None:
            raise ServiceNotFoundError(f"Service not found: {service}")

        if name not in svc.secrets:
            raise SecretNotFoundError(f"Secret not found: {name}")

        secret = self._crypto.encrypt(name, value)
        svc.secrets[name] = secret
        self._save()

    def rename_secret(self, service: str, old_name: str, new_name: str) -> None:
        """Rename a secret within a service.

        Args:
            service (str): Service name.
            old_name (str): Existing secret name.
            new_name (str): New secret name.

        Raises:
            ServiceNotFoundError: If the service does not exist.
            SecretNotFoundError: If ``old_name`` does not exist.
            SecretExistsError: If ``new_name`` already exists in the service.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        svc = vault.services.get(service)
        if svc is None:
            raise ServiceNotFoundError(f"Service not found: {service}")

        secret = svc.secrets.get(old_name)
        if secret is None:
            raise SecretNotFoundError(f"Secret not found: {old_name}")

        if new_name in svc.secrets:
            raise SecretExistsError(f"Secret already exists: service={service!r}, name={new_name!r}")

        new_secret = SecretModel(
            name=new_name,
            ciphertext=secret.ciphertext,
            nonce=secret.nonce,
        )

        del svc.secrets[old_name]
        svc.secrets[new_name] = new_secret
        self._save()

    def move_secret(self, source_service: str, name: str, target_service: str) -> None:
        """Move a secret from one service to another.

        The secret keeps the same name in the target service.

        Args:
            source_service (str): Name of the source service.
            name (str): Secret name.
            target_service (str): Name of the target service.

        Raises:
            ServiceNotFoundError: If the source service does not exist.
            SecretNotFoundError: If the secret does not exist in the source.
            SecretExistsError: If the target already has a secret with the
                same name.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        src = vault.services.get(source_service)
        if src is None:
            raise ServiceNotFoundError(f"Service not found: {source_service}")

        secret = src.secrets.get(name)
        if secret is None:
            raise SecretNotFoundError(f"Secret not found: {name}")

        dst = vault.services.get(target_service)
        if dst is None:
            dst = Service(name=target_service)
            vault.services[target_service] = dst

        if name in dst.secrets:
            raise SecretExistsError(f"Secret already exists: service={target_service!r}, name={name!r}")

        del src.secrets[name]
        dst.secrets[name] = secret

        if not src.secrets:
            del vault.services[source_service]

        self._save()

    def delete_secret(self, service: str, name: str) -> None:
        """Delete a secret.

        If the service becomes empty after deletion, it is removed.

        Args:
            service (str): Service name.
            name (str): Secret name.

        Raises:
            ServiceNotFoundError: If the service does not exist.
            SecretNotFoundError: If the secret does not exist.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_unlocked()
        vault = self._require_vault()

        svc = vault.services.get(service)
        if svc is None:
            raise ServiceNotFoundError(f"Service not found: {service}")

        if name not in svc.secrets:
            raise SecretNotFoundError(f"Secret not found: {name}")

        del svc.secrets[name]

        if not svc.secrets:
            del vault.services[service]

        self._save()

    # ----------------------------------------------------------------------
    # Internal helpers
    # ----------------------------------------------------------------------

    def _require_vault(self) -> Vault:
        """Return the loaded vault or raise an error.

        Returns:
            Vault: Loaded vault instance.

        Raises:
            VaultNotFoundError: If no vault is loaded in memory.
        """
        if self._vault is None:
            raise VaultNotFoundError("Vault is not loaded")
        return self._vault

    def _ensure_loaded(self) -> None:
        """Ensure that the vault is loaded into memory.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
        """
        if self._vault is None:
            self._load()

    def _ensure_unlocked(self) -> None:
        """Ensure that the vault is loaded and unlocked.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
            VaultLockedError: If the vault is locked.
        """
        self._ensure_loaded()

        if not self.is_unlocked:
            raise VaultLockedError("Vault is locked")

    def _load(self) -> None:
        """Load the vault from disk.

        Raises:
            VaultNotFoundError: If the vault file does not exist.
            VaultCorruptedError: If the vault file is structurally invalid.
        """
        if not self._file.exists():
            raise VaultNotFoundError(f"Vault not found: {self._file.path}")

        data = self._file.read()
        self._vault = self._binary.unpack(data)

    def _save(self) -> None:
        """Save the current vault state to disk.

        Raises:
            VaultNotFoundError: If there is no vault loaded in memory.
        """
        vault = self._require_vault()
        data = self._binary.pack(vault)
        self._file.write(data)
