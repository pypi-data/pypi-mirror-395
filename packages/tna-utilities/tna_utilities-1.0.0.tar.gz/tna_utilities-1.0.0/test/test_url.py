import unittest

from tna_utilities.url import QueryStringTransformer


class TestQueryStringObject:
    def lists(self):
        return iter(
            [
                ("a", ["1"]),
                ("b", ["2", "3"]),
            ]
        )


class TestQuery(unittest.TestCase):
    def test_init(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        self.assertEqual(manipulator.get_query_string(), "?a=1&b=2&b=3")

    def test_parameter_values(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        self.assertEqual(manipulator.parameter_values("a"), ["1"])
        self.assertEqual(manipulator.parameter_values("b"), ["2", "3"])
        with self.assertRaises(AttributeError):
            manipulator.parameter_values("c")

    def test_add_parameter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)

        manipulator.add_parameter("c", [])
        self.assertTrue(manipulator.parameter_exists("c"))
        self.assertEqual(manipulator.parameter_values("c"), [])

        manipulator.add_parameter("d", None)
        self.assertTrue(manipulator.parameter_exists("d"))
        self.assertEqual(manipulator.parameter_values("d"), [])

        manipulator.add_parameter("e", "")
        self.assertTrue(manipulator.parameter_exists("e"))
        self.assertEqual(manipulator.parameter_values("e"), [""])

        manipulator.add_parameter("f", "4")
        self.assertTrue(manipulator.parameter_exists("f"))
        self.assertEqual(manipulator.parameter_values("f"), ["4"])

        manipulator.add_parameter("g", ["5", "6"])
        self.assertTrue(manipulator.parameter_exists("g"))
        self.assertEqual(manipulator.parameter_values("g"), ["5", "6"])

        manipulator.add_parameter("h", [False])
        self.assertTrue(manipulator.parameter_exists("h"))
        self.assertEqual(manipulator.parameter_values("h"), ["False"])

        self.assertEqual(
            manipulator.get_query_string(), "?a=1&b=2&b=3&e=&f=4&g=5&g=6&h=False"
        )

    def test_update_parameter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        manipulator.update_parameter("a", "10")
        self.assertEqual(manipulator.parameter_values("a"), ["10"])
        manipulator.update_parameter("b", ["20", "30"])
        self.assertEqual(manipulator.parameter_values("b"), ["20", "30"])
        manipulator.update_parameter("c", ["40"])
        self.assertEqual(manipulator.parameter_values("c"), ["40"])
        self.assertEqual(manipulator.get_query_string(), "?a=10&b=20&b=30&c=40")

    def test_remove_parameter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        manipulator.remove_parameter("a")
        self.assertFalse(manipulator.parameter_exists("a"))
        manipulator.remove_parameter("b")
        self.assertFalse(manipulator.parameter_exists("b"))
        with self.assertRaises(AttributeError):
            manipulator.remove_parameter("c")
        self.assertEqual(manipulator.get_query_string(), "?")

    def test_is_value_in_parameter(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        self.assertTrue(manipulator.is_value_in_parameter("a", "1"))
        self.assertTrue(manipulator.is_value_in_parameter("b", "2"))
        self.assertTrue(manipulator.is_value_in_parameter("b", "3"))
        self.assertFalse(manipulator.is_value_in_parameter("b", "4"))
        with self.assertRaises(AttributeError):
            self.assertFalse(manipulator.is_value_in_parameter("c", "5"))

    def test_toggle_parameter_value(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        manipulator.toggle_parameter_value("a", "1")
        self.assertFalse(manipulator.is_value_in_parameter("a", "1"))
        manipulator.toggle_parameter_value("a", "10")
        self.assertTrue(manipulator.is_value_in_parameter("a", "10"))
        manipulator.toggle_parameter_value("b", "2")
        self.assertFalse(manipulator.is_value_in_parameter("b", "2"))
        self.assertEqual(manipulator.get_query_string(), "?a=10&b=3")
        manipulator.toggle_parameter_value("a", "1")
        self.assertTrue(manipulator.is_value_in_parameter("a", "1"))
        self.assertEqual(manipulator.get_query_string(), "?a=10&a=1&b=3")

    def test_add_remove_parameter_value(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        manipulator.add_parameter_value("a", "10")
        self.assertTrue(manipulator.is_value_in_parameter("a", "10"))
        self.assertEqual(manipulator.parameter_values("a"), ["1", "10"])

    def test_remove_parameter_value(self):
        test_query = TestQueryStringObject()
        manipulator = QueryStringTransformer(test_query)
        manipulator.remove_parameter_value("b", "2")
        self.assertFalse(manipulator.is_value_in_parameter("b", "2"))
        self.assertEqual(manipulator.parameter_values("b"), ["3"])
