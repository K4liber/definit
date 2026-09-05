from collections.abc import Iterable

from definit.definition.definition import Definition
from definit.definition.definition_key import DefinitionKey


class DefinitionGroup:
    """
    A named group of definitions.

    A single definition can belong to multiple groups. Groups are simple, optional labels used to
    filter definitions, e.g. all definitions created by the definit-dsa package can be grouped
    under "Data Structures and Algorithms". Unlike fields, groups are not part of the definition
    identity (uid).
    """

    def __init__(self, name: str, definitions: Iterable[Definition] = ()) -> None:
        self._name = name
        self._definitions = set(definitions)

    @property
    def name(self) -> str:
        return self._name

    @property
    def definitions(self) -> set[Definition]:
        return self._definitions

    @property
    def definition_keys(self) -> set[DefinitionKey]:
        return {definition.key for definition in self._definitions}

    def add(self, definition: Definition) -> None:
        self._definitions.add(definition)

    def __contains__(self, definition_key: DefinitionKey) -> bool:
        return definition_key in self.definition_keys

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DefinitionGroup):
            return NotImplemented

        return self.name == other.name

    def __lt__(self, other: "DefinitionGroup") -> bool:
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"DefinitionGroup(name={self.name!r})"

    def __str__(self) -> str:
        return self.name
