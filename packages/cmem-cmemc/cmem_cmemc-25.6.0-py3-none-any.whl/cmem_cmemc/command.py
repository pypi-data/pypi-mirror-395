"""cmemc Click Command"""

from subprocess import CalledProcessError
from typing import Any

import click
import requests
from click_help_colors import HelpColorsCommand

from cmem_cmemc.exceptions import CmemcError
from cmem_cmemc.utils import extract_error_message


class CmemcCommand(HelpColorsCommand):
    """Wrapper click.Command class to have a single extension point.

    Currently, wrapped click extensions and additional group features:#
    - click-help-colors: https://github.com/click-contrib/click-help-colors
    """

    color_for_headers = "yellow"
    color_for_options = "green"

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        """Init a cmemc group command."""
        kwargs.setdefault("help_headers_color", self.color_for_headers)
        kwargs.setdefault("help_options_color", self.color_for_options)
        super().__init__(*args, **kwargs)

    def invoke(self, ctx: click.core.Context) -> Any:  # noqa: ANN401
        """Execute the command and handles known exceptions by wrapping them in a CmemcError.

        This method overrides the default Click command invocation to catch a predefined
        set of exceptions (such as OSError, HTTPError, ValueError, etc.) and re-raises them
        as a unified CmemcError. This allows consistent error handling and messaging across
        all CLI commands.

        Args:
            ctx (click.core.Context): The Click context for the command.

        Raises:
            CmemcError: Wraps any of the caught exceptions and attaches context-specific data.

        """
        try:
            return super().invoke(ctx)
        except (
            OSError,
            CalledProcessError,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            ValueError,
            NotImplementedError,
            KeyError,
        ) as e:
            raise CmemcError(ctx.obj, extract_error_message(e, True)) from e
