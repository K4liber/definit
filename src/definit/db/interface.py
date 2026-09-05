from abc import ABC
from abc import abstractmethod

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.dag.dag import DefinitionKey
from definit.definition.definition_group import DefinitionGroup
from definit.definition.field import Field


class DatabaseAbstract(ABC):
    @abstractmethod
    def get_dag(self, definition_keys: set[DefinitionKey]) -> DAG:
        """
        Get the DAG for a set of definition keys.
        """
        ...

    @abstractmethod
    def get_dag_for_definition(self, root: DefinitionKey) -> DAG:
        """
        Get the DAG with a given definition as root.
        """
        ...

    @abstractmethod
    def get_index(
        self,
        field: Field | None = None,
        group: DefinitionGroup | None = None,
    ) -> set[DefinitionKey]:
        """
        Get the set of all definitions for a field (if field is specified, otherwise returns all),
        optionally filtered by group.
        """
        ...

    @abstractmethod
    def get_definition(self, definition_key: DefinitionKey) -> Definition:
        """
        Get the definition for a given key.
        """
        ...

    @abstractmethod
    def get_groups(self) -> set[DefinitionGroup]:
        """
        Get all groups present in the database.
        """
        ...
