import unittest

from tna_utilities import strtobool


class TestStrToBool(unittest.TestCase):
    def test_happy_truthy(self):
        self.assertEqual(strtobool("y"), True)
        self.assertEqual(strtobool("Y"), True)
        self.assertEqual(strtobool("t"), True)
        self.assertEqual(strtobool("true"), True)
        self.assertEqual(strtobool("on"), True)
        self.assertEqual(strtobool("1"), True)

    def test_happy_falsy(self):
        self.assertEqual(strtobool("n"), False)
        self.assertEqual(strtobool("N"), False)
        self.assertEqual(strtobool("no"), False)
        self.assertEqual(strtobool("f"), False)
        self.assertEqual(strtobool("false"), False)
        self.assertEqual(strtobool("off"), False)
        self.assertEqual(strtobool("0"), False)

    def test_unhappy_invalid(self):
        with self.assertRaises(ValueError):
            strtobool("")
        with self.assertRaises(ValueError):
            strtobool("maybe")
        with self.assertRaises(TypeError):
            strtobool(True)
        with self.assertRaises(TypeError):
            strtobool(False)
        with self.assertRaises(TypeError):
            strtobool(42)
        with self.assertRaises(TypeError):
            strtobool(None)
        with self.assertRaises(TypeError):
            strtobool({})
        with self.assertRaises(TypeError):
            strtobool(())
