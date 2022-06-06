

class InvalidNodeError(ValueError):
    pass


class Graph:
    """ Graph class using an adjacency list representation.
    """
    def __init__(self, num_nodes: int = 0):
        self._num_nodes = num_nodes
        self._num_edges = 0
        self._adjacency_list = [[] for _ in range(num_nodes)]

    def _validate_node(self, node: int) -> None:
        if node < 0 or node >= self._num_nodes:
            raise InvalidNodeError(f"{node} is not a node of this graph")

    @property
    def num_nodes(self) -> int:
        """ Returns the number of nodes in the graph. """
        return self._num_nodes

    @property
    def num_edges(self) -> int:
        """ Returns the number of edges in the graph. """
        return self._num_edges

    @property
    def adjacency_list(self) -> list[list[int]]:
        """ Returns the adjacency list of the graph. """
        return self._adjacency_list

    def add_edge(self, node_1: int, node_2: int) -> None:
        """ Add an edge between the given nodes to the graph. """
        if not self.is_neighbor(node_1, node_2):
            self._adjacency_list[node_1].append(node_2)
            self._adjacency_list[node_2].append(node_1)
            self._num_edges += 1

    def add_node(self) -> None:
        """ Adds a node to the graph. """
        self.adjacency_list.append([])
        self._num_nodes += 1

    def is_neighbor(self, node_1: int, node_2: int) -> bool:
        """ Returns true uf the given nodes are neighbors. """
        self._validate_node(node_1)
        self._validate_node(node_2)

        if node_2 in self._adjacency_list[node_1]:
            return True
        return False

    def neighbors(self, node: int) -> list[int]:
        """ Returns the neighbors of the given node"""
        self._validate_node(node)
        return self._adjacency_list[node]

    def _path_between_util(self, current_node: int, end_node: int,
                           visited: list[bool]) -> bool:
        """ Util method to find if there is a path between two nodes
            using a recursive algorithm.
        """
        if current_node == end_node:
            return True

        is_reachable = False
        visited[current_node] = True

        for neighbor in self.adjacency_list[current_node]:
            if not visited[neighbor]:
                is_reachable = self._path_between_util(neighbor, end_node, visited)
                if is_reachable:
                    break

        return is_reachable

    def path_between(self, start_node: int, end_node: int) -> bool:
        """ Returns true if there is a path between the given nodes. """
        self._validate_node(start_node)
        self._validate_node(end_node)

        visited = [False] * self.num_nodes
        return self._path_between_util(start_node, end_node, visited)

    def _explore(self, current_node: int, visited: list[bool]) -> None:
        """ Explore the nodes reachable from the given node.
        """
        visited[current_node] = True
        for neighbor in self.adjacency_list[current_node]:
            if not visited[neighbor]:
                self._explore(neighbor, visited)

    def num_connected_components(self) -> int:
        """ Returns the number of connected components.

            Performs a depth first search while counting the number
            of connected components.
        """
        visited = [False] * self._num_nodes
        connected_components = 0

        for node in range(0, self._num_nodes):
            if not visited[node]:
                self._explore(node, visited)
                connected_components += 1

        return connected_components

    def __len__(self):
        return self._num_nodes

    def __repr__(self):
        return f"Graph(num_nodes={self._num_nodes}, num_edges={self._num_edges})"