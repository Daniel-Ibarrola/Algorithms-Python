import numpy as np


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
