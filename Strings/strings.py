

def str_to_int(number: str) -> int:
    result = 0
    start = 0
    if number[0] == "-":
        start = 1

    for ii in range(start, len(number)):
        digit = ord(number[ii]) - ord("0")
        result = result*10 + digit

    if start > 0:
        result *= -1
    return result


def int_to_str(number: int) -> str:
    remaining = abs(number)
    result = ""
    while remaining > 0:
        digit = remaining % 10
        result += chr(digit + ord("0"))
        remaining = int(remaining / 10)

    if number < 0:
        remaining += "-"

    return result[::-1]
