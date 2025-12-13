"""The main command line interface."""

import os
import sys
import traceback
from importlib.resources import open_text
from os import environ as env

import click

from cmem_cmemc import completion
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.commands import (
    admin,
    config,
    dataset,
    graph,
    manual,
    project,
    query,
    vocabulary,
    workflow,
)
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.exceptions import CmemcError
from cmem_cmemc.utils import check_python_version, extract_error_message, get_version

CMEMC_VERSION = get_version()

# this will output a custom zsh completion function
if os.environ.get("_CMEMC_COMPLETE", "") == "zsh_source":
    with open_text("cmem_cmemc", "_cmemc.zsh") as zsh_output:
        click.secho(zsh_output.read())
    sys.exit(0)

version = sys.version_info
PYTHON_VERSION = f"{version.major}.{version.minor}.{version.micro}"
check_python_version(ctx=ApplicationContext)

# set the user-agent environment for the http request headers
os.environ["CMEM_USER_AGENT"] = f"cmemc/{CMEMC_VERSION} (Python {PYTHON_VERSION})"

# https://github.com/pallets/click/blob/master/examples/complex/complex/cli.py
CONTEXT_SETTINGS = {"auto_envvar_prefix": "CMEMC", "help_option_names": ["-h", "--help"]}


@click.group(name="cmemc", cls=CmemcGroup, context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c",
    "--connection",
    type=click.STRING,
    shell_complete=completion.connections,
    help="Use a specific connection from the config file.",
)
@click.option(
    "--config-file",
    shell_complete=completion.ini_files,
    type=click.Path(readable=True, allow_dash=False, dir_okay=False),
    default=ApplicationContext.DEFAULT_CONFIG_FILE,
    show_default=f"Using {env['CMEMC_CONFIG_FILE']} "
    f"instead of {ApplicationContext.DEFAULT_CONFIG_FILE}"
    if "CMEMC_CONFIG_FILE" in env
    else ApplicationContext.DEFAULT_CONFIG_FILE,
    help="Use this config file instead of the default one.",
)
@click.option("-q", "--quiet", is_flag=True, help="Suppress any non-error info messages.")
@click.option(
    "-d", "--debug", is_flag=True, help="Output debug messages and stack traces after errors."
)
@click.option(
    "--external-http-timeout",
    default=ApplicationContext.DEFAULT_EXTERNAL_HTTP_TIMEOUT,
    type=int,
    show_default=True,
    help="Timeout in seconds for external HTTP requests.",
)
@click.version_option(
    version=CMEMC_VERSION,
    message="%(prog)s, version %(version)s, " f"running under python {PYTHON_VERSION}",
)
@click.pass_context
def cli(  # noqa: PLR0913
    ctx: click.core.Context,
    debug: bool,
    quiet: bool,
    config_file: str,
    connection: str,
    external_http_timeout: int,
) -> None:
    """Eccenca Corporate Memory Control (cmemc).

    cmemc is the eccenca Corporate Memory Command Line Interface (CLI).

    Available commands are grouped by affecting resource type (such as graph,
    project and query).
    Each command and group has a separate --help screen for detailed
    documentation.
    In order to see possible commands in a group, simply
    execute the group command without further parameter (e.g. cmemc project).

    If your terminal supports colors, these coloring rules are applied:
    Groups are colored in white; Commands which change data are colored in
    red; all other commands as well as options are colored in green.

    Please also have a look at the cmemc online documentation:

                        https://eccenca.com/go/cmemc

    cmemc is © 2025 eccenca GmbH, licensed under the Apache License 2.0.
    """
    _ = connection, debug, quiet, config_file, external_http_timeout
    if " ".join(sys.argv).find("config edit") != -1:
        app = ApplicationContext(config_file=config_file, debug=debug, quiet=quiet)
    else:
        app = ApplicationContext.from_params(params=ctx.params)
    ctx.obj = app


cli.add_command(admin.admin)
cli.add_command(config.config)
cli.add_command(dataset.dataset)
cli.add_command(graph.graph)
cli.add_command(project.project)
cli.add_command(query.query)
cli.add_command(vocabulary.vocabulary)
cli.add_command(workflow.workflow)
cli.add_command(manual.manual_command)


def main() -> None:
    """Start the command line interface."""
    try:
        cli()  # pylint: disable=no-value-for-parameter
    except CmemcError as error:
        app: ApplicationContext = error.app
        app.echo_debug(traceback.format_exc())
        app.echo_error(extract_error_message(error))
        sys.exit(1)
