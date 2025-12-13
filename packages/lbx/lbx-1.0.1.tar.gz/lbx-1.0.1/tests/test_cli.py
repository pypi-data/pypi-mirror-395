# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from lbx import cli
from lbx.exceptions import DecryptionError, LbxError


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# ---------------------------------------------------------------------------
# Helpers: build_lbx / ensure_unlocked / retry_on_bad_key / read_secret_value
# ---------------------------------------------------------------------------


def test_build_lbx_uses_keychain(monkeypatch: pytest.MonkeyPatch) -> None:
    called: dict[str, Any] = {}

    class DummyLbx:
        def __init__(self, path: Path | None, use_keychain: bool) -> None:
            called["path"] = path
            called["use_keychain"] = use_keychain

    monkeypatch.setattr(cli, "Lbx", DummyLbx)

    vault_path = Path("/tmp/vault.lbx")
    result = cli.build_lbx(vault_path)

    assert isinstance(result, DummyLbx)
    assert called["path"] is vault_path
    assert called["use_keychain"] is True


def test_ensure_unlocked_noop_when_already_unlocked() -> None:
    class Dummy:
        def __init__(self) -> None:
            self.is_unlocked = True
            self.unlock_from_keychain_called = False
            self.unlock_called = False

        def unlock_from_keychain(self) -> bool:
            self.unlock_from_keychain_called = True
            return True

        def unlock(self, password: str) -> None:
            self.unlock_called = True

    d = Dummy()
    cli.ensure_unlocked(d)

    assert d.unlock_from_keychain_called is False
    assert d.unlock_called is False


def test_ensure_unlocked_unlocks_via_keychain(monkeypatch: pytest.MonkeyPatch) -> None:
    class Dummy:
        def __init__(self) -> None:
            self.is_unlocked = False
            self.keychain_called = False
            self.unlock_called = False

        def unlock_from_keychain(self) -> bool:
            self.keychain_called = True
            self.is_unlocked = True
            return True

        def unlock(self, password: str) -> None:
            self.unlock_called = True

    d = Dummy()
    # getpass should never be called on this path
    monkeypatch.setattr(cli.getpass, "getpass", lambda _: pytest.fail("should not prompt"))
    cli.ensure_unlocked(d)

    assert d.keychain_called is True
    assert d.unlock_called is False
    assert d.is_unlocked is True


def test_ensure_unlocked_fallback_when_keychain_false(monkeypatch: pytest.MonkeyPatch) -> None:
    class Dummy:
        def __init__(self) -> None:
            self.is_unlocked = False
            self.keychain_called = False
            self.unlock_password: str | None = None

        def unlock_from_keychain(self) -> bool:
            self.keychain_called = True
            return False

        def unlock(self, password: str) -> None:
            self.unlock_password = password
            self.is_unlocked = True

    d = Dummy()

    monkeypatch.setattr(cli.getpass, "getpass", lambda _: "pw123")
    cli.ensure_unlocked(d)

    assert d.keychain_called is True
    assert d.unlock_password == "pw123"
    assert d.is_unlocked is True


def test_ensure_unlocked_fallback_when_keychain_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    class Dummy:
        def __init__(self) -> None:
            self.is_unlocked = False
            self.keychain_called = False
            self.unlock_password: str | None = None

        def unlock_from_keychain(self) -> bool:
            self.keychain_called = True
            raise LbxError("keychain broken")

        def unlock(self, password: str) -> None:
            self.unlock_password = password
            self.is_unlocked = True

    d = Dummy()

    monkeypatch.setattr(cli.getpass, "getpass", lambda _: "pw456")
    cli.ensure_unlocked(d)

    assert d.keychain_called is True
    assert d.unlock_password == "pw456"
    assert d.is_unlocked is True


