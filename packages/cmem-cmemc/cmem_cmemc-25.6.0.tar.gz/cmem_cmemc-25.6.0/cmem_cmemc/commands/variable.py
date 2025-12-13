"""Build (DataIntegration) variable commands for cmemc."""

import re

import click
from click import UsageError
from cmem.cmempy.workspace.projects.variables import (
    create_or_update_variable,
    delete_variable,
    get_all_variables,
    get_variable,
)

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.utils import check_or_select_project, split_task_id

VARIABLES_FILTER_TYPES = ["project", "regex"]
VARIABLES_FILTER_TYPES_HIDDEN = ["ids"]
VARIABLES_FILTER_TEXT = (
    "Filter variables based on metadata. "
    f"First parameter CHOICE can be one of {VARIABLES_FILTER_TYPES!s}"
    ". The second parameter is based on CHOICE, e.g. a project "
    "ID or a regular expression string."
)


def _get_variables_filtered(
    variables: list[dict], filter_name: str, filter_value: str
) -> list[dict]:
    """Get variables but filtered according to name and value."""
    filter_types = VARIABLES_FILTER_TYPES + VARIABLES_FILTER_TYPES_HIDDEN
    # check for correct filter names (filter ids is used internally only)
    if filter_name not in filter_types:
        raise UsageError(
            f"{filter_name} is an unknown filter name. " f"Use one of {VARIABLES_FILTER_TYPES}."
        )
    # filter by ID list
    if filter_name == "ids":
        return [_ for _ in variables if _["id"] in filter_value]
    # filter by project
    if filter_name == "project":
        return [_ for _ in variables if _["project"] == filter_value]
    # filter by regex
    if filter_name == "regex":
        return [
            _
            for _ in variables
            if re.search(filter_value, _["id"])
            or re.search(filter_value, _["value"])
            or re.search(filter_value, _.get("description", ""))
            or re.search(filter_value, _.get("template", ""))
        ]
    # return unfiltered list
    return variables


@click.command(cls=CmemcCommand, name="list")
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only variables names and no other metadata. "
    "This is useful for piping the IDs into other commands.",
)
@click.option(
    "--filter",
    "filters_",
    multiple=True,
    type=(str, str),
    shell_complete=completion.variable_list_filter,
    help=VARIABLES_FILTER_TEXT,
)
@click.pass_obj
def list_command(
    app: ApplicationContext, raw: bool, id_only: bool, filters_: tuple[tuple[str, str]]
) -> None:
    """List available project variables.

    Outputs a table or a list of project variables.
    """
    variables = get_all_variables()

    for _ in filters_:
        filter_name, filter_value = _
        variables = _get_variables_filtered(variables, filter_name, filter_value)
    if raw:
        app.echo_info_json(variables)
        return
    if id_only:
        for _ in sorted(_["id"] for _ in variables):
            app.echo_result(_)
        return
    # output a user table
    table = []
    headers = ["ID", "Value", "Template", "Description"]
    for _ in variables:
        row = [
            _["id"],
            _["value"],
            _.get("template", ""),
            _.get("description", ""),
        ]
        table.append(row)
    app.echo_info_table(
        table,
        headers=headers,
        sort_column=0,
        empty_table_message="No project variables found. "
        "Use the `project variable create` command to create a new project variable.",
    )


@click.command(cls=CmemcCommand, name="get")
@click.argument(
    "variable_id", required=True, type=click.STRING, shell_complete=completion.variable_ids
)
@click.option(
    "--key",
    type=click.Choice(["value", "template", "description"], case_sensitive=False),
    default="value",
    show_default=True,
    help="Specify the name of the value you want to get.",
)
@click.option("--raw", is_flag=True, help="Outputs raw json.")
@click.pass_obj
def get_command(app: ApplicationContext, variable_id: str, key: str, raw: bool) -> None:
    """Get the value or other data of a project variable.

    Use the `--key` option to specify which information you want to get.

    Note: Only the `value` key is always available on a project variable.
    Static value variables have no `template` key, and the `description` key
    is optional for both types of variables.
    """
    project_name, variable_name = split_task_id(variable_id)
    _ = get_variable(variable_name=variable_name, project_name=project_name)
    if raw:
        app.echo_info_json(_)
        return
    try:
        app.echo_info(_[key], nl=False)
    except KeyError as error:
        raise UsageError(f"Variable {variable_name} has no value of '{key}'.") from error


@click.command(cls=CmemcCommand, name="delete")
@click.argument(
    "variable_id", required=True, type=click.STRING, shell_complete=completion.variable_ids
)
@click.pass_obj
def delete_command(app: ApplicationContext, variable_id: str) -> None:
    """Delete a project variable.

    Note: You can not delete a variable which is used by another
    (template based) variable. In order to do so, delete the template based
    variable first.
    """
    project_name, variable_name = split_task_id(variable_id)
    app.echo_info(f"Delete variable {variable_name} from project {project_name} ... ", nl=False)
    delete_variable(variable_name=variable_name, project_name=project_name)
    app.echo_success("done")


