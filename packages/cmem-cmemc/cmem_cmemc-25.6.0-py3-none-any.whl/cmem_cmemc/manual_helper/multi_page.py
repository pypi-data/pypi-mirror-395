"""Generate a multi page documentation for documentation.eccenca.com."""

import re
from pathlib import Path

import click
from click import Command, Group

EDIT_NOTE = "<!-- This file was generated - DO NOT CHANGE IT MANUALLY -->"


def get_icon_for_command_group(full_name: str) -> str:
    """Return in mkdocs material icon term for a command group.

    To look for icons: https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/
    """
    return {
        "admin": "material/key-link",
        "admin acl": "material/server-security",
        "admin client": "material/account-cog",
        "admin metrics": "material/chart-line-variant",
        "admin migration": "material/database-arrow-up-outline",
        "admin store": "material/database-outline",
        "admin user": "material/account-cog",
        "admin workspace": "material/folder-multiple-outline",
        "admin workspace python": "material/language-python",
        "config": "material/cog-outline",
        "dataset": "eccenca/artefact-dataset",
        "project": "eccenca/artefact-project",
        "project file": "eccenca/artefact-file",
        "project variable": "material/variable-box",
        "query": "eccenca/application-queries",
        "graph": "eccenca/artefact-dataset-eccencadataplatform",
        "graph imports": "material/family-tree",
        "graph insights": "eccenca/graph-insights",
        "graph validation": "octicons/verified-16",
        "vocabulary": "eccenca/application-vocabularies",
        "vocabulary cache": "eccenca/application-vocabularies",
        "workflow": "eccenca/artefact-workflow",
        "workflow scheduler": "material/calendar",
    }.get(full_name, "octicons/cross-reference-24")


def get_tags_for_command_group(full_name: str) -> str:
    """Get list of tags for a command group name as markdown head section."""
    # pylint: disable=consider-using-join
    tags = {
        "admin": ["cmemc"],
        "admin metrics": ["cmemc"],
        "admin store": ["SPARQL", "cmemc"],
        "admin user": ["Keycloak", "Security", "cmemc"],
        "admin client": ["Keycloak", "Security", "cmemc"],
        "admin acl": ["Security", "cmemc"],
        "admin workspace": ["cmemc"],
        "admin workspace python": ["Python", "cmemc"],
        "config": ["Configuration", "cmemc"],
        "dataset": ["cmemc"],
        "project": ["Project", "cmemc"],
        "project file": ["Files", "cmemc"],
        "project variable": ["Variables", "cmemc"],
        "query": ["SPARQL", "cmemc"],
        "graph": ["KnowledgeGraph", "cmemc"],
        "graph imports": ["KnowledgeGraph", "cmemc"],
        "graph validation": ["KnowledgeGraph", "Validation", "cmemc"],
        "vocabulary": ["Vocabulary", "cmemc"],
        "vocabulary cache": ["Vocabulary", "cmemc"],
        "workflow": ["Workflow", "cmemc"],
        "workflow scheduler": ["Automate", "cmemc"],
    }.get(full_name, ["cmemc"])
    markdown = "tags:\n"
    for tag in tags:
        markdown += f"  - {tag}\n"
    return markdown


