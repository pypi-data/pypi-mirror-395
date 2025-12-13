"""Migration: Chart and Workflow Property Shapes to Widget Integration"""

from typing import ClassVar

from cmem_cmemc.migrations.abc import MigrationRecipe, components


class ChartsOnNodeShapesToToWidgetIntegrations(MigrationRecipe):
    """24.3 Migrate Chart on NodeShapes to Widget Integrations"""

    id = "charts-on-nshapes-24.3"
    description = "Migrate Charts on Node Shapes to Widget Integrations"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT *
WHERE {
  GRAPH ?maybeOtherGraph {
    ?maybeOtherGraph a shui:ShapeCatalog .
    ?nodeShape a sh:NodeShape .
  }
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?nodeShape shui:provideChartVisualization ?shuiChart .
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeCatalog {
    ?nodeShape shui:provideChartVisualization ?shuiChart .
  }
}
INSERT {
  GRAPH ?shapeCatalog {
    ?newWidgetIntegration a shui:WidgetIntegration ;
      shui:WidgetIntegration_widget ?shuiChart ;
      rdfs:label ?name ;
      rdfs:comment ?description ;
      sh:order -1000 .
    ?nodeShape shui:WidgetIntegration_integrate ?newWidgetIntegration .
  }
}
WHERE {
  GRAPH ?maybeOtherGraph {
    ?maybeOtherGraph a shui:ShapeCatalog .
    ?nodeShape a sh:NodeShape .
  }
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?nodeShape shui:provideChartVisualization ?shuiChart .
  }
  OPTIONAL { ?shuiChart rdfs:label ?name }
  OPTIONAL { ?shuiChart rdfs:comment ?description }
  BIND (IRI(CONCAT(STR(?shuiChart), "_WidgetIntegration")) as ?newWidgetIntegration)
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        node_shapes_with_charts = self._select(self.check_query)
        return len(node_shapes_with_charts) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)


class ChartsOnPropertyShapesToWidgetIntegrations(MigrationRecipe):
    """24.3 Migrate Chart Property Shapes to Widget Integrations"""

    id = "charts-on-pshapes-24.3"
    description = "Migrate Charts on Property Shapes to Widget Integrations"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT *
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideChartVisualization ?shuiChart .
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeCatalog {
    ?propertyShape ?p ?o .
    ?nodeShape sh:property ?propertyShape .
  }
}
INSERT {
  GRAPH ?shapeCatalog {
    ?propertyShape a shui:WidgetIntegration ;
      shui:WidgetIntegration_widget ?shuiChart ;
      rdfs:label ?name ;
      rdfs:comment ?description ;
      sh:order ?order ;
      shui:WidgetIntegration_group ?group .
    ?nodeShape shui:WidgetIntegration_integrate ?propertyShape .
  }
}
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideChartVisualization ?shuiChart .
    ?propertyShape ?p ?o .
    OPTIONAL {?propertyShape sh:name ?name }
    OPTIONAL {?propertyShape sh:description ?description }
    OPTIONAL {?propertyShape sh:order ?order }
    OPTIONAL {?propertyShape sh:group ?group }
    OPTIONAL {?nodeShape sh:property ?propertyShape }
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        chart_property_shapes = self._select(self.check_query)
        return len(chart_property_shapes) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)


class WorkflowTriggerPropertyShapesToWidgetIntegrations(MigrationRecipe):
    """24.3 Migrate Workflow Trigger Property Shapes to Widget Integrations"""

    id = "trigger-on-pshapes-24.3"
    description = "Migrate Workflow Trigger on Property Shapes to Widget Integrations"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT *
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideWorkflowTrigger ?shuiChart .
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeCatalog {
    ?propertyShape ?p ?o .
    ?nodeShape sh:property ?propertyShape .
  }
}
INSERT {
  GRAPH ?shapeCatalog {
    ?propertyShape a shui:WidgetIntegration ;
      shui:WidgetIntegration_widget ?workflowTrigger ;
      rdfs:label ?name ;
      rdfs:comment ?description ;
      sh:order ?order ;
      shui:WidgetIntegration_group ?group .
    ?nodeShape shui:WidgetIntegration_integrate ?propertyShape .
  }
}
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideWorkflowTrigger ?workflowTrigger .
    ?propertyShape ?p ?o .
    OPTIONAL {?propertyShape sh:name ?name }
    OPTIONAL {?propertyShape sh:description ?description }
    OPTIONAL {?propertyShape sh:order ?order }
    OPTIONAL {?propertyShape sh:group ?group }
    OPTIONAL {?nodeShape sh:property ?propertyShape }
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        chart_property_shapes = self._select(self.check_query)
        return len(chart_property_shapes) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)


class TableReportPropertyShapesToWidgetIntegrations(MigrationRecipe):
    """24.3 Migrate Table Report Property Shapes to Widget Integrations"""

    id = "table-reports-on-pshapes-24.3"
    description = (
        "Migrate Table Reports (which use shui:null) on Property Shapes to Widget Integrations"
    )
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT ?propertyShape
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:valueQuery ?valueQuery ;
      sh:path shui:null .
    FILTER NOT EXISTS { ?propertyShape shui:isSystemResource true }
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeCatalog {
    ?propertyShape ?p ?o .
    ?nodeShape sh:property ?propertyShape .
  }
}
INSERT {
  GRAPH ?shapeCatalog {
    ?propertyShape a shui:WidgetIntegration ;
      shui:WidgetIntegration_widget ?newTableReport ;
      rdfs:label ?name ;
      rdfs:comment ?description ;
      sh:order ?order ;
      shui:WidgetIntegration_group ?group .
    ?nodeShape shui:WidgetIntegration_integrate ?propertyShape .

    ?newTableReport a shui:TableReport ;
      rdfs:label ?newTableReportLabel ;
      shui:TableReport_hideFooter ?hideFooter ;
      shui:TableReport_hideHeader ?hideHeader ;
      shui:TableReport_query ?valueQuery .
  }
}
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      sh:path shui:null ;
      shui:valueQuery ?valueQuery .
    FILTER NOT EXISTS { ?propertyShape shui:isSystemResource true }
    ?propertyShape ?p ?o .
    OPTIONAL {?propertyShape sh:name ?name }
    OPTIONAL {?propertyShape sh:description ?description }
    OPTIONAL {?propertyShape sh:order ?order }
    OPTIONAL {?propertyShape sh:group ?group }
    OPTIONAL {?propertyShape sh:name ?name }
    OPTIONAL {?propertyShape shui:valueQueryHideHeader ?hideHeaderValue }
    OPTIONAL {?propertyShape shui:valueQueryHideFooter ?hideFooterValue }
    OPTIONAL {?nodeShape sh:property ?propertyShape }
    BIND ( IRI(CONCAT(STR(?propertyShape), "-TableReport")) AS ?newTableReport )
    BIND ( STRLANG(CONCAT("Table Report: ", ?name), lang(?name)) AS ?newTableReportLabel )
    BIND ( COALESCE(?hideHeaderValue, false) as ?hideHeader)
    BIND ( COALESCE(?hideFooterValue, false) as ?hideFooter)
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        table_report_property_shapes = self._select(self.check_query)
        return len(table_report_property_shapes) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)
