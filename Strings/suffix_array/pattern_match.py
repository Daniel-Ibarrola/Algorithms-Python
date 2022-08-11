
def pattern_in_suffix(pattern: str, suffix: str) -> bool:
    """ Checks if the pattern is at the start of the suffix.
    """
    if len(suffix) < len(pattern):
        return False

    if suffix[0: len(pattern)] == pattern:
        return True
    return False


def pattern_matching_with_suffix_array(suffix_array: list[int],
                                       text: str, pattern: str) -> tuple[int, int]:
    """ Returns a tuple where the first element is the starting index int
        the suffix array where there is a match of the pattern and the second
        element is the last index where there is a match.

        If there are no matches it returns (-1, -1)
    """
    if len(suffix_array) == 0 or len(pattern) == 0 \
            or len(pattern) > len(text):
        return -1, -1

    # Use binary search to find the leftmost element in the
    # suffix array that contains the pattern.
    left = -1
    right = len(text) - 1
    while right - left > 1:
        middle = int(left + (right - left) / 2)
        suffix = text[suffix_array[middle]:]
        if pattern_in_suffix(pattern, suffix) or suffix > pattern:
            right = middle
        else:
            left = middle

    first = right
    # Use binary search to find the rightmost element in the
    # suffix array that contains the pattern.
    left = 0
    right = len(text)
    while right - left > 1:
        middle = int(left + (right - left) / 2)
        suffix = text[suffix_array[middle]:]
        if pattern_in_suffix(pattern, suffix) or suffix < pattern:
            left = middle
        else:
            right = middle

    last = left

    if first > last:
        return -1, -1

    return first, last
