"""Build project file commands for cmemc."""

import re

import click
from click import ClickException, Context, UsageError
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.workspace.projects.resources import get_all_resources
from cmem.cmempy.workspace.projects.resources.resource import (
    create_resource,
    delete_resource,
    get_resource_metadata,
    get_resource_response,
    get_resource_usage_data,
    resource_exist,
)

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.exceptions import CmemcError
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.smart_path import SmartPath as Path
from cmem_cmemc.string_processor import FileSize, TimeAgo
from cmem_cmemc.utils import check_or_select_project, split_task_id, struct_to_table

RESOURCE_FILTER_TYPES = ["project", "regex"]
RESOURCE_FILTER_TYPES_HIDDEN = ["ids"]
RESOURCE_FILTER_TEXT = (
    "Filter file resources based on metadata. "
    f"First parameter CHOICE can be one of {RESOURCE_FILTER_TYPES!s}"
    ". The second parameter is based on CHOICE, e.g. a project "
    "ID or a regular expression string."
)


def _upload_file_resource(
    app: ApplicationContext,
    project_id: str,
    local_file_name: str,
    remote_file_name: str,
    replace: bool,
) -> None:
    """Upload a local file as a dataset resource to a project.

    Args:
    ----
        app: the click cli app context.
        project_id: The project ID in the workspace.
        local_file_name: The path to the local file name
        remote_file_name: The remote file name
        replace: Replace resource if needed.

    Raises:
    ------
        ValueError: if resource exists and no replace

    """
    exist = resource_exist(project_name=project_id, resource_name=remote_file_name)
    if exist and not replace:
        raise CmemcError(
            app,
            f"A file resource with the name '{remote_file_name}' already "
            "exists in this project. \n"
            "Please rename the file or use the '--replace' "
            "parameter in order to overwrite the remote file.",
        )
    if exist:
        app.echo_info(
            f"Replace content of {remote_file_name} with content from "
            f"{local_file_name} in project {project_id} ... ",
            nl=False,
        )
    else:
        app.echo_info(
            f"Upload {local_file_name} as a file resource "
            f"{remote_file_name} to project {project_id} ... ",
            nl=False,
        )
    create_resource(
        project_name=project_id,
        resource_name=remote_file_name,
        file_resource=ClickSmartPath.open(local_file_name),
        replace=replace,
    )
    app.echo_success("done")


def _get_resources_filtered(
    resources: list[dict], filter_name: str, filter_value: str | tuple[str, ...]
) -> list[dict]:
    """Get file resources but filtered according to name and value."""
    # check for correct filter names (filter ids is used internally only)
    if filter_name not in RESOURCE_FILTER_TYPES + RESOURCE_FILTER_TYPES_HIDDEN:
        raise UsageError(
            f"{filter_name} is an unknown filter name. " f"Use one of {RESOURCE_FILTER_TYPES}."
        )
    # filter by ID list
    if filter_name == "ids":
        return [_ for _ in resources if _["id"] in filter_value]
    # filter by project
    if filter_name == "project":
        return [_ for _ in resources if _["project"] == str(filter_value)]
    # filter by regex
    if filter_name == "regex":
        return [_ for _ in resources if re.search(str(filter_value), _["name"])]
    # return unfiltered list
    return resources


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only resource IDs and no other metadata. "
    "This is useful for piping the IDs into other commands.",
)
@click.option(
    "--filter",
    "filters_",
    multiple=True,
    type=(str, str),
    shell_complete=completion.resource_list_filter,
    help=RESOURCE_FILTER_TEXT,
)
@click.pass_obj
def list_command(
    app: ApplicationContext, raw: bool, id_only: bool, filters_: tuple[tuple[str, str], ...]
) -> None:
    """List available file resources.

    Outputs a table or a list of file resources.
    """
    resources = get_all_resources()
    for _ in filters_:
        filter_name, filter_value = _
        resources = _get_resources_filtered(resources, filter_name, filter_value)
    if raw:
        app.echo_info_json(resources)
        return
    if id_only:
        for _ in sorted(_["id"] for _ in resources):
            app.echo_result(_)
        return
    # output a user table
    table = []
    headers = ["ID", "Modified", "Size"]
    for _ in resources:
        row = [
            _["id"],
            _["modified"],
            _["size"],
        ]
        table.append(row)

    caption = f"{len(table)} files of {get_cmem_base_uri()}"
    empty_note = "No resources found."
    if len(filters_) > 0:
        caption += " (filtered)"
        empty_note = "No resources found for these filters."

    app.echo_info_table(
        table,
        headers=headers,
        sort_column=0,
        cell_processing={1: TimeAgo(), 2: FileSize()},
        caption=caption,
        empty_table_message=f"{empty_note} "
        "Use the `dataset create` command to create a new file-based dataset, or "
        "the `project file upload` command to create only a file resource.",
    )


