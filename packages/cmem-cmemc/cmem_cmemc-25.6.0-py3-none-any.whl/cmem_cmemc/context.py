"""The main command line interface."""

import ast
import configparser
import json
import os
import re
import subprocess  # nosec
from datetime import datetime, timezone
from os import environ as env
from os import getenv
from pathlib import Path
from shutil import which

import click
import cmem.cmempy.config as cmempy_config
import urllib3
from cmem.cmempy.health import get_di_version, get_explore_version
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name
from rich import box
from rich.console import Console
from rich.table import Table
from urllib3.exceptions import InsecureRequestWarning

from cmem_cmemc.config_parser import PureSectionConfigParser
from cmem_cmemc.exceptions import InvalidConfigurationError
from cmem_cmemc.string_processor import StringProcessor, process_row
from cmem_cmemc.utils import is_enabled, str_to_bool

DI_TARGET_VERSION = "v25.3.0"

EXPLORE_TARGET_VERSION = "v25.3.0"

KNOWN_CONFIG_KEYS = {
    "CMEM_BASE_URI": cmempy_config.get_cmem_base_uri,
    "SSL_VERIFY": cmempy_config.get_ssl_verify,
    "REQUESTS_CA_BUNDLE": cmempy_config.get_requests_ca_bundle,
    "DP_API_ENDPOINT": cmempy_config.get_dp_api_endpoint,
    "DI_API_ENDPOINT": cmempy_config.get_di_api_endpoint,
    "KEYCLOAK_BASE_URI": cmempy_config.get_keycloak_base_uri,
    "KEYCLOAK_REALM_ID": cmempy_config.get_keycloak_realm_id,
    "OAUTH_TOKEN_URI": cmempy_config.get_oauth_token_uri,
    "OAUTH_GRANT_TYPE": cmempy_config.get_oauth_grant_type,
    "OAUTH_USER": cmempy_config.get_oauth_user,
    "OAUTH_PASSWORD": cmempy_config.get_oauth_password,
    "OAUTH_CLIENT_ID": cmempy_config.get_oauth_client_id,
    "OAUTH_CLIENT_SECRET": cmempy_config.get_oauth_client_secret,
    "OAUTH_ACCESS_TOKEN": cmempy_config.get_oauth_access_token,
}

KNOWN_SECRET_KEYS = ("OAUTH_PASSWORD", "OAUTH_CLIENT_SECRET", "OAUTH_ACCESS_TOKEN")

SSL_VERIFY_WARNING = "SSL verification is disabled (SSL_VERIFY=False)."


