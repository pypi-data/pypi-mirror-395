"""vocabularies commands for cmem command line interface."""

import io
from datetime import datetime, timezone
from re import match
from urllib.parse import urlparse

import click
from click import ClickException
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.dp.proxy import graph as graph_api
from cmem.cmempy.dp.titles import resolve
from cmem.cmempy.queries import SparqlQuery
from cmem.cmempy.vocabularies import (
    get_global_vocabs_cache,
    get_vocabularies,
    install_vocabulary,
    uninstall_vocabulary,
)
from cmem.cmempy.workspace import reload_prefixes, update_global_vocabulary_cache
from rdflib import Graph
from rdflib.plugins.parsers.notation3 import BadSyntax
from six.moves.urllib.parse import quote

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.parameter_types.path import ClickSmartPath

GET_ONTOLOGY_IRI_QUERY = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?iri
WHERE {
    ?iri a owl:Ontology;
}
"""

GET_PREFIX_DECLARATION = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX vann: <http://purl.org/vocab/vann/>
SELECT DISTINCT ?prefix ?namespace
WHERE {{
    <{}> a owl:Ontology;
        vann:preferredNamespacePrefix ?prefix;
        vann:preferredNamespaceUri ?namespace.
}}
"""

INSERT_CATALOG_ENTRY = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX voaf: <http://purl.org/vocommons/voaf#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX vann: <http://purl.org/vocab/vann/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
WITH <https://ns.eccenca.com/example/data/vocabs/>
INSERT {{
    <{iri}> a voaf:Vocabulary ;
        skos:prefLabel "{label}"{language} ;
        rdfs:label "{label}"{language} ;
        dct:description "{description}" ;
        vann:preferredNamespacePrefix "{prefix}" ;
        vann:preferredNamespaceUri "{namespace}" ;
        dct:modified "{date}"^^xsd:date .
}}
WHERE {{}}
"""


def _validate_vocabs_to_process(
    iris: tuple[str], filter_: str, all_flag: bool, replace: bool = False
) -> list[str]:
    """Return a list of vocabulary IRTs which will be processed.

    list is without duplicates, and validated if they exist
    """
    if iris == () and not all_flag:
        raise click.UsageError(
            "Either specify at least one vocabulary IRI "
            "or use the --all option to process over all vocabularies."
        )
    all_vocabs = {_["iri"]: _ for _ in get_vocabularies()}
    if all_flag:
        # in case --all is given, all installable / installed vocabs are processed
        if filter_ == "installed":  # uninstall command
            return [_ for _ in all_vocabs if all_vocabs[_]["installed"]]
        # install command
        if replace:
            return list(all_vocabs)
        return [_ for _ in all_vocabs if not all_vocabs[_]["installed"]]

    vocabs_to_process = list(set(iris))  # avoid double removal / installation
    # test if one of the vocabs does not exist or is already installed / not installed
    for _ in vocabs_to_process:
        # uninstall command
        if filter_ == "installed" and (_ not in all_vocabs or not all_vocabs[_]["installed"]):
            raise click.UsageError(f"Vocabulary {_} not installed.")
        if filter_ == "installable":  # install command
            if _ not in all_vocabs:
                raise click.UsageError(f"Vocabulary {_} does not exist.")
            if all_vocabs[_]["installed"] and not replace:
                raise click.UsageError(f"Vocabulary {_} already installed.")
    return vocabs_to_process


def _validate_namespace(app: ApplicationContext, namespace: tuple[str | None, str | None]) -> None:
    """User input validation for the namespace."""
    prefix, uri = namespace
    if prefix is None or uri is None:
        raise ClickException("No namespace given.")

    if uri[-1] not in ("/", "#"):
        app.echo_warning(
            f"Warning: Namespace IRI '{uri}' does not end in"
            " hash (#) or slash (/). This is most likely not what you want."
        )
    parsed_url = urlparse(uri)
    app.echo_debug(str(parsed_url))
    if parsed_url.scheme not in ("http", "https", "urn"):
        raise ClickException(f"Namespace IRI '{uri}' is not a https(s) URL or an URN.")
    prefix_expression = r"^[a-z][a-z0-9]*$"
    if not match(prefix_expression, prefix):
        raise ClickException(
            "Prefix string does not match this regular" f" expression: {prefix_expression}"
        )


def _insert_catalog_entry(iri: str, prefix: str, namespace: str, label: str, language: str) -> None:
    """Insert a cmem vocabulary catalog entry.

    This executes an INSERT WHERE query to the vocabulary catalog graph in
    order to list the new vocabulary graph as vocab in the catalog.

    Args:
    ----
        iri (str): The IRI of the vocabulary graph.
        prefix (str): The prefix of the vocabulary.
        namespace (str): The namespace IRI of the vocabulary.
        label (str): The title of the vocabulary to add to the entry.
        language (str): Optional language tag of the title.

    Returns:
    -------
        None

    """
    language = "@" + str(language).strip() if "@" + str(language).strip() != "@" else ""

    if not label.startswith(prefix + ":"):
        label = prefix + ": " + label

    query_text = INSERT_CATALOG_ENTRY.format(
        iri=iri,
        prefix=prefix,
        namespace=namespace,
        date=datetime.now(tz=timezone.utc).date(),
        label=label,
        language=language,
        description="vocabulary imported with cmemc",
    )
    query = SparqlQuery(text=query_text, origin="cmemc")
    query.get_results()


def _get_vocabulary_metadata_from_file(
    file: io.BytesIO, namespace_given: bool = False
) -> dict[str, str]:
    """Get potential graph iri and prefix/namespace from a turtle file."""
    metadata = {"iri": "", "prefix": "", "namespace": ""}
    try:
        graph = Graph().parse(file, format="ttl")
    except BadSyntax as error:
        raise ClickException("File {file} could not be parsed as turtle.") from error

    ontology_iris = graph.query(GET_ONTOLOGY_IRI_QUERY)
    if len(ontology_iris) == 0:
        raise ClickException("There is no owl:Ontology resource described " "in the turtle file.")
    if len(ontology_iris) > 1:
        ontology_iris_str = [str(iri[0]) for iri in ontology_iris]  # type: ignore[index]
        raise ClickException(
            "There are more than one owl:Ontology resources described "
            f"in the turtle file: {ontology_iris_str}"
        )
    iri = str(next(iter(ontology_iris))[0])  # type: ignore[index]
    metadata["iri"] = iri
    vann_data = graph.query(GET_PREFIX_DECLARATION.format(iri))
    if not vann_data and not namespace_given:
        raise ClickException(
            "There is no namespace defined "
            f"for the ontology '{iri}'.\n"
            "Please add a prefix and namespace to the sources"
            "or use the --namespace option.\n"
            "Refer to the documentation at "
            "https://vocab.org/vann/ for more information."
        )
    if vann_data and namespace_given:
        raise ClickException(
            "There is already a namespace defined "
            f"in the file for the ontology '{iri}'.\n"
            "You can not use the --namespace option with this file."
        )
    if len(vann_data) > 1:
        raise ClickException(
            "There is more than one vann namespace defined " f"for the ontology: {iri}"
        )
    if not namespace_given:
        namespace = next(iter(vann_data))
        metadata["prefix"] = str(namespace[0])  # type: ignore[index]
        metadata["namespace"] = str(namespace[1])  # type: ignore[index]
    return metadata


def _transform_cache_to_table(cache_category: list[dict], table: list) -> list:
    """Transform a cache category dict to a tabulate table."""
    for item in cache_category:
        uri = item["genericInfo"]["uri"]
        try:
            label = item["genericInfo"]["label"]
        except KeyError:
            label = ""
        row = [uri, "class", label]
        table.append(row)
    return table


@click.command(cls=CmemcCommand, name="open")
@click.argument("iri", type=click.STRING, shell_complete=completion.installed_vocabularies)
@click.pass_obj
def open_command(app: ApplicationContext, iri: str) -> None:
    """Open / explore a vocabulary graph in the browser.

    Vocabularies are identified by their graph IRI.
    Installed vocabularies can be listed with the `vocabulary list` command.
    """
    explore_uri = get_cmem_base_uri() + "/explore?graph=" + quote(iri)
    click.launch(explore_uri)
    app.echo_debug(explore_uri)


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only vocabulary identifier (IRIs) and no labels or other "
    "metadata. This is useful for piping the ids into other cmemc "
    "commands.",
)
@click.option(
    "--filter",
    "filter_",
    type=click.Choice(["all", "installed", "installable"], case_sensitive=True),
    default="installed",
    show_default=True,
    help="Filter list based on status.",
)
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.pass_obj
def list_command(app: ApplicationContext, id_only: bool, filter_: str, raw: bool) -> None:
    """Output a list of vocabularies.

    Vocabularies are graphs (see `graph` command group) which consists
    of class and property descriptions.
    """
    vocabs = get_vocabularies(filter_=filter_)
    if raw:
        app.echo_info_json(vocabs)
    elif id_only:
        for _ in vocabs:
            app.echo_info(_["iri"])
    else:
        table = []
        for _ in vocabs:
            iri = _["iri"]
            try:
                label = _["label"]["title"]
            except (KeyError, TypeError):
                label = _["vocabularyLabel"] if _["vocabularyLabel"] else "[no label given]"
            table.append((iri, label))
        app.echo_info_table(
            table,
            headers=["Vocabulary Graph IRI", "Label"],
            sort_column=1,
            empty_table_message="No installed vocabularies found. "
            "Use the `vocabulary install` command to install vocabulary from the catalog.",
        )


@click.command(cls=CmemcCommand, name="install")
@click.argument(
    "iris", nargs=-1, type=click.STRING, shell_complete=completion.installable_vocabularies
)
@click.option(
    "-a", "--all", "all_", is_flag=True, help="Install all vocabularies from the catalog."
)
@click.option(
    "--replace", is_flag=True, help="Replace (overwrite) existing vocabulary, if present."
)
@click.pass_obj
def install_command(app: ApplicationContext, iris: tuple[str], all_: bool, replace: bool) -> None:
    """Install one or more vocabularies from the catalog.

    Vocabularies are identified by their graph IRI.
    Installable vocabularies can be listed with the
    vocabulary list command.
    """
    vocabs_to_install = _validate_vocabs_to_process(
        iris=iris, filter_="installable", all_flag=all_, replace=replace
    )
    count: int = len(vocabs_to_install)
    for current, vocab in enumerate(vocabs_to_install, start=1):
        app.echo_info(f"Install vocabulary {current}/{count}: {vocab} ... ", nl=False)
        install_vocabulary(vocab)
        app.echo_success("done")


@click.command(cls=CmemcCommand, name="uninstall")
@click.argument(
    "iris", nargs=-1, type=click.STRING, shell_complete=completion.installed_vocabularies
)
@click.option("-a", "--all", "all_", is_flag=True, help="Uninstall all installed vocabularies.")
@click.pass_obj
def uninstall_command(app: ApplicationContext, iris: tuple[str], all_: bool) -> None:
    """Uninstall one or more vocabularies.

    Vocabularies are identified by their graph IRI.
    Already installed vocabularies can be listed with the
    vocabulary list command.
    """
    vocabs_to_uninstall = _validate_vocabs_to_process(iris=iris, filter_="installed", all_flag=all_)
    count: int = len(vocabs_to_uninstall)
    for current, vocab in enumerate(vocabs_to_uninstall, start=1):
        app.echo_info(f"Uninstall vocabulary {current}/{count}: {vocab} ... ", nl=False)
        uninstall_vocabulary(vocab)
        app.echo_success("done")


@click.command(cls=CmemcCommand, name="import")
@click.argument(
    "FILE",
    required=True,
    shell_complete=completion.triple_files,
    type=ClickSmartPath(allow_dash=True, readable=True, remote_okay=True),
)
@click.option(
    "--namespace",
    type=(str, str),
    default=(None, None),
    help="In case the imported vocabulary file does not include a preferred"
    " namespace prefix, you can manually add a namespace prefix"
    " with this option. Example: --namespace ex https://example.org/",
)
@click.option(
    "--replace", is_flag=True, help="Replace (overwrite) existing vocabulary, if present."
)
@click.pass_obj
def import_command(
    app: ApplicationContext, file: str, namespace: tuple[str | None, str | None], replace: bool
) -> None:
    """Import a turtle file as a vocabulary.

    With this command, you can import a local ontology file as a named graph
    and create a corresponding vocabulary catalog entry.

    The uploaded ontology file is analysed locally in order to discover the
    named graph and the prefix declaration. This requires an OWL ontology
    description which correctly uses the `vann:preferredNamespacePrefix` and
    `vann:preferredNamespaceUri` properties.
    """
    _buffer = io.BytesIO()
    with ClickSmartPath.open(file) as file_handle:
        _buffer.write(file_handle.read())
    _buffer.seek(0)

    # fetch metadata
    if namespace != (None, None):
        _validate_namespace(app, namespace)
        meta_data = _get_vocabulary_metadata_from_file(_buffer, True)
        meta_data["prefix"] = namespace[0]  # type: ignore[assignment]
        meta_data["namespace"] = namespace[1]  # type: ignore[assignment]
    else:
        meta_data = _get_vocabulary_metadata_from_file(_buffer, False)
    iri = meta_data["iri"]

    success_message = "done"
    if iri in [_["iri"] for _ in graph_api.get_graphs_list()]:
        if replace:
            success_message = "replaced"
        else:
            raise ClickException(f"Proposed graph {iri} does already exist.")
    app.echo_info(f"Import {file} as vocabulary to {iri} ... ", nl=False)
    # upload graph
    _buffer.seek(0)
    graph_api.post_streamed(iri, _buffer, replace=True)

    # resolve label
    resolved_label_object: dict = resolve([iri], graph=iri)[iri]
    app.echo_debug(str(resolved_label_object))
    label = resolved_label_object.get("title", iri)
    language = resolved_label_object.get("lang", "")

    # insert catalog entry
    _insert_catalog_entry(
        iri=iri,
        prefix=meta_data["prefix"],
        namespace=meta_data["namespace"],
        label=label,
        language=language,
    )
    # reload DI prefix
    reload_prefixes()
    # update cache
    update_global_vocabulary_cache(iri)
    app.echo_success(success_message)


@click.command(cls=CmemcCommand, name="update")
@click.argument(
    "iris", nargs=-1, type=click.STRING, shell_complete=completion.installed_vocabularies
)
@click.option(
    "-a", "--all", "all_", is_flag=True, help="Update cache for all installed vocabularies."
)
@click.pass_obj
def cache_update_command(app: ApplicationContext, iris: tuple[str], all_: bool) -> None:
    """Reload / updates the data integration cache for a vocabulary."""
    vocab_caches_to_update = _validate_vocabs_to_process(
        iris=iris, filter_="installed", all_flag=all_
    )
    count: int = len(vocab_caches_to_update)
    for current, vocab in enumerate(vocab_caches_to_update, start=1):
        app.echo_info(f"Update cache {current}/{count}: {vocab} ... ", nl=False)
        update_global_vocabulary_cache(vocab)
        app.echo_success("done")


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only vocabulary term identifier (IRIs) and no labels or other "
    "metadata. This is useful for piping the ids into other cmemc "
    "commands.",
)
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.pass_obj
def cache_list_command(app: ApplicationContext, id_only: bool, raw: bool) -> None:
    """Output the content of the global vocabulary cache."""
    cache_ = get_global_vocabs_cache()
    if raw:
        app.echo_info_json(cache_)
    elif id_only:
        for vocab in cache_["vocabularies"]:
            for class_ in vocab["classes"]:
                app.echo_info(class_["genericInfo"]["uri"])
            for property_ in vocab["properties"]:
                app.echo_info(property_["genericInfo"]["uri"])
    else:
        table: list[list] = []
        for vocab in cache_["vocabularies"]:
            table = _transform_cache_to_table(vocab["classes"], table)
            table = _transform_cache_to_table(vocab["properties"], table)
        app.echo_info_table(
            table,
            headers=["IRI", "Type", "Label"],
            sort_column=0,
            empty_table_message="No cache entries found. "
            "Use the `vocabulary install` command to install a vocabulary.",
        )


@click.group(cls=CmemcGroup)
def cache() -> CmemcGroup:  # type: ignore[empty-body]
    """List und update the vocabulary cache."""


cache.add_command(cache_update_command)
cache.add_command(cache_list_command)


@click.group(cls=CmemcGroup)
def vocabulary() -> CmemcGroup:  # type: ignore[empty-body]
    """List, (un-)install, import or open vocabs / manage cache."""


vocabulary.add_command(open_command)
vocabulary.add_command(list_command)
vocabulary.add_command(install_command)
vocabulary.add_command(uninstall_command)
vocabulary.add_command(import_command)
vocabulary.add_command(cache)
