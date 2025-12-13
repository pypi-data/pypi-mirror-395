"""Class to retrieve query placeholder resources

note: this is not the correct place for this class - it should be cmem_client or cmempy
"""

from cmem.cmempy.queries import SparqlQuery

FETCH_PLACEHOLDERS = """
PREFIX shui: <https://vocab.eccenca.com/shui/>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?key ?valueQuery
FROM <{{graph}}>
WHERE {
  ?placeholder a shui:QueryPlaceholder ;
    shui:QueryPlaceholder_key ?key ;
    shui:QueryPlaceholder_valueQuery ?valueQueryR ;
    shui:QueryPlaceholder_usedInQuery <{{query}}> .
  ?valueQueryR shui:queryText ?valueQuery
}
"""


class QueryPlaceholder:
    """A query placeholder"""

    key: str
    value_query: SparqlQuery

    def __init__(self, key: str, value_query: str):
        self.key = key
        self.value_query = SparqlQuery(value_query, query_type="SELECT")

    def complete(self, incomplete: str = "") -> list[str] | list[tuple[str, str]]:  # noqa: ARG002
        """Prepare a list of placeholder values"""
        result = self.value_query.get_json_results()
        projection_vars = result["head"]["vars"]
        bindings: list[dict] = result["results"]["bindings"]
        if "value" not in projection_vars:
            return []

        if "description" not in projection_vars:
            values_without_description = []
            for _ in bindings:
                value = str(_["value"]["value"])
                values_without_description.append(value)
            return values_without_description

        values_with_description = []
        for _ in bindings:
            value = str(_["value"]["value"])
            description = _.get("description", {}).get("value", "")
            values_with_description.append((value, description))
        return values_with_description


def get_placeholders_for_query(iri: str) -> dict[str, QueryPlaceholder]:
    """Get a placeholder dict for a query"""
    placeholders = {}
    results = SparqlQuery(
        FETCH_PLACEHOLDERS,
        query_type="SELECT",
    ).get_json_results(placeholder={"graph": "https://ns.eccenca.com/data/queries/", "query": iri})
    for binding in results["results"]["bindings"]:
        key = binding["key"]["value"]
        value_query = binding["valueQuery"]["value"]
        placeholders[key] = QueryPlaceholder(key=key, value_query=value_query)
    return placeholders
