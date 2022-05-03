
def min_edit_distance(str_1: str, str_2: str) -> int:
    """ Returns minimum edit distance """

    distances = [[0] * (len(str_1) + 1) for _ in range(len(str_2) + 1)]

    for ii in range(len(str_2) + 1):
        distances[ii][0] = ii

    for jj in range(len(str_2) + 1):
        distances[0][jj] = jj

    for ii in range(1, len(str_1) + 1):
        for jj in range(1, len(str_2) + 1):
        
            if str_1[ii - 1] == str_2[jj - 1]:
                distances[ii][jj] = distances[ii - 1][jj - 1]
            else:
                distances[ii][jj] = 1 + min(
                    distances[ii - 1][jj],
                    distances[ii][jj - 1],
                    distances[ii - 1][jj - 1],
                )
    
    return distances[len(str_1)][len(str_2)]


if __name__ == "__main__":
    print(min_edit_distance("short", "ports"))
