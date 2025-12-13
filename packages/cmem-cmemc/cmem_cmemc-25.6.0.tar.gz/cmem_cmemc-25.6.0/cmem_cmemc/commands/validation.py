"""graph validation command group"""

import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import click
import timeago
from click import Context, UsageError
from click.shell_completion import CompletionItem
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.dp.shacl import validation
from junit_xml import TestCase, TestSuite, to_xml_report_string
from rich.progress import Progress, SpinnerColumn, TaskID, TimeElapsedColumn

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.completion import finalize_completion
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.exceptions import ServerError
from cmem_cmemc.object_list import (
    DirectListPropertyFilter,
    DirectValuePropertyFilter,
    ObjectList,
    compare_int_greater_than,
    transform_lower,
)
from cmem_cmemc.string_processor import GraphLink, ResourceLink, TimeAgo
from cmem_cmemc.title_helper import TitleHelper
from cmem_cmemc.utils import get_query_text, struct_to_table


def _reports_to_junit(reports: list[dict]) -> str:
    """Create a jUnit XML document from a list of report dictionaries"""
    test_suites: list[TestSuite] = []

    for report in reports:
        test_cases: list[TestCase] = []
        context_graph = report["contextGraphIri"]
        shape_graph = report["shapeGraphIri"]
        time_elapsed = (report["executionFinished"] - report["executionStarted"]) / 1000
        violations: dict[str, list[dict]] = {}
        for resource in sorted(report["resources"]):
            # get a list of all tested resources
            violations[resource] = []
        average_elapsed_sec = time_elapsed / len(violations)
        for result in report["results"]:
            # collection violations per resource
            resource_iri = result["resourceIri"]
            violations[resource_iri] = result["violations"]
        for resource in violations:
            # create on test case per resource
            resource_violations = violations[resource]
            violations_count = len(violations[resource])
            constraints = Counter(
                _["reportEntryConstraintMessageTemplate"]["constraintName"]
                for _ in resource_violations
            )
            test_case_name = f"{resource}"
            if violations_count == 0:
                test_case_name += " has no violations"
            if violations_count == 1:
                test_case_name += f" has 1 violation ({next(iter(constraints.keys()))})"
            if violations_count > 1:
                constrains_str = ""
                for constraint, constraint_count in constraints.items():
                    constrains_str += f", {constraint_count}x{constraint}"
                test_case_name += f" has {violations_count} violations ({constrains_str[2:]})"

            test_case = TestCase(
                name=test_case_name,
                classname=f"{context_graph} tested with {shape_graph}",
                elapsed_sec=average_elapsed_sec,
            )
            if violations_count > 0:
                test_case.add_failure_info(output=json.dumps(resource_violations, indent=2))
            test_cases.append(test_case)
        test_suite = TestSuite(
            name=f"Testing {context_graph} with shapes from {shape_graph}.",
            test_cases=test_cases,
            id=report["id"],
            timestamp=report["executionFinished"],
        )
        test_suites.append(test_suite)
    return str(to_xml_report_string(test_suites, encoding="utf-8"))


def get_sorted_validations_list(ctx: Context) -> list[dict]:  # noqa: ARG001
    """Get a sorted list of validation objects (aggregations)"""
    objects = validation.get_all_aggregations()
    return sorted(objects, key=lambda o: str(o.get("executionStarted", "SCHEDULED")))


validations_list = ObjectList(
    name="validation processes",
    get_objects=get_sorted_validations_list,
    filters=[
        DirectValuePropertyFilter(
            name="status",
            description="Filter list by current status of the process.",
            property_key="state",
            transform=transform_lower,
        ),
        DirectValuePropertyFilter(
            name="context-graph",
            description="Filter list by used data / context graph IRI.",
            property_key="contextGraphIri",
        ),
        DirectValuePropertyFilter(
            name="shape-graph",
            description="Filter list by used shape graph IRI.",
            property_key="shapeGraphIri",
        ),
        DirectValuePropertyFilter(
            name="more-resources-than",
            description="Filter list by the number of resources.",
            property_key="resourceCount",
            compare=compare_int_greater_than,
            fixed_completion=[
                CompletionItem("0"),
                CompletionItem("100"),
                CompletionItem("500"),
            ],
        ),
        DirectValuePropertyFilter(
            name="more-violations-than",
            description="Filter list by the number of violations.",
            property_key="violationsCount",
            compare=compare_int_greater_than,
            fixed_completion=[
                CompletionItem("0"),
                CompletionItem("100"),
                CompletionItem("500"),
            ],
        ),
        DirectValuePropertyFilter(
            name="more-violated-resources-than",
            description="Filter list by the number of violated resources.",
            property_key="resourcesWithViolationsCount",
            compare=compare_int_greater_than,
            fixed_completion=[
                CompletionItem("0"),
                CompletionItem("100"),
                CompletionItem("500"),
            ],
        ),
    ],
)


