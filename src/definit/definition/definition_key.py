from dataclasses import dataclass

from definit.definition.field import Field


@dataclass(frozen=True)
class DefinitionKey:
    name: str
    field: Field

    def get_reference(self, phrase: str | None = None) -> str:
        if phrase is None:
            phrase = self.name

        return f"[{phrase}]({self.field}/{self.name})"
