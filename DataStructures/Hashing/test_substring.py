from substring import search_substring, poly_hash, precompute_hashes


def test_poly_hash():

    multiplier = 263
    prime = 1000000007
    hash_ = poly_hash("world", prime, multiplier)
    assert hash_ % 5 == 4

    hash_ = poly_hash("Hell0", prime, multiplier)
    assert hash_ % 5 == 4

    hash_ = poly_hash("GooD", prime, multiplier)
    assert hash_ % 5 == 2

    hash_ = poly_hash("luck", prime, multiplier)
    assert hash_ % 5 == 2


def test_precompute_hashes():

    text = "world"
    pattern = "orl"
    multiplier = 263
    prime = 1000000007
    hashes = precompute_hashes(text, len(pattern), prime, multiplier)
    assert hashes == [7914578, 7500345, 6945418]


def test_empty_string():

    text = "Hello world"
    positions = search_substring(text, '')
    assert len(positions) == 0


def test_equal_string():

    text = "Hello world"
    positions = search_substring(text, "Hello world")
    assert len(positions) == 1
    assert positions == [0]


def test_larger_string():

    text = "banana"
    pattern = "banana-split"
    positions = search_substring(text, pattern)
    assert len(positions) == 0


def test_substring():

    text = "abacaba"
    pattern = "aba"
    positions = search_substring(text, pattern)
    assert positions == [0, 4]

    text = "testTesttesT"
    pattern = "Test"
    positions = search_substring(text, pattern)
    assert positions == [4]

    text = "baaaaaaa"
    pattern = "aaaaa"
    positions = search_substring(text, pattern)
    assert positions == [1, 2, 3]

    text = "banana"
    pattern = "ana"
    positions = search_substring(text, pattern)
    assert positions == [1, 3]

    text = "My dog ate all the pizza."
    pattern = "dog"
    positions = search_substring(text, pattern)
    assert positions == [3]

    text = "Hello book duck table duck cellphone duck"
    pattern = "duck"
    positions = search_substring(text, pattern)
    assert len(positions) == 3
    assert text[positions[0]:positions[0] + len(pattern)] == "duck"
    assert text[positions[1]:positions[1] + len(pattern)] == "duck"
    assert text[positions[2]:positions[2] + len(pattern)] == "duck"


