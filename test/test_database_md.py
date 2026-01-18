from pathlib import Path

from definit.dag.dag import DefinitionKey
from definit.db.md import DatabaseMd
from definit.definition.definition import Definition

_expected_definitions: list[Definition] = [
    Definition(key=DefinitionKey(name="list", field="1"), content="a_list"),
    Definition(key=DefinitionKey(name="node", field="1", sub_categories=("a", "b")), content="a_node"),
    Definition(key=DefinitionKey(name="tree", field="2", sub_categories=("a",)), content="a_tree"),
    Definition(key=DefinitionKey(name="graph", field="2", sub_categories=("d", "e")), content="a_graph"),
]


class TestDatabaseMd:
    def test_write_and_load_definitions(self, tmp_path: Path) -> None:
        # Given
        data_md_path = tmp_path / "md_db"
        DatabaseMd.serialize(definitions=_expected_definitions, db_path=data_md_path)

        # When
        db_md = DatabaseMd(data_md_path=data_md_path, load_cache=True)
        actual_definition_keys = db_md.get_index()
        actual_definitions = [
            db_md.get_definition(definition_key=definition_key) for definition_key in actual_definition_keys
        ]

        # Then
        expected_definitions_sorted: list[Definition] = sorted(_expected_definitions)
        actual_definitions_sorted: list[Definition] = sorted(actual_definitions)
        assert expected_definitions_sorted == actual_definitions_sorted
        assert all(
            definition.key.full_path == actual_definition.key.full_path
            for definition, actual_definition in zip(expected_definitions_sorted, actual_definitions_sorted)
        ), "Not all definitions have the same full path"
