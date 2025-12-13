"""query commands for cmem command line interface."""

import csv
import json
import sys
from hashlib import sha1
from json import JSONDecodeError, load
from shutil import get_terminal_size
from time import sleep, time
from uuid import uuid4

import click
from click.shell_completion import CompletionItem
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.queries import (
    QueryCatalog,
    SparqlQuery,
    cancel_query,
    get_query_status,
)
from requests import HTTPError

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.object_list import (
    DirectListPropertyFilter,
    DirectValuePropertyFilter,
    Filter,
    ObjectList,
    compare_int_greater_than,
    compare_regex,
)
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.smart_path import SmartPath as Path
from cmem_cmemc.utils import extract_error_message, struct_to_table

QUERY_FILTER_TYPES = sorted(["graph", "status", "slower-than", "type", "regex", "trace-id", "user"])
QUERY_FILTER_HELP_TEXT = (
    "Filter queries based on execution status and time. "
    f"First parameter --filter CHOICE can be one of {QUERY_FILTER_TYPES!s}"
    ". The second parameter is based on CHOICE, e.g. int in case of"
    " slower-than, or a regular expression string."
)


class ReplayStatistics:
    """Capture and calculate statistics of a query replay command run."""

    # pylint: disable=too-many-instance-attributes
    run_id: str
    query_minimum: int | None
    query_maximum: int | None
    loop_count: int
    loop_durations: dict[str, int]
    query_durations: dict[str, list[int]]
    current_loop_key: str
    total_duration: int = 0
    query_count: int = 0
    error_count: int = 0
    query_average: float
    catalog = QueryCatalog()
    app: ApplicationContext

    def __init__(self, app: ApplicationContext, label: str | None = None):
        """Initialize instance."""
        self.app = app
        self.label = label
        self.run_id = str(uuid4())
        self.loop_count = 0
        self.query_minimum = None
        self.query_maximum = None
        self.loop_durations = {}
        self.query_durations = {}

    def init_loop(self) -> str:
        """Initialize a new loop and reset the loop counts/values."""
        loop_key = str(uuid4())
        self.current_loop_key = loop_key
        self.loop_durations[loop_key] = 0
        self.query_durations[loop_key] = []
        self.loop_count += 1
        self.app.echo_debug(f"Loop {self.loop_count} started: {loop_key}")
        return loop_key

    def _init_query(self, query_: dict) -> SparqlQuery:
        """Initialize query from dict."""
        try:
            if "iri" in query_:
                iri = query_["iri"]
                catalog_entry = self.catalog.get_query(iri)
                if catalog_entry is None:
                    raise click.ClickException(f"measure_query - query {iri} is not in catalog.")
                return catalog_entry
            query_string = query_["queryString"]
            return SparqlQuery(text=query_string)
        except KeyError as error:
            raise click.ClickException(
                "measure_query - given input dict has no queryString key."
            ) from error

    def _update_statistic_on_success(self, duration: int) -> None:
        """Update statistics and counters."""
        self.query_durations[self.current_loop_key].append(duration)
        if self.query_minimum is None or duration < self.query_minimum:
            self.query_minimum = duration
        if self.query_maximum is None or duration > self.query_maximum:
            self.query_maximum = duration
        self.total_duration += duration
        self.loop_durations[self.current_loop_key] += duration
        self.query_average = self.total_duration / self.query_count

    def measure_query_duration(self, query_: dict) -> dict:
        """Execute a query and measure the duration."""
        # create the query object
        executed_query = self._init_query(query_)

        # update and return the query object
        if "id" not in query_:
            # create a UUID4, if needed
            query_["id"] = str(uuid4())
        # always re-hash
        query_["queryStringSha1Hash"] = sha1(  # nosec  # noqa: S324
            executed_query.text.encode("utf-8")
        ).hexdigest()
        if "queryString" not in query_:
            # add queryString for catalog queries
            query_["queryString"] = executed_query.text
        if "iri" in query_:
            # use the full IRI in case short one is given
            query_["iri"] = executed_query.url
        if "iri" in query_ and "label" not in query_:
            # extend with label if possible (and needed)
            query_["label"] = executed_query.label
        if "replays" not in query_:
            # create replays list if needed
            query_["replays"] = []

        # init replay object
        this_replay = {
            "runId": self.run_id,
            "loopId": str(self.current_loop_key),
            "replayId": str(uuid4()),
        }
        if self.label is not None:
            this_replay["runLabel"] = self.label

        # execute and measure the query
        try:
            start = round(time() * 1000)
            executed_query.get_results(replace_placeholder=False)
            end = round(time() * 1000)
            duration = end - start

            this_replay["executionStarted"] = str(start)
            this_replay["executionFinished"] = str(end)
            this_replay["executionTime"] = str(duration)

            # update statistics and counters
            self.query_count += 1
            self._update_statistic_on_success(duration)
        except HTTPError as error:
            self.error_count += 1
            this_replay["executionError"] = extract_error_message(error)

        query_["replays"].append(this_replay)
        self.app.echo_debug(
            f"Query {self.query_count + self.error_count} " f"executed: {this_replay['replayId']}"
        )
        return query_

    def create_output(self) -> dict:
        """Create the structure for the output commands."""
        # create dict from object but ignore some internal vars on output
        output = {
            key: value
            for (key, value) in dict(vars(self)).items()
            if key not in ("current_loop_key", "app")
        }
        loop_average = 0
        loop_minimum = None
        loop_maximum = None
        for loop_duration in self.loop_durations.values():
            loop_average += loop_duration
            if loop_minimum is None or loop_duration < loop_minimum:
                loop_minimum = loop_duration
            if loop_maximum is None or loop_duration > loop_maximum:
                loop_maximum = loop_duration
        output["loop_minimum"] = loop_minimum
        output["loop_maximum"] = loop_maximum
        output["loop_average"] = loop_average / len(self.loop_durations)
        return output

    def output_table(self) -> None:
        """Output a table of the statistic values."""
        table = struct_to_table(self.create_output())
        self.app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)

    def output_json(self) -> None:
        """Output json of the statistic values."""
        self.app.echo_info_json(self.create_output())