def get_violations_list(ctx: Context) -> list[dict]:
    """Get a list of violations"""
    try:
        # sometimes process_id is in params, sometimes in args !?
        process_id = ctx.params.get("process_id", None)
        if not process_id:
            process_id = ctx.args[0]
    except IndexError:
        return []  # process_id not given
    violations: list[dict] = []  # create a new object which better matches object_list needs
    for result in validation.get(batch_id=process_id)["results"]:
        resource_iri = result["resourceIri"]
        node_shapes = result["nodeShapes"]
        for _ in result["violations"]:
            _["resourceIri"] = resource_iri
            _["nodeShapes"] = node_shapes
            _["constraintName"] = _["reportEntryConstraintMessageTemplate"]["constraintName"]
            violations.append(_)
    return violations


violations_list = ObjectList(
    name="violations",
    get_objects=get_violations_list,
    filters=[
        DirectValuePropertyFilter(
            name="constraint",
            description="Filter list by constraint name.",
            property_key="constraintName",
        ),
        DirectValuePropertyFilter(
            name="severity", description="Filter list by severity.", property_key="severity"
        ),
        DirectValuePropertyFilter(
            name="resource",
            description="Filter list by resource IRI.",
            property_key="resourceIri",
            title_helper=TitleHelper(),
        ),
        DirectListPropertyFilter(
            name="node-shape",
            description="Filter list by node shape IRI.",
            property_key="nodeShapes",
            title_helper=TitleHelper(),
        ),
        DirectValuePropertyFilter(
            name="source",
            description="Filter list by constraint source.",
            property_key="source",
            title_helper=TitleHelper(),
        ),
    ],
)


def _get_batch_validation_option(validation_: dict) -> tuple[str, str]:
    """Get a completion option of a single batch validation"""
    id_ = validation_["id"]
    state = validation_["state"]
    graph = validation_["contextGraphIri"]
    stamp = datetime.fromtimestamp(validation_["executionStarted"] / 1000, tz=timezone.utc)
    time_ago = timeago.format(stamp, datetime.now(tz=timezone.utc))
    resources = _get_resource_count(validation_)
    violations = _get_violation_count(validation_)
    return (
        id_,
        f"{state} - {time_ago}, {resources} resources, {violations} violations ({graph})",
    )


def _complete_all_batch_validations(
    ctx: click.Context,  # noqa: ARG001
    param: click.Argument,  # noqa: ARG001
    incomplete: str,
) -> list[CompletionItem]:
    """Provide completion for batch validation"""
    options = [_get_batch_validation_option(_) for _ in validation.get_all_aggregations()]
    return finalize_completion(candidates=options, incomplete=incomplete)


def _complete_running_batch_validations(
    ctx: click.Context,  # noqa: ARG001
    param: click.Argument,  # noqa: ARG001
    incomplete: str,
) -> list[CompletionItem]:
    """Provide completion for running batch validation"""
    options = [
        _get_batch_validation_option(_)
        for _ in validation.get_all_aggregations()
        if _["state"] == validation.STATUS_RUNNING
    ]
    return finalize_completion(candidates=options, incomplete=incomplete)


def _complete_finished_batch_validations(
    ctx: click.Context,  # noqa: ARG001
    param: click.Argument,  # noqa: ARG001
    incomplete: str,
) -> list[CompletionItem]:
    """Provide completion for finished batch validations"""
    options = [
        _get_batch_validation_option(_)
        for _ in validation.get_all_aggregations()
        if _["state"] == validation.STATUS_FINISHED
    ]
    return finalize_completion(candidates=options, incomplete=incomplete)


