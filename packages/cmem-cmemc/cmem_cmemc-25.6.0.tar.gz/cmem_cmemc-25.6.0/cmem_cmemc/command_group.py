"""cmemc Click Command Group"""

from click_didyoumean import DYMGroup
from click_help_colors import HelpColorsGroup


class CmemcGroup(HelpColorsGroup, DYMGroup):
    """Wrapper click.Group class to have a single extension point.

    Currently, wrapped click extensions and additional group features:#
    - click-help-colors: https://github.com/click-contrib/click-help-colors
    """

    color_for_command_groups = "white"
    color_for_writing_commands = "red"
    color_for_headers = "yellow"
    color_for_options = "green"

    def __init__(self, *args, **kwargs):  # noqa: ANN002, ANN003
        """Init a cmemc group command group."""
        # set default colors
        kwargs.setdefault("help_headers_color", self.color_for_headers)
        kwargs.setdefault("help_options_color", self.color_for_options)
        kwargs.setdefault(
            "help_options_custom_colors",
            {
                "acl": self.color_for_command_groups,
                "admin": self.color_for_command_groups,
                "bootstrap": self.color_for_writing_commands,
                "cache": self.color_for_command_groups,
                "cancel": self.color_for_writing_commands,
                "client": self.color_for_command_groups,
                "config": self.color_for_command_groups,
                "create": self.color_for_writing_commands,
                "dataset": self.color_for_command_groups,
                "delete": self.color_for_writing_commands,
                "disable": self.color_for_writing_commands,
                "enable": self.color_for_writing_commands,
                "eval": self.color_for_writing_commands,
                "execute": self.color_for_writing_commands,
                "file": self.color_for_command_groups,
                "graph": self.color_for_command_groups,
                "import": self.color_for_writing_commands,
                "imports": self.color_for_command_groups,
                "insights": self.color_for_command_groups,
                "install": self.color_for_writing_commands,
                "io": self.color_for_writing_commands,
                "metrics": self.color_for_command_groups,
                "migrate": self.color_for_writing_commands,
                "migrations": self.color_for_command_groups,
                "password": self.color_for_writing_commands,
                "project": self.color_for_command_groups,
                "python": self.color_for_command_groups,
                "query": self.color_for_command_groups,
                "reload": self.color_for_writing_commands,
                "replay": self.color_for_writing_commands,
                "resource": self.color_for_command_groups,
                "scheduler": self.color_for_command_groups,
                "secret": self.color_for_writing_commands,
                "showcase": self.color_for_writing_commands,
                "store": self.color_for_command_groups,
                "uninstall": self.color_for_writing_commands,
                "update": self.color_for_writing_commands,
                "upload": self.color_for_writing_commands,
                "user": self.color_for_command_groups,
                "validation": self.color_for_command_groups,
                "variable": self.color_for_command_groups,
                "vocabulary": self.color_for_command_groups,
                "workflow": self.color_for_command_groups,
                "workspace": self.color_for_command_groups,
            },
        )
        super().__init__(*args, **kwargs)
