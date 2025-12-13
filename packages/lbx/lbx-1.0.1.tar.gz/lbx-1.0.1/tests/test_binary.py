# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import struct

import pytest

from lbx.exceptions import (
    InvalidVaultFileError,
    UnsupportedVersionError,
    VaultCorruptedError,
)
from lbx.models import KDFParameters, MasterKey, Secret, Service, Vault
from lbx.services import BinaryService
from lbx.settings import BinaryFormat, Crypto


@pytest.fixture
def sample_master_key() -> MasterKey:
    kdf = KDFParameters(
        memory_cost=32_768,
        time_cost=4,
        parallelism=2,
    )
    return MasterKey(
        password_hash=b"hash-bytes",
        salt=b"a" * Crypto.SALT_LENGTH,
        encryption_salt=b"b" * Crypto.SALT_LENGTH,
        kdf_params=kdf,
    )


@pytest.fixture
def sample_vault(sample_master_key: MasterKey) -> Vault:
    s1 = Service(name="svc1")
    s1.secrets["alpha"] = Secret(
        name="alpha",
        ciphertext=b"cipher-alpha",
        nonce=b"x" * Crypto.NONCE_LENGTH,
    )
    s2 = Service(name="svc2")
    s2.secrets["beta"] = Secret(
        name="beta",
        ciphertext=b"cipher-beta",
        nonce=b"y" * Crypto.NONCE_LENGTH,
    )
    return Vault(
        master_key=sample_master_key,
        services={
            "svc1": s1,
            "svc2": s2,
        },
    )


# ---------------------------------------------------------------------------
# Round-trip and basic packing
# ---------------------------------------------------------------------------


def test_pack_roundtrip(sample_vault: Vault, sample_master_key: MasterKey) -> None:
    svc = BinaryService()
    data = svc.pack(sample_vault)

    svc2 = BinaryService()
    vault2 = svc2.unpack(data)

    # master key fields
    mk2 = vault2.master_key
    assert mk2.password_hash == sample_master_key.password_hash
    assert mk2.salt == sample_master_key.salt
    assert mk2.encryption_salt == sample_master_key.encryption_salt
    assert mk2.kdf_params.memory_cost == sample_master_key.kdf_params.memory_cost
    assert mk2.kdf_params.time_cost == sample_master_key.kdf_params.time_cost
    assert mk2.kdf_params.parallelism == sample_master_key.kdf_params.parallelism

    # services and secrets
    assert set(vault2.services.keys()) == {"svc1", "svc2"}
    svc1 = vault2.services["svc1"]
    svc2 = vault2.services["svc2"]

    assert set(svc1.secrets.keys()) == {"alpha"}
    assert set(svc2.secrets.keys()) == {"beta"}

    alpha = svc1.secrets["alpha"]
    beta = svc2.secrets["beta"]

    assert alpha.name == "alpha"
    assert alpha.ciphertext == b"cipher-alpha"
    assert alpha.nonce == b"x" * Crypto.NONCE_LENGTH

    assert beta.name == "beta"
    assert beta.ciphertext == b"cipher-beta"
    assert beta.nonce == b"y" * Crypto.NONCE_LENGTH


def test_pack_empty_services(sample_master_key: MasterKey) -> None:
    v = Vault(master_key=sample_master_key, services={})
    svc = BinaryService()
    data = svc.pack(v)

    svc2 = BinaryService()
    v2 = svc2.unpack(data)
    assert v2.services == {}


# ---------------------------------------------------------------------------
# Header / version / magic errors
# ---------------------------------------------------------------------------


def test_unpack_too_small_header_raises_corrupted() -> None:
    bs = BinaryService()
    magic = BinaryFormat.MAGIC
    # shorter than header_size -> "File too small"
    data = magic[:1]
    with pytest.raises(VaultCorruptedError) as excinfo:
        bs.unpack(data)
    assert "File too small" in str(excinfo.value)


def test_unpack_invalid_magic_raises() -> None:
    # Build a valid blob then corrupt the magic bytes
    mk = MasterKey(
        password_hash=b"h",
        salt=b"a" * Crypto.SALT_LENGTH,
        encryption_salt=b"b" * Crypto.SALT_LENGTH,
        kdf_params=KDFParameters(1, 1, 1),
    )
    v = Vault(master_key=mk, services={})
    bs = BinaryService()
    data = bytearray(bs.pack(v))

    # Corrupt first magic byte
    data[0] ^= 0xFF

    with pytest.raises(InvalidVaultFileError):
        BinaryService().unpack(bytes(data))


