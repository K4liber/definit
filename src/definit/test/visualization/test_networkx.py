import pytest

from definit.dag.dag import DefinitionKey
from definit.db.md import DatabaseMd
from definit.field import Field
from definit.track import Track
from definit.visualization.dag.networkx import DAGVisualizationNetworkX


class TestNetworkx:
    @pytest.mark.skip("manual test")
    def test_selected_definition_visualization(self) -> None:
        # Given
        definition_key = DefinitionKey(name="trie", field=Field.COMPUTER_SCIENCE)
        data_parser = DatabaseMd()
        data_parser._cache_index()
        dag = data_parser.get_dag_for_definition(root=definition_key)
        dag_visualization = DAGVisualizationNetworkX()
        # When
        dag_visualization.show(dag=dag, root=definition_key)
        # Then
        pass

    @pytest.mark.skip("manual test")
    def test_selected_track_circle_visualization(self) -> None:
        # Given
        data_parser = DatabaseMd()
        data_parser._cache_index()
        track = Track.DATA_STRUCTURES
        dag = data_parser.get_dag(track=track)
        dag_visualization = DAGVisualizationNetworkX()
        # When
        dag_visualization.show_circle(dag=dag, track=track, unrolled_tracks={track})
        # Then
        pass
