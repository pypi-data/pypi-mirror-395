"""Workspace Configuration migration recipe"""

from typing import ClassVar

from cmem.cmempy.dp.workspace import migrate_workspaces
from cmem.cmempy.health import get_complete_status_info

from cmem_cmemc.migrations.abc import MigrationRecipe, components


class MigrateWorkspaceConfiguration(MigrationRecipe):
    """Update Workspace Configuration to current version"""

    id = "workspace-configurations"
    description = "Migrate explore workspace configurations to the current version"
    component: components = "explore"
    first_version = "24.2"
    tags: ClassVar[list[str]] = ["system", "config"]

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        status_info = get_complete_status_info()
        config = status_info["explore"]["info"].get("workspaceConfiguration", {})
        return bool(config.get("workspacesToMigrate"))

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        migrate_workspaces()
