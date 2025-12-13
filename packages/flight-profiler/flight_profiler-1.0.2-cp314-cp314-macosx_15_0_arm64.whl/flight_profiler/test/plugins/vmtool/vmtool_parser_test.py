import argparse
import unittest

from flight_profiler.plugins.vmtool.vmtool_parser import (
    VmtoolArgumentParser,
    VmtoolParams,
)


class VmtoolParserTest(unittest.TestCase):

    def test_parse(self):
        src = "-a getInstances -c __main__ A"
        parser = VmtoolArgumentParser()
        param: VmtoolParams = parser.parse_params(src)

        self.assertEqual("getInstances", param.action)
        self.assertEqual("__main__", param.module_name)
        self.assertEqual("A", param.class_name)

        src = "-a getInstances -c __main__ A -e 'instances[0].target'"
        parser = VmtoolArgumentParser()
        param: VmtoolParams = parser.parse_params(src)

        self.assertEqual("getInstances", param.action)
        self.assertEqual("__main__", param.module_name)
        self.assertEqual("A", param.class_name)
        self.assertEqual("instances[0].target", param.expr)

        gc_src = "-a forceGc"
        param: VmtoolParams = parser.parse_params(gc_src)
        self.assertEqual("forceGc", param.action)
        self.assertIsNone(param.class_location)

    def test_parse_exp(self):

        src = "-a xxx -c __main__ A"
        parser = VmtoolArgumentParser()
        with self.assertRaises(argparse.ArgumentTypeError):
            parser.parse_params(src)

        src = "-a getInstances"
        with self.assertRaises(argparse.ArgumentTypeError):
            parser.parse_params(src)
