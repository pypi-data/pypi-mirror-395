# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import base64
import os

import pytest
from keyring.errors import KeyringError, KeyringLocked, NoKeyringError, PasswordDeleteError

from lbx.exceptions import (
    KeychainAccessError,
    KeychainDataError,
    KeychainNotAvailableError,
    KeyNotFoundError,
)
from lbx.services import key_ring
from lbx.services.key_ring import KeyringService
from lbx.settings import Crypto

# ---------------------------------------------------------------------------
# Basic construction / properties
# ---------------------------------------------------------------------------


def test_defaults() -> None:
    s = KeyringService()
    assert s.service == KeyringService.DEFAULT_SERVICE
    assert s.account == KeyringService.DEFAULT_ACCOUNT


def test_custom_service_and_account() -> None:
    s = KeyringService(service="svc", account="acc")
    assert s.service == "svc"
    assert s.account == "acc"


# ---------------------------------------------------------------------------
# store()
# ---------------------------------------------------------------------------


def test_store_success(monkeypatch) -> None:
    s = KeyringService(service="svc", account="acc")
    key = os.urandom(Crypto.KEY_LENGTH)

    calls: dict[str, tuple[str, str, str]] = {}

    def fake_set_password(service: str, account: str, password: str) -> None:
        calls["args"] = (service, account, password)

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"set_password": staticmethod(fake_set_password)}),
    )

    s.store(key)

    service, account, password = calls["args"]
    assert service == "svc"
    assert account == "acc"
    decoded = base64.b64decode(password.encode("ascii"), validate=True)
    assert decoded == key


def test_store_invalid_key_length_raises() -> None:
    s = KeyringService()
    key = b"short"
    with pytest.raises(KeychainDataError) as exc:
        s.store(key)

    assert "Invalid key length" in str(exc.value)


def test_store_no_keyring_raises_not_available(monkeypatch) -> None:
    s = KeyringService()

    def fake_set_password(service: str, account: str, password: str) -> None:
        raise NoKeyringError("no backend")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"set_password": staticmethod(fake_set_password)}),
    )

    with pytest.raises(KeychainNotAvailableError):
        s.store(os.urandom(Crypto.KEY_LENGTH))


def test_store_keyring_locked_raises_access_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_set_password(service: str, account: str, password: str) -> None:
        raise KeyringLocked("locked")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"set_password": staticmethod(fake_set_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.store(os.urandom(Crypto.KEY_LENGTH))

    msg = str(exc.value)
    assert "store" in msg
    assert "locked" in msg


def test_store_permission_error_raises_access_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_set_password(service: str, account: str, password: str) -> None:
        raise PermissionError("no access")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"set_password": staticmethod(fake_set_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.store(os.urandom(Crypto.KEY_LENGTH))

    msg = str(exc.value)
    assert "store" in msg
    assert "permission denied" in msg


def test_store_other_keyring_error_wrapped(monkeypatch) -> None:
    s = KeyringService()

    def fake_set_password(service: str, account: str, password: str) -> None:
        raise KeyringError("boom")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"set_password": staticmethod(fake_set_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.store(os.urandom(Crypto.KEY_LENGTH))

    msg = str(exc.value)
    assert "store" in msg
    assert "boom" in msg


# ---------------------------------------------------------------------------
# retrieve()
# ---------------------------------------------------------------------------


def test_retrieve_success(monkeypatch) -> None:
    s = KeyringService(service="svc", account="acc")
    key = os.urandom(Crypto.KEY_LENGTH)
    encoded = base64.b64encode(key).decode("ascii")

    def fake_get_password(service: str, account: str) -> str | None:
        assert service == "svc"
        assert account == "acc"
        return encoded

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    result = s.retrieve()
    assert result == key


def test_retrieve_missing_raises_key_not_found(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        return None

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    with pytest.raises(KeyNotFoundError):
        s.retrieve()


def test_retrieve_invalid_base64_raises_data_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        return "not-base64!!"

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    with pytest.raises(KeychainDataError) as exc:
        s.retrieve()

    assert "Corrupted key data" in str(exc.value)


def test_retrieve_wrong_key_length_raises_data_error(monkeypatch) -> None:
    s = KeyringService()
    bad_key = b"short"
    encoded = base64.b64encode(bad_key).decode("ascii")

    def fake_get_password(service: str, account: str) -> str | None:
        return encoded

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    with pytest.raises(KeychainDataError) as exc:
        s.retrieve()

    assert "Invalid key length in keychain" in str(exc.value)


def test_retrieve_no_keyring_raises_not_available(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        raise NoKeyringError("no backend")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    with pytest.raises(KeychainNotAvailableError):
        s.retrieve()


def test_retrieve_keyring_locked_raises_access_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        raise KeyringLocked("locked")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.retrieve()

    msg = str(exc.value)
    assert "retrieve" in msg
    assert "locked" in msg


def test_retrieve_permission_error_raises_access_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        raise PermissionError("no access")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.retrieve()

    msg = str(exc.value)
    assert "retrieve" in msg
    assert "permission denied" in msg


def test_retrieve_other_keyring_error_wrapped(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        raise KeyringError("boom")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.retrieve()

    msg = str(exc.value)
    assert "retrieve" in msg
    assert "boom" in msg


# ---------------------------------------------------------------------------
# delete()
# ---------------------------------------------------------------------------


def test_delete_success(monkeypatch) -> None:
    s = KeyringService(service="svc", account="acc")
    called = {"args": None}

    def fake_delete_password(service: str, account: str) -> None:
        called["args"] = (service, account)

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"delete_password": staticmethod(fake_delete_password)}),
    )

    s.delete()
    assert called["args"] == ("svc", "acc")


def test_delete_password_not_found_raises_key_not_found(monkeypatch) -> None:
    s = KeyringService()

    def fake_delete_password(service: str, account: str) -> None:
        raise PasswordDeleteError("noentry")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"delete_password": staticmethod(fake_delete_password)}),
    )

    with pytest.raises(KeyNotFoundError):
        s.delete()


