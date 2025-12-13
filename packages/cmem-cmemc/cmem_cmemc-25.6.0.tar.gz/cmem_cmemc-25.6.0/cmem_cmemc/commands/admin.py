"""admin commands for cmem command line interface."""

from datetime import datetime, timezone

import click
import jwt
import timeago
from click import ClickException
from cmem.cmempy.api import get_access_token, get_token
from cmem.cmempy.config import get_cmem_base_uri
from cmem.cmempy.health import get_complete_status_info
from dateutil.relativedelta import relativedelta

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.commands.acl import acl
from cmem_cmemc.commands.client import client
from cmem_cmemc.commands.metrics import metrics
from cmem_cmemc.commands.migration import migration
from cmem_cmemc.commands.store import store
from cmem_cmemc.commands.user import user
from cmem_cmemc.commands.workspace import workspace
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.utils import struct_to_table

WARNING_MIGRATION = (
    "Your workspace configuration version does not match your Explore version. "
    "Please consider migrating your workspace configuration (admin store migrate command)."
)
WARNING_SHAPES = (
    "Your ShapeCatalog version does not match your Explore version. "
    "Please consider updating your bootstrap data (admin store boostrap command)."
)


def _check_cmem_license(app: ApplicationContext, data: dict, exit_1: str) -> None:
    """Check grace period of CMEM license."""
    if "license" not in data["explore"]["info"]:
        # DP < 24.1 has no cmem license information here
        return
    license_ = data["explore"]["info"]["license"]
    in_grace_period: bool = license_.get("inGracePeriod", False)
    if in_grace_period:
        cmem_license_end = license_["validDate"]
        output = f"Your Corporate Memory license expired on {cmem_license_end}."
        if exit_1 in ("error", "always"):
            raise ClickException(output)
        app.echo_error(output)


def _check_graphdb_license(app: ApplicationContext, data: dict, months: int, exit_1: str) -> None:
    """Check grace period of graphdb license."""
    if "licenseExpiration" not in data["explore"]["info"]["store"]:
        # DP < 24.1 has no graph license information here
        return
    expiration_date_str = data["explore"]["info"]["store"]["licenseExpiration"]
    expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d").astimezone(tz=timezone.utc)
    grace_starts = expiration_date - relativedelta(months=months)
    if grace_starts < datetime.now(tz=timezone.utc):
        graphdb_license_end = data["explore"]["info"]["store"]["licenseExpiration"]
        output = f"Your GraphDB license expires on {graphdb_license_end}."
        if exit_1 == "always":
            raise ClickException(output)
        app.echo_warning(output)


@click.command(cls=CmemcCommand, name="status")
@click.option(
    "--key",
    "key",
    shell_complete=completion.status_keys,
    help="Get only specific key(s) from the status / info output. There are "
    "two special keys available: 'all' will list all available keys in "
    "the table, 'overall.healthy' with result in  UP in case all "
    "health flags are UP as well (otherwise DOWN).",
)
@click.option(
    "--exit-1",
    type=click.Choice(["never", "error", "always"]),
    default="never",
    show_default=True,
    help="Specify, when this command returns with exit code 1. Available options are "
    "'never' (exit 0 on errors and warnings), "
    "'error' (exit 1 on errors, exit 0 on warnings), "
    "'always' (exit 1 on errors and warnings).",
)
@click.option(
    "--enforce-table",
    is_flag=True,
    help="A single value with --key will be returned as plain text instead "
    "of a table with one row and the header. This default behaviour "
    "allows for more easy integration with scripts. This flag enforces "
    "the use of tabular output, even for single row tables.",
)
@click.option(
    "--raw", is_flag=True, help="Outputs combined raw JSON output of the health/info endpoints."
)
@click.pass_obj
def status_command(  # noqa: C901, PLR0912
    app: ApplicationContext, key: str, exit_1: str, enforce_table: bool, raw: bool
) -> None:
    """Output health and version information.

    This command outputs version and health information of the
    selected deployment. If the version information cannot be retrieved,
    UNKNOWN is shown.

    Additionally, this command informs you in one of these cases:
    (1) A warning, if the target version of your cmemc client is newer than the version
    of your backend.
    (2) A warning, if the ShapeCatalog has a different version than your Explore component.
    (3) An error, if your Corporate Memory license is expired (grace period).
    (4) A warning, if your Graph DB license will expire in less than a month.

    To get status information of all configured
    deployments use this command in combination with parallel.

    Example: cmemc config list | parallel --ctag cmemc -c {} admin status
    """
    _ = get_complete_status_info()
    if "error" in _["build"]:
        app.echo_debug(_["build"]["error"])
    if "error" in _["explore"]:
        app.echo_debug(_["explore"]["error"])

    if exit_1 in ("always", "error") and (_["overall"]["healthy"] != "UP"):
        raise ClickException(
            f"One or more major status flags are DOWN or UNKNOWN: {_!r}",
        )
    if raw:
        app.echo_info_json(_)
        return
    if key:
        table = [line for line in struct_to_table(_) if line[0].startswith(key) or key == "all"]
        if len(table) == 1 and not enforce_table:
            app.echo_info(table[0][1])
            return
        if len(table) == 0:
            raise ClickException(f"No values for key(s): {key}")
        app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)
        return
    app.check_versions()
    _workspace_config = _["explore"]["info"].get("workspaceConfiguration", {})
    if _workspace_config.get("workspacesToMigrate"):
        if exit_1 == "always":
            raise ClickException(WARNING_MIGRATION)
        app.echo_warning(WARNING_MIGRATION)

    if _["shapes"]["version"] not in (_["explore"]["version"], "UNKNOWN"):
        if exit_1 == "always":
            raise ClickException(WARNING_SHAPES)
        app.echo_warning(WARNING_SHAPES)

    _check_cmem_license(app=app, data=_, exit_1=exit_1)
    _check_graphdb_license(app=app, data=_, months=1, exit_1=exit_1)
    if _["store"]["type"] != "GRAPHDB":
        store_version = _["store"]["type"] + "/" + _["store"]["version"]
    else:
        store_version = _["store"]["version"]
    table = [
        ("EXPLORE", _["explore"]["version"], _["explore"]["healthy"]),
        ("BUILD", _["build"]["version"], _["build"]["healthy"]),
        ("SHAPES", _["shapes"]["version"], _["shapes"]["healthy"]),
        ("STORE", store_version, _["store"]["healthy"]),
    ]
    app.echo_info_table(
        table,
        headers=["Component", "Version", "Status"],
        sort_column=0,
        caption=f"Status of {get_cmem_base_uri()}",
    )