def get_enhanced_help_text_markdown(
    command_or_group: click.Command | click.Group, skip_first_line: bool = False
) -> str:
    """Add ammunition and code ticks where possible."""
    text = str(command_or_group.help)
    first_line = command_or_group.get_short_help_str(limit=200)
    help_text_ = ""
    for line in text.splitlines():
        if skip_first_line and line.strip().startswith(first_line):
            continue
        help_text_ = f"{help_text_}\n\n" if line == "" else f"{help_text_} {line.rstrip().strip()}"
    help_text = ""
    for _ in help_text_.splitlines():
        line = _
        line = line.strip()
        if line.startswith("Example:"):
            # add EXAMPLE as code
            line = line.replace("Example:", "$")
            line = f"""```shell-session title="Example"
{line}
```
"""
        elif line.startswith("Warning:"):
            # add WARNING admonition
            line = line.replace("Warning: ", "")
            line = f"""!!! warning
    {line}
"""
        elif line.startswith("Note:"):
            # add NOTE admonition
            line = line.replace("Note: ", "")
            line = f"""!!! note
    {line}
"""
        else:
            # plain - non-admonition text will get some auto code ticks

            # surround placeholder, such as {{xxx}} with code ticks (`)
            line = re.sub(r"({{[a-zA-Z\-]+}})", r"`\1`", line)
            # surround short options, such as -p, by code ticks (`)
            line = re.sub(r" (-[a-z])", r"`\1`", line)
            # surround options, such as --raw, by code ticks (`)
            line = re.sub(r"(--[a-z\-]+)", r"`\1`", line)
            # surround parameters, such as GRAPH_URI, by code ticks (`)
            line = re.sub(r"([A-Z]+(_[A-Z]+)+)", r"`\1`", line)
        help_text += f"{line}\n"
    return help_text


def get_commands_for_table_recursive(
    ctx: click.core.Context,
    command_group: click.Command | click.Group,
    table_data: list[dict],
    prefix: str,
    group_name: str,
) -> list[dict]:
    """Get flat list of dicts, representing a command each."""
    new_table_data: list[dict] = []
    commands = command_group.commands  # type: ignore[union-attr]
    for key in command_group.commands:  # type: ignore[union-attr]
        item = commands[key]
        if isinstance(item, Group):
            table_data = get_commands_for_table_recursive(
                ctx,
                item,
                table_data,
                f"{prefix} {group_name}".strip(),
                item.name,  # type: ignore[arg-type]
            )
            continue
        if isinstance(item, Command):
            command_name = item.name
            group_link = f"{prefix}/{group_name}/index.md".replace(" ", "/")
            group_link = group_link.removeprefix("/")
            command_anchor = f"{prefix}-{group_name}".replace(" ", "-")
            command_anchor += f"-{command_name}"
            command_anchor = command_anchor.removeprefix("-")
            command_link = f"{group_link}#{command_anchor}"
            new_command = {
                "command_name": command_name,
                "command_link": command_link,
                "group_name": f"{prefix} {group_name}".strip(),
                "group_link": group_link,
                "command_description": item.get_short_help_str(limit=200),
            }
            new_table_data.append(new_command)

    return table_data + new_table_data


def get_markdown_for_index(ctx: click.core.Context, commands: dict) -> str:
    """Create the Markdown text for the command reference index.md."""
    header_md = f"""---
title: "cmemc: Command Reference"
description: "This page lists all commands with its short descriptions."
icon: octicons/cross-reference-24
tags:
  - Reference
  - cmemc
---
# Command Reference
{EDIT_NOTE}

!!! info

    cmemc is organized as a tree of command groups, each with a set of
    commands. You can access the command groups in the table as well as in the
    navigation on the left. You can access the commands directly from the table
    or by visiting a command group page first.
"""
    # get commands
    table_data: list[dict] = []
    for key in commands:
        item = commands[key]
        if isinstance(item, Group):
            table_data = get_commands_for_table_recursive(ctx, item, table_data, "", item.name)  # type: ignore[arg-type]
    table_data = sorted(table_data, key=lambda d: d["group_name"])

    rows_string = ""
    for _ in table_data:
        rows_string += f"| [{_['group_name']}]({_['group_link']}) "
        rows_string += f"| [{_['command_name']}]({_['command_link']}) "
        rows_string += f"| {_['command_description']} |\n"
    commands_md = f"""
| Command Group | Command | Description |
| ------------: | :------ | :---------- |
{rows_string}
"""

    return header_md + commands_md


