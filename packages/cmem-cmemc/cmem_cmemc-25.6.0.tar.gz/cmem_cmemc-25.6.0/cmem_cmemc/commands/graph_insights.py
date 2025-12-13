"""Graph Insights command group"""

import time

import click
from click import Argument, Context
from click.shell_completion import CompletionItem
from cmem.cmempy.api import get_json, request
from cmem.cmempy.config import get_dp_api_endpoint
from requests import HTTPError

from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.completion import NOT_SORTED, finalize_completion, graph_uris
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.exceptions import CmemcError
from cmem_cmemc.object_list import (
    DirectListPropertyFilter,
    DirectValuePropertyFilter,
    ObjectList,
    transform_lower,
)
from cmem_cmemc.string_processor import GraphLink, TimeAgo
from cmem_cmemc.utils import get_graphs_as_dict, struct_to_table


def get_api_url(path: str = "") -> str:
    """Get URLs of the graph insights API.

    Constructs the full URL for accessing graph insights API endpoints by combining
    the DataPlatform API endpoint with the semspect extension base path and an
    optional resource path.

    Args:
        path: The API resource path to append to the base URL. Defaults to an empty
            string for the root endpoint.

    Returns:
        The complete URL for the specified graph insights API endpoint.

    Example:
        >>> get_api_url()
        'https://example.com/dataplatform/api/ext/semspect'
        >>> get_api_url("/snapshot/status")
        'https://example.com/dataplatform/api/ext/semspect/snapshot/status'

    """
    base_url = get_dp_api_endpoint() + "/api/ext/semspect"
    return f"{base_url}{path}"


def is_available() -> bool:
    """Check availability of graph insights endpoints

    {
     "isActive": true,
     "isUserAllowed": true
    }
    """
    try:
        data: dict[str, bool] = get_json(get_api_url())
    except HTTPError:
        return False
    return bool(data["isActive"] is True and data["isUserAllowed"] is True)


def check_availability(ctx: click.Context) -> None:
    """Check availability of graph insights endpoints or raise an exception"""
    if is_available():
        return
    app: ApplicationContext = ctx.obj
    raise CmemcError(app, "Graph Insights is not available.")


def get_snapshots(ctx: click.Context) -> list[dict[str, str | bool | list[str]]]:
    """Get the snapshot list (all snapshots)"""
    check_availability(ctx)
    data: list[dict[str, str | bool | list[str]]] = get_json(
        get_api_url("/snapshot/status"), params={"includeManagementOnly": True}
    )
    return data


