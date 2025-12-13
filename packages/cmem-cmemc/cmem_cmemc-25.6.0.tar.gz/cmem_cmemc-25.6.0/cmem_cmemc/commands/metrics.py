"""metrics commands for cmem command line interface."""

import click
from click import Argument, ClickException, Context, UsageError
from click.shell_completion import CompletionItem
from cmem.cmempy.api import request
from cmem.cmempy.config import get_cmem_base_uri, get_di_api_endpoint, get_dp_api_endpoint
from prometheus_client.parser import text_string_to_metric_families
from requests import HTTPError

from cmem_cmemc import completion
from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.command_group import CmemcGroup
from cmem_cmemc.context import ApplicationContext
from cmem_cmemc.object_list import (
    DirectValuePropertyFilter,
    ObjectList,
    compare_regex,
    compare_str_equality,
)
from cmem_cmemc.utils import (
    metric_get_labels,
    struct_to_table,
)


def get_all_metrics(ctx: click.Context) -> list[dict]:
    """Get metrics data for object list"""
    known_metrics_urls: list[tuple[str, str]] = [
        ("explore", get_dp_api_endpoint() + "/actuator/prometheus"),
        ("build", get_di_api_endpoint() + "/metrics"),
        ("store", get_dp_api_endpoint() + "/actuator/proxy/graphdb/metrics/structures"),
        ("store", get_dp_api_endpoint() + "/actuator/proxy/graphdb/metrics/infrastructure"),
        ("store", get_dp_api_endpoint() + "/actuator/proxy/graphdb/metrics/cluster"),
        ("store", get_dp_api_endpoint() + "/actuator/proxy/graphdb/metrics/repository/cmem"),
    ]
    app: ApplicationContext = ctx.obj
    all_metrics: list[dict] = []
    for job, url in known_metrics_urls:
        try:
            families = text_string_to_metric_families(request(url).text)
        except HTTPError as error:
            if app is not None:
                # when in completion mode, obj is not set :-(
                app.echo_debug(str(error))
            continue
        for family in families:
            documentation = family.documentation
            if documentation == "":
                documentation = f"No documentation available for {job}:{family.name}"
            new_metric = {
                "id": f"{job}:{family.name}",
                "job": job,
                "name": family.name,
                "type": family.type,
                "documentation": documentation,
                "labels": metric_get_labels(family),
                "samples": family.samples,
                # "object": family
            }
            if family.type not in ("unknown", "histogram"):
                all_metrics.append(new_metric)
    return all_metrics


metrics_list = ObjectList(
    name="metrics",
    get_objects=get_all_metrics,
    filters=[
        DirectValuePropertyFilter(
            name="job",
            description="Filter metrics by job ID.",
            property_key="job",
        ),
        DirectValuePropertyFilter(
            name="name",
            description="Filter metrics by regex matching the name.",
            property_key="name",
            compare=compare_regex,
            fixed_completion=[],
        ),
        DirectValuePropertyFilter(
            name="type",
            description="Filter metrics by type.",
            property_key="type",
        ),
        DirectValuePropertyFilter(
            name="id",
            description="Filter metrics by ID.",
            property_key="id",
            compare=compare_str_equality,
        ),
    ],
)


def _complete_metrics_id(ctx: Context, param: Argument, incomplete: str) -> list[CompletionItem]:  # noqa: ARG001
    """Prepare a list of metric identifier."""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    candidates = [(_["id"], _["documentation"]) for _ in metrics_list.apply_filters(ctx=ctx)]
    return completion.finalize_completion(candidates=candidates, incomplete=incomplete)


def _complete_metric_label_filter(
    ctx: Context,
    param: Argument,  # noqa: ARG001
    incomplete: str,
) -> list[CompletionItem]:
    """Prepare a list of label name or values"""
    ApplicationContext.set_connection_from_params(ctx.find_root().params)
    args = completion.get_completion_args(incomplete)
    incomplete = incomplete.lower()
    options: list[str] = []
    try:
        metric_id = ctx.args[0]
        metric = metrics_list.apply_filters(ctx=ctx, filter_=[("id", metric_id)])[0]
    except IndexError:
        # means: --filter is used before we have a metrics ID
        return []
    labels = metric["labels"]
    if args[len(args) - 1] in "--filter":
        # we are in the name position
        options = list(labels.keys())
    if args[len(args) - 2] in "--filter":
        label_name = args[len(args) - 1]
        # we are in the value position
        options = labels[label_name]
    return completion.finalize_completion(candidates=options, incomplete=incomplete)


def _filter_samples(family: dict, label_filter: tuple[tuple[str, str], ...]) -> list:
    """Filter samples by labels."""
    family_name = family.get("name")
    all_samples: list[list] = family["samples"]
    if not label_filter:
        return all_samples
    labels: dict[str, list[str]] = family["labels"]
    samples = []
    for sample in all_samples:
        matching_labels = 0
        sample_labels = sample[1]
        for name, value in label_filter:
            if name not in labels:
                raise ClickException(
                    f"The metric '{family_name}' does " f"not have a label named '{name}'."
                )
            if value not in labels[name]:
                raise ClickException(
                    f"The metric '{family_name}' does "
                    f"not have a label '{name}' with the value '{value}'."
                )
            if name in sample_labels and sample_labels[name] == value:
                matching_labels += 1
        if matching_labels == len(label_filter):
            # all filter match
            samples.append(sample)
    return samples


