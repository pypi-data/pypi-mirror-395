"""workspace commands for cmem command line interface."""

import os

import click
from cmem.cmempy.workspace import reload_workspace
from cmem.cmempy.workspace.export_ import export
from cmem.cmempy.workspace.import_ import import_workspace
from jinja2 import Template

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.commands.python import python
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.smart_path import SmartPath as Path


@click.command(cls=CmemcCommand, name="export")
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    hidden=True,
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace existing files. This is a dangerous option, so use it with care.",
)
@click.option(
    "--type",
    "marshalling_plugin",
    default="xmlZip",
    show_default=True,
    type=click.STRING,
    shell_complete=completion.marshalling_plugins,
    help="Type of the exported workspace file.",
)
@click.option(
    "--filename-template",
    "-t",
    "template",
    default="{{date}}-{{connection}}.workspace",
    show_default=True,
    type=click.STRING,
    shell_complete=completion.workspace_export_templates,
    help="Template for the export file name. "
    "Possible placeholders are (Jinja2): "
    "{{connection}} (from the --connection option) and "
    "{{date}} (the current date as YYYY-MM-DD). "
    "The file suffix will be appended. "
    "Needed directories will be created.",
)
@click.argument(
    "file",
    shell_complete=completion.workspace_files,
    required=False,
    type=ClickSmartPath(writable=True, allow_dash=False, dir_okay=False),
)
@click.pass_obj
def export_command(  # noqa: PLR0913
    app: ApplicationContext,
    overwrite: bool,
    replace: bool,
    marshalling_plugin: str,
    template: str,
    file: str,
) -> None:
    """Export the complete workspace (all projects) to a ZIP file.

    Depending on the requested export type, this ZIP file contains either one
    Turtle file per project (type `rdfTurtle`) or a substructure of resource
    files and XML descriptions (type `xmlZip`).

    The file name is optional and will be generated with by
    the template if absent.
    """
    if overwrite:
        replace = overwrite
        app.echo_warning(
            "The option --overwrite is deprecated and will be removed with the next major release."
            " Please use the --replace option instead."
        )
    if file is None:
        # prepare the template data and create the actual file incl. suffix
        template_data = app.get_template_data()
        file = Template(template).render(template_data) + ".zip"
    file = os.path.normpath(file)
    app.echo_info(f"Export workspace to {file} ... ", nl=False)
    if Path(file).exists() and replace is not True:
        app.echo_error("file exists")
    else:
        # output directory is created lazy
        Path(file).parent.mkdir(parents=True, exist_ok=True)
        # do the export
        export_data = export(marshalling_plugin)
        with Path(file).open(mode="wb") as export_file:
            export_file.write(export_data)
        app.echo_success("done")


@click.command(cls=CmemcCommand, name="import")
@click.option(
    "--type",
    "marshalling_plugin",
    default="xmlZip",
    show_default=True,
    type=click.STRING,
    shell_complete=completion.marshalling_plugins,
    help="Type of the exported workspace file.",
)
@click.argument(
    "file",
    shell_complete=completion.workspace_files,
    type=ClickSmartPath(readable=True, allow_dash=False, dir_okay=False),
)
@click.pass_obj
def import_command(app: ApplicationContext, file: str, marshalling_plugin: str) -> None:
    """Import the workspace from a file."""
    app.echo_info(f"Import workspace from {file} ... ", nl=False)
    import_workspace(file, marshalling_plugin)
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="reload")
@click.pass_obj
def reload_command(app: ApplicationContext) -> None:
    """Reload the workspace from the backend."""
    app.echo_info("Reload workspace  ... ", nl=False)
    reload_workspace()
    app.echo_success("done")


@click.group(cls=CmemcGroup)
def workspace() -> CmemcGroup:  # type: ignore[empty-body]
    """Import, export and reload the project workspace."""


workspace.add_command(export_command)
workspace.add_command(import_command)
workspace.add_command(reload_command)
workspace.add_command(python)
