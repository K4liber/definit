from abc import ABC
from abc import abstractmethod

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.field import Field


class DataParserAbstract(ABC):
    @abstractmethod
    def get_dag(self, definition: Definition) -> DAG:
        """
        Get the DAG for a given definition.
        """
        ...

    @abstractmethod
    def get_index(self, field: Field | None = None) -> set[Definition]:
        """
        Get the set of all definitions.
        """
        ...