def complete_snapshot_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:  # noqa: ARG001
    """Provide auto-completion for snapshot Ids"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    if not is_available():
        return []
    snapshots = get_snapshots(ctx)
    snapshots = sorted(
        snapshots, key=lambda snapshot: snapshot["updateInfoTimestamp"], reverse=True
    )
    options = [
        (
            snapshot["databaseId"],
            f"{snapshot['mainGraphSynced']} ({snapshot['updateInfoTimestamp']})",
        )
        for snapshot in snapshots
    ]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=NOT_SORTED)


snapshot_list = ObjectList(
    name="insight snapshots",
    get_objects=get_snapshots,
    filters=[
        DirectValuePropertyFilter(
            name="id",
            description="Snapshots with a specific id.",
            property_key="databaseId",
            transform=transform_lower,
        ),
        DirectValuePropertyFilter(
            name="main-graph",
            description="Snapshots with a specific main graph.",
            property_key="mainGraphSynced",
        ),
        DirectValuePropertyFilter(
            name="status",
            description="Snapshots with a specific status.",
            property_key="status",
        ),
        DirectListPropertyFilter(
            name="affected-graph",
            description="Snapshots with a specific affected graph (main or sub-graphs).",
            property_key="allGraphsSynced",
        ),
        DirectValuePropertyFilter(
            name="valid",
            description="Snapshots with a specific validity indicator.",
            property_key="isValid",
            transform=transform_lower,
        ),
    ],
)


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    help=snapshot_list.get_filter_help_text(),
    shell_complete=snapshot_list.complete_values,
    multiple=True,
)
@click.option("--raw", is_flag=True, help="Outputs raw JSON response.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Return the snapshot IDs only. This is useful for piping the IDs into other commands.",
)
@click.pass_context
def list_command(ctx: Context, filter_: tuple[tuple[str, str]], id_only: bool, raw: bool) -> None:
    """List graph insight snapshots.

    Graph Insights Snapshots are identified by an ID.
    """
    check_availability(ctx)
    app: ApplicationContext = ctx.obj
    snapshots = snapshot_list.apply_filters(ctx=ctx, filter_=filter_)

    if id_only:
        for _ in snapshots:
            click.echo(_["databaseId"])
        return

    if raw:
        app.echo_info_json(snapshots)
        return

    graphs = get_graphs_as_dict()
    table = []
    for _ in snapshots:
        id_ = _["databaseId"]
        main_graph = _["mainGraphSynced"]
        updated = _["updateInfoTimestamp"]
        status = _["status"]
        is_valid = _["isValid"]
        if main_graph not in graphs:
            main_graph = rf"\[missing: {main_graph}]"
        table.append([id_, main_graph, updated, status, is_valid])

    app.echo_info_table(
        table,
        headers=["ID", "Main Graph", "Updated", "Status", "Valid"],
        sort_column=0,
        cell_processing={1: GraphLink(), 2: TimeAgo()},
        empty_table_message="No graph insight snapshots found.",
    )


@click.command(cls=CmemcCommand, name="delete")
@click.argument("SNAPSHOT_ID", type=str, shell_complete=complete_snapshot_ids, required=False)
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    help=snapshot_list.get_filter_help_text(),
    shell_complete=snapshot_list.complete_values,
    multiple=True,
)
@click.option("-a", "--all", "all_", is_flag=True, help="Delete all snapshots.")
@click.pass_context
def delete_command(
    ctx: Context, snapshot_id: str | None, filter_: tuple[tuple[str, str]], all_: bool
) -> None:
    """Delete a graph insight snapshot.

    Graph Insight Snapshots are identified by an ID.
    To get a list of existing snapshots,
    execute the `graph insights list` command or use tab-completion.
    """
    check_availability(ctx)
    app: ApplicationContext = ctx.obj
    if snapshot_id is None and not filter_ and not all_:
        raise click.UsageError("Either provide a snapshot ID or a filter, or use the --all flag.")

    if all_:
        app.echo_info("Deleting all snapshots ... ", nl=False)
        request(method="DELETE", uri=get_api_url("/snapshot"))
        app.echo_success("done")
        return

    filter_to_apply = list(filter_) if filter_ else []
    if snapshot_id:
        filter_to_apply.append(("id", snapshot_id))
    snapshots_to_delete = snapshot_list.apply_filters(ctx=ctx, filter_=filter_to_apply)

    if not snapshots_to_delete and snapshot_id:
        raise click.ClickException(f"Snapshot ID '{snapshot_id}' does not exist.")

    if not snapshots_to_delete and not snapshot_id:
        raise click.ClickException("No snapshots found to delete.")

    for _ in snapshots_to_delete:
        id_to_delete = _["databaseId"]
        app.echo_info(f"Deleting snapshot {id_to_delete} ... ", nl=False)
        request(method="DELETE", uri=get_api_url(f"/snapshot/{id_to_delete}"))
        app.echo_success("done")


def wait_for_snapshot(snapshot_id: str, polling_interval: int) -> None:
    """Poll until the snapshot reaches 'DONE' status."""
    while True:
        snapshot: dict[str, str | bool | list[str]] = get_json(
            get_api_url(f"/snapshot/status/{snapshot_id}")
        )
        if snapshot.get("status") == "DONE":
            break
        time.sleep(polling_interval)


@click.command(cls=CmemcCommand, name="create")
@click.argument("iri", type=click.STRING, shell_complete=graph_uris)
@click.option("--wait", is_flag=True, help="Wait until snapshot creation is done.")
@click.option(
    "--polling-interval",
    type=click.IntRange(min=0, max=60),
    show_default=True,
    default=1,
    help="How many seconds to wait between status polls. Status polls are"
    " cheap, so a higher polling interval is most likely not needed.",
)
@click.pass_context
def create_command(ctx: Context, iri: str, wait: bool, polling_interval: int) -> None:
    """Create or update a graph insight snapshot.

    Create a graph insight snapshot for a given graph.
    If the snapshot already exists, it is hot-swapped after re-creation.
    The snapshot contains only the (imported) graphs the requesting user can read.
    """
    check_availability(ctx)
    app: ApplicationContext = ctx.obj
    app.echo_info(f"Create / Update graph snapshot for graph {iri} ... ", nl=False)
    snapshot_id = request(
        method="POST", uri=get_api_url("/snapshot"), params={"contextGraph": iri}
    ).text
    app.echo_success("started", nl=not wait)
    if wait:
        app.echo_info(" ... ", nl=False)
        wait_for_snapshot(snapshot_id, polling_interval)
        app.echo_success("created")


@click.command(cls=CmemcCommand, name="update")
@click.argument("SNAPSHOT_ID", type=str, shell_complete=complete_snapshot_ids, required=False)
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    help=snapshot_list.get_filter_help_text(),
    shell_complete=snapshot_list.complete_values,
    multiple=True,
)
@click.option("-a", "--all", "all_", is_flag=True, help="Delete all snapshots.")
@click.option("--wait", is_flag=True, help="Wait until snapshot creation is done.")
@click.option(
    "--polling-interval",
    type=click.IntRange(min=0, max=60),
    show_default=True,
    default=1,
    help="How many seconds to wait between status polls. Status polls are"
    " cheap, so a higher polling interval is most likely not needed.",
)
@click.pass_context
def update_command(  # noqa: PLR0913
    ctx: Context,
    snapshot_id: str | None,
    filter_: tuple[tuple[str, str]],
    all_: bool,
    wait: bool,
    polling_interval: int,
) -> None:
    """Update a graph insight snapshot.

    Update a graph insight snapshot.
    After the update, the snapshot is hot-swapped.
    """
    check_availability(ctx)
    app: ApplicationContext = ctx.obj
    if snapshot_id is None and not filter_ and not all_:
        raise click.UsageError("Either provide a snapshot ID or a filter, or use the --all flag.")

    filter_to_apply = list(filter_) if filter_ else []
    if snapshot_id:
        filter_to_apply.append(("id", snapshot_id))
    snapshots_to_update = snapshot_list.apply_filters(ctx=ctx, filter_=filter_to_apply)

    if all_:
        snapshots_to_update = get_snapshots(ctx)

    if not snapshots_to_update and snapshot_id:
        raise click.ClickException(f"Snapshot ID '{snapshot_id}' does not exist.")

    if not snapshots_to_update and not snapshot_id:
        raise click.ClickException("No snapshots found to update.")

    for _ in snapshots_to_update:
        id_to_update = _["databaseId"]
        app.echo_info(f"Update snapshot {id_to_update} ... ", nl=False)
        request(method="PUT", uri=get_api_url(f"/snapshot/{id_to_update}"))
        app.echo_success("started", nl=not wait)
        if wait:
            app.echo_info(" ... ", nl=False)
            wait_for_snapshot(id_to_update, polling_interval)
            app.echo_success("updated")


@click.command(cls=CmemcCommand, name="inspect")
@click.argument("SNAPSHOT_ID", type=str, shell_complete=complete_snapshot_ids)
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.pass_context
def inspect_command(ctx: Context, snapshot_id: str, raw: bool) -> None:
    """Inspect the metadata of a graph insight snapshot."""
    check_availability(ctx)
    app: ApplicationContext = ctx.obj
    snapshot: dict[str, str | bool | list[str]] = get_json(
        get_api_url(f"/snapshot/status/{snapshot_id}")
    )
    if raw:
        app.echo_info_json(snapshot)
    else:
        table = struct_to_table(snapshot)
        app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)


@click.group(cls=CmemcGroup, name="insights")
def insights_group() -> CmemcGroup:  # type: ignore[empty-body]
    """List, create, delete and inspect graph insight snapshots.

    Graph Insight Snapshots are identified by an ID.
    To get a list of existing snapshots,
    execute the `graph insights list` command or use tab-completion.
    """


insights_group.add_command(list_command)
insights_group.add_command(delete_command)
insights_group.add_command(create_command)
insights_group.add_command(update_command)
insights_group.add_command(inspect_command)
