import asyncio
import pickle
import time
import unittest
from asyncio import Queue
from typing import Tuple

from flight_profiler.plugins.server_plugin import Message, ServerQueue
from flight_profiler.plugins.tt.time_tunnel_parser import TimeTunnelArgumentParser
from flight_profiler.plugins.tt.time_tunnel_recorder import (
    BaseInvocationRecord,
    FullInvocationRecord,
    TimeTunnelRecorder,
    global_tt_indexer,
)


class A:
    def func(self, name):
        return name


class TimeTunnelRecorderTest(unittest.TestCase):

    def record_and_return(self) -> Tuple[TimeTunnelRecorder, FullInvocationRecord]:
        global_tt_indexer.refresh()
        recorder = TimeTunnelRecorder()
        record = recorder.records(
            index=global_tt_indexer.get_index(),
            start_time=int(time.time()),
            cost_ms=40,
            is_ret=True,
            is_exp=False,
            module_name="flight_profiler.test.plugins.tt.time_tunnel_recorder_test",
            class_name="A",
            method_name="func",
            args=[None, "key1"],
            kwargs={},
            return_obj="key1",
            exp_obj=None,
        )
        return recorder, record

    def test_records(self):
        recorder, record = self.record_and_return()

        self.assertEqual(type(record), FullInvocationRecord)
        self.assertEqual(1, len(recorder.invocation_records))

    def test_show_list_records(self):
        recorder, record = self.record_and_return()

        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd(
            "-l -m flight_profiler.test.plugins.tt.time_tunnel_recorder_test.A.func"
        )
        cmd.out_q = ServerQueue(out_q, loop)

        recorder.show_list_records(cmd)

        async def get_msg(q):
            return await q.get()

        msg: Message = loop.run_until_complete(get_msg(out_q))
        self.assertTrue(msg.is_end)
        record_list = pickle.loads(msg.msg)

        self.assertEqual(type(record_list), list)
        self.assertEqual(1, len(record_list))
        self.assertEqual(type(record_list[0]), BaseInvocationRecord)
        self.assertEqual(
            "flight_profiler.test.plugins.tt.time_tunnel_recorder_test",
            record_list[0].module_name,
        )
        self.assertEqual("A", record_list[0].class_name)
        global_tt_indexer.refresh()

        cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd("-l -m __main__.B.func")
        cmd.out_q = ServerQueue(out_q, loop)

        loop = asyncio.get_event_loop()
        recorder.show_list_records(cmd)

        msg: Message = loop.run_until_complete(get_msg(out_q))
        record_list = pickle.loads(msg.msg)
        self.assertTrue(msg.is_end)
        self.assertEqual(type(record_list), list)
        self.assertEqual(0, len(record_list))

    def test_index_records(self):
        recorder, record = self.record_and_return()

        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd("-i 1000")
        cmd.out_q = ServerQueue(out_q, loop)

        recorder.show_indexed_record(cmd)

        async def get_msg(q):
            return await q.get()

        msg: Message = loop.run_until_complete(get_msg(out_q))
        self.assertTrue(msg.is_end)

        full_record: FullInvocationRecord = pickle.loads(msg.msg)
        self.assertEqual(1000, full_record.base_record.index)
        self.assertEqual("[\n  \"key1\"\n]", full_record.args)
        self.assertEqual("None", full_record.exp_obj)
        self.assertTrue(full_record.base_record.is_ret)
        self.assertFalse(full_record.base_record.is_exp)

    def test_delete(self):
        recorder, record = self.record_and_return()

        self.assertEqual(1, len(recorder.invocation_records))
        self.assertFalse(recorder.delete_specified_record(400))
        self.assertTrue(recorder.delete_specified_record(1000))
        self.assertEqual(0, len(recorder.invocation_records))

    def test_replay_method(self):
        recorder, record = self.record_and_return()

        out_q = Queue(maxsize=200)
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        cmd = TimeTunnelArgumentParser().parse_time_tunnel_cmd("-i 1000 -p")
        cmd.out_q = ServerQueue(out_q, loop)

        recorder.replay_time_fragment(cmd)

        async def get_msg(q):
            return await q.get()

        msg: Message = loop.run_until_complete(get_msg(out_q))
        self.assertTrue(msg.is_end)

        full_record: FullInvocationRecord = pickle.loads(msg.msg)
        self.assertEqual(1001, full_record.base_record.index)
        self.assertEqual("[\n  \"key1\"\n]", full_record.args)
        self.assertEqual("None", full_record.exp_obj)
        self.assertTrue(full_record.base_record.is_ret)
        self.assertFalse(full_record.base_record.is_exp)
