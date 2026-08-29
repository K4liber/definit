from pathlib import Path

from definit.dag.dag import DefinitionKey
from definit.db.md import DatabaseMd
from definit.definition.definition import Definition
from definit.definition.definition_group import DefinitionGroup

_dsa_group = DefinitionGroup(name="Data Structures and Algorithms")
_advanced_group = DefinitionGroup(name="Advanced Concepts")

_expected_definitions: list[Definition] = [
    Definition(key=DefinitionKey(name="list", field="1"), content="a_list", aliases=("array", "sequence")),
    Definition(key=DefinitionKey(name="node", field="1"), content="a_node"),
    Definition(key=DefinitionKey(name="tree", field="2"), content="a_tree"),
    Definition(key=DefinitionKey(name="graph", field="2"), content="a_graph [node](1/node)"),
]

# a single definition can belong to multiple groups
_expected_groups: set[DefinitionGroup] = {
    DefinitionGroup(
        name=_dsa_group.name,
        definitions=(
            _expected_definitions[1],  # node
            _expected_definitions[2],  # tree
        ),
    ),
    DefinitionGroup(
        name=_advanced_group.name,
        definitions=(
            _expected_definitions[2],  # tree
            _expected_definitions[3],  # graph
        ),
    ),
}


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
        assert all(
            definition.aliases == actual_definition.aliases
            for definition, actual_definition in zip(expected_definitions_sorted, actual_definitions_sorted)
        ), "Not all definitions have the same aliases"

    def test_groups_are_serialized_and_loaded(self, tmp_path: Path) -> None:
        # Given
        data_md_path = tmp_path / "md_db"
        DatabaseMd.serialize(
            definitions=_expected_definitions,
            db_path=data_md_path,
            groups=_expected_groups,
        )

        # When
        db_md = DatabaseMd(data_md_path=data_md_path, load_cache=True)

        # Then
        actual_groups = db_md.get_groups()
        assert {group.name for group in actual_groups} == {group.name for group in _expected_groups}
        for expected_group in _expected_groups:
            (actual_group,) = [group for group in actual_groups if group.name == expected_group.name]
            assert actual_group.definition_keys == expected_group.definition_keys

    def test_get_index_filtered_by_group(self, tmp_path: Path) -> None:
        # Given
        data_md_path = tmp_path / "md_db"
        DatabaseMd.serialize(
            definitions=_expected_definitions,
            db_path=data_md_path,
            groups=_expected_groups,
        )
        db_md = DatabaseMd(data_md_path=data_md_path, load_cache=True)

        # When
        actual_dsa_keys = db_md.get_index(group=_dsa_group)
        actual_advanced_keys = db_md.get_index(group=_advanced_group)

        # Then
        assert actual_dsa_keys == {_expected_definitions[1].key, _expected_definitions[2].key}
        assert actual_advanced_keys == {_expected_definitions[2].key, _expected_definitions[3].key}

    def test_get_index_filtered_by_field_and_group(self, tmp_path: Path) -> None:
        # Given
        data_md_path = tmp_path / "md_db"
        DatabaseMd.serialize(
            definitions=_expected_definitions,
            db_path=data_md_path,
            groups=_expected_groups,
        )
        db_md = DatabaseMd(data_md_path=data_md_path, load_cache=True)

        # When
        actual_definition_keys = db_md.get_index(field="1", group=_dsa_group)

        # Then
        assert actual_definition_keys == {DefinitionKey(name="node", field="1")}

    def test_no_groups_file_written_when_no_groups(self, tmp_path: Path) -> None:
        # Given
        data_md_path = tmp_path / "md_db"
        definitions_without_groups = [
            Definition(key=DefinitionKey(name="list", field="1"), content="a_list"),
        ]

        # When
        DatabaseMd.serialize(definitions=definitions_without_groups, db_path=data_md_path)

        # Then
        assert not (data_md_path / "groups.md").exists()
        db_md = DatabaseMd(data_md_path=data_md_path, load_cache=True)
        assert db_md.get_groups() == set()
