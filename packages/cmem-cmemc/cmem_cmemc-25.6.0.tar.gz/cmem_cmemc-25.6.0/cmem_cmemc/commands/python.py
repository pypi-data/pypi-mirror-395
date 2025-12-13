"""Build (DataIntegration) python management commands."""

import sys
from dataclasses import asdict
from re import match

import click
from click import ClickException, UsageError
from cmem.cmempy.workspace.python import (
    install_package_by_file,
    install_package_by_name,
    list_packages,
    list_plugins,
    uninstall_package,
    update_plugins,
)

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.utils import get_published_packages


def _get_package_id(module_name: str) -> str:
    """Return package identifier."""
    return module_name.split(".")[0].replace("_", "-")


def _looks_like_a_package(package: str) -> bool:
    """Check if a string looks like a package requirement string."""
    return bool(match("^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*((==|<=|>=|>|<).*)?$", package))


@click.command(cls=CmemcCommand, name="install")
@click.argument(
    "PACKAGE",
    shell_complete=completion.installable_packages,
    type=ClickSmartPath(readable=True, allow_dash=False, dir_okay=False),
)
@click.pass_obj
def install_command(app: ApplicationContext, package: str) -> None:
    """Install a python package to the workspace.

    This command is essentially a `pip install` in the remote python
    environment.

    You can install a package by uploading a source distribution
    .tar.gz file, by uploading a build distribution .whl file, or by
    specifying a package name, i.e., a pip requirement specifier with a
    package name available on pypi.org (e.g. `requests==2.27.1`).

    Note: The tab-completion of this command lists only public packages from
    pypi.org and not from additional or changed python package repositories you
    may have configured on the server.
    """
    app.echo_info(f"Install package {package} ... ", nl=False)
    try:
        install_response = install_package_by_file(package_file=package)
    except FileNotFoundError as not_found_error:
        if not _looks_like_a_package(package):
            raise ClickException(
                f"{package} does not look like a package name or requirement "
                "string, and a file with this name also does not exists."
            ) from not_found_error
        install_response = install_package_by_name(package_name=package)

    # DI >= 24.1 has a combine 'output' key, before 24.1 'standardOutput' and 'errorOutput' existed
    install_output: list[str] = []
    install_output.extend(install_response.get("output", "").splitlines())
    install_output.extend(install_response.get("standardOutput", "").splitlines())
    install_output.extend(install_response.get("errorOutput", "").splitlines())
    app.echo_debug(install_output)

    update_plugin_response = update_plugins()
    app.echo_debug(f"Updated Plugins: {update_plugin_response!s}")
    update_errors = update_plugin_response.get("errors", [])
    if install_response["success"] is True and len(update_errors) == 0:
        app.echo_success("done")
        return

    # something went wrong
    app.echo_error("error")
    app.echo_error(install_output, prepend_line=True)
    for update_error in update_errors:
        app.echo_error(
            f"Error while updating the plugins of "
            f"{update_error.get('packageName')}: {update_error.get('errorMessage')} "
            f"({update_error.get('errorType')})",
            prepend_line=True,
        )
        app.echo_error(update_error.get("stackTrace"))
    sys.exit(1)


@click.command(cls=CmemcCommand, name="uninstall")
@click.argument("PACKAGE_NAME", nargs=-1, shell_complete=completion.installed_package_names)
@click.option(
    "-a",
    "--all",
    "all_",
    is_flag=True,
    help="This option removes all installed packages from the system,"
    " leaving only the pre-installed mandatory packages in the environment.",
)
@click.pass_obj
def uninstall_command(app: ApplicationContext, package_name: str, all_: bool) -> None:
    """Uninstall a python packages from the workspace.

    This command is essentially a `pip uninstall` in the remote
    python environment.
    """
    if all_:
        app.echo_info("Wiping Python environment ... ", nl=False)
        uninstall_package(package_name="--all")
        app.echo_success("done")
        app.echo_debug("Updated Plugins: " + str(update_plugins()))
        return

    if not package_name:
        raise UsageError(
            "Either give at least one package name or wipe the whole python"
            " environment with the '--all' option."
        )
    packages = list_packages()
    app.echo_debug(packages)
    for _ in package_name:
        app.echo_info(f"Uninstall package {_} ... ", nl=False)
        if _ not in [package["name"] for package in packages]:
            app.echo_error("not installed")
            app.echo_debug("Updated Plugins: " + str(update_plugins()))
            sys.exit(1)
        response = uninstall_package(package_name=_)
        output: list[str] = []
        output.extend(response.get("output", "").splitlines())
        output.extend(response.get("standardOutput", "").splitlines())
        output.extend(response.get("errorOutput", "").splitlines())
        for output_line in output:
            app.echo_debug(output_line)
        if response["success"]:
            app.echo_success("done")
        else:
            app.echo_error("error")
            app.echo_debug(response.content.decode())
    app.echo_debug("Updated Plugins: " + str(update_plugins()))


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only package identifier. " "This is useful for piping the IDs into other commands.",
)
@click.option(
    "--available",
    is_flag=True,
    help="Instead of listing installed packages, this option lists installable packages"
    " from pypi.org, which are prefixed with 'cmem-plugin-' and so are most likely"
    " Corporate Memory plugin packages.",
)
@click.pass_obj
def list_command(app: ApplicationContext, raw: bool, id_only: bool, available: bool) -> None:
    """List installed python packages.

    This command is essentially a `pip list` in the remote python environment.

    It outputs a table of python package identifiers with version information.
    """
    if available:
        published_packages = get_published_packages()

        if raw:
            app.echo_info_json([asdict(_) for _ in published_packages])
            return

        if id_only:
            for _ in published_packages:
                app.echo_info(_.name)
            return

        table_published = [
            (_.name, _.version, str(_.published)[:10], _.description) for _ in published_packages
        ]
        app.echo_info_table(
            table_published,
            headers=["Name", "Version", "Published", "Description"],
            sort_column=0,
            empty_table_message="No available python packages found.",
        )
        return

    installed_packages = list_packages()
    if raw:
        app.echo_info_json(installed_packages)
        return

    if id_only:
        for package in installed_packages:
            app.echo_info(package["name"])
        return

    table_installed = [(_["name"], _["version"]) for _ in installed_packages]
    app.echo_info_table(
        table_installed,
        headers=["Name", "Version"],
        sort_column=0,
        empty_table_message="No installed python packages found."
        "Most likely, this is due to a wrong deployment.",
    )