def test_retry_on_bad_key_success_no_retry() -> None:
    class Dummy:
        def __init__(self) -> None:
            self.unlocked_with: str | None = None

        def unlock(self, password: str) -> None:
            self.unlocked_with = password

    d = Dummy()

    def func(x: int) -> int:
        return x + 1

    result = cli.retry_on_bad_key(d, func, 10)
    assert result == 11
    assert d.unlocked_with is None


def test_retry_on_bad_key_retries_on_decryption_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class Dummy:
        def __init__(self) -> None:
            self.unlocked_with: str | None = None

        def unlock(self, password: str) -> None:
            self.unlocked_with = password

    d = Dummy()
    calls = {"count": 0}

    def func(x: int) -> int:
        calls["count"] += 1
        if calls["count"] == 1:
            raise DecryptionError("bad key")
        return x * 2

    monkeypatch.setattr(cli.getpass, "getpass", lambda _: "pw789")

    result = cli.retry_on_bad_key(d, func, 5)

    assert result == 10
    assert calls["count"] == 2
    assert d.unlocked_with == "pw789"


def test_read_secret_value_prefers_value_opt() -> None:
    value = cli.read_secret_value("name", "provided")
    assert value == "provided"


def test_read_secret_value_reads_from_stdin_when_not_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeStdin:
        def isatty(self) -> bool:
            return False

        def read(self) -> str:
            return "HELLO\n"

    monkeypatch.setattr(cli.sys, "stdin", FakeStdin())
    value = cli.read_secret_value("name", None)
    assert value == "HELLO"


def test_read_secret_value_prompts_when_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeStdin:
        def isatty(self) -> bool:
            return True

    monkeypatch.setattr(cli.sys, "stdin", FakeStdin())
    monkeypatch.setattr(cli.getpass, "getpass", lambda _: "from-prompt")

    value = cli.read_secret_value("name", None)
    assert value == "from-prompt"


# ---------------------------------------------------------------------------
# CLI: vault commands
# ---------------------------------------------------------------------------


def test_vault_init_success(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = path or Path("/tmp/vault.lbx")
            self.created_with: str | None = None

        def create(self, password: str) -> None:
            self.created_with = password

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))
    passwords = ["secret", "secret"]
    monkeypatch.setattr(cli.getpass, "getpass", lambda _: passwords.pop(0))

    result = runner.invoke(cli.lbx, ["vault", "init"])

    assert result.exit_code == 0
    assert "Vault created at" in result.output


def test_vault_init_password_mismatch(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = path or Path("/tmp/vault.lbx")
            self.create_called = False

        def create(self, password: str) -> None:
            self.create_called = True

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))
    passwords = ["one", "two"]
    monkeypatch.setattr(cli.getpass, "getpass", lambda _: passwords.pop(0))

    result = runner.invoke(cli.lbx, ["vault", "init"])

    assert result.exit_code == 1
    assert "Error: passwords do not match" in result.output


def test_vault_unlock(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = path
            self.unlocked_with: str | None = None

        def unlock(self, password: str) -> None:
            self.unlocked_with = password

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))
    monkeypatch.setattr(cli.getpass, "getpass", lambda _: "pw-unlock")

    result = runner.invoke(cli.lbx, ["vault", "unlock"])

    assert result.exit_code == 0
    assert "Vault unlocked" in result.output


def test_vault_lock(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = path
            self.lock_called = False

        def lock(self) -> None:
            self.lock_called = True

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))

    result = runner.invoke(cli.lbx, ["vault", "lock"])

    assert result.exit_code == 0
    assert "Vault locked." in result.output


def test_vault_delete_abort(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = Path("/tmp/vault.lbx")
            self.deleted = False

        def delete_vault(self) -> None:
            self.deleted = True

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli.click, "prompt", lambda *a, **k: "NOPE")

    result = runner.invoke(cli.lbx, ["vault", "delete"])

    assert result.exit_code == 1
    assert "Aborted." in result.output
    assert dummy.deleted is False


