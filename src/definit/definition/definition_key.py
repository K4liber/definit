from dataclasses import dataclass
from functools import cached_property

from definit.definition.field import Field


@dataclass(frozen=True)
class DefinitionKey:
    name: str
    field: Field

    @cached_property
    def uid(self) -> str:
        return f"{self.field}/{self._fixed_name}"

    @cached_property
    def full_path(self) -> str:
        return self.uid

    @staticmethod
    def from_full_path(full_path: str) -> "DefinitionKey":
        parts = full_path.split("/")
        field = Field(parts[0])
        name = parts[-1]
        return DefinitionKey(name=name, field=field)

    def get_reference(self, phrase: str | None = None) -> str:
        if phrase is None:
            phrase = self._fixed_name

        return f"[{phrase}]({self.uid})"

    def get_index_reference(self) -> str:
        return f"[{self._fixed_name}]({self.full_path})"

    # Internal methods

    def __hash__(self) -> int:
        return hash(self.uid)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, DefinitionKey):
            return NotImplemented

        return self.__hash__() == hash(value)

    @cached_property
    def _fixed_name(self) -> str:
        return self.name.replace(" ", "_").replace("'", "").replace("-", "_").lower()