def _print_process_summary(app: ApplicationContext, process_id: str) -> None:
    """Show summary of the validation process"""
    app.echo_info_table(
        struct_to_table(validation.get_aggregation(batch_id=process_id)),
        headers=["Key", "Value"],
        sort_column=0,
        caption="Validation Summary",
    )


def show_violated_resources(app: ApplicationContext, data: list[dict]) -> None:
    """Show violated resource IRIs of a validation process"""
    messages = sorted({_["resourceIri"] for _ in data})
    app.echo_info(message=messages)


def _wait_for_process_completion(
    app: ApplicationContext, process_id: str, polling_interval: int, use_rich: bool = False
) -> str:
    class State:
        """State of a validation process"""

        id_: str
        data: dict
        status: str
        completed: int
        total: int

        def __init__(self, id_: str):
            self.id_ = id_
            self.refresh()

        def refresh(self) -> None:
            self.data = validation.get_aggregation(batch_id=self.id_)
            self.status = self.data.get("state", "UNKNOWN")
            self.completed = self.data.get("resourceProcessedCount", 0)
            self.total = self.data.get("resourceCount", 0)
            app.echo_debug(f"Process {self.id_} has status {self.status}.")

    state = State(id_=process_id)
    progress: Progress | None = None
    task: TaskID | None = None
    if use_rich:
        progress = Progress(
            SpinnerColumn(),
            *Progress.get_default_columns(),
            TimeElapsedColumn(),
            transient=True,
            console=app.console,
        )
        progress.__enter__()  # simulate context manager (with:)
        task = progress.add_task(f"{state.status.capitalize()} ... ", total=state.total)
    while True:
        time.sleep(polling_interval)
        state.refresh()
        if progress is not None and task is not None:
            progress.update(
                task_id=task,
                completed=state.completed,
                description=f"{state.status.capitalize()} ... {state.completed} / {state.total}",
            )
        if state.status in (validation.STATUS_SCHEDULED, validation.STATUS_RUNNING):
            # when reported as running or scheduled, start another loop
            continue
        # when reported as finished, error or cancelled break out
        break
    if progress is not None and task is not None:
        progress.stop()
        progress.__exit__(None, None, None)
    if state.status == validation.STATUS_CANCELLED:
        raise ServerError(app, "Process was cancelled.")
    if state.status == validation.STATUS_ERROR:
        error_message = state.data.get("error", "")
        raise ServerError(app, f"Process ended with error: {error_message}")
    return state.status


def _print_violation_table(
    app: ApplicationContext, data_graph: str, shape_graph: str, violations: list[dict]
) -> None:
    """Print violation table from batch validation result"""
    # fetch titles
    resources = []
    for violation in violations:
        resources.append(str(violation.get("resourceIri")))
        resources.extend(violation.get("nodeShapes", []))
    title_helper = TitleHelper()
    title_helper.get(resources)

    # prepare link helper
    resource_link = ResourceLink(graph_iri=data_graph, title_helper=title_helper)
    shape_link = ResourceLink(graph_iri=shape_graph, title_helper=title_helper)

    table = []
    for violation in violations:
        combined_cell = ""

        path = violation.get("path", None)
        if path is not None:
            combined_cell = f"Path: {path}\n"

        source = violation.get("source", None)
        if source is not None:
            combined_cell = f"{combined_cell}Source: {shape_link.process(text=source)}"

        node_shapes = violation.get("nodeShapes", [])
        if len(node_shapes) == 1:
            combined_cell = f"{combined_cell}\nNodeShape: {shape_link.process(text=node_shapes[0])}"
        if len(node_shapes) > 1:
            combined_cell = f"{combined_cell}\nNodeShapes:"
            for node_shape in node_shapes:
                combined_cell = f"{combined_cell}\n - {shape_link.process(text=node_shape)}"

        text = violation["messages"][0]["value"]  # default: use the text of the first message
        for message in violation["messages"]:
            # look for en non non-lang messages to use
            if message["lang"] == "" or message["lang"] == "en":
                text = str(message["value"])
                break
        combined_cell = f"{combined_cell}\nMessage: {text}"

        row = [
            resource_link.process(text=str(violation.get("resourceIri"))),
            violation.get("constraintName", "UNKNOWN"),
            combined_cell,
        ]
        table.append(row)

    app.echo_info_table(
        table,
        headers=["Resource", "Constraint", "Details"],
        sort_column=0,
        caption="Violation List",
        empty_table_message="No violations found.",
    )