def test_vault_delete_confirm(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = Path("/tmp/vault.lbx")
            self.deleted = False

        def delete_vault(self) -> None:
            self.deleted = True

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli.click, "prompt", lambda *a, **k: "DELETE")

    result = runner.invoke(cli.lbx, ["vault", "delete"])

    assert result.exit_code == 0
    assert "Vault and keychain entry deleted." in result.output
    assert dummy.deleted is True


def test_vault_status_not_found(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = Path("/tmp/vault.lbx")

        def exists(self) -> bool:
            return False

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))

    result = runner.invoke(cli.lbx, ["vault", "status"])

    assert result.exit_code == 0
    assert "Vault: not found" in result.output


def test_vault_status_locked_and_unlocked(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None, unlocked: bool) -> None:
            self.path = Path("/tmp/vault.lbx")
            self._unlocked = unlocked

        def exists(self) -> bool:
            return True

        @property
        def is_unlocked(self) -> bool:
            return self._unlocked

    # locked
    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault, False))
    result_locked = runner.invoke(cli.lbx, ["vault", "status"])
    assert "Status: locked" in result_locked.output

    # unlocked
    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault, True))
    result_unlocked = runner.invoke(cli.lbx, ["vault", "status"])
    assert "Status: unlocked" in result_unlocked.output


# ---------------------------------------------------------------------------
# CLI: service commands
# ---------------------------------------------------------------------------


def test_service_list(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            pass

        def list_services(self) -> list[str]:
            return ["github", "gitlab"]

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))

    result = runner.invoke(cli.lbx, ["service", "list"])

    assert result.exit_code == 0
    lines = [_.strip() for _ in result.output.splitlines() if _.strip()]
    assert lines == ["github", "gitlab"]


def test_service_rename(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.calls: list[tuple[str, str]] = []

        def rename_service(self, old: str, new: str) -> None:
            self.calls.append((old, new))

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)

    result = runner.invoke(cli.lbx, ["service", "rename", "oldsvc", "newsvc"])

    assert result.exit_code == 0
    assert dummy.calls == [("oldsvc", "newsvc")]
    assert "oldsvc" in result.output
    assert "newsvc" in result.output


def test_service_delete(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.deleted: list[str] = []

        def delete_service(self, name: str) -> None:
            self.deleted.append(name)

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)

    result = runner.invoke(cli.lbx, ["service", "delete", "svc"])

    assert result.exit_code == 0
    assert dummy.deleted == ["svc"]
    assert "Deleted service 'svc'" in result.output


# ---------------------------------------------------------------------------
# CLI: secret commands
# ---------------------------------------------------------------------------


def test_secret_list_without_service_filter(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            pass

        def list_secrets(self, service: str | None) -> list[tuple[str, str]]:
            assert service is None
            return [("svc1", "name1"), ("svc2", "name2")]

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))

    result = runner.invoke(cli.lbx, ["secret", "list"])

    assert result.exit_code == 0
    lines = [_.strip() for _ in result.output.splitlines() if _.strip()]
    assert "svc1:name1" in lines
    assert "svc2:name2" in lines