# pylint: disable-msg=too-many-arguments
@click.command(cls=CmemcCommand, name="get")
@click.argument("metric_id", required=True, type=click.STRING, shell_complete=_complete_metrics_id)
@click.option(
    "--filter",
    "label_filter",
    type=(str, str),
    shell_complete=_complete_metric_label_filter,
    multiple=True,
    help="A set of label name/value pairs in order to filter the samples "
    "of the requested metric family. Each metric has a different set "
    "of labels with different values. "
    "In order to get a list of possible label names and values, use "
    "the command without this option. The label names are then shown "
    "as column headers and label values as cell values of this column.",
)
@click.option(
    "--enforce-table",
    is_flag=True,
    help="A single sample value will be returned as plain text instead "
    "of the normal table. This allows for more easy integration "
    "with scripts. This flag enforces the use of tabular output, "
    "even for single row tables.",
)
@click.option("--raw", is_flag=True, help="Outputs raw prometheus sample classes.")
@click.pass_context
def get_command(
    ctx: click.Context,
    metric_id: str,
    label_filter: tuple[tuple[str, str], ...],
    raw: bool,
    enforce_table: bool,
) -> None:
    """Get sample data of a metric.

    A metric of a specific job is identified by a metric ID. Possible
    metric IDs of a job can be retrieved with the `metrics list`
    command. A metric can contain multiple samples.
    These samples are distinguished by labels (name and value).
    """
    app = ctx.obj
    data = metrics_list.apply_filters(ctx=ctx, filter_=[("id", metric_id)])
    if len(data) == 0:
        raise UsageError(
            f"No metric with ID '{metric_id}' found. "
            "Use the `metrics list` command to list all metrics."
        )
    if len(data) > 1:
        raise UsageError("Unknown Error - More than one metric with ID '{metric_id}' found.")
    metric = data[0]

    samples = _filter_samples(metric, label_filter)
    if raw:
        app.echo_info_json(samples)
        return

    if len(samples) == 0:
        raise ClickException(
            "No data - the given label combination filtered out "
            f"all available samples of the metric {metric_id}."
        )

    if len(samples) == 1 and enforce_table is not True:
        app.echo_info(str(samples[0].value))
        return

    label_dict = metric["labels"]
    table = []
    for sample in samples:
        row = [sample.labels[key] for key in sorted(label_dict.keys())]
        table.append(row)
        row.append(str(sample.value))
    headers = sorted(label_dict.keys())
    headers.append("value")
    app.echo_info_table(table, headers=headers, sort_column=0)


@click.command(cls=CmemcCommand, name="inspect")
@click.argument("metric_id", required=True, type=click.STRING, shell_complete=_complete_metrics_id)
@click.option("--raw", is_flag=True, help="Outputs raw JSON of the table data.")
@click.pass_context
def inspect_command(ctx: Context, metric_id: str, raw: bool) -> None:
    """Inspect a metric.

    This command outputs the data of a metric.
    The first table includes basic metadata about the metric.
    The second table includes sample labels and values.
    """
    app = ctx.obj
    data = metrics_list.apply_filters(ctx=ctx, filter_=[("id", metric_id)])
    if len(data) == 0:
        raise UsageError(
            f"No metric with ID '{metric_id}' found. "
            "Use the `metrics list` command to list all metrics."
        )
    if len(data) > 1:
        raise UsageError("Unknown Error - More than one metric with ID '{metric_id}' found.")
    if raw:
        app.echo_info_json(data)
        return
    app.echo_info_table(struct_to_table(data), headers=["Key", "Value"], sort_column=0)


@click.command(cls=CmemcCommand, name="list")
@click.option(
    "--filter",
    "filter_",
    type=(str, str),
    multiple=True,
    help=metrics_list.get_filter_help_text(),
    shell_complete=metrics_list.complete_values,
)
@click.option(
    "--id-only",
    is_flag=True,
    help="Lists metric identifier only. " "This is useful for piping the IDs into other commands.",
)
@click.option(
    "--raw", is_flag=True, help="Outputs (sorted) JSON dict, parsed from the metrics API output."
)
@click.pass_context
def list_command(
    ctx: click.Context, filter_: tuple[tuple[str, str]], id_only: bool, raw: bool
) -> None:
    """List metrics for a specific job.

    For each metric, the output table shows the metric ID,
    the type of the metric, a count of how many labels (label names)
    are describing the samples (L) and a count of how many samples are
    currently available for a metric (S).
    """
    app = ctx.obj
    data = metrics_list.apply_filters(ctx=ctx, filter_=filter_)
    if raw:
        app.echo_info_json(data)
        return
    if id_only:
        for _ in sorted([_.get("id") for _ in data]):
            app.echo_info(_)
        return

    table = [
        [
            _.get("id"),
            _.get("type"),
            len(_.get("labels")),
            len(_.get("samples")),
            _.get("documentation"),
        ]
        for _ in data
    ]
    app.echo_info_table(
        table,
        headers=["ID", "Type", "L", "S", "Documentation"],
        sort_column=0,
        caption=f"{len(table)} metrics families of {get_cmem_base_uri()}",
        empty_table_message="No metrics families available.",
    )


@click.group(cls=CmemcGroup)
def metrics() -> CmemcGroup:  # type: ignore[empty-body]
    """List and get metrics.

    This command group consists of commands for reading and listing
    internal monitoring metrics of eccenca Corporate Memory. A
    deployment consists of multiple jobs (e.g. DP, DI), which provide
    multiple metric families for an endpoint.

    Each metric family can consist of different samples identified by
    labels with a name and a value (dimensions). A metric has a specific
    type (counter, gauge, summary and histogram) and additional metadata.

    Please have a look at https://prometheus.io/docs/concepts/data_model/
    for further details.
    """


metrics.add_command(get_command)
metrics.add_command(inspect_command)
metrics.add_command(list_command)
