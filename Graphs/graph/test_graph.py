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


def test_add_edges_from_list():
    graph = Graph(4)
    graph.add_edges([
        (0, 1), (1, 2), (2, 3), (3, 0)
    ])
    assert graph.num_edges == 4
    assert graph.is_neighbor(0, 1)
    assert graph.is_neighbor(1, 2)
    assert graph.is_neighbor(2, 3)
    assert graph.is_neighbor(3, 0)


def test_add_edges_to_node():
    graph = Graph(6)
    graph.add_edges_to_node(0, [1, 2, 3, 4])
    assert graph.num_edges == 4
    assert graph.is_neighbor(0, 1)
    assert graph.is_neighbor(0, 2)
    assert graph.is_neighbor(0, 3)
    assert graph.is_neighbor(0, 4)


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


def test_distances_from_node_and_shortest_path():
    graph_1 = Graph(4)
    graph_1.add_edges([
        (0, 1), (0, 2), (0, 3), (1, 2),
    ])
    assert graph_1.distances_from_node(1) == [1, 0, 1, 2]
    assert graph_1.shortest_path(1, 0) == 1
    assert graph_1.shortest_path(1, 2) == 1
    assert graph_1.shortest_path(1, 3) == 2

    graph_2 = Graph(5)
    graph_2.add_edges([
        (0, 2), (0, 3), (1, 4), (2, 3)
    ])
    assert graph_2.distances_from_node(0) == [0, float("inf"),
                                              1, 1, float("inf")]
    assert graph_2.shortest_path(0, 2) == 1
    assert graph_2.shortest_path(0, 3) == 1
    assert graph_2.shortest_path(0, 4) == -1
    assert graph_2.shortest_path(4, 1) == 1
    assert graph_2.shortest_path(4, 2) == -1

    graph_3 = Graph(9)
    graph_3.add_edges_to_node(0, [1, 2, 4, 5])
    graph_3.add_edges_to_node(1, [0, 2, 5, 6, 7])
    graph_3.add_edges_to_node(2, [0, 1, 3, 7])
    graph_3.add_edges_to_node(3, [2, 4, 7, 8])
    graph_3.add_edges_to_node(4, [0, 3, 5, 8])
    graph_3.add_edges_to_node(5, [0, 1, 4, 6, 8])
    graph_3.add_edges_to_node(6, [1, 5, 7, 8])
    graph_3.add_edges_to_node(7, [1, 2, 3, 6, 8])
    graph_3.add_edges_to_node(8, [3, 4, 5, 6, 7])
    assert graph_3.distances_from_node(6) == [
        2, 1, 2, 2, 2, 1, 0, 1, 1
    ]
    assert graph_3.shortest_path(6, 1) == 1
    assert graph_3.shortest_path(6, 2) == 2
    assert graph_3.shortest_path(0, 6) == 2


def test_is_graph_bipartite():

    empty_graph = Graph()
    assert empty_graph.is_bipartite()

    no_edges_graph = Graph(4)
    assert no_edges_graph.is_bipartite()

    graph_1 = Graph(4)
    graph_1.add_edges([
        (0, 1), (0, 2), (0, 3), (1, 2),
    ])
    assert not graph_1.is_bipartite()

    graph_2 = Graph(5)
    graph_2.add_edges([
        (0, 3), (1, 3), (1, 4), (2, 3),
    ])
    assert graph_2.is_bipartite()

    graph_3 = Graph(5)
    graph_3.add_edges([
        (0, 1), (1, 2), (1, 3), (2, 4), (3, 4)
    ])
    assert graph_3.is_bipartite()

    multi_component_graph_1 = Graph(7)
    multi_component_graph_1.add_edges([
        (0, 1), (1, 2), (2, 3),
        (4, 5), (4, 6), (5, 6),
    ])
    assert not multi_component_graph_1.is_bipartite()

    multi_component_graph_2 = Graph(8)
    multi_component_graph_2.add_edges([
        (0, 1), (1, 2), (2, 3),
        (4, 5), (5, 6), (6, 7),
        (7, 4),
    ])
    assert multi_component_graph_2.is_bipartite()
