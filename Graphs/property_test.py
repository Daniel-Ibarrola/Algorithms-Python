

class House:

    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise TypeError
        self._price = new_price


if __name__ == "__main__":
    house = House(1000)
    price = house.price

    price = 2000
    print(house.price)


