# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""Exception hierarchy for Lbx.

All library-specific exceptions derive from `LbxError`. Catch this base class
if you want to handle all library errors in one place.
"""

from __future__ import annotations


class LbxError(Exception):
    """Base class for all Lbx-specific errors."""


class InvalidVaultFileError(LbxError):
    """File is not a valid Lbx vault.

    This usually means the magic header does not match `BinaryFormat.MAGIC`,
    or the file is not an Lbx vault at all.

    Args:
        message (str | None): Optional custom error message.
    """

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or "Invalid Lbx vault file")


class UnsupportedVersionError(LbxError):
    """Vault version is not supported by this build.

    Args:
        version (int): Version number found in the vault file.
    """

    def __init__(self, version: int) -> None:
        self.version = version
        super().__init__(f"Unsupported vault version: {version}")


class VaultCorruptedError(LbxError):
    """Vault file is truncated or structurally inconsistent.

    This indicates that the file appears to be an Lbx vault (magic matches)
    but internal structure or lengths are invalid.

    Common causes:
        * Length-prefixed blocks exceed available bytes.
        * Reads attempt to go past the end of the buffer.
        * Sections are incomplete or malformed.

    Args:
        message (str): Human-readable description of the corruption.
        offset (int | None, optional): Byte offset where the error was
            detected.
        section (str | None, optional): Logical section name.
    """

    def __init__(
        self,
        message: str,
        *,
        offset: int | None = None,
        section: str | None = None,
    ) -> None:
        self.offset = offset
        self.section = section

        details: list[str] = []
        if section is not None:
            details.append(f"section={section}")
        if offset is not None:
            details.append(f"offset={offset}")

        full_message = f"{message} ({', '.join(details)})" if details else message
        super().__init__(full_message)


class EncryptionError(LbxError):
    """Symmetric encryption or key-derivation error.

    Raised when:
        * The encryption key is invalid or not set.
        * Encryption or key derivation fails.
    """


class DecryptionError(LbxError):
    """Symmetric decryption error.

    Raised when:
        * The decryption key is invalid or not set.
        * The authentication tag is invalid.
        * The decrypted plaintext cannot be decoded.
    """


class InvalidPasswordError(LbxError):
    """Password-related error.

    Raised when:
        * The password is empty where required.
        * The password does not match the stored master key.
    """


class VaultNotFoundError(LbxError):
    """Vault file does not exist.

    Args:
        path (str): Path to the missing vault file.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"Vault file not found: {path}")


class VaultIOError(LbxError):
    """Filesystem I/O error related to vault operations.

    Wraps lower-level OS and pathlib errors for consistency.

    Args:
        operation (str): Operation being performed (e.g., "read", "write").
        path (str): Filesystem path involved.
        reason (str): Human-readable description of the failure.
    """

    def __init__(self, operation: str, path: str, reason: str) -> None:
        self.operation = operation
        self.path = path
        self.reason = reason
        message = f"Vault I/O error during {operation!r} on {path}: {reason}"
        super().__init__(message)


class KeychainNotAvailableError(LbxError):
    """System keychain is not available.

    Raised when the keyring backend cannot be found or initialized.
    """

    def __init__(self) -> None:
        super().__init__("OS keychain is not available")


class KeychainAccessError(LbxError):
    """System keychain access error.

    Args:
        operation (str): Operation being performed (e.g., "store", "retrieve").
        reason (str): Reason for the failure (e.g., "permission denied").
    """

    def __init__(self, operation: str, reason: str) -> None:
        self.operation = operation
        self.reason = reason
        message = f"Keychain access error during {operation!r}: {reason}"
        super().__init__(message)


class KeychainDataError(LbxError):
    """Invalid or corrupted data in the system keychain.

    Raised when stored key data cannot be parsed or has unexpected format.
    """


class KeyNotFoundError(LbxError):
    """Key not found in the system keychain.

    Args:
        service (str): Keyring service name.
        account (str): Keyring account name.
    """

    def __init__(self, service: str, account: str) -> None:
        self.service = service
        self.account = account
        super().__init__(f"Key not found in keychain: service={service!r}, account={account!r}")


class VaultExistsError(LbxError):
    """Vault already exists at the target path."""


class VaultLockedError(LbxError):
    """Operation requires an unlocked vault, but the vault is locked."""


class ServiceNotFoundError(LbxError):
    """Service does not exist in the vault."""


class SecretNotFoundError(LbxError):
    """Secret does not exist within the given service."""


class ServiceExistsError(LbxError):
    """Service already exists in the vault."""


class SecretExistsError(LbxError):
    """Secret already exists within the given service."""
