from splay import SplayTree, Node
from splay import NoRightChildError, NoLeftChildError, ParentNotRootError, KeyNotInTreeError
import pytest


# Methods to implement the splay operation #

def test_right_rotation():
    # Test rotation with tree nodes
    root = Node(3, None)
    root.left = Node(2, root)
    root.left.left = Node(1, root.left)

    root = SplayTree._right_rotation(root)

    assert root.key == 2
    assert root.left.key == 1
    assert root.right.key == 3
    assert root.parent is None

    assert root.left.parent.key == 2
    assert root.right.parent.key == 2

    # Test raises error
    root = Node(3, None)
    root.right = Node(2, root)
    with pytest.raises(NoLeftChildError):
        SplayTree._right_rotation(root)

    # Test rotation with a tree
    tree = SplayTree()
    nodes = [3.0, 2.0, 1.0, 4.0, 2.5]
    for n in nodes:
        tree.insert_no_splay(n)

    assert tree.n_nodes == len(nodes)
    root = tree.root
    root = SplayTree._right_rotation(root)

    assert root.key == 2.0
    assert root.left.key == 1.0
    assert root.right.key == 3.0
    assert root.parent is None

    assert root.left.parent.key == 2.0
    assert root.right.parent.key == 2.0

    assert root.left.left is None
    assert root.left.right is None

    assert root.right.left.key == 2.5
    assert root.right.right.key == 4.0


def test_left_rotation():
    # Test rotation with tree nodes
    root = Node(1, None)
    root.right = Node(2, root)
    root.right.right = Node(3, root.right)

    root = SplayTree._left_rotation(root)

    assert root.key == 2
    assert root.left.key == 1
    assert root.right.key == 3
    assert root.parent is None

    assert root.left.parent.key == 2
    assert root.right.parent.key == 2

    # Test raises error
    root = Node(3, None)
    root.left = Node(2, root)
    with pytest.raises(NoRightChildError):
        SplayTree._left_rotation(root)

    # Test rotation with a tree
    tree = SplayTree()
    nodes = [1.0, 2.0, 3.0, 0.5, 1.5]
    for n in nodes:
        tree.insert_no_splay(n)

    assert tree.n_nodes == len(nodes)
    root = tree.root
    root = SplayTree._left_rotation(root)

    assert root.key == 2.0
    assert root.left.key == 1.0
    assert root.right.key == 3.0
    assert root.parent is None

    assert root.left.parent.key == 2.0
    assert root.right.parent.key == 2.0

    assert root.left.left.key == 0.5
    assert root.left.right.key == 1.5


def test_zig():
    # Test zig with nodes
    root = Node(3, None)
    root.left = Node(2, root)
    root.left.left = Node(1, root.left)

    # Should be a right rotation
    root = SplayTree._zig(root.left)
    assert root.key == 2
    assert root.left.key == 1
    assert root.right.key == 3
    assert root.parent is None
    assert root.left.parent.key == 2
    assert root.right.parent.key == 2

    # Test raises error
    root = Node(4, None)
    root.left = Node(3, root)
    root.left.left = Node(2, root.left)
    root.left.left.left = Node(1, root.left.left)
    with pytest.raises(ParentNotRootError):
        SplayTree._zig(root.left.left.left)

    # Test with tree
    # Should be a left rotation
    tree = SplayTree()
    nodes = [1.0, 2.0, 3.0, 0.5, 1.5]
    for n in nodes:
        tree.insert_no_splay(n)

    tree.root = SplayTree._zig(tree.root.right)

    assert tree.root.key == 2.0
    assert tree.root.left.key == 1.0
    assert tree.root.right.key == 3.0
    assert tree.root.parent is None

    assert tree.root.left.parent.key == 2.0
    assert tree.root.right.parent.key == 2.0

    assert tree.root.left.left.key == 0.5
    assert tree.root.left.right.key == 1.5


