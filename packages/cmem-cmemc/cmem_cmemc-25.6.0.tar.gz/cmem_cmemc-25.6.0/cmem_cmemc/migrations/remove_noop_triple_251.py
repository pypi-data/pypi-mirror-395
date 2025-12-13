"""RemoveHideHeaderFooterStatements migration"""

from typing import ClassVar

from cmem_cmemc.migrations.abc import MigrationRecipe, components


class RemoveHideHeaderFooterStatements(MigrationRecipe):
    """25.1 Remove Non-Operational shui:valueQueryHideHeader|Footer Triple"""

    id = "hide-header-footer-25.1"
    description = "Remove triples using deprecated shui:valueQueryHideHeader|Footer terms"
    component: components = "explore"
    first_version = "25.1"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT ?shape
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?shape ?deprecatedProperty ?value .
  }
  VALUES ?deprecatedProperty {
    shui:valueQueryHideHeader shui:valueQueryHideFooter
  }
} LIMIT 1
    """
    delete_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeCatalog { ?shape ?deprecatedProperty ?value . }
}
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?shape ?deprecatedProperty ?value .
  }
  VALUES ?deprecatedProperty {
    shui:valueQueryHideHeader shui:valueQueryHideFooter
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        existing_triples = self._select(self.check_query)
        return len(existing_triples) == 1

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.delete_query)
