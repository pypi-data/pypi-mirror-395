"""Graph imports command"""

import os

import click
from click import Argument, ClickException, Context, UsageError
from click.shell_completion import CompletionItem
from cmem.cmempy.dp.proxy.graph import get_graph_import_tree
from cmem.cmempy.queries import SparqlQuery
from treelib import Tree

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.constants import UNKNOWN_GRAPH_ERROR
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.object_list import DirectValuePropertyFilter, ObjectList
from cmem_cmemc.string_processor import GraphLink
from cmem_cmemc.title_helper import TitleHelper
from cmem_cmemc.utils import get_graphs_as_dict, tuple_to_list

GRAPH_IMPORTS_LIST_SPARQL = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?from_graph ?to_graph
WHERE
{
  GRAPH ?from_graph {
    ?from_graph owl:imports ?to_graph
  }
}
"""

GRAPH_IMPORTS_CREATE_SPARQL = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>

INSERT DATA {
  GRAPH <{{from_graph}}> {
    <{{from_graph}}> owl:imports <{{to_graph}}> .
  }
}
"""

GRAPH_IMPORTS_DELETE_SPARQL = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>

DELETE DATA {
  GRAPH <{{from_graph}}> {
    <{{from_graph}}> owl:imports <{{to_graph}}> .
  }
}
"""


def _prepare_tree_output_id_only(iris: list[str], graphs: dict) -> str:
    """Prepare a sorted, de-duplicated IRI list of graph imports."""
    output_iris = []
    for iri in iris:
        # get response for one requested graph
        api_response = get_graph_import_tree(iri)

        # add all imported IRIs to the IRI list
        # add the requested graph as well
        output_iris.append(iri)
        for top_graph in api_response["tree"]:
            output_iris.append(top_graph)
            for sub_graph in api_response["tree"][top_graph]:
                output_iris.append(sub_graph)  # noqa: PERF402

    # prepare a sorted, de-duplicated IRI list of existing graphs
    # and create a line-by-line output of it
    output_iris = sorted(set(output_iris), key=lambda x: x.lower())
    filtered_iris = [iri for iri in output_iris if iri in graphs]
    return "\n".join(filtered_iris[0:]) + "\n"


def _create_node_label(iri: str, graphs: dict) -> str:
    """Create a label for a node in the tree."""
    if iri not in graphs:
        return "[missing: " + iri + "]"
    title = graphs[iri]["label"]["title"]
    return f"{title} -- {iri}"


def _add_tree_nodes_recursive(tree: Tree, structure: dict, iri: str, graphs: dict) -> Tree:
    """Add all child nodes of iri from structure to tree.

    Call recursively until no child node can be used as parent anymore.

    Args:
    ----
        tree: the graph where to add the nodes
        structure: the result dict of get_graph_import_tree()
        iri: The IRI of the parent
        graphs: the result of get_graphs()

    Returns:
    -------
        the new treelib.Tree object with the additional nodes

    """
    if not tree.contains(iri):
        tree.create_node(tag=_create_node_label(iri, graphs), identifier=iri)
    if iri not in structure:
        return tree
    for child in structure[iri]:
        tree.create_node(tag=_create_node_label(child, graphs), identifier=child, parent=iri)
    for child in structure[iri]:
        if child in structure:
            tree = _add_tree_nodes_recursive(tree, structure, child, graphs)
    return tree


def _add_ignored_nodes(tree: Tree, structure: dict) -> Tree:
    """Add all child nodes as ignored nodes.

    Args:
    ----
        tree: the graph where to add the nodes
        structure: the result dict of get_graph_import_tree()

    Returns:
    -------
        the new treelib.Tree object with the additional nodes

    """
    if len(structure.keys()) > 0:
        for parent in structure:
            for children in structure[parent]:
                tree.create_node(tag="[ignored: " + children + "]", parent=parent)
    return tree


def get_imports_list(ctx: click.Context) -> list[dict[str, str]]:  # noqa: ARG001
    """Get the import list"""
    list_query = SparqlQuery(text=GRAPH_IMPORTS_LIST_SPARQL)
    result = list_query.get_json_results()
    return [
        {"from_graph": _["from_graph"]["value"], "to_graph": _["to_graph"]["value"]}
        for _ in result["results"]["bindings"]
    ]


@click.command(cls=CmemcCommand, name="tree")
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
@click.pass_obj
def tree_command(
    app: ApplicationContext, all_: bool, raw: bool, id_only: bool, iris: list[str]
) -> None:
    """Show graph tree(s) of the imports statement hierarchy.

    You can output one or more trees of the import hierarchy.

    Imported graphs which do not exist are shown as `[missing: IRI]`.
    Imported graphs which will result in an import cycle are shown as
    `[ignored: IRI]`.
    Each graph is shown with label and IRI.
    """
    graphs = get_graphs_as_dict()
    if not iris and not all_:
        raise UsageError(
            "Either specify at least one graph IRI or use the "
            "--all option to show the owl:imports tree of all graphs."
        )
    if all_:
        iris = [str(_) for _ in graphs]

    for iri in iris:
        if iri not in graphs:
            raise ClickException(UNKNOWN_GRAPH_ERROR.format(iri))

    iris = sorted(iris, key=lambda x: graphs[x]["label"]["title"].lower())

    if raw:
        for iri in iris:
            # direct output of the response for one requested graph
            app.echo_info_json(get_graph_import_tree(iri))
        return

    if id_only:
        app.echo_result(_prepare_tree_output_id_only(iris, graphs), nl=False)
        return

    # normal execution
    output = ""
    for iri in iris:
        # get response for on requested graph
        api_response = get_graph_import_tree(iri)

        tree = _add_tree_nodes_recursive(Tree(), api_response["tree"], iri, graphs)
        tree = _add_ignored_nodes(tree, api_response["ignored"])

        # strip empty lines from the tree.show output
        output += os.linesep.join(
            [
                line
                for line in tree.show(key=lambda x: x.tag.lower(), stdout=False).splitlines()  # type: ignore[arg-type, return-value]
                if line.strip()
            ]
        )
        output += "\n"
    # result output
    app.echo_result(output, nl=False)


graph_imports_list = ObjectList(
    name="imports",
    get_objects=get_imports_list,
    filters=[
        DirectValuePropertyFilter(
            name="from-graph",
            description="List only matches from graph",
            property_key="from_graph",
            title_helper=TitleHelper(),
        ),
        DirectValuePropertyFilter(
            name="to-graph",
            description="List only matches to graph",
            property_key="to_graph",
            title_helper=TitleHelper(),
        ),
    ],
)


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON response.")
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    help=graph_imports_list.get_filter_help_text(),
    shell_complete=graph_imports_list.complete_values,
)
@click.pass_context
def list_command(ctx: Context, raw: bool, filter_: tuple[str, str]) -> None:
    """List accessible graph imports statements.

    Graphs are identified by an IRI. Statement imports are managed by
    creating owl:imports statements such as "FROM_GRAPH owl:imports TO_GRAPH"
    in the FROM_GRAPH. All statements in the TO_GRAPH are then available
    in the FROM_GRAPH.
    """
    app: ApplicationContext = ctx.obj
    filters_to_apply = []
    if filter_:
        filters_to_apply.append(filter_)
    imports = graph_imports_list.apply_filters(ctx=ctx, filter_=filters_to_apply)

    if raw:
        app.echo_info_json(imports)
        return

    table = []
    graphs = get_graphs_as_dict()
    for _ in imports:
        from_graph = _["from_graph"]
        to_graph = _["to_graph"]
        if to_graph not in graphs:
            to_graph = rf"\[missing: {to_graph}]"
        table.append([from_graph, to_graph])

    app.echo_info_table(
        table,
        headers=["From graph", "To graph"],
        sort_column=0,
        cell_processing={0: GraphLink(), 1: GraphLink()},
        empty_table_message="No imports found. "
        "You can use the `graph imports create` command to create a graph import.",
    )


def _validate_graphs(from_graph: str | None, to_graph: str | None) -> None:
    graphs = get_graphs_as_dict(writeable=True, readonly=True)
    if from_graph and from_graph not in graphs:
        raise click.UsageError(f"From graph {from_graph} not found.")

    if to_graph and to_graph not in graphs:
        raise click.UsageError(f"To graph {to_graph} not found.")


def _from_graph_uris(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Provide auto completion items for delete command from-graph argument"""
    imports = get_imports_list(ctx)
    from_graphs = {_["from_graph"] for _ in imports}
    return [
        _
        for _ in completion.graph_uris(ctx=ctx, param=param, incomplete=incomplete)
        if _.value in from_graphs
    ]


