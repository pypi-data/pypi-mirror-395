"""graph commands for cmem command line interface."""

import gzip
import hashlib
import io
import json
import mimetypes
import os
from xml.dom import minidom  # nosec
from xml.etree.ElementTree import (  # nosec
    Element,
    SubElement,
    tostring,
)

import click
from click import ClickException, Context, UsageError
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.dp.authorization import refresh
from cmem.cmempy.dp.proxy import graph as graph_api
from cmem.cmempy.dp.proxy.graph import get_graph_imports
from cmem.cmempy.dp.proxy.sparql import get as sparql_api
from jinja2 import Template
from six.moves.urllib.parse import quote

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.commands.graph_imports import graph_imports_list, imports_group
from cmem_cmemc.commands.graph_insights import insights_group
from cmem_cmemc.commands.validation import validation_group
from cmem_cmemc.constants import UNKNOWN_GRAPH_ERROR
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.smart_path import SmartPath
from cmem_cmemc.utils import (
    RdfGraphData,
    convert_uri_to_filename,
    get_graphs,
    get_graphs_as_dict,
    iri_to_qname,
    read_rdf_graph_files,
    tuple_to_list,
)


def count_graph(graph_iri: str) -> int:
    """Count triples in a graph and return integer."""
    query = "SELECT (COUNT(*) AS ?triples) " + " FROM <" + graph_iri + "> WHERE { ?s ?p ?o }"  # noqa: S608
    result = json.loads(sparql_api(query, owl_imports_resolution=False))
    count = result["results"]["bindings"][0]["triples"]["value"]
    return int(count)


def _get_graph_to_file(  # noqa: PLR0913
    graph_iri: str,
    file_path: str,
    app: ApplicationContext,
    numbers: tuple[int, int] | None = None,
    overwrite: bool = True,
    mime_type: str = "application/n-triples",
) -> None:
    """Request a single graph to a single file (streamed).

    numbers is a tuple of current and count (for output only).
    """
    if SmartPath(file_path).exists():
        if overwrite is True:
            app.echo_warning(f"Output file {file_path} does exist: will overwrite it.")
        else:
            app.echo_warning(f"Output file {file_path} does exist: will append to it.")
    if numbers is not None:
        running_number, count = numbers
        if running_number is not None and count is not None:
            app.echo_info(
                f"Export graph {running_number}/{count}: " f"{graph_iri} to {file_path} ... ",
                nl=False,
            )
    # create and write the .ttl content file
    mode = "wb" if overwrite is True else "ab"

    with (
        gzip.open(file_path, mode)
        if file_path.endswith(".gz")
        else click.open_file(file_path, mode) as triple_file,
        graph_api.get_streamed(graph_iri, accept=mime_type) as response,
    ):
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                triple_file.write(chunk)
        request_headers = response.request.headers
        request_headers.pop("Authorization")
        app.echo_debug(f"cmemc request headers: {request_headers}")
        app.echo_debug(f"server response headers: {response.headers}")
    if numbers is not None:
        app.echo_success("done")


def _get_export_names(
    app: ApplicationContext, iris: list[str], template: str, file_extension: str = ".ttl"
) -> dict:
    """Get a dictionary of generated file names based on a template.

    Args:
    ----
        app: the context click application
        iris: list of graph iris
        template (str): the template string to use
        file_extension(str): the file extension to use

    Returns:
    -------
        a dictionary with IRIs as keys and filenames as values

    Raises:
    ------
        ClickException in case the template string produces a naming clash,
            means two IRIs result in the same filename

    """
    template_data = app.get_template_data()
    _names = {}
    for iri in iris:
        template_data.update(
            hash=hashlib.sha256(iri.encode("utf-8")).hexdigest(),
            iriname=convert_uri_to_filename(iri),
        )
        _name_created = f"{Template(template).render(template_data)}{file_extension}"
        _names[iri] = _name_created
    if len(_names.values()) != len(set(_names.values())):
        raise ClickException(
            "The given template string produces a naming clash. "
            "Please use a different template to produce unique names."
        )
    return _names


