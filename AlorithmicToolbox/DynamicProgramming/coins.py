def min_number_coins(denominations, amount, index):
    
    if amount == 0:
        return 0
    if index >= len(denominations) or denominations[index] > amount:
        return float("inf")
    
    return min(
        min_number_coins(denominations, amount, index + 1),
        1 + min_number_coins(denominations, amount - denominations[index], index)
    )


def main():

    denominations = [1, 2, 5]
    min_coins = min_number_coins(denominations, 6, 0)
    print(f"Min number of coins is {min_coins}")


if __name__=="__main__":
    main()
