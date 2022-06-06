from digraph import Digraph, InvalidNodeError
import pytest


def test_digraph_default_constructor():
    graph = Digraph()
    assert graph.num_nodes == 0
    assert graph.num_edges == 0


def test_digraph_number_of_nodes_constructor():
    graph = Digraph(5)
    assert graph.num_nodes == 5
    assert graph.num_edges == 0


def test_create_graph_from_edge_list():
    graph = Digraph()
    graph.from_edge_list(5, [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
    ])
    assert graph.num_nodes == 5
    assert graph.num_edges == 4


def test_cannot_modify_number_of_nodes_and_edges():
    graph = Digraph(3)
    assert graph.num_nodes == 3

    with pytest.raises(AttributeError):
        graph.num_nodes = 5

    with pytest.raises(AttributeError):
        graph.num_edges = 6


def test_get_adjacency_list():
    graph = Digraph(4)
    adj_list = graph.adjacency_list
    assert len(adj_list) == 4


def test_cannot_modify_adjacency_list():
    graph = Digraph(4)

    with pytest.raises(AttributeError):
        graph.adjacency_list = [1, 2, 3]


def test_add_edges_to_graph():
    graph = Digraph(3)
    graph.add_edge(0, 1)
    assert graph.num_edges == 1
    assert graph.is_edge(0, 1)
    assert not graph.is_edge(1, 0)

    graph.add_edge(1, 0)
    assert graph.num_edges == 2
    assert graph.is_edge(1, 0)


def test_invalid_node_throws_error():

    graph = Digraph(3)
    with pytest.raises(InvalidNodeError):
        graph.add_edge(1, 4)
    with pytest.raises(InvalidNodeError):
        graph.is_edge(3, 2)


def test_add_repeated_edges_doesnt_modify_graph():
    graph = Digraph(3)
    graph.add_edge(0, 1)
    graph.add_edge(0, 1)
    graph.add_edge(0, 1)
    assert graph.num_edges == 1
    assert graph.is_edge(0, 1)


def test_add_nodes_and_edges():
    graph = Digraph()
    graph.add_node()
    graph.add_node()
    graph.add_node()

    assert graph.num_nodes == 3

    graph.add_edge(0, 1)
    graph.add_edge(2, 0)
    assert graph.num_edges == 2
    assert graph.is_edge(0, 1)
    assert graph.is_edge(2, 0)


def test_add_edges_from_list():
    graph = Digraph(4)
    graph.add_edges([
        (0, 1),
        (0, 2),
        (2, 3),
        (3, 2)
    ])

    assert graph.num_edges == 4
    assert graph.is_edge(0, 1)
    assert graph.is_edge(3, 2)


def test_node_out_degree():
    graph = Digraph(5)
    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(0, 4)
    graph.add_edge(1, 0)
    graph.add_edge(2, 0)

    assert graph.out_degree(0) == 3
    assert graph.out_degree(1) == 1
    assert graph.out_degree(2) == 1


def test_in_degree():
    graph = Digraph(5)
    graph.add_edge(0, 3)
    graph.add_edge(1, 3)
    graph.add_edge(2, 3)
    graph.add_edge(4, 3)
    graph.add_edge(2, 0)
    graph.add_edge(4, 2)
    graph.add_edge(1, 2)

    assert graph.in_degree(3) == 4
    assert graph.in_degree(0) == 1
    assert graph.in_degree(2) == 2


