# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""Core data models for the Lbx vault.

These models describe the in-memory structure used by the vault system.
They are intentionally minimal and avoid exposing sensitive values.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from lbx.settings import Crypto


@dataclass(frozen=True, slots=True)
class KDFParameters:
    """Argon2id key derivation parameters.

    Defaults follow the values configured in `lbx.settings.Crypto`.

    Attributes:
        memory_cost (int): Memory cost in KiB.
        time_cost (int): Number of iterations.
        parallelism (int): Number of parallel lanes.
    """

    memory_cost: int = Crypto.ARGON2_MEMORY
    time_cost: int = Crypto.ARGON2_TIME
    parallelism: int = Crypto.ARGON2_PARALLELISM


@dataclass(frozen=True, slots=True)
class MasterKey:
    """Master key configuration.

    Holds information needed to verify a password and derive encryption keys.
    Sensitive bytes are redacted in `repr()`.

    Attributes:
        password_hash (bytes): Derived password hash.
        salt (bytes): Salt used for password hash derivation.
        encryption_salt (bytes): Salt used for encryption key derivation.
        kdf_params (KDFParameters): Argon2id parameters for derivation.
    """

    password_hash: bytes = field(repr=False)
    salt: bytes = field(repr=False)
    encryption_salt: bytes = field(repr=False)
    kdf_params: KDFParameters = field(default_factory=KDFParameters, repr=False)

    def __repr__(self) -> str:
        return "MasterKey(<redacted>)"


@dataclass(frozen=True, slots=True)
class Secret:
    """Encrypted secret (AES-256-GCM).

    The ciphertext includes both the encrypted payload and the GCM
    authentication tag.

    Attributes:
        name (str): Logical secret name.
        ciphertext (bytes): Ciphertext bytes (ciphertext || tag).
        nonce (bytes): Per-encryption nonce used with AES-GCM.
    """

    name: str
    ciphertext: bytes = field(repr=False)
    nonce: bytes = field(repr=False)

    def __repr__(self) -> str:
        return f"Secret({self.name!r})"


@dataclass(slots=True)
class Service:
    """Logical grouping of related secrets.

    Attributes:
        name (str): Service name.
        secrets (dict[str, Secret]): Mapping of secret name to Secret.
    """

    name: str
    secrets: dict[str, Secret] = field(default_factory=dict)


@dataclass(slots=True)
class Vault:
    """Top-level vault container.

    Attributes:
        master_key (MasterKey): Vault master key configuration.
        services (dict[str, Service]): Mapping of service name to Service.
    """

    master_key: MasterKey
    services: dict[str, Service] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class SecretEntry:
    """Decrypted secret entry for in-memory use only.

    Plaintext must never be persisted or logged.

    Attributes:
        service (str): Service name the secret belongs to.
        name (str): Secret name within the service.
        value (str): Decrypted plaintext value (redacted in repr).
    """

    service: str
    name: str
    value: str = field(repr=False)

    def __repr__(self) -> str:
        return f"SecretEntry(service={self.service!r}, name={self.name!r}, value=<redacted>)"
