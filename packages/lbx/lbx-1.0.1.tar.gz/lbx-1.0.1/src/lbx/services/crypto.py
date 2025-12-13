# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""Cryptographic operations for Lbx.

This module provides CryptoService, which encapsulates:

* AES-256-GCM encryption and decryption of secrets.
* Argon2id-based key derivation from a password.
* Creation and verification of the master key.
"""

from __future__ import annotations

import hmac
import os

from argon2.low_level import Type, hash_secret_raw
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from lbx.exceptions import DecryptionError, EncryptionError, InvalidPasswordError
from lbx.models import KDFParameters, MasterKey, Secret
from lbx.settings import Crypto


class CryptoService:
    """Cryptographic operations for vault encryption."""

    __slots__ = ("_cipher", "_key")

    def __init__(self, key: bytes | None = None) -> None:
        """Initialize the CryptoService.

        Args:
            key (bytes | None): Optional AES-256 key. If provided, an AESGCM
                instance is created immediately; otherwise, `set_key` must be
                called before encrypting or decrypting.
        """
        self._key = key
        self._cipher = AESGCM(key) if key else None

    @property
    def key(self) -> bytes | None:
        """Get the current AES key.

        Returns:
            bytes | None: Active key bytes, or None if no key is set.
        """
        return self._key

    def set_key(self, key: bytes) -> None:
        """Set the AES encryption key.

        Args:
            key (bytes): Key bytes. Must be `Crypto.KEY_LENGTH` bytes long.

        Raises:
            EncryptionError: If the key length is invalid.
        """
        if len(key) != Crypto.KEY_LENGTH:
            raise EncryptionError(f"Key must be {Crypto.KEY_LENGTH} bytes")
        self._key = key
        self._cipher = AESGCM(key)

    def clear_key(self) -> None:
        """Clear the AES encryption key from memory.

        Sets both the internal key reference and the AESGCM cipher to None.
        This does not guarantee secure memory wiping but avoids accidental
        reuse.
        """
        self._key = None
        self._cipher = None

    def encrypt(self, name: str, value: str) -> Secret:
        """Encrypt a secret value.

        Args:
            name (str): Logical name of the secret (for example, "token",
                "password").
            value (str): Plaintext value to encrypt.

        Returns:
            Secret: Encrypted secret containing ciphertext and nonce.

        Raises:
            EncryptionError: If the key is not set, inputs are invalid, or
                encryption fails.
        """
        if not name:
            raise EncryptionError("Secret name cannot be empty")

        if not value:
            raise EncryptionError("Secret value cannot be empty")

        if self._cipher is None:
            raise EncryptionError("Encryption key not set")

        try:
            nonce = os.urandom(Crypto.NONCE_LENGTH)
            ciphertext = self._cipher.encrypt(nonce, value.encode(), None)
            return Secret(name=name, ciphertext=ciphertext, nonce=nonce)
        except Exception as e:  # pragma: no cover (defensive catch-all)
            raise EncryptionError(f"Encryption failed: {e}") from e

    def decrypt(self, secret: Secret) -> str:
        """Decrypt a secret value.

        Args:
            secret (Secret): Secret instance to decrypt.

        Returns:
            str: Decrypted plaintext string.

        Raises:
            DecryptionError: If the key is not set, the authentication tag
                is invalid, plaintext cannot be decoded, or decryption fails.
        """
        if self._cipher is None:
            raise DecryptionError("Encryption key not set")

        try:
            plaintext = self._cipher.decrypt(secret.nonce, secret.ciphertext, None)
            return plaintext.decode()
        except InvalidTag as e:
            raise DecryptionError("Data corrupted or wrong key") from e
        except UnicodeDecodeError as e:
            raise DecryptionError("Invalid data encoding") from e
        except Exception as e:  # pragma: no cover
            raise DecryptionError(f"Decryption failed: {e}") from e

    @staticmethod
    def generate_salt() -> bytes:
        """Generate a random salt.

        Returns:
            bytes: Random salt of length `Crypto.SALT_LENGTH`.
        """
        return os.urandom(Crypto.SALT_LENGTH)

    @staticmethod
    def derive_key(password: str, salt: bytes, params: KDFParameters) -> bytes:
        """Derive a key from a password using Argon2id.

        Args:
            password (str): Password string.
            salt (bytes): Salt bytes. Must be `Crypto.SALT_LENGTH` bytes long.
            params (KDFParameters): Argon2id parameters.

        Returns:
            bytes: Derived key bytes of length `Crypto.KEY_LENGTH`.

        Raises:
            EncryptionError: If the salt length is invalid or key derivation
                fails.
        """
        if len(salt) != Crypto.SALT_LENGTH:
            raise EncryptionError(f"Salt must be {Crypto.SALT_LENGTH} bytes")

        try:
            return hash_secret_raw(
                secret=password.encode(),
                salt=salt,
                time_cost=params.time_cost,
                memory_cost=params.memory_cost,
                parallelism=params.parallelism,
                hash_len=Crypto.KEY_LENGTH,
                type=Type.ID,
            )
        except Exception as e:  # pragma: no cover
            raise EncryptionError(f"Key derivation failed: {e}") from e

    @staticmethod
    def create_master_key(password: str) -> tuple[MasterKey, bytes]:
        """Create a new master key from a password.

        Derives both a password hash and a separate encryption key from the
        password using two independent salts.

        Args:
            password (str): Password string. Must not be empty.

        Returns:
            tuple[MasterKey, bytes]: Tuple of:

                * MasterKey: Master key for storage in the vault.
                * bytes: Encryption key for immediate use.

        Raises:
            InvalidPasswordError: If the password is empty.
            EncryptionError: If key derivation fails.
        """
        if not password:
            raise InvalidPasswordError("Password cannot be empty")

        params = KDFParameters()
        salt = CryptoService.generate_salt()
        encryption_salt = CryptoService.generate_salt()

        password_hash = CryptoService.derive_key(password, salt, params)
        encryption_key = CryptoService.derive_key(password, encryption_salt, params)

        master_key = MasterKey(
            password_hash=password_hash,
            salt=salt,
            encryption_salt=encryption_salt,
            kdf_params=params,
        )

        return master_key, encryption_key

    @staticmethod
    def verify_password(password: str, master_key: MasterKey) -> bytes:
        """Verify a password against a stored master key.

        On success, returns the derived encryption key.

        Args:
            password (str): Password string to verify.
            master_key (MasterKey): Stored master key configuration.

        Returns:
            bytes: Derived encryption key bytes.

        Raises:
            InvalidPasswordError: If the password is empty or incorrect.
            EncryptionError: If key derivation fails.
        """
        if not password:
            raise InvalidPasswordError("Password cannot be empty")

        computed_hash = CryptoService.derive_key(
            password,
            master_key.salt,
            master_key.kdf_params,
        )

        if not hmac.compare_digest(computed_hash, master_key.password_hash):
            raise InvalidPasswordError("Incorrect password")

        return CryptoService.derive_key(
            password,
            master_key.encryption_salt,
            master_key.kdf_params,
        )