def _get_graphs_filtered(filter_name: str, filter_value: str) -> list[dict]:
    """Get graphs but filtered according to name and value."""
    # not filtered means all graphs
    graphs: list[dict]
    if filter_name is None:
        return get_graphs()
    # check for correct filter names
    possible_filter_names = ("access", "imported-by")
    if filter_name not in possible_filter_names:
        raise ClickException(
            f"{filter_name} is an unknown filter name. " f"Use one of {possible_filter_names}."
        )
    # filter by access condition
    if filter_name == "access":
        if filter_value == "writeable":
            graphs = get_graphs(writeable=True, readonly=False)
        elif filter_value == "readonly":
            graphs = get_graphs(writeable=False, readonly=True)
        else:
            raise ClickException("Filter access is either 'readonly' or 'writeable'.")
    else:
        # default is all graphs
        graphs = get_graphs()
    # filter by imported-by
    if filter_name == "imported-by":
        if filter_value not in get_graphs_as_dict():
            raise ClickException(UNKNOWN_GRAPH_ERROR.format(filter_value))
        imported_graphs = get_graph_imports(filter_value)
        graphs = [_ for _ in graphs if _["iri"] in imported_graphs]
    return graphs


def _add_imported_graphs(iris: list[str], all_graphs: dict) -> list[str]:
    """Get a list of graph IRIs extended with the imported graphs.

    Args:
    ----
        iris: list of graph IRIs
        all_graphs: output of get_graphs_as_dict (dict of all graphs)

    Returns:
    -------
        list of graph IRIs

    """
    extended_list = iris
    for iri in set(iris):
        for _ in get_graph_imports(iri):
            # check if graph exist
            if _ in all_graphs:
                extended_list.append(_)
    return list(set(extended_list))


def _check_and_extend_exported_graphs(
    iris: list[str], all_flag: bool, imported_flag: bool, all_graphs: dict
) -> list[str]:
    """Get a list of IRIs checked and extended.

    Args:
    ----
        iris: List or tuple of given user IRIs
        all_flag: user wants all graphs
        imported_flag: user wants imported graphs as well
        all_graphs: dict of all graphs (get_graph_as_dict())

    Returns:
    -------
        checked and extended list of IRIs

    Raises:
    ------
         UsageError or ClickException

    """
    # transform given IRI-tuple to a distinct IRI-list
    iris = list(set(iris))
    if len(iris) == 0 and not all_flag:
        raise UsageError(
            "Either provide at least one graph IRI or use the --all option "
            "in order to work with all graphs."
        )
    for iri in iris:
        if iri not in all_graphs:
            raise ClickException(UNKNOWN_GRAPH_ERROR.format(iri))
    if all_flag:
        # in case --all is given,
        # list of graphs is filled with all available graph IRIs
        iris = [str(_) for _ in all_graphs]
    elif imported_flag:
        # does not need be executed in case of --all
        iris = _add_imported_graphs(iris, all_graphs)
    return iris


def _create_xml_catalog_file(app: ApplicationContext, names: dict, output_dir: str) -> None:
    """Create a Protégé suitable XML catalog file.

    Args:
    ----
        app: the cmemc context object
        names: output of _get_export_names()
        output_dir: path where to create the XML file

    """
    file_name = SmartPath(output_dir) / "catalog-v001.xml"
    catalog = Element("catalog")
    catalog.set("prefer", "public")
    catalog.set("xmlns", "urn:oasis:names:tc:entity:xmlns:xml:catalog")
    for name in names:
        uri = SubElement(catalog, "uri")
        uri.set("id", "Auto-Generated Import Resolution by cmemc")
        uri.set("name", name)
        uri.set("uri", names[name])
    parsed_string = minidom.parseString(  # nosec - since source is trusted  # noqa: S318
        tostring(catalog, "utf-8")
    ).toprettyxml(indent="  ")
    file = click.open_file(str(file_name), "w")
    file.truncate(0)
    file.write(parsed_string)
    app.echo_success(f"XML catalog file created as {file_name}.")


