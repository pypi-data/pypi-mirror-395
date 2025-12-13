"""access control"""

import click
import requests.exceptions
from click import Option
from cmem.cmempy.dp.authorization.conditions import (
    create_access_condition,
    delete_access_condition,
    fetch_all_acls,
    get_access_condition_by_iri,
    review_graph_rights,
    update_access_condition,
)
from cmem.cmempy.keycloak.user import get_user_by_username, user_groups

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.constants import NS_ACL, NS_ACTION, NS_GROUP, NS_USER
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.utils import (
    convert_iri_to_qname,
    convert_qname_to_iri,
    get_query_text,
    struct_to_table,
)

# option descriptions
HELP_TEXTS = {
    "name": "A optional name.",
    "id": "An optional ID (will be an UUID otherwise).",
    "description": "An optional description.",
    "user": "A specific user account required by the access condition.",
    "group": "A membership in a user group required by the access condition.",
    "read_graph": "Grants read access to a graph.",
    "write_graph": "Grants write access to a graph (includes read access).",
    "action": "Grants usage permissions to an action / functionality.",
    "read_graph_pattern": (
        "Grants management of conditions granting read access on graphs matching the defined "
        "pattern. A pattern consists of a constant string and a wildcard ('*') at the end of "
        "the pattern or the wildcard alone."
    ),
    "write_graph_pattern": (
        "Grants management of conditions granting write access on graphs matching the defined "
        "pattern. A pattern consists of a constant string and a wildcard ('*') at the end of "
        "the pattern or the wildcard alone."
    ),
    "action_pattern": (
        "Grants management of conditions granting action allowance for actions matching the "
        "defined pattern. A pattern consists of a constant string and a wildcard ('*') at the "
        "end of the pattern or the wildcard alone."
    ),
    "query": "Dynamic access condition query (file or the query catalog IRI).",
    "replace": (
        "Replace (overwrite) existing access condition, if present. "
        "Can be used only in combination with '--id'."
    ),
}

WARNING_UNKNOWN_USER = "Unknown User or no access to get user info."
WARNING_NO_GROUP_ACCESS = "You do not have the permission to retrieve user groups"
WARNING_USE_GROUP = "Use the --group option to assign groups manually (what-if-scenario)."

PUBLIC_USER_URI = "https://vocab.eccenca.com/auth/AnonymousUser"
PUBLIC_GROUP_URI = "https://vocab.eccenca.com/auth/PublicGroup"

KNOWN_ACCESS_CONDITION_URLS = [PUBLIC_USER_URI, PUBLIC_GROUP_URI]


def _list_to_acl_url(ctx: ApplicationContext, param: Option, value: list) -> list:
    """Option callback which returns a URI for a list of strings.

    or list of URIs, if a tuple comes from click
    or not, if it is already a known URI .... or None
    """
    return [_value_to_acl_url(ctx, param, _) for _ in value]


def _value_to_acl_url(
    ctx: ApplicationContext,  # noqa: ARG001
    param: Option,
    value: str | None,
) -> str | None:
    """Option callback which returns a URI for a string.

    or not, if it is already a known URI .... or None
    """
    if value == "" or value is None:
        return value
    if value.startswith(("http://", "https://")):
        return value
    match param.name:
        case "groups":
            return f"{NS_GROUP}{value}"
        case "user":
            return f"{NS_USER}{value}"
    return f"{NS_ACL}{value}"


def generate_acl_name(user: str | None, groups: list[str], query: str | None) -> str:
    """Create an access condition name based on user and group assignments."""
    if query is not None:
        return "Query based Dynamic Access Condition"
    if len(groups) > 0:
        group_term = "groups" if len(groups) > 1 else "group"
        groups_labels = ", ".join(
            [convert_iri_to_qname(iri=_, default_ns=NS_GROUP)[1:] for _ in groups]
        )
        if user:
            return (
                f"Condition for user {convert_iri_to_qname(iri=user, default_ns=NS_USER)[1:]} "
                f"and {group_term} {groups_labels}"
            )
        return f"Condition for {group_term} {groups_labels}"
    if user:
        return f"Condition for user: {convert_iri_to_qname(iri=user, default_ns=NS_USER)[1:]}"
    return "Condition for ALL users"


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only URIs. This is useful for piping the IDs into other commands.",
)
@click.pass_obj
def list_command(app: ApplicationContext, raw: bool, id_only: bool) -> None:
    """List access conditions.

    This command retrieves and lists all access conditions, which are manageable
    by the current account.
    """
    acls = fetch_all_acls()
    if raw:
        app.echo_info_json(acls)
        return
    if id_only:
        for graph in acls:
            app.echo_info(convert_iri_to_qname(iri=graph.get("iri"), default_ns=NS_ACL))
        return
    table = [
        (convert_iri_to_qname(iri=_.get("iri"), default_ns=NS_ACL), _.get("name", "-"))
        for _ in acls
    ]
    app.echo_info_table(
        table,
        headers=["URI", "Name"],
        sort_column=0,
        empty_table_message="No access conditions found. "
        "Use the `admin acl create` command to create a new access condition.",
    )


