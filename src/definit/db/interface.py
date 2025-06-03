from abc import ABC
from abc import abstractmethod

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.dag.dag import DefinitionKey
from definit.definition.field import Field
from definit.definition.track import Track


class DatabaseAbstract(ABC):
    @abstractmethod
    def get_dag(self, track: Track | None = None) -> DAG:
        """
        Get the DAG for a given track if specified, otherwise returns the full DAG.
        """
        ...

    @abstractmethod
    def get_dag_for_definition(self, root: DefinitionKey) -> DAG:
        """
        Get the DAG with a given definition as root.
        """
        ...

    @abstractmethod
    def get_index(self, field: Field | None = None) -> set[DefinitionKey]:
        """
        Get the set of all definitions for a field (if field is specified, otherwise returns all).
        """
        ...

    @abstractmethod
    def get_definition(self, definition_key: DefinitionKey) -> Definition:
        """
        Get the definition for a given key.
        """
        ...
