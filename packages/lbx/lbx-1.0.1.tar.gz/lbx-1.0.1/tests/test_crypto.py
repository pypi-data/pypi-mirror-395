# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import os

import pytest

from lbx.exceptions import DecryptionError, EncryptionError, InvalidPasswordError
from lbx.models import KDFParameters, MasterKey, Secret
from lbx.services.crypto import CryptoService
from lbx.settings import Crypto

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def crypto() -> CryptoService:
    return CryptoService()


@pytest.fixture
def key() -> bytes:
    # Proper AES-256 key length
    return os.urandom(Crypto.KEY_LENGTH)


@pytest.fixture
def kdf_params() -> KDFParameters:
    # Use smaller params to keep tests fast
    return KDFParameters(memory_cost=8_192, time_cost=2, parallelism=1)


# ---------------------------------------------------------------------------
# Key management
# ---------------------------------------------------------------------------


def test_init_with_no_key(crypto: CryptoService) -> None:
    assert crypto.key is None


def test_init_with_key(key: bytes) -> None:
    c = CryptoService(key)
    assert c.key == key


def test_set_key_valid_length(crypto: CryptoService, key: bytes) -> None:
    crypto.set_key(key)
    assert crypto.key == key  # and AESGCM is initialized implicitly


def test_set_key_invalid_length_raises(crypto: CryptoService) -> None:
    bad_key = b"too-short"
    with pytest.raises(EncryptionError) as excinfo:
        crypto.set_key(bad_key)

    assert str(Crypto.KEY_LENGTH) in str(excinfo.value)


def test_clear_key_resets_cipher_and_key(crypto: CryptoService, key: bytes) -> None:
    crypto.set_key(key)
    assert crypto.key is not None

    crypto.clear_key()
    assert crypto.key is None
    # encrypt should now fail
    with pytest.raises(EncryptionError):
        crypto.encrypt("name", "value")


# ---------------------------------------------------------------------------
# Encryption / decryption
# ---------------------------------------------------------------------------


def test_encrypt_and_decrypt_round_trip(crypto: CryptoService, key: bytes) -> None:
    crypto.set_key(key)

    secret = crypto.encrypt("token", "value123")
    assert isinstance(secret, Secret)
    assert secret.name == "token"
    assert len(secret.nonce) == Crypto.NONCE_LENGTH
    assert secret.ciphertext

    decrypted = crypto.decrypt(secret)
    assert decrypted == "value123"


def test_encrypt_empty_name_raises(crypto: CryptoService, key: bytes) -> None:
    crypto.set_key(key)
    with pytest.raises(EncryptionError):
        crypto.encrypt("", "value")


def test_encrypt_empty_value_raises(crypto: CryptoService, key: bytes) -> None:
    crypto.set_key(key)
    with pytest.raises(EncryptionError):
        crypto.encrypt("name", "")


def test_encrypt_without_key_raises(crypto: CryptoService) -> None:
    with pytest.raises(EncryptionError):
        crypto.encrypt("name", "value")


def test_decrypt_without_key_raises(crypto: CryptoService, key: bytes) -> None:
    # encrypt with a separate instance
    c2 = CryptoService(key)
    secret = c2.encrypt("name", "value")

    # crypto has no key set
    with pytest.raises(DecryptionError):
        crypto.decrypt(secret)


def test_decrypt_with_wrong_key_raises_decryption_error(key: bytes) -> None:
    # encrypt with key1
    key1 = key
    key2 = os.urandom(Crypto.KEY_LENGTH)

    c1 = CryptoService(key1)
    secret = c1.encrypt("name", "value")

    # decrypt with key2 -> InvalidTag -> DecryptionError
    c2 = CryptoService(key2)
    with pytest.raises(DecryptionError) as excinfo:
        c2.decrypt(secret)

    assert "Data corrupted or wrong key" in str(excinfo.value)


def test_decrypt_invalid_utf8_raises_decryption_error(key: bytes) -> None:
    # use CryptoService's AESGCM directly to produce non-UTF8 plaintext
    c = CryptoService(key)
    nonce = os.urandom(Crypto.NONCE_LENGTH)
    # invalid UTF-8 bytes
    plaintext = b"\xff\xff\xff"
    ciphertext = c._cipher.encrypt(nonce, plaintext, None)  # type: ignore[attr-defined]

    secret = Secret(name="bad", ciphertext=ciphertext, nonce=nonce)

    with pytest.raises(DecryptionError) as excinfo:
        c.decrypt(secret)

    assert "Invalid data encoding" in str(excinfo.value)


# ---------------------------------------------------------------------------
# KDF / salts
# ---------------------------------------------------------------------------


def test_generate_salt_length() -> None:
    salt = CryptoService.generate_salt()
    assert isinstance(salt, bytes)
    assert len(salt) == Crypto.SALT_LENGTH


def test_derive_key_success(kdf_params: KDFParameters) -> None:
    password = "secret-pass"
    salt = CryptoService.generate_salt()

    key = CryptoService.derive_key(password, salt, kdf_params)
    assert isinstance(key, bytes)
    assert len(key) == Crypto.KEY_LENGTH

    # same inputs -> same key
    key2 = CryptoService.derive_key(password, salt, kdf_params)
    assert key == key2

    # different salt -> different key
    other_salt = CryptoService.generate_salt()
    key3 = CryptoService.derive_key(password, other_salt, kdf_params)
    assert key != key3


def test_derive_key_invalid_salt_length_raises(kdf_params: KDFParameters) -> None:
    password = "pw"
    bad_salt = b"short"
    with pytest.raises(EncryptionError) as excinfo:
        CryptoService.derive_key(password, bad_salt, kdf_params)

    assert "Salt must be" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Master key creation and verification
# ---------------------------------------------------------------------------


def test_create_master_key_success() -> None:
    password = "master-password"

    master_key, enc_key = CryptoService.create_master_key(password)

    assert isinstance(master_key, MasterKey)
    assert isinstance(enc_key, bytes)
    assert len(enc_key) == Crypto.KEY_LENGTH

    assert len(master_key.salt) == Crypto.SALT_LENGTH
    assert len(master_key.encryption_salt) == Crypto.SALT_LENGTH
    assert len(master_key.password_hash) == Crypto.KEY_LENGTH

    # hash and encryption key must differ (different salts)
    assert master_key.password_hash != enc_key


def test_create_master_key_empty_password_raises() -> None:
    with pytest.raises(InvalidPasswordError):
        CryptoService.create_master_key("")


def test_verify_password_success_matches_create_master_key() -> None:
    password = "pw-123"
    master_key, enc_key = CryptoService.create_master_key(password)

    derived = CryptoService.verify_password(password, master_key)
    assert derived == enc_key


def test_verify_password_empty_raises(sample_master_key: MasterKey | None = None) -> None:
    # create a simple master key manually
    params = KDFParameters()
    salt = CryptoService.generate_salt()
    encryption_salt = CryptoService.generate_salt()
    password_hash = CryptoService.derive_key("pw", salt, params)
    mk = MasterKey(
        password_hash=password_hash,
        salt=salt,
        encryption_salt=encryption_salt,
        kdf_params=params,
    )

    with pytest.raises(InvalidPasswordError):
        CryptoService.verify_password("", mk)


def test_verify_password_incorrect_raises() -> None:
    password = "correct"
    master_key, _ = CryptoService.create_master_key(password)

    with pytest.raises(InvalidPasswordError):
        CryptoService.verify_password("wrong", master_key)