@click.command(cls=CmemcCommand, name="delete")
@click.argument("resource_ids", nargs=-1, type=click.STRING, shell_complete=completion.resource_ids)
@click.option("--force", is_flag=True, help="Delete resource even if in use by a task.")
@click.option(
    "-a",
    "--all",
    "all_",
    is_flag=True,
    help="Delete all resources. " "This is a dangerous option, so use it with care.",
)
@click.option(
    "--filter",
    "filters_",
    multiple=True,
    type=(str, str),
    shell_complete=completion.resource_list_filter,
    help=RESOURCE_FILTER_TEXT,
)
@click.pass_obj
def delete_command(
    app: ApplicationContext,
    resource_ids: tuple[str, ...],
    force: bool,
    all_: bool,
    filters_: tuple[tuple[str, str], ...],
) -> None:
    """Delete file resources.

    There are three selection mechanisms: with specific IDs - only those
    specified resources will be deleted; by using --filter - resources based
    on the filter type and value will be deleted; by using --all, which will
    delete all resources.
    """
    if resource_ids == () and not all_ and filters_ == ():
        raise UsageError(
            "Either specify at least one resource ID or use the --all or "
            "--filter options to specify resources for deletion."
        )

    resources = get_all_resources()
    if len(resource_ids) > 0:
        for resource_id in resource_ids:
            if resource_id not in [_["id"] for _ in resources]:
                raise ClickException(f"Resource {resource_id} not available.")
        # "filter" by id
        resources = _get_resources_filtered(resources, "ids", resource_ids)
    for _ in filters_:
        resources = _get_resources_filtered(resources, _[0], _[1])

    # avoid double removal as well as sort IDs
    processed_ids = sorted({_["id"] for _ in resources}, key=lambda v: v.lower())
    count = len(processed_ids)
    for current, resource_id in enumerate(processed_ids, start=1):
        current_string = str(current).zfill(len(str(count)))
        app.echo_info(f"Delete resource {current_string}/{count}: {resource_id} ... ", nl=False)
        project_id, resource_local_id = split_task_id(resource_id)
        usage = get_resource_usage_data(project_id, resource_local_id)
        if len(usage) > 0:
            app.echo_error(f"in use by {len(usage)} task(s)", nl=False)
            if force:
                app.echo_info(" ... ", nl=False)
            else:
                app.echo_info("")
                continue
        delete_resource(project_name=project_id, resource_name=resource_local_id)
        app.echo_success("deleted")


@click.command(cls=CmemcCommand, name="download")
@click.argument("resource_ids", nargs=-1, type=click.STRING, shell_complete=completion.resource_ids)
@click.option(
    "--output-dir",
    default=".",
    show_default=True,
    type=ClickSmartPath(writable=True, file_okay=False),
    help="The directory where the downloaded files will be saved. "
    "If this directory does not exist, it will be created.",
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace existing files. This is a dangerous option, " "so use it with care!",
)
@click.pass_obj
def download_command(
    app: ApplicationContext, resource_ids: tuple[str], output_dir: str, replace: bool
) -> None:
    """Download file resources to the local file system.

    This command downloads one or more file resources from projects to your local
    file system. Files are saved with their resource names in the output directory.

    Resources are identified by their IDs in the format PROJECT_ID:RESOURCE_NAME.

    Example: cmemc project file download my-proj:my-file.csv

    Example: cmemc project file download my-proj:file1.csv my-proj:file2.csv --output-dir /tmp
    """
    import os

    if not resource_ids:
        raise UsageError(
            "At least one resource ID must be specified. "
            "Use 'project file list' to see available resources."
        )

    count = len(resource_ids)
    for current, resource_id in enumerate(resource_ids, start=1):
        try:
            project_id, resource_name = split_task_id(resource_id)
        except ValueError:
            app.echo_error(f"Invalid resource ID format: {resource_id}")
            continue

        # Build output path
        output_path = os.path.normpath(str(Path(output_dir) / resource_name))

        app.echo_info(
            f"Download resource {current}/{count}: {resource_id} to {output_path} ... ",
            nl=False,
        )

        if Path(output_path).exists() and replace is not True:
            app.echo_error("target file exists")
            continue

        # Create parent directory if it doesn't exist
        Path(output_path).parent.mkdir(exist_ok=True, parents=True)

        try:
            with (
                get_resource_response(project_id, resource_name) as response,
                click.open_file(output_path, "wb") as resource_file,
            ):
                for chunk in response.iter_content(chunk_size=8192):
                    resource_file.write(chunk)
            app.echo_success("done")
        except (OSError, ClickException) as error:
            app.echo_error(f"failed: {error!s}")
            continue


