"""Bootstrap Data migration recipe"""

from typing import ClassVar

from cmem.cmempy.dp.admin import import_bootstrap_data
from cmem.cmempy.health import get_complete_status_info

from cmem_cmemc.migrations.abc import MigrationRecipe, components


class MigrateBootstrapData(MigrationRecipe):
    """Update Bootstrap Data to current version"""

    id = "bootstrap-data"
    description = "Migrate bootstrap system data (same as admin store bootstrap --import)"
    component: components = "explore"
    first_version = "20.12"
    tags: ClassVar[list[str]] = ["system", "shapes"]

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        status_info = get_complete_status_info()
        shapes_status = status_info["shapes"]["version"]
        return bool(shapes_status != status_info["explore"]["version"])

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        import_bootstrap_data()
