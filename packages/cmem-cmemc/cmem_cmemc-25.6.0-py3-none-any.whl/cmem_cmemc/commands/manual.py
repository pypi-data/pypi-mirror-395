"""manual command for cmem command line interface"""

import click
from click import Context, UsageError

from cmem_cmemc.command import CmemcCommand
from cmem_cmemc.manual_helper.graph import print_manual_graph
from cmem_cmemc.manual_helper.multi_page import create_multi_page_documentation
from cmem_cmemc.manual_helper.single_page import print_manual
from cmem_cmemc.parameter_types.path import ClickSmartPath
from cmem_cmemc.utils import get_version

FORMAT_MD_FILE = "markdown-single-page"
FORMAT_MD_DIRECTORY = "markdown-multi-page"
FORMAT_TURTLE_FILE = "turtle"


@click.command(cls=CmemcCommand, name="manual", hidden=True)
@click.option(
    "--format",
    "format_",
    type=click.Choice([FORMAT_MD_FILE, FORMAT_MD_DIRECTORY, FORMAT_TURTLE_FILE]),
    help=f"Output format. The '{FORMAT_TURTLE_FILE}' and '{FORMAT_MD_FILE}' formats will "
    f"be returned to stdout. The '{FORMAT_MD_DIRECTORY}' format creates a directory tree "
    f"(use '--output-dir' to specify the root directory)",
)
@click.option(
    "--output-dir",
    type=ClickSmartPath(writable=True, file_okay=False),
    help=f"The output directory to create the '{FORMAT_MD_DIRECTORY}' documentation. "
    f"Warning: Existing directories will be overwritten.",
)
@click.pass_context
def manual_command(ctx: Context, format_: str, output_dir: str) -> None:
    """Generate reference documentation assets.

    This command generates the cmemc reference documentation from the help texts
    and outputs it in different formats.
    """
    if format_ is None:
        raise UsageError(
            "Please use the --format option to specify an output format. "
            "Use --help for more information."
        )
    if format_ == FORMAT_TURTLE_FILE:
        print_manual_graph(ctx.find_root(), get_version())
        return
    if format_ == FORMAT_MD_FILE:
        print_manual(ctx.find_root())
        return
    if output_dir is None:
        raise UsageError(
            f"The output format '{FORMAT_MD_DIRECTORY}' needs an output directory "
            f"('--output-dir'). Use --help for more information."
        )
    create_multi_page_documentation(ctx.find_root(), str(output_dir))