@click.command(cls=CmemcCommand, name="inspect")
@click.argument("access_condition_id", type=click.STRING, shell_complete=completion.acl_ids)
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.pass_obj
def inspect_command(app: ApplicationContext, access_condition_id: str, raw: bool) -> None:
    """Inspect an access condition.

    Note: access conditions can be listed by using the `acl list` command.
    """
    iri = convert_qname_to_iri(qname=access_condition_id, default_ns=NS_ACL)
    access_condition = get_access_condition_by_iri(iri).json()

    if raw:
        app.echo_info_json(access_condition)
        return

    table = struct_to_table(access_condition)
    app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)


@click.command(cls=CmemcCommand, name="create")
@click.option(
    "--user",
    type=click.STRING,
    shell_complete=completion.acl_users,
    help=HELP_TEXTS["user"],
    callback=_value_to_acl_url,
)
@click.option(
    "--group",
    "groups",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.acl_groups,
    help=HELP_TEXTS["group"],
    callback=_list_to_acl_url,
)
@click.option(
    "--read-graph",
    "read_graphs",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.graph_uris_with_all_graph_uri,
    help=HELP_TEXTS["read_graph"],
)
@click.option(
    "--write-graph",
    "write_graphs",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.graph_uris_with_all_graph_uri,
    help=HELP_TEXTS["write_graph"],
)
@click.option(
    "--action",
    "actions",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.acl_actions,
    help=HELP_TEXTS["action"],
)
@click.option(
    "--read-graph-pattern",
    "read_graph_patterns",
    type=click.STRING,
    multiple=True,
    help=HELP_TEXTS["read_graph_pattern"],
)
@click.option(
    "--write-graph-pattern",
    "write_graph_patterns",
    type=click.STRING,
    multiple=True,
    help=HELP_TEXTS["write_graph_pattern"],
)
@click.option(
    "--action-pattern",
    "action_patterns",
    type=click.STRING,
    multiple=True,
    help=HELP_TEXTS["action_pattern"],
)
@click.option(
    "--query",
    "query",
    type=click.STRING,
    shell_complete=completion.remote_queries_and_sparql_files,
    help=HELP_TEXTS["query"],
)
@click.option(
    "--id",
    "id_",
    type=click.STRING,
    help=HELP_TEXTS["id"],
)
@click.option(
    "--name",
    "name",
    type=click.STRING,
    help=HELP_TEXTS["name"],
)
@click.option(
    "--description",
    "description",
    type=click.STRING,
    help=HELP_TEXTS["description"],
)
@click.option("--replace", is_flag=True, help=HELP_TEXTS["replace"])
@click.pass_obj
# pylint: disable-msg=too-many-arguments
def create_command(  # noqa: PLR0913
    app: ApplicationContext,
    name: str,
    id_: str,
    description: str,
    user: str,
    groups: list[str],
    read_graphs: tuple[str],
    write_graphs: tuple[str],
    actions: tuple[str],
    read_graph_patterns: tuple[str],
    write_graph_patterns: tuple[str],
    action_patterns: tuple[str],
    query: str,
    replace: bool,
) -> None:
    """Create an access condition.

    With this command, new access conditions can be created.

    An access condition captures information about WHO gets access to WHAT.
    In order to specify WHO gets access, use the `--user` and / or `--group` options.
    In order to specify WHAT an account get access to, use the `--read-graph`,
    `--write-graph` and `--action` options.`

    In addition to that, you can specify a name, a description and an ID (all optional).

    A special case are dynamic access conditions, based on a SPARQL query: Here you
    have to provide a query with the projection variables `user`, `group` `readGraph`
    and `writeGraph` to create multiple grants at once. You can either provide a query file
    or a query URL from the query catalog.

    Note: Queries for dynamic access conditions are copied into the ACL, so changing the
    query in the query catalog does not change it in the access condition.

    Example: cmemc admin acl create --group local-users --write-graph https://example.org/
    """
    if replace and not id_:
        raise click.UsageError("To replace an access condition, you must specify an ID.")

    if (
        not read_graphs
        and not write_graphs
        and not actions
        and not read_graph_patterns
        and not write_graph_patterns
        and not action_patterns
        and not query
    ):
        raise click.UsageError(
            "Missing access / usage grant. Use at least one of the following options: "
            "--read-graph, --write-graph, --action, --read-graph-pattern, "
            "--write-graph-pattern, --action-pattern or --query."
        )
    query_str = None
    if query:
        query_str = get_query_text(query, {"user", "group", "readGraph", "writeGraph"})

    if not user and not groups and not query:
        app.echo_warning("Access conditions without a user or group assignment affects ALL users.")

    if not name:
        name = generate_acl_name(user=user, groups=groups, query=query)

    if not description:
        description = "This access condition was created with cmemc."

    if replace and NS_ACL + id_ in [_["iri"] for _ in fetch_all_acls()]:
        app.echo_info(f"Replacing access condition '{id_}' ... ", nl=False)
        delete_access_condition(iri=NS_ACL + id_)
    else:
        app.echo_info(f"Creating access condition '{name}' ... ", nl=False)
    create_access_condition(
        name=name,
        static_id=id_,
        description=description,
        user=user,
        groups=groups,
        read_graphs=list(read_graphs),
        write_graphs=list(write_graphs),
        actions=[convert_qname_to_iri(qname=_, default_ns=NS_ACTION) for _ in actions],
        read_graph_patterns=list(read_graph_patterns),
        write_graph_patterns=list(write_graph_patterns),
        action_patterns=list(action_patterns),
        query=query_str,
    )
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="update")
@click.argument(
    "access_condition_id",
    nargs=1,
    required=True,
    type=click.STRING,
    shell_complete=completion.acl_ids,
)
@click.option(
    "--name",
    "name",
    type=click.STRING,
    help=HELP_TEXTS["name"],
)
@click.option(
    "--description",
    "description",
    type=click.STRING,
    help=HELP_TEXTS["description"],
)
@click.option(
    "--user",
    type=click.STRING,
    shell_complete=completion.acl_users,
    help=HELP_TEXTS["user"],
    callback=_value_to_acl_url,
)
@click.option(
    "--group",
    "groups",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.acl_groups,
    help=HELP_TEXTS["group"],
    callback=_list_to_acl_url,
)
@click.option(
    "--read-graph",
    "read_graphs",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.graph_uris_with_all_graph_uri,
    help=HELP_TEXTS["read_graph"],
)
@click.option(
    "--write-graph",
    "write_graphs",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.graph_uris_with_all_graph_uri,
    help=HELP_TEXTS["write_graph"],
)
@click.option(
    "--action",
    "actions",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.acl_actions,
    help=HELP_TEXTS["action"],
)
@click.option(
    "--read-graph-pattern",
    "read_graph_patterns",
    type=click.STRING,
    multiple=True,
    help=HELP_TEXTS["read_graph_pattern"],
)
@click.option(
    "--write-graph-pattern",
    "write_graph_patterns",
    type=click.STRING,
    multiple=True,
    help=HELP_TEXTS["write_graph_pattern"],
)
@click.option(
    "--action-pattern",
    "action_patterns",
    type=click.STRING,
    multiple=True,
    help=HELP_TEXTS["action_pattern"],
)
@click.option(
    "--query",
    "query",
    type=click.STRING,
    shell_complete=completion.remote_queries_and_sparql_files,
    help=HELP_TEXTS["query"],
)
@click.pass_obj
# pylint: disable-msg=too-many-arguments
def update_command(  # noqa: PLR0913
    app: ApplicationContext,
    access_condition_id: str,
    name: str,
    description: str,
    user: str,
    groups: list[str],
    read_graphs: tuple[str],
    write_graphs: tuple[str],
    actions: tuple[str],
    read_graph_patterns: tuple[str],
    write_graph_patterns: tuple[str],
    action_patterns: tuple[str],
    query: str,
) -> None:
    """Update an access condition.

    Given an access condition URL, you can change specific options
    to new values.
    """
    iri = convert_qname_to_iri(qname=access_condition_id, default_ns=NS_ACL)
    payload = get_access_condition_by_iri(iri=iri).json()
    app.echo_info(
        f"Updating access condition {payload['name']} ... ",
        nl=False,
    )
    query_str = None
    if query:
        query_str = get_query_text(query, {"user", "group", "readGraph", "writeGraph"})

    update_access_condition(
        iri=iri,
        name=name,
        description=description,
        user=user,
        groups=groups,
        read_graphs=read_graphs,
        write_graphs=write_graphs,
        actions=[convert_qname_to_iri(qname=_, default_ns=NS_ACTION) for _ in actions],
        read_graph_patterns=read_graph_patterns,
        write_graph_patterns=write_graph_patterns,
        action_patterns=action_patterns,
        query=query_str,
    )
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="delete")
@click.option(
    "-a",
    "--all",
    "all_",
    is_flag=True,
    help="Delete all access conditions. " "This is a dangerous option, so use it with care.",
)
@click.argument(
    "access_condition_ids",
    nargs=-1,
    type=click.STRING,
    shell_complete=completion.acl_ids,
)
@click.pass_obj
def delete_command(app: ApplicationContext, all_: bool, access_condition_ids: list[str]) -> None:
    """Delete access conditions.

    This command deletes existing access conditions from the account.

    Note: Access conditions can be listed by using the `cmemc admin acs list` command.
    """
    if access_condition_ids == () and not all_:
        raise click.UsageError(
            "Either specify at least one access condition ID,"
            " or use the --all option to delete all access conditions."
        )
    if all_:
        access_condition_ids = [_["iri"] for _ in fetch_all_acls()]

    count = len(access_condition_ids)
    for index, _ in enumerate(access_condition_ids, 1):
        app.echo_info(f"Delete access condition {index}/{count}: {_} ... ", nl=False)
        delete_access_condition(iri=convert_qname_to_iri(qname=_, default_ns=NS_ACL))
        app.echo_success("done")


