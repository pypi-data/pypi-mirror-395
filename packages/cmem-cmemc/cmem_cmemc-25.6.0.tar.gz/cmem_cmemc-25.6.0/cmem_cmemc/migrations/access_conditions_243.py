"""Access Conditions migration recipes from before 24.3"""

from typing import ClassVar

from cmem.cmempy.dp.authorization.refresh import get as refresh_acls

from cmem_cmemc.migrations.abc import MigrationRecipe, components


class MoveAccessConditionsToNewGraph(MigrationRecipe):
    """24.4 Access Conditions Migration"""

    id = "acl-graph-24.3"
    description = "Move access conditions and used queries to new ACL graph"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["system", "acl"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT ?subject
FROM <urn:elds-backend-access-conditions-graph>
WHERE {
  ?subject a ?class .
  FILTER NOT EXISTS { ?subject shui:isSystemResource true }
  FILTER (?class IN (auth:AccessCondition, shui:SparqlQuery) ) .
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE { GRAPH <urn:elds-backend-access-conditions-graph> { ?s ?p ?o . } }
INSERT { GRAPH <https://ns.eccenca.com/data/ac/> { ?s ?p ?o . } }
WHERE {
  GRAPH <urn:elds-backend-access-conditions-graph> {
    ?s ?p ?o .
    ?s a ?class .
    FILTER (?class IN (auth:AccessCondition, shui:SparqlQuery) ) .
    FILTER NOT EXISTS { ?s shui:isSystemResource true }
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        old_acls = self._select(self.check_query)
        return len(old_acls) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)
        refresh_acls()


class RenameAuthVocabularyResources(MigrationRecipe):
    """24.4 Access Conditions Migration"""

    id = "acl-vocab-24.3"
    description = "Migrate auth vocabulary terms (actions and other grants)"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["system", "acl"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT DISTINCT ?acl_id
WHERE {
  GRAPH ?acl_graph {
	?acl_id a auth:AccessCondition .
    FILTER NOT EXISTS { ?acl_id shui:isSystemResource true }
    ?acl_id ?property ?old_term .
    FILTER (?old_term in (
        <urn:elds-backend-all-actions>,
        <urn:elds-backend-actions-auth-access-control>,
        <urn:eccenca:di>,
        <urn:eccenca:ThesaurusUserInterface>,
        <urn:eccenca:AccessInternalGraphs>,
        <urn:eccenca:QueryUserInterface>,
        <urn:eccenca:VocabularyUserInterface>,
        <urn:eccenca:ExploreUserInterface>,
        <https://vocab.eccenca.com/auth/Action/Viz/Manage>,
        <https://vocab.eccenca.com/auth/Action/Viz/Read>,
        <urn:elds-backend-anonymous-user>,
        <urn:elds-backend-public-group>,
        <urn:elds-backend-all-graphs>
      ))
  }
  FILTER (?acl_graph IN (<urn:elds-backend-access-conditions-graph>, <https://ns.eccenca.com/data/ac/>))
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE { GRAPH ?acl_graph { ?s ?p <{{OLD_IRI}}> . } }
INSERT { GRAPH ?acl_graph { ?s ?p <{{NEW_IRI}}> . } }
WHERE {
  GRAPH ?acl_graph {
    ?s ?p ?o .
    FILTER NOT EXISTS { ?s shui:isSystemResource true }
    FILTER (?o = <{{OLD_IRI}}> )
  }
  FILTER (?acl_graph IN (<urn:elds-backend-access-conditions-graph>, <https://ns.eccenca.com/data/ac/>))
}
    """
    terms: ClassVar[dict[str, str]] = {
        "urn:elds-backend-all-actions": "https://vocab.eccenca.com/auth/Action/AllActions",
        "urn:elds-backend-actions-auth-access-control": "https://vocab.eccenca.com/auth/Action/ChangeAccessConditions",
        "urn:eccenca:di": "https://vocab.eccenca.com/auth/Action/ChangeAccessConditions",
        "urn:eccenca:ThesaurusUserInterface": "https://vocab.eccenca.com/auth/Action/Explore-ThesaurusCatalog",
        "urn:eccenca:AccessInternalGraphs": "https://vocab.eccenca.com/auth/Action/Explore-ListSystemGraphs",
        "urn:eccenca:QueryUserInterface": "https://vocab.eccenca.com/auth/Action/Explore-QueryCatalog",
        "urn:eccenca:VocabularyUserInterface": "https://vocab.eccenca.com/auth/Action/Explore-VocabularyCatalog",
        "urn:eccenca:ExploreUserInterface": "https://vocab.eccenca.com/auth/Action/Explore-KnowledgeGraphs",
        "https://vocab.eccenca.com/auth/Action/Viz/Manage": "https://vocab.eccenca.com/auth/Action/Explore-BKE-Manage",
        "https://vocab.eccenca.com/auth/Action/Viz/Read": "https://vocab.eccenca.com/auth/Action/Explore-BKE-Read",
        "urn:elds-backend-anonymous-user": "https://vocab.eccenca.com/auth/AnonymousUser",
        "urn:elds-backend-public-group": "https://vocab.eccenca.com/auth/PublicGroup",
        "urn:elds-backend-all-graphs": "https://vocab.eccenca.com/auth/AllGraphs",
    }

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        acls_with_vocabs_to_change = self._select(self.check_query)
        return len(acls_with_vocabs_to_change) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        for old_iri, new_iri in self.terms.items():
            self._update(self.move_query, placeholder={"OLD_IRI": old_iri, "NEW_IRI": new_iri})
        refresh_acls()