def test_secret_list_with_service_filter(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            pass

        def list_secrets(self, service: str | None) -> list[tuple[str, str]]:
            assert service == "svc"
            return [("svc", "name1"), ("svc", "name2")]

    monkeypatch.setattr(cli, "build_lbx", lambda vault: DummyLbx(vault))

    result = runner.invoke(cli.lbx, ["secret", "list", "--service", "svc"])

    assert result.exit_code == 0
    lines = [_.strip() for _ in result.output.splitlines() if _.strip()]
    assert lines == ["name1", "name2"]


def test_secret_add_uses_read_secret_value(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.added: list[tuple[str, str, str]] = []

        def add_secret(self, service: str, name: str, value: str) -> None:
            self.added.append((service, name, value))

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)
    monkeypatch.setattr(cli, "read_secret_value", lambda n, v: f"VAL-{n}")

    result = runner.invoke(cli.lbx, ["secret", "add", "svc", "name"])

    assert result.exit_code == 0
    assert dummy.added == [("svc", "name", "VAL-name")]
    assert "Added svc:name" in result.output


def test_secret_update(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.updated: list[tuple[str, str, str]] = []

        def update_secret(self, service: str, name: str, value: str) -> None:
            self.updated.append((service, name, value))

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)
    monkeypatch.setattr(cli, "read_secret_value", lambda n, v: f"NEW-{n}")

    result = runner.invoke(cli.lbx, ["secret", "update", "svc", "name"])

    assert result.exit_code == 0
    assert dummy.updated == [("svc", "name", "NEW-name")]
    assert "Updated svc:name" in result.output


def test_secret_rename(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.renamed: list[tuple[str, str, str]] = []

        def rename_secret(self, service: str, old: str, new: str) -> None:
            self.renamed.append((service, old, new))

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)

    result = runner.invoke(cli.lbx, ["secret", "rename", "svc", "old", "new"])

    assert result.exit_code == 0
    assert dummy.renamed == [("svc", "old", "new")]
    assert "svc:old -> svc:new" in result.output


def test_secret_move(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.moved: list[tuple[str, str, str]] = []

        def move_secret(self, source: str, name: str, target: str) -> None:
            self.moved.append((source, name, target))

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)

    result = runner.invoke(cli.lbx, ["secret", "move", "src", "name", "dst"])

    assert result.exit_code == 0
    assert dummy.moved == [("src", "name", "dst")]
    assert "src:name -> dst:name" in result.output


def test_secret_delete(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.deleted: list[tuple[str, str]] = []

        def delete_secret(self, service: str, name: str) -> None:
            self.deleted.append((service, name))

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)

    result = runner.invoke(cli.lbx, ["secret", "delete", "svc", "name"])

    assert result.exit_code == 0
    assert dummy.deleted == [("svc", "name")]
    assert "Deleted svc:name" in result.output


def test_secret_get_uses_retry_on_bad_key(monkeypatch: pytest.MonkeyPatch, runner: CliRunner) -> None:
    class DummyEntry:
        def __init__(self, value: str) -> None:
            self.value = value

    class DummyLbx:
        def __init__(self, path: Path | None) -> None:
            self.path = path

        # This will never actually be used because we stub retry_on_bad_key,
        # but it must exist so `s.get_secret` attribute access succeeds.
        def get_secret(self, service: str, name: str) -> DummyEntry:
            raise AssertionError("get_secret should not be called directly in this test")

    dummy = DummyLbx(None)
    monkeypatch.setattr(cli, "build_lbx", lambda vault: dummy)
    monkeypatch.setattr(cli, "ensure_unlocked", lambda s: None)

    def fake_retry(lbx_obj: Any, func: Any, *a: Any, **kw: Any) -> DummyEntry:
        return DummyEntry("VALUE123")

    monkeypatch.setattr(cli, "retry_on_bad_key", fake_retry)

    result = runner.invoke(cli.lbx, ["secret", "get", "svc", "name"])

    assert result.exit_code == 0
    assert "VALUE123" in result.output


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def test_main_success(monkeypatch: pytest.MonkeyPatch, capsys: Any) -> None:
    called = {"n": 0}

    def fake_lbx() -> None:
        called["n"] += 1

    monkeypatch.setattr(cli, "lbx", fake_lbx)

    cli.main()

    assert called["n"] == 1
    captured = capsys.readouterr()
    # no error output
    assert captured.err == ""


def test_main_wraps_lbx_error(monkeypatch: pytest.MonkeyPatch, capsys: Any) -> None:
    def failing_lbx() -> None:
        raise LbxError("boom")

    monkeypatch.setattr(cli, "lbx", failing_lbx)

    with pytest.raises(SystemExit) as excinfo:
        cli.main()

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error: boom" in captured.err
