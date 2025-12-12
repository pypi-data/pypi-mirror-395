import unittest

from tna_utilities.currency import currency, pretty_price, pretty_price_range


class TestCurrency(unittest.TestCase):
    def test_happy_number(self):
        self.assertEqual(currency(0), "0")
        self.assertEqual(currency(5), "5")
        self.assertEqual(currency(5.0), "5")
        self.assertEqual(currency(5.00), "5")
        self.assertEqual(currency(5.1), "5.10")
        self.assertEqual(currency(5.01), "5.01")
        self.assertEqual(currency(5.001), "5.00")
        self.assertEqual(currency(5.005), "5.00")
        self.assertEqual(currency(5.006), "5.01")

    def test_happy_string(self):
        self.assertEqual(currency("0"), "0")
        self.assertEqual(currency("5"), "5")
        self.assertEqual(currency("5.0"), "5")
        self.assertEqual(currency("5.00"), "5")
        self.assertEqual(currency("5.1"), "5.10")
        self.assertEqual(currency("5.01"), "5.01")
        self.assertEqual(currency("5.001"), "5.00")
        self.assertEqual(currency("5.005"), "5.00")
        self.assertEqual(currency("5.006"), "5.01")

    def test_happy_not_simplified(self):
        self.assertEqual(currency("0", False), "0.00")
        self.assertEqual(currency("5", False), "5.00")
        self.assertEqual(currency("5.0", False), "5.00")
        self.assertEqual(currency("5.00", False), "5.00")


class TestPrettyPrice(unittest.TestCase):
    def test_happy_number(self):
        self.assertEqual(pretty_price(0), "Free")
        self.assertEqual(pretty_price(0.1), "£0.10")
        self.assertEqual(pretty_price(0.101), "£0.10")
        self.assertEqual(pretty_price(0.001), "Free")
        self.assertEqual(pretty_price(0.009), "£0.01")
        self.assertEqual(pretty_price(1), "£1")
        self.assertEqual(pretty_price(1.1), "£1.10")
        self.assertEqual(pretty_price(1.11), "£1.11")
        self.assertEqual(pretty_price(1.111), "£1.11")
        self.assertEqual(pretty_price(123456789), "£123,456,789")
        self.assertEqual(pretty_price(123456789.01), "£123,456,789.01")

    def test_happy_string(self):
        self.assertEqual(pretty_price("0"), "Free")
        self.assertEqual(pretty_price("0.1"), "£0.10")
        self.assertEqual(pretty_price("0.10"), "£0.10")
        self.assertEqual(pretty_price("0.101"), "£0.10")
        self.assertEqual(pretty_price("0.001"), "Free")
        self.assertEqual(pretty_price("0.009"), "£0.01")
        self.assertEqual(pretty_price("1"), "£1")
        self.assertEqual(pretty_price("01"), "£1")
        self.assertEqual(pretty_price("1.1"), "£1.10")
        self.assertEqual(pretty_price("1.11"), "£1.11")
        self.assertEqual(pretty_price("1.111"), "£1.11")
        self.assertEqual(pretty_price("123456789"), "£123,456,789")
        self.assertEqual(pretty_price("123456789.01"), "£123,456,789.01")

    def test_happy_not_simplified(self):
        self.assertEqual(pretty_price("0", False), "Free")
        self.assertEqual(pretty_price("0.1"), "£0.10")
        self.assertEqual(pretty_price("0.10"), "£0.10")
        self.assertEqual(pretty_price("0.101"), "£0.10")
        self.assertEqual(pretty_price("0.001"), "Free")
        self.assertEqual(pretty_price("0.009"), "£0.01")
        self.assertEqual(pretty_price("5", False), "£5.00")
        self.assertEqual(pretty_price("5.0", False), "£5.00")
        self.assertEqual(pretty_price("5.00", False), "£5.00")


class TestPrettyPriceRange(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(pretty_price_range(0, 0), "Free")
        self.assertEqual(pretty_price_range("0", "0"), "Free")
        self.assertEqual(pretty_price_range(5, 5), "£5")
        self.assertEqual(pretty_price_range("5", 5), "£5")
        self.assertEqual(pretty_price_range(5, "5"), "£5")
        self.assertEqual(pretty_price_range("5", "5"), "£5")
        self.assertEqual(pretty_price_range(5.1, 5.1), "£5.10")
        self.assertEqual(pretty_price_range(0, 5), "Free to £5")
        self.assertEqual(pretty_price_range(None, 5), "Free to £5")
        self.assertEqual(pretty_price_range(5, 0), "From £5")
        self.assertEqual(pretty_price_range(5, 10), "£5 to £10")
        self.assertEqual(pretty_price_range(10, 5), "£5 to £10")
        with self.assertRaises(ValueError):
            pretty_price_range(5, "a")
        with self.assertRaises(TypeError):
            pretty_price_range(5, [])
        with self.assertRaises(TypeError):
            pretty_price_range(5, True)
