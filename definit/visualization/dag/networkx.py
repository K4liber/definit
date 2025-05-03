from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Ellipse

from definit.dag.dag import DAG
from definit.dag.dag import DefinitionKey
from definit.field import Field
from definit.track import Track
from definit.visualization.dag.interface import DAGVisualizationAbstract

_node_colors = {Field.COMPUTER_SCIENCE: "lightblue", Field.MATHEMATICS: "yellow"}


class DAGVisualizationNetworkX(DAGVisualizationAbstract):
    def show_circle(self, dag: DAG, track: Track | None = None) -> None:
        graph = nx.DiGraph()
        edges = [edge for edge in dag.edges]
        graph.add_edges_from(edges)

        # Calculate level for each node
        levels = {}

        for node in graph.nodes():
            DAGVisualizationNetworkX.get_node_level(graph=graph, node=node, node_levels=levels)

        # Group nodes by level
        nodes_by_level = {}
        max_level = max(levels.values()) if levels else 0
        for level in range(max_level + 1):
            nodes_by_level[level] = [node for node, node_level in levels.items() if node_level == level]

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
            node_field = node.field
            node_color = _node_colors[node_field]
            level = levels[node]

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
                str(node),
                fontsize=8,
                ha="center",
                va="center",
                rotation=angle + 180,
                rotation_mode="anchor",
                color="black",
            )

            if node_field not in labels:
                handles.append(plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=node_color, markersize=10))
                labels.append(node_field)

        # Add level circles (optional visual guide)
        for level in range(max_level + 1):
            radius = 0.2 + (level / max_level) * 0.8 if max_level > 0 else 0.5
            circle = plt.Circle((0, 0), radius, fill=False, linestyle="--", alpha=0.2, color="gray")
            ax.add_patch(circle)

        no_nodes = len(graph.nodes())
        no_dependencies = len(graph.edges())
        root_name = f"'{track}'" if track else "All definitions"
        ax.set_title(
            f"{root_name} DAG (definitions={no_nodes}, dependencies={no_dependencies}, levels={max_level + 1})"
        )

        ax.set_aspect("equal")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis("off")

        ax.legend(
            handles=handles, labels=labels, title="Knowledge fields", loc="upper right", bbox_to_anchor=(1.1, 1.1)
        )
        fig.tight_layout()
        plt.show()

    def show(self, dag: DAG, root: DefinitionKey | None = None) -> None:
        graph = nx.DiGraph()
        edges = [edge for edge in dag.edges]
        graph.add_edges_from(edges)
        no_levels = 0
        no_nodes = 0
        # calculate positions
        levels = {}

        for node in graph.nodes():
            level = DAGVisualizationNetworkX.get_node_level(graph=graph, node=node, node_levels=levels)
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
            node_color = _node_colors[node_field]
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
    def get_node_level(graph: nx.DiGraph, node: Any, node_levels: dict[Any, int]) -> int:
        if node in node_levels:
            return node_levels[node]

        children = list(graph.successors(node))
        if not children:  # leaf node
            node_levels[node] = 0
            return 0

        # Node's level is max level of children + 1
        max_child_level = max(
            DAGVisualizationNetworkX.get_node_level(graph=graph, node=child, node_levels=node_levels)
            for child in children
        )
        node_levels[node] = max_child_level + 1
        return node_levels[node]
