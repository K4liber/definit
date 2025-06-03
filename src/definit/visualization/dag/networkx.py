from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Ellipse

from definit.dag.dag import DAG
from definit.dag.dag import Definition
from definit.dag.dag import DefinitionKey
from definit.db import get_database
from definit.definition.field import Field
from definit.definition.track import Track
from definit.visualization.dag.interface import DAGVisualizationAbstract

_field_to_color: dict[Field, str] = {}
_track_to_color: dict[Track, str] = {}


def _get_color_for_track(track: Track) -> str:
    if track not in _track_to_color:
        _track_to_color[track] = f"#{np.random.randint(0, 0xFFFFFF):06x}"

    return _track_to_color[track]

def _get_color_for_field(field: Field) -> str:
    if field not in _field_to_color:
        _field_to_color[field] = f"#{np.random.randint(0, 0xFFFFFF):06x}"

    return _field_to_color[field]

class DefinitionWithTrack(Definition):
    
    def __init__(self, key: DefinitionKey, content: str, track: Track) -> None:
        super().__init__(key=key, content=content)
        self._track = track
        
    @property
    def track(self) -> Track:
        return self._track


def _get_dag_with_rolled_definitions(dag: DAG, rolled_definitions: dict[Definition, Track]) -> DAG:
    """
    Create a new DAG with rolled definitions replaced by their tracks.
    This function creates a new DAG where each rolled definition is replaced by its corresponding track.
    If a definition is rolled, it will be replaced by its track in the new DAG.
    If a definition is not rolled, it will remain unchanged."""
    # Create a new DAG to avoid modifying the original
    new_dag = DAG()
    rolled_key_to_definition = {definition.key for definition in rolled_definitions}

    for node_from, node_to in dag.edges:
        node_from_definition = dag.get_node(node_from)

        if node_from_definition.key in rolled_key_to_definition:
            track = rolled_definitions[node_from_definition]
            node_from_key = DefinitionKey(name=str(track), field=track)
            node_from_definition = DefinitionWithTrack(key=node_from_key, content="", track=track)

        node_to_definition = dag.get_node(node_to)

        if node_to_definition.key in rolled_key_to_definition:
            track = rolled_definitions[node_to_definition]
            node_to_key = DefinitionKey(name=str(track), field=track)
            node_to_definition = DefinitionWithTrack(key=node_to_key, content="", track=track)

        if node_from_definition.key != node_to_definition.key:
            # Add the edge only if the nodes are not the same
            new_dag.add_edge(node_from_definition, node_to_definition)

    return new_dag


