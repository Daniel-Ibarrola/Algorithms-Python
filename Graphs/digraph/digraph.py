from enum import Enum
from collections import deque


class InvalidNodeError(ValueError):
    pass


class Colors(Enum):
    # Colors for labeling the nodes in the isCyclic function
    white = 0  # Node not processed
    gray = 1  # Node being processed
    black = 2  # Node completely processed


class Digraph:

    def __init__(self, num_nodes: int = 0):
        self._num_nodes = num_nodes
        self._num_edges = 0
        self._adjacency_list = [[] for _ in range(num_nodes)]

    @property
    def num_nodes(self):
        return self._num_nodes

    @property
    def num_edges(self):
        return self._num_edges

    @property
    def adjacency_list(self):
        return self._adjacency_list

    def from_edge_list(self, num_nodes: int,
                       edge_list: list[tuple[int, int]]) -> None:
        """ Create a graph from an edge list. """
        self._adjacency_list = [[] for _ in range(num_nodes)]
        self._num_nodes = num_nodes
        self.add_edges(edge_list)

    def _validate_node(self, node: int) -> None:
        """ Check if a node is part of the graph. """
        if node < 0 or node >= self._num_nodes:
            raise InvalidNodeError

    def add_edge(self, node_1: int, node_2: int) -> None:
        """ Adds an edge to the graph that goes from
            node_1 to node_2.
        """
        if not self.is_edge(node_1, node_2):
            self._adjacency_list[node_1].append(node_2)
            self._num_edges += 1

    def add_edges(self, edge_list: list[tuple[int, int]]) -> None:
        """ Adds multiple edges to the graph. """
        for edge in edge_list:
            self.add_edge(edge[0], edge[1])

    def is_edge(self, node_1: int, node_2: int) -> bool:
        """ Returns true if there is an edge that goes from
            node_1 to node_2.
        """
        self._validate_node(node_1)
        self._validate_node(node_2)

        if node_2 in self._adjacency_list[node_1]:
            return True
        return False

    def add_node(self) -> None:
        """ Add a new node to the graph. """
        self._num_nodes += 1
        self._adjacency_list.append([])

    def out_degree(self, node: int) -> int:
        """ Returns the out degree of the given node. """
        self._validate_node(node)
        return len(self._adjacency_list[node])

    def in_degree(self, node: int) -> int:
        """ Returns the in-degree of the given node. """
        self._validate_node(node)

        node_in_degree = 0
        for node_list in self._adjacency_list:
            for neighbor in node_list:
                if neighbor == node:
                    node_in_degree += 1

        return node_in_degree

    def _is_cyclic_util(self, node: int, colors: list[Colors]) -> bool:
        """ Traverse the nodes reachable from the given node,
            assigning them colors and if two adjacent nodes are found
            to be gray as cycle has been found.
        """
        # Mark the node as being processed
        colors[node] = Colors.gray

        for neighbor in self._adjacency_list[node]:

            # An adjacent node is gray too so there must be a cycle
            if colors[neighbor] == Colors.gray:
                return True
            if colors[neighbor] == Colors.white and self._is_cyclic_util(neighbor, colors):
                return True

        # No cycle was found. We mark the node as completely processed
        colors[node] = Colors.black
        return False

    def is_cyclic(self) -> bool:
        """ Returns True if the graph has a cycle. """

        # We use the coloring method to determine if the graph is cyclic
        # or not
        colors = [Colors.white] * self._num_nodes

        # Traverse the graph in DFS
        for node in range(self._num_nodes):
            if colors[node] == Colors.white and \
                    self._is_cyclic_util(node, colors):
                return True

        return False

    def _explore_and_stack(self, current_node: int,
                           visited: list[bool],
                           stack: deque) -> None:
        """ Explore the nodes reachable from the given node and put them
            in a stack.
        """
        visited[current_node] = True
        for node in self._adjacency_list[current_node]:
            if not visited[node]:
                self._explore_and_stack(node, visited, stack)

        stack.append(current_node)

    def topological_order(self) -> list[int]:
        """ Compute the topological ordering of the graph.
            Returns a list with the nodes.
        """
        if self.is_cyclic():
            return []
        # We do a DFS while pushing the nodes into a stack.
        # The stack will contain the nodes in reverse topological order
        visited = [False] * self._num_nodes
        stack = deque()
        for node in range(self._num_nodes):
            if not visited[node]:
                self._explore_and_stack(node, visited, stack)
        assert len(stack) == self._num_nodes

        topological_order = []
        while len(stack) > 0:
            topological_order.append(stack.pop())

        return topological_order

    def reverse(self) -> "Digraph":
        """ Returns the reverse graph. """
        reverse_graph = Digraph(self._num_nodes)
        for node in range(self._num_nodes):
            for neighbor in self._adjacency_list[node]:
                reverse_graph.add_edge(neighbor, node)

        return reverse_graph

    def _explore(self, current_node: int, visited: list[bool]) -> None:
        """ Traverse the nodes reachable from the given node. """
        visited[current_node] = True
        for node in self._adjacency_list[current_node]:
            if not visited[node]:
                self._explore(node, visited)

    def num_strongly_connected_components(self) -> int:
        """ Returns the number of strongly connected components. """

        # First we do a DFS of the original graph while pushing the nodes
        # into a stack
        visited = [False] * self._num_nodes
        stack = deque()
        for node in range(self._num_nodes):
            if not visited[node]:
                self._explore_and_stack(node, visited, stack)
        assert len(stack) == self._num_nodes

        reverse_graph = self.reverse()
        for ii in range(len(visited)):
            visited[ii] = False
        # Now we do a DFS of the reverse graph so, we can count the number of SCC
        num_scc = 0
        while len(stack) > 0:
            current_node = stack.pop()
            if not visited[current_node]:
                reverse_graph._explore(current_node, visited)
                num_scc += 1

        return num_scc
