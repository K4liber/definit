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

    def get_definition_levels(self) -> list[tuple[Definition, int]]:
        """Return the definition levels.

        Each definition is paired with its level in the DAG.
        Level 0 corresponds to definitions with no dependencies.
        """
        visited: set[DefinitionKey] = set()
        added: set[DefinitionKey] = set()
        levels: dict[DefinitionKey, int] = {}
        definitions_with_levels: list[tuple[Definition, int]] = []

        def visit(node_key: DefinitionKey) -> int:
            if node_key in visited:
                return levels.get(node_key, 0)

            visited.add(node_key)
            max_level = 0

            for neighbor in self._edges.get(node_key, []):
                neighbor_level = visit(neighbor)
                max_level = max(max_level, neighbor_level + 1)

            levels[node_key] = max_level

            if node_key not in added:
                definitions_with_levels.append((self._definitions[node_key], max_level))
                added.add(node_key)

            return max_level

        for node_key in self._definitions.keys():
            visit(node_key)

        return definitions_with_levels