def _get_resource_count(batch_validation: dict) -> str:
    """Get resource count from validation report"""
    resource_count = str(batch_validation.get("resourceCount", "-"))
    processed_count = str(batch_validation.get("resourceProcessedCount", "-"))
    if resource_count == processed_count:
        return resource_count
    return f"{processed_count} / {resource_count}"


def _get_violation_count(process_data: dict) -> str:
    """Get violation count from validation report"""
    if process_data.get("executionStarted") is None:
        return "-"
    resources = str(process_data.get("resourcesWithViolationsCount", "0"))
    violations = str(process_data.get("violationsCount", "0"))
    if violations == "0":
        return "0"
    return f"{violations} ({resources} Resources)"


@click.command(cls=CmemcCommand, name="execute")
@click.argument("iri", type=click.STRING, shell_complete=completion.graph_uris)
@click.option(
    "--wait",
    is_flag=True,
    help="Wait until the process is finished. When using this option without the "
    "`--id-only` flag, it will enable a progress bar and a summary view.",
)
@click.option(
    "--shape-graph",
    shell_complete=completion.graph_uris_skip_check,
    default="https://vocab.eccenca.com/shacl/",
    show_default=True,
    help="The shape catalog used for validation.",
)
@click.option(
    "--query",
    shell_complete=completion.remote_queries_and_sparql_files,
    help="SPARQL query to select the resources which you want to validate from "
    "the data graph. "
    "Can be provided as a local file or as a query catalog IRI. "
    "[default: all typed resources]",
)
@click.option(
    "--result-graph",
    shell_complete=completion.writable_graph_uris,
    help="(Optionally) write the validation results to a Knowledge Graph. " "[default: None]",
)
@click.option(
    "--replace",
    is_flag=True,
    default=False,
    help="Replace the result graph instead of just adding the new results. "
    "This is a dangerous option, so use it with care!",
)
@click.option(
    "--ignore-graph",
    shell_complete=completion.ignore_graph_uris,
    type=click.STRING,
    multiple=True,
    help="A set of data graph IRIs which are not queried in the resource selection. "
    "This option is useful for validating only parts of an integration graph "
    "which imports other graphs.",
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Return the validation process identifier only. "
    "This is useful for piping the ID into other commands.",
)
@click.option(
    "--inspect",
    is_flag=True,
    help="Return the list of violations instead of the summary (includes --wait).",
)
@click.option(
    "--polling-interval",
    type=click.IntRange(min=1),
    show_default=True,
    default=1,
    help="How many seconds to wait between status polls. Status polls are"
    " cheap, so a higher polling interval is most likely not needed.",
)
@click.pass_context
def execute_command(  # noqa: PLR0913
    ctx: Context,
    iri: str,
    shape_graph: str,
    query: str,
    result_graph: str,
    replace: bool,
    ignore_graph: list[str],
    id_only: bool,
    wait: bool,
    inspect: bool,
    polling_interval: int,
) -> None:
    """Start a new validation process.

    Validation is performed on all typed resources of the data / context graph
    (and its sub-graphs). Each resource is validated against all applicable node
    shapes from the shape catalog.
    """
    app: ApplicationContext = ctx.obj
    if id_only and inspect:
        raise UsageError(
            "Output can be the summary (default), the process ID (--id-only) "
            "or the violation list (--inspect)."
        )
    process_id = validation.start(
        context_graph=iri,
        shape_graph=shape_graph,
        query=get_query_text(query, {"resource"}) if query else None,
        result_graph=result_graph,
        replace=replace,
        ignore_graph=ignore_graph,
    )
    if wait or inspect:
        _wait_for_process_completion(
            app=app, process_id=process_id, use_rich=not id_only, polling_interval=polling_interval
        )
    if id_only:
        app.echo_info(process_id)
        return
    if inspect:
        ctx.params["process_id"] = process_id
        data = violations_list.apply_filters(ctx=ctx, filter_=[])
        _print_violation_table(app=app, data_graph=iri, shape_graph=shape_graph, violations=data)
        return
    _print_process_summary(process_id=process_id, app=app)


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    multiple=True,
    help=validations_list.get_filter_help_text(),
    shell_complete=validations_list.complete_values,
)
@click.option(
    "--id-only",
    is_flag=True,
    help="List validation process identifier only. "
    "This is useful for piping the IDs into other commands.",
)
@click.option("--raw", is_flag=True, help="Outputs raw JSON of the validation list.")
@click.pass_context
def list_command(ctx: Context, filter_: tuple[tuple[str, str]], id_only: bool, raw: bool) -> None:
    """List running and finished validation processes.

    This command provides a filterable table or identifier list of validation
    processes. The command operates on the process summary and provides some statistics.

    Note: Detailed information on the found violations can be listed with the
    `graph validation inspect` command.
    """
    validations = validations_list.apply_filters(ctx=ctx, filter_=filter_)
    app: ApplicationContext = ctx.obj

    if raw:
        app.echo_info_json(validations)
        return

    if id_only:
        for _ in validations:
            app.echo_info(_["id"])
        return

    # output a user table
    table = []
    for _ in validations:
        row = [
            _["id"],
            _["state"],
            _.get("executionStarted", None),
            _["contextGraphIri"],
            _get_resource_count(_),
            _get_violation_count(_),
        ]
        table.append(row)
    app.echo_info_table(
        table,
        headers=["ID", "Status", "Started", "Graph", "Resources", "Violations"],
        caption=f"Validation Processes of {get_cmem_base_uri()}",
        cell_processing={2: TimeAgo(), 3: GraphLink()},
        empty_table_message="No validation processes found. "
        "Use `graph validation execute` to start a new validation process.",
    )


