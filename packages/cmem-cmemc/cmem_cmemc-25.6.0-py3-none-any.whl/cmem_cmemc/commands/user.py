"""Keycloak user management commands"""

import sys
from getpass import getpass

import click
from click import ClickException
from cmem.cmempy.config import get_keycloak_base_uri, get_keycloak_realm_id
from cmem.cmempy.keycloak.group import list_groups
from cmem.cmempy.keycloak.user import (
    assign_groups,
    create_user,
    delete_user,
    get_user_by_username,
    list_users,
    request_password_change,
    reset_password,
    unassign_groups,
    update_user,
    user_groups,
)

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.object_list import (
    DirectValuePropertyFilter,
    ObjectList,
    compare_regex,
    transform_lower,
)

NO_USER_ERROR = (
    "{} is not a valid user account. Use the 'admin user list' command "
    "to get a list of existing user accounts."
)
EXISTING_USER_ERROR = "{} does already exist"
NO_GROUP_ERROR = "{} is not a valid group. Valid groups are {}"
INVALID_UNASSIGN_GROUP_ERROR = "Group {} is not assigned to user. Valid groups are {}"
NO_EMAIL_ERROR = "Email is empty for {} user."


def get_users(ctx: click.Context) -> list[dict]:  # noqa: ARG001
    """Get users for object list"""
    users: list[dict] = list_users()
    return users


user_list = ObjectList(
    name="users",
    get_objects=get_users,
    filters=[
        DirectValuePropertyFilter(
            name="enabled",
            description="Filter accounts by enabled flag.",
            property_key="enabled",
            transform=transform_lower,
        ),
        DirectValuePropertyFilter(
            name="email",
            description="Filter accounts by regex matching the email address.",
            property_key="email",
            compare=compare_regex,
            fixed_completion=[],
        ),
        DirectValuePropertyFilter(
            name="username",
            description="Filter accounts by regex matching the username.",
            property_key="username",
            compare=compare_regex,
            fixed_completion=[],
        ),
    ],
)


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    multiple=True,
    help=user_list.get_filter_help_text(),
    shell_complete=user_list.complete_values,
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only username. " "This is useful for piping the IDs into other commands.",
)
@click.pass_context
def list_command(
    ctx: click.Context, filter_: tuple[tuple[str, str]], raw: bool, id_only: bool
) -> None:
    """List user accounts.

    Outputs a list of user accounts, which can be used to get an overview as well
    as a reference for the other commands of the `admin user` command group.
    """
    app = ctx.obj
    users = user_list.apply_filters(ctx=ctx, filter_=filter_)
    if raw:
        app.echo_info_json(users)
        return
    if id_only:
        for usr in users:
            app.echo_info(usr["username"])
        return
    table = [
        (
            usr["username"],
            usr.get("firstName", "-"),
            usr.get("lastName", "-"),
            usr.get("email", "-"),
        )
        for usr in users
    ]
    app.echo_info_table(
        table,
        headers=["Username", "First Name", "Last Name", "Email"],
        sort_column=0,
        empty_table_message="No user accounts found. "
        "Use the `admin user create` command to create an account.",
    )


@click.command(cls=CmemcCommand, name="delete")
@click.argument("username", shell_complete=completion.user_ids)
@click.pass_obj
def delete_command(app: ApplicationContext, username: str) -> None:
    """Delete a user account.

    This command deletes a user account from a realm.

    Note: The deletion of a user account does not delete the assigned groups of
    this account, only the assignments to these groups.
    """
    app.echo_info(f"Deleting user {username} ... ", nl=False)
    users = get_user_by_username(username)
    if not users:
        raise ClickException(NO_USER_ERROR.format(username))

    delete_user(users[0]["id"])
    app.echo_success("deleted")