def test_zig_zig_left():
    # Test zig-zig with nodes
    root = Node(3, None)
    root.left = Node(2, root)
    root.left.left = Node(1, root.left)

    root = SplayTree._zig_zig_left(root.left.left)
    assert root.parent is None
    assert root.key == 1
    assert root.left is None
    assert root.right.key == 2
    assert root.right.right.key == 3

    # Test zig-zig with tree
    tree = SplayTree()
    nodes = [8, 6, 4, 3, 5, 7, 9]
    for n in nodes:
        tree.insert_no_splay(n)

    tree.root = tree._zig_zig_left(tree.root.left.left)
    root = tree.root
    assert root.parent is None
    assert root.key == 4
    assert root.left.key == 3
    assert root.right.key == 6
    assert root.right.left.key == 5
    assert root.right.right.key == 8
    assert root.right.right.right.key == 9


def test_zag_zag_right():
    # Test zag-zag with nodes
    root = Node(1, None)
    root.right = Node(2, root)
    root.right.right = Node(3, root.right)

    root = SplayTree._zag_zag_right(root.right.right)
    assert root.parent is None
    assert root.key == 3
    assert root.right is None
    assert root.left.key == 2
    assert root.left.left.key == 1

    # Test zig-zig with tree
    tree = SplayTree()
    nodes = [4, 6, 8, 3, 5, 7, 9]
    for n in nodes:
        tree.insert_no_splay(n)

    tree.root = tree._zag_zag_right(tree.root.right.right)
    root = tree.root
    assert root.parent is None
    assert root.key == 8
    assert root.right.key == 9
    assert root.left.key == 6
    assert root.left.left.key == 4
    assert root.left.right.key == 7
    assert root.left.left.left.key == 3
    assert root.left.left.right.key == 5

    # Test with a node that is not the root
    tree_1 = SplayTree()
    nodes = [5, 1, 2, 3, 4]
    for n in nodes:
        tree_1.insert_no_splay(n)
    node_1 = tree_1.root.left.right.right.right
    tree_1._zag_zag_right(node_1)

    root_1 = tree_1.root
    assert root_1.key == 5
    assert root_1.left.key == 1
    assert root_1.left.right.key == 4
    assert root_1.left.right.left.key == 3
    assert root_1.left.right.left.left.key == 2


def test_zag_zig():
    tree = SplayTree()
    nodes = [8, 4, 9, 6, 3, 5, 7]
    for n in nodes:
        tree.insert_no_splay(n)

    node = tree.root.left.right
    tree.root = tree._zag_zig(node)
    root = tree.root

    assert root.parent is None
    assert root.key == 6
    assert root.left.key == 4
    assert root.right.key == 8
    assert root.left.left.key == 3
    assert root.left.right.key == 5
    assert root.right.left.key == 7
    assert root.right.right.key == 9


def test_zig_zag():
    tree = SplayTree()
    nodes = [5, 12, 4, 7, 14, 6, 8]
    for n in nodes:
        tree.insert_no_splay(n)

    node = tree.root.right.left
    tree.root = tree._zig_zag(node)
    root = tree.root

    assert root.parent is None
    assert root.key == 7
    assert root.left.key == 5
    assert root.right.key == 12
    assert root.left.left.key == 4
    assert root.left.right.key == 6
    assert root.right.right.key == 14
    assert root.right.left.key == 8


def test_splay():
    # Splaying 4 in this tree should be a zig-zig
    # followed by a zigzag.
    tree_1 = SplayTree()
    nodes = [5, 1, 2, 3, 4]
    for n in nodes:
        tree_1.insert_no_splay(n)
    node = tree_1.root.left.right.right.right
    tree_1.root = tree_1._splay(node)
    root = tree_1.root

    assert root.key == 4
    assert root.left.key == 1
    assert root.right.key == 5
    assert root.left.right.key == 3
    assert root.left.right.left.key == 2


@pytest.fixture
def tree_not_splayed():
    """ Returns a binary search tree on which no splay operations
        have been performed
    """
    keys = [15, 10, 20, 8, 12, 25]
    tree = SplayTree()

    for k in keys:
        tree.insert_no_splay(k)

    return tree


