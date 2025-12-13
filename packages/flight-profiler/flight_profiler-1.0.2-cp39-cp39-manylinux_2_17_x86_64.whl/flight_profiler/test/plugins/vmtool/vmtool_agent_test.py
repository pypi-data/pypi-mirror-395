import unittest

from flight_profiler.common.expression_result import ExpressionResult
from flight_profiler.plugins.vmtool.vmtool_agent import GLOBAL_VMTOOL_AGENT
from flight_profiler.plugins.vmtool.vmtool_parser import (
    VmtoolArgumentParser,
    VmtoolParams,
)


class A:
    def test_func(self):
        print("hello")

    async def async_test_func(self):
        print("hello")


class NotExist:
    def __init__(self):
        pass


def test_func():
    print("hello")


async def async_test_func():
    print("hello")


class VmtoolAgentTest(unittest.TestCase):

    def test_getInstances(self):
        params: VmtoolParams = VmtoolArgumentParser().parse_params(
            "-a getInstances -c flight_profiler.test.plugins.vmtool.vmtool_agent_test A"
        )

        test_a = A()
        result: ExpressionResult = GLOBAL_VMTOOL_AGENT.do_action(params)

        self.assertIsNotNone(result.type)
        self.assertTrue("A({})" in result.value)
        self.assertIsNone(result.failed_reason)
        self.assertFalse(result.failed)

        params: VmtoolParams = VmtoolArgumentParser().parse_params(
            "-a getInstances -c flight_profiler.test.plugins.vmtool.vmtool_agent_test NotExist"
        )

        result = GLOBAL_VMTOOL_AGENT.do_action(params)

        self.assertEqual("instances", result.expr)
        self.assertFalse(result.failed)

        params: VmtoolParams = VmtoolArgumentParser().parse_params(
            "-a getInstances -c flight_profiler.test.plugins.vmtool.vmtool_agent_test A -e instan"
        )

        test_a = A()
        result = GLOBAL_VMTOOL_AGENT.do_action(params)

        self.assertTrue(result.failed)
        self.assertIsNotNone(result.failed_reason)

    def test_forceGc(self):
        params: VmtoolParams = VmtoolArgumentParser().parse_params("-a forceGc")

        result = GLOBAL_VMTOOL_AGENT.do_action(params)
        self.assertTrue("Gc execute successfully" in result)


if __name__ == "__main__":
    unittest.main()
