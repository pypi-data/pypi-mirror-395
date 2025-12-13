"""Migration recipe abstract base class"""

import re
from abc import ABC, abstractmethod
from typing import ClassVar, Literal

from cmem.cmempy.health import get_complete_status_info
from cmem.cmempy.queries import SparqlQuery
from packaging.version import Version

components = Literal["explore", "build"]


class MigrationRecipe(ABC):
    """Tests and migration functions to migrate a specific type of resource between versions"""

    id: str
    description: str
    component: components = "explore"
    first_version: str | None = None
    last_version: str | None = None
    tags: ClassVar[list[str]] = []
    default_prefixes: ClassVar[dict[str, str]] = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "sh": "http://www.w3.org/ns/shacl#",
        "auth": "https://vocab.eccenca.com/auth/",
        "shui": "https://vocab.eccenca.com/shui/",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
    }

    @abstractmethod
    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""

    @abstractmethod
    def apply(self) -> None:
        """Apply the recipe to the current version."""

    def version_matches(self, component_version: str = "") -> bool:
        """Test if the component version matches the version specification of the recipe"""
        status_info = get_complete_status_info()
        first_version = self.first_version if self.first_version else "0.0.0"
        last_version = self.last_version if self.last_version else "1000.0.0"
        if component_version == "":
            if self.component == "explore":
                component_version = str(status_info["explore"]["version"])
            if self.component == "build":
                component_version = str(status_info["build"]["version"])
        if component_version.startswith("v"):
            component_version = component_version[1:]
        # remove git describe stuff (24.2.1-501-gb0ca19b14)
        component_version = re.sub(r"-.*", "", component_version)
        if component_version == "":
            return False
        return Version(first_version) <= Version(component_version) <= Version(last_version)

    def _get_default_prefixes(self) -> str:
        """Get default prefixes as SPARQL Snippet"""
        snippet = ""
        for prefix, namespace in self.default_prefixes.items():
            snippet += f"PREFIX {prefix}: <{namespace}>\n"
        return snippet

    def _select(self, query_text: str, placeholder: dict[str, str] | None = None) -> list[dict]:
        """Get the bindings of a SPARQL Query result"""
        if not placeholder:
            placeholder = {"DEFAULT_PREFIXES": self._get_default_prefixes()}
        else:
            placeholder["DEFAULT_PREFIXES"] = self._get_default_prefixes()
        query = SparqlQuery(query_text)
        response: dict = query.get_json_results(placeholder=placeholder)
        results: dict = response.get("results", {"bindings": []})
        bindings: list[dict] = results.get("bindings")  # type: ignore[assignment]
        return bindings

    def _update(self, query_text: str, placeholder: dict[str, str] | None = None) -> None:
        """Send an update query"""
        if not placeholder:
            placeholder = {"DEFAULT_PREFIXES": self._get_default_prefixes()}
        else:
            placeholder["DEFAULT_PREFIXES"] = self._get_default_prefixes()
        query = SparqlQuery(query_text)
        query.query_type = "UPDATE"
        query.get_results(placeholder=placeholder)