# Basic operations #

def test_insert(tree_not_splayed: SplayTree):
    # Test insert method without splaying

    tree = tree_not_splayed
    root = tree.root

    assert tree.n_nodes == 6

    assert root.key == 15
    assert root.parent is None

    assert root.left.key == 10
    assert root.right.key == 20
    assert root.left.parent.key == 15
    assert root.right.parent.key == 15

    assert root.left.left.key == 8
    assert root.left.right.key == 12
    assert root.left.left.parent.key == 10
    assert root.left.right.parent.key == 10

    assert root.right.right.key == 25
    assert root.right.right.parent.key == 20


def test_insert_splay_tree():
    # Test with empty tree
    tree_1 = SplayTree()
    tree_1.insert(3)
    assert tree_1.n_nodes == 1
    assert tree_1.root.key == 3

    tree_1.insert(2)
    assert tree_1.root.key == 2
    assert tree_1.root.right.key == 3

    tree_1.insert(4)
    assert tree_1.root.key == 4
    assert tree_1.root.left.key == 3
    assert tree_1.root.left.left.key == 2

    tree_1.insert(5)
    assert tree_1.root.key == 5
    assert tree_1.root.left.key == 4
    assert tree_1.root.left.right is None
    assert tree_1.root.left.left.key == 3
    assert tree_1.root.left.left.left.key == 2

    # Test splay with a not empty tree
    tree_2 = SplayTree()
    nodes = [5, 1, 2, 3]
    for n in nodes:
        tree_2.insert_no_splay(n)

    tree_2.insert(4)
    root = tree_2.root

    assert root.key == 4
    assert root.left.key == 1
    assert root.right.key == 5
    assert root.left.right.key == 3
    assert root.left.right.left.key == 2


def test_remove():
    keys = [6, 8, 9, 12]
    tree = SplayTree()
    tree.insert_from_list(keys)

    with pytest.raises(KeyNotInTreeError):
        tree.remove(20)

    tree.remove(12)
    assert tree.n_nodes == 3
    tree.remove(6)
    assert tree.n_nodes == 2
    tree.remove(8)
    assert tree.n_nodes == 1
    assert tree.root.key == 9
    assert tree.root.left is None
    assert tree.root.right is None
    assert tree.root.parent is None

    # Test with another tree

    keys = [15, 10, 20, 8, 12, 25]
    tree_2 = SplayTree()
    tree_2.insert_from_list(keys)

    tree_2.remove(20)
    assert tree_2.n_nodes == 5
    assert (list(tree_2.inorder_traversal())
            == [8, 10, 12, 15, 25])

    tree_2.remove(12)
    assert tree_2.n_nodes == 4
    assert (list(tree_2.inorder_traversal())
            == [8, 10, 15, 25])


# Find Methods #

def test_find(tree_not_splayed: SplayTree):
    # Test find without splaying
    keys_list = [15, 10, 20, 8, 12, 25]
    tree = tree_not_splayed

    for k in keys_list:
        assert tree._find(tree.root, k).key == k

    # Test that when the key isn't present it returns the closest one
    assert tree._find(tree.root, 14).key == 12
    assert tree._find(tree.root, 23).key == 25
    assert tree._find(tree.root, 9).key == 8


def test_find_splay_tree():
    keys = [6, 8, 9, 12]
    tree = SplayTree()
    tree.insert_from_list(keys)

    for k in keys:
        assert tree.find(k)
        assert tree.root.key == k

    tree_2 = SplayTree()
    tree_2.insert_from_list([6, 5, 4])
    assert not tree_2.find(3)
    assert tree_2.root.key == 4


def test_left_descendant(tree_not_splayed: SplayTree):
    tree = tree_not_splayed
    node = tree._find(tree.root, 10)
    assert tree._left_descendant(node).key == 8
    node = tree.root
    assert tree._left_descendant(node).key == 8
    node = tree._find(tree.root, 25)
    assert tree._left_descendant(node).key == 25


