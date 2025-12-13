"""migrations command group"""

from typing import TYPE_CHECKING

import click
from click import Argument, Context
from click.shell_completion import CompletionItem

from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.completion import check_option_in_params, finalize_completion
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.migrations.access_conditions_243 import (
    MoveAccessConditionsToNewGraph,
    RenameAuthVocabularyResources,
)
from cmem_cmemc.migrations.bootstrap_data import MigrateBootstrapData
from cmem_cmemc.migrations.remove_noop_triple_251 import RemoveHideHeaderFooterStatements
from cmem_cmemc.migrations.shapes_widget_integrations_243 import (
    ChartsOnNodeShapesToToWidgetIntegrations,
    ChartsOnPropertyShapesToWidgetIntegrations,
    TableReportPropertyShapesToWidgetIntegrations,
    WorkflowTriggerPropertyShapesToWidgetIntegrations,
)
from cmem_cmemc.migrations.sparql_query_texts_242 import SparqlDatatypesToXsdString
from cmem_cmemc.migrations.workspace_configurations import MigrateWorkspaceConfiguration
from cmem_cmemc.object_list import (
    DirectListPropertyFilter,
    DirectValuePropertyFilter,
    ObjectList,
    compare_regex,
    transform_lower,
)

if TYPE_CHECKING:
    from cmem_cmemc.migrations.abc import MigrationRecipe


def get_migrations(ctx: click.Context) -> list[dict]:  # noqa: ARG001
    """Get users for object list"""
    data = [
        {
            "id": _.id,
            "description": _.description,
            "component": _.component,
            "first_version": _.first_version,
            "last_version": _.last_version,
            "tags": _.tags,
            "object": _,
        }
        for _ in [
            MoveAccessConditionsToNewGraph(),
            RenameAuthVocabularyResources(),
            MigrateBootstrapData(),
            MigrateWorkspaceConfiguration(),
            ChartsOnNodeShapesToToWidgetIntegrations(),
            ChartsOnPropertyShapesToWidgetIntegrations(),
            WorkflowTriggerPropertyShapesToWidgetIntegrations(),
            TableReportPropertyShapesToWidgetIntegrations(),
            SparqlDatatypesToXsdString(),
            RemoveHideHeaderFooterStatements(),
        ]
    ]
    data.sort(key=lambda x: x["first_version"])
    return data