@click.command(cls=CmemcCommand, name="tree", hidden=True)
@click.option("-a", "--all", "all_", is_flag=True, help="Show tree of all (readable) graphs.")
@click.option("--raw", is_flag=True, help="Outputs raw JSON of the graph importTree API response.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only graph identifier (IRIs) and no labels or other "
    "metadata. This is useful for piping the IRIs into other commands. "
    "The output with this option is a sorted, flat, de-duplicated list "
    "of existing graphs.",
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    shell_complete=completion.graph_uris,
    callback=tuple_to_list,
)
@click.pass_context
def tree_command(ctx: Context, all_: bool, raw: bool, id_only: bool, iris: list[str]) -> None:
    """(Hidden) Deprecated: use 'graph imports tree' instead."""
    app: ApplicationContext = ctx.obj
    app.echo_warning(
        "The 'tree' command is deprecated and will be removed with the next major release."
        " Please use the 'graph imports tree' command instead."
    )
    imports_cmd = graph.commands["imports"]
    tree_cmd = imports_cmd.commands["tree"]  # type: ignore[attr-defined]
    ctx.invoke(tree_cmd, all_=all_, raw=raw, id_only=id_only, iris=iris)


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON of the graphs list API response.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only graph identifier (IRIs) and no labels or other "
    "metadata. This is useful for piping the IRIs into other commands.",
)
@click.option(
    "--filter",
    "filter_",
    type=click.Tuple([click.Choice(["access", "imported-by"]), str]),
    shell_complete=completion.graph_list_filter,
    default=[None] * 2,
    help="Filter graphs based on effective access conditions or import "
    "closure. "
    "First parameter CHOICE can be 'access' or 'imported-by'. "
    "The second parameter can be 'readonly' or 'writeable' in case "
    "of 'access' or any readable graph in case of 'imported-by'.",
)
@click.pass_obj
def list_command(
    app: ApplicationContext, raw: bool, id_only: bool, filter_: tuple[str, str]
) -> None:
    """List accessible graphs."""
    filter_name, filter_value = filter_
    graphs = _get_graphs_filtered(filter_name, filter_value)

    if raw:
        app.echo_info_json(graphs)
        return
    if id_only:
        # output a sorted list of graph IRIs
        for graph_desc in sorted(graphs, key=lambda k: k["iri"].lower()):
            app.echo_result(graph_desc["iri"])
        return
    # output a user table
    table = []
    for _ in graphs:
        if len(_["assignedClasses"]) > 0:
            graph_class = iri_to_qname(sorted(_["assignedClasses"])[0])
        else:
            graph_class = ""
        row = [
            _["iri"],
            graph_class,
            _["label"]["title"],
        ]
        table.append(row)
    app.echo_info_table(
        table,
        headers=["Graph IRI", "Type", "Label"],
        sort_column=2,
        empty_table_message="No graphs found. "
        "Use the `graph import` command to import a graph from a file, or "
        "use the `admin store bootstrap` command to import the default graphs.",
    )


def _validate_export_command_input_parameters(
    output_dir: str, output_file: str, compress: str, create_catalog: bool
) -> None:
    """Validate export command input parameters combinations"""
    if output_dir and create_catalog and compress:
        raise UsageError(
            "Cannot create a catalog file when using a compressed graph file."
            " Please remove either the --create-catalog or --compress option."
        )
    if output_file == "- " and compress:
        raise UsageError("Cannot output a binary file to terminal. Use --output-file option.")


def _write_graph_imports(ctx: Context, filename: str, iri: str) -> None:
    imports = graph_imports_list.apply_filters(ctx=ctx, filter_=[("to-graph", iri)])
    if imports:
        imports_file = click.open_file(filename, "w")
        for _ in imports:
            imports_file.write(_["from_graph"] + "\n")
        imports_file.close()


