

def hamiltonian_path_cnf(num_nodes: int,
                         edge_list: list[tuple[int, int]]) -> list[list[int]]:
    """ Returns a CNF formula for the hamiltonian path for the graph defined by the
        given edge list.

        The formula is satisfiable if there exists such a path and unsatisfiable if
        there isn't.

        The formula is obtaining by imposing 5 constrains to the nodes of the graph in
        the path.
    """
    expression = []
    node_belongs_to_path(num_nodes, expression)
    node_appears_once(num_nodes, expression)
    positions_occupied(num_nodes, expression)
    different_positions(num_nodes, expression)

    graph = Graph(num_nodes, edge_list)
    graph.connectivity_cnf(expression)

    return expression


def node_belongs_to_path(num_nodes: int, expression: list) -> None:
    """ Constrain each vertex to belong to a path. Updates
        the given expression.
    """
    # We create a literal for each node occupying the ith position in the path.
    # For a total of num_nodes**2 variables, starting at 1 and ending in num_nodes**2.
    literal = 1
    for ii in range(0, num_nodes):
        expression.append([])
        for jj in range(0, num_nodes):
            expression[ii].append(literal)
            literal += 1


def node_appears_once(num_nodes: int, expression: list) -> None:
    """ Constrain each vertex to appear only once in the path. Updates
        the given expression.
    """
    start = -1
    for ii in range(0, num_nodes):
        # All the literals corresponding to a node
        node_literals = list(range(start, start - num_nodes, -1))
        for jj in range(0, num_nodes):
            for kk in range(jj + 1, num_nodes):
                expression.append([node_literals[jj], node_literals[kk]])
        start -= num_nodes


def positions_occupied(num_nodes: int, expression: list) -> None:
    """ Constrain each position in the path to be occupied by some vertex.
        Updates the given expression.
    """
    start = 1
    iter_end = len(expression) + num_nodes
    for ii in range(len(expression), iter_end):
        expression.append([])
        for jj in range(0, num_nodes):
            expression[ii].append(start + jj * num_nodes)
        start += 1


def different_positions(num_nodes: int, expression: list) -> None:
    """ Constrain that does not allow two vertices to occupy the same
        position of a path. Updates the given expression.
    """
    start = -1
    for ii in range(0, num_nodes):

        path_literals = []
        for ll in range(0, num_nodes):
            path_literals.append(start - ll * num_nodes)

        for jj in range(0, num_nodes):
            for kk in range(jj + 1, num_nodes):
                expression.append([path_literals[jj], path_literals[kk]])
        start -= 1


class Graph:
    """ Undirected graph represented by an adjacency matrix.
    """

    def __init__(self, num_nodes: int, edge_list: list[tuple[int, int]]):
        self._adjacency_matrix = self.build_matrix(num_nodes, edge_list)

    @property
    def num_nodes(self):
        return len(self._adjacency_matrix)

    @staticmethod
    def build_matrix(num_nodes: int, edge_list: list[tuple[int, int]]) -> list[list[int]]:
        """ Builds the adjacency matrix for the graph.
        """
        matrix = [[False] * num_nodes for ii in range(0, num_nodes)]
        for edge in edge_list:
            matrix[edge[0] - 1][edge[1] - 1] = True
            matrix[edge[1] - 1][edge[0] - 1] = True

        return matrix

    def connectivity_cnf(self, expression: list) -> None:
        """ Returns a CNF formula for the nodes that are not connected. """
        num_nodes = self.num_nodes
        for ii in range(num_nodes):
            for jj in range(num_nodes):
                if ii != jj and not self._adjacency_matrix[ii][jj]:
                    for kk in range(num_nodes - 1):
                        lit_1 = -(1 + num_nodes*ii + kk)
                        lit_2 = -(2 + num_nodes*jj + kk)
                        expression.append([lit_1, lit_2])