# pylint: disable=too-many-arguments
@click.command(cls=CmemcCommand, name="create")
@click.argument(
    "variable_name",
    required=True,
    type=click.STRING,
)
@click.option("--value", type=click.STRING, help="The value of the new project variable.")
@click.option(
    "--template",
    type=click.STRING,
    help="The template of the new project variable. You can use Jinja template "
    "syntax, e.g. use '{{global.myVar}}' for accessing global variables, or "
    "'{{project.myVar}}' for accessing variables from the same project.",
)
@click.option(
    "--description", type=click.STRING, help="The optional description of the new project variable."
)
@click.option(
    "--project",
    "project_id",
    type=click.STRING,
    shell_complete=completion.project_ids,
    help="The project, where you want to create the variable in. If there is "
    "only one project in the workspace, this option can be omitted.",
)
@click.pass_obj
def create_command(  # noqa: PLR0913
    app: ApplicationContext,
    variable_name: str,
    value: str,
    template: str,
    description: str,
    project_id: str,
) -> None:
    """Create a new project variable.

    Variables need to be created with a value or a template (not both).
    In addition to that, a project ID and a name are mandatory.

    Example: cmemc project variable create my_var --project my_project --value abc

    Note: cmemc is currently not able to manage the order of the variables in a
    project. This means you have to create plain value variables in advance,
    before you can create template based variables, which access these values.
    """
    if value and template:
        raise UsageError("Either use '--value' or '--template' but not both.")
    if not value and not template:
        raise UsageError("Use '--value' or '--template' to create a new variable.")
    project_id = check_or_select_project(app, project_id)
    data = get_variable(project_name=project_id, variable_name=variable_name)
    if data:
        raise UsageError(f"Variable '{variable_name}' already exist in project '{project_id}'.")
    data = {"name": variable_name, "isSensitive": False, "scope": "project"}
    if value:
        data["value"] = value
    if template:
        data["template"] = template
    if description:
        data["description"] = description
    app.echo_info(f"Create variable {variable_name} in project {project_id} ... ", nl=False)
    create_or_update_variable(project_name=project_id, variable_name=variable_name, data=data)
    app.echo_success("done")


@click.command(cls=CmemcCommand, name="update")
@click.argument(
    "variable_id", required=True, type=click.STRING, shell_complete=completion.variable_ids
)
@click.option("--value", type=click.STRING, help="The new value of the project variable.")
@click.option(
    "--template",
    type=click.STRING,
    help="The new template of the project variable. You can use Jinja template "
    "syntax, e.g. use '{{global.myVar}}' for accessing global variables, or "
    "'{{project.myVar}}' for accessing variables from the same project.",
)
@click.option(
    "--description", type=click.STRING, help="The new description of the project variable."
)
@click.pass_obj
def update_command(
    app: ApplicationContext,
    variable_id: str,
    value: str,
    template: str,
    description: str,
) -> None:
    """Update data of an existing project variable.

    With this command you can update the value or the template, as well as the
    description of a project variable.

    Note: If you update the template of a static variable, it will be transformed
    to a template based variable. If you want to change the value of a template
    based variable, an error will be shown.
    """
    project_id, variable_name = split_task_id(variable_id)
    data = get_variable(project_name=project_id, variable_name=variable_name)
    if not data:
        raise UsageError(f"Variable '{variable_name}' does not exist in project '{project_id}'.")
    if value and template:
        raise UsageError(
            "Project variables are based on a static value or on a template, but not " "both."
        )
    if not value and not template and not description:
        raise UsageError(
            "Please specify what you want to update. "
            "Use at least one of the following options: "
            "'--value', '--template', '--description'."
        )
    if value:
        if data.get("template", None):
            raise UsageError("You can not change the value of a template based variable.")
        data["value"] = value
    if template:
        if not data.get("template", None):
            app.echo_warning(
                f"Variable '{variable_id}' will be converted from a "
                f"simple to a template based variable."
            )
        data["template"] = template
    if description:
        data["description"] = description
    app.echo_info(f"Update variable {variable_name} in project {project_id} ... ", nl=False)
    create_or_update_variable(project_name=project_id, variable_name=variable_name, data=data)
    app.echo_success("done")


@click.group(cls=CmemcGroup)
def variable() -> CmemcGroup:  # type: ignore[empty-body]
    """List, create, delete or get data from project variables.

    Project variables can be used in dataset and task parameters, and in the template
    transform operator.
    Variables are either based on a static value or based on a template.
    They may use templates that access globally configured
    variables or other preceding variables from the same project.

    Variables are identified by a VARIABLE_ID. To get a list of existing
    variables, execute the list command or use tab-completion.
    The VARIABLE_ID is a concatenation of a PROJECT_ID and a VARIABLE_NAME,
    such as `my-project:my-variable`.
    """


variable.add_command(list_command)
variable.add_command(get_command)
variable.add_command(delete_command)
variable.add_command(create_command)
variable.add_command(update_command)