def _to_graph_uris(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Provide auto completion items for create/delete command to-graph argument"""
    from_graph = ctx.params["from_graph"]
    imports = graph_imports_list.apply_filters(ctx=ctx, filter_=[("from-graph", from_graph)])
    to_graphs = {_["to_graph"] for _ in imports}
    command = ctx.command.name
    return [
        _
        for _ in completion.graph_uris(ctx=ctx, param=param, incomplete=incomplete)
        if (command == "delete" and _.value in to_graphs)
        or (command == "create" and _.value not in to_graphs and _.value != from_graph)
    ]


@click.command(cls=CmemcCommand, name="create")
@click.argument("from_graph", type=str, shell_complete=completion.graph_uris)
@click.argument("to_graph", type=str, shell_complete=_to_graph_uris)
@click.pass_context
def create_command(ctx: Context, from_graph: str, to_graph: str) -> None:
    """Add statement to import a TO_GRAPH into a FROM_GRAPH.

    Graphs are identified by an IRI. Statement imports are managed by
    creating owl:imports statements such as "FROM_GRAPH owl:imports TO_GRAPH"
    in the FROM_GRAPH. All statements in the TO_GRAPH are then available
    in the FROM_GRAPH.

    Note: The get a list of existing graphs, execute the `graph list` command or
    use tab-completion.
    """
    app: ApplicationContext = ctx.obj
    _validate_graphs(from_graph, to_graph)
    if from_graph == to_graph:
        raise click.UsageError("From graph and to graph cannot be the same.")

    imports = graph_imports_list.apply_filters(
        ctx=ctx, filter_=[("from-graph", from_graph), ("to-graph", to_graph)]
    )
    if imports:
        raise click.UsageError("Import combination already exists.")
    app.echo_info(f"Creating graph import from {from_graph} to {to_graph} ... ", nl=False)

    create_query = SparqlQuery(
        text=GRAPH_IMPORTS_CREATE_SPARQL,
        query_type="UPDATE",
    )
    create_query.get_results(
        placeholder={
            "from_graph": from_graph,
            "to_graph": to_graph,
        }
    )
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="delete")
@click.argument("from_graph", type=str, shell_complete=_from_graph_uris)
@click.argument("to_graph", type=str, shell_complete=_to_graph_uris)
@click.pass_context
def delete_command(ctx: Context, from_graph: str, to_graph: str) -> None:
    """Delete statement to import a TO_GRAPH into a FROM_GRAPH.

    Graphs are identified by an IRI. Statement imports are managed by
    creating owl:imports statements such as "FROM_GRAPH owl:imports TO_GRAPH"
    in the FROM_GRAPH. All statements in the TO_GRAPH are then available
    in the FROM_GRAPH.

    Note: The get a list of existing graph imports, execute the
    `graph imports list` command or use tab-completion.
    """
    app: ApplicationContext = ctx.obj
    _validate_graphs(from_graph, None)
    imports = graph_imports_list.apply_filters(
        ctx=ctx, filter_=[("from-graph", from_graph), ("to-graph", to_graph)]
    )
    if not imports:
        raise click.UsageError("Import combination does not exists.")
    app.echo_info(f"Deleting graph import from {from_graph} to {to_graph} ... ", nl=False)

    delete_query = SparqlQuery(
        text=GRAPH_IMPORTS_DELETE_SPARQL,
        query_type="UPDATE",
    )
    delete_query.get_results(
        placeholder={
            "from_graph": from_graph,
            "to_graph": to_graph,
        }
    )
    app.echo_success("done")


@click.group(cls=CmemcGroup, name="imports")
def imports_group() -> CmemcGroup:  # type: ignore[empty-body]
    """List, create, delete and show graph imports.

    Graphs are identified by an IRI. Statement imports are managed by
    creating owl:imports statements such as "FROM_GRAPH owl:imports TO_GRAPH"
    in the FROM_GRAPH. All statements in the TO_GRAPH are then available
    in the FROM_GRAPH.

    Note: The get a list of existing graphs,
    execute the `graph list` command or use tab-completion.
    """


imports_group.add_command(tree_command)
imports_group.add_command(list_command)
imports_group.add_command(create_command)
imports_group.add_command(delete_command)
