

class InvalidQueryError(ValueError):
    pass


class HashTable:
    """ A hash table with list chaining. """
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, size: int) -> None:
        self.size = size
        self.elements = [[] for _ in range(self.size)]

    def _hash_function(self, string: str) -> int:
        """ A polynomial hash function to compute the hash
            of strings.
        """
        result = 0
        for char in reversed(string):
            result = (result * self._multiplier + ord(char)) % self._prime
        return result % self.size

    def add(self, string: str) -> None:
        """ Add a string to the hash table. """
        if not self.find(string):
            self.elements[self._hash_function(string)].insert(0, string)

    def delete(self, string: str) -> None:
        """ Delete a string of the hash table. """
        index = None
        chain = self._hash_function(string)
        for ii, obj in enumerate(self.elements[chain]):
            if obj == string:
                index = ii
                break
        if index is not None:
            self.elements[chain].pop(index)

    def find(self, string: str) -> bool:
        """ Find a string in the hash table. """
        chain = self._hash_function(string)
        for obj in self.elements[chain]:
            if obj == string:
                return True
        return False

    def check(self, index: int) -> list[str]:
        """ Returns the content of a chain of the hash table. """
        return self.elements[index]

    def process_query(self, query: str) -> None:
        """ Process a query. Queries can be of type 'add', 'del',
            'find' and 'check'.
        """
        query_split = query.split()
        query_type = query_split[0]
        if query_type == "add":
            self.add(query_split[1])
        elif query_type == "del":
            self.delete(query_split[1])
        elif query_type == "find":
            self.print_search_result(query_split[1])
        elif query_type == "check":
            self.print_chain(self.check(int(query_split[1])))
        else:
            raise InvalidQueryError

    @staticmethod
    def print_chain(chain: list[str]) -> None:
        """ Prints a chain of the hash table. """
        for obj in chain:
            print(obj, end=" ")
        print("")

    def print_search_result(self, string: str) -> None:
        """ Prints the result of searching a key in the table. """
        if self.find(string):
            print("yes")
        else:
            print("no")


def proces_queries(size: int, queries: list[str], table_num: int) -> None:
    """ Process all given queries. """
    print(f"\nHash table {table_num}")
    table = HashTable(size)
    for q in queries:
        table.process_query(q)


def main() -> None:

    queries = [
        "add world",
        "add HellO",
        "check 4",
        "find World",
        "find world",
        "del world",
        "check 4",
        "del HellO",
        "add luck",
        "add GooD",
        "check 2",
        "del good",
    ]
    proces_queries(5, queries, 1)

    queries = [
        "add test",
        "add test",
        "find test",
        "del test",
        "find test",
        "find Test",
        "add Test",
        "find Test",
    ]
    proces_queries(4, queries, 2)

    queries = [
        "check 0",
        "find help",
        "add help",
        "add del",
        "add add",
        "find add",
        "find del",
        "del del",
        "find del",
        "check 0",
        "check 1",
        "check 2",
    ]
    proces_queries(3, queries, 3)


if __name__ == "__main__":
    main()
