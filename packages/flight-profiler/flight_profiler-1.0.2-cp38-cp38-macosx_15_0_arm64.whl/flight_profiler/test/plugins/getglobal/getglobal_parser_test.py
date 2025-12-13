import unittest

from flight_profiler.plugins.getglobal.getglobal_parser import GetGlobalParser


class GetGlobalParserTest(unittest.TestCase):

    def test_parse_getglobal_args(self):
        parser = GetGlobalParser()

        no_cls_src = "--mod __main__ --var C"
        params = parser.parse_getglobal_params(no_cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("C", params.variable)
        self.assertIsNone(params.class_name)
        self.assertEqual("target", params.expr)

        cls_src = "--mod __main__ --cls A --var C"
        params = parser.parse_getglobal_params(cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("C", params.variable)
        self.assertEqual("A", params.class_name)

        no_spec_src = "__main__ C"
        params = parser.parse_getglobal_params(no_spec_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("C", params.variable)
        self.assertIsNone(params.class_name)
        self.assertEqual(2, params.expand_level)

        no_spec_cls_src = "__main__ A C -x 3 -e target.length"
        params = parser.parse_getglobal_params(no_spec_cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("C", params.variable)
        self.assertEqual("A", params.class_name)
        self.assertEqual(3, params.expand_level)
        self.assertEqual("target.length", params.expr)
