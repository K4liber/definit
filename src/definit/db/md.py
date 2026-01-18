import logging
import re
from dataclasses import dataclass
from pathlib import Path

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.dag.dag import DefinitionKey
from definit.db.interface import DatabaseAbstract
from definit.definition.field import Field

_logger = logging.getLogger(__name__)


class DataParserMdException(Exception):
    pass


@dataclass(frozen=True)
class _Const:
    INDEX_FILE_NAME = "index.md"


_CONST = _Const()


class DatabaseMd(DatabaseAbstract):
    """
    Database with markdown files as a source.
    """

    def __init__(self, data_md_path: Path, load_cache: bool = False) -> None:
        self._data_md_path = data_md_path
        self._definitions_path = data_md_path / "definitions"
        self._definition_uid_to_absolute_path: dict[str, Path] = dict()
        self._definition_cache: dict[DefinitionKey, str] = dict()

        if load_cache:
            self._assure_cache_loaded()

    ##### DatabaseAbstract methods implementation #####

    def get_dag_for_definition(self, root: DefinitionKey) -> DAG:
        self._assure_cache_loaded()
        definitions = {root}
        return self._get_dag(definitions=definitions)

    def get_index(self, field: Field | None = None) -> set[DefinitionKey]:
        index: set[DefinitionKey] = set()

        for absolute_path in self._definition_uid_to_absolute_path.values():
            full_path = self._get_full_path(absolute_path=absolute_path).removesuffix(".md")
            definition_key = DefinitionKey.from_full_path(full_path=full_path)

            if field is None or definition_key.field == field:
                index.add(definition_key)

        return index

    def get_definition(self, definition_key: DefinitionKey) -> Definition:
        """
        Get the definition for a given key.
        """
        self._assure_cache_loaded()
        return self._get_definition(
            definition_key=definition_key,
            parent_definition_key=None,
        )

    ##### Static methods #####

    @staticmethod
    def serialize(definitions: list[Definition], db_path: Path) -> None:
        for definition in definitions:
            definitions_path = db_path / "definitions"
            definition_file_path = _get_definition_file_path(definition=definition, definitions_path=definitions_path)
            md_content = _get_md_formatted_content(definition=definition)
            with open(definition_file_path, "w", encoding="utf-8") as f:
                f.write(md_content)
        # Write the index Markdown file for the field
        _write_index_md(
            db_path=db_path,
            definitions=definitions,
        )

    ##### Internal methods #####

    def _get_full_path(self, absolute_path: Path) -> str:
        return absolute_path.relative_to(self._definitions_path).as_posix()

    def _get_dag(self, definitions: set[DefinitionKey]) -> DAG:
        dag = DAG()

        for definition in definitions:
            self._update_dag_in_place(definition_key=definition, dag=dag)

        definition_keys = {key for key in definitions}
        dag_definition_keys = {definition.key for definition in dag.nodes}
        missing_definition_keys = definition_keys - dag_definition_keys

        if missing_definition_keys:
            _logger.warning(f"Following definitions are not a part of DAG: {missing_definition_keys}")

        if not dag.has_dag_structure():
            msg = f"DAG has an invalid structure: {dag.edges}"
            raise DataParserMdException(msg)

        return dag

    def _assure_cache_loaded(self) -> None:
        if self._definition_uid_to_absolute_path:
            return  # cache already loaded

        index_file_path = self._data_md_path / _CONST.INDEX_FILE_NAME

        with open(index_file_path) as index_file:
            lines = index_file.readlines()

            for line in lines:
                matches = re.findall(r"\[(.*?)\]\((.*?)\)", line)

                for _, full_path in matches:
                    definition_key = DefinitionKey.from_full_path(full_path=full_path)
                    absolute_path = self._data_md_path.joinpath("definitions", full_path).with_suffix(".md")
                    self._definition_uid_to_absolute_path[definition_key.uid] = absolute_path
                    # cache the definition for quick access
                    self._get_definition(
                        definition_key=definition_key,
                        parent_definition_key=None,
                    )

    def _get_definition(
        self,
        definition_key: DefinitionKey,
        parent_definition_key: DefinitionKey | None = None,
    ) -> Definition:
        if definition_key in self._definition_cache:
            content_md = self._definition_cache[definition_key]
        else:
            definition_absolute_path = self._definition_uid_to_absolute_path[definition_key.uid]

            if not definition_absolute_path.exists():
                if parent_definition_key is None:
                    raise DataParserMdException(f"Root definition file {definition_absolute_path} does not exist.")
                else:
                    raise DataParserMdException(
                        f"Child definition file {definition_absolute_path} inside definition "
                        f"'{parent_definition_key}' does not exist."
                    )

            with open(definition_absolute_path) as definition_file:
                content_md = "\n".join(definition_file.readlines())
                self._definition_cache[definition_key] = content_md

        return Definition(
            key=definition_key,
            content=_get_pure_content_from_md(content_md=content_md),
        )

    def _update_dag_in_place(
        self,
        definition_key: DefinitionKey,
        dag: DAG,
        parent_definition_key: DefinitionKey | None = None,
    ) -> None:
        definition = self._get_definition(definition_key=definition_key, parent_definition_key=parent_definition_key)
        matches = re.findall(r"\[(.*?)\]\((.*?)\)", definition.content)

        for _, child_uid in matches:
            child_definition_key = DefinitionKey.from_full_path(child_uid)
            child_definition = self._get_definition(
                definition_key=child_definition_key,
                parent_definition_key=definition_key,
            )
            dag.add_edge(node_from=definition, node_to=child_definition)
            self._update_dag_in_place(
                definition_key=child_definition_key,
                dag=dag,
                parent_definition_key=definition_key,
            )


def _write_index_md(db_path: Path, definitions: list[Definition]) -> None:
    lines: list[str] = []

    for definition in definitions:
        lines.append(f"- {definition.key.get_index_reference()}")

    index_path = db_path / _CONST.INDEX_FILE_NAME

    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _get_definition_file_path(definition: Definition, definitions_path: Path) -> Path:
    definition_file_path = definitions_path / (definition.key.full_path + ".md")
    definition_file_path.parent.mkdir(parents=True, exist_ok=True)
    return definition_file_path


def _get_md_formatted_content(definition: Definition) -> str:
    return f"# {definition.key.name}\n\n{definition.content}\n"


def _get_pure_content_from_md(content_md: str) -> str:
    lines = content_md.splitlines()

    if lines and lines[0].startswith("# "):
        lines = lines[1:]  # Remove the title line

    return "\n".join(lines).strip()
