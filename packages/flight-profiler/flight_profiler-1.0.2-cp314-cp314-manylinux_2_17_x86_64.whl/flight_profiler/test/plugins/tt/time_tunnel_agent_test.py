import asyncio
import pickle
import unittest
from asyncio import Queue

from flight_profiler.plugins.server_plugin import ServerQueue
from flight_profiler.plugins.tt.time_tunnel_agent import global_tt_agent
from flight_profiler.plugins.tt.time_tunnel_parser import TimeTunnelArgumentParser
from flight_profiler.plugins.tt.time_tunnel_recorder import (
    BaseInvocationRecord,
    FullInvocationRecord,
    global_tt_indexer,
)


class A:
    def func(self):
        print("hello")

    async def async_func(self):
        print("hello")


def func():
    print("hello")


async def async_func():
    print("hello")


class TimeTunnelAgentTest(unittest.TestCase):

    def test_time_tunnel_module_method(self):
        global_tt_indexer.refresh()
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        tt_cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd(
            "-t flight_profiler.test.plugins.tt.time_tunnel_agent_test func"
        )
        tt_cmd.out_q = ServerQueue(out_q, loop)
        global_tt_agent.on_action(tt_cmd)

        func()

        async def get_msg_with_title(q):
            title = await q.get()
            return await q.get()

        async def get_msg_wo_title(q):
            return await q.get()

        result = loop.run_until_complete(get_msg_with_title(out_q))
        self.assertIsNotNone(result)

        record: BaseInvocationRecord = pickle.loads(result.msg)

        self.assertEqual(
            "flight_profiler.test.plugins.tt.time_tunnel_agent_test", record.module_name
        )
        self.assertIsNone(record.class_name)
        self.assertEqual("func", record.method_name)
        self.assertTrue(record.is_ret)
        self.assertFalse(record.is_exp)

        global_tt_agent.clear_tt_point(tt_cmd)

        out_q = Queue(maxsize=200)
        tt_cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd("-i 1000")
        tt_cmd.out_q = ServerQueue(out_q, loop)
        global_tt_agent.on_action(tt_cmd)
        result = loop.run_until_complete(get_msg_wo_title(out_q))

        self.assertIsNotNone(result)

        record: FullInvocationRecord = pickle.loads(result.msg)

        self.assertEqual(type(record), FullInvocationRecord)

        base_record = record.base_record
        self.assertEqual(
            "flight_profiler.test.plugins.tt.time_tunnel_agent_test",
            base_record.module_name,
        )
        self.assertIsNone(base_record.class_name)
        self.assertEqual("func", base_record.method_name)
        self.assertTrue(base_record.is_ret)
        self.assertFalse(base_record.is_exp)

        out_q = Queue(maxsize=200)
        tt_cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd("-i 1000 -p")
        tt_cmd.out_q = ServerQueue(out_q, loop)
        global_tt_agent.on_action(tt_cmd)
        result = loop.run_until_complete(get_msg_wo_title(out_q))

        self.assertIsNotNone(result)

        record: FullInvocationRecord = pickle.loads(result.msg)

        self.assertEqual(type(record), FullInvocationRecord)

        base_record = record.base_record
        self.assertNotEqual(1000, base_record.index)
        self.assertEqual(
            "flight_profiler.test.plugins.tt.time_tunnel_agent_test",
            base_record.module_name,
        )
        self.assertIsNone(base_record.class_name)
        self.assertEqual("func", base_record.method_name)
        self.assertTrue(base_record.is_ret)
        self.assertFalse(base_record.is_exp)

        out_q = Queue(maxsize=200)
        tt_cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd("-d 1000")
        tt_cmd.out_q = ServerQueue(out_q, loop)
        global_tt_agent.on_action(tt_cmd)
        result = loop.run_until_complete(get_msg_wo_title(out_q))

        self.assertIsNotNone(result)
        self.assertTrue("Index 1000 is deleted successfully" in result.msg)

    def test_time_tunnel_class_method(self):
        global_tt_indexer.refresh()
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        tt_cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd(
            "-t flight_profiler.test.plugins.tt.time_tunnel_agent_test A func"
        )
        tt_cmd.out_q = ServerQueue(out_q, loop)
        global_tt_agent.on_action(tt_cmd)

        A().func()

        async def get_msg_with_title():
            await out_q.get()
            return await out_q.get()

        result = loop.run_until_complete(get_msg_with_title())
        self.assertIsNotNone(result)

        record: BaseInvocationRecord = pickle.loads(result.msg)

        self.assertEqual(
            "flight_profiler.test.plugins.tt.time_tunnel_agent_test", record.module_name
        )
        self.assertEqual("A", record.class_name)
        self.assertEqual("func", record.method_name)
        self.assertTrue(record.is_ret)
        self.assertFalse(record.is_exp)

        global_tt_agent.clear_tt_point(tt_cmd)

    def test_time_tunnel_async_module_func(self):
        global_tt_indexer.refresh()
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        tt_cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd(
            "-t flight_profiler.test.plugins.tt.time_tunnel_agent_test async_func"
        )
        tt_cmd.out_q = ServerQueue(out_q, loop)
        global_tt_agent.on_action(tt_cmd)

        loop.run_until_complete(async_func())

        async def get_msg():
            await out_q.get()
            return await out_q.get()

        result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)
        self.assertFalse(result.is_end)

        record: BaseInvocationRecord = pickle.loads(result.msg)

        self.assertEqual(
            "flight_profiler.test.plugins.tt.time_tunnel_agent_test", record.module_name
        )
        self.assertIsNone(record.class_name)
        self.assertEqual("async_func", record.method_name)
        self.assertTrue(record.is_ret)
        self.assertFalse(record.is_exp)

    def test_time_tunnel_async_class_func(self):
        global_tt_indexer.refresh()
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        tt_cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd(
            "-t flight_profiler.test.plugins.tt.time_tunnel_agent_test A async_func"
        )
        tt_cmd.out_q = ServerQueue(out_q, loop)
        global_tt_agent.on_action(tt_cmd)

        loop.run_until_complete(A().async_func())

        async def get_msg():
            await out_q.get()
            return await out_q.get()

        result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)
        self.assertFalse(result.is_end)

        record: BaseInvocationRecord = pickle.loads(result.msg)

        self.assertEqual(
            "flight_profiler.test.plugins.tt.time_tunnel_agent_test", record.module_name
        )
        self.assertEqual("A", record.class_name)
        self.assertEqual("async_func", record.method_name)
        self.assertTrue(record.is_ret)
        self.assertFalse(record.is_exp)


if __name__ == "__main__":
    unittest.main()