def create_multi_page_documentation(ctx: click.core.Context, directory: str) -> None:
    """Create a multipage reference manual for documentation.eccenca.com.

    Returns: None
    """
    commands = ctx.command.commands  # type: ignore[attr-defined]
    for key in commands:
        item = commands[key]
        if isinstance(item, Group):
            create_group_manual_dir_recursive(item, ctx, prefix=directory, full_name=key)
    # create the main index.md
    Path(directory).mkdir(parents=True, exist_ok=True)
    file_name = f"{directory}/index.md"
    with Path(file_name).open(mode="w", encoding="UTF-8") as text_file:
        text_file.write(get_markdown_for_index(ctx, commands))


def create_group_manual_dir_recursive(
    command_group: click.Command | click.Group, ctx: click.core.Context, prefix: str, full_name: str
) -> None:
    """Create documentation directory (recursive)."""
    name = command_group.name
    directory = f"{prefix}/{name}"
    create_group_index_md(ctx, command_group, directory, full_name)
    commands = command_group.commands  # type: ignore[union-attr]
    for key in commands:
        item = commands[key]
        if isinstance(item, Group):
            create_group_manual_dir_recursive(
                item, ctx=ctx, prefix=directory, full_name=f"{full_name} {item.name}".strip()
            )


def create_group_index_md(
    ctx: click.core.Context,
    command_group: click.Command | click.Group,
    directory: str,
    full_name: str,
) -> None:
    """Create the index.md of command group."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    file_name = f"{directory}/index.md"

    help_text = get_enhanced_help_text_markdown(command_group)
    # config help has now text but too much lists
    if command_group.name == "config":
        help_text = f"```text\n{command_group.help}\n```"

    with Path(file_name).open(mode="w", encoding="UTF-8") as text_file:
        text_file.write(
            f"""---
title: "cmemc: Command Group - {full_name}"
description: "{command_group.get_short_help_str(limit=200)}"
icon: {get_icon_for_command_group(full_name)}
{get_tags_for_command_group(full_name)}---
# {full_name} Command Group
{EDIT_NOTE}

{help_text}

"""
        )
        for key in command_group.commands:  # type: ignore[union-attr]
            item = command_group.commands[key]  # type: ignore[union-attr]
            if isinstance(item, Group):
                continue
            if isinstance(item, Command):
                text_file.write(get_markdown_for_command(ctx, item, full_name))


def get_markdown_for_command(
    ctx: click.core.Context, command: click.Command, group_name: str
) -> str:
    """Create markdown for a single command."""
    formatter = ctx.make_formatter()
    command.format_help(ctx, formatter)

    # the help text is everything without options and usages
    help_text = get_enhanced_help_text_markdown(command, True)

    # the options text is the documentation of the options
    options_text_ = str(formatter.getvalue())
    # remove usage note (beginning)
    options_text_ = options_text_.replace(
        "Usage: cmemc", f"Usage: cmemc {group_name} {command.name}"
    )
    # remove --help option (end)
    options_text_ = options_text_.replace(
        """Options:
  -h, --help  Show this message and exit.""",
        "",
    )
    options_text_ = options_text_.replace("-h, --help", "")
    options_text_ = options_text_.replace("Show this message and exit.", "")
    options_text_ = options_text_.strip()
    # remove help text (ignore everything until Options)
    options_arrived = False
    options_text = ""
    for line in options_text_.splitlines():
        if options_arrived is True:
            options_text = f"{options_text}\n  {line}"
        if line == "Options:":
            options_arrived = True
    if options_text != "":
        options_text = f"""
??? info "Options"
    ```text
{options_text}
    ```
"""

    # the usage text is a singe line of code
    usage_text = (
        str(command.get_usage(ctx))
        .replace("Usage: cmemc", f"$ cmemc {group_name} {command.name}")
        .strip()
    )
    if options_text == "":
        usage_text = usage_text.replace(" [OPTIONS]", "")
    usage_text = f"""```shell-session title="Usage"
{usage_text}
```
"""

    return f"""## {group_name} {command.name}

{command.get_short_help_str(limit=200)}

{usage_text}

{help_text}

{options_text}
"""
