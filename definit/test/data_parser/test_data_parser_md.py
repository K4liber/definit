from definit.dag.dag import DefinitionKey
from definit.data_parser.md import DataParserMd
from definit.field import Field
from definit.test.common import CONST


class TestDataParserMD:
    def test_list_definition(self) -> None:
        # Given
        data_parser = DataParserMd(data_md_path=CONST.PACKAGE_ROOT_DIR.parent / "data_md")
        definition_key_list = DefinitionKey(name="list", field=Field.COMPUTER_SCIENCE)
        # When
        dag = data_parser.get_dag_for_definition(root=definition_key_list)
        # Then
        assert dag is not None
        assert len([edge for edge in dag.edges]) == 15
        assert len(dag.nodes) == 11

    def test_parse_all_definitions(self) -> None:
        # Given
        data_parser = DataParserMd(data_md_path=CONST.PACKAGE_ROOT_DIR.parent / "data_md")
        # When
        index = data_parser.get_index()
        # Then
        assert index is not None
        assert len(index) == 62
        [data_parser.get_dag_for_definition(root=definition) for definition in index]
