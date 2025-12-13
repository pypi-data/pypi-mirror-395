import pickle
import unittest

from flight_profiler.plugins.getglobal.getglobal_agent import GlobalGetGlobalAgent
from flight_profiler.plugins.getglobal.getglobal_parser import GetGlobalParams


class GetGlobalAgentTest(unittest.TestCase):

    def test_search_module_var(self):

        params = GetGlobalParams(
            module_name="flight_profiler.test.plugins.getglobal.getglobal_src_module",
            class_name=None,
            variable="global_varA",
            expr="target",
        )

        self.assertEqual(
            str(3), pickle.loads(GlobalGetGlobalAgent.search_global_var(params)).value
        )

        cls_params = GetGlobalParams(
            module_name="flight_profiler.test.plugins.getglobal.getglobal_src_module",
            class_name="TestClass",
            variable="VARB",
            expr="target",
        )
        self.assertEqual(
            "\"hello\"",
            pickle.loads(GlobalGetGlobalAgent.search_global_var(cls_params)).value
        )

        list_params = GetGlobalParams(
            module_name="flight_profiler.test.plugins.getglobal.getglobal_src_module",
            class_name=None,
            variable="global_list",
            expr="target",
        )

        self.assertEqual(
            "[\n  1,\n  2,\n  3\n]",
            pickle.loads(
                GlobalGetGlobalAgent.search_global_var(list_params)
            ).value,
        )

        dict_params = GetGlobalParams(
            module_name="flight_profiler.test.plugins.getglobal.getglobal_src_module",
            class_name=None,
            variable="global_dict",
            expr="target",
        )
        self.assertEqual(
            "{\n  \"hello\": \"world\"\n}",
            pickle.loads(
                GlobalGetGlobalAgent.search_global_var(dict_params)
            ).value
        )