def complete_migration_ids(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:
    """Prepare a list of migration recipe IDs"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    options = []
    for _ in get_migrations(ctx=ctx):
        id_ = _["id"]
        description = _["description"]
        if check_option_in_params(id_, ctx.params.get(param.name)):  # type: ignore[attr-defined, arg-type]
            continue
        options.append((id_, description))
    return finalize_completion(candidates=options, incomplete=incomplete)


migrations_list = ObjectList(
    name="migration recipes",
    get_objects=get_migrations,
    filters=[
        DirectValuePropertyFilter(
            name="id",
            description="Filter migrations by id.",
            property_key="id",
            transform=transform_lower,
        ),
        DirectValuePropertyFilter(
            name="description",
            description="Filter migrations by regex over description.",
            property_key="description",
            compare=compare_regex,
            fixed_completion=[],
        ),
        DirectValuePropertyFilter(
            name="first_version",
            description="Filter migrations by first version which is target of this migration.",
            property_key="first_version",
            transform=transform_lower,
        ),
        DirectListPropertyFilter(
            name="tag",
            description="Filter migrations by tags",
            property_key="tags",
        ),
    ],
)


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    multiple=True,
    help=migrations_list.get_filter_help_text(),
    shell_complete=migrations_list.complete_values,
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists only IDs. This is useful for piping the IDs into other commands.",
)
@click.option("--raw", is_flag=True, help="Outputs raw JSON.")
@click.pass_context
def list_command(
    ctx: click.Context, filter_: tuple[tuple[str, str]], id_only: bool, raw: bool
) -> None:
    """List migration recipies.

    This command lists all available migration recipies
    """
    app: ApplicationContext = ctx.obj
    data = migrations_list.apply_filters(ctx=ctx, filter_=filter_)
    if raw:
        # https://stackoverflow.com/questions/17665809/
        app.echo_info_json([(_, _.pop("object"))[0] for _ in data])
        return
    if id_only:
        for _ in sorted([_.get("id") for _ in data]):
            app.echo_info(_)
        return

    table = [
        [
            _.get("id"),
            _.get("description"),
            ", ".join(sorted(_.get("tags"))),
            f"{_.get('first_version')} ({_.get('component')})",
        ]
        for _ in data
    ]
    app.echo_info_table(
        table,
        headers=["ID", "Description", "Tags", "First Version"],
        sort_column=3,
        caption=f"{len(table)} migration(s)",
        empty_table_message="No migrations available.",
    )


@click.command(cls=CmemcCommand, name="execute")
@click.argument(
    "migration_id", type=click.STRING, required=False, shell_complete=complete_migration_ids
)
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    multiple=True,
    help=migrations_list.get_filter_help_text(),
    shell_complete=migrations_list.complete_values,
)
@click.option(
    "-a",
    "--all",
    "all_",
    is_flag=True,
    help="Execute all needed migrations.",
)
@click.option("--test-only", is_flag=True, help="Only test, do not execute migrations.")
@click.option("--id-only", is_flag=True, help="Lists only recipe identifier. ")
@click.pass_context
def execute_command(  # noqa: PLR0913
    ctx: click.Context,
    migration_id: str,
    filter_: tuple[tuple[str, str]],
    all_: bool,
    test_only: bool,
    id_only: bool,
) -> None:
    """Execute needed migration recipes.

    This command executes one or more migration recipes.
    Each recipe has a check method to determine if a migration is needed.
    In addition to that, the current component version needs to match the specified
    first-last-version range of the recipe.

    Recipes are executed ordered by first_version.

    Here are some argument examples, in order to see how to use this command:
    execute --all --test-only will list all needed migrations (but not execute them),
    execute --filter tag system will apply all migrations which target system data,
    execute bootstrap-data will apply bootstrap-data migration if needed.
    """
    app: ApplicationContext = ctx.obj
    if not all_ and not migration_id and not filter_:
        raise click.UsageError(
            "You can execute a single recipe, some recipes based on filter, or all recipes. "
            "See the documentation for more information."
        )
    data = migrations_list.apply_filters(ctx=ctx, filter_=filter_)
    if migration_id:
        data = migrations_list.apply_filters(ctx=ctx, filter_=[("id", migration_id)])
        if not data:
            raise click.UsageError(
                f"Migration recipe '{migration_id}' not found. "
                "Use the 'migration list' command to get available migration recipes."
            )
    applied_counter = 0
    for _ in data:
        recipe: MigrationRecipe = _.get("object")
        if not recipe.version_matches():
            app.echo_debug(f"Migration '{recipe.id}' does not match component version.")
            continue
        if not recipe.is_applicable():
            app.echo_debug(f"Migration '{recipe.id}' is not applicable.")
            continue
        app.echo_debug(f"Migration '{recipe.id}' could be applied.")
        applied_counter += 1

        app.echo_info(recipe.id, condition=id_only)
        app.echo_info(f"{recipe.description} ({recipe.id}) ... ", nl=False, condition=not id_only)
        if test_only:
            app.echo_warning("needed", condition=not id_only)
            continue
        recipe.apply()
        app.echo_success("done", condition=not id_only)
    app.echo_success("No migration needed.", condition=(not applied_counter and not id_only))


@click.group(cls=CmemcGroup)
def migration() -> CmemcGroup:  # type: ignore[empty-body]
    """List and apply migration recipes.

    With this command group, you can check your instance for needed
    migration activities as well as apply them to your data.

    Beside an ID and a description, migration recipes have the following
    metadata: 'First Version' is the first Corporate Memory version,
    where this recipe is maybe applicable. The recipe will never be applied
    to a version below this version. 'Tags' is a classification of the recipe
    with regard to the target data, it migrates.

    The following tags are important:
    `system` recipes target data structures
    which are needed to run the most basic functionality properly. These recipes
    can and should be applied after each version upgrade.
    `user` recipes can change user and / or customizing data.
    `acl` recipes migrate access condition data.
    `shapes` recipes migrate shape data.
    `config` recipes migrate configuration data.
    """


migration.add_command(list_command)
migration.add_command(execute_command)
