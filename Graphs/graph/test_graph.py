from graph import Graph, InvalidNodeError
import pytest


def test_graph_empty_constructor():
    g = Graph()
    assert g.num_nodes == 0
    assert g.num_edges == 0


def test_graph_constructor_with_number_of_nodes():
    g = Graph(5)
    assert g.num_nodes == 5
    assert g.num_edges == 0


def test_get_adjacency_list():
    g = Graph()
    assert len(g.adjacency_list) == 0

    g = Graph(6)
    assert len(g.adjacency_list) == 6

    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(2, 3)
    g.add_edge(4, 5)

    assert len(g.adjacency_list[0]) == 2
    assert len(g.adjacency_list[2]) == 2
    assert len(g.adjacency_list[4]) == 1


def test_number_of_edges_after_adding_edge():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert g.num_edges == 2


def test_adding_repeated_edge():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(0, 1)

    assert g.num_edges == 1
    assert g.is_neighbor(0, 1)


def test_is_neighbor():
    g = Graph(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert g.is_neighbor(0, 1)
    assert g.is_neighbor(1, 0)
    assert g.is_neighbor(1, 2)
    assert g.is_neighbor(2, 1)
    assert not g.is_neighbor(0, 2)
    assert not g.is_neighbor(2, 0)


def test_invalid_node_raises_error():
    g = Graph(3)

    with pytest.raises(InvalidNodeError):
        g.add_edge(0, 4)

    with pytest.raises(InvalidNodeError):
        g.add_edge(5, 4)

    with pytest.raises(InvalidNodeError):
        g.is_neighbor(0, 3)

    with pytest.raises(InvalidNodeError):
        g.is_neighbor(3, 0)


def test_add_nodes_and_edges():
    g = Graph()
    g.add_node()
    g.add_node()

    assert g.num_nodes == 2

    g.add_edge(0, 1)

    assert g.num_edges == 1
    assert g.is_neighbor(0, 1)


def test_get_neighbors():
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(2, 3)
    g.add_edge(3, 4)

    assert g.neighbors(0) == [1, 2, 3, 4]
    assert g.neighbors(1) == [0]
    assert g.neighbors(2) == [0, 3]
    assert g.neighbors(3) == [0, 2, 4]
    assert g.neighbors(4) == [0, 3]


@pytest.fixture
def c4_graph() -> Graph:
    """ Returns the C4 graph. """
    c4 = Graph(4)
    c4.add_edge(0, 1)
    c4.add_edge(0, 2)
    c4.add_edge(1, 3)
    c4.add_edge(2, 3)
    return c4


@pytest.fixture
def graph_with_two_connected_components() -> Graph:
    """ Returns a graph with 4 nodes and two connected components"""
    graph = Graph(4)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    return graph


@pytest.fixture
def graph_with_three_connected_components() -> Graph:
    """ Returns a graph with 8 nodes and three connected components
    """
    graph = Graph(8)
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    graph.add_edge(5, 6)
    graph.add_edge(6, 7)
    return graph


def test_path_between(c4_graph,
                      graph_with_two_connected_components,
                      graph_with_three_connected_components):
    assert c4_graph.path_between(0, 0)
    assert c4_graph.path_between(0, 1)
    assert c4_graph.path_between(0, 2)
    assert c4_graph.path_between(0, 3)

    graph_2 = graph_with_two_connected_components
    assert not graph_2.path_between(0, 3)
    assert not graph_2.path_between(1, 3)
    assert graph_2.path_between(0, 2)

    graph_3 = graph_with_three_connected_components
    assert graph_3.path_between(5, 7)
    assert not graph_3.path_between(6, 2)
    assert not graph_3.path_between(6, 3)


def test_number_of_connected_components(c4_graph,
                                        graph_with_two_connected_components,
                                        graph_with_three_connected_components):
    # Empty graph has 0 connected components
    g = Graph()
    assert g.num_connected_components() == 0

    # A graph with no edges has as many connected components as it has nodes
    g = Graph(20)
    assert g.num_connected_components() == 20

    assert c4_graph.num_connected_components() == 1

    assert graph_with_two_connected_components.num_connected_components() == 2

    assert graph_with_three_connected_components.num_connected_components() == 3


def test_graph_repr(c4_graph):
    assert str(c4_graph) == "Graph(num_nodes=4, num_edges=4)"
