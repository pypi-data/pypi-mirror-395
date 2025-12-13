"""Generate a single page documentation Markdown."""

import click


def print_manual(ctx: click.core.Context) -> None:
    """Output the complete manual.

    Returns: None
    """
    ctx.obj.echo_info(
        """# Command Reference

This section lists the help texts of all commands as a reference
and to search for it.
"""
    )
    print_group_manual_recursive(ctx.command, ctx=ctx)


def print_group_manual_recursive(
    command_group: click.Command | click.Group, ctx: click.core.Context, prefix: str = ""
) -> None:
    """Output the help text of a command group (recursive)."""
    commands = command_group.commands  # type: ignore[union-attr]
    for key in commands:
        if key == "manual":
            continue
        command = commands[key]
        formatter = ctx.make_formatter()
        if isinstance(command, click.Group):
            ctx.obj.echo_info(f"## Command group: {prefix}{key}\n")
            ctx.obj.echo_info("```")
            command.format_help(ctx, formatter)
            ctx.obj.echo_info(formatter.getvalue().rstrip("\n"))
            ctx.obj.echo_info("```\n")

            print_group_manual_recursive(command, ctx=ctx, prefix=f"{prefix}{key} ")
        elif isinstance(command, click.Command):
            ctx.obj.echo_info(f"### Command: {prefix}{key}\n")
            ctx.obj.echo_info("```text")
            command.format_help(ctx, formatter)
            ctx.obj.echo_info(formatter.getvalue().rstrip("\n"))
            ctx.obj.echo_info("```\n")
        else:
            pass
