"""Utility functions for CLI interface."""

import json
import os
import pathlib
import re
import sys
import unicodedata
from dataclasses import dataclass
from importlib.metadata import version as cmemc_version
from typing import TYPE_CHECKING
from zipfile import BadZipFile, ZipFile

import requests
from click import Argument, ClickException
from cmem.cmempy.dp.proxy.graph import get_graphs_list
from cmem.cmempy.queries import QueryCatalog
from cmem.cmempy.workspace.projects.project import get_projects
from prometheus_client import Metric

from cmem_cmemc.config_parser import PureSectionConfigParser
from cmem_cmemc.constants import NAMESPACES
from cmem_cmemc.smart_path import SmartPath

if TYPE_CHECKING:
    from cmem_cmemc.context import ApplicationContext


def get_version() -> str:
    """Get the current version or SNAPSHOT."""
    return cmemc_version("cmem-cmemc")


def check_python_version(ctx: type["ApplicationContext"]) -> None:
    """Check the runtime python version and warn or error."""
    version = sys.version_info
    major_expected = [3]
    minor_expected = [13]
    if version.major not in major_expected:
        ctx.echo_error(f"Error: cmemc can not be executed with Python {version.major}.")
        sys.exit(1)
    if version.minor not in minor_expected and not ctx.is_completing():
        ctx.echo_warning(
            "Warning: You are running cmemc under a non-tested python "
            f"environment ({version.major}.{version.minor})."
        )


def extract_error_message(error: Exception, ignore_error_prefix: bool = False) -> str:
    """Extract a message from an exception."""
    # exceptions with response is HTTPError
    message = type(error).__name__ + ": " + str(error) + "\n"
    if ignore_error_prefix:
        message = str(error) + "\n"

    try:
        # try to load Problem Details for HTTP API JSON
        details = json.loads(error.response.text)  # type: ignore[attr-defined]
        message += type(error).__name__ + ": "
        if "title" in details:
            message += details["title"] + ": "
        if "detail" in details:
            message += details["detail"]
    except (AttributeError, ValueError):
        # is not json or any other issue, output plain response text
        pass
    return message.strip()


def iri_to_qname(iri: str) -> str:
    """Return a qname for an IRI based on well known namespaces.

    In case of no matching namespace, the full IRI is returned.

    Args:
    ----
        iri: the IRI to transform

    Returns: string

    """
    for prefix, namespace in NAMESPACES.items():
        iri = iri.replace(namespace, prefix + ":")
    return iri


@dataclass
class RdfGraphData:
    """Represents the data structure for RDF graph information.

    Attributes:
        file_path: The absolute path to the RDF data file.
        graph_iri: The iri of the graph.
        graph_imports: A list of graph imports.

    """

    file_path: str
    graph_iri: str
    graph_imports: list[str]


def read_rdf_graph_files(directory_path: str) -> list[RdfGraphData]:
    """Read all files from directory_path and output as RdfGraphData."""
    rdf_graphs: list[RdfGraphData] = []
    for root, _, files in os.walk(directory_path):
        for _file in files:
            if _file.endswith((".graph", ".imports")):
                continue
            file_path = SmartPath(root) / _file
            # Handle compressed files (like .gz)
            if _file.endswith(".gz"):
                _graph_file = _file.replace(".gz", ".graph")
                _graph_imports_file = _file.replace(".gz", ".imports")
            else:
                _graph_file = f"{_file}.graph"
                _graph_imports_file = f"{_file}.imports"
            graph_file_path = SmartPath(root) / _graph_file
            imports_file_path = SmartPath(root) / _graph_imports_file
            graph_name = ""
            graph_imports = []
            if graph_file_path.exists():
                graph_name = read_file_to_string(str(graph_file_path)).strip()

            if imports_file_path.exists():
                # Read the graph imports.
                imports_content = read_file_to_string(str(imports_file_path)).strip()
                graph_imports = imports_content.split("\n") if imports_content else []

            if graph_name:
                rdf_graphs.append(
                    RdfGraphData(
                        file_path=str(file_path.resolve()),
                        graph_iri=graph_name,
                        graph_imports=graph_imports,
                    )
                )
    return rdf_graphs


