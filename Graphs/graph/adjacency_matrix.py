import numpy as np


class InvalidNodeError(ValueError):
    pass


class Graph:
    """ Graph class that uses an adjacency matrix to represent its nodes and edges."""
    def __init__(self, num_nodes: int = 0) -> None:
        self._adj_matrix = np.full((num_nodes, num_nodes),
                                   False)
        self._num_nodes = num_nodes
        self._num_edges = 0

    @property
    def num_nodes(self) -> int:
        """ Returns the number of nodes of the graph"""
        return self._num_nodes

    @property
    def num_edges(self) -> int:
        """ Returns the number of edges"""
        return self._num_edges

    @property
    def adjacency_matrix(self) -> np.ndarray:
        """ Returns the adjacency matrix of the graph"""
        return self._adj_matrix

    def _validate_node(self, node: int) -> None:
        if node < 0 or node >= self._num_nodes:
            raise InvalidNodeError(f"{node} is not a node of this graph")

    def add_edge(self, node_1: int, node_2: int) -> None:
        """ Adds an edge to the graph """
        self._validate_node(node_1)
        self._validate_node(node_2)

        self._adj_matrix[node_1][node_2] = True
        self._adj_matrix[node_2][node_1] = True
        self._num_edges += 1

    def is_neighbor(self, node_1: int, node_2: int) -> bool:
        """ Checks if the given nodes are neighbors (there is an edge
            between them).
        """
        self._validate_node(node_1)
        self._validate_node(node_2)

        return self._adj_matrix[node_1][node_2]

    def get_neighbors(self, node: int) -> list[int]:
        """ Returns the neighbors of a given node"""
        self._validate_node(node)

        neighbors = []
        for ii, is_neighbor in enumerate(self._adj_matrix[node]):
            if is_neighbor:
                neighbors.append(ii)

        return neighbors

    def num_neighbors(self, node: int) -> int:
        """ Returns the number of neighbors of the given node"""
        self._validate_node(node)

        neighbor_count = 0
        for is_neighbor in self._adj_matrix[node]:
            if is_neighbor:
                neighbor_count += 1
        return neighbor_count

    def __repr__(self) -> str:
        return f"Graph(num_nodes={self.num_nodes}, num_edges={self.num_edges})"
