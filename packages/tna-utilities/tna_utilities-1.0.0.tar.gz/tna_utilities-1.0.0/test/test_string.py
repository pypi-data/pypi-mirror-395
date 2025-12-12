import unittest

from tna_utilities.string import slugify, unslugify


class TestSlugify(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("test"), "test")
        self.assertEqual(slugify("  test TEST"), "test-test")
        self.assertEqual(slugify("test 12 3 -4 "), "test-12-3-4")
        self.assertEqual(slugify("test---test"), "test-test")
        self.assertEqual(slugify("test---"), "test")
        self.assertEqual(slugify("test---$"), "test")
        self.assertEqual(slugify("test---$---"), "test")

    def test_happy_unicode(self):
        self.assertEqual(slugify("tést"), "test")
        self.assertEqual(slugify("téßt"), "tet")
        self.assertEqual(slugify("tést", allow_unicode=True), "tést")
        self.assertEqual(slugify("téßt", allow_unicode=True), "téßt")

    def test_unhappy_none(self):
        with self.assertRaises(TypeError):
            slugify(None)

    def test_unhappy_boolean(self):
        with self.assertRaises(TypeError):
            slugify(False)

    def test_unhappy_list(self):
        with self.assertRaises(TypeError):
            slugify([])

    def test_unhappy_tuple(self):
        with self.assertRaises(TypeError):
            slugify(("a", "b"))

    def test_unhappy_int(self):
        with self.assertRaises(TypeError):
            slugify(123)

    def test_unhappy_dict(self):
        with self.assertRaises(TypeError):
            slugify({})


class TestUnslugify(unittest.TestCase):
    def test_happy(self):
        self.assertEqual(unslugify("test-test"), "Test test")
        self.assertEqual(unslugify("test-test", capitalize_first=False), "test test")
        self.assertEqual(unslugify("test-123"), "Test 123")
        self.assertEqual(unslugify("test-1-2-3"), "Test 1 2 3")

    def test_unhappy_none(self):
        with self.assertRaises(TypeError):
            unslugify(None)

    def test_unhappy_boolean(self):
        with self.assertRaises(TypeError):
            unslugify(False)

    def test_unhappy_list(self):
        with self.assertRaises(TypeError):
            unslugify([])

    def test_unhappy_tuple(self):
        with self.assertRaises(TypeError):
            unslugify(("a", "b"))

    def test_unhappy_int(self):
        with self.assertRaises(TypeError):
            unslugify(123)

    def test_unhappy_dict(self):
        with self.assertRaises(TypeError):
            unslugify({})
