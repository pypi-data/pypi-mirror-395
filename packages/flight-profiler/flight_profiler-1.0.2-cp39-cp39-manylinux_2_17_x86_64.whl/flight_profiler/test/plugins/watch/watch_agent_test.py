import asyncio
import pickle
import unittest
from asyncio import Queue

from flight_profiler.plugins.server_plugin import ServerQueue
from flight_profiler.plugins.watch.watch_agent import global_watch_agent
from flight_profiler.plugins.watch.watch_displayer import WatchResult
from flight_profiler.plugins.watch.watch_parser import WatchArgumentParser


class A:
    def test_func(self):
        return "hello"


async def async_test_func():
    return "hello"


def test_func():
    return "hello"


def test_builtin_func():
    serialize_msg = pickle.dumps("hello")
    return pickle.loads(serialize_msg)


class WatchAgentTest(unittest.TestCase):

    def test_watch_module_func(self):
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        watch_setting = WatchArgumentParser().parse_watch_setting(
            "flight_profiler.test.plugins.watch.watch_agent_test test_func --expr return_obj"
        )
        watch_setting.out_q = ServerQueue(out_q, loop)
        global_watch_agent.add_watch(watch_setting)
        test_func()

        async def get_msg():
            await out_q.get()
            return await out_q.get()

        result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)

        watch_result: WatchResult = pickle.loads(result.msg)
        self.assertTrue(isinstance(watch_result, WatchResult))
        self.assertEqual("\"hello\"", watch_result.value)

        self.assertTrue(
            "flight_profiler.test.plugins.watch.watch_agent_test&None&test_func&None"
            in global_watch_agent.aop_points
        )
        global_watch_agent.clear_watch(watch_setting)
        self.assertTrue(
            "flight_profiler.test.plugins.watch.watch_agent_test&None&test_func&None"
            not in global_watch_agent.aop_points
        )

    def test_watch_module_async_func(self):
        out_q = Queue(maxsize=200)
        watch_setting = WatchArgumentParser().parse_watch_setting(
            "flight_profiler.test.plugins.watch.watch_agent_test async_test_func --expr return_obj"
        )
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        watch_setting.out_q = ServerQueue(out_q, loop)
        global_watch_agent.add_watch(watch_setting)
        loop.run_until_complete(async_test_func())

        async def get_msg():
            await out_q.get()
            return await out_q.get()

        result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)

        watch_result: WatchResult = pickle.loads(result.msg)
        self.assertTrue(isinstance(watch_result, WatchResult))
        self.assertEqual("\"hello\"", watch_result.value)

        self.assertTrue(
            "flight_profiler.test.plugins.watch.watch_agent_test&None&async_test_func&None"
            in global_watch_agent.aop_points
        )
        global_watch_agent.clear_watch(watch_setting)
        self.assertTrue(
            "flight_profiler.test.plugins.watch.watch_agent_test&None&async_test_func&None"
            not in global_watch_agent.aop_points
        )

    def test_watch_class_func(self):
        out_q = Queue(maxsize=200)
        watch_setting = WatchArgumentParser().parse_watch_setting(
            "flight_profiler.test.plugins.watch.watch_agent_test A test_func --expr return_obj"
        )
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        watch_setting.out_q = ServerQueue(out_q, loop)
        global_watch_agent.add_watch(watch_setting)
        A().test_func()

        async def get_msg():
            await out_q.get()
            return await out_q.get()

        result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)

        watch_result: WatchResult = pickle.loads(result.msg)
        self.assertTrue(isinstance(watch_result, WatchResult))
        self.assertEqual("\"hello\"", watch_result.value)

        self.assertTrue(
            "flight_profiler.test.plugins.watch.watch_agent_test&A&test_func&None"
            in global_watch_agent.aop_points
        )
        global_watch_agent.clear_watch(watch_setting)
        self.assertTrue(
            "flight_profiler.test.plugins.watch.watch_agent_test&A&test_func&None"
            not in global_watch_agent.aop_points
        )

    def test_watch_builtin_func(self):
        out_q = Queue(maxsize=200)
        watch_setting = WatchArgumentParser().parse_watch_setting(
            "pickle loads --expr return_obj"
        )
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        watch_setting.out_q = ServerQueue(out_q, loop)
        global_watch_agent.add_watch(watch_setting)
        test_builtin_func()

        async def get_msg():
            await out_q.get()
            return await out_q.get()

        result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)

        watch_result: WatchResult = pickle.loads(result.msg)
        self.assertTrue(isinstance(watch_result, WatchResult))
        self.assertEqual("\"hello\"", watch_result.value)

        self.assertTrue("pickle&None&loads&None" in global_watch_agent.aop_points)
        global_watch_agent.clear_watch(watch_setting)
        self.assertTrue("pickle&None&loads&None" not in global_watch_agent.aop_points)


if __name__ == "__main__":
    unittest.main()