@click.command(name="review")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.argument("user", type=click.STRING, shell_complete=completion.acl_users)
@click.option(
    "--group",
    "groups",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.acl_groups,
    callback=_list_to_acl_url,
    help="Add groups to the review request (what-if-scenario).",
)
@click.pass_obj
def review_command(app: ApplicationContext, raw: bool, user: str, groups: list[str] | None) -> None:
    """Review grants for a given account.

    This command has two working modes: (1) You can review the access conditions
    of an actual account,
    (2) You can review the access conditions of an imaginary account with a set of
    freely added groups (what-if-scenario).

    The output of the command is a list of grants the account has based on your input
    and all access conditions loaded in the store. In addition to that, some metadata
    of the account is shown.
    """
    if not groups:
        app.echo_debug("Trying to fetch groups from keycloak.")
        keycloak_user = get_user_by_username(username=user)
        if not keycloak_user:
            if user != PUBLIC_USER_URI:
                app.echo_warning(WARNING_UNKNOWN_USER)
                app.echo_warning(WARNING_USE_GROUP)
        else:
            try:
                keycloak_user_groups = user_groups(user_id=keycloak_user[0]["id"])
                groups = [f"{NS_GROUP}{_['name']}" for _ in keycloak_user_groups]
            except (requests.exceptions.HTTPError, IndexError):
                app.echo_warning(WARNING_NO_GROUP_ACCESS)
                app.echo_warning(WARNING_USE_GROUP)
    app.echo_debug(f"Got groups: {groups}")
    account_iri = f"{NS_USER}{user}" if user != PUBLIC_USER_URI else PUBLIC_USER_URI
    review_info: dict = review_graph_rights(account_iri=account_iri, group_iris=groups).json()
    review_info["groupIri"] = groups
    if raw:
        app.echo_info_json(review_info)
        return
    table = struct_to_table(review_info)
    app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)


@click.group(cls=CmemcGroup)
def acl() -> CmemcGroup:  # type: ignore[empty-body]
    """List, create, delete and modify and review access conditions.

    With this command group, you can manage and inspect access conditions
    in eccenca Corporate Memory. Access conditions are identified by a URL.
    They grant access to knowledge graphs or actions to user or groups.
    """


acl.add_command(list_command)
acl.add_command(inspect_command)
acl.add_command(create_command)
acl.add_command(update_command)
acl.add_command(delete_command)
acl.add_command(review_command)
