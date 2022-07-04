from inverse import sorted_positions_array, inverse_burrow_wheeler_transform
import numpy as np


def test_sorted_positions_array():

    positions_expected = np.array([13, 8, 9, 12, 7, 10, 11, 1, 2, 3, 4, 5, 0, 6])
    assert np.all(sorted_positions_array("smnpbnnaaaaa$a") == positions_expected)


def test_inverse_burrow_wheeler_transform():

    assert inverse_burrow_wheeler_transform("AC$A") == "ACA$"
    assert inverse_burrow_wheeler_transform("AGGGAA$") == "GAGAGA$"
    assert inverse_burrow_wheeler_transform("smnpbnnaaaaa$a") == "panamabananas$"
    assert inverse_burrow_wheeler_transform("annb$aa") == "banana$"