@click.command(cls=CmemcCommand, name="create")
@click.argument("username")
@click.pass_obj
def create_command(app: ApplicationContext, username: str) -> None:
    """Create a user account.

    This command creates a new user account.

    Note: The created user account has no metadata such as personal data or group
    assignments. In order to add these details to a user account, use the
    `admin user update` command.
    """
    app.echo_info(f"Creating user {username} ... ", nl=False)
    users = get_user_by_username(username)
    if users:
        raise ClickException(EXISTING_USER_ERROR.format(username))

    create_user(username=username)
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="update")
@click.argument("username", shell_complete=completion.user_ids)
@click.option("--first-name", type=click.STRING, required=False, help="Set a new first name.")
@click.option("--last-name", type=click.STRING, required=False, help="Set a new last name.")
@click.option("--email", type=click.STRING, required=False, help="Set a new email.")
@click.option(
    "--assign-group",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.user_group_ids,
    help="Assign a group.",
)
@click.option(
    "--unassign-group",
    type=click.STRING,
    multiple=True,
    shell_complete=completion.user_group_ids,
    help="Unassign a group.",
)
@click.pass_obj
def update_command(  # noqa: PLR0913
    app: ApplicationContext,
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    assign_group: tuple[str, ...],
    unassign_group: tuple[str, ...],
) -> None:
    """Update a user account.

    This command updates metadata and group assignments of a user account.

    For each data value, a separate option needs to be used. All options can
    be combined in a single execution.

    Note: In order to assign a group to a user account, the group need to be
    added or imported to the realm upfront.
    """
    options = (first_name, last_name, email, assign_group, unassign_group)
    if all(_ is None or _ == () for _ in options):
        raise click.UsageError(
            "This commands needs to be used with at least one option "
            "(e.g. --email). See the command help for a list of options."
        )
    app.echo_info(f"Updating user {username} ... ", nl=False)
    users = get_user_by_username(username)
    if not users:
        raise ClickException(NO_USER_ERROR.format(username))
    user_id = users[0]["id"]
    all_groups = {group["name"]: group["id"] for group in list_groups()}
    invalid_groups = [group for group in assign_group if group not in all_groups]
    existing_user_groups = {group["name"] for group in user_groups(user_id)}

    if invalid_groups:
        raise ClickException(
            NO_GROUP_ERROR.format(
                ", ".join(invalid_groups), ", ".join(all_groups.keys() - set(existing_user_groups))
            )
        )

    invalid_unassign_groups = [
        group for group in unassign_group if group not in existing_user_groups
    ]
    if invalid_unassign_groups:
        raise ClickException(
            INVALID_UNASSIGN_GROUP_ERROR.format(
                ", ".join(invalid_unassign_groups), ", ".join(existing_user_groups)
            )
        )

    assign_group_ids = [all_groups[name] for name in assign_group]
    unassign_groups_ids = [all_groups[name] for name in unassign_group]
    unassign_groups(user_id, unassign_groups_ids)
    assign_groups(user_id, assign_group_ids)

    update_user(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        email_verified=True if email else None,
    )
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="password")
@click.argument("username", shell_complete=completion.user_ids)
@click.option(
    "--value", help="With this option, the new password can be set in a non-interactive way."
)
@click.option(
    "--temporary", is_flag=True, help="If enabled, the user must change the password on next login."
)
@click.option(
    "--request-change",
    is_flag=True,
    help="If enabled, will send a email to user to reset the password.",
)
@click.pass_obj
def password_command(
    app: ApplicationContext, username: str, value: str, temporary: bool, request_change: bool
) -> None:
    """Change the password of a user account.

    With this command, the password of a user account can be changed.
    The default execution mode of this command is an interactive prompt which asks
    for the password (twice). In order automate password changes, you can use the
    `--value` option.

    Warning: Providing passwords on the command line can be dangerous
    (e.g. due to a potential exploitation in the shell history).
    A suggested more save way for automation is to provide the password in a variable
    first (e.g. with `NEW_PASS=$(pwgen -1 40)`) and use it afterward in the
    cmemc call: `cmemc admin user password max --value ${NEW_PASS}`.
    """
    app.echo_info(f"Changing password for account {username} ... ", nl=False)
    users = get_user_by_username(username)
    if not users:
        raise ClickException(NO_USER_ERROR.format(username))
    if not value and not request_change:
        app.echo_info("\nNew password: ", nl=False)
        value = getpass(prompt="")
        app.echo_info("Retype new password: ", nl=False)
        retype_password = getpass(prompt="")
        if value != retype_password:
            app.echo_error("Sorry, passwords do not match.")
            app.echo_error("password unchanged")
            sys.exit(1)
    if value:
        reset_password(user_id=users[0]["id"], value=value, temporary=temporary)
    if request_change and not users[0].get("email", None):
        raise ClickException(NO_EMAIL_ERROR.format(username))
    if request_change:
        request_password_change(users[0]["id"])
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="open")
@click.argument(
    "usernames", nargs=-1, required=False, type=click.STRING, shell_complete=completion.user_ids
)
@click.pass_obj
def open_command(app: ApplicationContext, usernames: str) -> None:
    """Open user in the browser.

    With this command, you can open a user in the keycloak console in
    your browser to change them.

    The command accepts multiple usernames which results in
    opening multiple browser tabs.
    """
    open_user_base_uri = (
        f"{get_keycloak_base_uri()}/admin/master/console/#/" f"{get_keycloak_realm_id()}/users"
    )
    if not usernames:
        app.echo_debug(f"Open users list: {open_user_base_uri}")
        click.launch(open_user_base_uri)
    else:
        users = list_users()
        user_name_id_map = {u["username"]: u["id"] for u in users}
        for _ in usernames:
            if _ not in user_name_id_map:
                raise ClickException(NO_USER_ERROR.format(_))
            user_id = user_name_id_map[_]
            open_user_uri = f"{open_user_base_uri}/{user_id}/settings"

            app.echo_debug(f"Open {_}: {open_user_uri}")
            click.launch(open_user_uri)


@click.group(cls=CmemcGroup)
def user() -> CmemcGroup:  # type: ignore[empty-body]
    """List, create, delete and modify user accounts.

    This command group is an opinionated interface to the Keycloak realm of your
    Corporate Memory instance. In order to be able to manage user data, the
    configured cmemc connection account needs to be equipped with the
    `manage-users` role in the used realm.

    User accounts are identified by a username which unique in the scope of
    the used realm.

    In case your Corporate Memory deployment does not use the default deployment
    layout, the following additional config variables can be used in your
    connection configuration: `KEYCLOAK_BASE_URI` defaults to
    `/auth` on `CMEM_BASE_URI` and locates your Keycloak deployment;
    `KEYCLOAK_REALM_ID` defaults to `cmem` and identifies the used realm.
    """


user.add_command(list_command)
user.add_command(create_command)
user.add_command(update_command)
user.add_command(delete_command)
user.add_command(password_command)
user.add_command(open_command)
