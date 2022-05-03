#!/usr/bin/python3

import sys
import threading
from collections import namedtuple

from binarytree import BinaryTree

sys.setrecursionlimit(10 ** 7)  # max depth of recursion
threading.stack_size(2 ** 25)  # new thread will get stack of such size

Test = namedtuple("Test", ["tree", "result"])


def get_tree_user_input() -> BinaryTree:
    """ Construct a tree from user input. """
    n_nodes = int(sys.stdin.readline().strip())
    nodes = []
    for _ in range(n_nodes):
        nodes.append(list(map(int, sys.stdin.readline().strip().split())))

    return BinaryTree(nodes)


def print_answer(tree: BinaryTree) -> None:
    if tree.is_search_tree():
        print("CORRECT")
    else:
        print("INCORRECT")


def load_tests(test_dir: str) -> list[tuple[BinaryTree, bool]]:
    """ Load trees test file and return a list of tuples
      containing the binary tree and the result.
  """
    trees = []
    with open(test_dir, "r") as fp:
        for line in fp.readlines():
            if line.startswith("#START"):
                tree_str = ""
            elif line.startswith("#RESULT"):
                result_str = line.split()[-1]
                if result_str == "CORRECT":
                    result = True
                elif result_str == "INCORRECT":
                    result = False
                else:
                    assert False, "Unexpected error while parsing file"
            elif line.startswith("#END"):
                trees.append(Test(BinaryTree.from_string(tree_str), result))
            else:
                tree_str += line

    if "duplicates" in test_dir:
        assert len(trees) == 5
    else:
        assert len(trees) == 8

    return trees


def test_is_bst(tree_tests: list[Test],
                algorithm: str) -> None:
    """ Test is binary search tree using the loaded tests. """

    print(f"Testing is binary search tree with {algorithm} algorithm")

    fails = 0
    for ii, test in enumerate(tree_tests):
        if not test.tree.is_search_tree(method=algorithm) == test.result:
            print(f"Failed test case for tree {ii}")
            fails += 1

    if fails > 0:
        print(f"Finished Testing. {fails} tests failed")
    else:
        print("All tests passed!!!\n")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "t":
        trees = load_tests("./trees/isbst_tests.txt")
        test_is_bst(trees, "recursive")
        test_is_bst(trees, "iterative")

        print("\nTesting is binary search tree with duplicates\n")
        trees = load_tests("./trees/isbst_duplicates.txt")
        test_is_bst(trees, "recursive")
        test_is_bst(trees, "iterative")
    else:
        tree = get_tree_user_input()
        print_answer(tree)


if __name__ == "__main__":
    threading.Thread(target=main).start()
