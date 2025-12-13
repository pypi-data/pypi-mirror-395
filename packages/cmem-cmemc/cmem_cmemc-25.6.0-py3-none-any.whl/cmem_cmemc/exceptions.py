"""Declares all cli exceptions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cmem_cmemc.context import ApplicationContext


class CmemcError(ValueError):
    """Base exception for CMEM-CMEMC-related errors."""

    def __init__(self, app: "ApplicationContext", *args: str):
        super().__init__(*args)
        self.app = app


class InvalidConfigurationError(CmemcError):
    """The configuration given was not found or is broken."""


class ServerError(CmemcError):
    """The server reported an error with a process."""
