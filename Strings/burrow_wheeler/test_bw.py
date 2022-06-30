from inverse import sorted_positions_dict, inverse_burrow_wheeler_transform


def test_sorted_positions_dict():

    positions_expected = {0: 1, 1: 0, 2 : 3, 3: 2}
    assert sorted_positions_dict("badc") == positions_expected

    positions_expected = {
        0: 6,
        1: 0,
        2: 4,
        3: 5,
        4: 1,
        5: 2,
        6: 3,
    }
    assert sorted_positions_dict("AGGGAA$") == positions_expected


def test_inverse_burrow_wheeler_transform():

    assert inverse_burrow_wheeler_transform("AC$A") == "ACA$"
    assert inverse_burrow_wheeler_transform("AGGGAA$") == "GAGAGA$"
    assert inverse_burrow_wheeler_transform("smnpbnnaaaaa$a") == "panamabananas$"
    assert inverse_burrow_wheeler_transform("annb$aa") == "banana$"
