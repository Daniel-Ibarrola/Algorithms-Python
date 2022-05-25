from disjoint_set import DisjointSets, IndexOutOfRangeError
import pytest


def test_constructor():
    djs = DisjointSets(size=10)
    assert len(djs.parent) == 10
    assert len(djs.rank) == 10


def test_make_set():
    djs = DisjointSets(size=5)
    for ii in range(0, 5):
        djs.make_set(ii)

    for ii in range(0, 5):
        assert djs.parent[ii] == ii
        assert djs.rank[ii] == 0

    with pytest.raises(IndexOutOfRangeError):
        djs.make_set(10)


@pytest.fixture
def disjoint_sets() -> list[DisjointSets]:
    """ Returns a List of disjoints sets to test """
    djs = DisjointSets(size=5, path_compression=False)
    for ii in range(0, 5):
        djs.make_set(ii)
    for ii in range(0, 4):
        djs.union(ii, ii + 1)

    djs_list = [djs]

    djs_2 = DisjointSets(size=12, path_compression=False)
    for ii in range(0, 12):
        djs_2.make_set(ii)
    djs_2.union(1, 9)
    djs_2.union(6, 4)
    djs_2.union(5, 0)
    djs_2.union(2, 3)
    djs_2.union(4, 10)
    djs_2.union(6, 7)
    djs_2.union(6, 2)
    djs_2.union(11, 1)
    djs_2.union(8, 5)

    djs_list.append(djs_2)
    return djs_list


def test_union_by_rank(disjoint_sets):

    assert disjoint_sets[0].parent == [1, 1, 1, 1, 1]
    assert disjoint_sets[0].rank == [0, 1, 0, 0, 0]

    assert disjoint_sets[1].parent == [0, 9, 3, 3, 3, 0, 4, 4, 0, 9, 4, 9]
    assert disjoint_sets[1].rank == [1, 0, 0, 2, 1, 0, 0, 0, 0, 1, 0, 0]


def test_find_no_compression(disjoint_sets):

    # Test with first disjoint set
    assert disjoint_sets[0].find(0) == 1
    assert disjoint_sets[0].find(1) == 1
    assert disjoint_sets[0].find(2) == 1
    assert disjoint_sets[0].find(3) == 1
    assert disjoint_sets[0].find(4) == 1

    # Test with second disjoint set
    assert disjoint_sets[1].find(0) == 0
    assert disjoint_sets[1].find(1) == 9
    assert disjoint_sets[1].find(2) == 3
    assert disjoint_sets[1].find(3) == 3
    assert disjoint_sets[1].find(4) == 3
    assert disjoint_sets[1].find(5) == 0
    assert disjoint_sets[1].find(6) == 3
    assert disjoint_sets[1].find(7) == 3
    assert disjoint_sets[1].find(8) == 0
    assert disjoint_sets[1].find(9) == 9
    assert disjoint_sets[1].find(10) == 3
    assert disjoint_sets[1].find(11) == 9


def test_find_with_compression():

    parent = [5, 2, 4, 8, 4, 11, 9, 11, 4, 4, 5, 2]
    rank = [0, 0, 3, 0, 4, 1, 0, 0, 1, 1, 0, 2]
    assert len(parent) == len(rank)

    djs = DisjointSets(size=12, path_compression=True)
    djs.parent = parent
    djs.rank = rank

    djs.find(5)
    assert djs.parent == [5, 2, 4, 8, 4, 4, 9, 11, 4, 4, 5, 4]
    assert djs.rank == rank

