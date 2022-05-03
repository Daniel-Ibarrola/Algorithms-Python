from typing import Any, Callable, Generator
from collections import deque


class EmptyTreeError(ValueError):
    pass


class Node:
    """ Class to work with nodes for a binary tree."""
    def __init__(self, data) -> None:
        self.data  =  data
        self.left  =  None
        self.right =  None


class BinarySearchTree:
    """ Binary search tree class. """

    def __init__(self) -> None:
        self.root = None

    def is_empty(self) -> bool:
        """ Check whether the tree is empty"""
        if self.root is None:
            return True
        return False

    def _insert_node(self, root: Node, data: Any) -> Node:
        """ Private method to insert a new node in the tree using recursion. 
        """
        if root is None:
            return Node(data)
        elif data <= root.data:
            root.left = self._insert_node(root.left, data)
        else:
            root.right = self._insert_node(root.right, data)
        
        return root

    def insert(self, data: Any) -> None:
        """ Inserts a new node in the tree"""
        # This method is a wrapper for _insert_node method
        self.root = self._insert_node(self.root, data)

    def _find_node(self, root: Node, data: Any) -> bool:
        """ Private method to find a node with given data in the tree using recursion. 
        """
        if root is None:
            return False
        elif root.data == data:
            return True
        elif data < root.data:
            return self._find_node(root.left, data)
        else:
            return self._find_node(root.right, data)

    def find(self, data: Any) -> bool:
        """ Find if there is a node with given data in the tree."""
        return self._find_node(self.root, data)

    def min(self) -> Any:
        """ Returns the min element"""

        if self.is_empty():
            raise EmptyTreeError
        
        current = self.root
        while current.left is not None:
            current = current.left

        return current.data

    def max(self) -> Any:
        """ Returns the max element"""
        if self.is_empty():
            raise EmptyTreeError

        current = self.root
        while current.right is not None:
            current = current.right
        
        return current.data

    def _height(self, root: Node) -> int:
        """ Private method to find the height of the tree."""
        if root is None:
            return -1
        return max(self._height(root.left), self._height(root.right)) + 1
        
    def height(self) -> int:
        """ Returns the height of the tree."""
        return self._height(self.root)
    
    def _delete_node(self, root: Node, data: Any) -> Node:
        pass

    def delete(self, data: Any) -> None:
        pass

    def level_order_iterator(self) -> Generator[Any, None, None]:
        """ Iterates the nodes in level order. """
        if self.is_empty():
            raise EmptyTreeError

        nodes_queue = deque()
        current = self.root
        nodes_queue.append(current)

        while len(nodes_queue) != 0:
            current = nodes_queue.popleft()
            if current.left is not None:
                nodes_queue.append(current.left)
            if current.right is not None:
                nodes_queue.append(current.right)

            yield current.data

    def _preorder_generator(self, root: Node) -> Generator[Any, None, None]:
        if root is not None:
            yield root.data
            yield from self._preorder_generator(root.left)
            yield from self._preorder_generator(root.right)

    def preorder_iterator(self) -> Generator[Any, None, None]:
        """ Iterates the nodes in preorder traversal. """
        return self._preorder_generator(self.root)

    def _inorder_generator(self, root: Node) -> Generator[Any, None, None]:
        if root is not None:
            yield from self._inorder_generator(root.left)
            yield root.data
            yield from self._inorder_generator(root.right)

    def inorder_iterator(self) -> Generator[Any, None, None]:
        """ Iterates the nodes in preorder traversal. """
        return self._inorder_generator(self.root)

    def _postorder_generator(self, root: Node) -> Generator[Any, None, None]:
        if root is not None:
            yield from self._postorder_generator(root.left)
            yield from self._postorder_generator(root.right)
            yield root.data

    def postorder_iterator(self) -> Generator[Any, None, None]:
        """ Iterates the nodes in preorder traversal. """
        return self._postorder_generator(self.root)

    def __repr__(self) -> str:
        return "BinarySearchTree"


def create_tree() -> None:

    tree = BinarySearchTree()
    tree.insert("F")
    tree.insert("J")
    tree.insert("D")
    tree.insert("B")
    tree.insert("E")
    tree.insert("A")
    tree.insert("C")
    tree.insert("G")
    tree.insert("K")
    tree.insert("I")
    tree.insert("H")

    assert tree.find("H")
    assert tree.find("C")

    print(f"Min element is {tree.min()}")
    print(f"Max element is {tree.max()}")
    print(f"Tree height is {tree.height()}")

    print("Level Order Traversal:")
    for item in tree.level_order_iterator():
        print(item, end=" ")
    print('\n')

    print("Preorder Traversal:")
    for item in tree.preorder_iterator():
        print(item, end=" ")
    print('\n')

    print("Inorder Traversal:")
    for item in tree.inorder_iterator():
        print(item, end=" ")
    print('\n')

    print("Postorder Traversal:")
    for item in tree.postorder_iterator():
        print(item, end=" ")
    print('\n')


if __name__ == "__main__":
    create_tree()