@click.command(cls=CmemcCommand, name="inspect")
@click.argument("process_id", type=click.STRING, shell_complete=_complete_all_batch_validations)
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    multiple=True,
    help=violations_list.get_filter_help_text(),
    shell_complete=violations_list.complete_values,
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Return violated resource identifier only. "
    "This is useful for piping the ID into other commands.",
)
@click.option(
    "--summary",
    is_flag=True,
    help="Outputs the summary of the graph validation "
    "instead of the violations list (not filterable).",
)
@click.option("--raw", is_flag=True, help="Outputs raw JSON of the validation result.")
@click.pass_context
def inspect_command(  # noqa: PLR0913
    ctx: Context,
    process_id: str,
    filter_: tuple[tuple[str, str]],
    id_only: bool,
    summary: bool,
    raw: bool,
) -> None:
    """List and inspect errors found with a validation process.

    This command provides detailed information on the found violations of
    a validation process.

    Use the `--filter` option to limit the output based on different criteria such as
    constraint name (`constraint`), origin node shape of the rule (`node-shape`), or
    the validated resource (`resource`).

    Note: Validation processes IDs can be listed with the `graph validation list`
    command, or by utilizing the tab completion of this command.
    """
    app: ApplicationContext = ctx.obj
    if process_id not in [_["id"] for _ in validation.get_all_aggregations()]:
        raise UsageError(f"Validation process with ID '{process_id}' is not known (anymore).")

    if summary:
        if raw:
            app.echo_info_json(validation.get_aggregation(batch_id=process_id))
        else:
            _print_process_summary(app=app, process_id=process_id)
        return

    data = violations_list.apply_filters(ctx=ctx, filter_=filter_)

    if id_only:
        show_violated_resources(app=app, data=data)
        return

    if raw:
        app.echo_info_json(data)
        return

    if len(data) == 0 and len(filter_) == 0:
        app.echo_warning(
            "The given validation process does not have any violations - "
            "I will show the summary instead."
        )
        _print_process_summary(app=app, process_id=process_id)
    else:
        process_data = validation.get_aggregation(batch_id=process_id)
        _print_violation_table(
            app=app,
            violations=data,
            shape_graph=process_data["shapeGraphIri"],
            data_graph=process_data["contextGraphIri"],
        )


@click.command(cls=CmemcCommand, name="cancel")
@click.argument("process_id", type=click.STRING, shell_complete=_complete_running_batch_validations)
@click.pass_obj
def cancel_command(app: ApplicationContext, process_id: str) -> None:
    """Cancel a running validation process.

    Note: In order to get the process IDs of all currently running validation
    processes, use the `graph validation list` command with the option
    `--filter status running`, or utilize the tab completion of this command.
    """
    all_status = {_["id"]: _["state"] for _ in validation.get_all_aggregations()}
    if process_id not in all_status:
        raise UsageError(f"Validation process with ID '{process_id}' is not known (anymore).")
    if all_status[process_id] != validation.STATUS_RUNNING:
        raise click.UsageError(
            f"Validation process with ID '{process_id}' is not a running anymore."
        )
    app.echo_info(f"Validation process with ID '{process_id}' ... ", nl=False)
    validation.cancel(batch_id=process_id)
    app.echo_success("cancelled")