@click.command(cls=CmemcCommand, name="list-plugins")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.option("--id-only", is_flag=True, help="Lists only plugin identifier.")
@click.option("--package-id-only", is_flag=True, help="Lists only plugin package identifier.")
@click.pass_obj
def list_plugins_command(
    app: ApplicationContext, raw: bool, id_only: bool, package_id_only: bool
) -> None:
    """List installed workspace plugins.

    This commands lists all discovered plugins.

    Note: The plugin discovery is restricted to package prefix (`cmem-`).
    """
    raw_output = list_plugins()
    try:
        plugins = raw_output["plugins"]  # DI >= 22.1.1 output
    except TypeError:
        plugins = raw_output  # DI <= 22.1 output

    if not all(plugin.get("isRegistered", True) for plugin in plugins):
        app.echo_warning(
            "Some plugins are installed but not registered. "
            "Use the 'admin workspace python reload' command to register all installed plugins."
        )

    if raw:
        app.echo_info_json(plugins)
        return

    if id_only:
        for plugin in sorted(plugins, key=lambda k: k["id"].lower()):
            app.echo_info(plugin["id"])
        return

    if package_id_only:
        package_ids = set()
        for plugin in plugins:
            package_ids.add(_get_package_id(plugin["moduleName"]))
        for package_id in sorted(package_ids):
            app.echo_info(package_id)
        return

    table = [
        (
            _["id"],
            _get_package_id(_["moduleName"]),
            _["pluginType"],
            _["label"],
        )
        for _ in sorted(plugins, key=lambda k: k["id"].lower())
    ]
    app.echo_info_table(
        table,
        headers=["ID", "Package ID", "Type", "Label"],
        sort_column=0,
        empty_table_message="No plugins found. "
        "Use the `admin workspace python install` command to install python packages with plugins.",
    )
    if "error" in raw_output:
        app.echo_error(raw_output["error"])


@click.command(cls=CmemcCommand, name="open")
@click.argument(
    "PACKAGE",
    shell_complete=completion.published_package_names,
)
@click.pass_obj
def open_command(app: ApplicationContext, package: str) -> None:
    """Open a package pypi.org page in the browser.

    With this command, you can open the pypi.org page of a published package in your
    browser. From there, you can follow links, review the version history as well
    as the origin of the package, and read the provided documentation.
    """
    full_url = f"https://pypi.org/project/{package}/"
    app.echo_debug(f"Open {package}: {full_url}")
    click.launch(full_url)


@click.command(cls=CmemcCommand, name="reload")
@click.pass_obj
def reload_command(app: ApplicationContext) -> None:
    """Reload / Register all installed plugins.

    This command will register all installed plugins into the Build
    (DataIntegration) workspace.
    This command is useful, when you are installing packages
    into the Build Python environment without using the provided cmemc
    commands (e.g. by mounting a prepared filesystem in the docker container).
    """
    app.echo_info("Reloading python packages ... ", nl=False)
    update_plugin_response = update_plugins()
    app.echo_debug(f"Updated Plugins: {update_plugin_response!s}")
    update_errors = update_plugin_response.get("errors", [])
    if len(update_errors) == 0:
        app.echo_success("done")
    else:
        app.echo_error("error (use --debug for more information)")


@click.group(cls=CmemcGroup)
def python() -> CmemcGroup:  # type: ignore[empty-body]
    """List, install, or uninstall python packages.

    Python packages are used to extend the Build (DataIntegration) workspace
    with python plugins. To get a list of installed packages, execute the
    list command.

    Warning: Installing packages from unknown sources is not recommended.
    Plugins are not verified for malicious code.
    """


python.add_command(install_command)
python.add_command(uninstall_command)
python.add_command(list_command)
python.add_command(list_plugins_command)
python.add_command(open_command)
python.add_command(reload_command)
