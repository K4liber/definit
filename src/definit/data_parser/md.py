import json
import re
from dataclasses import dataclass
from pathlib import Path

from definit_db_md import CONFIG

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.dag.dag import DefinitionKey
from definit.data_parser.interface import DataParserAbstract
from definit.field import Field
from definit.track import Track


class DataParserMdException(Exception):
    pass


@dataclass(frozen=True)
class _Const:
    FIELD_DIR = "field"
    TRACK_DIR = "track"
    INDEX_FILE_NAME = "index.md"


_CONTS = _Const()


class DataParserMd(DataParserAbstract):
    """
    Data parser for markdown files.
    """

    def __init__(self, data_md_path: Path = CONFIG.DATA_PATH) -> None:
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

    def get_track(self, track: Track) -> set[DefinitionKey]:
        """
        It is a MD parser, but track is a JSON file with the following structure:
        [
            {
                "name": "set",
                "field": "mathematics"
            },
            {
                "name": "multiset",
                "field": "mathematics"
            },
            ...
        ]
        """
        track_json_file_path = self._data_md_path / _CONTS.TRACK_DIR / f"{track.value}.json"

        if not track_json_file_path.exists():
            raise DataParserMdException(f"Track file {track_json_file_path} does not exist.")

        with open(track_json_file_path, "r") as f:
            track_data = json.load(f)

        definitions: set[DefinitionKey] = set()

        for item in track_data:
            try:
                field = Field(item["field"])
                definition_key = DefinitionKey(name=item["name"], field=field)
                definitions.add(definition_key)
            except (KeyError, ValueError) as e:
                raise DataParserMdException(f"Invalid track file format: {e}")

        return definitions

    def _get_dag(self, definitions: set[DefinitionKey]) -> DAG:
        dag = DAG()

        for definition in definitions:
            definition_file_path = self._index_cache[definition.field][definition.name]
            self._update_dag_in_place(definition_key=definition, dag=dag, definition_path=definition_file_path)

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
        index_file_path = field_path / _CONTS.INDEX_FILE_NAME

        with open(index_file_path) as index_file:
            lines = index_file.readlines()

            for line in lines:
                matches = re.findall(r"\[(.*?)\]\((.*?)\)", line)

                for definition_name, definition_relative_path in matches:
                    definition_path = self._get_field_path(field=field).joinpath(definition_relative_path)
                    self._index_cache[field][definition_name] = definition_path

    def _get_definition(
        self,
        definition_key: DefinitionKey,
        definition_path: Path,
        parent_definition_key: DefinitionKey | None = None,
    ) -> Definition:
        if definition_key in self._definition_cache:
            lines = self._definition_cache[definition_key]
        else:
            if not definition_path.exists():
                if parent_definition_key is None:
                    raise DataParserMdException(f"Root definition file {definition_path} does not exist.")
                else:
                    raise DataParserMdException(
                        f"Child definition file {definition_path} inside definition {parent_definition_key} does not exist."
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
        definition_path: Path,
        parent_definition_key: DefinitionKey | None = None,
    ) -> None:
        definition = self._get_definition(
            definition_key=definition_key, definition_path=definition_path, parent_definition_key=parent_definition_key
        )
        matches = re.findall(r"\[(.*?)\]\((.*?)\)", definition.content)

        for child_definition_name, child_definition_relative_path in matches:
            path_parts = Path(child_definition_relative_path).parts
            child_definition_field = Field(path_parts[2])
            child_definition_path = self._fields_path.joinpath(Path(*path_parts[2:]))
            # definition name could have a different form, we can get the correct form from the path
            child_definition_name = child_definition_path.stem
            child_definition_key = DefinitionKey(name=child_definition_name, field=child_definition_field)
            child_definition = self._get_definition(
                definition_key=child_definition_key,
                definition_path=child_definition_path,
                parent_definition_key=definition_key,
            )
            dag.add_edge(node_from=definition, node_to=child_definition)
            self._update_dag_in_place(
                definition_key=child_definition_key,
                dag=dag,
                definition_path=child_definition_path,
                parent_definition_key=definition_key,
            )

    @property
    def _fields_path(self) -> Path:
        return self._data_md_path / _CONTS.FIELD_DIR

    def _get_field_path(self, field: Field) -> Path:
        return self._fields_path / field.value