@click.command(cls=CmemcCommand, name="export")
@click.argument(
    "process_ids", nargs=-1, type=click.STRING, shell_complete=_complete_finished_batch_validations
)
@click.option(
    "--output-file",
    type=click.Path(writable=True, allow_dash=False, dir_okay=False),
    default="report.xml",
    show_default=True,
    help="Export the report to this file. Existing files will be overwritten.",
)
@click.option(
    "--exit-1",
    type=click.Choice(["never", "error"]),
    default="error",
    show_default=True,
    help="Specify, when this command returns with exit code 1. Available options are "
    "'never' (exit 0, even if there are violations in the reports), "
    "'error' (exit 1 if there is at least one violation in a report).), ",
)
@click.option(
    "--format",
    "format_",
    type=click.Choice(["JSON", "XML"], case_sensitive=True),
    default="XML",
    help="Export either the plain JSON report or a distilled jUnit XML report.",
    show_default=True,
)
@click.pass_context
def export_command(
    ctx: Context, process_ids: tuple[str], output_file: str, exit_1: str, format_: str
) -> None:
    """Export a report of finished validations.

    This command exports a jUnit XML or JSON report in order to process
    them somewhere else (e.g. a CI pipeline).

    You can export a single report of multiple validation processes.

    For jUnit XML: Each validation process result will be transformed to
    a single test suite. All violations of one resource in a result will be
    collected and attached to a single test case in that test suite.

    Note: Validation processes IDs can be listed with the `graph validation list`
    command, or by utilizing the tab completion of this command.
    """
    if len(process_ids) == 0:
        raise UsageError("This command needs at least one validation process ID.")
    app: ApplicationContext = ctx.obj
    process_ids_to_test = {_: True for _ in process_ids}
    overall_violations = 0
    overall_resources = 0
    for _ in validation.get_all_aggregations():
        if _["id"] in process_ids_to_test:
            if _["state"] != "FINISHED":
                raise UsageError(f"Validation process with ID '{_['id']}' is still running.")
            del process_ids_to_test[_["id"]]
            overall_violations += int(_["violationsCount"])
            overall_resources += int(_["resourceProcessedCount"])
    if len(process_ids_to_test) > 0:
        raise UsageError(
            "Validation processes with the following IDs not known (anymore): "
            + ", ".join(process_ids_to_test)
        )
    reports = []
    for process_id in process_ids:
        report = validation.get(batch_id=process_id)
        reports.append(report)
    app.echo_info(
        f"Export of {len(reports)} validation report(s) with"
        f" {overall_violations} violations in {overall_resources} resources"
        f" to {output_file} ... ",
        nl=False,
    )
    output_path = Path(output_file)

    with output_path.open("w", encoding="utf-8") as file:
        if format_ == "XML":
            file.write(_reports_to_junit(reports))
        if format_ == "JSON":
            json.dump(reports, file, indent=2)
    app.echo_success("done")
    if exit_1 == "error" and overall_violations > 0:
        app.echo_error(
            "Exit 1 since violations where found in the reports "
            "(can be suppressed with '--exit-1 never')."
        )
        sys.exit(1)


@click.group(cls=CmemcGroup, name="validation")
def validation_group() -> CmemcGroup:  # type: ignore[empty-body]
    """Validate resources in a graph.

    This command group is dedicated to the management of resource validation processes.
    A validation process verifies, that resources in a specific graph are valid according
    to the node shapes in a shape catalog graph.

    Note: Validation processes are identified with a random ID and can be listed with
    the `graph validation list` command. To start or cancel validation processes,
    use the `graph validation execute` and `graph validation cancel` command.
    To inspect the found violations of a validation process, use the
    `graph validation inspect` command.
    """


validation_group.add_command(execute_command)
validation_group.add_command(list_command)
validation_group.add_command(inspect_command)
validation_group.add_command(cancel_command)
validation_group.add_command(export_command)
