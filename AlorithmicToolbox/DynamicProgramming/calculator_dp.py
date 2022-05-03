
def optimal_sequence(number: int) -> list:
    """ Get the optimal sequence to obtain a number "number" from 1.
        Returns a list with the sequence.

        Parameters
        ----------
        number : int
            The final number of the sequence.

        Returns
        -------
        list of int
            The optimal sequence
    """
    # Create a list to store the minimum number of operations for each number
    # up to "number"
    min_ops = [0] * (number + 1)
    min_ops[1] = 1

    for num in range(2, len(min_ops)):
        # Obtain the minimum number of operations for the current number
        # by considering +1, x2 if it's divisble by 2 and x3 if it's 
        # divisible by 3
        num_operations = [min_ops[num - 1]]
        if num % 2 == 0:
            num_operations.append(min_ops[num // 2])
        if num % 3 == 0:
            num_operations.append(min_ops[num // 3])
        
        min_ops[num] = min(num_operations) + 1

    # Create a list to store the optimal sequence, which has lenght min_ops[number]
    # it's first element is one and it's last element is equal to number
    sequence = [0] * min_ops[number]
    sequence[0] = 1
    sequence[-1] = number

    # Iterate the vector of min operations in reverse. To find the optimal
    # sequence we compute for each number the minimum number of operations
    current_num = number
    for ii in range(len(sequence) - 2, 0, -1):
        
        # To store all possible previous numbers in the sequence
        prev_numbers = [(current_num - 1, min_ops[current_num - 1])]
        if current_num % 2 == 0:
            prev_numbers.append((current_num // 2, min_ops[current_num // 2]))
        if current_num % 3 == 0:
            prev_numbers.append((current_num // 3, min_ops[current_num // 3]))

        # Find the previous number with the minimum operations
        current_num, _ = min(prev_numbers, key=lambda n: n[1])
        sequence[ii] = current_num

    return sequence


if __name__ == "__main__":
    print(optimal_sequence(96234))