@click.command(cls=CmemcCommand, name="upload")
@click.argument(
    "input_path",
    required=True,
    type=ClickSmartPath(
        allow_dash=False, dir_okay=False, readable=True, exists=True, remote_okay=True
    ),
)
@click.option(
    "--project",
    "project_id",
    type=click.STRING,
    shell_complete=completion.project_ids,
    help="The project where you want to upload the file. If there is "
    "only one project in the workspace, this option can be omitted.",
)
@click.option(
    "--path",
    "remote_name",
    type=click.STRING,
    shell_complete=completion.resource_paths,
    help="The path/name of the file resource in the project (e.g., 'data/file.csv'). "
    "If not specified, the local file name will be used.",
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace existing file resource. This is a dangerous option, " "so use it with care!",
)
@click.pass_obj
def upload_command(
    app: ApplicationContext, input_path: str, project_id: str, remote_name: str, replace: bool
) -> None:
    """Upload a file to a project.

    This command uploads a file to a project as a file resource.

    Note: If you want to create a dataset from your file, the `dataset create`
    command is maybe the better option.

    Example: cmemc project file upload my-file.csv --project my-project
    """
    project_id = check_or_select_project(app, project_id)
    local_file_name = Path(input_path).name

    if remote_name and remote_name.endswith("/"):
        app.echo_warning(
            f"Remote path ends with a slash, so the local file name is appended: {local_file_name}."
        )
        remote_name = remote_name + local_file_name

    # Use local filename if remote name not specified
    if not remote_name:
        remote_name = local_file_name

    _upload_file_resource(
        app=app,
        remote_file_name=remote_name,
        project_id=project_id,
        local_file_name=input_path,
        replace=replace,
    )


@click.command(cls=CmemcCommand, name="inspect")
@click.argument("resource_id", type=click.STRING, shell_complete=completion.resource_ids)
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.pass_obj
def inspect_command(app: ApplicationContext, resource_id: str, raw: bool) -> None:
    """Display all metadata of a file resource."""
    project_id, resource_id = split_task_id(resource_id)
    resource_data = get_resource_metadata(project_id, resource_id)
    if raw:
        app.echo_info_json(resource_data)
    else:
        table = struct_to_table(resource_data)
        app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)


@click.command(cls=CmemcCommand, name="usage")
@click.argument("resource_id", type=click.STRING, shell_complete=completion.resource_ids)
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.pass_obj
def usage_command(app: ApplicationContext, resource_id: str, raw: bool) -> None:
    """Display all usage data of a file resource."""
    project_id, resource_id = split_task_id(resource_id)
    usage = get_resource_usage_data(project_id, resource_id)
    if raw:
        app.echo_info_json(usage)
        return
    # output a user table
    table = []
    headers = ["Task ID", "Type", "Label"]
    for _ in usage:
        row = [project_id + ":" + _["id"], _["taskType"], _["label"]]
        table.append(row)
    app.echo_info_table(
        table,
        empty_table_message=f"The file resource '{resource_id}' is not used in "
        f"any task in project '{project_id}'.",
        headers=headers,
        sort_column=2,
    )


@click.group(
    cls=CmemcGroup,
    hidden=True,
)
@click.pass_context
def resource(ctx: Context) -> None:
    """List, inspect or delete dataset file resources.

    File resources are identified by their paths and project IDs.

    Warning: This command group is deprecated and will be removed with the next major release.
    Please use the `project file` command group instead.
    """
    app: ApplicationContext = ctx.obj
    app.echo_warning(
        "The 'dataset resource' command group is deprecated and will be removed with the next"
        " major release. Please use the 'project file' command group instead.",
    )


@click.group(cls=CmemcGroup)
def file() -> CmemcGroup:  # type: ignore[empty-body]
    """List, inspect, up-/download or delete project file resources.

    File resources are identified with a RESOURCE_ID which is a concatenation
    of its project ID and its relative path, e.g. `my-project:path-to/table.csv`.

    Note: To get a list of existing file resources, execute the `project file list` command
    or use tab-completion.
    """


resource.add_command(list_command)
resource.add_command(delete_command)
resource.add_command(inspect_command)
resource.add_command(usage_command)

file.add_command(list_command)
file.add_command(delete_command)
file.add_command(download_command)
file.add_command(upload_command)
file.add_command(inspect_command)
file.add_command(usage_command)