def get_queries(ctx: click.Context) -> list[dict]:  # noqa: ARG001
    """Get queries for object list"""
    _: list[dict] = get_query_status()
    return _


def transform_status_names(ctx: Filter, value: str) -> str:  # noqa: ARG001
    """Transform: status names

    FINISHED_SUCCESS -> finished
    FINISHED_* -> *
    others -> same
    all lowercase
    """
    value = value.replace("FINISHED_", "").lower()
    if value == "success":
        value = "finished"
    return value


query_status_list = ObjectList(
    name="queries",
    get_objects=get_queries,
    filters=[
        DirectValuePropertyFilter(
            name="status",
            description="List only queries which have a certain status.",
            property_key="queryExecutionState",
            transform=transform_status_names,
            fixed_completion=[
                CompletionItem("running", help="List only queries which are currently running."),
                CompletionItem(
                    "finished", help="List only queries which are successfully finished."
                ),
                CompletionItem(
                    "error", help="List only queries which were NOT successfully executed."
                ),
                CompletionItem("cancelled", help="List only queries which were cancelled."),
                CompletionItem("timeout", help="List only queries which ran into a timeout."),
            ],
            fixed_completion_only=True,
        ),
        DirectValuePropertyFilter(
            name="type",
            description="List only queries of a certain query type.",
            property_key="type",
        ),
        DirectValuePropertyFilter(
            name="trace-id",
            description="List only queries which have the specified trace ID.",
            property_key="traceId",
        ),
        DirectValuePropertyFilter(
            name="user",
            description="List only queries executed by the specified account (URL).",
            property_key="user",
        ),
        DirectListPropertyFilter(
            name="graph",
            description="List only queries which affected a certain graph (URL).",
            property_key="affectedGraphs",
        ),
        DirectValuePropertyFilter(
            name="slower-than",
            description="List only queries which are slower than X milliseconds.",
            property_key="executionTime",
            compare=compare_int_greater_than,
            fixed_completion=[
                CompletionItem("5", help="List only queries which are executed slower than 5ms."),
                CompletionItem(
                    "100", help="List only queries which are executed slower than 100ms."
                ),
                CompletionItem(
                    "1000", help="List only queries which are executed slower than 1000ms."
                ),
                CompletionItem(
                    "5000", help="List only queries which are executed slower than 5000ms."
                ),
            ],
        ),
        DirectValuePropertyFilter(
            name="regex",
            description="List only queries which query text matches a regular expression.",
            property_key="queryString",
            compare=compare_regex,
            fixed_completion=[
                CompletionItem(
                    r"http://schema.org",
                    help="List only queries which somehow use the schema.org namespace.",
                ),
                CompletionItem(
                    r"http://www.w3.org/2000/01/rdf-schema#",
                    help="List only queries which somehow use the RDF schema namespace.",
                ),
                CompletionItem(
                    r"?value",
                    help="List only queries which are using the ?value projection variable.",
                ),
                CompletionItem(
                    "^CREATE SILENT GRAPH",
                    help="List only queries which start with CREATE SILENT GRAPH.",
                ),
            ],
        ),
    ],
)


