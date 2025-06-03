from typing import Iterator

from definit.definition.definition import Definition
from definit.definition.definition_key import DefinitionKey


class DAG:
    def __init__(self) -> None:
        self._edges: dict[DefinitionKey, set[DefinitionKey]] = {}
        self._definitions: dict[DefinitionKey, Definition] = {}

    def add_edge(self, node_from: Definition, node_to: Definition) -> None:
        if node_from.key in self._edges:
            self._edges[node_from.key].add(node_to.key)
        else:
            self._edges[node_from.key] = {node_to.key}

        self._definitions[node_from.key] = node_from
        self._definitions[node_to.key] = node_to

    @property
    def edges(self) -> Iterator[tuple[DefinitionKey, DefinitionKey]]:
        for node_from, nodes_to in self._edges.items():
            for node_to in nodes_to:
                yield node_from, node_to

    def get_node(self, node_key: DefinitionKey) -> Definition:
        return self._definitions[node_key]

    @property
    def nodes(self) -> set[Definition]:
        return set(self._definitions.values())
