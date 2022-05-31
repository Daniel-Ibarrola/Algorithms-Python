# Program to search for substring occurrences in another string using
# Rabin-Karp's algorithm


def poly_hash(string: str, prime: int, multiplier: int) -> int:
    """ Polynomial hash function. Returns the hash of a string.
    """
    hash_ = 0
    for char in reversed(string):
        hash_ = (hash_ * multiplier + ord(char)) % prime
    return hash_


def precompute_hashes(text: str, pattern_size: int,
                      prime: int, multiplier: int) -> list[int]:
    """ Precompute the hashes of the substrings of the 'text' string
    """
    text_size = len(text)

    hashes = [0] * (text_size - pattern_size + 1)
    sub_str = text[text_size - pattern_size: text_size]
    hashes[text_size - pattern_size] = poly_hash(sub_str, prime, multiplier)

    y = 1
    for ii in range(1, pattern_size + 1):
        y = (y * multiplier) % prime

    for ii in range(text_size - pattern_size - 1, -1, -1):
        hashes[ii] = (multiplier * hashes[ii + 1] + ord(text[ii]) -
                      y * ord(text[ii + pattern_size])) % prime

    return hashes


def search_substring(text: str, pattern: str) -> list[int]:
    """ Returns a list with all positions where the substring 'pattern' is found
        on the string 'text'.

        Uses Robin-Karp's algorithm.
    """
    positions: list[int]
    positions = []

    if len(text) == 0 or len(pattern) == 0:
        return positions
    if len(pattern) > len(text):
        return positions

    prime = 1000000007
    multiplier = 263
    pattern_hash = poly_hash(pattern, prime, multiplier)
    hashes = precompute_hashes(text, len(pattern), prime, multiplier)

    for ii in range(0, len(text) - len(pattern) + 1):
        if pattern_hash != hashes[ii]:
            continue
        if text[ii: ii + len(pattern)] == pattern:
            positions.append(ii)

    return positions