class ApplicationContext:
    """Context of the command line interface."""

    APP_NAME: str = "cmemc"
    DEFAULT_CONFIG_FILE: str = str(Path(click.get_app_dir(APP_NAME)) / "config.ini")
    DEFAULT_EXTERNAL_HTTP_TIMEOUT: int = 10

    debug: bool
    quiet: bool
    external_http_timeout: int
    config_dir: Path
    config_file: Path
    config: PureSectionConfigParser
    connection: str | None
    console: Console
    console_width: int | None = None

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods

    def __init__(
        self,
        config_file: str,
        connection: str | None = None,
        debug: bool = False,
        quiet: bool = False,
    ):
        """Initialize main context."""
        self.config_file = Path(config_file)
        self.app_name = "cmemc"
        self.set_debug(debug)
        self.set_quiet(quiet)
        self.ensure_app_config_dir()
        self.set_connection(connection)
        self.set_external_http_timeout(self.DEFAULT_EXTERNAL_HTTP_TIMEOUT)
        self.console = Console(markup=True, emoji_variant="emoji")
        self.update_console_width()

    @staticmethod
    def from_params(params: dict) -> "ApplicationContext":
        """Create an ApplicationContext instance from a dictionary.

        Expects 'config_file' key to be present in the dictionary.
        """
        config_file = params.get("config_file")
        debug = str_to_bool(str(params.get("debug")))
        quiet = str_to_bool(str(params.get("quiet")))
        external_http_timeout = (
            int(str(params.get("external_http_timeout")))
            if "external_http_timeout" in params
            else ApplicationContext.DEFAULT_EXTERNAL_HTTP_TIMEOUT
        )
        connection = str(params.get("connection")) if params.get("connection") else None
        if not config_file:
            raise ValueError("Missing required key: 'config_file' in config dictionary")
        app = ApplicationContext(
            config_file=config_file, connection=connection, debug=debug, quiet=quiet
        )
        app.set_external_http_timeout(external_http_timeout)
        if not app.debug:
            app.set_debug(is_enabled(params, app.get_config(), "debug"))
        if not app.quiet:
            app.set_quiet(is_enabled(params, app.get_config(), "quiet"))
        app.echo_debug(f"use config file: {app.config_file}")
        if app.connection:
            app.echo_debug(f"set connection: {app.connection}")
        defaults = app.get_defaults()
        app.apply_config(defaults)
        section_config = app.get_connection_config()
        app.clear_known_keys()
        app.apply_config(section_config)
        app.configure_cmempy()
        return app

    def update_console_width(self) -> None:
        """Update console width from environment variable."""
        console_width_env = getenv("CMEMC_CONSOLE_WIDTH", None)
        console_width = int(console_width_env) if isinstance(console_width_env, str) else None
        self.console_width = console_width
        if console_width is not None:
            self.console.width = console_width

    def get_template_data(self) -> dict[str, str]:
        """Get the template data dict with vars from the context."""
        data: dict[str, str] = {}
        today = str(datetime.now(tz=timezone.utc).date())
        data.update(date=today)
        if self.connection is not None:
            data.update(connection=self.connection)
        else:
            data.update(connection="unnamed")
        return data

    def set_debug(self, debug: bool = False) -> None:
        """Set debug state"""
        self.debug = debug

    def set_quiet(self, quiet: bool = False) -> None:
        """Set quiets state"""
        self.quiet = quiet

    def set_external_http_timeout(self, timeout: int) -> None:
        """Set external http timeout"""
        self.external_http_timeout = timeout
        os.environ["CMEMC_EXTERNAL_HTTP_TIMEOUT"] = str(timeout)

    def ensure_app_config_dir(self) -> None:
        """Ensure the application's configuration directory exists."""
        try:
            self.config_dir = Path(click.get_app_dir(self.app_name))
            self.config_dir.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError, FileNotFoundError):
            self.echo_debug(f"Could not create config directory {self.config_dir}")

    def set_config_file(self, config_file: str | None = None) -> None:
        """Set and return the context config file"""
        if config_file:
            self.config_file = Path(config_file)
        else:
            self.config_file = self.config_dir / "config.ini"
        self.echo_debug(f"Set config to {self.config_file.absolute()}")

    def get_defaults(self) -> dict[str, str]:
        """Populate missing values in `params` using defaults from the configuration."""
        config = self.get_config()
        defaults = dict(config.defaults())
        if "CMEMC_CONFIG_FILE" in defaults:
            defaults.pop("CMEMC_CONFIG_FILE")
        if "CMEMC_DEBUG" in defaults and self.debug:
            defaults.pop("CMEMC_DEBUG")
        if "CMEMC_QUIET" in defaults and self.quiet:
            defaults.pop("CMEMC_QUIET")
        if "CMEMC_CONNECTION" in defaults and self.connection:
            defaults.pop("CMEMC_CONNECTION")
        if (
            "CMEMC_EXTERNAL_HTTP_TIMEOUT" in defaults
            and self.external_http_timeout != self.DEFAULT_EXTERNAL_HTTP_TIMEOUT
        ):
            defaults.pop("CMEMC_EXTERNAL_HTTP_TIMEOUT")
        for key in defaults:
            if key in os.environ:
                defaults.pop(key)
        return defaults

    def get_connection_config(self) -> dict[str, str]:
        """Get connection section config"""
        if not self.connection:
            return {}
        config = dict(self.get_config()[self.connection])
        if "CMEMC_CONFIG_FILE" in config:
            config.pop("CMEMC_CONFIG_FILE")
        if "CMEMC_CONNECTION" in config:
            config.pop("CMEMC_CONNECTION")
        return config

    def apply_config(self, config: dict[str, str]) -> None:
        """Apply the configuration to the context."""
        for key, value in config.items():
            if key == "CMEMC_DEBUG":
                self.set_debug(str_to_bool(value))
            elif key == "CMEMC_QUIET":
                self.set_quiet(str_to_bool(value))
            elif key == "CMEMC_CONNECTION":
                self.echo_debug(f"set connection to {value}")
                self.set_connection(value)
            elif key == "CMEMC_EXTERNAL_HTTP_TIMEOUT":
                self.set_external_http_timeout(int(value))
            else:
                if key in KNOWN_SECRET_KEYS:
                    self.echo_debug(key + " set by config")
                else:
                    self.echo_debug(key + " set by config to " + value)
                env[key] = value

    def clear_known_keys(self) -> None:
        """Clear know keys if the connection is set."""
        if self.connection:
            # clear all known keys
            for key in KNOWN_CONFIG_KEYS:
                if key in env:
                    env.pop(key)

    def configure_cmempy(self) -> None:
        """Configure the cmempy API to use a new connection."""
        # With or without connection config, we do not want API stdout prints
        env["CMEMPY_IS_CHATTY"] = "False"
        if self.connection:
            config = self.get_config()[self.connection]
            # allow to fetch all secrets from an external process
            for _ in KNOWN_SECRET_KEYS:
                self.set_credential_from_process(_, _ + "_PROCESS", config)

            self.echo_debug(f"CA bundle loaded from {cmempy_config.get_requests_ca_bundle()}")
        # If cert validation is disabled, output a warning
        # Also disable library warnings:
        # https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
        if not cmempy_config.get_ssl_verify():
            self.echo_warning(SSL_VERIFY_WARNING)
            urllib3.disable_warnings(category=InsecureRequestWarning)

    @staticmethod
    def set_connection_from_params(params: dict) -> None:
        """Set connection and config by manually checking params (completion)."""
        app = ApplicationContext.from_params(params)
        defaults = app.get_defaults()
        app.apply_config(defaults)
        section_config = app.get_connection_config()
        app.clear_known_keys()
        app.apply_config(section_config)
        app.configure_cmempy()

    def set_connection(self, section_string: str | None = None) -> None:
        """Set connection config section based on section string."""
        self.connection = None
        if section_string is None or section_string == "":
            return
        if section_string not in self.get_config():
            raise InvalidConfigurationError(
                self,
                f"There is no connection '{section_string}' configured in "
                f"config '{self.config_file}'.",
            )
        self.connection = section_string

    def get_config_file(self) -> Path:
        """Check the connection config file."""
        if not self.config_file.exists():
            with self.config_file.open(mode="a", encoding="UTF-8"):
                self.echo_warning(f"Empty config created: {self.config_file.name}")
        return self.config_file

    def get_config(self) -> PureSectionConfigParser:
        """Parse the configuration"""
        config = PureSectionConfigParser()
        try:
            # https://stackoverflow.com/questions/1648517/
            config.read(self.get_config_file(), encoding="utf-8")
        except configparser.Error as error:
            raise InvalidConfigurationError(
                self,
                "The following config parser error needs to be fixed with your config file:\n"
                f"{error!s}\n"
                "You can use the 'config edit' command to fix this.",
            ) from error
        except Exception as error:  # noqa: BLE001
            self.echo_debug(f"Could not read config file - provide empty config: {error!s}")
        return config

    @staticmethod
    def is_completing() -> bool:
        """Test for environment which indicates that we are in completion mode.

        Returns true if in validation mode, otherwise false.

        Note: moved from utils due to circular imports

        Returns: boolean
        """
        comp_words = os.getenv("COMP_WORDS", default=None)
        cmemc_complete = os.getenv("_CMEMC_COMPLETE", default=None)
        if comp_words is not None:
            return True
        return cmemc_complete is not None

    @staticmethod
    def echo_warning(message: str, nl: bool = True, condition: bool = True) -> None:
        """Output a warning message."""
        if not condition:
            return
        if ApplicationContext.is_completing():
            return
        click.secho(message, fg="yellow", err=True, nl=nl)

    @staticmethod
    def echo_error(
        message: str | list[str], nl: bool = True, err: bool = True, prepend_line: bool = False
    ) -> None:
        """Output an error message.

        2024-05-17: also allows list of strings now
        2024-05-17: new prepend_line parameter
        """
        # pylint: disable=invalid-name
        click.echo("") if prepend_line is True else None
        messages: list[str] = [message] if isinstance(message, str) else message
        for _ in messages:
            click.secho(_, fg="red", err=err, nl=nl)

    def echo_debug(self, message: str | list[str]) -> None:
        """Output a debug message if --debug is enabled.

        2024-05-17: also allows list of strings now
        2025-04-07: extract output function
        """
        messages: list[str] = [message] if isinstance(message, str) else message
        if self.debug and not ApplicationContext.is_completing():
            self.echo_debug_string(messages)

    @staticmethod
    def echo_debug_string(message: str | list[str]) -> None:
        """Output a debug message"""
        messages: list[str] = [message] if isinstance(message, str) else message
        now = datetime.now(tz=timezone.utc)
        for _ in messages:
            click.secho(f"[{now!s}] {_}", err=True, dim=True)

    def echo_info(
        self,
        message: str | list[str] | set[str],
        nl: bool = True,
        fg: str = "",
        condition: bool = True,
    ) -> None:
        """Output one or more info messages, if not suppressed by --quiet.

        message: the string to output
        nl: True if newlines need to be added (default)
        fg: color
        condition: do nothing if False
        """
        if not condition:
            return
        if self.quiet:
            return
        if isinstance(message, str):
            click.secho(message, nl=nl, fg=fg)
            return
        if isinstance(message, list | set):
            for msg in message:
                click.secho(msg, nl=nl, fg=fg)

    def echo_info_json(self, object_: object) -> None:
        """Output a formatted and highlighted json as info message."""
        message = highlight(
            json.dumps(object_, indent=2),
            get_lexer_by_name("json"),
            get_formatter_by_name("terminal"),
        )
        self.echo_info(message)

    def echo_info_xml(self, document: str) -> None:
        """Output a formatted and highlighted XML as info message."""
        message = highlight(
            document,
            get_lexer_by_name("xml"),
            get_formatter_by_name("terminal"),
        )
        self.echo_info(message)

    def echo_info_table(  # noqa: PLR0913
        self,
        rows: list,
        headers: list[str],
        sort_column: int | None = None,
        caption: str | None = None,
        cell_processing: dict[int, StringProcessor] | None = None,
        empty_table_message: str | None = None,
    ) -> None:
        """Output a formatted and highlighted table as info message."""
        self.update_console_width()

        if len(rows) == 0 and empty_table_message:
            self.echo_warning(empty_table_message)
            return

        if sort_column is not None:
            rows = sorted(rows, key=lambda k: k[sort_column].lower())

        if cell_processing:
            rows = [process_row(row, cell_processing) for row in rows]

        table = Table(
            box=box.HEAVY,
            row_styles=["bold", ""],
            header_style="Yellow",
            border_style="Yellow",
        )
        if caption is not None:
            table.caption = caption
        for header in headers:
            table.add_column(header, overflow="fold")
        for row_source in rows:
            row = [str(cell) for cell in row_source]
            table.add_row(*row)
        self.console.print(table)

    def echo_info_sparql(self, query_text: str) -> None:
        """Output a formatted and highlighted sparql query as info message."""
        message = highlight(
            query_text, get_lexer_by_name("sparql"), get_formatter_by_name("terminal")
        )
        self.echo_info(message)

    def echo_success(self, message: str, nl: bool = True, condition: bool = True) -> None:
        """Output success message, if not suppressed by --quiet."""
        # pylint: disable=invalid-name
        self.echo_info(message, fg="green", nl=nl, condition=condition)

    @staticmethod
    def echo_result(message: str, nl: bool = True) -> None:
        """Output result message, can NOT be suppressed by --quiet."""
        # pylint: disable=invalid-name
        click.echo(message, nl=nl)

    def check_concrete_version(self, name: str, version: str, target_version: str) -> None:
        """Check and compare a concrete backend version against a concrete target version.

        Args:
        ----
            name: Name of the backend
            version: Version of the backend
            target_version: Target version of cmemc for this backend

        """
        # backend version
        if not (match := re.match(r"^v([0-9]+)\.([0-9]+)(.*)?$", version)):
            self.echo_warning(f"There was an error checking the {name} version.")
            return
        year = int(match.group(1))
        major = int(match.group(2))
        # target version
        if not (target_match := re.match(r"^v([0-9]+)\.([0-9]+)(.*)?$", target_version)):
            self.echo_warning(f"There was an error checking the {name} version.")
            return
        target_year = int(target_match.group(1))
        target_major = int(target_match.group(2))
        if year < target_year or (year == target_year and major < target_major):
            self.echo_warning(
                f"Your {name} version v{year}.{major} is lower than the "
                f"target version of your cmemc deployment (v{target_year}.{target_major}).\n"
                "Some feature may be not supported with this backend."
            )

    def check_versions(self) -> None:
        """Check server versions against supported versions."""
        # check Explore version
        self.check_concrete_version(
            name="Explore", version=get_explore_version(), target_version=EXPLORE_TARGET_VERSION
        )
        self.check_concrete_version(
            name="DataIntegration", version=get_di_version(), target_version=DI_TARGET_VERSION
        )

    def set_credential_from_process(
        self, pw_key: str, command_key: str, config: configparser.SectionProxy
    ) -> None:
        """Set a credential env var from the output of an external process.

        Execute a command from the config key command_key and set/overwrite
        the environment variable pw_key with the first line of stdout of
        this process.

        Both stdout and stderr are captured. Output is not shown.

        Args:
        ----
            pw_key (str): the env variable which is created/set
            command_key (str): the env variable which holds the command
            config: the config object

        """
        if command_key not in config:
            return
        self.echo_debug(f"Fetching {pw_key} from external process.")
        command = str(config.get(command_key))
        parsed_list = None
        # first, we try to find command in PATH
        if which(command) is None:
            try:
                # if not in PATH, we try to parse it as list
                parsed_list = list(ast.literal_eval(command))
            except SyntaxError as error:
                raise ValueError(
                    f"'{command}' could not be found in PATH or the value "
                    "could not be parsed as list, e.g. ['echo', 'this']."
                ) from error
            # else: if it is a parsed list, we try to find the first element only
            if which(parsed_list[0]) is None:
                raise ValueError(f"'{parsed_list[0]}' could not be found in PATH.")
            parsed_list[0] = which(parsed_list[0])
        checked_command = parsed_list if parsed_list is not None else command
        if env.get("CMEMC_CREDENTIAL_PROCESS_NO_WARNING", "false") != "true":
            self.echo_warning(
                "Consider possible security implications associated with "
                "executing the external credential process:\n"
                f"{checked_command}\n"
                "You can suppress this warning by setting "
                "CMEMC_CREDENTIAL_PROCESS_NO_WARNING to 'true'."
                ""
            )
        self.echo_debug(f"External credential process started {checked_command}")
        split_output = (
            subprocess.run(  # nosec  # noqa: S603
                checked_command,
                capture_output=True,
                check=True,
            )
            .stdout.decode("utf-8")
            .splitlines()
        )
        if len(split_output) == 0:
            raise ValueError(
                f"The configured credential process '{checked_command}' "
                "did not produce any output on stdout."
            )
        pw_value = split_output[0]
        # set the password environment variable
        env[pw_key] = pw_value
