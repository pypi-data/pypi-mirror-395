import inspect
import os.path
import sys
import unittest
from types import FrameType

from flight_profiler.utils.frame_util import get_class_name, global_filepath_operator


class TestClass:

    def frame(self):
        return inspect.currentframe()


def test_func() -> FrameType:
    return inspect.currentframe()


class FrameUtilTest(unittest.TestCase):

    def test_class_name(self):
        frame = TestClass().frame()
        self.assertEqual("TestClass", get_class_name(frame))

        frame = test_func()
        self.assertIsNone(get_class_name(frame))

    def test_shorten_path(self):
        global_filepath_operator.set_sys_path([])
        current_file_path: str = os.path.abspath(__file__)
        self.assertEqual(
            current_file_path,
            global_filepath_operator.shorten_filepath(current_file_path),
        )

        global_filepath_operator.clear()
        global_filepath_operator.set_sys_path(sys.path)
        self.assertEqual(
            "flight_profiler/test/util/frame_util_test.py",
            global_filepath_operator.shorten_filepath(current_file_path),
        )
