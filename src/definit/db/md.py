import re
from dataclasses import dataclass
from pathlib import Path

from definit_db import CONFIG

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.dag.dag import DefinitionKey
from definit.db.interface import DatabaseAbstract
from definit.field import Field
from definit.track import Track


class DataParserMdException(Exception):
    pass


@dataclass(frozen=True)
class _Const:
    FIELD_DIR = "field"
    TRACK_DIR = "track"
    INDEX_FILE_NAME = "index.md"


_CONST = _Const()


class DatabaseMd(DatabaseAbstract):
    """
    Database with markdown files as a source.
    """

    def __init__(self, data_md_path: Path = CONFIG.DATA_PATH_MD) -> None:
        self._data_md_path = data_md_path
        self._index_cache: dict[Field, dict[str, Path]] = dict()
        self._definition_cache: dict[DefinitionKey, str] = dict()

    def get_dag(self, track: Track | None = None) -> DAG:
        if track is None:
            # Get all definitions
            definitions = self.get_index()
        else:
            # Get all definitions for a given track
            definitions = self.get_track(track=track)

        return self._get_dag(definitions=definitions)

    def get_dag_for_definition(self, root: DefinitionKey) -> DAG:
        self._load_index_cache(field=root.field)
        definitions = {root}
        return self._get_dag(definitions=definitions)

    def get_index(self, field: Field | None = None) -> set[DefinitionKey]:
        self._cache_index(field=field)
        index: set[DefinitionKey] = set()

        for field, field_definitions in self._index_cache.items():
            for definition_name in field_definitions.keys():
                index.add(DefinitionKey(name=definition_name, field=field))

        return index

    def get_definition(self, definition_key: DefinitionKey) -> Definition:
        """
        Get the definition for a given key.
        """
        self._load_index_cache(field=definition_key.field)
        return self._get_definition(
            definition_key=definition_key,
            parent_definition_key=None,
        )

    def get_track(self, track: Track) -> set[DefinitionKey]:
        """
        It is a MD parser for track files. Track file has the following format:

        - [set](mathematics/set)
        - [multiset](mathematics/multiset)
        - [finite_set](mathematics/finite_set)
        - [function](mathematics/function)
        - [relation](mathematics/relation)
        - [object](mathematics/object)
        - [graph](mathematics/graph)
        - [node](mathematics/node)
        - ...
        """
        track_md_file_path = self._data_md_path / _CONST.TRACK_DIR / f"{track.value}.md"

        if not track_md_file_path.exists():
            raise DataParserMdException(f"Track file {track_md_file_path} does not exist.")

        definitions: set[DefinitionKey] = set()

        with open(track_md_file_path, "r") as f:
            track_data = f.readlines()

            for line in track_data:
                matches = re.findall(r"\[(.*?)\]\((.*?)\)", line)

                for _, definition_key_str in matches:
                    field_name, definition_name = definition_key_str.split("/")
                    field = Field(field_name)
                    definition_key = DefinitionKey(name=definition_name, field=field)
                    definitions.add(definition_key)

        return definitions

    def _get_dag(self, definitions: set[DefinitionKey]) -> DAG:
        dag = DAG()

        for definition in definitions:
            self._update_dag_in_place(definition_key=definition, dag=dag)

        return dag

    def _cache_index(self, field: Field | None = None) -> None:
        fields = [field for field in Field] if field is None else [field]

        for field in fields:
            self._load_index_cache(field=field)

    def _load_index_cache(self, field: Field) -> None:
        if field in self._index_cache:
            return

        if field not in self._index_cache:
            self._index_cache[field] = {}

        field_path = self._get_field_path(field=field)
        index_file_path = field_path / _CONST.INDEX_FILE_NAME

        with open(index_file_path) as index_file:
            lines = index_file.readlines()

            for line in lines:
                matches = re.findall(r"\[(.*?)\]\((.*?)\)", line)

                for definition_name, definition_relative_path in matches:
                    definition_path = (
                        self._get_field_definitions_path(field=field)
                        .joinpath(definition_relative_path)
                        .with_suffix(".md")
                    )
                    self._index_cache[field][definition_name] = definition_path

    def _get_definition(
        self,
        definition_key: DefinitionKey,
        parent_definition_key: DefinitionKey | None = None,
    ) -> Definition:
        if definition_key in self._definition_cache:
            lines = self._definition_cache[definition_key]
        else:
            definition_path = self._index_cache[definition_key.field][definition_key.name]

            if not definition_path.exists():
                if parent_definition_key is None:
                    raise DataParserMdException(f"Root definition file {definition_path} does not exist.")
                else:
                    raise DataParserMdException(
                        f"Child definition file {definition_path} inside definition "
                        f"'{parent_definition_key}' does not exist."
                    )

            with open(definition_path) as definition_file:
                lines = "\n".join(definition_file.readlines())

        return Definition(
            key=definition_key,
            content=lines,
        )

    def _update_dag_in_place(
        self,
        definition_key: DefinitionKey,
        dag: DAG,
        parent_definition_key: DefinitionKey | None = None,
    ) -> None:
        definition = self._get_definition(definition_key=definition_key, parent_definition_key=parent_definition_key)
        matches = re.findall(r"\[(.*?)\]\((.*?)\)", definition.content)

        for _, child_definition_source in matches:
            source_parts = Path(child_definition_source).parts
            child_definition_field = Field(source_parts[0])
            child_definition_name = source_parts[-1]
            child_definition_key = DefinitionKey(name=child_definition_name, field=child_definition_field)
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

    @property
    def _fields_path(self) -> Path:
        return self._data_md_path / _CONST.FIELD_DIR

    def _get_field_path(self, field: Field) -> Path:
        return self._fields_path / field.value

    def _get_field_definitions_path(self, field: Field) -> Path:
        return self._get_field_path(field=field) / "definitions"
