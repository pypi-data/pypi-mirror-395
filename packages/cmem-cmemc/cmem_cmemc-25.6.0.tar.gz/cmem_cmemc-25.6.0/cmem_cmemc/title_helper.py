"""Title helper functions."""

import json

from cmem.cmempy.api import get_json
from cmem.cmempy.config import get_dp_api_endpoint


class TitleHelper:
    """Title helper class."""

    fetched_labels: dict[str, dict]

    def __init__(self) -> None:
        self.fetched_labels = {}
        self.endpoint = f"{get_dp_api_endpoint()}/api/explore/titles"

    def get(self, iri: str | list[str]) -> str | dict[str, str]:
        """Get the title of an IRI (or list of IRI)."""
        output = {}
        iris = [iri] if isinstance(iri, str) else list(set(iri))

        iris_to_fetch = []
        for _ in iris:
            if _ in self.fetched_labels:
                output[_] = self.fetched_labels[_]["title"]
            else:
                iris_to_fetch.append(_)

        if len(iris_to_fetch) > 0:
            titles: dict = get_json(
                self.endpoint,
                method="POST",
                data=json.dumps(iris_to_fetch),
                headers={"Content-type": "application/json"},
            )
            for title in titles.values():
                self.fetched_labels[title["iri"]] = title
                output[title["iri"]] = title["title"]

        return output[iri] if isinstance(iri, str) else output
