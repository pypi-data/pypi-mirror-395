import unittest

from flight_profiler.plugins.watch.watch_parser import WatchArgumentParser


class WatchParserTest(unittest.TestCase):

    def test_parse_trace_args(self):
        parser = WatchArgumentParser()

        no_cls_src = "__main__ test_func"
        params = parser.parse_watch_setting(no_cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertFalse(params.record_on_exception)

        filter_src = r'__main__ test_func -f "args[0][\"query\"]==\"he llo\""'
        params = parser.parse_watch_setting(filter_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertEqual('args[0]["query"]=="he llo"', params.filter_expr)
        self.assertEqual(1 + 2, params.watch_displayer.expand_level)
        self.assertFalse(params.record_on_exception)

        filter_exc_src = "__main__ test_func -f args[0]['query']=='hello' --exception "
        params = parser.parse_watch_setting(filter_exc_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertEqual("args[0]['query']=='hello'", params.filter_expr)
        self.assertTrue(params.record_on_exception)

        filter_sim_exc_src = "__main__ test_func -f args[0]['query']=='hello' -e -x 3"
        params = parser.parse_watch_setting(filter_sim_exc_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertEqual("args[0]['query']=='hello'", params.filter_expr)
        self.assertEqual(3 + 2, params.watch_displayer.expand_level)
        self.assertTrue(params.record_on_exception)