def _output_query_status_details(app: ApplicationContext, status_dict: dict) -> None:
    """Output key/value table as well as query string of a query.

    Args:
    ----
        app: application context
        status_dict: The dict from the query status list.

    """
    table = []
    for key in status_dict:
        if key != "queryString":
            row = [key, str(status_dict[key])]
            table.append(row)
    app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)
    app.echo_info("")
    app.echo_info_sparql(status_dict["queryString"])


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--catalog-graph",
    default="https://ns.eccenca.com/data/queries/",
    show_default=True,
    shell_complete=completion.graph_uris,
    help="The used query catalog graph.",
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only query identifier and no labels or other metadata. "
    "This is useful for piping the ids into other cmemc commands.",
)
@click.pass_obj
def list_command(app: ApplicationContext, catalog_graph: str, id_only: bool) -> None:
    """List available queries from the catalog.

    Outputs a list of query URIs which can be used as reference for
    the query execute command.
    """
    queries = QueryCatalog(graph=catalog_graph).get_queries().items()
    if id_only:
        # sort dict by short_url - https://docs.python.org/3/howto/sorting.html
        for _, sparql_query in sorted(queries, key=lambda k: k[1].short_url.lower()):
            app.echo_info(sparql_query.short_url)
    else:
        table = []
        for _, sparql_query in queries:
            row = [
                sparql_query.short_url,
                sparql_query.query_type,
                ",".join(sparql_query.get_placeholder_keys()),
                sparql_query.label,
            ]
            table.append(row)
        app.echo_info_table(
            table,
            headers=["Query URI", "Type", "Placeholder", "Label"],
            sort_column=3,
            empty_table_message="There are no query available in the "
            f"selected catalog ({catalog_graph}).",
            caption=f"Queries from {catalog_graph} ({get_cmem_base_uri()})",
        )


