# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""Global configuration for Lbx.

This module defines:

* BinaryFormat: On-disk vault format layout and versioning.
* Crypto: Cryptographic parameter defaults for AES-256-GCM and Argon2id.
"""

from __future__ import annotations

from pathlib import Path


class BinaryFormat:
    """Vault file binary format specification.

    Layout (little-endian)::

        MAGIC   (len(MAGIC) bytes)
        VERSION (2 bytes, unsigned integer)
        BODY    (master key + services)

    The BODY structure is defined by `lbx.services.binary.BinaryService`.

    Attributes:
        MAGIC (bytes): File magic prefix used to identify Lbx vaults.
        VERSION (int): Format version stored as a uint16.
    """

    __slots__ = ()

    MAGIC: bytes = b"LBX"
    VERSION: int = 1

    @classmethod
    def header_size(cls) -> int:
        """Return the size of the fixed header.

        Returns:
            int: Header size in bytes (MAGIC + 2-byte version).
        """
        return len(cls.MAGIC) + 2


class Crypto:
    """Cryptographic parameters (AES-256-GCM + Argon2id).

    Attributes:
        KEY_LENGTH (int): AES-256 key size in bytes.
        NONCE_LENGTH (int): AES-GCM nonce length in bytes.
        TAG_LENGTH (int): AES-GCM tag length in bytes.
        SALT_LENGTH (int): Salt size in bytes for Argon2id.
        ARGON2_MEMORY (int): Argon2 memory cost in KiB.
        ARGON2_TIME (int): Argon2 time cost (iterations).
        ARGON2_PARALLELISM (int): Argon2 parallelism (lanes).
    """

    __slots__ = ()

    # AES-256-GCM
    KEY_LENGTH: int = 32
    NONCE_LENGTH: int = 12
    TAG_LENGTH: int = 16
    SALT_LENGTH: int = 32

    # Argon2id (OWASP-style defaults; adjust as needed for environment)
    ARGON2_MEMORY: int = 65_536
    ARGON2_TIME: int = 3
    ARGON2_PARALLELISM: int = 4


#: Default directory used when no explicit vault path is provided.
DEFAULT_DIR: Path = Path.home() / ".lbx"

#: Default vault file name used when no explicit name is provided.
DEFAULT_NAME: str = "vault.lbx"


def default_vault_path() -> Path:
    """Return the default vault path.

    Returns:
        Path: Default vault file path, for example ``~/.lbx/vault.lbx``.
    """
    return DEFAULT_DIR / DEFAULT_NAME
