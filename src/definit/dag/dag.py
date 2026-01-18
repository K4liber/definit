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

    def has_dag_structure(self) -> bool:
        """Check if the DAG has a valid structure (i.e., no cycles)."""
        visited: set[DefinitionKey] = set()
        rec_stack: set[DefinitionKey] = set()

        def visit(node_key: DefinitionKey) -> bool:
            if node_key in rec_stack:
                return True
            if node_key in visited:
                return False

            visited.add(node_key)
            rec_stack.add(node_key)

            for neighbor in self._edges.get(node_key, []):
                if visit(neighbor):
                    return True

            rec_stack.remove(node_key)
            return False

        for node_key in self._definitions.keys():
            if visit(node_key):
                return False

        return True
