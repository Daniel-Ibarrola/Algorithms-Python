# Program that implements a "primitive calculator". This calculator can only do 
# certain operations such as add 1, multiply 2 and multiply 3. Here we use a greegy
# algorithm which is easy to implement. However, it's not always correct.

def calculator_greedy(amount: int) -> tuple:
    """ Greedy algorithm for the primitive calculator. Doesn't always give
        the correct answer.
    """
    number = 1
    num_operations = 0
    sequence = [number]

    while number != amount:

        if number * 3 <= amount:
            number *= 3
        elif number * 2 <= amount:
            number *= 2
        elif number + 1 <= amount:
            number += 1
        else:
            assert False, "This should not happen"

        num_operations += 1
        sequence.append(number)

    return sequence, num_operations


def assert_test_case(result: int, expected: int,
                     amount, function_name: str) -> None:
    message = f"Wrong result on {function_name} with amount {amount}. "
    message += f"Expected {expected}, got {result}"
    assert result == expected, message


def test_calculator_greedy(amount: list,
                           expected: list) -> None:
    # Greedy algorithm fails with 15, it gives 8. The answer should be 4

    for ii in range(len(amount)):
        result = calculator_greedy(amount[ii])
        assert_test_case(result, expected[ii], amount[ii], calculator_greedy.__name__)


def main():
    amount = [1, 2, 3, 6, 10, 15]
    expected = [0, 1, 1, 2, 3, 4]

    test_calculator_greedy(amount, expected)


if __name__ == "__main__":
    main()
