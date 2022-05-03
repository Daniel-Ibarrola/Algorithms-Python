from collections import namedtuple


class WrongOperatorError(ValueError):
    pass


def evaluate(num_1: int, num_2: int, operator: str) -> int:
    """ Evaluates an expression consisting of two numbers and an operator
    """
    if operator == "+":
        return num_1 + num_2
    elif operator == "-":
        return num_1 - num_2
    elif operator == "*":
        return num_1 * num_2
    else:
        raise WrongOperatorError(f"{operator} is not a supported operator")


Values = namedtuple("Values", ["min", "max"])


def min_and_max(ii: int,   
                jj: int, 
                max_vals:  list[list[int]],
                min_vals:  list[list[int]], 
                operators: list[str]) -> Values:
    """ Returns the min and max value of an arithmetic subexpression
    """
    min_value = float("inf")
    max_val = float("inf") * -1
    
    for kk in range(ii, jj):

        val_1 = evaluate(max_vals[ii][kk], max_vals[kk + 1][jj], operators[kk])
        val_2 = evaluate(max_vals[ii][kk], min_vals[kk + 1][jj], operators[kk])
        val_3 = evaluate(min_vals[ii][kk], max_vals[kk + 1][jj], operators[kk])
        val_4 = evaluate(min_vals[ii][kk], min_vals[kk + 1][jj], operators[kk])

        min_value = min(min_value, val_1, val_2, val_3, val_4)
        max_val = max(max_val, val_1, val_2, val_3, val_4)

    return Values(min_value, max_val)


def max_value(expression: str) -> int:
    """ Returns the maximum value that can be obtained by
        parenthesizing an arithmetic expression.

        Example: 

        The max value of the following expression 5-8+7*4-8+9 is 
        200 = (5((8+7)x(4(-8+9))))

        Parameters
        ----------
        expression : str
            An arithmetic expression

        Returns
        -------
        int
            max value

    """
    # Create a list to store the numbers and another to store the operators
    sequence = []
    operators = []
    for char in expression:
        if char == "-" or char == "+" or char == "*":
            operators.append(char)
        else:
            sequence.append(int(char))
    
    # Create a table to store the max values of each subexpression and another to
    # store the min values
    max_vals = [[0] * len(sequence) for _ in range(len(sequence))]
    min_vals = [[0] * len(sequence) for _ in range(len(sequence))]

    # Base Case. The expression is a single number
    for ii in range(len(max_vals)):
        max_vals[ii][ii] = sequence[ii]
        min_vals[ii][ii] = sequence[ii]
    
    # Fill the rest of the table diagonally
    nn = len(max_vals)
    jj = 0 # column index
    for ss in range(1, nn):
        for ii in range(0, nn - ss):
            jj = ii + ss
            vals = min_and_max(ii, jj, max_vals, min_vals, operators)
            min_vals[ii][jj] = vals.min
            max_vals[ii][jj] = vals.max

    return max(max_vals[0][-1], min_vals[0][-1])


def main() -> None:

    expressions = ["5-8+7", "4-8+9", "5-8+7*4-8+9"]
    for exp in expressions:
        max_val = max_value(exp)
        print(f"Max value for {exp} is {max_val}")


if __name__ == "__main__":
    main()