@click.command(cls=CmemcCommand, name="execute")
@click.argument(
    "QUERIES", nargs=-1, required=True, shell_complete=completion.remote_queries_and_sparql_files
)
@click.option(
    "--catalog-graph",
    default="https://ns.eccenca.com/data/queries/",
    show_default=True,
    shell_complete=completion.graph_uris,
    help="The used query catalog graph.",
)
@click.option(
    "--accept",
    default="default",
    show_default=True,
    shell_complete=completion.sparql_accept_types,
    help="Accept header for the HTTP request(s). Setting this to 'default' "
    "means that cmemc uses an appropriate output for terminals.",
)
@click.option(
    "--no-imports",
    is_flag=True,
    help="Graphs which include other graphs (using owl:imports) will be "
    "queried as merged overall-graph. This flag disables this "
    "default behaviour. The flag has no effect on update queries.",
)
@click.option(
    "--base64",
    is_flag=True,
    help="Enables base64 encoding of the query parameter for the "
    "SPARQL requests (the response is not touched). "
    "This can be useful in case there is an aggressive firewall between "
    "cmemc and Corporate Memory.",
)
@click.option(
    "--parameter",
    "-p",
    type=(str, str),
    shell_complete=completion.placeholder,
    multiple=True,
    help="In case of a parameterized query (placeholders with the '{{key}}' "
    "syntax), this option fills all placeholder with a given value "
    "before the query is executed."
    "Pairs of placeholder/value need to be given as a tuple 'KEY VALUE'. "
    "A key can be used only once.",
)
@click.option(
    "--limit",
    type=int,
    help="Override or set the LIMIT in the executed SELECT query. Note that "
    "this option will never give you more results than the LIMIT given "
    "in the query itself.",
)
@click.option("--offset", type=int, help="Override or set the OFFSET in the executed SELECT query.")
@click.option(
    "--distinct", is_flag=True, help="Override the SELECT query by make the result set DISTINCT."
)
@click.option(
    "--timeout", type=int, help="Set max execution time for query evaluation (in milliseconds)."
)
@click.pass_obj
def execute_command(  # noqa: PLR0913
    app: ApplicationContext,
    queries: tuple[str, ...],
    catalog_graph: str,
    accept: str,
    no_imports: bool,
    base64: bool,
    parameter: tuple[tuple[str, str], ...],
    limit: int,
    offset: int,
    distinct: bool,
    timeout: int,
) -> None:
    """Execute queries which are loaded from files or the query catalog.

    Queries are identified either by a file path, a URI from the query
    catalog, or a shortened URI (qname, using a default namespace).

    If multiple queries are executed one after the other, the first failing
    query stops the whole execution chain.

    Limitations: All optional parameters (e.g. accept, base64, ...) are
    provided for ALL queries in an execution chain. If you need different
    parameters for each query in a chain, run cmemc multiple times and use
    the logical operators && and || of your shell instead.
    """
    # pylint: disable=too-many-arguments
    placeholder = {}
    for key, value in parameter:
        if key in placeholder:
            raise click.UsageError(
                "Parameter can be given only once, " f"Value for '{key}' was given twice."
            )
        placeholder[key] = value
    app.echo_debug("Parameter: " + str(placeholder))
    for file_or_uri in queries:
        app.echo_debug(f"Start of execution: {file_or_uri} with " f"placeholder {placeholder}")
        executed_query: SparqlQuery = QueryCatalog(graph=catalog_graph).get_query(
            file_or_uri, placeholder=placeholder
        )
        if executed_query is None:
            raise click.UsageError(
                f"{file_or_uri} is neither a (readable) file nor "
                f"a query URI in the catalog graph {catalog_graph}"
            )
        app.echo_debug(
            f"Execute ({executed_query.query_type}): "
            f"{executed_query.label} < {executed_query.url}"
        )
        if accept == "default":
            submitted_accept = executed_query.get_default_accept_header()
            app.echo_debug(f"Accept header set to default value: '{submitted_accept}'")
        else:
            submitted_accept = accept

        results = executed_query.get_results(
            accept=submitted_accept,
            owl_imports_resolution=not no_imports,
            base64_encoded=base64,
            placeholder=placeholder,
            distinct=distinct,
            limit=limit,
            offset=offset,
            timeout=timeout,
        )
        if accept == "default" and submitted_accept == "text/csv":
            csv_reader = csv.reader(results.splitlines(), delimiter=",", quotechar='"')
            table = []
            headers = []
            for index, row in enumerate(csv_reader):
                if index == 0:
                    headers = row
                else:
                    table.append(row)
            app.echo_info_table(
                table,
                headers=headers,
                empty_table_message="No results for this query.",
                caption=f"Query results: {executed_query.label}",
            )
        else:
            app.echo_result(results)


