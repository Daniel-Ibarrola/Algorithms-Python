from graph_coloring import Graph
from to_minisat import to_minisat


def three_coloring_c3_cnf():
    """ Returns the expression in CNF for the C3 graph. """
    expression = [
        # At least one color
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        # At most one color
        [-1, -2],
        [-1, -3],
        [-2, -3],
        [-4, -5],
        [-4, -6],
        [-5, -6],
        [-7, -8],
        [-7, -9],
        [-8, -9],
        # Different colors
        [-1, -4],
        [-2, -5],
        [-3, -6],
        [-1, -7],
        [-2, -8],
        [-3, -9],
        [-4, -7],
        [-5, -8],
        [-6, -9],
    ]
    for clause in expression:
        clause.append(0)
    return expression


def test_three_colors_cnf_satisfied():
    n_variables = 9
    expression = three_coloring_c3_cnf()
    result = to_minisat(expression, n_variables)
    assert "SAT" in result


def test_graph_to_cnf_formula():
    edge_list = [
        (1, 2),
        (1, 3),
        (2, 3),
    ]
    n_nodes = 3
    graph = Graph(n_nodes, edge_list)
    expression = graph.three_color_cnf_expression()
    expected_expression = three_coloring_c3_cnf()
    assert expression == expected_expression


def test_three_colors_cnf_not_satisfied():
    # This edge list represent C4 graph. It cannot be three colored.
    edge_list = [
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
    ]
    n_nodes = 4
    graph = Graph(n_nodes, edge_list)
    result = graph.to_minisat()
    assert "UNSAT" in result
