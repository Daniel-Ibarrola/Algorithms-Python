

class IndexOutOfRangeError(ValueError):
    pass


class DisjointSets:
    """ Disjoint sets data structure using trees. """

    def __init__(self, size: int, path_compression: bool = False) -> None:
        self.parent = [0] * size
        self.rank = [0] * size
        self._path_compression = path_compression

    def make_set(self, element: int) -> None:
        """ Make a set with the given element. """
        if element < 0 or element > len(self.parent):
            raise IndexOutOfRangeError(f"{element} is not a valid element")

        self.parent[element] = element
        self.rank[element] = 0

    def union(self, element_1: int, element_2: int) -> None:
        """ Joins two trees on the union by rank heuristic.
        """
        self._validate_index(element_1)
        self._validate_index(element_2)
        # Get the root of each element
        root_1 = self.find(element_1)
        root_2 = self.find(element_2)

        # If they are already in the same set we do nothing
        if root_1 == root_2:
            return

        # Join the root with the lower rank to the root with higher rank
        if self.rank[root_1] > self.rank[root_2]:
            self.parent[root_2] = root_1
        else:
            self.parent[root_1] = root_2
            # If the rank is the same it needs to be updated
            if self.rank[root_1] == self.rank[root_2]:
                self.rank[root_2] += 1

    def find(self, element: int) -> int:
        """ Find the set to which the elements belong to. Returns the root
            of the tree it belongs to.
        """
        if element < 0 or element > len(self.parent):
            raise IndexOutOfRangeError(f"{element} is not a valid element")
        if not self._path_compression:
            return self._find_std(element)
        else:
            return self._find_path_compression(element)

    def _find_std(self, element: int) -> int:
        """ Finds the set which the element belongs to. Doesn't modify
            links in the tree.
        """
        while element != self.parent[element]:
            element = self.parent[element]

        return element

    def _find_path_compression(self, element: int) -> int:
        """ Finds the set which the element belongs to, and reattaches
            all elements in the path to the root of the tree.
        """
        if element != self.parent[element]:
            self.parent[element] = self._find_path_compression(self.parent[element])
        return self.parent[element]

    def _validate_index(self, index: int) -> None:
        if index < 0 or index > len(self.parent):
            raise IndexOutOfRangeError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
