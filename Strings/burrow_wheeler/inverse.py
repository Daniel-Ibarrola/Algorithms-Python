import numpy as np


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


def sorted_positions_array(string: str) -> np.ndarray:
    """ Returns an array with the indices that each character
        would have in the sorted string
    """
    sorted_indices = [ii[0] for ii in sorted(enumerate(string), key=lambda x: x[1])]
    return np.argsort(sorted_indices)


def inverse_burrow_wheeler_transform(transform: str) -> str:
    """ Returns the inverse Burrow-Wheeler transform. """

    sorted_positions = sorted_positions_array(transform)
    inverse = ""
    next_index = 0

    for _ in range(0, len(transform) - 1):
        inverse += transform[next_index]
        next_index = sorted_positions[next_index]

    inverse = inverse[::-1]
    return inverse + '$'
