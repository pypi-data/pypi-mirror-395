"""Provides client classes for interacting with different storage systems."""

from __future__ import annotations

import os
import urllib.parse
from pathlib import Path
from typing import IO, TYPE_CHECKING, ClassVar

import smart_open

from cmem_cmemc.smart_path.clients.http import HttpPath

if TYPE_CHECKING:
    from collections.abc import Generator

    from cmem_cmemc.smart_path.clients import StoragePath


class SmartPath:
    """Smart path"""

    SUPPORTED_SCHEMAS: ClassVar = {
        "file": Path,
        "http": HttpPath,
        "https": HttpPath,
    }

    def __init__(self, path: str):
        self.path = path
        self.schema = self._sniff_schema(self.path)
        if self.schema not in self.SUPPORTED_SCHEMAS:
            raise NotImplementedError(f"Schema '{self.schema}' not supported")
        self._client: StoragePath = self.SUPPORTED_SCHEMAS.get(self.schema)(self.path)

    @staticmethod
    def _sniff_schema(path: str) -> str:
        """Return the scheme of the URL only, as a string."""
        #
        # urlsplit doesn't work on Windows -- it parses the drive as the scheme...
        # no protocol given => assume a local file
        #
        if os.name == "nt" and "://" not in path:
            path = "file://" + path
        schema = urllib.parse.urlsplit(path).scheme
        return schema if schema else "file"

    def is_dir(self) -> bool:
        """Determine if path is a directory or not."""
        return self._client.is_dir()

    def is_file(self) -> bool:
        """Return the suffix of the path."""
        return self._client.is_file()

    def exists(self) -> bool:
        """Determine if path exists or not."""
        return self._client.exists()

    @property
    def suffix(self) -> str:
        """Return the suffix of the path."""
        return self._client.suffix

    @property
    def parent(self) -> StoragePath:
        """The logical parent of the path."""
        return self._client.parent

    @property
    def name(self) -> str:
        """Determine the name of the path."""
        return self._client.name

    def open(self, mode: str = "r", encoding: str | None = None) -> IO:
        """Open the file pointed by this path."""
        file: IO = smart_open.open(self.path, mode=mode, encoding=encoding)
        return file

    def mkdir(self, parents: bool = False, exist_ok: bool = False) -> None:
        """Return the suffix of the path."""
        self._client.mkdir(parents=parents, exist_ok=exist_ok)

    def glob(self, pattern: str) -> Generator[StoragePath, StoragePath, StoragePath]:
        """Iterate over this subtree and yield all existing files"""
        return self._client.glob(pattern=pattern)

    def resolve(self) -> StoragePath:
        """Iterate over this subtree and yield all existing files"""
        return self._client.resolve()

    def __truediv__(self, key: str) -> StoragePath:
        """Return StoragePath with appending the key to the exising path"""
        return self._client.__truediv__(key)
