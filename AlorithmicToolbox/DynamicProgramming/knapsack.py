
def knapsack(weights: list[int], capacity: int) -> int:
    """ Finds the optimal weight of a knapsack of a given
        capacity.
    """

    # Create a table to store the results
    table = [[0] * (capacity + 1) for _ in range(len(weights) + 1)]

    for item in range(1, len(weights) + 1):
        for current_weight in range(1, capacity + 1):
            # If item weight is greater than the current weight skip it
            if weights[item - 1] > current_weight:
                table[item][current_weight] = table[item - 1][current_weight]
            else:
                table[item][current_weight] = max(
                    table[item - 1][current_weight],
                    weights[item - 1] + table[item - 1][current_weight - weights[item - 1]]
                )
    
    return table[-1][-1]


def main():

    weights = [1, 4, 8]
    capacity = 10
    print("Weights: ", weights)
    print("Knapsack capacity: ", capacity)
    print("Optimal weight: ", knapsack(weights, capacity))

    weights = [4, 5, 5, 6, 6, 6 ,10, 9, 8, 8]
    capacity = 20
    print("Weights: ", weights)
    print("Knapsack capacity: ", capacity)
    print("Optimal weight: ", knapsack(weights, capacity))


if __name__ == "__main__":
    main()