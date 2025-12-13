"""Client module to handle Path API calls."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


class StoragePath(ABC):
    """Storage path interface."""

    def __init__(self, path: str):
        self.path = path

    @property
    @abstractmethod
    def suffix(self) -> str:
        """Return the suffix of the path."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the file name."""

    @property
    @abstractmethod
    def parent(self) -> StoragePath:
        """The logical parent of the path."""

    @abstractmethod
    def is_dir(self) -> bool:
        """Check if the path is a directory."""

    @abstractmethod
    def is_file(self) -> bool:
        """Check if the path is a file."""

    @abstractmethod
    def exists(self) -> bool:
        """Check if the path exists."""

    @abstractmethod
    def mkdir(self, parents: bool = False, exist_ok: bool = False) -> None:
        """Create a directory."""

    @abstractmethod
    def absolute(self) -> StoragePath:
        """Return an absolute version of this path"""

    def resolve(self) -> StoragePath:
        """Resolve the resolved path of the path."""
        raise NotImplementedError(f"resolve in {self.__class__} is not implemented yet.")

    @abstractmethod
    def glob(self, pattern: str) -> Generator[StoragePath, StoragePath, StoragePath]:
        """Iterate over this subtree and yield all existing files"""

    @abstractmethod
    def __truediv__(self, key: str) -> StoragePath:
        """Return StoragePath with appending the key to the exising path"""
