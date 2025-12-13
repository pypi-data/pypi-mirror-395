import asyncio
import pickle
import unittest
from asyncio import Queue

from flight_profiler.plugins.server_plugin import Message, ServerQueue
from flight_profiler.plugins.trace.trace_agent import global_trace_agent
from flight_profiler.plugins.trace.trace_frame import (
    WrapTraceFrame,
    deserialize_string_frames,
)
from flight_profiler.plugins.trace.trace_parser import TracePoint


class A:
    def test_func(self):
        print("hello")

    async def async_test_func(self):
        print("hello")


def test_func():
    print("hello")


async def async_test_func():
    print("hello")


class TraceAgentTest(unittest.TestCase):

    def test_trace_module_func(self):
        out_q = Queue(maxsize=200)

        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        point = TracePoint(
            module_name="flight_profiler.test.plugins.trace.trace_agent_test",
            class_name=None,
            method_name="test_func",
            interval=0,
            out_q=ServerQueue(out_q, loop),
            limits=10,
            entrance_time=0,
            depth=-1
        )
        global_trace_agent.set_point(point)
        test_func()

        async def get_msg():
            sys_path: Message = await out_q.get()
            hello_title = await out_q.get()
            return sys_path, await out_q.get()

        sys_path, result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)
        self.assertIsNotNone(sys_path)

        wrap: WrapTraceFrame = pickle.loads(result.msg)
        # print(wrap)
        wrap = deserialize_string_frames(wrap)

        self.assertTrue("test_func" in wrap.frames[0].description)
        self.assertTrue("print" in wrap.frames[1].description)

        self.assertTrue(len(global_trace_agent.aop_points) > 0)
        self.assertTrue(
            point.unique_key() in global_trace_agent.aop_points
        )

        global_trace_agent.clear_point(point)
        self.assertTrue(point.unique_key() not in global_trace_agent.aop_points)

    def test_trace_async_module_func(self):
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        point = TracePoint(
            module_name="flight_profiler.test.plugins.trace.trace_agent_test",
            class_name=None,
            method_name="async_test_func",
            interval=0,
            out_q=ServerQueue(out_q, loop),
            limits=10,
            entrance_time=0,
            depth=-1
        )
        global_trace_agent.set_point(point)
        loop.run_until_complete(async_test_func())

        async def get_msg():
            sys_path: Message = await out_q.get()
            hello_title = await out_q.get()
            return sys_path, await out_q.get()

        sys_path, result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)
        self.assertIsNotNone(sys_path)

        wrap: WrapTraceFrame = pickle.loads(result.msg)
        wrap = deserialize_string_frames(wrap)

        self.assertTrue("async_test_func" in wrap.frames[0].description)
        self.assertTrue("print" in wrap.frames[1].description)

        self.assertTrue(len(global_trace_agent.aop_points) > 0)
        self.assertTrue(
            point.unique_key() in global_trace_agent.aop_points
        )

        global_trace_agent.clear_point(point)
        self.assertTrue(point.unique_key() not in global_trace_agent.aop_points)

    def test_trace_cls_func(self):
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        point = TracePoint(
            module_name="flight_profiler.test.plugins.trace.trace_agent_test",
            class_name="A",
            method_name="test_func",
            interval=0,
            out_q=ServerQueue(out_q, loop),
            limits=10,
            entrance_time=0,
            depth=-1
        )
        global_trace_agent.set_point(point)
        A().test_func()

        async def get_msg():
            sys_path: Message = await out_q.get()
            hello_title = await out_q.get()
            return sys_path, await out_q.get()

        sys_path, result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)
        self.assertIsNotNone(sys_path)

        wrap: WrapTraceFrame = pickle.loads(result.msg)
        wrap = deserialize_string_frames(wrap)

        self.assertTrue("test_func" in wrap.frames[0].description)
        self.assertTrue("print" in wrap.frames[1].description)

        self.assertTrue(len(global_trace_agent.aop_points) > 0)
        self.assertTrue(
            point.unique_key() in global_trace_agent.aop_points
        )

        global_trace_agent.clear_point(point)
        self.assertTrue(point.unique_key() not in global_trace_agent.aop_points)

    def test_trace_async_cls_func(self):
        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        point = TracePoint(
            module_name="flight_profiler.test.plugins.trace.trace_agent_test",
            class_name="A",
            method_name="async_test_func",
            interval=0,
            out_q=ServerQueue(out_q, loop),
            limits=10,
            entrance_time=0,
            depth=-1
        )
        global_trace_agent.set_point(point)
        loop.run_until_complete(A().async_test_func())

        async def get_msg():
            sys_path: Message = await out_q.get()
            hello_title = await out_q.get()
            return sys_path, await out_q.get()

        sys_path, result = loop.run_until_complete(get_msg())
        self.assertIsNotNone(result)
        self.assertIsNotNone(sys_path)

        wrap: WrapTraceFrame = pickle.loads(result.msg)
        wrap = deserialize_string_frames(wrap)

        self.assertTrue("async_test_func" in wrap.frames[0].description)
        self.assertTrue("print" in wrap.frames[1].description)

        self.assertTrue(len(global_trace_agent.aop_points) > 0)
        self.assertTrue(
            point.unique_key() in global_trace_agent.aop_points
        )

        global_trace_agent.clear_point(point)
        self.assertTrue(point.unique_key() not in global_trace_agent.aop_points)


if __name__ == "__main__":
    unittest.main()
