import pytest
from adjacency_matrix import Graph, InvalidNodeError


def test_graph_constructor_no_nodes():
    graph = Graph()
    assert graph.num_nodes == 0


def test_graph_constructor_num_nodes():
    graph = Graph(5)
    assert graph.num_nodes == 5


def test_get_adjacency_matrix():
    graph = Graph(3)
    matrix = graph.adjacency_matrix
    assert matrix.shape == (3, 3)


def test_cannot_modify_matrix():
    graph = Graph(3)
    with pytest.raises(AttributeError):
        graph.adjacency_matrix = [0, 1, 1]


def test_number_of_edges():
    k3 = Graph(3)
    k3.add_edge(0, 1)
    k3.add_edge(0, 2)
    k3.add_edge(1, 2)

    assert k3.num_edges == 3


def test_is_neighbor():
    k3 = Graph(3)
    k3.add_edge(0, 1)
    k3.add_edge(0, 2)
    k3.add_edge(1, 2)

    assert k3.is_neighbor(0, 1)
    assert k3.is_neighbor(1, 0)
    assert k3.is_neighbor(0, 2)
    assert k3.is_neighbor(2, 0)
    assert k3.is_neighbor(1, 2)
    assert k3.is_neighbor(2, 1)

    graph = Graph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)

    assert graph.is_neighbor(0, 2)
    assert graph.is_neighbor(3, 4)
    assert not graph.is_neighbor(1, 4)


def test_get_neighbors():

    # Graph with no edges
    g = Graph(3)
    assert g.get_neighbors(1) == []

    k3 = Graph(3)
    k3.add_edge(0, 1)
    k3.add_edge(0, 2)
    k3.add_edge(1, 2)
    assert k3.get_neighbors(0) == [1, 2]


def test_num_neighbors():
    # Graph with no edges
    g = Graph(3)
    assert g.num_neighbors(2) == 0

    k3 = Graph(3)
    k3.add_edge(0, 1)
    k3.add_edge(0, 2)
    k3.add_edge(1, 2)
    assert k3.num_neighbors(0) == 2


def test_representation():
    g = Graph(5)
    assert str(g) == "Graph(num_nodes=5, num_edges=0)"

    g.add_edge(1, 2)
    g.add_edge(0, 3)
    assert str(g) == "Graph(num_nodes=5, num_edges=2)"


def test_invalid_node_raises_error():
    graph = Graph(3)
    with pytest.raises(InvalidNodeError):
        graph.add_edge(2, 4)
