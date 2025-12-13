"""Custom Click smart_path ParamType"""

import os
from typing import IO, Any

import click
import smart_open
from click.core import Context, Parameter
from smart_open import compression

from cmem_cmemc.context import ApplicationContext


class ClickSmartPath(click.Path):
    """Custom Click smart_path ParamType"""

    name = "click-smart-path"

    def __init__(  # noqa: PLR0913
        self,
        exists: bool = False,
        file_okay: bool = True,
        dir_okay: bool = True,
        writable: bool = False,
        readable: bool = True,
        resolve_path: bool = False,
        allow_dash: bool = False,
        remote_okay: bool = False,
    ):
        super().__init__(
            exists=exists,
            file_okay=file_okay,
            dir_okay=dir_okay,
            writable=writable,
            readable=readable,
            resolve_path=resolve_path,
            allow_dash=allow_dash,
        )
        self.remote_okay = remote_okay

    def convert(
        self,
        value: str | os.PathLike[str],
        param: Parameter | None,
        ctx: Context | None,
    ) -> str | bytes | os.PathLike[str]:
        """Convert the given value"""
        try:
            parsed_path = smart_open.parse_uri(value)
        except NotImplementedError as exe:
            self.fail(f"{exe}", param, ctx)
        if parsed_path.scheme == "file":
            return super().convert(parsed_path.uri_path, param, ctx)
        if not self.remote_okay:
            self.fail("Remote path not supported", param, ctx)

        return value

    @staticmethod
    def open(
        file_path: str, mode: str = "rb", transport_params: dict[str, Any] | None = None
    ) -> IO:
        """Open the file and return the file handle."""
        if file_path == "-":
            return click.open_file(file_path, mode=mode)
        if transport_params is None:
            transport_params = {}
        transport_params["timeout"] = os.getenv(
            "CMEM_TRANSPORT_TIMEOUT", ApplicationContext.DEFAULT_EXTERNAL_HTTP_TIMEOUT
        )
        return smart_open.open(  # type: ignore[no-any-return]
            file_path,
            mode,
            transport_params=transport_params,
            compression=compression.NO_COMPRESSION,
        )