@click.command(cls=CmemcCommand, name="open")
@click.argument(
    "QUERIES", nargs=-1, required=True, shell_complete=completion.remote_queries_and_sparql_files
)
@click.option(
    "--catalog-graph",
    default="https://ns.eccenca.com/data/queries/",
    show_default=True,
    shell_complete=completion.graph_uris,
    help="The used query catalog graph.",
)
@click.pass_obj
def open_command(app: ApplicationContext, queries: tuple[str, ...], catalog_graph: str) -> None:
    """Open queries in the editor of the query catalog in your browser.

    With this command, you can open (remote) queries from the query catalog in
    the query editor in your browser (e.g. in order to change them).
    You can also load local query files into the query editor, in order to
    import them into the query catalog.

    The command accepts multiple query URIs or files which results in
    opening multiple browser tabs.
    """
    for file_or_uri in queries:
        opened_query = QueryCatalog(graph=catalog_graph).get_query(file_or_uri)
        if opened_query is None:
            raise click.UsageError(
                f"{file_or_uri} is neither a (readable) file nor "
                f"a query URI in the catalog graph {catalog_graph}"
            )
        open_query_uri = opened_query.get_editor_url(graph=catalog_graph)
        app.echo_debug(f"Open {file_or_uri}: {open_query_uri}")
        click.launch(open_query_uri)


@click.command(cls=CmemcCommand, name="status")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only query identifier and no labels or other metadata. "
    "This is useful for piping the ids into other cmemc commands.",
)
@click.option("--raw", is_flag=True, help="Outputs raw JSON response of the query status API.")
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    multiple=True,
    help=query_status_list.get_filter_help_text(),
    shell_complete=query_status_list.complete_values,
)
@click.argument("query_id", required=False, type=click.STRING)
@click.pass_context
def status_command(
    ctx: click.Context,
    id_only: bool,
    raw: bool,
    filter_: tuple[tuple[str, str]],
    query_id: str,
) -> None:
    """Get status information of executed and running queries.

    With this command, you can access the latest executed SPARQL queries
    on the Explore backend (DataPlatform).
    These queries are identified by UUIDs and listed
    ordered by starting timestamp.

    You can filter queries based on status and runtime in order to investigate
    slow queries. In addition to that, you can get the details of a specific
    query by using the ID as a parameter.
    """
    width, height = get_terminal_size((120, 20))
    max_query_string_width = width - 46 - 1
    app: ApplicationContext = ctx.obj
    app.echo_debug(f"Terminal size = {width} x {height}")

    if query_id:
        query_status_list.add_filter(
            DirectValuePropertyFilter(name="id", property_key="id", description="id")
        )
        queries = query_status_list.apply_filters(ctx=ctx, filter_=[("id", query_id)])
        query_status_list.remove_filter("id")
    else:
        queries = query_status_list.apply_filters(ctx=ctx, filter_=filter_)

    if query_id and len(queries) == 0:
        raise click.UsageError(f"Query with ID '{query_id}' does not exist (anymore).")

    if raw:
        app.echo_info_json(queries)
        return

    if id_only:
        for _ in queries:
            app.echo_info(_["id"])
        return

    if query_id:
        _output_query_status_details(app, queries[0])
        return
    table = []
    for _ in queries:
        query_id = _["id"]
        query_execution_time = str(_.get("executionTime", ""))
        query_string = " ".join(_["queryString"].splitlines())
        if len(query_string) > max_query_string_width:
            query_string = query_string[0:max_query_string_width] + "…"
        row = [query_id, query_execution_time, query_string]
        table.append(row)
    app.echo_info_table(table, headers=["Query ID", "Time", "Query String"])


