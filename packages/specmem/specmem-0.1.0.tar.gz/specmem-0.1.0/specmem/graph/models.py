"""Data models for Impact Graph visualization."""

from dataclasses import dataclass, field
from enum import Enum


class NodeType(str, Enum):
    """Types of nodes in the impact graph."""

    SPEC = "spec"
    CODE = "code"
    TEST = "test"
    FEATURE = "feature"


class EdgeType(str, Enum):
    """Types of edges in the impact graph."""

    IMPLEMENTS = "implements"
    TESTED_BY = "tested_by"
    DEPENDS_ON = "depends_on"
    CONTAINS = "contains"


@dataclass
class GraphNode:
    """A node in the impact graph.

    Represents a spec, code file, test, or feature.
    """

    id: str
    type: NodeType
    label: str
    metadata: dict = field(default_factory=dict)

    # Optional position for layout (set by frontend)
    x: float | None = None
    y: float | None = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "type": self.type.value,
            "label": self.label,
            "metadata": self.metadata,
            "x": self.x,
            "y": self.y,
        }


@dataclass
class GraphEdge:
    """An edge in the impact graph.

    Represents a relationship between two nodes.
    """

    source: str  # Node ID
    target: str  # Node ID
    relationship: EdgeType
    weight: float = 1.0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "source": self.source,
            "target": self.target,
            "relationship": self.relationship.value,
            "weight": self.weight,
        }


@dataclass
class ImpactGraphData:
    """Complete graph data for visualization.

    Contains all nodes and edges for the impact graph.
    """

    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "nodes_by_type": self._count_by_type(),
            },
        }

    def _count_by_type(self) -> dict[str, int]:
        """Count nodes by type."""
        counts: dict[str, int] = {}
        for node in self.nodes:
            type_str = node.type.value
            counts[type_str] = counts.get(type_str, 0) + 1
        return counts

    def filter_by_type(self, node_types: list[NodeType]) -> "ImpactGraphData":
        """Filter graph to only include specified node types.

        Args:
            node_types: List of node types to include

        Returns:
            New ImpactGraphData with filtered nodes and edges
        """
        # Filter nodes
        filtered_nodes = [n for n in self.nodes if n.type in node_types]
        filtered_node_ids = {n.id for n in filtered_nodes}

        # Filter edges to only include those between filtered nodes
        filtered_edges = [
            e for e in self.edges if e.source in filtered_node_ids and e.target in filtered_node_ids
        ]

        return ImpactGraphData(nodes=filtered_nodes, edges=filtered_edges)

    def get_connected_nodes(self, node_id: str) -> set[str]:
        """Get all nodes connected to a given node.

        Args:
            node_id: ID of the node to find connections for

        Returns:
            Set of connected node IDs
        """
        connected = set()
        for edge in self.edges:
            if edge.source == node_id:
                connected.add(edge.target)
            elif edge.target == node_id:
                connected.add(edge.source)
        return connected
