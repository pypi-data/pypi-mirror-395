# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from lbx import core
from lbx.exceptions import (
    SecretExistsError,
    SecretNotFoundError,
    ServiceExistsError,
    ServiceNotFoundError,
    VaultExistsError,
    VaultLockedError,
    VaultNotFoundError,
)
from lbx.models import Secret as SecretModel
from lbx.models import SecretEntry, Service, Vault

# ---------------------------------------------------------------------------
# Dummy services
# ---------------------------------------------------------------------------


class DummyFileService:
    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path or "/tmp/vault.lbx")
        self.data: bytes | None = None
        self.exists_flag: bool = False
        self.deleted: bool = False

    def exists(self) -> bool:
        return self.exists_flag

    def read(self) -> bytes:
        if self.data is None:
            raise RuntimeError("No data to read")
        return self.data

    def write(self, data: bytes) -> None:
        self.data = data
        self.exists_flag = True

    def delete(self) -> None:
        self.data = None
        self.exists_flag = False
        self.deleted = True


class DummyBinaryService:
    def __init__(self) -> None:
        self.last_packed: Vault | None = None
        self.unpack_vault: Vault | None = None

    def pack(self, vault: Vault) -> bytes:
        self.last_packed = vault
        # fixed marker to keep things simple
        return b"VAULT-DATA"

    def unpack(self, data: bytes) -> Vault:
        if data != b"VAULT-DATA":
            raise RuntimeError("Unexpected data")
        if self.unpack_vault is None:
            raise RuntimeError("No vault set for unpack")
        return self.unpack_vault


class DummyCryptoService:
    def __init__(self) -> None:
        self.key: bytes | None = None
        self.encrypted: list[tuple[str, str]] = []
        self.decrypted: list[SecretModel] = []

    def set_key(self, key: bytes) -> None:
        self.key = key

    def clear_key(self) -> None:
        self.key = None

    def encrypt(self, name: str, value: str) -> SecretModel:
        self.encrypted.append((name, value))
        # encode name/value in ciphertext for easy checks
        return SecretModel(
            name=name,
            ciphertext=f"{name}:{value}".encode(),
            nonce=b"NONCE",
        )

    def decrypt(self, secret: SecretModel) -> str:
        self.decrypted.append(secret)
        return secret.ciphertext.decode().split(":", 1)[1]


class DummyKeyringService:
    def __init__(self) -> None:
        self._exists: bool = False
        self.stored_key: bytes | None = None
        self.deleted: bool = False

    def store(self, key: bytes) -> None:
        self.stored_key = key
        self._exists = True

    def exists(self) -> bool:
        return self._exists

    def retrieve(self) -> bytes:
        if self.stored_key is None:
            raise RuntimeError("No key stored")
        return self.stored_key

    def delete(self) -> None:
        self.deleted = True
        self.stored_key = None
        self._exists = False


# ---------------------------------------------------------------------------
# Common fixture: Lbx with dummy services and patched CryptoService methods
# ---------------------------------------------------------------------------


