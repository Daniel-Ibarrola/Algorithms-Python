from to_minisat import to_minisat


class Graph:
    """ A graph represented by an edge list. """

    def __init__(self, n_nodes: int, edge_list: list[tuple[int, int]]):
        self._n_nodes = n_nodes
        self._edge_list = edge_list

    @property
    def num_nodes(self) -> int:
        return self._n_nodes

    @property
    def num_edges(self) -> int:
        return len(self._edge_list)

    def three_color_cnf_expression(self) -> list[list[int]]:
        """ Returns an expression in CNF that must be satisfied if
            the graph can be colored with three colors.
        """
        # We will represent a vertex by three literals ranging from 1 to 3*|V|
        # For example vertex 1 will be represented by x1, x2 and x3 vertex 2 by x4, x5 and x6
        # and so on. Each literal for each node represents a color.
        clauses = []
        num_literals = 3 * self.num_nodes
        # There are three type of clauses that we must generate.
        # 1. At least one color  i.e (x1 or x2 or x3)
        for ii in range(1, num_literals + 1, 3):
            # All clauses must end with 0 to be read by minisat
            clauses.append([ii, ii + 1, ii + 2, 0])
        # 2. At most one color i.e (-x1 or -x2) and (-x1 or -x2) and (-x2 or -x3)
        for ii in range(1, num_literals + 1, 3):
            clauses.append([-ii, -(ii + 1), 0])
            clauses.append([-ii, -(ii + 2), 0])
            clauses.append([-(ii + 1), -(ii + 2), 0])
        # 3. Two nodes connected by an edge have different colors.
        # i.e (-x1 or -x4) and (-x2 or -x5) and (-x3 or -x6)
        edge_to_literal = list(range(1, num_literals, 3))
        for node_1, node_2 in self._edge_list:
            literal_1 = edge_to_literal[node_1 - 1]
            literal_2 = edge_to_literal[node_2 - 1]
            clauses.append([-literal_1, -literal_2, 0])
            clauses.append([-(literal_1 + 1), -(literal_2 + 1), 0])
            clauses.append([-(literal_1 + 2), -(literal_2 + 2), 0])

        assert len(clauses) == 4 * self.num_nodes + 3 * self.num_edges, \
            f"There are {len(clauses)} clauses"
        return clauses

    def to_minisat(self) -> str:
        """ Returns the result of passing the tree color CNF expression
            to the minisat program
        """
        expression = self.three_color_cnf_expression()
        num_literals = 3 * self.num_nodes
        return to_minisat(expression, num_literals)
