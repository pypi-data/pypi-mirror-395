"""Migration: Chart and Workflow Property Shapes to Widget Integration"""

from typing import ClassVar

from cmem_cmemc.migrations.abc import MigrationRecipe, components


class SparqlDatatypesToXsdString(MigrationRecipe):
    """24.2 Migrate shui:sparqlQuery|sparqlUpdate datatype literals to xsd:string literals"""

    id = "sparql-query-datatypes-24.2"
    description = "Migrate shui SPARQL datatype literals to xsd:string literals"
    component: components = "explore"
    first_version = "24.2"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT DISTINCT ?query
WHERE {
  GRAPH ?shapeOrQueryGraph {
    ?query shui:queryText ?text .
    FILTER ( datatype(?text) IN (shui:sparqlQuery, shui:sparqlUpdate) )
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeOrQueryGraph {
    ?query shui:queryText ?oldLiteral .
  }
}
INSERT {
  GRAPH ?shapeOrQueryGraph {
    ?query shui:queryText ?newLiteral .
  }
}
# SELECT DISTINCT ?query
WHERE {
  GRAPH ?shapeOrQueryGraph {
    ?query shui:queryText ?oldLiteral .
    FILTER ( datatype(?oldLiteral) IN (shui:sparqlQuery, shui:sparqlUpdate) )
    BIND (STRDT(STR(?oldLiteral), xsd:string) AS ?newLiteral)
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        queries_with_old_literals = self._select(self.check_query)
        return len(queries_with_old_literals) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)
