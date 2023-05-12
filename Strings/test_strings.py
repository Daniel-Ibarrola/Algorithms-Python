import strings as stg


class TestStrToInt:

    def test_positive_number(self):
        number = "123"
        assert stg.str_to_int(number) == 123

    def test_negative_number(self):
        number = "-123"
        assert stg.str_to_int(number) == -123


class TestIntToStr:

    def test_positive_number(self):
        number = 123
        assert stg.int_to_str(number) == "123"

    def test_negative_number(self):
        number = 123
        assert stg.int_to_str(number) == "123"
