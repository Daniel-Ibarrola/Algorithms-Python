

def sorted_positions_dict(string: str) -> dict[int, int]:
    """ Returns a dictionary with the indexes of the original string
        as keys, and the indexes of the sorted string as value.

        Example:
        -------
            >>> sorted_positions_dict("badc")
            >>> {0: 1, 1: 0, 2 : 3, 3: 2}
    """
    sorted_indices = sorted(range(len(string)), key=lambda k: string[k])
    sorted_positions = {}
    for ii, jj in enumerate(sorted_indices):
        sorted_positions[ii] = jj
    return sorted_positions


def inverse_burrow_wheeler_transform(transform: str) -> str:
    """ Returns the inverse Burrow-Wheeler transform. """
    pass

