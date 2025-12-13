# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""OS keychain integration for Lbx.

This module provides KeyringService for storing the symmetric encryption key
in the operating system keychain via the `keyring` library.
"""

from __future__ import annotations

import base64

import keyring
from keyring.errors import KeyringError, KeyringLocked, NoKeyringError, PasswordDeleteError

from lbx.exceptions import (
    KeychainAccessError,
    KeychainDataError,
    KeychainNotAvailableError,
    KeyNotFoundError,
)
from lbx.settings import Crypto


class KeyringService:
    """OS keychain operations for encryption key storage.

    The key is stored as a base64-encoded string under a given service and
    account name in the system keyring.

    Attributes:
        DEFAULT_SERVICE (str): Default keyring service name.
        DEFAULT_ACCOUNT (str): Default keyring account name.
    """

    __slots__ = ("_account", "_service")

    DEFAULT_SERVICE = "lbx"
    DEFAULT_ACCOUNT = "master_key"

    def __init__(
        self,
        service: str = DEFAULT_SERVICE,
        account: str = DEFAULT_ACCOUNT,
    ) -> None:
        """Initialize a KeyringService.

        Args:
            service (str): Service name used by the OS keychain.
            account (str): Account name used by the OS keychain.
        """
        self._service = service
        self._account = account

    @property
    def service(self) -> str:
        """Return the keyring service name.

        Returns:
            str: Keyring service name.
        """
        return self._service

    @property
    def account(self) -> str:
        """Return the keyring account name.

        Returns:
            str: Keyring account name.
        """
        return self._account

    def store(self, key: bytes) -> None:
        """Store the encryption key in the OS keychain.

        The key is base64-encoded to store it as a text password.

        Args:
            key (bytes): Raw encryption key bytes. Must be `Crypto.KEY_LENGTH`
                bytes long.

        Raises:
            KeychainDataError: If the key length is invalid.
            KeychainNotAvailableError: If no keyring backend is available.
            KeychainAccessError: If the keychain is locked, access is denied,
                or another keyring error occurs.
        """
        if len(key) != Crypto.KEY_LENGTH:
            raise KeychainDataError(f"Invalid key length: expected {Crypto.KEY_LENGTH} bytes, got {len(key)}")

        try:
            encoded = base64.b64encode(key).decode("ascii")
            keyring.set_password(self._service, self._account, encoded)
        except NoKeyringError as e:
            raise KeychainNotAvailableError from e
        except KeyringLocked as e:
            raise KeychainAccessError("store", "keychain is locked") from e
        except PermissionError as e:
            raise KeychainAccessError("store", "permission denied") from e
        except KeyringError as e:
            raise KeychainAccessError("store", str(e)) from e

    def retrieve(self) -> bytes:
        """Retrieve the encryption key from the OS keychain.

        Returns:
            bytes: Raw encryption key bytes.

        Raises:
            KeyNotFoundError: If no entry exists for the configured
                service/account.
            KeychainDataError: If the stored data is not valid base64 or the
                decoded key has an unexpected length.
            KeychainNotAvailableError: If no keyring backend is available.
            KeychainAccessError: If the keychain is locked, access is denied,
                or another keyring error occurs.
        """
        try:
            encoded = keyring.get_password(self._service, self._account)
            if encoded is None:
                raise KeyNotFoundError(self._service, self._account)

            try:
                key = base64.b64decode(encoded, validate=True)
            except ValueError as e:
                raise KeychainDataError(f"Corrupted key data in keychain: {e}") from e

            if len(key) != Crypto.KEY_LENGTH:
                raise KeychainDataError(
                    f"Invalid key length in keychain: expected {Crypto.KEY_LENGTH} bytes, got {len(key)}"
                )

            return key
        except (KeyNotFoundError, KeychainDataError):
            # Preserve the specific meaning for "no key" and "bad key data".
            raise
        except NoKeyringError as e:
            raise KeychainNotAvailableError from e
        except KeyringLocked as e:
            raise KeychainAccessError("retrieve", "keychain is locked") from e
        except PermissionError as e:
            raise KeychainAccessError("retrieve", "permission denied") from e
        except KeyringError as e:
            raise KeychainAccessError("retrieve", str(e)) from e

    def delete(self) -> None:
        """Delete the encryption key from the OS keychain.

        Raises:
            KeyNotFoundError: If no entry exists for the configured
                service/account.
            KeychainNotAvailableError: If no keyring backend is available.
            KeychainAccessError: If the keychain is locked, access is denied,
                or another keyring error occurs.
        """
        try:
            keyring.delete_password(self._service, self._account)
        except PasswordDeleteError as e:
            raise KeyNotFoundError(self._service, self._account) from e
        except NoKeyringError as e:
            raise KeychainNotAvailableError from e
        except KeyringLocked as e:
            raise KeychainAccessError("delete", "keychain is locked") from e
        except PermissionError as e:
            raise KeychainAccessError("delete", "permission denied") from e
        except KeyringError as e:
            raise KeychainAccessError("delete", str(e)) from e

    def exists(self) -> bool:
        """Check whether a key exists in the OS keychain.

        Returns:
            bool: True if an entry exists for the configured service/account,
            False if no entry exists or the keyring is unavailable.

        Note:
            This method swallows keyring backend errors and returns False
            in that case. Use `retrieve` if you need detailed error
            information.
        """
        try:
            password = keyring.get_password(self._service, self._account)
            return password is not None
        except (NoKeyringError, KeyringError):
            return False
