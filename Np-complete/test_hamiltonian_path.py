import hamiltonian_path as hp
from to_minisat import to_minisat
import pytest


@pytest.fixture()
def hamiltonian_path_expression():
    constrain_1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    constrain_2 = [
        [-1, -2],
        [-1, -3],
        [-2, -3],
        [-4, -5],
        [-4, -6],
        [-5, -6],
        [-7, -8],
        [-7, -9],
        [-8, -9],
    ]
    constrain_3 = [
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
    ]
    constrain_4 = [
        [-1, -4],
        [-1, -7],
        [-4, -7],
        [-2, -5],
        [-2, -8],
        [-5, -8],
        [-3, -6],
        [-3, -9],
        [-6, -9],
    ]
    constrain_5 = [
        [-1, -8],
        [-2, -9],
        [-7, -2],
        [-8, -3],
    ]
    expression = (
        constrain_1, constrain_2, constrain_3, constrain_4, constrain_5
    )
    return expression


@pytest.fixture()
def graph_with_hamiltonian_path():
    edge_list = [
        (1, 2), (2, 3)
    ]
    num_nodes = 3
    return num_nodes, edge_list


def test_node_belongs_to_path(hamiltonian_path_expression):
    expression = []
    expected_expression = hamiltonian_path_expression[0]
    hp.node_belongs_to_path(3, expression)
    assert expected_expression == expression


def test_node_appears_once(hamiltonian_path_expression):
    expression = []
    expected_expression = hamiltonian_path_expression[1]
    hp.node_appears_once(3, expression)
    assert expected_expression == expression


def test_positions_occupied(hamiltonian_path_expression):
    expression = []
    expected_expression = hamiltonian_path_expression[2]
    hp.positions_occupied(3, expression)
    assert expected_expression == expression


def test_different_positions(hamiltonian_path_expression):
    expression = []
    expected_expression = hamiltonian_path_expression[3]
    hp.different_positions(3, expression)
    assert expected_expression == expression


def test_hamiltonian_path_cnf(hamiltonian_path_expression, graph_with_hamiltonian_path):
    expected_expression = []
    for constrain in hamiltonian_path_expression:
        expected_expression += constrain
    num_nodes, edge_list = graph_with_hamiltonian_path
    assert hp.hamiltonian_path_cnf(num_nodes, edge_list) == expected_expression


@pytest.fixture()
def graph_with_no_hamiltonian_path():
    edge_list = [
        (1, 2), (1, 3), (1, 4)
    ]
    num_nodes = 4
    return num_nodes, edge_list


def test_hamiltonian_path_cnf_minisat(graph_with_hamiltonian_path,
                                      graph_with_no_hamiltonian_path):
    num_nodes, edge_list = graph_with_hamiltonian_path
    expression = hp.hamiltonian_path_cnf(num_nodes, edge_list)
    num_literals = num_nodes * num_nodes
    assert "SAT" in to_minisat(expression, num_literals, add_zeros=True)

    num_nodes, edge_list = graph_with_no_hamiltonian_path
    expression = hp.hamiltonian_path_cnf(num_nodes, edge_list)
    num_literals = num_nodes * num_nodes
    assert "UNSAT" in to_minisat(expression, num_literals, add_zeros=True)


def test_init_graph(graph_with_hamiltonian_path):
    num_nodes, edge_list = graph_with_hamiltonian_path
    graph = hp.Graph(num_nodes, edge_list)
    assert graph.num_nodes == 3


def test_graph_adjacency_matrix(graph_with_hamiltonian_path,
                                graph_with_no_hamiltonian_path):
    num_nodes, edge_list = graph_with_hamiltonian_path
    adjacency_matrix = hp.Graph.build_matrix(num_nodes, edge_list)
    expected_matrix = [[False, True, False],
                       [True, False, True],
                       [False, True, False]]
    assert adjacency_matrix == expected_matrix

    num_nodes, edge_list = graph_with_no_hamiltonian_path
    adjacency_matrix = hp.Graph.build_matrix(num_nodes, edge_list)
    expected_matrix = [
        [False, True, True, True],
        [True, False, False, False],
        [True, False, False, False],
        [True, False, False, False],
    ]
    assert adjacency_matrix == expected_matrix


def test_connectivity_cnf(graph_with_hamiltonian_path,
                          graph_with_no_hamiltonian_path):
    num_nodes, edge_list = graph_with_hamiltonian_path
    graph = hp.Graph(num_nodes, edge_list)
    expected_expression = [
        [-1, -8],
        [-2, -9],
        [-7, -2],
        [-8, -3],
    ]
    expression = []
    graph.connectivity_cnf(expression)
    assert expression == expected_expression

    num_nodes, edge_list = graph_with_no_hamiltonian_path
    graph = hp.Graph(num_nodes, edge_list)
    expected_expression = [
        [-5, -10],
        [-6, -11],
        [-7, -12],
        [-5, -14],
        [-6, -15],
        [-7, -16],
        [-9, -6],
        [-10, -7],
        [-11, -8],
        [-9, -14],
        [-10, -15],
        [-11, -16],
        [-13, -6],
        [-14, -7],
        [-15, -8],
        [-13, -10],
        [-14, -11],
        [-15, -12],
    ]
    expression = []
    graph.connectivity_cnf(expression)
    assert expression == expected_expression
