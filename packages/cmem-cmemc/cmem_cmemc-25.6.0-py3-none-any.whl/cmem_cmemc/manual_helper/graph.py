"""Generate a help text and command structure graph."""

import contextlib

import click.core


def print_manual_graph(ctx: click.core.Context, version: str) -> None:
    """Output the complete manual graph.

    Returns: None
    """
    comment = "This dataset represents the complete inline documentation " "of cmemc as a graph"
    ctx.obj.echo_info(
        f"""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix void: <http://rdfs.org/ns/void#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix skos: <http://www.w3.org/2004/02/skos/core#>.
@prefix cli: <https://vocabs.eccenca.com/cli/>.
@prefix s: <http://schema.org/>.
@prefix : <https://cmemc.eccenca.dev/>.
@prefix i: <https://eccenca.com/go/cmemc>.

: a void:Dataset ;
    owl:versionInfo "{version}" ;
    rdfs:label "cmemc: Documentation Graph" ;
    rdfs:comment "{comment}" .

i: a s:SoftwareApplication ;
    rdfs:label "cmemc" ;
    s:softwareVersion "{version}" .
"""
    )
    print_group_manual_graph_recursive(ctx.command, ctx=ctx)


def print_group_manual_graph_recursive(
    command_group: click.Command | click.Group, ctx: click.core.Context, prefix: str = ""
) -> None:
    """Output documentation graph (recursive)."""
    commands = command_group.commands  # type: ignore[union-attr]
    for key in commands:
        if key == "manual":
            continue
        item = commands[key]
        iri = f":{prefix}{key}"
        ctx.obj.echo_info(f"{iri} skos:notation '{key}' .")
        if isinstance(item, click.Group):
            comment = item.get_short_help_str(limit=200)
            sub_group_iri = f":{prefix[:-1]}"
            if sub_group_iri == ":":
                sub_group_iri = "<https://eccenca.com/go/cmemc>"
            ctx.obj.echo_info(f"{iri} a cli:CommandGroup .")
            ctx.obj.echo_info(f"{iri} rdfs:label '{prefix}{key} Command Group' .")
            ctx.obj.echo_info(f"{iri} cli:subGroupOf {sub_group_iri} .")
            ctx.obj.echo_info(f'{iri} rdfs:comment """{comment}""" .')
            print_group_manual_graph_recursive(item, ctx=ctx, prefix=f"{prefix}{key}-")
        elif isinstance(item, click.Command):
            comment = item.get_short_help_str(limit=200)
            group_iri = f":{prefix[:-1]}"
            ctx.obj.echo_info(f"{iri} a cli:Command .")
            ctx.obj.echo_info(f"{iri} rdfs:label '{prefix}{key} Command' .")
            ctx.obj.echo_info(f"{iri} cli:group {group_iri} .")
            ctx.obj.echo_info(f'{iri} rdfs:comment """{comment}""" .')
            for parameter in item.params:
                print_parameter_manual_graph(parameter, ctx=ctx, prefix=f"{prefix}{key}-")
        else:
            pass


def print_parameter_manual_graph(
    item: click.Parameter | click.Option, ctx: click.core.Context, prefix: str = ""
) -> None:
    """Output documentation graph for parameter."""
    iri = f":{prefix}{item.name}"
    ctx.obj.echo_info(f"{iri} a cli:Parameter .")
    ctx.obj.echo_info(f"{iri} cli:command :{prefix[:-1]}.")
    if len(item.opts) == 1:
        ctx.obj.echo_info(f"{iri} rdfs:label '{item.opts[0]}'.")
    else:
        ctx.obj.echo_info(f'{iri} rdfs:label """{max(item.opts, key=len)}""".')
        ctx.obj.echo_info(f'{iri} cli:shortenedOption """{min(item.opts, key=len)}""".')
    if item.default not in (None, False, [None, None]):
        ctx.obj.echo_info(f"{iri} cli:defaultValue '{item.default}'.")
    with contextlib.suppress(AttributeError):
        ctx.obj.echo_info(f'{iri} rdfs:comment """{item.help}""".')  # type: ignore[union-attr]
