from dataclasses import dataclass
from functools import cached_property

from definit.definition.field import Field


@dataclass(frozen=True)
class DefinitionKey:
    name: str
    field: Field
    sub_categories: tuple[str, ...] = ()

    @cached_property
    def uid(self) -> str:
        return "/".join([self.field, self._fixed_name])

    @cached_property
    def full_path(self) -> str:
        return "/".join([self.field, *self.sub_categories, self._fixed_name])

    @staticmethod
    def from_full_path(full_path: str) -> "DefinitionKey":
        parts = full_path.split("/")
        field = Field(parts[0])
        name = parts[-1]
        sub_categories = tuple(parts[1:-1])
        return DefinitionKey(name=name, field=field, sub_categories=sub_categories)

    def get_reference(self, phrase: str | None = None) -> str:
        if phrase is None:
            phrase = self.name

        return f"[{phrase}]({self.uid})"

    def get_index_reference(self) -> str:
        return f"[{self.name}]({self.full_path})"

    # Internal methods

    def __hash__(self) -> int:
        return hash(self.uid)

    @cached_property
    def _fixed_name(self) -> str:
        return self.name.replace(" ", "_").replace("'", "").replace("-", "_").lower()
