import pprint


def lcs(str1: str, str2: str) -> int:
    """ Returns the length of the longest common subsequence
        of two strings.
    """
    
    # Create a table to store the lcs length for each substring
    table = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    
    for ii in range(1, len(str1) + 1):
        for jj in range(1, len(str2) + 1):
            # If characters match add 1 to the left diagonal element
            if str1[ii - 1] == str2[jj - 1]:
                table[ii][jj] = 1 + table[ii - 1][jj - 1]
            else:
                # Take the max of the left and upper elements
                table[ii][jj] = max(table[ii - 1][jj], table[ii][jj - 1])

    pprint.pprint(table)
    return table[-1][-1]


def main() -> None:
    
    length = lcs("ABCDGH", "AEDFHR")
    print(f"LCS lenght is {length}")


if __name__ == '__main__':
    main()