def test_is_graph_cyclic():

    empty_graph = Digraph()
    assert not empty_graph.is_cyclic()

    no_edges_graph = Digraph(5)
    assert not no_edges_graph.is_cyclic()

    cyclic_graph_1 = Digraph(4)
    cyclic_graph_1.add_edge(0, 1)
    cyclic_graph_1.add_edge(1, 2)
    cyclic_graph_1.add_edge(2, 0)
    cyclic_graph_1.add_edge(3, 0)
    assert cyclic_graph_1.is_cyclic()

    cyclic_graph_2 = Digraph(8)
    cyclic_graph_2.add_edge(0, 1)
    cyclic_graph_2.add_edge(1, 2)
    cyclic_graph_2.add_edge(2, 3)
    cyclic_graph_2.add_edge(3, 4)
    cyclic_graph_2.add_edge(4, 5)
    cyclic_graph_2.add_edge(5, 6)
    cyclic_graph_2.add_edge(6, 7)
    cyclic_graph_2.add_edge(7, 0)
    assert cyclic_graph_2.is_cyclic()

    non_cyclic_graph_1 = Digraph(5)
    non_cyclic_graph_1.add_edge(0, 3)
    non_cyclic_graph_1.add_edge(0, 2)
    non_cyclic_graph_1.add_edge(0, 1)
    non_cyclic_graph_1.add_edge(1, 2)
    non_cyclic_graph_1.add_edge(1, 4)
    non_cyclic_graph_1.add_edge(2, 3)
    non_cyclic_graph_1.add_edge(2, 4)
    assert not non_cyclic_graph_1.is_cyclic()

    non_cyclic_graph_2 = Digraph(8)
    non_cyclic_graph_2.add_edge(0, 1)
    non_cyclic_graph_2.add_edge(1, 2)
    non_cyclic_graph_2.add_edge(2, 3)
    non_cyclic_graph_2.add_edge(3, 4)
    non_cyclic_graph_2.add_edge(4, 5)
    non_cyclic_graph_2.add_edge(5, 6)
    non_cyclic_graph_2.add_edge(6, 7)
    non_cyclic_graph_2.add_edge(0, 7)
    assert not non_cyclic_graph_2.is_cyclic()


def test_topological_ordering_cyclic_graph():
    # A cyclic graph does not have a topological ordering
    # so, it must return an empty list
    cyclic_graph_1 = Digraph(4)
    cyclic_graph_1.add_edge(0, 1)
    cyclic_graph_1.add_edge(1, 2)
    cyclic_graph_1.add_edge(2, 0)
    cyclic_graph_1.add_edge(3, 0)
    assert isinstance(cyclic_graph_1.topological_order(), list)
    assert len(cyclic_graph_1.topological_order()) == 0


def test_topological_ordering_DAG():
    # Test topological ordering for different DAGs
    graph_1 = Digraph(4)
    graph_1.add_edges([
        (0, 1), (2, 0), (3, 0)
    ])
    assert graph_1.topological_order() == [3, 2, 0, 1]

    graph_2 = Digraph(4)
    graph_2.add_edge(2, 0)
    assert graph_2.topological_order() == [3, 2, 1, 0]

    graph_3 = Digraph(5)
    graph_3.add_edges([
        (1, 0),
        (2, 0),
        (2, 1),
        (3, 0),
        (3, 2),
        (4, 1),
        (4, 2),
    ])
    assert graph_3.topological_order() == [4, 3, 2, 1, 0]

    graph_4 = Digraph(4)
    graph_4.add_edges([
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 3),
    ])
    assert graph_4.topological_order() == [0, 2, 1, 3]


def test_reverse_graph():

    empty_graph = Digraph()
    reverse = empty_graph.reverse()
    assert reverse.num_nodes == 0
    assert reverse.num_edges == 0

    no_edges_graph = Digraph(5)
    reverse = no_edges_graph.reverse()
    assert reverse.num_nodes == 5
    assert reverse.num_edges == 0

    graph = Digraph(4)
    graph.add_edges([(0, 1), (2, 0), (3, 0)])
    reverse = graph.reverse()
    assert reverse.num_edges == 3
    assert reverse.num_nodes == 4
    assert not reverse.is_edge(0, 1)
    assert not reverse.is_edge(2, 0)
    assert not reverse.is_edge(3, 0)
    assert reverse.is_edge(1, 0)
    assert reverse.is_edge(0, 2)
    assert reverse.is_edge(0, 3)


def test_strongly_connected_components():

    empty_graph = Digraph()
    assert empty_graph.num_strongly_connected_components() == 0

    no_edges_graph = Digraph(20)
    assert no_edges_graph.num_strongly_connected_components() == 20

    graph_1 = Digraph(4)
    graph_1.add_edges([(0, 1), (1, 2), (2, 0), (3, 0)])
    assert graph_1.num_strongly_connected_components() == 2

    graph_2 = Digraph(5)
    graph_2.add_edges([
        (1, 0),
        (2, 0),
        (2, 1),
        (3, 0),
        (3, 2),
        (4, 1),
        (4, 2),
    ])
    assert graph_2.num_strongly_connected_components() == 5

    graph_3 = Digraph(9)
    graph_3.add_edges([
        (0, 1),
        (1, 4),
        (1, 5),
        (2, 1),
        (3, 0),
        (3, 6),
        (4, 0),
        (4, 2),
        (4, 7),
        (6, 7),
        (7, 8),
        (8, 5),
        (8, 7),
    ])
    assert graph_3.num_strongly_connected_components() == 5

