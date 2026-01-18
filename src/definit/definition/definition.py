from abc import abstractmethod

from definit.definition.definition_key import DefinitionKey


class Definition:
    def __init__(self, key: DefinitionKey, content: str | None = None) -> None:
        self._key = key
        self._content = self._get_content() if content is None else content

    @property
    def key(self) -> DefinitionKey:
        return self._key

    @property
    def content(self) -> str:
        return self._content

    @abstractmethod
    def _get_content(self) -> str: ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Definition):
            return NotImplemented

        return self.key.uid == other.key.uid and self.content == other.content

    def __lt__(self, other: "Definition") -> bool:
        return (self.key.uid, self.content) < (other.key.uid, other.content)

    def __hash__(self) -> int:
        return hash((self.key.__hash__(), self.content))