@click.command(cls=CmemcCommand, name="replay")
@click.argument(
    "REPLAY_FILE",
    required=True,
    shell_complete=completion.replay_files,
    type=ClickSmartPath(exists=True, allow_dash=False, readable=True, dir_okay=False),
)
@click.option("--raw", is_flag=True, help="Output the execution statistic as raw JSON.")
@click.option(
    "--loops",
    required=False,
    default=1,
    show_default=True,
    type=int,
    help="Number of loops to run the replay file.",
)
@click.option(
    "--wait",
    required=False,
    default=0,
    show_default=True,
    type=int,
    help="Number of seconds to wait between query executions.",
)
@click.option(
    "--output-file",
    required=False,
    shell_complete=completion.replay_files,
    help="Save the optional output to this file. Input and output of the "
    "command can be the same file. The output is written at the end "
    "of a successful command execution. The output can be stdout "
    "('-') - in this case, the execution statistic output is "
    "oppressed.",
    type=ClickSmartPath(exists=False, allow_dash=True, writable=True, dir_okay=False),
)
@click.option("--run-label", type=click.STRING, help="Optional label of this replay run.")
@click.pass_obj
def replay_command(  # noqa: PLR0913
    app: ApplicationContext,
    replay_file: str,
    raw: bool,
    loops: int,
    wait: int,
    output_file: str,
    run_label: str,
) -> None:
    """Re-execute queries from a replay file.

    This command reads a REPLAY_FILE and re-executes the logged queries.
    A REPLAY_FILE is a JSON document which is an array of JSON objects with
    at least a key `queryString` holding the query text OR a key `iri`
    holding the IRI of the query in the query catalog.
    It can be created with the `query status` command.

    Example: query status --raw > replay.json

    The output of this command shows basic query execution statistics.

    The queries are executed one after another in the order given in the
    input REPLAY_FILE. Query placeholders / parameters are ignored. If a
    query results in an error, the duration is not counted.

    The optional output file is the same JSON document which is used as input,
    but each query object is annotated with an additional `replays` object,
    which is an array of JSON objects which hold values for the
    replay|loop|run IDs, start and end time as well as duration and
    other data.
    """
    if loops <= 0:
        raise click.UsageError("Please set a positive loops integer value (>=1).")
    try:
        with Path(replay_file).open(encoding="utf8") as _:
            input_queries = load(_)
    except JSONDecodeError as error:
        raise click.ClickException(f"File {replay_file} is not a valid JSON document.") from error
    if len(input_queries) == 0:
        raise click.ClickException(f"File {replay_file} contains no queries.")
    app.echo_debug(f"File {replay_file} contains {len(input_queries)} queries.")

    statistic = ReplayStatistics(app=app, label=run_label)
    for _loop in range(loops):
        statistic.init_loop()
        for _ in input_queries:
            statistic.measure_query_duration(_)
            if wait > 0:
                sleep(wait)

    if output_file:
        if output_file == "-":
            app.echo_info_json(input_queries)
            return
        with Path(output_file).open(mode="w", encoding="utf-8") as output:
            json.dump(input_queries, output, ensure_ascii=False, indent=2)

    if raw:
        statistic.output_json()
    else:
        statistic.output_table()


@click.command(cls=CmemcCommand, name="cancel")
@click.argument("query_id", required=True, type=click.STRING)
@click.pass_context
def cancel_command(ctx: click.Context, query_id: str) -> None:
    """Cancel a running query.

    With this command, you can cancel a running query.
    Depending on the backend triple store, this will result in a
    broken result stream (stardog, neptune and virtuoso) or a valid
    result stream with incomplete results (graphdb)
    """
    app = ctx.obj
    app.echo_info(f"Cancel query {query_id} ... ", nl=False)
    query_status_list.add_filter(
        DirectValuePropertyFilter(name="id", property_key="id", description="id")
    )
    queries = query_status_list.apply_filters(
        ctx=ctx, filter_=[("id", query_id), ("status", "running")]
    )
    if not queries:
        app.echo_error("not known or not running (anymore)")
        sys.exit(1)
    cancel_query(queries[0]["id"])
    app.echo_success("done")


@click.group(cls=CmemcGroup)
def query() -> CmemcGroup:  # type: ignore[empty-body]
    """List, execute, get status or open SPARQL queries.

    Queries are identified either by a file path, a URI from the query
    catalog or a shortened URI (qname, using a default namespace).

    One or more queries can be executed one after the other with the
    execute command. With open command you can jump to the query editor in your
    browser.

    Queries can use a mustache like syntax to specify placeholder for
    parameter values (e.g. {{resourceUri}}). These parameter values need to
    be given as well, before the query can be executed (use the -p option).

    Note: In order to get a list of queries from the query catalog, execute
    the `query list` command or use tab-completion.
    """


query.add_command(execute_command)
query.add_command(list_command)
query.add_command(open_command)
query.add_command(status_command)
query.add_command(replay_command)
query.add_command(cancel_command)
