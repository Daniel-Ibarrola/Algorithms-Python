from pattern_match import pattern_matching_with_suffix_array, pattern_in_suffix


def test_pattern_is_in_suffix():

    pattern = "abra"
    suffix = "abracadabra$"
    assert pattern_in_suffix(pattern, suffix)

    suffix = "abra"
    assert pattern_in_suffix(pattern, suffix)

    suffix = "bracadabra$"
    assert not pattern_in_suffix(pattern, suffix)

    suffix = "adabra$"
    assert not pattern_in_suffix(pattern, suffix)

    suffix = "a$"
    assert not pattern_in_suffix(pattern, suffix)


def test_pattern_matching_with_suffix_array():

    text = "abracadabra$"
    pattern = "abra"
    suffix_array = [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
    matches = pattern_matching_with_suffix_array(suffix_array, text, pattern)
    assert matches == (2, 3)

    text = "panamabananas$"
    pattern = "ana"
    suffix_array = [13, 5, 3, 1, 7, 9, 11, 6, 4, 2, 8, 10, 0, 12]
    matches = pattern_matching_with_suffix_array(suffix_array, text, pattern)
    assert matches == (3, 5)