class DAGVisualizationNetworkX(DAGVisualizationAbstract):
    def show_circle(
        self,
        dag: DAG,
        track: Track | None = None,
        unrolled_tracks: set[Track] | None = None,
    ) -> None:
        if unrolled_tracks is not None:
            db = get_database()
            all_tracks: set[Track] = {track for track in Track}
            rolled_tracks: set[Track] = all_tracks - unrolled_tracks
            rolled_definitions: dict[Definition, Track] = {}

            for rolled_track in rolled_tracks:
                track_rolled_definition_keys = db.get_track(track=rolled_track)

                for track_rolled_definition_key in track_rolled_definition_keys:
                    rolled_definitions[db.get_definition(track_rolled_definition_key)] = rolled_track

            dag = _get_dag_with_rolled_definitions(dag=dag, rolled_definitions=rolled_definitions)

        graph = nx.DiGraph()
        edges = [(dag.get_node(node_from_key), dag.get_node(node_to_key)) for (node_from_key, node_to_key) in dag.edges]
        graph.add_edges_from(edges)  # type: ignore , networkx typing issue
        node_key_to_level = DAGVisualizationNetworkX.get_node_levels(graph=graph)

        # Group nodes by level
        nodes_by_level: dict[int, list[Definition]] = {}
        max_level = max(node_key_to_level.values()) if node_key_to_level else 0

        for level in range(max_level + 1):
            nodes_by_level[level] = [node for node, node_level in node_key_to_level.items() if node_level == level]

        # Calculate positions in orbital layout
        pos = {}
        for level in range(max_level + 1):
            nodes = nodes_by_level[level]
            # Base radius on level (inner circles for lower levels)
            radius = 0.2 + (level / max_level) * 0.8 if max_level > 0 else 0.5

            # Distribute nodes evenly around the circle at this radius
            for idx, node in enumerate(nodes):
                angle = (2 * np.pi * idx) / len(nodes) if len(nodes) > 1 else 0
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                pos[node] = (x, y)

        # Create visualization
        fig, ax = plt.subplots(figsize=(12, 12))

        # Draw edges with curved arrows
        for edge in graph.edges():
            # Create curved edge
            rad = 0.2  # controls curve intensity
            nx.draw_networkx_edges(
                graph,
                pos,
                edgelist=[edge],
                ax=ax,
                arrows=True,
                connectionstyle=f"arc3, rad = {rad}",
                edge_color="gray",
                alpha=0.3,
                width=0.5,
            )

        handles = []
        labels = []

        # Draw nodes
        for node, (x, y) in pos.items():
            if isinstance(node, DefinitionWithTrack):
                node_category = f"[TRACK] {node.track}"
                node_color = _get_color_for_track(track=node.track)
            elif isinstance(node, Definition):
                node_category = f"[FIELD] {node.key.field}"
                node_color = _get_color_for_field(field=node.key.field)

            # Calculate rotation angle based on position
            angle = np.degrees(np.arctan2(y, x))
            # Add 90 degrees to align with orbit
            angle += 90

            # Create rotated ellipse
            width = 0.1
            height = 0.05

            ellipse = Ellipse(
                (x, y),
                width=width,
                height=height,
                angle=angle,  # Apply rotation to ellipse
                facecolor=node_color,
                edgecolor="black",
                linewidth=0,
            )
            ax.add_patch(ellipse)
            ax.text(
                x,
                y,
                str(node.key.name),
                fontsize=8,
                ha="center",
                va="center",
                rotation=angle + 180,
                rotation_mode="anchor",
                color="black",
            )

            if node_category not in labels:
                handles.append(plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=node_color, markersize=10))
                labels.append(node_category)

        # Add level circles (optional visual guide)
        for level in range(max_level + 1):
            radius = 0.2 + (level / max_level) * 0.8 if max_level > 0 else 0.5
            circle = plt.Circle((0, 0), radius, fill=False, linestyle="--", alpha=0.2, color="gray")
            ax.add_patch(circle)

        no_nodes = len(graph.nodes())
        no_dependencies = len(graph.edges())
        root_name = f"'{track}'" if track else "All definitions"
        ax.set_title(
            f"{root_name} DAG (definitions={no_nodes}, dependencies={no_dependencies}, levels={max_level + 1}). "
        )

        ax.set_aspect("equal")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis("off")

        ax.legend(handles=handles, labels=labels, title="Legend", loc="lower left")
        fig.tight_layout(rect=(0.25, 0, 0.75, 1))
        plt.show()

    def show(self, dag: DAG, root: DefinitionKey | None = None) -> None:
        graph = nx.DiGraph()
        edges = [edge for edge in dag.edges]
        graph.add_edges_from(edges)
        no_levels = 0
        no_nodes = 0
        # calculate positions
        node_to_level = DAGVisualizationNetworkX.get_node_levels(graph=graph)

        for node, level in node_to_level.items():
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            graph.nodes[node]["layer"] = level
            no_levels = max(no_levels, level + 1)  # +1 because levels are 0-indexed
            no_nodes += 1

        pos = nx.multipartite_layout(graph, subset_key="layer", align="horizontal")
        fig, ax = plt.subplots(figsize=(8, 6))
        nx.draw_networkx_edges(graph, pos, ax=ax, arrows=False)

        # Get unique y-coordinates representing each level
        y_levels = sorted(set(y for _, y in pos.values()))

        # Draw horizontal level lines
        for y in y_levels:
            ax.axhline(y=y, color="gray", linestyle="--", alpha=0.2)

        # Draw nodes
        handles = []
        labels = []
        node_to_position: dict[DefinitionKey, tuple[float, float]] = {node: position for node, position in pos.items()}

        for node, (x, y) in node_to_position.items():
            node_field = node.field
            node_color = _get_color_for_field(field=node_field)
            ellipse = Ellipse(
                (x, y),
                width=0.2,
                height=0.1,
                facecolor=node_color,
                edgecolor="black",
                linewidth=(2 if node == root else 0),
            )
            ax.add_patch(ellipse)
            ax.text(x, y, str(node), fontsize=10, ha="center", va="center", color="black")
            # Add entry to legend if it's a new color
            if node_field not in labels:
                handles.append(plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=node_color, markersize=10))
                labels.append(node_field)

        no_dependencies = no_nodes - 1  # -1 because we are excluding root node
        root_name = f"'{root}'" if root else "All definitions"
        ax.set_title(f"{root_name} DAG (lvl={no_levels}, dependencies={no_dependencies})")
        ax.set_xlim(-0.5, 0.5)  # Adjust limits if needed
        y_values = [y for _, y in pos.values()]
        min_y, max_y = min(y_values), max(y_values)
        ax.set_ylim(min_y - 0.2, max_y + 0.3)  # Add extra space at the top
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis("off")  # Hide axes
        ax.legend(handles=handles, labels=labels, title="Knowledge fields", loc="upper right")
        fig.tight_layout()
        plt.show()

    @staticmethod
    def get_node_levels(graph: nx.DiGraph) -> dict[Definition, int]:
        node_levels: dict[Definition, int] = {}

        def update_node_level(node: Any) -> None:
            if node in node_levels:
                return

            children = list(graph.successors(node))

            if not children:  # leaf node
                node_levels[node] = 0
                return

            for child in children:
                update_node_level(node=child)

            # Node's level is max level of children + 1
            max_child_level = max((node_levels[child] for child in children))
            node_levels[node] = max_child_level + 1

        for node in graph.nodes():
            update_node_level(node=node)

        return node_levels