# pylint: disable=too-many-arguments,too-many-locals
@click.command(cls=CmemcCommand, name="export")
@click.option("-a", "--all", "all_", is_flag=True, help="Export all readable graphs.")
@click.option(
    "--include-imports",
    is_flag=True,
    help="Export selected graph(s) and all graphs which are imported from "
    "these selected graph(s).",
)
@click.option(
    "--include-import-statements",
    is_flag=True,
    help="Save graph imports information from other graphs to the exported graphs "
    "and write *.imports files.",
)
@click.option(
    "--create-catalog",
    is_flag=True,
    help="In addition to the .ttl and .graph files, cmemc will create an "
    "XML catalog file (catalog-v001.xml) which can be used by "
    "applications such as Protégé.",
)
@click.option(
    "--output-dir",
    type=ClickSmartPath(writable=True, file_okay=False),
    help="Export to this directory.",
)
@click.option(
    "--output-file",
    type=ClickSmartPath(writable=True, allow_dash=True, dir_okay=False),
    default="-",
    show_default=True,
    shell_complete=completion.triple_files,
    help="Export to this file.",
)
@click.option(
    "--filename-template",
    "-t",
    "template",
    default="{{hash}}",
    show_default=True,
    type=click.STRING,
    shell_complete=completion.graph_export_templates,
    help="Template for the export file name(s). "
    "Used together with --output-dir. "
    "Possible placeholders are (Jinja2): "
    "{{hash}} - sha256 hash of the graph IRI, "
    "{{iriname}} - graph IRI converted to filename, "
    "{{connection}} - from the --connection option and "
    "{{date}} - the current date as YYYY-MM-DD. "
    "The file suffix will be appended. "
    "Needed directories will be created.",
)
@click.option(
    "--mime-type",
    default="text/turtle",
    show_default=True,
    type=click.Choice(["application/n-triples", "text/turtle", "application/rdf+xml"]),
    help="Define the requested mime type",
)
@click.option(
    "--compress",
    type=click.Choice(["gzip"]),
    help="Compress the exported graph files.",
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    shell_complete=completion.graph_uris,
    callback=tuple_to_list,
)
@click.pass_context
def export_command(  # noqa: C901, PLR0913
    ctx: Context,
    all_: bool,
    include_imports: bool,
    include_import_statements: bool,
    create_catalog: bool,
    output_dir: str,
    output_file: str,
    template: str,
    mime_type: str,
    iris: list[str],
    compress: str,
) -> None:
    """Export graph(s) as NTriples to stdout (-), file or directory.

    In case of file export, data from all selected graphs will be concatenated
    in one file.
    In case of directory export, .graph and .ttl files will be created
    for each graph.
    """
    app: ApplicationContext = ctx.obj
    _validate_export_command_input_parameters(output_dir, output_file, compress, create_catalog)
    iris = _check_and_extend_exported_graphs(iris, all_, include_imports, get_graphs_as_dict())

    count: int = len(iris)
    app.echo_debug("graph count is " + str(count))
    if output_dir:
        # output directory set
        app.echo_debug("output is directory")
        # pre-calculate all filenames with the template,
        # in order to output errors on naming clashes as early as possible
        extension = mimetypes.guess_extension(mime_type)
        _names = _get_export_names(
            app, iris, template, f"{extension}.gz" if compress else f"{extension}"
        )
        _graph_file_names = _get_export_names(app, iris, template, f"{extension}.graph")
        _graph_imports_file_names = _get_export_names(app, iris, template, f"{extension}.imports")

        # create directory
        if not SmartPath(output_dir).exists():
            app.echo_warning("Output directory does not exist: " + "will create it.")
            SmartPath(output_dir).mkdir(parents=True)
        # one .graph, one .ttl file per named graph
        for current, iri in enumerate(iris, start=1):
            # join with given output directory and normalize full path
            triple_file_name = os.path.normpath(SmartPath(output_dir) / _names[iri])
            graph_file_name = os.path.normpath(SmartPath(output_dir) / _graph_file_names[iri])
            imports_file_name = os.path.normpath(
                SmartPath(output_dir) / _graph_imports_file_names[iri]
            )
            # output directory is created lazy
            SmartPath(triple_file_name).parent.mkdir(parents=True, exist_ok=True)
            # create and write the .ttl.graph metadata file
            graph_file = click.open_file(graph_file_name, "w")
            graph_file.write(iri + "\n")
            graph_file.close()
            if include_import_statements:
                _write_graph_imports(ctx=ctx, filename=imports_file_name, iri=iri)
            _get_graph_to_file(
                iri, triple_file_name, app, numbers=(current, count), mime_type=mime_type
            )

        if create_catalog:
            _create_xml_catalog_file(app, _names, output_dir)
        return
    # no output directory set -> file export
    if output_file == "-":
        if compress:
            raise UsageError("Cannot output a binary file to terminal. Use --output-file option.")
        # in case a file is stdout,
        # all triples from all graphs go in and other output is suppressed
        app.echo_debug("output is stdout")
        for iri in iris:
            _get_graph_to_file(iri, output_file, app, mime_type=mime_type)
    else:
        # in case a file is given, all triples from all graphs go in
        if compress and not output_file.endswith(".gz"):
            output_file = output_file + ".gz"

        app.echo_debug("output is file")
        for current, iri in enumerate(iris, start=1):
            _get_graph_to_file(
                iri,
                output_file,
                app,
                numbers=(current, count),
                overwrite=False,
                mime_type=mime_type,
            )