def test_right_ancestor(tree_not_splayed: SplayTree):
    tree = tree_not_splayed
    node = tree._find(tree.root, 8)
    assert tree._right_ancestor(node).key == 10
    node = tree._find(tree.root, 12)
    assert tree._right_ancestor(node).key == 15


def test_next(tree_not_splayed: SplayTree):
    # Test with the not splayed tree
    tree = tree_not_splayed
    node = tree._find(tree.root, 8)
    assert tree._next(node).key == 10
    node = tree._find(tree.root, 10)
    assert tree._next(node).key == 12
    node = tree._find(tree.root, 12)
    assert tree._next(node).key == 15
    node = tree._find(tree.root, 15)
    assert tree._next(node).key == 20
    node = tree._find(tree.root, 20)
    assert tree._next(node).key == 25

    # Test with the splayed tree
    keys = [15, 10, 20, 8, 12, 25]
    tree = SplayTree()
    tree.insert_from_list(keys)

    assert tree.next_key(8) == 10
    assert tree.next_key(10) == 12
    assert tree.next_key(12) == 15
    assert tree.next_key(15) == 20
    # Test with the largest key
    assert tree.next_key(25) == 25


# Split and Merge #


def test_split():

    keys = [5, 4, 12, 7, 14, 6, 8]
    tree = SplayTree()
    for k in keys:
        tree.insert_no_splay(k)
    left_tree, right_tree = tree.split(7)

    assert left_tree.n_nodes == 4
    assert right_tree.n_nodes == 3
    assert left_tree.root.key == 7
    assert left_tree.root.right is None
    assert left_tree.root.left.key == 5
    assert left_tree.root.left.left.key == 4
    assert left_tree.root.left.right.key == 6
    assert right_tree.root.key == 12
    assert right_tree.root.left.key == 8
    assert right_tree.root.right.key == 14


def test_merge():
    keys_left_tree = [5, 4, 12, 7, 14, 6, 8]
    keys_right_tree = [18, 20, 19, 24]
    left_tree = SplayTree()
    right_tree = SplayTree()
    for k in keys_left_tree:
        left_tree.insert_no_splay(k)
    for k in keys_right_tree:
        right_tree.insert_no_splay(k)

    left_tree.merge(right_tree)
    assert left_tree.n_nodes == 11
    assert left_tree.root.key == 14
    assert left_tree.root.right.key == right_tree.root.key


# Basic statistics #

def test_min(tree_not_splayed: SplayTree):
    assert tree_not_splayed.min_key() == 8

    keys = [15, 10, 20, 8, 12, 25]
    tree = SplayTree()
    tree.insert_from_list(keys)

    assert tree.min_key() == 8


def test_max(tree_not_splayed: SplayTree):
    assert tree_not_splayed.max_key() == 25

    keys = [15, 10, 20, 8, 12, 25]
    tree = SplayTree()
    tree.insert_from_list(keys)
    assert tree.max_key() == 25


# Iterators #


def test_level_order_iterator(tree_not_splayed: SplayTree):
    keys_level_order = [15, 10, 20, 8, 12, 25]
    keys = list(tree_not_splayed.level_order_traversal())
    assert keys_level_order == keys


def test_inorder_iterator():
    tree = SplayTree()
    tree.insert_from_list([15, 10, 20, 8, 12, 25])

    keys_inorder = [8, 10, 12, 15, 20, 25]
    assert keys_inorder == list(tree.inorder_traversal())


def test_preorder_iterator(tree_not_splayed: SplayTree):
    keys_pre_order = [15, 8, 10, 12, 20, 25]
    keys = list(tree_not_splayed.preorder_traversal())
    assert keys_pre_order == keys


def test_postorder_iterator(tree_not_splayed: SplayTree):
    keys_post_order = [8, 10, 12, 20, 25, 15]
    keys = list(tree_not_splayed.postorder_traversal())
    assert keys_post_order == keys
