from abc import ABC
from abc import abstractmethod

from definit.dag.dag import DAG
from definit.dag.dag import DefinitionKey


class DAGVisualizationAbstract(ABC):
    @abstractmethod
    def show(self, root: DefinitionKey, dag: DAG) -> None: ...
