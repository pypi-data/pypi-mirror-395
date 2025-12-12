from abc import ABC

import networkx as nx
import matplotlib.pyplot as plt
from .data_constraint import (
    DataVertex, ConceptVertex,
)
from typedb.driver import (Concept, Relation, Entity, Attribute)


class MatplotlibVisualizer(ABC):  # Keep it static
    NODE_ATTRIBUTES = None  # Late initialized

    def draw(graph: nx.MultiDiGraph):
        node_attributes = {node: MatplotlibVisualizer._get_attributes(node) for node in graph.nodes}
        node_shapes = {node: node_attributes[node][1] for node in graph.nodes}

        pos = nx.forceatlas2_layout(graph) if hasattr(nx, 'forceatlas2_layout') else nx.planar_layout(graph)
        nodes_by_shape = {node_shapes[n]: [] for n in graph.nodes}
        for node in graph.nodes:
            nodes_by_shape[node_shapes[node]].append(node)
        for (shape, node_subset) in nodes_by_shape.items():
            node_colors = [node_attributes[node][0] for node in node_subset]
            node_labels = {node: node_attributes[node][2](node) for node in node_subset}
            nx.draw_networkx_nodes(graph, pos, nodelist=nodes_by_shape[shape], node_color=node_colors, node_shape=shape)
            nx.draw_networkx_labels(graph, pos, labels = node_labels)
        nx.draw_networkx_edges(graph, pos)
        edge_labels = { (u,v): edge_type for (u, v, edge_type) in graph.edges(data="label")}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        plt.show()

    def _entity_relation_label(vertex: ConceptVertex):
        concept = vertex.concept
        return f"{concept.get_type().get_label()}({concept.get_iid()[-4:]})"

    def _attribute_value_as_label(vertex: ConceptVertex):
        concept = vertex.concept
        return f"{concept.get_type().get_label()}({concept.get_value()})"

    def _get_attributes(node: DataVertex):
        what = node.concept if isinstance(node, ConceptVertex) else node
        found = [c for c in MatplotlibVisualizer.NODE_ATTRIBUTES.keys() if c and isinstance(what, c)]
        key = found[0] if len(found) > 0 else None
        return MatplotlibVisualizer.NODE_ATTRIBUTES[key]

    # start


MatplotlibVisualizer.NODE_ATTRIBUTES = {
    Relation: ("b", "s", MatplotlibVisualizer._entity_relation_label),
    Entity: ("r", "o", MatplotlibVisualizer._entity_relation_label),
    Attribute: ("g", "o", MatplotlibVisualizer._attribute_value_as_label),
    None: ("c", "o", str),  # DEFAULT
}
