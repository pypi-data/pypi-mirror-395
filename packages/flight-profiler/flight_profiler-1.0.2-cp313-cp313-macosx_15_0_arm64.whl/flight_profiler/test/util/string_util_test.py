import unittest

from flight_profiler.utils.args_util import split_regex, split_space_brackets


class StringUtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_split_regex(self):
        str1 = "1 2    3\t4\t\t5"
        splits = split_regex(str1)
        self.assertEqual(len(splits), 5)
        self.assertEqual(splits[0], "1")
        self.assertEqual(splits[1], "2")
        self.assertEqual(splits[2], "3")
        self.assertEqual(splits[3], "4")
        self.assertEqual(splits[4], "5")

    def test_split_space_brackets(self):

        src = "__module__ test_func {return_obj, args} "
        splits = split_space_brackets(src)
        self.assertEqual(len(splits), 3)
        self.assertEqual(splits[0], "__module__")
        self.assertEqual(splits[1], "test_func")
        self.assertEqual(splits[2], "{return_obj, args}")

        src = "__module__ test_func [{return_obj, args}, {args}] "
        splits = split_space_brackets(src)
        self.assertEqual(len(splits), 3)
        self.assertEqual(splits[0], "__module__")
        self.assertEqual(splits[1], "test_func")
        self.assertEqual(splits[2], "[{return_obj, args}, {args}]")
