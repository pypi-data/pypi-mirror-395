"""Keycloak client management commands"""

import click
from click import ClickException, UsageError
from cmem.cmempy.config import get_keycloak_base_uri, get_keycloak_realm_id
from cmem.cmempy.keycloak.client import (
    generate_client_secret,
    get_client_by_client_id,
    get_client_secret,
    list_open_id_clients,
)

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext

NO_CLIENT_ERROR = (
    "{} is not a valid client account. "
    "Use the 'admin client list' command "
    "to get a list of existing client accounts."
)


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only Client ID. " "This is useful for piping the IDs into other commands.",
)
@click.pass_obj
def list_command(app: ApplicationContext, raw: bool, id_only: bool) -> None:
    """List client accounts.

    Outputs a list of client accounts, which can be used to get an overview as well
    as a reference for the other commands of the `admin client` command group.

    Note: The list command only outputs clients which have a client secret.
    """
    clients = list_open_id_clients()
    if raw:
        app.echo_info_json(clients)
        return
    if id_only:
        for cnt in clients:
            app.echo_info(cnt["clientId"])
        return
    table = [(_["clientId"], _.get("description", "-")) for _ in clients]
    app.echo_info_table(table, headers=["Client ID", "Description"], sort_column=0)


@click.command(cls=CmemcCommand, name="secret")
@click.argument("client-id", shell_complete=completion.client_ids)
@click.option("--generate", is_flag=True, help="Generate a new secret")
@click.option("--output", is_flag=True, help="Display client secret")
@click.pass_obj
def secret_command(app: ApplicationContext, client_id: str, generate: bool, output: bool) -> None:
    """Get or generate a new secret for a client account.

    This command retrieves or generates a new secret for a client account from a realm.
    """
    if not output and not generate:
        app.echo_info(click.get_current_context().get_help())
        raise UsageError("You need to use '--output' or '--generate' as an option.")

    clients = get_client_by_client_id(client_id)
    if not clients:
        raise ClickException(NO_CLIENT_ERROR.format(client_id))

    if generate:
        if not output:
            app.echo_info(f"Generating a new secret for {client_id} ... ", nl=False)
        credential = generate_client_secret(client_id=clients[0]["id"])
        if not output:
            app.echo_success("done")
    else:
        credential = get_client_secret(client_id=clients[0]["id"])

    if output:
        app.echo_result(credential["value"])


@click.command(cls=CmemcCommand, name="open")
@click.argument(
    "client-ids", nargs=-1, required=False, type=click.STRING, shell_complete=completion.client_ids
)
@click.pass_obj
def open_command(app: ApplicationContext, client_ids: tuple[str]) -> None:
    """Open clients in the browser.

    With this command, you can open a client in the keycloak web
    interface in your browser.

    The command accepts multiple client IDs which results in
    opening multiple browser tabs.
    """
    open_client_base_uri = (
        f"{get_keycloak_base_uri()}/admin/master/console/#/" f"{get_keycloak_realm_id()}/clients"
    )
    if not client_ids:
        app.echo_debug(f"Open users list: {open_client_base_uri}")
        click.launch(open_client_base_uri)
    else:
        clients = list_open_id_clients()
        client_id_map = {c["clientId"]: c["id"] for c in clients}
        for _ in client_ids:
            if _ not in client_id_map:
                raise ClickException(NO_CLIENT_ERROR.format(_))
            client_id = client_id_map[_]
            open_user_uri = f"{open_client_base_uri}/{client_id}/settings"

            app.echo_debug(f"Open {_}: {open_user_uri}")
            click.launch(open_user_uri)


@click.group(cls=CmemcGroup)
def client() -> CmemcGroup:  # type: ignore[empty-body]
    """List client accounts, get or generate client account secrets.

    This command group is an opinionated interface to the Keycloak realm of your
    Corporate Memory instance. In order to be able to use the commands in this group,
    the configured cmemc connection account needs to be equipped with the
    `manage-clients` role in the used realm.

    Client accounts are identified by a client ID which is unique in the scope of
    the used realm.

    In case your Corporate Memory deployment does not use the default deployment
    layout, the following additional config variables can be used in your
    connection configuration: `KEYCLOAK_BASE_URI` defaults to
    `{CMEM_BASE_URI}/auth` and locates your Keycloak deployment;
    `KEYCLOAK_REALM_ID` defaults to `cmem` and identifies the used realm.
    """


client.add_command(list_command)
client.add_command(secret_command)
client.add_command(open_command)
