from binarytree import BinaryTree
import os

class WrongTraversalError(ValueError):
  pass


def traverse_tree(tree: BinaryTree, traversal: str) -> None:
  """ Travese a tree in the specified order. """
  print(f"{traversal.capitalize()} traversal:")
  
  if traversal == "inorder":
    for node in tree.inorder_traversal():
      print(node, end=" ")
  elif traversal == "postorder":
    for node in tree.preorder_traversal():
      print(node, end=" ")
  elif traversal == "preorder":
    for node in tree.postorder_traversal():
      print(node, end=" ")
  else:
    raise WrongTraversalError
  
  print("\n")

def create_and_traverse_tree(tree_file: str) -> None:
  """ Creates a tree from a file and traverses it in different orders. """
  if not os.path.isfile(tree_file):
    tree_file = os.path.join("./DataStructures/BST/", tree_file)
  tree = BinaryTree.from_file(tree_file)
  print(tree)
  traverse_tree(tree, "inorder")
  traverse_tree(tree, "preorder")
  traverse_tree(tree, "postorder")

def main() -> None:

  create_and_traverse_tree("./tree1.txt")
  create_and_traverse_tree("./tree2.txt")


if __name__=="__main__":
  main()