from dataclasses import dataclass
from functools import cached_property

from definit.definition.field import Field


@dataclass(frozen=True)
class DefinitionKey:
    name: str
    field: Field
    sub_categories: tuple[str, ...] = ()

    def __hash__(self) -> int:
        return hash(self.uid)

    @cached_property
    def uid(self) -> str:
        fixed_name = self.name.replace(" ", "_").replace("'", "").replace("-", "_").lower()
        return "/".join([self.field, *self.sub_categories, fixed_name])

    @staticmethod
    def from_uid(uid: str) -> "DefinitionKey":
        parts = uid.split("/")
        field = Field(parts[0])
        name = parts[-1]
        sub_categories = tuple(parts[1:-1])
        return DefinitionKey(name=name, field=field, sub_categories=sub_categories)

    def get_reference(self, phrase: str | None = None) -> str:
        if phrase is None:
            phrase = self.name

        return f"[{phrase}]({self.uid})"
