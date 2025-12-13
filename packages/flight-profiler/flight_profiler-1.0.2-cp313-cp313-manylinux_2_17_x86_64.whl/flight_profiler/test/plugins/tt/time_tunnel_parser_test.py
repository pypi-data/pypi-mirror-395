import unittest

from flight_profiler.plugins.tt.time_tunnel_agent import TimeTunnelCmd
from flight_profiler.plugins.tt.time_tunnel_parser import TimeTunnelArgumentParser


class TimeTunnelParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = TimeTunnelArgumentParser()

    def test_parse_trace_args(self):

        no_cls_src = "-t __main__ test_func"
        params = self.parser.parse_time_tunnel_cmd(no_cls_src)
        self.assertEqual("__main__", params.module_name)
        self.assertEqual("test_func", params.method_name)
        self.assertEqual("__main__ test_func", params.time_tunnel)
        self.assertIsNone(params.class_name)
        self.assertEqual(50, params.limits)
        self.assertFalse(params.show_list)
        self.assertIsNone(params.index)
        self.assertEqual(2, params.expand_level)
        self.assertIsNone(params.delete_id)
        self.assertFalse(params.delete_all)
        self.assertFalse(params.play)

    def test_parse_args_with_options(self):
        index_src = "-i 1000 -p"
        cmd: TimeTunnelCmd = self.parser.parse_time_tunnel_cmd(index_src)
        self.assertEqual(1000, cmd.index)
        self.assertTrue(cmd.play)
        self.assertIsNone(cmd.time_tunnel)

        filter_src = '-t __main__ A func -f \'args[0]=="hello" and return_obj["success"]==True\' -n 100'
        cmd: TimeTunnelCmd = self.parser.parse_time_tunnel_cmd(filter_src)
        self.assertEqual(
            'args[0]=="hello" and return_obj["success"]==True', cmd.filter_expr
        )
        self.assertEqual(100, cmd.limits)

        delete_src = "-d 1000"
        cmd: TimeTunnelCmd = self.parser.parse_time_tunnel_cmd(delete_src)
        self.assertEqual(1000, cmd.delete_id)
        self.assertFalse(False, cmd.delete_all)

        list_src = "-l -m __main__.A.hello"
        cmd: TimeTunnelCmd = self.parser.parse_time_tunnel_cmd(list_src)
        self.assertTrue(cmd.show_list)
        self.assertEqual("__main__.A.hello", cmd.method_filter)
