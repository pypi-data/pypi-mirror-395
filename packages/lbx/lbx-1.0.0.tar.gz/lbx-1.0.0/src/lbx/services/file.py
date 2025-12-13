# SPDX-FileCopyrightText: 2025-present Jitesh Sahani (JD) <jitesh.sahani@outlook.com>
#
# SPDX-License-Identifier: MIT

"""File operations for Lbx vault storage.

This module provides FileService for reading, writing, and deleting vault
files on disk. All I/O errors are wrapped in Lbx-specific exceptions to keep
the public API consistent.
"""

from __future__ import annotations

from pathlib import Path

from lbx.exceptions import VaultIOError, VaultNotFoundError
from lbx.settings import default_vault_path


class FileService:
    """File operations for vault storage.

    This service abstracts basic filesystem interactions used by the vault:

    * Checking whether the vault file exists.
    * Reading the vault file as raw bytes.
    * Writing the vault file atomically.
    * Deleting the vault file.

    All filesystem-related errors are mapped to VaultIOError or
    VaultNotFoundError.
    """

    __slots__ = ("_path",)

    def __init__(self, path: Path | str | None = None) -> None:
        """Initialize a FileService.

        If `path` is not provided, the default path
        `DEFAULT_DIR / DEFAULT_NAME` (for example, `~/.lbx/vault.lbx`) is used.

        Args:
            path (Path | str | None): Optional path to the vault file. May be a
                Path instance, string, or None to use the default location.
        """
        if path is None:
            path = default_vault_path()
        self._path: Path = Path(path)

    @property
    def path(self) -> Path:
        """Return the path of the vault file.

        Returns:
            Path: Path to the vault file.
        """
        return self._path

    def exists(self) -> bool:
        """Check whether the vault file exists.

        Returns:
            bool: True if the path exists and is a regular file, False
            otherwise.
        """
        return self._path.is_file()

    def read(self) -> bytes:
        """Read the vault file.

        Returns:
            bytes: Raw bytes read from the vault file.

        Raises:
            VaultNotFoundError: If the file does not exist.
            VaultIOError: If the file cannot be read due to permission or
                other OS errors.
        """
        if not self._path.exists():
            raise VaultNotFoundError(str(self._path))

        try:
            return self._path.read_bytes()
        except PermissionError as e:
            raise VaultIOError("read", str(self._path), "permission denied") from e
        except OSError as e:
            raise VaultIOError("read", str(self._path), str(e)) from e

    def write(self, data: bytes) -> None:
        """Write the vault file using an atomic save.

        The data is first written to a temporary `.tmp` file in the same
        directory and then moved into place using `Path.replace`. If an error
        occurs during write or replace, the temporary file is removed.

        Args:
            data (bytes): Serialized vault data to write.

        Raises:
            VaultIOError: If the directory cannot be created or the file
                cannot be written due to permission or other OS errors.
        """
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise VaultIOError(
                "create directory",
                str(self._path.parent),
                "permission denied",
            ) from e
        except OSError as e:
            raise VaultIOError(
                "create directory",
                str(self._path.parent),
                str(e),
            ) from e

        temp = self._path.with_suffix(self._path.suffix + ".tmp")
        try:
            temp.write_bytes(data)
            temp.replace(self._path)
        except PermissionError as e:
            temp.unlink(missing_ok=True)
            raise VaultIOError("write", str(self._path), "permission denied") from e
        except OSError as e:
            temp.unlink(missing_ok=True)
            raise VaultIOError("write", str(self._path), str(e)) from e

    def delete(self) -> None:
        """Delete the vault file.

        If the file does not exist, the operation is a no-op.

        Raises:
            VaultIOError: If the file cannot be deleted due to permission
                or other OS errors.
        """
        try:
            self._path.unlink(missing_ok=True)
        except PermissionError as e:
            raise VaultIOError("delete", str(self._path), "permission denied") from e
        except OSError as e:
            raise VaultIOError("delete", str(self._path), str(e)) from e
