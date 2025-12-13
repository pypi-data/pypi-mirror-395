import unittest

from flight_profiler.plugins.trace.trace_frame import (
    FlattenTreeTraceFrame,
    TraceFrame,
    WrapTraceFrame,
    build_frame_stack,
    deserialize_string_frames,
)
from flight_profiler.test.plugins.trace import SENDING_FRAMES


class TraceFrameTest(unittest.TestCase):

    def test_deserialize_string_frame(self):
        wrap_frame: WrapTraceFrame = WrapTraceFrame(SENDING_FRAMES)
        raw_trace_frame: TraceFrame = TraceFrame("print\x00<built-in>\x000", 0)

        self.assertTrue(type(wrap_frame.frames[0]) is str)
        wrap_frame = deserialize_string_frames(wrap_frame)

        self.assertEqual(3, len(wrap_frame.frames))
        self.assertEqual(type(wrap_frame.frames[0]), type(raw_trace_frame))

    def test_build_frame_stack(self):

        wrap_frame: WrapTraceFrame = deserialize_string_frames(
            WrapTraceFrame(SENDING_FRAMES)
        )
        tree_frame: FlattenTreeTraceFrame = build_frame_stack(wrap_frame.frames)

        self.assertEqual(1, len(tree_frame.sub_frames))
        self.assertEqual("hello", tree_frame.method_name)
        self.assertEqual("main.py", tree_frame.filename)
        self.assertEqual("11", tree_frame.line_no)
        self.assertEqual(45188000, tree_frame.cost_ns)
        self.assertEqual(1729678259710756000, tree_frame.start_ns)

        child_frame: FlattenTreeTraceFrame = tree_frame.sub_frames[0]

        self.assertEqual(1, len(child_frame.sub_frames))
        self.assertEqual("test_func", child_frame.method_name)
        self.assertEqual("main.py", child_frame.filename)
        self.assertEqual("28", child_frame.line_no)
        self.assertEqual(45181000, child_frame.cost_ns)
        self.assertEqual(1729678259710761000, child_frame.start_ns)
        self.assertFalse(child_frame.c_frame)

        cc_frame: FlattenTreeTraceFrame = child_frame.sub_frames[0]

        self.assertEqual(0, len(cc_frame.sub_frames))
        self.assertEqual("print", cc_frame.method_name)
        self.assertEqual("<built-in>", cc_frame.filename)
        self.assertEqual("0", cc_frame.line_no)
        self.assertEqual(20000, cc_frame.cost_ns)
        self.assertEqual(1729678259755912000, cc_frame.start_ns)
        self.assertTrue(cc_frame.c_frame)