def validate_input_path(input_path: str) -> None:
    """Validate input path

    This function checks the provided folder for any .ttl or .nt files
    that have corresponding .gz files. If such files are found, it raises a ClickException.
    """
    files = os.listdir(input_path)

    # Check for files with the given extensions (.ttl and .nt)
    rdf_files = [f for f in files if f.endswith((".ttl", ".nt"))]

    # Check for corresponding .gz files
    gz_files = [f"{f}.gz" for f in rdf_files]
    conflicting_files = [f for f in gz_files if f in files]

    if conflicting_files:
        raise ClickException(
            f"The following RDF files (.ttl/.nt) have corresponding '.gz' files,"
            f" which is not allowed: {', '.join(conflicting_files)}"
        )


def _get_graph_supported_formats() -> dict[str, str]:
    return {
        "application/rdf+xml": "xml",
        "application/ld+json": "jsonld",
        "text/turtle": "turtle",
        "application/n-triples": "nt",
    }


def _get_buffer_and_content_type(
    triple_file: str, app: ApplicationContext
) -> tuple[io.BytesIO, str, None | str]:
    """Get the io.BytesIO buffer, the content type and the content encoding of a triple_file"""
    smart_file = SmartPath(triple_file)
    content_type, encoding = mimetypes.guess_type(triple_file)
    content_encoding = "gzip" if smart_file.name.endswith(".gz") else None
    if content_type is None:
        content_type = "text/turtle"
        for supported_type, supported_suffix in _get_graph_supported_formats().items():
            if smart_file.name.endswith(f".{supported_suffix}") or smart_file.name.endswith(
                f".{supported_suffix}.gz"
            ):
                content_type = supported_type
    elif content_type not in _get_graph_supported_formats():
        app.echo_warning(
            f"Content type {content_type} of {triple_file} is "
            f"not one of {', '.join(_get_graph_supported_formats().keys())} "
            "(but will try to import anyways)."
        )

    transport_params = {}
    if smart_file.schema in ["http", "https"]:
        transport_params["headers"] = {
            "Accept": "text/turtle; q=1.0, application/x-turtle; q=0.9, text/n3;"
            " q=0.8, application/rdf+xml; q=0.5, text/plain; q=0.1"
        }

    buffer = io.BytesIO()
    with ClickSmartPath.open(triple_file, transport_params=transport_params) as file_obj:
        buffer.write(file_obj.read())
    buffer.seek(0)
    return buffer, content_type, content_encoding


def _create_graph_imports(ctx: Context, graphs: list[RdfGraphData]) -> None:
    # Locate and invoke the 'create' subcommand under 'graph imports' command
    app: ApplicationContext = ctx.obj
    imports_cmd = graph.commands["imports"]
    create_cmd = imports_cmd.commands["create"]  # type: ignore[attr-defined]
    for _ in graphs:
        if not _.graph_imports:
            continue
        for _import in _.graph_imports:
            from_graph = _import
            to_graph = _.graph_iri
            imports = graph_imports_list.apply_filters(
                ctx=ctx, filter_=[("from-graph", from_graph), ("to-graph", to_graph)]
            )
            if imports:
                app.echo_info(
                    f"Creating graph import from {from_graph} to {to_graph} ... ", nl=False
                )
                app.echo_warning("exists")
            else:
                ctx.invoke(create_cmd, from_graph=from_graph, to_graph=to_graph)


def _process_input_directory(input_path: str, iri: str) -> list[RdfGraphData]:
    if iri is None:
        # in case a directory is the source (and no IRI is given),
        # the graph/nt file structure is crawled
        graphs = read_rdf_graph_files(input_path)
    else:
        # in case a directory is the source AND IRI is given
        graphs = []
        for _ in _get_graph_supported_formats():
            extension = mimetypes.guess_extension(_)
            graphs += [
                RdfGraphData(str(file), iri, [])
                for file in SmartPath(input_path).glob(f"*{extension}")
            ]
            graphs += [
                RdfGraphData(str(file), iri, [])
                for file in SmartPath(input_path).glob(f"*{extension}.gz")
            ]
    return graphs


