import json
import re
from dataclasses import dataclass
from pathlib import Path

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.data_parser.interface import DataParserAbstract
from definit.field import Field
from definit.track import Track


class DataParserMdException(Exception):
    pass


@dataclass(frozen=True)
class _Const:
    TRACK_DIR = "track"


_CONTS = _Const()


class DataParserMd(DataParserAbstract):
    """
    Data parser for markdown files.
    """

    def __init__(self, data_md_path: Path) -> None:
        self._data_md_path = data_md_path
        self._index_cache: dict[Field, dict[str, Path]] = dict()
        self._definition_cache: dict[Definition, str] = dict()

    def get_dag(self, track: Track | None = None) -> DAG:
        if track is None:
            # Get all definitions
            definitions = self.get_index()
        else:
            # Get all definitions for a given track
            definitions = self.get_track(track=track)

        return self._get_dag(definitions=definitions)

    def get_dag_for_definition(self, root: Definition) -> DAG:
        self._load_index_cache(field=root.field)
        definitions = {root}
        return self._get_dag(definitions=definitions)

    def get_index(self, field: Field | None = None) -> set[Definition]:
        self._cache_index(field=field)
        index: set[Definition] = set()

        for field, field_definitions in self._index_cache.items():
            for definition_name in field_definitions.keys():
                index.add(Definition(name=definition_name, field=field))

        return index

    def get_track(self, track: Track) -> set[Definition]:
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

        definitions = set()

        for item in track_data:
            try:
                field = Field(item["field"])
                definition = Definition(name=item["name"], field=field)
                definitions.add(definition)
            except (KeyError, ValueError) as e:
                raise DataParserMdException(f"Invalid track file format: {e}")

        return definitions

    def _get_dag(self, definitions: set[Definition]) -> DAG:
        dag = DAG()

        for definition in definitions:
            definition_file_path = self._index_cache[definition.field][definition.name]
            self._update_dag_in_place(definition=definition, dag=dag, definition_path=definition_file_path)

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
        index_file_path = field_path / self._index_file_name

        with open(index_file_path) as index_file:
            lines = index_file.readlines()

            for line in lines:
                matches = re.findall(r"\[(.*?)\]\((.*?)\)", line)

                for definition_name, definition_relative_path in matches:
                    definition_path = self._get_field_path(field=field).joinpath(definition_relative_path)
                    self._index_cache[field][definition_name] = definition_path

    def _update_dag_in_place(
        self, definition: Definition, dag: DAG, definition_path: Path, parent_definition: Definition | None = None
    ) -> None:
        if definition in self._definition_cache:
            lines = self._definition_cache[definition]
        else:
            if not definition_path.exists():
                if parent_definition is None:
                    raise DataParserMdException(f"Root definition file {definition_path} does not exist.")
                else:
                    raise DataParserMdException(
                        f"Child definition file {definition_path} inside definition {parent_definition} does not exist."
                    )

            with open(definition_path) as definition_file:
                lines = "\n".join(definition_file.readlines())

        matches = re.findall(r"\[(.*?)\]\((.*?)\)", lines)

        for child_definition_name, child_definition_relative_path in matches:
            path_parts = Path(child_definition_relative_path).parts
            child_definition_field = Field(path_parts[2])
            child_definition_path = self._data_md_path.joinpath(Path(*path_parts[2:]))
            # definition name could have a different form, we can get the correct form from the path
            child_definition_name = child_definition_path.stem
            child_definition = Definition(name=child_definition_name, field=child_definition_field)
            dag.add_edge(node_from=definition, node_to=child_definition)
            self._update_dag_in_place(
                definition=child_definition,
                dag=dag,
                definition_path=child_definition_path,
                parent_definition=definition,
            )

    def _get_field_path(self, field: Field) -> Path:
        return self._data_md_path / field.value

    @property
    def _index_file_name(self) -> str:
        return "index.md"
