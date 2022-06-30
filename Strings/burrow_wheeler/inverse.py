
def sorted_positions_dict(string: str) -> dict[int, int]:
    """ Returns a dictionary with the indexes of the original string
        as keys, and the indexes of the sorted string as value.

        Example:
        -------
            >>> sorted_positions_dict("badc")
            >>> {0: 1, 1: 0, 2 : 3, 3: 2}
    """
    sorted_indices = sorted(range(len(string)), key=lambda k: string[k])
    return {
        ii: jj for ii, jj in enumerate(sorted_indices)
    }


def inverse_burrow_wheeler_transform(transform: str) -> str:
    """ Returns the inverse Burrow-Wheeler transform. """

    sorted_positions = sorted_positions_dict(transform)
    inverse = "$"
    for ii in range(len(sorted_positions)):
        pass

    assert len(inverse) == len(transform), "inverse and transform aren't the same size"
    return inverse[::-1]