@click.command(cls=CmemcCommand, name="token")
@click.option(
    "--raw",
    is_flag=True,
    help="Outputs raw JSON. Note that this option will always try to fetch "
    "a new JSON token response. In case you are working with "
    "OAUTH_GRANT_TYPE=prefetched_token, this may lead to an error.",
)
@click.option(
    "--decode",
    is_flag=True,
    help="Decode the access token and outputs the raw JSON. Note that the "
    "access token is only decoded and esp. not validated.",
)
@click.option(
    "--ttl",
    is_flag=True,
    help="Output information about the lifetime of the access token. "
    "In combination with --raw, it outputs the TTL in seconds.",
)
@click.pass_obj
def token_command(app: ApplicationContext, raw: bool, decode: bool, ttl: bool) -> None:
    """Fetch and output an access token.

    This command can be used to check for correct authentication as well as
    to use the token with wget / curl or similar standard tools:

    Example: curl -H "Authorization: Bearer $(cmemc -c my admin token)"
    $(cmemc -c my config get DP_API_ENDPOINT)/api/custom/slug

    Please be aware that this command can reveal secrets which you might
    not want to be present in log files or on the screen.
    """
    # Note:
    # - get_access_token returns the token string which is maybe from conf
    # - get_token fetches a new token incl. envelope from keycloak

    token = get_access_token()
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    if ttl:
        app.echo_debug(token)
        iat_ts = decoded_token["iat"]
        exp_ts = decoded_token["exp"]
        ttl_in_seconds = exp_ts - iat_ts
        if raw:
            app.echo_info_json(ttl_in_seconds)
            return
        exp_time = datetime.fromtimestamp(exp_ts, tz=timezone.utc)
        now_time = datetime.now(tz=timezone.utc)
        ttl_delta = timeago.format(exp_time, now_time)
        if ttl_delta.startswith("in"):
            app.echo_info(
                f"The provided access token will expire {ttl_delta} "
                f"(TTL is {ttl_in_seconds} seconds)."
            )
        else:
            app.echo_info(
                f"The provided access token expired {ttl_delta} (TTL was {ttl_in_seconds} seconds)."
            )
        return
    if decode:
        if raw:
            app.echo_info_json(decoded_token)
            return
        table = struct_to_table(decoded_token)
        app.echo_info_table(table, headers=["Key", "Value"], sort_column=0)
        return
    if raw:
        app.echo_info_json(get_token())
        return
    app.echo_info(token)


@click.group(cls=CmemcGroup)
def admin() -> CmemcGroup:  # type: ignore[empty-body]
    """Import bootstrap data, backup/restore workspace or get status.

    This command group consists of commands for setting up and
    configuring eccenca Corporate Memory.
    """


admin.add_command(status_command)
admin.add_command(token_command)
admin.add_command(metrics)
admin.add_command(workspace)
admin.add_command(store)
admin.add_command(user)
admin.add_command(acl)
admin.add_command(client)
admin.add_command(migration)
