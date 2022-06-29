from inverse import sorted_positions_dict, inverse_burrow_wheeler_transform


def test_sorted_positions_dict():

    positions_expected = {0: 1, 1: 0, 2 : 3, 3: 2}
    assert sorted_positions_dict("badc") == positions_expected


def test_inverse_burrow_wheeler_transform():

    assert inverse_burrow_wheeler_transform("AC$A") == "ACA$"
    assert inverse_burrow_wheeler_transform("AGGGAA$") == "GAGAGA$"
    assert inverse_burrow_wheeler_transform("smnpbnnaaaaa$a") == "panamabananas$"
    assert inverse_burrow_wheeler_transform("annb$aa") == "banana$"
