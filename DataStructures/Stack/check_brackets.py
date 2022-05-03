import os
from collections import deque


class Bracket:
    """ Class to store a bracket and its position in a string."""

    def __init__(self, bracket_type, position):
        self.bracket_type = bracket_type
        self.position = position

    def match(self, closing_bracket) -> bool:
        """ Checks whether a closing bracket matches its corresponding
            opening bracket.
        """
        if self.bracket_type == '[' and closing_bracket == ']':
            return True
        if self.bracket_type == '{' and closing_bracket == '}':
            return True
        if self.bracket_type == '(' and closing_bracket == ')':
            return True
        return False


def load_files() -> tuple[list[str], list[str]]:
    """ Loads files for testing check brackets function. """
    files_dir = "./brackets_tests"

    test_files = []
    answers = []

    for dirpath, dirnames, filenames in os.walk(files_dir):

        for file in filenames:
            if file.endswith(".a"):
                answers.append(file)
            else:
                test_files.append(file)

    assert len(test_files) == len(answers)

    return test_files, answers


def check_brackets(text: str) -> int:
    """ Check if a string with brackets is balanced. If it's not it returns
        the position in the string where the unbalance occurs.

        Parameters
        ----------
        text : str
            A string with brackets.

        Returns
        -------
        int
            The position (1-based) where the unbalance occurs. -1 is returned if the
            string is balanced
    """

    brackets_stack = deque()

    for position, char in enumerate(text):

        if char == '(' or char == '[' or char == '{':
            brackets_stack.append(Bracket(char, position))

        elif char == ')' or char == ']' or char == '}':

            # If the stack is empty there is an unmatched closing bracket
            if len(brackets_stack) == 0:
                return position + 1

            match = brackets_stack.pop().match(char)
            if not match:
                return position + 1

    if len(brackets_stack) == 0:
        return -1
    else:
        return brackets_stack.pop().position + 1


def assert_test_case(result, text, expected):
    message = f"Test case failed for {text}. Expected {expected}, got {result}"
    assert result == expected, message


def test_brackets(tests: list, answers: list) -> None:
    """ Test check_brackets function with different test cases.
    """
    files_dir = "./brackets_tests"

    for ii in range(len(tests)):
        test_file = os.path.join(files_dir, tests[ii])
        answer_file = os.path.join(files_dir, answers[ii])
        # All files contain a single string
        with open(test_file, "r") as fp:
            text = fp.readline().rstrip()
        with open(answer_file, "r") as fp:
            answer_str = fp.readline().rstrip()
            if answer_str == "Success":
                expected = -1
            else:
                expected = int(answer_str)

        result = check_brackets(text)
        assert_test_case(result, text, expected)


def main() -> None:
    tests, answers = load_files()
    tests = sorted(tests)
    answers = sorted(answers)

    test_brackets(tests, answers)
    print("ALL TESTS PASSED!")


if __name__ == "__main__":
    main()
