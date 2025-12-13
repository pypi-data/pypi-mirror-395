import unittest

from flight_profiler.plugins.trace.trace_parser import TraceArgumentParser


class TraceParserTest(unittest.TestCase):

    def test_parse_trace_args(self):
        parser = TraceArgumentParser()

        no_cls_src = "--mod __main__ --func test_func"
        params = parser.parse_trace_point(no_cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertIsNone(params.class_name)
        self.assertEqual(0.1, params.interval)

        no_cls_src = "__main__ test_func"
        params = parser.parse_trace_point(no_cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertIsNone(params.class_name)
        self.assertEqual(0.1, params.interval)

        cls_src = "--mod __main__ --cls A --func test_func"
        params = parser.parse_trace_point(cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertEqual("A", params.class_name)
        self.assertEqual(0.1, params.interval)

        cls_src = "__main__ A test_func"
        params = parser.parse_trace_point(cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertEqual("A", params.class_name)
        self.assertEqual(0.1, params.interval)

        cls_src = "__main__ A test_func -i 10"
        params = parser.parse_trace_point(cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertEqual("A", params.class_name)
        self.assertEqual(10, params.interval)