def _validate_graph_imports(graphs_to_import: list[RdfGraphData]) -> None:
    graphs = {_["iri"] for _ in get_graphs()}
    graphs.update({_.graph_iri for _ in graphs_to_import})
    graph_imports: set[str] = set()
    for graph_data in graphs_to_import:
        for item in graph_data.graph_imports:
            graph_imports.add(str(item))
    if graph_imports - graphs:
        raise click.UsageError(
            f"The following graphs are not available, "
            f"so you can not add import statements to them: {','.join(graph_imports - graphs)}"
        )


@click.command(cls=CmemcCommand, name="import")
@click.option(
    "--replace",
    is_flag=True,
    help="Replace / overwrite the graph(s), instead of just adding the triples to the graph.",
)
@click.option(
    "--skip-existing",
    is_flag=True,
    help="Skip importing a file if the target graph already exists in "
    "the store. Note that the graph list is fetched once at the "
    "beginning of the process, so that you can still add multiple "
    "files to one single graph (if it does not exist).",
)
@click.option(
    "--include-import-statements",
    is_flag=True,
    help="Use *.imports files to re-apply the graph imports of the imported graphs.",
)
@click.argument(
    "input_path",
    required=True,
    shell_complete=completion.triple_files,
    type=ClickSmartPath(allow_dash=False, readable=True, remote_okay=True),
)
@click.argument("iri", type=click.STRING, required=False, shell_complete=completion.graph_uris)
@click.pass_context
def import_command(  # noqa: PLR0913
    ctx: Context,
    input_path: str,
    replace: bool,
    skip_existing: bool,
    include_import_statements: bool,
    iri: str,
) -> None:
    """Import graph(s) to the store.

    If input is a file, content will be uploaded to the graph identified with the IRI.

    If input is a directory and NO IRI is given, it scans for file-pairs such as
    `xyz.ttl` and `xyz.ttl.graph`, where `xyz.ttl` is the actual triples file and
    `xyz.ttl.graph` contains the graph IRI in the first line: `https://mygraph.de/xyz/`.

    If input is a directory AND a graph IRI is given, it scans for all `*.ttl` files
    in the directory and imports all content to the graph, ignoring the `*.ttl.graph`
    files.

    If the `--replace` flag is set, the data in the graphs will be overwritten,
    if not, it will be added.

    Note: Directories are scanned on the first level only (not recursively).
    """
    app: ApplicationContext = ctx.obj
    if replace and skip_existing:
        raise UsageError(
            "The options --replace and --skip-existing are mutually "
            "exclusive, so please remove one of them."
        )
    # is an array of tuples like this [('path/to/triple.file', 'graph IRI')]
    graphs: list[RdfGraphData]
    if SmartPath(input_path).is_dir():
        validate_input_path(input_path)
        graphs = _process_input_directory(input_path, iri)
        if include_import_statements:
            _validate_graph_imports(graphs)
    elif SmartPath(input_path).is_file():
        if iri is None:
            raise UsageError(
                "Either specify an input file AND a graph IRI or an input directory ONLY."
            )
        graphs = [RdfGraphData(input_path, iri, [])]
    else:
        raise NotImplementedError(
            "Input from special files (socket, FIFO, device file) is not supported."
        )

    existing_graphs = get_graphs_as_dict()
    processed_graphs: set = set()
    count: int = len(graphs)
    current: int = 1
    for _ in graphs:
        triple_file = _.file_path
        graph_iri = _.graph_iri
        app.echo_info(
            f"Import file {current}/{count}: " f"{graph_iri} from {triple_file} ... ", nl=False
        )
        if graph_iri in existing_graphs and skip_existing:
            app.echo_warning("skipped")
            continue
        # prevents re-replacing of graphs in a single run
        _replace = False if graph_iri in processed_graphs else replace
        _buffer, content_type, content_encoding = _get_buffer_and_content_type(triple_file, app)
        response = graph_api.post_streamed(
            graph_iri,
            _buffer,
            replace=_replace,
            content_type=content_type,
            content_encoding=content_encoding,
        )
        request_headers = response.request.headers
        request_headers.pop("Authorization")
        app.echo_debug(f"cmemc request headers: {request_headers}")
        app.echo_debug(f"server response headers: {response.headers}")
        app.echo_success("replaced" if _replace else "added")
        # refresh access conditions in case of dropped AC graph
        if graph_iri == refresh.AUTHORIZATION_GRAPH_URI:
            refresh.get()
            app.echo_debug("Access conditions refreshed.")
        processed_graphs.add(graph_iri)
        current += 1
    # create graph imports
    if include_import_statements:
        _create_graph_imports(ctx, graphs)