def test_unpack_unsupported_version_raises() -> None:
    mk = MasterKey(
        password_hash=b"h",
        salt=b"a" * Crypto.SALT_LENGTH,
        encryption_salt=b"b" * Crypto.SALT_LENGTH,
        kdf_params=KDFParameters(1, 1, 1),
    )
    v = Vault(master_key=mk, services={})
    bs = BinaryService()
    data = bytearray(bs.pack(v))

    magic_len = len(BinaryFormat.MAGIC)
    (version,) = struct.unpack_from("<H", data, offset=magic_len)
    bad_version = (version + 1) & 0xFFFF

    struct.pack_into("<H", data, magic_len, bad_version)

    with pytest.raises(UnsupportedVersionError) as excinfo:
        BinaryService().unpack(bytes(data))
    assert excinfo.value.version == bad_version


def test_unpack_trailing_data_raises_corrupted(sample_vault: Vault) -> None:
    bs = BinaryService()
    data = bs.pack(sample_vault)
    # append junk byte
    data_with_junk = data + b"\x00"

    with pytest.raises(VaultCorruptedError) as excinfo:
        BinaryService().unpack(data_with_junk)

    assert "Trailing data after vault content" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Master key corruption / low-level read errors
# ---------------------------------------------------------------------------


def test_corrupted_master_key_length_raises_corrupted(sample_vault: Vault) -> None:
    bs = BinaryService()
    data = bytearray(bs.pack(sample_vault))

    header_len = BinaryFormat.header_size()
    # increase master-key blob length beyond available to force _read_bytes failure
    (orig_len,) = struct.unpack_from("<I", data, offset=header_len)
    struct.pack_into("<I", data, header_len, orig_len + 10_000)

    with pytest.raises(VaultCorruptedError) as excinfo:
        BinaryService().unpack(bytes(data))

    msg = str(excinfo.value)
    assert "Unexpected end of data" in msg
    assert "master_key" in getattr(excinfo.value, "section", "")


def test_truncated_services_section_raises_corrupted(sample_vault: Vault) -> None:
    bs = BinaryService()
    data = bs.pack(sample_vault)

    # remove last byte so some read in services/secrets will run out
    truncated = data[:-1]

    with pytest.raises(VaultCorruptedError) as excinfo:
        BinaryService().unpack(truncated)

    assert "Unexpected end of data" in str(excinfo.value)
    # section will be something like "services" or "service[0].secret[0]"
    assert getattr(excinfo.value, "section", "").startswith("service") or "services" in getattr(
        excinfo.value, "section", ""
    )


# ---------------------------------------------------------------------------
# _unpack_services / _unpack_secrets edge cases
# ---------------------------------------------------------------------------


def test_unpack_zero_services(sample_master_key: MasterKey) -> None:
    v = Vault(master_key=sample_master_key, services={})
    bs = BinaryService()
    data = bs.pack(v)

    v2 = BinaryService().unpack(data)
    assert v2.services == {}


def test_unpack_service_with_zero_secrets(sample_master_key: MasterKey) -> None:
    svc = Service(name="empty")
    v = Vault(master_key=sample_master_key, services={"empty": svc})
    bs = BinaryService()
    data = bs.pack(v)

    v2 = BinaryService().unpack(data)
    assert set(v2.services.keys()) == {"empty"}
    assert v2.services["empty"].secrets == {}


# ---------------------------------------------------------------------------
# _read_uint32 / _read_bytes_prefixed / _read_string behaviour
# ---------------------------------------------------------------------------


def test_read_uint32_and_prefixed_helpers_via_public_unpack(sample_master_key: MasterKey) -> None:
    # Build a minimal vault with one service/secret to exercise the helpers
    svc = Service(name="s")
    secret = Secret(
        name="n",
        ciphertext=b"c",
        nonce=b"z" * Crypto.NONCE_LENGTH,
    )
    svc.secrets["n"] = secret
    v = Vault(master_key=sample_master_key, services={"s": svc})

    # Round-trip to ensure uint32 and prefixed/string logic works
    bs = BinaryService()
    data = bs.pack(v)
    v2 = BinaryService().unpack(data)

    assert set(v2.services.keys()) == {"s"}
    s2 = v2.services["s"]
    assert set(s2.secrets.keys()) == {"n"}
    sec2 = s2.secrets["n"]
    assert sec2.name == "n"
    assert sec2.ciphertext == b"c"
    assert sec2.nonce == b"z" * Crypto.NONCE_LENGTH
