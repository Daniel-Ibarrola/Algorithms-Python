import copy
from typing import Any, Generator
from collections import deque


class EmptyTreeError(ValueError):
    pass


class NoLeftChildError(ValueError):
    pass


class NoRightChildError(ValueError):
    pass


class ParentNotRootError(ValueError):
    pass


class MergeError(ValueError):
    pass


class KeyNotInTreeError(ValueError):
    pass


class Node:
    """ Class to store nodes from a binary search tree."""

    def __init__(self, key: Any, parent: "Node" = None) -> None:
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return f"Node(key={self.key})"


class SplayTree:
    """Binary Search tree that puts the most frequent queries near the root"""

    def __init__(self) -> None:
        self.root = None
        self.n_nodes = 0

    # Public Methods #

    def is_empty(self) -> bool:
        if self.root is None:
            return True
        return False

    def insert(self, key: Any) -> None:
        """ Inserts a node in the tree. """
        self._insert_splay_tree(key)

    def insert_from_list(self, keys: list[Any]):
        """ Inserts new nodes to the tree from a list. """
        for k in keys:
            self._insert_splay_tree(k)

    def insert_no_splay(self, key: Any) -> None:
        """ Inserts a node in the tree without splaying.
            This method shouldn't be used. Instead, use the insert method.
        """
        self.root = self._insert(self.root, key)
        self.n_nodes += 1

    def find(self, key: Any) -> bool:
        """ Check whether the given key is in the tree. """
        if self._find_splay_tree(key).key == key:
            return True
        return False

    def min_key(self) -> Any:
        """ Returns the minimum key in the tree. """
        return self._min().key

    def max_key(self) -> Any:
        """ Returns the maximum key in the tree. """
        return self._max().key

    def next_key(self, key: Any) -> Any:
        """ Returns the next key larger than the given key."""
        current_node = self._find_splay_tree(key)
        return self._next(current_node).key

    def range_search(self, lower: Any, upper: Any) -> list[Any]:
        """ Returns a list with all the keys between lower and upper
            limits.
        """
        data = []
        current_node = self._find_splay_tree(lower)
        while current_node.key < upper:
            data.append(current_node.key)
            current_node = self._next(current_node)

        return data

    def remove(self, key: Any) -> None:
        """ Deletes a node from the tree. """
        node = self._find(self.root, key)
        if node.key != key:
            raise KeyNotInTreeError(f"Key {key} is not present in this tree")
        # Splay the successor of the node
        successor = self._splay(self._next(node))
        node = self._splay(node)
        if successor.key == node.key:
            # Case when the node to be deleted is the largest and has no successor
            left = node.left
            left.parent = None
            self.root = left
        else:
            # Splay the node, so it becomes the root and is successor
            # is to the right
            left = node.left
            if left is not None:
                left.parent = successor
            successor.left = left
            successor.parent = None
            self.root = successor

        del node
        self.n_nodes -= 1

        # Split and Merge #

    def split(self, key: Any, make_copy: bool = True) -> tuple["SplayTree", "SplayTree"]:
        """ Split the tree on a key. Returns a tuple with the trees.

            The node with the split key becomes the root in the left tree. If the key is
            not found the tree is split by the closest key.
        """
        if make_copy:
            tree_copy = copy.deepcopy(self)
            root_left = tree_copy._find_splay_tree(key)
        else:
            root_left = self._find_splay_tree(key)

        root_right = root_left.right
        root_left.right = None
        if root_right is not None:
            root_right.parent = None

        left_tree = SplayTree()
        left_tree.root = root_left
        right_tree = SplayTree()
        right_tree.root = root_right

        # Recompute the number of nodes
        n_nodes_left = 0
        for _ in left_tree.level_order_traversal():
            n_nodes_left += 1
        right_tree.n_nodes = self.n_nodes - n_nodes_left
        left_tree.n_nodes = n_nodes_left

        return left_tree, right_tree

    def merge(self, tree: "SplayTree", make_copy: bool = True) -> None:
        """ Merge two trees into a single one. The elements of the other tree
            should be greater than those of the current tree.
        """
        # Find max of this tree and splay it
        self.root = self._splay(self._max())
        # Now the root has no right child
        if tree.min_key() < self.root.key:
            raise MergeError("Right tree should be greater than left tree")
        assert self.root.right is None

        if make_copy:
            right_root = copy.deepcopy(tree).root
        else:
            right_root = tree.root

        self.root.right = right_root
        right_root.parent = self.root
        self.n_nodes += tree.n_nodes

    def level_order_traversal(self):
        """ Iterate the nodes in level order. """
        return self._level_order_iterator()

    def inorder_traversal(self):
        """ Iterate the nodes in inorder. """
        return self._inorder_iterator(self.root)

    def preorder_traversal(self):
        """ Iterate the nodes in preorder. """
        return self._preorder_iterator(self.root)

    def postorder_traversal(self):
        """ Iterate the nodes in postorder. """
        return self._postorder_iterator(self.root)

    # Private Methods #

    # Methods to implement the splay operation #

    @staticmethod
    def _right_rotation(node: Node) -> Node:
        """ Performs a right rotation of the given node.
            The node must have a left child.
        """
        left_temp = node.left
        if left_temp is None:
            raise NoLeftChildError
        # Fix parents
        left_temp.parent = node.parent
        node.parent = left_temp
        if left_temp.right is not None:
            left_temp.right.parent = node
        # Rewire left and right
        node.left = left_temp.right
        left_temp.right = node

        if left_temp.parent is not None:
            # Check if node is a left subtree of another node
            if (left_temp.parent.left is not None and
                    left_temp.parent.left.key == left_temp.right.key):
                left_temp.parent.left = left_temp
            else:
                # The node is the right subtree of another node
                left_temp.parent.right = left_temp

        return left_temp

    @staticmethod
    def _left_rotation(node: Node) -> Node:
        """ Performs a right rotation of the given node.
            The node must have a right child.
        """
        right_temp = node.right
        if right_temp is None:
            raise NoRightChildError
        # Fix parents
        right_temp.parent = node.parent
        node.parent = right_temp
        if right_temp.left is not None:
            right_temp.left.parent = node
        # Rewire left and right
        node.right = right_temp.left
        right_temp.left = node

        if right_temp.parent is not None:
            # Check if node is a left subtree of another node
            if (right_temp.parent.left is not None and
                    right_temp.parent.left.key == right_temp.left.key):
                right_temp.parent.left = right_temp
            else:
                # The node is the right subtree of another node
                right_temp.parent.right = right_temp

        return right_temp

    @staticmethod
    def _zig(node: Node) -> Node:
        """ Rotates the given node so it becomes the root. Node parent must
            be the root. 
        """
        if node.parent.parent is not None:
            raise ParentNotRootError

        # Node is to the left of its parent. Perform right rotation
        if (node.parent.left is not None and
                node.parent.left.key == node.key):
            node = SplayTree._right_rotation(node.parent)
        # Node is to the right of its parent. Perform left rotation
        else:
            node = SplayTree._left_rotation(node.parent)

        return node

    @staticmethod
    def _zig_zig_left(node: Node) -> Node:
        """ Splay operation when a node is to the left of
            its parent and grandparent.
        """
        # Perform two right rotations
        node = SplayTree._right_rotation(node.parent.parent)
        return SplayTree._right_rotation(node)

    @staticmethod
    def _zag_zag_right(node: Node) -> Node:
        """ Splay operation when a node is to the right of
            its parent and grandparent.
        """
        # Perform two left rotations
        node = SplayTree._left_rotation(node.parent.parent)
        return SplayTree._left_rotation(node)

    @staticmethod
    def _zag_zig(node: Node) -> Node:
        """ Splay operation when a node is to the right of its parent
            and its parent is to the left of its grandparent.
        """
        # Perform a left rotation followed by a right rotation
        node = SplayTree._left_rotation(node.parent)
        return SplayTree._right_rotation(node.parent)

    @staticmethod
    def _zig_zag(node: Node) -> Node:
        """ Splay operation when a node is to the left of its parent
            and its parent is to the right of its grandparent.
        """
        # Perform a right rotation followed by a left rotation
        node = SplayTree._right_rotation(node.parent)
        return SplayTree._left_rotation(node.parent)

    def _splay(self, node: Node) -> Node:
        """ Splay operation that makes the given node become the root
            of the tree.
        """
        # Base Case: node is the root node
        if node.parent is None:
            return node

        grandparent = node.parent.parent
        # Case when the node doesn't have a grandparent
        if grandparent is None:
            node = self._zig(node)

        # Cases when the parent is to the right of the grandparent
        elif (grandparent.right is not None
                and grandparent.right.key == node.parent.key):
            # All on the same side
            if (node.parent.right is not None and
                    node.parent.right.key == node.key):
                node = self._zag_zag_right(node)
            # On opposite side
            else:
                node = self._zig_zag(node)

        # Cases when the parent is to the left of the grandparent
        elif (grandparent.left is not None
                and grandparent.left.key == node.parent.key):
            # All on the same side
            if (node.parent.left is not None and
                    node.parent.left.key == node.key):
                node = self._zig_zig_left(node)
            # On opposite side
            else:
                node = self._zag_zig(node)
        else:
            # This should not happen
            assert False

        return self._splay(node)

    # Basic operations #

    def _insert(self, root: Node, key: Any, parent: Node = None) -> Node:
        """ Insert a new node in the tree recursively. """
        if root is None:
            return Node(key, parent)
        elif key < root.key:
            root.left = self._insert(root.left, key, root)
        else:
            root.right = self._insert(root.right, key, root)

        return root

    def _insert_splay_tree(self, key: Any) -> None:
        """ Inserts a node and then splays the tree."""
        self.root = self._insert(self.root, key)
        self.n_nodes += 1
        self._find_splay_tree(key)

    # Find Methods #

    def _find(self, root: Node, key: Any) -> Node:
        """ Finds and returns node with given key in the tree. 
            If it's not found, it returns the node with the 
            closest key.
        """
        if root.key == key:
            return root
        elif key < root.key:
            # Go to the left of the tree
            if root.left is not None:
                return self._find(root.left, key)
            else:
                return root
        else:
            # Go to the right of the tree
            if root.right is not None:
                return self._find(root.right, key)
            else:
                return root

    def _find_splay_tree(self, key: Any) -> Node:
        """ Searches for a node with given key and then splays the tree.
            If the node is found the tree is splayed with that node, else
            it is splayed with the closest node.
        """
        node = self._find(self.root, key)
        self.root = self._splay(node)
        return node

    def _left_descendant(self, node: Node) -> Node:
        """ Returns the left descendant of the given node.
        """
        if node.left is None:
            return node
        else:
            return self._left_descendant(node.left)

    def _right_ancestor(self, node: Node) -> Node:
        """ Returns the right ancestor of the given node.
        """
        # Base case node is the root node
        if node.parent is None:
            return node

        if node.parent.key > node.key:
            return node.parent
        else:
            return self._right_ancestor(node.parent)

    def _next(self, node: Node) -> Node:
        """ Returns the node with the next larger key.
        """
        # Go to the right and then to the left to find the next key
        if node.right is not None:
            return self._left_descendant(node.right)
        # If node doesn't have a right child find a larger right ancestor
        else:
            return self._right_ancestor(node)

    # Basic statistics #

    def _min(self) -> Node:
        """ Returns the node with the minimum key"""
        if self.is_empty():
            raise EmptyTreeError

        current = self.root
        while current.left is not None:
            current = current.left

        return current

    def _max(self) -> Node:
        """ Returns the node with the maximum key"""
        if self.is_empty():
            raise EmptyTreeError

        current = self.root
        while current.right is not None:
            current = current.right

        return current

    # Iterators #

    def _level_order_iterator(self) -> Generator[Any, None, None]:
        """ Generator function that yields the nodes in inorder.
        """
        nodes_queue = deque()
        nodes_queue.append(self.root)

        while len(nodes_queue) > 0:
            current = nodes_queue.pop()
            if current.left is not None:
                nodes_queue.appendleft(current.left)
            if current.right is not None:
                nodes_queue.appendleft(current.right)

            yield current.key

    def _inorder_iterator(self, root: Node) -> Generator[Any, None, None]:
        """ Generator function that yields the nodes in inorder.
        """
        if root is not None:
            yield from self._inorder_iterator(root.left)
            yield root.key
            yield from self._inorder_iterator(root.right)

    def _preorder_iterator(self, root: Node) -> Generator[Any, None, None]:
        """ Generator function that yields the nodes in preorder.
        """
        if root is not None:
            yield root.key
            yield from self._inorder_iterator(root.left)
            yield from self._inorder_iterator(root.right)

    def _postorder_iterator(self, root: Node) -> Generator[Any, None, None]:
        """ Generator function that yields the nodes in postorder.
        """
        if root is not None:
            yield from self._inorder_iterator(root.left)
            yield from self._inorder_iterator(root.right)
            yield root.key

    # Other #
    def __repr__(self) -> str:
        return f"SplayTree(n_nodes={self.n_nodes})"