def read_file_to_string(file_path: str) -> str:
    """Read file to string."""
    with SmartPath(file_path).open(mode="rb") as _file:
        return str(_file.read().decode("utf-8"))


def get_graphs(writeable: bool = True, readonly: bool = True) -> list:
    """Retrieve list of accessible graphs from DP endpoint.

    readonly=True|writeable=True outputs all graphs
    readonly=False|writeable=True outputs only writeable graphs
    readonly=True|writeable=False outputs graphs without write access
    (but read access)
    """
    all_graphs = get_graphs_list()
    filtered_graphs = []
    for graph in all_graphs:
        if graph["writeable"] and writeable:
            filtered_graphs.append(graph)
        if not graph["writeable"] and readonly:
            filtered_graphs.append(graph)
    return filtered_graphs


def get_graphs_as_dict(writeable: bool = True, readonly: bool = True) -> dict:
    """Get the graph response as dict with IRI as main key."""
    graph_dict = {}
    for graph in get_graphs(writeable=writeable, readonly=readonly):
        graph_dict[graph["iri"]] = graph
    return graph_dict


def convert_uri_to_filename(value: str, allow_unicode: bool = False) -> str:
    """Convert URI to unix friendly filename.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert / to underscore. Convert to lowercase.
    Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\.", "_", value.lower())
    value = re.sub(r"/", "_", value.lower())
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def struct_to_table(
    source: str | bool | float | list | dict, table: list | None = None, prefix: str = ""
) -> list:
    """Prepare flat key/value table from a deep structure.

    This function takes structure and creates a flat table out of it,
    key by key, value by value. For each level deeper it prefixes the
    father keys.

    Example input:  {'k1': '1', 'k2': {'k3': '3', 'k4': '4'}}
    Example output: [['k1', '1'], ['k2:k3', '3'], ['k2:k4', '4']]

    Args:
    ----
        source (any): The structure which is transformed into a flat table.
        table (list): The table where the key/value rows will be appended.
        prefix (str): A prefix which is used to indicate the level.

    Returns:
    -------
        The input table extended with rows from the input source.

    """
    if table is None:
        table = []
    if type(source) in (str, bool, int, float):
        table.append([prefix, source])
        return table
    if isinstance(source, dict):
        if len(prefix) != 0:
            prefix = prefix + "."
        for key in source:
            table = struct_to_table(source[key], table, prefix + key)
        return table
    if isinstance(source, list):
        for value in source:
            table = struct_to_table(value, table, prefix)
        return table
    return table


def split_task_id(task_id: str) -> tuple[str, str]:
    """Validate and split cmemc task ID.

    Args:
    ----
        task_id (str): The task ID in the workspace.

    Raises:
    ------
        ClickException: in case the task ID is not splittable

    """
    try:
        project_part = task_id.split(":")[0]
        task_part = task_id.split(":")[1]
    except IndexError as error:
        raise ClickException(f"{task_id} is not a valid task ID.") from error
    return project_part, task_part


def metric_get_labels(family: Metric, clean: bool = True) -> dict[str, list[str]]:
    """Get the labels of a metric family.

    clean: remove keys with only one dimension
    family: the metric family

    Returns: labels as dict
    """
    labels: dict[str, list[str]] = {}
    # build tree structure
    for sample in family.samples:
        for label in sample.labels:
            value = sample.labels[label]
            if label not in labels:
                labels[label] = []
            if value not in labels[label]:
                labels[label].append(value)
    if clean:
        labels = dict(filter(lambda elem: len(elem[1]) > 1, labels.items()))
    return labels


def check_or_select_project(app: "ApplicationContext", project_id: str | None = None) -> str:
    """Check for given project, select the first one if there is only one.

    Args:
    ----
        app (ApplicationContext): the click cli app context.
        project_id (str): The project ID.

    Raises:
    ------
        ClickException: if no projects available.
        ClickException: if more than one project is.

    Returns:
    -------
        Maybe project_id if there was no project_id before.

    """
    if project_id is not None:
        return project_id

    projects = get_projects()
    if len(projects) == 1:
        project_name = str(projects[0]["name"])
        app.echo_warning(
            "Missing project (--project) - since there is only one project, "
            f"this is selected: {project_name}"
        )
        return project_name

    if len(projects) == 0:
        raise ClickException(
            "There are no projects available. "
            "Please create a project with 'cmemc project create'."
        )

    # more than one project
    raise ClickException(
        "There is more than one project available so you need to "
        "specify the project with '--project'."
    )


@dataclass
class PublishedPackage:
    """Represents a published package from pypi.org."""

    name: str
    description: str
    published: str
    version: str


def get_published_packages() -> list[PublishedPackage]:
    """Get a scraped list of plugin packages scraped from pypi.org."""
    url = "https://download.eccenca.com/cmem-plugin-index/cmem-plugin-index.json"
    package_names = []
    packages = []
    for _ in requests.get(url, timeout=5).json():
        name = _["name"]
        if name == "cmem-plugin-base":
            continue
        if not name.startswith("cmem-plugin-"):
            continue
        if name not in package_names:
            package_names.append(name)
            packages.append(
                PublishedPackage(
                    name=name,
                    description=_["summary"],
                    published=_["latest_version_time"],
                    version=_["latest_version"],
                )
            )
    return packages


def convert_iri_to_qname(iri: str, default_ns: str) -> str:
    """Convert IRI to a QName based on the default namespace.

    If the IRI does not match the default namespace, the method returns the full IRI.
    """
    if iri.startswith(default_ns):
        return iri.replace(default_ns, ":")
    return iri


def convert_qname_to_iri(qname: str, default_ns: str) -> str:
    """Convert a QName to an IRI based on the default namespace.

    If the QName does not match the default namespace, the method returns the full IRI.
    """
    if qname.startswith(":"):
        return default_ns + qname[1:]

    return qname


def get_query_text(file_or_uri: str, required_projections: set) -> str:
    """Get query text for a file or graph catalog URI.

    Args:
    ----
        file_or_uri (str): The file path or URI to fetch the query from.
        required_projections (set): A set of required projections.

    Returns:
    -------
        str: The query text.

    Raises:
    ------
        ClickException: If the input is not a readable file or a query URI,
                    or if the query contains placeholders,
                    or if the query does not include the required projections.

    """
    sparql_query = QueryCatalog().get_query(file_or_uri)
    if sparql_query is None:
        raise ClickException(f"{file_or_uri} is neither a readable file nor a query URI.")

    if sparql_query.get_placeholder_keys():
        raise ClickException("Placeholder queries are not supported.")

    result = sparql_query.get_json_results()
    projected_vars = set(result["head"]["vars"])

    missing_projections = required_projections - projected_vars
    if missing_projections:
        missing = ", ".join(missing_projections)
        raise ClickException(f"Select query must include projections for: {missing}")
    txt: str = sparql_query.text
    return txt


def validate_zipfile(zipfile: str | pathlib.Path) -> bool:
    """Validate a zipfile."""
    zipfile = pathlib.Path(zipfile)
    try:
        ZipFile(zipfile).testzip()
    except BadZipFile:
        return False
    return True


def str_to_bool(value: str | bool) -> bool:
    """Convert common string representations of boolean values to True/False."""
    if isinstance(value, bool):  # If it's already a boolean, return it directly
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "on"}


def is_enabled(params: dict[str, str], config: PureSectionConfigParser, key: str) -> bool:
    """Check if a parameter is enabled."""
    # Check in params dictionary (highest priority)
    if key in params and str_to_bool(params[key]):
        return True
    key = f"CMEMC_{key.upper()}"
    section = params.get("connection")
    defaults = config.defaults()
    if section is None:
        section = defaults.get("CMEMC_CONNECTION")

    # Check in the specified section
    if section and section in config and key in config[section]:
        return str_to_bool(config[section][key])

    # Check in the default section
    if key in defaults:
        return str_to_bool(config.defaults()[key])

    return False


def tuple_to_list(ctx: type["ApplicationContext"], param: Argument, value: tuple) -> list:  # noqa: ARG001
    """Get a list from a tuple

    Used as callback to have mutable values
    """
    return list(value)
