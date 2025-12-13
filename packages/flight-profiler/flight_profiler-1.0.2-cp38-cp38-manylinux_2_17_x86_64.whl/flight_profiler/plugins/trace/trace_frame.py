import threading
from typing import Any, Dict, List, Union


class TraceFrame:

    def __init__(self, description: str, start_ns: int):
        """
        :param description: method_name\x00file_name\x00lineno
        : start_ns: method execute start time
        """
        self.description = description
        self.start_ns = start_ns
        self.cost_ns = 0
        self.pid = 0


class WrapTraceFrame:
    """
    server sent frame list, contains frame level infos
    """

    def __init__(self, frames: List[Union[str, TraceFrame]]):
        self.frames = frames
        self.thread_id = threading.get_ident()
        self.thread_name = None
        self.is_daemon = None
        for thread in threading.enumerate():
            if thread.ident == self.thread_id:
                self.thread_name = thread.name
                self.is_daemon = thread.daemon


class FlattenTreeTraceFrame:

    def __init__(
        self,
        description: str,
        start_ns: int,
        cost_ns: int,
    ):
        infos: List[Any] = description.split("\x00")
        self.method_name = infos[0]
        self.filename = infos[1]
        self.line_no = str(infos[2])
        self.start_ns = start_ns
        self.cost_ns = cost_ns
        self.c_frame = self.filename == "<built-in>"
        self.await_frame = self.method_name == "[await]"
        self.sub_frames: List[FlattenTreeTraceFrame] = []

    def append_child(self, frame) -> None:
        self.sub_frames.append(frame)


def build_frame_stack(frames: List[TraceFrame]) -> FlattenTreeTraceFrame:
    """
    build frame tree by server frame pid list
    """
    frame_map: Dict[int, FlattenTreeTraceFrame] = dict()
    for idx, frame in enumerate(frames):
        if frame is None:
            continue
        tree_frame = FlattenTreeTraceFrame(
            frame.description, frame.start_ns, frame.cost_ns
        )
        frame_map[idx] = tree_frame
        if frame.pid in frame_map:
            frame_map[frame.pid].append_child(tree_frame)
    return frame_map[0]


def deserialize_string_frames(wrap: WrapTraceFrame) -> WrapTraceFrame:
    """
    server frame info is 'method_name\x00file_name\x00lineno\x01start_ns\x01cost_ns\x01parent_id'
    parent_id is the offset of parent frame in wrap.frames, starts with 0.
    """
    deserialized_frames = []
    for frame in wrap.frames:
        if frame is not None:
            parts = frame.split("\x01")
            t = TraceFrame(parts[0], int(parts[1]))
            t.cost_ns = int(parts[2])
            t.pid = int(parts[3])
        else:
            t = None
        deserialized_frames.append(t)
    wrap.frames = deserialized_frames
    return wrap
