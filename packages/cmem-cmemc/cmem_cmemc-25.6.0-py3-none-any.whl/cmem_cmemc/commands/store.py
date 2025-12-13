"""Explore backend (DataPlatform) store commands for the cmem command line interface."""

import os
from dataclasses import dataclass

import click
from click import Argument, Context, UsageError
from click.shell_completion import CompletionItem
from cmem.cmempy.dp.admin import create_showcase_data, delete_bootstrap_data, import_bootstrap_data
from cmem.cmempy.dp.admin.backup import get_zip, post_zip
from cmem.cmempy.dp.workspace import migrate_workspaces
from cmem.cmempy.health import get_dp_info
from cmem.cmempy.workspace import reload_workspace
from jinja2 import Template

from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.completion import file_list
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.smart_path import SmartPath as Path
from cmem_cmemc.utils import validate_zipfile


def complete_store_backup_files(
    ctx: Context,  # noqa: ARG001
    param: Argument,  # noqa: ARG001
    incomplete: str,
) -> list[CompletionItem]:
    """Prepare a list of Store Backip Files."""
    return file_list(incomplete=incomplete, suffix=".store.zip", description="Store Backup File")


@click.command(cls=CmemcCommand, name="bootstrap")
@click.option(
    "--import",
    "import_",
    is_flag=True,
    help="Delete existing bootstrap data if present and import bootstrap "
    "data which was delivered with Corporate Memory.",
)
@click.option("--remove", is_flag=True, help="Delete existing bootstrap data if present.")
@click.pass_obj
def bootstrap_command(app: ApplicationContext, import_: bool, remove: bool) -> None:
    """Update/Import or remove bootstrap data.

    Use `--import` to import the bootstrap data needed for managing shapes and
    configuration objects. This will remove the old data first.

    Use `--remove` to delete bootstrap data.

    Note: The removal of existing bootstrap data will search for resources which are
    flagged with the isSystemResource property.

    Note: The import part of this command is equivalent to the 'bootstrap-data' migration recipe
    """
    if (import_ and remove) or (not import_ and not remove):
        raise UsageError("Either use the --import or the --remove option.")
    if import_:
        app.echo_info("Update or import bootstrap data ... ", nl=False)
        import_bootstrap_data()
        app.echo_success("done")
        return
    if remove:
        app.echo_info("Remove bootstrap data ... ", nl=False)
        delete_bootstrap_data()
        app.echo_success("done")
        return


@click.command(cls=CmemcCommand, name="showcase")
@click.option(
    "--scale",
    type=click.INT,
    default="10",
    show_default=True,
    help="The scale factor provides a way to set the target size of the "
    "scenario. A value of 10 results in around 40k triples, a value of "
    "50 in around 350k triples.",
)
@click.option(
    "--create",
    is_flag=True,
    help="Delete old showcase data if present and create new showcase data"
    "based on the given scale factor.",
)
@click.option("--delete", is_flag=True, help="Delete existing showcase data if present.")
@click.pass_obj
def showcase_command(app: ApplicationContext, scale: int, create: bool, delete: bool) -> None:
    """Create showcase data.

    This command creates a showcase scenario of multiple graphs including
    integration graphs, shapes, statement annotations, etc.

    Note: There is currently no deletion mechanism for the showcase data, and
    you need to remove the showcase graphs manually (or just remove all
    graphs).
    """
    if not delete and not create:
        raise UsageError("Either use the --create or the --delete flag.")
    if delete:
        raise NotImplementedError(
            "This feature is not implemented yet. Please delete the graphs manually."
        )
    if create:
        app.echo_info(f"Create showcase data with scale factor {scale} ... ", nl=False)
        create_showcase_data(scale_factor=scale)
        app.echo_success("done")
        app.echo_info("Reload workspace  ... ", nl=False)
        reload_workspace()
        app.echo_success("done")


