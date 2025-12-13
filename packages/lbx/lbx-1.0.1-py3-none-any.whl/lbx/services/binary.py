# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""Binary serialization for Lbx vaults.

This module defines BinaryService, which is responsible for packing and
unpacking lbx.models.Vault instances to and from the binary format defined
by lbx.settings.BinaryFormat.
"""

from __future__ import annotations

import struct
from typing import cast

from lbx.exceptions import (
    InvalidVaultFileError,
    UnsupportedVersionError,
    VaultCorruptedError,
)
from lbx.models import KDFParameters, MasterKey, Secret, Service, Vault
from lbx.settings import BinaryFormat, Crypto


class BinaryService:
    """Binary format packing and unpacking.

    Instances of this class are stateful during an unpack operation. A new
    instance is used internally for unpacking nested structures (for example,
    the master key payload).
    """

    __slots__ = ("_data", "_offset", "_section")

    def __init__(self) -> None:
        """Initialize an empty BinaryService."""
        self._data: bytes = b""
        self._offset: int = 0
        self._section: str = "header"

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def pack(self, vault: Vault) -> bytes:
        """Pack a vault into the binary format.

        Args:
            vault (Vault): Vault instance to serialize.

        Returns:
            bytes: Binary representation of the vault.
        """
        # Header: MAGIC + 2-byte version
        magic = BinaryFormat.MAGIC
        header = b"".join(
            [
                magic,
                struct.pack("<H", BinaryFormat.VERSION),  # uint16 version
            ]
        )

        # Body: master key + services
        body = b"".join(
            [
                self._pack_master_key(vault.master_key),
                self._pack_services(vault.services),
            ]
        )

        return header + body

    def unpack(self, data: bytes) -> Vault:
        """Unpack a vault from the binary format.

        Args:
            data (bytes): Bytes object containing the serialized vault.

        Returns:
            Vault: Reconstructed vault instance.

        Raises:
            InvalidVaultFileError: If the file does not start with the Lbx
                magic header.
            UnsupportedVersionError: If the on-disk version does not match
                BinaryFormat.VERSION.
            VaultCorruptedError: If the file is structurally invalid or
                truncated.
        """
        magic = BinaryFormat.MAGIC
        magic_len = len(magic)
        header_len = BinaryFormat.header_size()

        if len(data) < header_len:
            raise VaultCorruptedError("File too small", section="header")

        if data[:magic_len] != magic:
            raise InvalidVaultFileError("Invalid magic header")

        # 2-byte little-endian version after MAGIC
        (version,) = struct.unpack_from("<H", data, offset=magic_len)
        if version != BinaryFormat.VERSION:
            raise UnsupportedVersionError(version)

        self._data = data
        self._offset = header_len

        self._section = "master_key"
        master_key = self._unpack_master_key()

        self._section = "services"
        services = self._unpack_services()

        # Strict: no trailing junk
        if self._offset != len(self._data):
            raise VaultCorruptedError(
                "Trailing data after vault content",
                offset=self._offset,
                section=self._section,
            )

        return Vault(master_key=master_key, services=services)

    # -------------------------------------------------------------------------
    # Packing helpers
    # -------------------------------------------------------------------------

    def _pack_master_key(self, mk: MasterKey) -> bytes:
        """Pack a master key as a length-prefixed blob.

        Layout inside the blob (little-endian)::

            [0:12]  Argon2 params: memory_cost, time_cost, parallelism (3 * uint32)
            [... ]  password_hash (length-prefixed)
            [... ]  salt (SALT_LENGTH bytes)
            [... ]  encryption_salt (SALT_LENGTH bytes)

        Args:
            mk (MasterKey): Master key instance.

        Returns:
            bytes: Serialized bytes for the master key.
        """
        kdf = mk.kdf_params
        body = b"".join(
            [
                struct.pack("<III", kdf.memory_cost, kdf.time_cost, kdf.parallelism),
                self._pack_bytes(mk.password_hash),
                mk.salt,
                mk.encryption_salt,
            ]
        )
        return self._pack_bytes(body)

    def _pack_services(self, services: dict[str, Service]) -> bytes:
        """Pack the services mapping.

        Layout::

            count   (uint32)
            repeat count times:
                name   (length-prefixed UTF-8)
                secrets (see _pack_secrets)

        Args:
            services (dict[str, Service]): Mapping of service name to Service.

        Returns:
            bytes: Serialized bytes for all services.
        """
        parts = [struct.pack("<I", len(services))]
        for service in services.values():
            parts.append(self._pack_string(service.name))
            parts.append(self._pack_secrets(service.secrets))
        return b"".join(parts)

    def _pack_secrets(self, secrets: dict[str, Secret]) -> bytes:
        """Pack the secrets mapping for a single service.

        Layout::

            count   (uint32)
            repeat count times:
                name_len     (uint32)
                cipher_len   (uint32)
                name         (name_len bytes, UTF-8)
                ciphertext   (cipher_len bytes)
                nonce        (NONCE_LENGTH bytes)

        Args:
            secrets (dict[str, Secret]): Mapping of secret name to Secret.

        Returns:
            bytes: Serialized bytes for all secrets.
        """
        parts = [struct.pack("<I", len(secrets))]
        for secret in secrets.values():
            name = secret.name.encode()
            parts.append(struct.pack("<II", len(name), len(secret.ciphertext)))
            parts.append(name)
            parts.append(secret.ciphertext)
            parts.append(secret.nonce)
        return b"".join(parts)

    @staticmethod
    def _pack_bytes(data: bytes) -> bytes:
        """Pack a bytes buffer as a length-prefixed field.

        Args:
            data (bytes): Raw bytes.

        Returns:
            bytes: Length-prefixed bytes (uint32 length + data).
        """
        return struct.pack("<I", len(data)) + data

    @staticmethod
    def _pack_string(value: str) -> bytes:
        """Pack a string as a length-prefixed UTF-8 buffer.

        Args:
            value (str): String to encode.

        Returns:
            bytes: Length-prefixed bytes (uint32 length + UTF-8 data).
        """
        encoded = value.encode()
        return struct.pack("<I", len(encoded)) + encoded

    # -------------------------------------------------------------------------
    # Unpacking helpers
    # -------------------------------------------------------------------------

    def _unpack_master_key(self) -> MasterKey:
        """Unpack the master key from the current position.

        Returns:
            MasterKey: Reconstructed master key.

        Raises:
            VaultCorruptedError: If the master key blob is truncated or
                malformed.
        """
        body = self._read_bytes_prefixed()

        inner = BinaryService()
        inner._data = body
        inner._offset = 0
        inner._section = "master_key"

        memory, time, parallelism = struct.unpack("<III", inner._read_bytes(12))
        password_hash = inner._read_bytes_prefixed()
        salt = inner._read_bytes(Crypto.SALT_LENGTH)
        encryption_salt = inner._read_bytes(Crypto.SALT_LENGTH)

        return MasterKey(
            password_hash=password_hash,
            salt=salt,
            encryption_salt=encryption_salt,
            kdf_params=KDFParameters(memory, time, parallelism),
        )

    def _unpack_services(self) -> dict[str, Service]:
        """Unpack all services from the current position.

        Returns:
            dict[str, Service]: Mapping of service name to Service.

        Raises:
            VaultCorruptedError: If the services section is truncated or
                malformed.
        """
        count = self._read_uint32()
        services: dict[str, Service] = {}

        for i in range(count):
            base_section = f"service[{i}]"
            self._section = base_section
            name = self._read_string()
            self._section = base_section
            secrets = self._unpack_secrets()
            services[name] = Service(name=name, secrets=secrets)

        return services

    def _unpack_secrets(self) -> dict[str, Secret]:
        """Unpack all secrets for the current service.

        Returns:
            dict[str, Secret]: Mapping of secret name to Secret.

        Raises:
            VaultCorruptedError: If any secret entry is truncated or malformed.
        """
        count = self._read_uint32()
        secrets: dict[str, Secret] = {}

        base_section = self._section
        for i in range(count):
            self._section = f"{base_section}.secret[{i}]"
            name_len, cipher_len = struct.unpack("<II", self._read_bytes(8))
            name = self._read_bytes(name_len).decode()
            ciphertext = self._read_bytes(cipher_len)
            nonce = self._read_bytes(Crypto.NONCE_LENGTH)
            secrets[name] = Secret(name=name, ciphertext=ciphertext, nonce=nonce)

        self._section = base_section
        return secrets

    # -------------------------------------------------------------------------
    # Low-level read helpers
    # -------------------------------------------------------------------------

    def _read_uint32(self) -> int:
        """Read a little-endian uint32 value.

        Returns:
            int: Parsed uint32 value.

        Raises:
            VaultCorruptedError: If not enough bytes remain.
        """
        data = self._read_bytes(4)
        return cast(int, struct.unpack("<I", data)[0])

    def _read_bytes(self, length: int) -> bytes:
        """Read a fixed number of bytes from the internal buffer.

        Args:
            length (int): Number of bytes to read.

        Returns:
            bytes: Requested slice of bytes.

        Raises:
            VaultCorruptedError: If fewer than ``length`` bytes remain.
        """
        available = len(self._data) - self._offset
        if available < length:
            raise VaultCorruptedError(
                f"Unexpected end of data (needed {length}, got {available})",
                offset=self._offset,
                section=self._section,
            )
        data = self._data[self._offset : self._offset + length]
        self._offset += length
        return data

    def _read_bytes_prefixed(self) -> bytes:
        """Read a length-prefixed bytes buffer.

        Returns:
            bytes: Bytes buffer that was prefixed with a uint32 length.

        Raises:
            VaultCorruptedError: If the length or data are truncated.
        """
        return self._read_bytes(self._read_uint32())

    def _read_string(self) -> str:
        """Read a length-prefixed UTF-8 string.

        Returns:
            str: Decoded string value.

        Raises:
            VaultCorruptedError: If the underlying bytes are truncated.
            UnicodeDecodeError: If the bytes are not valid UTF-8.
        """
        return self._read_bytes_prefixed().decode()