@click.command(cls=CmemcCommand, name="delete")
@click.option("-a", "--all", "all_", is_flag=True, help="Delete all writeable graphs.")
@click.option(
    "--include-imports",
    is_flag=True,
    help="Delete selected graph(s) and all writeable graphs which are "
    "imported from these selected graph(s).",
)
@click.option(
    "--include-import-statements", is_flag=True, help="Delete import reference of deleted graphs"
)
@click.argument(
    "iris",
    nargs=-1,
    type=click.STRING,
    shell_complete=completion.writable_graph_uris,
    callback=tuple_to_list,
)
@click.pass_context
def delete_command(
    ctx: Context,
    all_: bool,
    include_imports: bool,
    include_import_statements: bool,
    iris: list[str],
) -> None:
    """Delete graph(s) from the store."""
    app: ApplicationContext = ctx.obj
    graphs = get_graphs_as_dict(writeable=True, readonly=False)
    iris = _check_and_extend_exported_graphs(iris, all_, include_imports, graphs)
    imports_to_be_deleted = []
    count: int = len(iris)
    for current, iri in enumerate(iris, start=1):
        imports_to_be_deleted += graph_imports_list.apply_filters(
            ctx=ctx, filter_=[("to-graph", iri)]
        )

        app.echo_info(f"Drop graph {current}/{count}: {iri} ... ", nl=False)
        graph_api.delete(iri)
        app.echo_success("done")
        # refresh access conditions in case of dropped AC graph
        if iri == refresh.AUTHORIZATION_GRAPH_URI:
            refresh.get()
            app.echo_debug("Access conditions refreshed.")
    if include_import_statements:
        # Locate and invoke the 'delete' subcommand under 'graph imports' command
        imports_cmd = graph.commands["imports"]
        delete_cmd = imports_cmd.commands["delete"]  # type: ignore[attr-defined]
        for _ in imports_to_be_deleted:
            if _["from_graph"] not in iris:
                ctx.invoke(delete_cmd, from_graph=_["from_graph"], to_graph=_["to_graph"])


@click.command(cls=CmemcCommand, name="open")
@click.argument("iri", type=click.STRING, shell_complete=completion.graph_uris)
@click.pass_obj
def open_command(app: ApplicationContext, iri: str) -> None:
    """Open / explore a graph in the browser."""
    explore_uri = get_cmem_base_uri() + "/explore?graph=" + quote(iri)
    click.launch(explore_uri)
    app.echo_debug(explore_uri)


@click.command(cls=CmemcCommand, name="count")
@click.option("-a", "--all", "all_", is_flag=True, help="Count all graphs")
@click.option(
    "-s", "--summarize", is_flag=True, help="Display only a sum of all counted graphs together"
)
@click.argument("iris", nargs=-1, type=click.STRING, shell_complete=completion.graph_uris)
@click.pass_obj
def count_command(
    app: ApplicationContext, all_: bool, summarize: bool, iris: tuple[str, ...]
) -> None:
    """Count triples in graph(s).

    This command lists graphs with their triple count.
    Counts do not include imported graphs.
    """
    if not iris and not all_:
        raise UsageError(
            "Either specify at least one graph IRI " "or use the --all option to count all graphs."
        )
    if all_:
        # in case --all is given,
        # list of graphs is filled with all available graph IRIs
        iris = tuple(iri["iri"] for iri in get_graphs())

    count: int
    overall_sum: int = 0
    for iri in iris:
        count = count_graph(iri)
        overall_sum = overall_sum + count
        if not summarize:
            app.echo_result(f"{count!s} {iri}")
    if summarize:
        app.echo_result(str(overall_sum))


@click.group(cls=CmemcGroup)
def graph() -> CmemcGroup:  # type: ignore[empty-body]
    """List, import, export, delete, count, tree or open graphs.

    Graphs are identified by an IRI.

    Note: The get a list of existing graphs,
    execute the `graph list` command or use tab-completion.
    """


graph.add_command(count_command)
graph.add_command(tree_command)
graph.add_command(list_command)
graph.add_command(export_command)
graph.add_command(delete_command)
graph.add_command(import_command)
graph.add_command(open_command)
graph.add_command(validation_group)
graph.add_command(imports_group)
graph.add_command(insights_group)