@pytest.fixture
def lbx_with_dummies(
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[core.Lbx, DummyBinaryService, DummyFileService, DummyCryptoService, DummyKeyringService]:
    binary = DummyBinaryService()
    file = DummyFileService()
    crypto = DummyCryptoService()
    keyring = DummyKeyringService()

    # patch class-level CryptoService methods used by create/unlock
    def fake_create_master_key(password: str) -> tuple[bytes, bytes]:
        return (b"MK:" + password.encode(), b"KEY:" + password.encode())

    def fake_verify_password(password: str, master_key: bytes) -> bytes:
        return b"KEY:" + password.encode()

    monkeypatch.setattr(core.CryptoService, "create_master_key", staticmethod(fake_create_master_key))
    monkeypatch.setattr(core.CryptoService, "verify_password", staticmethod(fake_verify_password))

    s = core.Lbx(
        path=file.path,
        use_keychain=True,
        binary_service=binary,
        file_service=file,
        keyring_service=keyring,
        crypto_service=crypto,
    )

    return s, binary, file, crypto, keyring


# ---------------------------------------------------------------------------
# Basic properties
# ---------------------------------------------------------------------------


def test_is_unlocked_and_path(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, crypto, _keyring = lbx_with_dummies

    assert s.is_unlocked is False
    crypto.set_key(b"K")
    assert s.is_unlocked is True

    assert s.path == file.path


def test_exists_uses_file_service(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = False
    assert s.exists() is False

    file.exists_flag = True
    assert s.exists() is True


# ---------------------------------------------------------------------------
# create / unlock / lock / keychain
# ---------------------------------------------------------------------------


def test_create_new_vault(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, keyring = lbx_with_dummies

    file.exists_flag = False
    binary.unpack_vault = Vault(master_key=b"MK:pw")

    s.create("pw")

    # file now exists and binary.pack saw a vault
    assert file.exists_flag is True
    assert binary.last_packed is not None
    assert isinstance(binary.last_packed, Vault)
    assert binary.last_packed.master_key == b"MK:pw"

    # crypto key set from create_master_key
    assert crypto.key == b"KEY:pw"
    # key stored in keyring
    assert keyring.stored_key == b"KEY:pw"


def test_create_raises_if_vault_exists(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = True

    with pytest.raises(VaultExistsError):
        s.create("pw")


def test_unlock_success(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, keyring = lbx_with_dummies

    # simulate existing vault on disk
    file.exists_flag = True
    file.data = b"VAULT-DATA"
    binary.unpack_vault = Vault(master_key=b"MK:pw")

    s.unlock("pw")

    assert isinstance(s._vault, Vault)
    assert crypto.key == b"KEY:pw"
    assert keyring.stored_key == b"KEY:pw"


def test_unlock_raises_if_vault_missing(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = False

    with pytest.raises(VaultNotFoundError):
        s.unlock("pw")


def test_unlock_from_keychain_no_entry(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, crypto, keyring = lbx_with_dummies

    file.exists_flag = True
    file.data = b"VAULT-DATA"
    keyring._exists = False  # no key stored

    result = s.unlock_from_keychain()

    assert result is False
    assert crypto.key is None


def test_unlock_from_keychain_success(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, keyring = lbx_with_dummies

    file.exists_flag = True
    file.data = b"VAULT-DATA"
    binary.unpack_vault = Vault(master_key=b"MK:any")
    keyring.store(b"SAVED-KEY")

    result = s.unlock_from_keychain()

    assert result is True
    assert crypto.key == b"SAVED-KEY"
    assert isinstance(s._vault, Vault)


def test_lock_and_lock_and_forget(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, _file, crypto, keyring = lbx_with_dummies

    crypto.set_key(b"K")
    keyring.store(b"K")

    s.lock()
    assert crypto.key is None
    assert keyring.stored_key == b"K"

    crypto.set_key(b"K2")
    keyring.store(b"K2")
    s.lock_and_forget()

    assert crypto.key is None
    assert keyring.stored_key is None
    assert keyring.deleted is True


def test_delete_vault_clears_everything(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, crypto, keyring = lbx_with_dummies

    file.exists_flag = True
    file.data = b"VAULT-DATA"
    s._vault = Vault(master_key=b"MK")
    crypto.set_key(b"K")
    keyring.store(b"K")

    s.delete_vault()

    assert file.deleted is True
    assert keyring.stored_key is None
    assert crypto.key is None
    assert s._vault is None


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------


def _make_vault_with_services() -> Vault:
    s1 = Service(name="svc1")
    s2 = Service(name="svc2")
    return Vault(
        master_key=b"MK",
        services={
            "svc1": s1,
            "svc2": s2,
        },
    )


def test_list_services(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    s._vault = _make_vault_with_services()

    names = s.list_services()
    assert set(names) == {"svc1", "svc2"}


def test_list_services_raises_if_vault_missing(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = False
    s._vault = None

    with pytest.raises(VaultNotFoundError):
        s.list_services()


def test_has_service(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    s._vault = _make_vault_with_services()

    assert s.has_service("svc1") is True
    assert s.has_service("missing") is False


def test_delete_service_success(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = _make_vault_with_services()
    s._vault = vault
    crypto.set_key(b"K")  # unlocked

    s.delete_service("svc1")

    assert "svc1" not in vault.services
    assert binary.last_packed is vault


def test_delete_service_not_found(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    s._vault = _make_vault_with_services()
    crypto.set_key(b"K")  # unlocked

    with pytest.raises(ServiceNotFoundError):
        s.delete_service("nope")


def test_rename_service_success(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = _make_vault_with_services()
    s._vault = vault
    crypto.set_key(b"K")  # unlocked

    svc_obj = vault.services["svc1"]

    s.rename_service("svc1", "newsvc")

    assert "svc1" not in vault.services
    assert "newsvc" in vault.services
    assert vault.services["newsvc"] is svc_obj
    assert svc_obj.name == "newsvc"
    assert binary.last_packed is vault


def test_rename_service_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = _make_vault_with_services()
    s._vault = vault
    crypto.set_key(b"K")  # unlocked

    with pytest.raises(ServiceNotFoundError):
        s.rename_service("missing", "new")

    with pytest.raises(ServiceExistsError):
        s.rename_service("svc1", "svc2")  # target already exists


# ---------------------------------------------------------------------------
# Secrets
# ---------------------------------------------------------------------------


def test_list_secrets_all(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    svc1 = Service(name="svc1")
    svc1.secrets = {"a": SecretModel("a", b"c1", b"n1")}
    svc2 = Service(name="svc2")
    svc2.secrets = {"b": SecretModel("b", b"c2", b"n2")}
    vault.services = {"svc1": svc1, "svc2": svc2}
    s._vault = vault

    pairs = s.list_secrets()
    assert set(pairs) == {("svc1", "a"), ("svc2", "b")}


def test_list_secrets_by_service_and_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    svc = Service(name="svc")
    svc.secrets = {"x": SecretModel("x", b"cx", b"nx")}
    vault.services = {"svc": svc}
    s._vault = vault

    pairs = s.list_secrets("svc")
    assert pairs == [("svc", "x")]

    with pytest.raises(ServiceNotFoundError):
        s.list_secrets("missing")


def test_has_secret(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, _crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    svc = Service(name="svc")
    svc.secrets = {"x": SecretModel("x", b"cx", b"nx")}
    vault.services = {"svc": svc}
    s._vault = vault

    assert s.has_secret("svc", "x") is True
    assert s.has_secret("svc", "y") is False
    assert s.has_secret("missing", "x") is False


def test_get_secret_success_and_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    svc = Service(name="svc")
    svc.secrets = {"x": SecretModel("x", b"x:VALUE", b"n")}
    vault.services = {"svc": svc}
    s._vault = vault
    crypto.set_key(b"K")  # unlocked

    entry = s.get_secret("svc", "x")
    assert isinstance(entry, SecretEntry)
    assert entry.service == "svc"
    assert entry.name == "x"
    assert entry.value == "VALUE"

    with pytest.raises(ServiceNotFoundError):
        s.get_secret("missing", "x")

    with pytest.raises(SecretNotFoundError):
        s.get_secret("svc", "missing")


def test_add_secret_creates_service_and_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK", services={})
    s._vault = vault
    crypto.set_key(b"K")

    # new service created
    s.add_secret("svc", "name", "VAL")
    assert "svc" in vault.services
    svc = vault.services["svc"]
    assert "name" in svc.secrets
    assert binary.last_packed is vault

    # duplicate secret
    with pytest.raises(SecretExistsError):
        s.add_secret("svc", "name", "OTHER")


def test_update_secret_success_and_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    svc = Service(name="svc")
    svc.secrets = {"x": SecretModel("x", b"old", b"n")}
    vault.services = {"svc": svc}
    s._vault = vault
    crypto.set_key(b"K")

    s.update_secret("svc", "x", "NEW")
    assert svc.secrets["x"].ciphertext.startswith(b"x:NEW")
    assert binary.last_packed is vault

    with pytest.raises(ServiceNotFoundError):
        s.update_secret("missing", "x", "VAL")

    with pytest.raises(SecretNotFoundError):
        s.update_secret("svc", "missing", "VAL")


def test_rename_secret_success_and_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    svc = Service(name="svc")
    svc.secrets = {
        "old": SecretModel("old", b"c", b"n"),
        "exists": SecretModel("exists", b"c2", b"n2"),
    }
    vault.services = {"svc": svc}
    s._vault = vault
    crypto.set_key(b"K")

    # errors
    with pytest.raises(ServiceNotFoundError):
        s.rename_secret("missing", "old", "new")

    with pytest.raises(SecretNotFoundError):
        s.rename_secret("svc", "missing", "new")

    with pytest.raises(SecretExistsError):
        s.rename_secret("svc", "old", "exists")

    # success
    s.rename_secret("svc", "old", "new")
    assert "old" not in svc.secrets
    assert "new" in svc.secrets
    new_secret = svc.secrets["new"]
    assert new_secret.name == "new"
    assert new_secret.ciphertext == b"c"
    assert new_secret.nonce == b"n"
    assert binary.last_packed is vault


def test_move_secret_success_and_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    src = Service(name="src")
    src.secrets = {"x": SecretModel("x", b"c", b"n")}
    dst = Service(name="dst")
    dst.secrets = {}
    vault.services = {"src": src, "dst": dst}
    s._vault = vault
    crypto.set_key(b"K")

    # errors
    with pytest.raises(ServiceNotFoundError):
        s.move_secret("missing", "x", "dst")

    with pytest.raises(SecretNotFoundError):
        s.move_secret("src", "missing", "dst")

    dst.secrets["x"] = SecretModel("x", b"other", b"n2")
    with pytest.raises(SecretExistsError):
        s.move_secret("src", "x", "dst")

    # reset and success, including auto-create target and auto-remove empty source
    dst.secrets.clear()
    del vault.services["dst"]

    s.move_secret("src", "x", "dst")

    assert "src" not in vault.services  # removed because empty
    assert "dst" in vault.services
    assert "x" in vault.services["dst"].secrets
    assert binary.last_packed is vault


def test_delete_secret_success_and_errors(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    vault = Vault(master_key=b"MK")
    svc = Service(name="svc")
    svc.secrets = {"x": SecretModel("x", b"c", b"n")}
    vault.services = {"svc": svc}
    s._vault = vault
    crypto.set_key(b"K")

    with pytest.raises(ServiceNotFoundError):
        s.delete_secret("missing", "x")

    with pytest.raises(SecretNotFoundError):
        s.delete_secret("svc", "missing")

    # success; service removed once empty
    s.delete_secret("svc", "x")
    assert "svc" not in vault.services
    assert binary.last_packed is vault


# ---------------------------------------------------------------------------
# Internals: _require_vault / _ensure_loaded / _ensure_unlocked / _load / _save
# ---------------------------------------------------------------------------


def test_require_vault(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, _file, _crypto, _keyring = lbx_with_dummies

    s._vault = None
    with pytest.raises(VaultNotFoundError):
        s._require_vault()

    v = Vault(master_key=b"MK")
    s._vault = v
    assert s._require_vault() is v


def test_ensure_loaded_and_load(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, _crypto, _keyring = lbx_with_dummies

    # load fails if file missing
    file.exists_flag = False
    s._vault = None
    with pytest.raises(VaultNotFoundError):
        s._ensure_loaded()

    # success path
    file.exists_flag = True
    file.data = b"VAULT-DATA"
    v = Vault(master_key=b"MK")
    binary.unpack_vault = v
    s._vault = None

    s._ensure_loaded()
    assert s._vault is v


def test_ensure_unlocked(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, _binary, file, crypto, _keyring = lbx_with_dummies

    file.exists_flag = True
    s._vault = Vault(master_key=b"MK")

    # locked
    crypto.clear_key()
    with pytest.raises(VaultLockedError):
        s._ensure_unlocked()

    # unlocked
    crypto.set_key(b"K")
    s._ensure_unlocked()  # should not raise


def test_save_requires_vault(lbx_with_dummies: tuple[Any, ...]) -> None:
    s, binary, file, _crypto, _keyring = lbx_with_dummies

    s._vault = None
    with pytest.raises(VaultNotFoundError):
        s._save()

    file.exists_flag = True
    v = Vault(master_key=b"MK")
    s._vault = v
    s._save()

    assert binary.last_packed is v
    assert file.data == b"VAULT-DATA"
