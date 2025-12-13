"""Provides functionality for interacting with http/https paths"""

from __future__ import annotations

from typing import TYPE_CHECKING

from cmem_cmemc.smart_path.clients import StoragePath

if TYPE_CHECKING:
    from collections.abc import Generator


class HttpPath(StoragePath):
    """Client class for interacting with Amazon S3 storage.

    This class provides methods for working with http paths within the context
    of the `Path` application.
    """

    @property
    def suffix(self) -> str:
        """Return the suffix of the path."""
        raise NotImplementedError(f"suffix in {self.__class__} is not implemented yet.")

    @property
    def name(self) -> str:
        """Determine the name of the path."""
        return self.path.split("/")[-1]

    @property
    def parent(self) -> HttpPath:
        """The logical parent of the path."""
        raise NotImplementedError(f"parent in {self.__class__} is not implemented yet.")

    def is_dir(self) -> bool:
        """Determine if path is a directory or not."""
        return False

    def is_file(self) -> bool:
        """Determine if path is a file or not."""
        return not self.is_dir()

    def exists(self) -> bool:
        """Return the suffix of the path."""
        raise NotImplementedError(f"exists in {self.__class__} is not implemented yet.")

    def mkdir(self, parents: bool = False, exist_ok: bool = False) -> None:
        """Return the suffix of the path."""
        raise NotImplementedError(f"mkdir in {self.__class__} is not implemented yet.")

    def absolute(self) -> HttpPath:
        """Return an absolute version of this path"""
        raise NotImplementedError(f"absolute in {self.__class__} is not implemented yet.")

    def resolve(self) -> HttpPath:
        """Resolve the resolved path of the path."""
        raise NotImplementedError(f"resolve in {self.__class__} is not implemented yet.")

    def glob(self, pattern: str) -> Generator[StoragePath, StoragePath, StoragePath]:
        """Iterate over this subtree and yield all existing files"""
        raise NotImplementedError(f"glob in {self.__class__} is not implemented yet.")

    def __truediv__(self, key: str) -> HttpPath:
        """Return path with appending the key"""
        raise NotImplementedError(f"__truediv__ in {self.__class__} is not implemented yet.")
