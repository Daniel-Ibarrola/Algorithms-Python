# python3
import os
import pprint
import sys
import threading
from typing import Any

sys.setrecursionlimit(10**7)  # max depth of recursion
threading.stack_size(2**27)  # new thread will get stack of such size


class Node:
    """ Node data structure class."""

    def __init__(self, key: Any = None) -> None:
        self.key = key
        self.children = []

    def add_child(self, child: int) -> None:
        """ Add a child to the node. """
        self.children.append(child)

    def set_key(self, key: Any) -> None:
        """ Set the key of the node. """
        self.key = key

    def has_children(self):
        """ Check if the node has any children. """
        if len(self.children) > 0:
            return True
        return False

    def __repr__(self) -> str:
        return f"Node(key={self.key}, children={self.children})"


class Tree:
    """ Tree data structure class. """

    def __init__(self, nodes: list[Node] = None, root: int = None) -> None:
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes
        self.n_nodes = len(nodes)
        self.root = root

    def is_empty(self) -> bool:
        """ Check whether the tree is empty.
        """
        if len(self.nodes) == 0:
            return True
        return False

    @classmethod
    def from_file(cls, tree_file: str) -> "Tree":
        """ Reads a tree from a file.
        """
        with open(tree_file, "r") as fp:
            # Number of nodes is in the first line
            n_nodes = int(fp.readline())
            # Second line contains the nodes
            tree_str = fp.readline()

        return Tree.from_string(tree_str, n_nodes)

    @classmethod
    def from_string(cls, tree_str: str, n_nodes: int) -> "Tree":
        """ Reads a tree from a string
        """
        node_data = map(int, tree_str.split())

        nodes = [Node() for _ in range(n_nodes)]
        for ii, child_index in enumerate(node_data):
            if child_index == -1:
                root = ii
            else:
                nodes[child_index].add_child(ii)
            nodes[ii].set_key(ii)
        return cls(nodes, root)

    def height(self) -> int:
        """ Returns the height of the tree.
        """
        if self.is_empty():
            return 0
        return self._height(self.root)

    def _height(self, index: int) -> int:
        """ Computes the height of the tree recursively.
        """
        if not self.nodes[index].has_children():
            return 1
        else:
            height = 1
            for child in self.nodes[index].children:
                height = max(height, self._height(child))
            return height + 1

    def get_max_number_children(self) -> int:
        """ Returns the maximum number of children in the tree"""
        max_children = 0
        for node in self.nodes:
            max_children = max(max_children, len(node.children))

        return max_children

    def __repr__(self) -> str:
        return f"Tree(n_nodes={self.n_nodes})"


test_dir = "./tests"


class Test:

    def __init__(self, tree: Tree, result: int, test_num: int):
        self.test_num = test_num
        self.tree = tree
        self.result = result
        self.actual = tree.height()

    @classmethod
    def from_file(cls, filename: str) -> "Test":
        test_num = int(filename)
        tree = Tree.from_file(os.path.join(test_dir, filename))
        with open(os.path.join(test_dir, filename + ".a")) as fp:
            result = int(fp.readline())
        return cls(tree, result, test_num)

    def assert_test(self) -> bool:
        if self.actual == self.result:
            return True
        return False

    def test_result(self) -> None:
        if self.assert_test():
            print(f"Test {self.test_num} Passed!")
        else:
            print(f"Test {self.test_num} failed")
            print(f"Expected {self.result} but got {self.actual} with this tree")
            if self.tree.n_nodes < 30:
                pprint.pprint(self.tree.nodes)
        print("==============================================\n")


def get_test_file_names() -> list[str]:
    """ Get all test file names and store them in a list. """
    files = []
    for root, dirs, filenames in os.walk(test_dir):
        for file in filenames:
            if file.endswith(".a"):
                continue
            else:
                files.append(file)
    return files


def run_tests() -> None:
    test_files = get_test_file_names()
    test_files = sorted(test_files)
    for file in test_files:
        tree_test = Test.from_file(file)
        tree_test.test_result()


def main() -> None:
    run_tests()


if __name__ == "__main__":
    threading.Thread(target=main).start()
