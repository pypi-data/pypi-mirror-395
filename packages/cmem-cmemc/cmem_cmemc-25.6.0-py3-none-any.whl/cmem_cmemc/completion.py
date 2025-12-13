"""Utility functions for CLI auto-completion functionality."""

# ruff: noqa: ARG001
import os
import pathlib
from collections import OrderedDict
from contextlib import suppress
from typing import Any

import requests.exceptions
from click import Argument, ClickException, Context
from click.shell_completion import CompletionItem, split_arg_string
from cmem.cmempy.dp.authorization.conditions import (
    fetch_all_acls,
    get_actions,
    get_groups,
    get_users,
)
from cmem.cmempy.dp.proxy.graph import get_graph_import_tree
from cmem.cmempy.health import get_complete_status_info
from cmem.cmempy.keycloak.client import list_open_id_clients
from cmem.cmempy.keycloak.group import list_groups
from cmem.cmempy.keycloak.user import get_user_by_username, list_users, user_groups
from cmem.cmempy.plugins.marshalling import get_marshalling_plugins
from cmem.cmempy.queries import QueryCatalog
from cmem.cmempy.vocabularies import get_vocabularies
from cmem.cmempy.workflow.workflows import get_workflows_io
from cmem.cmempy.workspace import (
    get_task_plugin_description,
    get_task_plugins,
)
from cmem.cmempy.workspace.projects.datasets.dataset import get_dataset
from cmem.cmempy.workspace.projects.project import get_projects
from cmem.cmempy.workspace.projects.resources import get_all_resources, get_resources
from cmem.cmempy.workspace.projects.variables import get_all_variables
from cmem.cmempy.workspace.python import list_packages
from cmem.cmempy.workspace.search import list_items
from natsort import natsorted, ns

from cmem_cmemc.constants import NS_ACL, NS_ACTION, NS_GROUP, NS_USER
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.placeholder import QueryPlaceholder, get_placeholders_for_query
from cmem_cmemc.smart_path import SmartPath as Path
from cmem_cmemc.utils import (
    convert_iri_to_qname,
    get_graphs,
    get_published_packages,
    struct_to_table,
)

NOT_SORTED = -1
SORT_BY_KEY = 0
SORT_BY_DESC = 1


def finalize_completion(
    candidates: list,
    incomplete: str = "",
    sort_by: int = SORT_BY_KEY,
    nat_sort: bool = False,
    reverse: bool = False,
) -> list[CompletionItem]:
    """Sort and filter candidates list.

    candidates are sorted with natsort library by sort_by key.

    Args:
    ----
        candidates (list):  completion dictionary to filter
        incomplete (str):   incomplete string at the cursor
        sort_by (str):      SORT_BY_KEY, SORT_BY_DESC or NOT_SORTED
        nat_sort (bool):    if true, uses the natsort package for sorting
        reverse (bool):     if true, sorts in reverse order

    Returns:
    -------
        filtered and sorted candidates list

    Raises:
    ------
        ClickException in case of wrong sort_by parameter

    """
    if sort_by not in (SORT_BY_KEY, SORT_BY_DESC, NOT_SORTED):
        raise ClickException("sort_by should be -1, 0 or 1.")
    incomplete = incomplete.lower()
    if len(candidates) == 0:
        return candidates
    # remove duplicates (preserving the order)
    candidates = list(OrderedDict.fromkeys(candidates))

    if isinstance(candidates[0], str):
        # list of strings filtering and sorting
        filtered_candidates = [
            element for element in candidates if element.lower().find(incomplete) != -1
        ]
        if sort_by == NOT_SORTED:
            return filtered_candidates
        if nat_sort:
            return natsorted(seq=filtered_candidates, alg=ns.IGNORECASE, reverse=reverse)
        # this solves that case-insensitive sorting is not stable in ordering
        # of "equal" keys (https://stackoverflow.com/a/57923460)
        return sorted(filtered_candidates, key=lambda x: (str(x).casefold(), x), reverse=reverse)

    if isinstance(candidates[0], tuple):
        # list of tuples filtering and sorting
        filtered_candidates = [
            element
            for element in candidates
            if str(element[0]).lower().find(incomplete) != -1
            or str(element[1]).lower().find(incomplete) != -1
        ]
        if sort_by == NOT_SORTED:
            sorted_list = filtered_candidates
        elif nat_sort:
            sorted_list = natsorted(
                seq=filtered_candidates,
                key=lambda k: k[sort_by],
                alg=ns.IGNORECASE,
                reverse=reverse,
            )
        else:
            sorted_list = sorted(
                filtered_candidates,
                key=lambda x: (str(x[sort_by]).casefold(), str(x[sort_by])),
                reverse=reverse,
            )
        return [CompletionItem(value=element[0], help=element[1]) for element in sorted_list]

    raise ClickException(
        "Candidates should be a list of strings or a list of tuples." f" Got {candidates}"
    )


