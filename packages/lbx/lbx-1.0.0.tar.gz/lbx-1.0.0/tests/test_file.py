# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path

import pytest

import lbx.services.file as file_mod
from lbx.exceptions import VaultIOError, VaultNotFoundError
from lbx.services.file import FileService

# ---------------------------------------------------------------------------
# Construction / path
# ---------------------------------------------------------------------------


def test_init_uses_default_vault_path_when_none(monkeypatch, tmp_path) -> None:
    fake_default = tmp_path / "default.vault"
    monkeypatch.setattr(file_mod, "default_vault_path", lambda: fake_default)

    fs = FileService()
    assert fs.path == fake_default


def test_init_with_explicit_path_path_instance(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    fs = FileService(p)
    assert fs.path == p


def test_init_with_explicit_path_string(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    fs = FileService(str(p))
    assert fs.path == p


def test_path_property_returns_internal_path(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    fs = FileService(p)
    assert isinstance(fs.path, Path)
    assert fs.path == p


# ---------------------------------------------------------------------------
# exists()
# ---------------------------------------------------------------------------


def test_exists_false_when_file_missing(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    fs = FileService(p)
    assert fs.exists() is False


def test_exists_true_when_regular_file(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    p.write_bytes(b"data")
    fs = FileService(p)
    assert fs.exists() is True


# ---------------------------------------------------------------------------
# read()
# ---------------------------------------------------------------------------


def test_read_success(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    p.write_bytes(b"hello")
    fs = FileService(p)

    assert fs.read() == b"hello"


def test_read_missing_raises_vault_not_found(tmp_path) -> None:
    p = tmp_path / "missing.vault"
    fs = FileService(p)

    with pytest.raises(VaultNotFoundError):
        fs.read()


def test_read_permission_error_wrapped(monkeypatch, tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    p.write_bytes(b"x")
    fs = FileService(p)

    orig_read_bytes = Path.read_bytes

    def fake_read_bytes(self: Path) -> bytes:
        if self == p:
            raise PermissionError("nope")
        return orig_read_bytes(self)

    monkeypatch.setattr(Path, "read_bytes", fake_read_bytes)

    with pytest.raises(VaultIOError) as exc:
        fs.read()

    msg = str(exc.value)
    assert "read" in msg
    assert "permission denied" in msg
    assert str(p) in msg


def test_read_os_error_wrapped(monkeypatch, tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    p.write_bytes(b"x")
    fs = FileService(p)

    orig_read_bytes = Path.read_bytes

    def fake_read_bytes(self: Path) -> bytes:
        if self == p:
            raise OSError("boom")
        return orig_read_bytes(self)

    monkeypatch.setattr(Path, "read_bytes", fake_read_bytes)

    with pytest.raises(VaultIOError) as exc:
        fs.read()

    msg = str(exc.value)
    assert "read" in msg
    assert "boom" in msg
    assert str(p) in msg


# ---------------------------------------------------------------------------
# write() - happy path
# ---------------------------------------------------------------------------


def test_write_success_creates_file_atomically(tmp_path) -> None:
    p = tmp_path / "dir" / "vault.lbx"
    fs = FileService(p)

    fs.write(b"payload")

    assert p.read_bytes() == b"payload"
    # temp file must be removed
    assert not p.with_suffix(p.suffix + ".tmp").exists()


# ---------------------------------------------------------------------------
# write() - directory creation errors
# ---------------------------------------------------------------------------


def test_write_directory_permission_error_wrapped(monkeypatch, tmp_path) -> None:
    p = tmp_path / "dir" / "vault.lbx"
    fs = FileService(p)

    orig_mkdir = Path.mkdir

    def fake_mkdir(self: Path, *a, **kw) -> None:
        if self == p.parent:
            raise PermissionError("no mkdir")
        return orig_mkdir(self, *a, **kw)

    monkeypatch.setattr(Path, "mkdir", fake_mkdir)

    with pytest.raises(VaultIOError) as exc:
        fs.write(b"data")

    msg = str(exc.value)
    assert "create directory" in msg
    assert "permission denied" in msg
    assert str(p.parent) in msg


def test_write_directory_os_error_wrapped(monkeypatch, tmp_path) -> None:
    p = tmp_path / "dir" / "vault.lbx"
    fs = FileService(p)

    orig_mkdir = Path.mkdir

    def fake_mkdir(self: Path, *a, **kw) -> None:
        if self == p.parent:
            raise OSError("mkdir fail")
        return orig_mkdir(self, *a, **kw)

    monkeypatch.setattr(Path, "mkdir", fake_mkdir)

    with pytest.raises(VaultIOError) as exc:
        fs.write(b"data")

    msg = str(exc.value)
    assert "create directory" in msg
    assert "mkdir fail" in msg
    assert str(p.parent) in msg


# ---------------------------------------------------------------------------
# write() - temp write/replace errors (and cleanup)
# ---------------------------------------------------------------------------


def test_write_temp_permission_error_cleans_up(monkeypatch, tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    fs = FileService(p)
    temp = p.with_suffix(p.suffix + ".tmp")

    orig_write_bytes = Path.write_bytes

    def fake_write_bytes(self: Path, data: bytes) -> int:
        if self == temp:
            raise PermissionError("no write")
        return orig_write_bytes(self, data)

    monkeypatch.setattr(Path, "write_bytes", fake_write_bytes)

    with pytest.raises(VaultIOError) as exc:
        fs.write(b"payload")

    msg = str(exc.value)
    assert "write" in msg
    assert "permission denied" in msg
    assert str(p) in msg
    assert not temp.exists()


def test_write_replace_os_error_cleans_up(monkeypatch, tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    fs = FileService(p)
    temp = p.with_suffix(p.suffix + ".tmp")

    orig_replace = Path.replace

    def fake_replace(self: Path, target: Path) -> Path:
        if self == temp:
            raise OSError("replace fail")
        return orig_replace(self, target)

    monkeypatch.setattr(Path, "replace", fake_replace)

    with pytest.raises(VaultIOError) as exc:
        fs.write(b"payload")

    msg = str(exc.value)
    assert "write" in msg
    assert "replace fail" in msg
    assert str(p) in msg
    assert not temp.exists()


# ---------------------------------------------------------------------------
# delete()
# ---------------------------------------------------------------------------


def test_delete_success_when_file_exists(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    p.write_bytes(b"x")

    fs = FileService(p)
    fs.delete()

    assert not p.exists()


def test_delete_success_when_file_missing(tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    fs = FileService(p)

    # should not raise even if file is absent
    fs.delete()
    assert not p.exists()


def test_delete_permission_error_wrapped(monkeypatch, tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    p.write_bytes(b"x")
    fs = FileService(p)

    orig_unlink = Path.unlink

    def fake_unlink(self: Path, *a, **kw) -> None:
        if self == p:
            raise PermissionError("no delete")
        return orig_unlink(self, *a, **kw)

    monkeypatch.setattr(Path, "unlink", fake_unlink)

    with pytest.raises(VaultIOError) as exc:
        fs.delete()

    msg = str(exc.value)
    assert "delete" in msg
    assert "permission denied" in msg
    assert str(p) in msg


def test_delete_os_error_wrapped(monkeypatch, tmp_path) -> None:
    p = tmp_path / "vault.lbx"
    p.write_bytes(b"x")
    fs = FileService(p)

    orig_unlink = Path.unlink

    def fake_unlink(self: Path, *a, **kw) -> None:
        if self == p:
            raise OSError("delete fail")
        return orig_unlink(self, *a, **kw)

    monkeypatch.setattr(Path, "unlink", fake_unlink)

    with pytest.raises(VaultIOError) as exc:
        fs.delete()

    msg = str(exc.value)
    assert "delete" in msg
    assert "delete fail" in msg
    assert str(p) in msg