def test_delete_no_keyring_raises_not_available(monkeypatch) -> None:
    s = KeyringService()

    def fake_delete_password(service: str, account: str) -> None:
        raise NoKeyringError("no backend")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"delete_password": staticmethod(fake_delete_password)}),
    )

    with pytest.raises(KeychainNotAvailableError):
        s.delete()


def test_delete_keyring_locked_raises_access_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_delete_password(service: str, account: str) -> None:
        raise KeyringLocked("locked")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"delete_password": staticmethod(fake_delete_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.delete()

    msg = str(exc.value)
    assert "delete" in msg
    assert "locked" in msg


def test_delete_permission_error_raises_access_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_delete_password(service: str, account: str) -> None:
        raise PermissionError("no access")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"delete_password": staticmethod(fake_delete_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.delete()

    msg = str(exc.value)
    assert "delete" in msg
    assert "permission denied" in msg


def test_delete_other_keyring_error_wrapped(monkeypatch) -> None:
    s = KeyringService()

    def fake_delete_password(service: str, account: str) -> None:
        raise KeyringError("boom")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"delete_password": staticmethod(fake_delete_password)}),
    )

    with pytest.raises(KeychainAccessError) as exc:
        s.delete()

    msg = str(exc.value)
    assert "delete" in msg
    assert "boom" in msg


# ---------------------------------------------------------------------------
# exists()
# ---------------------------------------------------------------------------


def test_exists_true_when_password_present(monkeypatch) -> None:
    s = KeyringService(service="svc", account="acc")

    def fake_get_password(service: str, account: str) -> str | None:
        assert service == "svc"
        assert account == "acc"
        return "something"

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    assert s.exists() is True


def test_exists_false_when_password_missing(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        return None

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    assert s.exists() is False


def test_exists_returns_false_on_no_keyring(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        raise NoKeyringError("no backend")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    assert s.exists() is False


def test_exists_returns_false_on_keyring_error(monkeypatch) -> None:
    s = KeyringService()

    def fake_get_password(service: str, account: str) -> str | None:
        raise KeyringError("boom")

    monkeypatch.setattr(
        key_ring,
        "keyring",
        type("KR", (), {"get_password": staticmethod(fake_get_password)}),
    )

    assert s.exists() is False
