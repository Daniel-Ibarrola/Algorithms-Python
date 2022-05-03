from typing import Any, Generator


class EmptyTreeError(ValueError):
    pass


class InvalidMethodError(ValueError):
    pass


class Node:

    def __init__(self, data: Any, left: int = None, right: int = None) -> None:
        self.data = data
        self.left = left
        self.right = right


class BinaryTree:
    """ Binary tree class. It is not necessarily a binary search tree"""

    def __init__(self, nodes: list = None) -> None:
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes

    def is_empty(self) -> bool:
        """ Check whether the tree is empty. """
        if len(self.nodes) > 0:
            return False
        return True

    @classmethod
    def from_file(cls, filename: str) -> "BinaryTree":
        """ Reads a tree from a text file."""
        nodes = []

        with open(filename, "r") as fp:
            n_nodes = int(fp.readline())
            for line in fp.readlines():
                data = line.rstrip().split()
                key = int(data[0])
                left = int(data[1])
                right = int(data[2])

                if left == -1:
                    left = None
                if right == -1:
                    right = None

                nodes.append(Node(key, left, right))

        assert len(nodes) == n_nodes

        return cls(nodes)

    @classmethod
    def from_string(cls, tree_str: str) -> "BinaryTree":
        """ Loads a tree from a string. """
        tree_data = tree_str.split()
        n_nodes = int(tree_data[0])
        nodes = []

        # To keep track if the number is node data, right or left index
        current_type = 0
        for num in tree_data[1:]:

            if current_type == 0:
                data = int(num)
            elif current_type == 1:
                left = int(num)
                if left == -1:
                    left = None
            elif current_type == 2:
                right = int(num)
                if right == -1:
                    right = None

                nodes.append(Node(data, left, right))
                current_type = -1

            current_type += 1

        assert len(nodes) == n_nodes
        return cls(nodes)

    def height(self) -> int:
        """ Returns the height of the tree.
        """
        if self.is_empty():
            return -1
        return self._height(0)

    def _height(self, index: int) -> int:
        """ Finds the height of the tree recursively.
        """
        if index is None:
            return -1

        root = self.nodes[index]
        return 1 + max(self._height(root.left),
                       self._height(root.right))

    def _is_search_tree_recursive(self, index: int,
                                  min_val: Any, max_val: Any) -> bool:
        """ Checks whether the tree is a binary search tree using a
            recursive algorithm.
        """
        if index is None:
            return True
        root = self.nodes[index]
        if (min_val <= root.data < max_val
                and self._is_search_tree_recursive(root.left, min_val, root.data)
                and self._is_search_tree_recursive(root.right, root.data, max_val)):
            return True
        else:
            return False

    def _is_search_tree_iterative(self) -> bool:
        """ Checks whether the tree is a binary search tree using an
        iterative algorithm. 
    """
        # Get the first node
        inorder_iterator = self.inorder_traversal()
        prev = next(inorder_iterator)

        for current in inorder_iterator:
            if not current >= prev:
                return False
            prev = current

        return True

    def is_search_tree(self, method="recursive") -> bool:
        """ Checks whether the tree is a binary search tree. """
        if len(self.nodes) > 0:
            if method == "recursive":
                return self._is_search_tree_recursive(0, -1 * float("inf"), float("inf"))
            elif method == "iterative":
                return self._is_search_tree_iterative()
            else:
                raise InvalidMethodError
        else:
            return True

    def _inorder_generator(self, root: Node) -> Generator[Any, None, None]:
        """ Generator to traverse the nodes in in-order."""
        if root.left is not None:
            yield from self._inorder_generator(self.nodes[root.left])

        yield root.data

        if root.right is not None:
            yield from self._inorder_generator(self.nodes[root.right])

    def inorder_traversal(self) -> Generator[Any, None, None]:
        """ Iterates the nodes in in-order."""
        if self.is_empty():
            raise EmptyTreeError

        root = self.nodes[0]
        return self._inorder_generator(root)

    def _preorder_generator(self, root: Node) -> Generator[Any, None, None]:
        """ Generator to traverse the nodes in preorder."""
        yield root.data

        if root.left is not None:
            yield from self._preorder_generator(self.nodes[root.left])
        if root.right is not None:
            yield from self._preorder_generator(self.nodes[root.right])

    def preorder_traversal(self) -> Generator[Any, None, None]:
        """ Iterates the nodes in preorder."""
        if self.is_empty():
            raise EmptyTreeError

        root = self.nodes[0]
        return self._preorder_generator(root)

    def _postorder_generator(self, root: Node) -> Generator[Any, None, None]:
        """ Generator to traverse the nodes in postorder."""
        if root.left is not None:
            yield from self._postorder_generator(self.nodes[root.left])
        if root.right is not None:
            yield from self._postorder_generator(self.nodes[root.right])

        yield root.data

    def postorder_traversal(self) -> Generator[Any, None, None]:
        """ Iterates the nodes in postorder."""
        if self.is_empty():
            raise EmptyTreeError

        root = self.nodes[0]
        return self._postorder_generator(root)

    def __repr__(self) -> str:
        return f"({self.__class__.__name__}; n_nodes={len(self.nodes)})"
