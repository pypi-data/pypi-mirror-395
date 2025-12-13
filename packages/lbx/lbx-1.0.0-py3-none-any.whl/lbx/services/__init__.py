# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""Service layer for Lbx.

This package exposes the core service classes used internally and externally
by the Lbx library:

* BinaryService: Serialize and deserialize vaults to the on-disk binary
  format defined in `lbx.settings.BinaryFormat`.
* CryptoService: Cryptographic operations (AES-256-GCM + Argon2id) for
  encrypting secrets and deriving keys from passwords.
* FileService: Filesystem interactions for reading, writing, and deleting
  vault files safely and atomically.
* KeyringService: Integration with the OS keychain for securely storing the
  derived encryption key.

These services form the core operational layer of Lbx. Higher-level APIs or
CLI tools should build on top of these abstractions.
"""

from __future__ import annotations

from lbx.services.binary import BinaryService
from lbx.services.crypto import CryptoService
from lbx.services.file import FileService
from lbx.services.key_ring import KeyringService

__all__ = [
    "BinaryService",
    "CryptoService",
    "FileService",
    "KeyringService",
]
