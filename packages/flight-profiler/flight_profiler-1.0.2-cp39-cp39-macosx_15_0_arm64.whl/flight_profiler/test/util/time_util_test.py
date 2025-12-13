import time
import unittest

from flight_profiler.utils.time_util import time_ns_to_formatted_string


class TimeUtilTest(unittest.TestCase):

    def test_get_datetime_by_ns(self):
        ns = time.time_ns()
        format_str = time_ns_to_formatted_string(ns)

        self.assertEqual("-", format_str[4])
        self.assertEqual(":", format_str[-4])