@click.command(cls=CmemcCommand, name="export")
@click.argument(
    "BACKUP_FILE",
    shell_complete=complete_store_backup_files,
    required=False,
    type=ClickSmartPath(writable=True, allow_dash=False, dir_okay=False),
)
@click.option(
    "--overwrite",
    is_flag=True,
    hidden=True,
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace existing files. This is a dangerous option, so use it with care.",
)
@click.pass_obj
def export_command(
    app: ApplicationContext, backup_file: str, overwrite: bool, replace: bool
) -> None:
    """Backup all knowledge graphs to a ZIP archive.

    The backup file is a ZIP archive containing all knowledge graphs (one
    Turtle file + configuration file per graph).

    This command will create lots of load on the server.
    It can take a long time to complete.
    """
    if not backup_file:
        backup_file = Template("{{date}}-{{connection}}.store.zip").render(app.get_template_data())
    if overwrite:
        replace = overwrite
        app.echo_warning(
            "The option --overwrite is deprecated and will be removed with the next major release."
            " Please use the --replace option instead."
        )
    if Path(backup_file).exists() and replace is not True:
        raise UsageError(
            f"Export file {backup_file} already exists and --replace option is not used."
        )
    with get_zip() as request:
        request.raise_for_status()
        with Path(backup_file).open(mode="wb") as _:
            requested_size = 1024 * 1024
            byte_counter = 0
            overall_byte_counter = 0
            app.echo_info(f"Exporting graphs backup to {backup_file} ...", nl=False)
            for chunk in request.iter_content(chunk_size=requested_size):
                chunk_size = len(chunk)
                app.echo_debug(f"Got new chuck of {chunk_size} bytes.")
                byte_counter += chunk_size
                overall_byte_counter += chunk_size
                _.write(chunk)
                _.flush()
                os.fsync(_.fileno())
                if byte_counter > requested_size:
                    app.echo_info(".", nl=False)
                    byte_counter = 0
            app.echo_debug(f"Wrote {overall_byte_counter} bytes to {backup_file}.")
            if validate_zipfile(zipfile=backup_file):
                app.echo_debug(f"{backup_file} successfully validated")
                app.echo_success(" done")
            else:
                app.echo_error(" error (file corrupt)")


@click.command(cls=CmemcCommand, name="import")
@click.argument(
    "BACKUP_FILE",
    shell_complete=complete_store_backup_files,
    required=True,
    type=ClickSmartPath(readable=True, exists=True, allow_dash=False, dir_okay=False),
)
@click.pass_obj
def import_command(app: ApplicationContext, backup_file: str) -> None:
    """Restore graphs from a ZIP archive.

    The backup file is a ZIP archive containing all knowledge graphs  (one
    Turtle file + configuration file per graph).

    The command will load a single backup ZIP archive into the triple store
    by replacing all graphs with the content of the Turtle files in the
    archive and deleting all graphs which are not in the archive.

    This command will create lots of load on the server.
    It can take a long time to complete.
    The backup file will be transferred to the server, then unzipped and
    imported graph by graph. After the initial transfer the network
    connection is not used anymore and may be closed by proxies.
    This does not mean that the import failed.
    """
    app.echo_info(f"Importing graphs backup from {backup_file} ...", nl=False)
    request = post_zip(backup_file)
    request.raise_for_status()
    app.echo_success(" done")


@dataclass
class CommandResult:
    """Represents the result of a command execution"""

    data: list
    headers: list[str]
    caption: str
    empty_state_message: str


def _migrate_workspaces() -> CommandResult:
    """Migrate workspace configurations to the current CMEM version."""
    request = migrate_workspaces()
    return CommandResult(
        data=[(iri,) for iri in request],
        headers=["IRI"],
        caption="Migrated workspace configurations",
        empty_state_message="No migrateable workspace configurations found.",
    )


def _get_migrate_workspaces() -> CommandResult:
    """Retrieve workspace configurations that have been migrated to the current CMEM version."""
    dp_info = get_dp_info()
    migratable_workspace_configurations = dp_info["workspaceConfiguration"]["workspacesToMigrate"]
    return CommandResult(
        data=[(_["iri"], _["label"]) for _ in migratable_workspace_configurations],
        headers=["IRI", "LABEL"],
        caption="Migrateable configurations workspaces",
        empty_state_message="No migrateable workspace configurations found.",
    )


@click.command("migrate")
@click.option(
    "--workspaces",
    is_flag=True,
    help="Migrate workspace configurations to the current version.",
)
@click.pass_obj
def migrate_command(app: ApplicationContext, workspaces: bool) -> None:
    """Migrate configuration resources to the current version.

    This command serves two purposes: (1) When invoked without an option, it lists
    all migrateable configuration resources. (2) When invoked with the `--workspaces`
    option, it migrates the workspace configurations to the current version.
    """
    app.echo_warning(
        "The command is deprecated and will be removed with the next major release. "
        "Please use the `admin migration` command group instead."
    )
    result = _migrate_workspaces() if workspaces else _get_migrate_workspaces()

    if result.data:
        app.echo_info_table(
            result.data,
            headers=result.headers,
            sort_column=0,
            caption=result.caption,
        )
    else:
        app.echo_success(result.empty_state_message)


@click.group(cls=CmemcGroup)
def store() -> CmemcGroup:  # type: ignore[empty-body]
    """Import, export and bootstrap the knowledge graph store.

    This command group consist of commands to administrate the
    knowledge graph store as a whole.
    """


store.add_command(showcase_command)
store.add_command(bootstrap_command)
store.add_command(export_command)
store.add_command(import_command)
store.add_command(migrate_command)
