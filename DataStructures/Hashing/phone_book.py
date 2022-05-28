# python3

class InvalidNumberError(ValueError):
    pass


class InvalidQueryError(ValueError):
    pass


class PhoneBook:
    """Phone book manager implementation using direct addressing"""

    def __init__(self):
        self.contacts = [""] * 10000000
        self.n_contacts = 0
        self.find_results = []

    def process_query(self, query: str) -> None:
        """ Process a query.

            Example:
                add 911 police
                Will add the phone number 911 with name police to the phone book.
        """
        query_split = query.split()
        query_type = query_split[0]
        phone_number = int(query_split[1])

        if query_type == "add":
            name = query_split[2]
            self.add(phone_number, name)

        elif query_type == "find":
            if self.find(phone_number):
                self.find_results.append(self.contacts[phone_number])
            else:
                self.find_results.append("not found")

        elif query_type == "del":
            self.delete(phone_number)

        else:
            raise InvalidQueryError

    def add(self, phone_number: int, name: str) -> None:
        """ Add a contact to the phone book. """
        self._validate_number(phone_number)
        self.contacts[phone_number] = name
        self.n_contacts += 1

    def delete(self, phone_number: int) -> None:
        """ Delete a contact from the phone book. """
        self._validate_number(phone_number)
        self.contacts[phone_number] = ""
        self.n_contacts -= 1

    def find(self, phone_number: int) -> bool:
        """ Find a contact in the phone book. """
        self._validate_number(phone_number)
        if self.contacts[phone_number]:
            return True
        return False

    def print_find_results(self):
        for result in self.find_results:
            print(result)

    @staticmethod
    def _validate_number(phone_number: int):
        """Check if the phone number is a valid number. """
        if phone_number < 0 or phone_number > 10000000:
            raise InvalidNumberError

    def __repr__(self):
        return f"{self.__class__.__name__}(n_contacts={self.n_contacts})"


def test_phone_book(queries: list[str]) -> None:
    """ Test the phone book class using multiple queries. """
    phone_book = PhoneBook()
    for q in queries:
        phone_book.process_query(q)

    phone_book.print_find_results()


def main() -> None:

    queries = [
        "add 911 police",
        "add 76213 Mom",
        "add 17239 Bob",
        "find 76213",
        "find 910",
        "find 911",
        "del 910",
        "del 911",
        "find 911",
        "find 76213",
        "add 76213 daddy",
        "find 76213",
    ]

    print("\nTest 1")
    test_phone_book(queries)

    queries = [
        "find 3839442",
        "add 123456 me",
        "add 0 granny",
        "find 0",
        "find 123456",
        "del 0",
        "del 0",
        "find 0",
    ]

    print("\nTest 2")
    test_phone_book(queries)


if __name__ == "__main__":
    main()