def get_completion_args(incomplete: str) -> list[str]:
    """Get completion args

    This is a workaround to get partial tuple options in a completion function
    see https://github.com/pallets/click/issues/2597
    """
    args = split_arg_string(os.environ.get("COMP_WORDS", ""))
    if incomplete and len(args) > 0 and args[len(args) - 1] == incomplete:
        args.pop()
    return args


def check_option_in_params(option: str, params: Any) -> bool:  # noqa: ANN401
    """Check if the given 'option' is present in the 'params' dictionary or any of its values."""
    if hasattr(params, "__iter__") and option in params:
        return True
    return bool(option == params)


def add_metadata_parameter(list_: list | None = None) -> list:
    """Extend a list with metadata keys and key descriptions."""
    if list_ is None:
        list_ = []
    list_.insert(0, ("description", "Metadata: A description."))
    list_.insert(0, ("label", "Metadata: A name."))
    return list_


def acl_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of access condition identifier"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = []
    acls = fetch_all_acls()
    for access_condition in acls:
        iri = convert_iri_to_qname(access_condition.get("iri"), default_ns=NS_ACL)
        label = access_condition.get("name")
        if check_option_in_params(iri, ctx.params.get(str(param.name))):
            continue
        options.append((iri, label))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def acl_actions(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of access condition actions"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = []
    results = get_actions().json()
    for _ in results:
        try:
            iri = _["iri"]
            name = _["name"]
        except (KeyError, TypeError):
            return []
        qname = convert_iri_to_qname(iri, default_ns=NS_ACTION)
        if check_option_in_params(qname, ctx.params.get(str(param.name))):
            continue
        if check_option_in_params(iri, ctx.params.get(str(param.name))):
            continue
        options.append((qname, name))
    if not check_option_in_params("urn:elds-backend-all-actions", ctx.params.get(str(param.name))):
        options.append(
            ("urn:elds-backend-all-actions", "All Actions (until 24.2.x, now deprecated)")
        )
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def acl_users(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of access condition users"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = []
    try:
        for _ in list_users():
            if check_option_in_params(_["username"], ctx.params.get(str(param.name))):
                continue
            options.append(_["username"])
    except requests.exceptions.HTTPError:
        pass
    results = get_users().json()
    for _ in results:
        username = _.replace(NS_USER, "")
        if check_option_in_params(username, ctx.params.get(str(param.name))) or username in options:
            continue
        options.append(username)

    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def acl_groups(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of access condition groups"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = []
    try:
        for _ in list_groups():
            if check_option_in_params(_["name"], ctx.params.get(str(param.name))):
                continue
            options.append(_["name"])
    except requests.exceptions.HTTPError:
        pass
    results = get_groups().json()
    for _ in results:
        _ = _.replace(NS_GROUP, "") if _.startswith(NS_GROUP) else _
        if check_option_in_params(_, ctx.params.get(str(param.name))) or _ in options:
            continue
        options.append(_)
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def add_read_only_and_uri_property_parameters(list_: list | None = None) -> list:
    """Extend a list with readonly/uriProperty keys and key descriptions."""
    if list_ is None:
        list_ = []
    list_.append(
        (
            "readOnly",
            "Read-only: If enabled, all write operations using this dataset object "
            "will fail, e.g. when used as output in workflows or transform/linking "
            "executions. This will NOT protect the underlying resource in general, "
            "e.g. files, databases or knowledge graphs could still be changed "
            "externally.",
        )
    )
    list_.append(
        (
            "uriProperty",
            "URI attribute: When reading data from the dataset, the specified "
            "attribute will be used to get the URIs of the entities. "
            "When writing to a dataset, the specified attribute will be automatically "
            "added to the schema as well as the generated entity URIs will be added as "
            "values for each entity. If the entered value is not a valid URI, "
            "it will be converted to a valid URI.",
        )
    )
    return list_


def dataset_parameter(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of dataset parameters for a dataset type."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    args = get_completion_args(incomplete)
    incomplete = incomplete.lower()
    # look if cursor is in value position of the -p option and
    # return nothing in case it is (values are not completed atm)
    if args[len(args) - 2] in ("-p", "--parameter"):
        return []
    # try to determine the dataset type
    dataset_type = ctx.params.get("dataset_type")
    if dataset_type is None:
        try:
            dataset_id = ctx.args[0]
            project = get_dataset(
                project_name=dataset_id.split(":")[0], dataset_name=dataset_id.split(":")[1]
            )
            dataset_type = project["data"]["type"]
        except IndexError:
            pass

    # without type, we know nothing
    if dataset_type is None:
        return []
    plugin = get_task_plugin_description(dataset_type)
    properties = plugin["properties"]
    options = []
    for key in properties:
        title = properties[key]["title"]
        description = properties[key]["description"]
        option = f"{title}: {description}"
        options.append((key, option))

    options = add_read_only_and_uri_property_parameters(options)
    # sorting: metadata on top, then parameter per key
    options = sorted(options, key=lambda k: k[0].lower())
    options = add_metadata_parameter(options)
    # restrict to search
    options = [
        key
        for key in options
        if (
            key[0].lower().find(incomplete.lower()) != -1
            or key[1].lower().find(incomplete.lower()) != -1
        )
    ]

    return [CompletionItem(value=option[0], help=option[1]) for option in options]


def dataset_types(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of dataset types."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    incomplete = incomplete.lower()
    options = []
    plugins = get_task_plugins()
    for plugin_id in plugins:
        plugin = plugins[plugin_id]
        title = plugin["title"]
        description = plugin["description"].partition("\n")[0]
        option = f"{title}: {description}"
        if plugin["taskType"] == "Dataset" and (
            plugin_id.lower().find(incomplete.lower()) != -1
            or option.lower().find(incomplete.lower()) != -1
        ):
            options.append((plugin_id, option))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def dataset_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of projectid:datasetid dataset identifier."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    results = list_items(item_type="dataset")
    datasets = results["results"]
    options = [(f"{_['projectId']}:{_['id']}", _["label"]) for _ in datasets]
    return finalize_completion(candidates=options, incomplete=incomplete)


def dataset_list_filter(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of filter names and values for dataset list filter."""
    filter_names = [
        ("project", "Filter by project ID."),
        ("regex", "Filter by regular expression on the dataset label."),
        ("tag", "Filter by tag label."),
        ("type", "Filter by dataset type."),
    ]
    filter_regex = [
        ("^Final:", "Example: Dataset label starts with 'Final:'."),
        (
            r"[12][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]",
            "Example: Dataset label contains a date-like string.",
        ),
    ]
    options = []
    args = get_completion_args(incomplete)
    if args[len(args) - 1] == "--filter":
        options = finalize_completion(candidates=filter_names, incomplete=incomplete)
    if args[len(args) - 1] == "type":
        options = dataset_types(ctx, param, incomplete)
    if args[len(args) - 1] == "project":
        options = project_ids(ctx, param, incomplete)
    if args[len(args) - 1] == "tag":
        options = tag_labels(ctx, param, incomplete, "dataset")
    if args[len(args) - 1] == "regex":
        options = finalize_completion(candidates=filter_regex, incomplete=incomplete)
    return options


def resource_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of projectid:resourceid resource identifier."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = [_["id"] for _ in get_all_resources()]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def scheduler_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of projectid:schedulerid scheduler identifier."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = []
    schedulers = list_items(
        item_type="task",
        facets=[{"facetId": "taskType", "keywordIds": ["Scheduler"], "type": "keyword"}],
    )["results"]
    for _ in schedulers:
        if check_option_in_params(_["projectId"] + ":" + _["id"], ctx.params.get(str(param.name))):
            continue
        options.append((_["projectId"] + ":" + _["id"], _["label"]))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def vocabularies(
    ctx: Context, param: Argument, incomplete: str, filter_: str = "all"
) -> list[CompletionItem]:
    """Prepare a list of vocabulary graphs for auto-completion."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    vocabs = get_vocabularies(filter_=filter_)
    options = []
    for _ in vocabs:
        url = _["iri"]
        if check_option_in_params(url, ctx.params.get(str(param.name))):
            continue
        url = _["iri"]
        try:
            label = _["label"]["title"]
        except (KeyError, TypeError):
            label = "Vocabulary in graph " + url
        options.append((url, label))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def installed_vocabularies(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of installed vocabulary graphs."""
    return vocabularies(ctx, param, incomplete, filter_="installed")


def installable_vocabularies(
    ctx: Context, param: Argument, incomplete: str
) -> list[CompletionItem]:
    """Prepare a list of installable vocabulary graphs."""
    return vocabularies(ctx, param, incomplete, filter_="installable")


def file_list(
    incomplete: str = "", suffix: str = "", description: str = "", prefix: str = ""
) -> list[CompletionItem]:
    """Prepare a list of files with specific parameter."""
    directory = str(pathlib.Path().cwd())
    options = [
        (file_name, description)
        for file_name in os.listdir(directory)
        if (
            Path(file_name).exists() and file_name.endswith(suffix) and file_name.startswith(prefix)
        )
    ]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_KEY)


def workflow_io_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of io workflows."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = []
    for _ in get_workflows_io():
        workflow_id = _["projectId"] + ":" + _["id"]
        label = _["label"]
        options.append((workflow_id, label))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def replay_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of JSON replay files."""
    return file_list(incomplete=incomplete, suffix=".json", description="JSON query replay file")


def installed_package_names(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of installed packages."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = [(_["name"], _["version"]) for _ in list_packages()]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_KEY)


def published_package_names(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """List of plugin packages scraped from pypi.org."""
    options = [(_.name, f"{_.version}: {_.description}") for _ in get_published_packages()]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_KEY)


def python_package_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of acceptable python package files."""
    return file_list(
        incomplete=incomplete,
        suffix=".tar.gz",
        description="Plugin Python Package file",
        prefix="cmem-plugin-",
    )


def installable_packages(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Installable packages from files and pypi.org."""
    return python_package_files(ctx, param, incomplete) + published_package_names(
        ctx, param, incomplete
    )


def workflow_io_output_files(
    ctx: Context, param: Argument, incomplete: str
) -> list[CompletionItem]:
    """Prepare a list of acceptable workflow io output files."""
    return (
        file_list(incomplete=incomplete, suffix=".csv", description="CSV Dataset resource")
        + file_list(incomplete=incomplete, suffix=".xml", description="XML Dataset resource")
        + file_list(incomplete=incomplete, suffix=".json", description="JSON Dataset resource")
        + file_list(incomplete=incomplete, suffix=".xlsx", description="Excel Dataset resource")
        + file_list(incomplete=incomplete, suffix=".ttl", description="RDF file Dataset resource")
        + file_list(incomplete=incomplete, suffix=".nt", description="RDF file Dataset resource")
    )


def workflow_io_input_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of acceptable workflow io input files."""
    files = []
    for extension, info in get_dataset_file_mapping().items():
        # handle zip extension separately.
        if extension != ".zip":
            files += file_list(
                incomplete=incomplete, suffix=extension, description=info["description"]
            )
    return files


def get_dataset_file_mapping() -> dict[str, dict[str, str]]:
    """Return file extension to type and description mapping"""
    return {
        ".csv": {"description": "CSV Dataset resource", "type": "csv"},
        ".csv.zip": {"description": "CSV Dataset resource (zipped)", "type": "csv"},
        ".xls": {"description": "Excel Dataset resource", "type": "excel"},
        ".xlsx": {"description": "Excel Dataset resource", "type": "excel"},
        ".xml": {"description": "XML Dataset resource", "type": "xml"},
        ".xml.zip": {"description": "XML Dataset resource (zipped)", "type": "xml"},
        ".json": {"description": "JSON Dataset resource", "type": "json"},
        ".json.zip": {"description": "JSON Dataset resource (zipped)", "type": "json"},
        ".jsonl": {"description": "JSON Lines Dataset resource", "type": "json"},
        ".jsonl.zip": {"description": "JSON Lines Dataset resource (zipped)", "type": "json"},
        ".yaml": {"description": "YAML Text Document", "type": "text"},
        ".yaml.zip": {"description": "YAML Text Document (zipped)", "type": "text"},
        ".md": {"description": "Markdown Text Document", "type": "text"},
        ".md.zip": {"description": "Markdown Text Document (zipped)", "type": "text"},
        ".yml": {"description": "YAML Text Document", "type": "text"},
        ".yml.zip": {"description": "YAML Text Document (zipped)", "type": "text"},
        ".ttl": {"description": "RDF file Dataset resource", "type": "file"},
        ".orc": {"description": "Apache ORC Dataset resource", "type": "orc"},
        ".txt": {"description": "Text dataset resource", "type": "text"},
        ".txt.zip": {"description": "Text dataset resource (zipped)", "type": "text"},
        ".zip": {"description": "Potential multiCsv Dataset resource", "type": "multiCsv"},
        ".pdf": {"description": "Potential Binary Dataset resource", "type": "binaryFile"},
        ".png": {"description": "Potential Binary Dataset resource", "type": "binaryFile"},
        ".jpg": {"description": "Potential Binary Dataset resource", "type": "binaryFile"},
        ".gif": {"description": "Potential Binary Dataset resource", "type": "binaryFile"},
        ".tiff": {"description": "Potential Binary Dataset resource", "type": "binaryFile"},
    }


def dataset_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of dataset files."""
    files = []
    for extension, info in get_dataset_file_mapping().items():
        # handle zip extension separately.
        if extension != ".zip":
            files += file_list(
                incomplete=incomplete, suffix=extension, description=info["description"]
            )

    multicsv = file_list(
        incomplete=incomplete,
        suffix=".zip",
        description=get_dataset_file_mapping()[".zip"]["description"],
    )

    list_of_file_names = {item.value for item in files}
    filtered_multicsv = [item for item in multicsv if item.value not in list_of_file_names]

    return files + filtered_multicsv


def project_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of workspace files."""
    return file_list(
        incomplete=incomplete,
        suffix=".project.zip",
        description="eccenca Corporate Memory project backup file",
    )


def ini_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of workspace files."""
    return file_list(incomplete=incomplete, suffix=".ini", description="INI file")


def workspace_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of workspace files."""
    return file_list(
        incomplete=incomplete,
        suffix=".workspace.zip",
        description="eccenca Corporate Memory workspace backup file",
    )


def sparql_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of SPARQL files."""
    return file_list(
        incomplete=incomplete, suffix=".sparql", description="SPARQL query file"
    ) + file_list(incomplete=incomplete, suffix=".rq", description="SPARQL query file")


def triple_files(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of triple files."""
    return (
        file_list(incomplete=incomplete, suffix=".ttl", description="Turtle file")
        + file_list(incomplete=incomplete, suffix=".nt", description="NTriples file")
        + file_list(incomplete=incomplete, suffix=".rdf", description="RDF/XML file")
        + file_list(incomplete=incomplete, suffix=".jsonld", description="JSON-LD file")
        + file_list(incomplete=incomplete, suffix=".ttl.gz", description="Turtle file (compressed)")
        + file_list(
            incomplete=incomplete, suffix=".nt.gz", description="NTriples file (compressed)"
        )
        + file_list(
            incomplete=incomplete, suffix=".rdf.gz", description="RDF/XML file (compressed)"
        )
        + file_list(
            incomplete=incomplete, suffix=".jsonld.gz", description="JSON-LD file (compressed)"
        )
    )


def sparql_accept_types(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of commonly used SPARQL accept content types."""
    examples = [
        (
            "text/csv",
            "CSV response, used for SELECT queries, omits language tags and datatypes of literals",
        ),
        ("application/sparql-results+json", "JSON response, used for SELECT queries"),
        ("text/turtle", "Turtle response, used for CONSTRUCT queries"),
        ("application/n-triples", "N-Triples response, used for CONSTRUCT queries"),
    ]
    return finalize_completion(candidates=examples, incomplete=incomplete)


def placeholder(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of placeholder from the to-be executed queries."""
    args = get_completion_args(incomplete)
    # setup configuration
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    catalog_graph = ctx.params.get("catalog_graph")
    # extract placeholder from given queries in the command line
    options = []
    placeholders: dict[str, QueryPlaceholder] = {}
    catalog = QueryCatalog(graph=catalog_graph) if catalog_graph else QueryCatalog()
    for _, arg in enumerate(args):
        query = catalog.get_query(arg)
        if query is not None:
            # collect all placeholder descriptions of existing queries
            placeholders = placeholders | get_placeholders_for_query(iri=query.url)
            # collect all placeholder keys
            options.extend(list(query.get_placeholder_keys()))
    # look if the cursor is in value position of the -p option and
    # use placeholder value completion, in case it is
    if args[len(args) - 2] in ("-p", "--parameter"):
        key = args[len(args) - 1]
        if key in placeholders:
            candidates = placeholders[key].complete(incomplete=incomplete)
            return finalize_completion(
                candidates=candidates, incomplete=incomplete, sort_by=NOT_SORTED
            )
        return []

    # look for already given parameter in the arguments and remove them from
    # the available options
    for num, arg in enumerate(args):
        if num - 1 > 0 and args[num - 1] in ("-p", "--parameter"):
            options.remove(arg)
    return finalize_completion(candidates=options, incomplete=incomplete)


def remote_queries(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of query URIs."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    catalog_graph = ctx.params.get("catalog_graph")
    catalog = QueryCatalog(graph=catalog_graph) if catalog_graph else QueryCatalog()
    options = []
    for query in catalog.get_queries().values():
        url = query.short_url
        label = query.label
        options.append((url, label))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def remote_queries_and_sparql_files(
    ctx: Context, param: Argument, incomplete: str
) -> list[CompletionItem]:
    """Prepare a list of named queries, query files and directories."""
    remote = remote_queries(ctx, param, incomplete)
    files = sparql_files(ctx, param, incomplete)
    return remote + files


def workflow_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of projectid:taskid workflow identifier."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    workflows = list_items(item_type="workflow")["results"]
    options = []
    for _ in workflows:
        workflow = _["projectId"] + ":" + _["id"]
        label = _["label"]
        if check_option_in_params(workflow, ctx.params.get(str(param.name))):
            continue
        options.append((workflow, label))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def marshalling_plugins(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of supported workspace/project import/export plugins."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = get_marshalling_plugins()
    if "description" in options[0]:
        final_options = [(_["id"], _["description"]) for _ in options]
    else:
        # in case, no descriptions are available, labels are fine as well
        final_options = [(_["id"], _["label"]) for _ in options]

    return finalize_completion(
        candidates=final_options, incomplete=incomplete, sort_by=SORT_BY_DESC
    )


def project_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of project IDs for auto-completion."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    projects = get_projects()
    options = []
    for _ in projects:
        project_id = _["name"]
        label = _["metaData"].get("label", "")
        # do not add project if already in the command line
        if check_option_in_params(project_id, ctx.params.get(str(param.name))):
            continue
        options.append((project_id, label))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def _prepare_graph_options(
    ctx: Context,
    param: Argument,
    writeable: bool = True,
    readonly: bool = True,
    skip_selected_iris: bool = True,
) -> list[tuple[str, str]]:
    """Prepare a list of graphs with iri and label"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    graphs = get_graphs(writeable=writeable, readonly=readonly)
    options = []
    for graph in graphs:
        iri = graph["iri"]
        label = graph["label"]["title"]
        # do not add graph if already in the command line
        if skip_selected_iris & check_option_in_params(iri, ctx.params.get(str(param.name))):
            continue
        options.append((iri, label))
    return options


def graph_uris_skip_check(
    ctx: Context, param: Argument, incomplete: str, writeable: bool = True, readonly: bool = True
) -> list[CompletionItem]:
    """Prepare a list of graphs for auto-completion without checking selected IRIs"""
    options = _prepare_graph_options(
        ctx, param, writeable=writeable, readonly=readonly, skip_selected_iris=False
    )
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def graph_uris(
    ctx: Context, param: Argument, incomplete: str, writeable: bool = True, readonly: bool = True
) -> list[CompletionItem]:
    """Prepare a list of graphs for auto-completion."""
    options = _prepare_graph_options(ctx, param, writeable=writeable, readonly=readonly)
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def ignore_graph_uris(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of import graphs for auto-completion."""
    data_graph = ctx.args[0]
    import_tree = get_graph_import_tree(data_graph)
    imported_graphs = {iri for values in import_tree["tree"].values() for iri in values}
    options = _prepare_graph_options(ctx, param, writeable=True, readonly=True)
    options = [_ for _ in options if _[0] in imported_graphs]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def writable_graph_uris(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of writable graphs for auto-completion."""
    return graph_uris(ctx, param, incomplete, writeable=True, readonly=False)


def graph_uris_with_all_graph_uri(
    ctx: Context, param: Argument, incomplete: str
) -> list[CompletionItem]:
    """Prepare a list of all graphs for acl command auto-completion."""
    options = graph_uris(ctx, param, incomplete, writeable=True, readonly=True)
    options.append(
        CompletionItem(
            value=r"urn:elds-backend-all-graphs", help="All Graphs (until 24.2.x, now deprecated)"
        )
    )
    options.append(
        CompletionItem(value=r"https://vocab.eccenca.com/auth/AllGraphs", help="All Graphs")
    )
    return options


def connections(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of config connections for auto-completion."""
    # since ctx does not have an obj here, we re-create the object
    app = ApplicationContext.from_params(ctx.find_root().params)
    options = app.get_config().sections()
    return finalize_completion(candidates=options, incomplete=incomplete)


def graph_export_templates(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of example templates for the graph export command."""
    examples = [
        ("{{hash}}", "Example: 6568a[...]00b08.ttl"),
        ("{{iriname}}", "Example: https__ns_eccenca_com_data_config.ttl"),
        ("{{date}}-{{iriname}}", "Example: 2021-11-29-https__ns_eccenca_com_data_config.ttl"),
        (
            "{{date}}-{{connection}}-{{iriname}}",
            "Example: 2021-11-29-mycmem-https__ns_eccenca_com_data_config.ttl",
        ),
    ]
    return finalize_completion(candidates=examples, incomplete=incomplete)


def project_export_templates(
    ctx: Context, param: Argument, incomplete: str
) -> list[CompletionItem]:
    """Prepare a list of example templates for the project export command."""
    examples = [
        ("{{id}}.project", "Example: Plain file name"),
        ("{{date}}-{{connection}}-{{id}}.project", "Example: More descriptive file name"),
        ("dumps/{{connection}}/{{id}}/{{date}}.project", "Example: Whole directory tree"),
    ]
    return finalize_completion(candidates=examples, incomplete=incomplete)


def workspace_export_templates(
    ctx: Context, param: Argument, incomplete: str
) -> list[CompletionItem]:
    """Prepare a list of example templates for the workspace export command."""
    examples = [
        ("workspace", "Example: a plain file name"),
        ("{{date}}-{{connection}}.workspace", "Example: a more descriptive file name"),
        ("dumps/{{connection}}/{{date}}.workspace", "Example: a whole directory tree"),
    ]
    return finalize_completion(candidates=examples, incomplete=incomplete)


def graph_list_filter(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of filter names and values for graph list filter."""
    filter_names = [
        (
            "access",
            "List only graphs which have a certain access condition " "(readonly or writeable).",
        ),
        ("imported-by", "List only graphs which are in the import tree of a " "specified graph."),
    ]
    filter_values_access = [
        ("readonly", "List only graphs which are NOT writable for the current user."),
        ("writeable", "List only graphs which ARE writeable for the current user."),
    ]
    args = get_completion_args(incomplete)
    options = []
    if args[len(args) - 1] == "--filter":
        options = finalize_completion(candidates=filter_names, incomplete=incomplete)
    if args[len(args) - 1] == "access":
        options = finalize_completion(candidates=filter_values_access, incomplete=incomplete)
    if args[len(args) - 1] == "imported-by":
        options = graph_uris(ctx, param, incomplete)
    return options


def variable_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of variables IDs for auto-completion."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    variables = get_all_variables()
    options = []
    for _ in variables:
        variable_id = _["id"]
        label = _.get("description", "").partition("\n")[0]
        if label == "":
            label = f"Current value: {_['value']}"
        # do not add project if already in the command line
        if check_option_in_params(variable_id, ctx.params.get(str(param.name))):
            continue
        options.append((variable_id, label))
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_KEY)


def variable_list_filter(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of filter names and values for variable list filter."""
    filter_names = [
        ("project", "Filter for variables from a specific project."),
        (
            "regex",
            "Filter for variables with a regular expression search over "
            "id, value and description.",
        ),
    ]
    filter_values_regex = [
        ("ending$", "Variables name ends with 'ending'."),
        ("^starting", "Variables name starts with 'starting'."),
    ]
    args = get_completion_args(incomplete)
    if args[len(args) - 1] == "--filter":
        return [CompletionItem(value=f[0], help=f[1]) for f in filter_names]
    if args[len(args) - 1] == "regex":
        return finalize_completion(candidates=filter_values_regex, incomplete=incomplete)
    if args[len(args) - 1] == "project":
        return project_ids(ctx, param, incomplete)
    return []


def resource_list_filter(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of filter names and values for resource list filter."""
    filter_names = [
        ("project", "Filter for file resources from a specific project."),
        (
            "regex",
            "Filter for file resources with a regular expression search on " "the name field.",
        ),
    ]
    filter_values_regex = [
        ("csv$", "File resources which name ends with .csv"),
        ("2021-10-[0-9][0-9]", "File resources which name has a date from 2021-10 in it"),
    ]
    args = get_completion_args(incomplete)
    if args[len(args) - 1] == "--filter":
        return [CompletionItem(value=f[0], help=f[1]) for f in filter_names]
    if args[len(args) - 1] == "project":
        return project_ids(ctx, param, incomplete)
    if args[len(args) - 1] == "regex":
        return finalize_completion(candidates=filter_values_regex, incomplete=incomplete)
    return []


def workflow_list_filter(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of filter names and values for workflow list filter."""
    filter_names = [
        ("project", "Filter by project ID."),
        ("io", "Filter by workflow io feature."),
        ("regex", "Filter by regular expression on the workflow label."),
        ("tag", "Filter by tag label."),
    ]
    filter_values_io = [
        ("any", "List all workflows suitable for the io command."),
        ("input-only", "List only workflows with a variable input dataset."),
        ("output-only", "List only workflows with a variable output dataset."),
        ("input-output", "List only workflows with a variable input and output dataset."),
    ]
    filter_regex = [
        (r"^Final:", "Example: Workflow label starts with 'Final:'."),
        (
            r"[12][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]",
            "Example: Workflow label contains a data-like string.",
        ),
    ]
    options = []
    args = get_completion_args(incomplete)
    if args[len(args) - 1] == "--filter":
        options = filter_names
    if args[len(args) - 1] == "io":
        options = filter_values_io
    if args[len(args) - 1] == "project":
        return project_ids(ctx, param, incomplete)
    if args[len(args) - 1] == "tag":
        return tag_labels(ctx, param, incomplete, "workflow")
    if args[len(args) - 1] == "regex":
        options = filter_regex

    return finalize_completion(candidates=options, incomplete=incomplete)


def tag_labels(
    ctx: Context, param: Argument, incomplete: str, item_type: str
) -> list[CompletionItem]:
    """Prepare a list of tag labels for a item_type."""
    datasets = list_items(item_type=item_type)
    options = []
    counts: dict[str, int] = {}
    for _dataset in datasets["results"]:
        for _tag in _dataset["tags"]:
            if _tag["label"] in counts:
                counts[_tag["label"]] += 1
            else:
                counts[_tag["label"]] = 1
    for tag, count in counts.items():
        options.append((tag, f"{count} item(s): {tag}"))
    return finalize_completion(
        candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC, reverse=True
    )


def status_keys(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of status keys for the admin status command."""
    os.environ["CMEMPY_IS_CHATTY"] = "false"
    status_info = struct_to_table(get_complete_status_info())
    options = [_[0] for _ in status_info]
    options.insert(0, "all")
    return finalize_completion(candidates=options, incomplete=incomplete)


def user_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of username for admin update/delete/password command."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = [_["username"] for _ in list_users()]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def user_group_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of group name for admin user update --(un)assign-group parameter"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    if not ctx.args:
        return []
    users = get_user_by_username(username=str(ctx.args[0]))
    if not users:
        return []

    if param.name == "unassign_group":
        groups = user_groups(user_id=users[0]["id"])
    else:
        user_group_names = [group["name"] for group in user_groups(user_id=users[0]["id"])]
        groups = [group for group in list_groups() if group["name"] not in user_group_names]
    options = [_["name"] for _ in groups]

    for arg in ctx.params["assign_group"]:
        with suppress(ValueError):
            options.remove(arg)
    for arg in ctx.params["unassign_group"]:
        with suppress(ValueError):
            options.remove(arg)

    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def client_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of client ids for admin secret and update command."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = [_["clientId"] for _ in list_open_id_clients()]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def transformation_task_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of projectId:transformation task identifier."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    results = list_items(item_type="transform")
    datasets = results["results"]
    options = [(f"{_['projectId']}:{_['id']}", _["label"]) for _ in datasets]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)


def resource_paths(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of file resource paths within a project.

    Returns the full path of file resources (not including the project ID prefix).
    If a project_id is available in context, lists resources from that project.
    If only one project exists, automatically uses that project.
    """
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    project_id = ctx.params.get("project_id")
    if not project_id:
        projects = get_projects()
        if len(projects) == 1:
            project_id = projects[0]["name"]
    if project_id is None:
        return []
    options = [_["fullPath"] for _ in list(get_resources(project_id))]
    return finalize_completion(candidates=options, incomplete=incomplete, sort_by=SORT_BY_DESC)
