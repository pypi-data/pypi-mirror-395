import asyncio
import queue
from asyncio import Queue
from typing import Optional, Union


class Message:
    def __init__(
        self,
        is_end: bool,
        msg: Optional[Union[str, bytes]],
        is_newline: bool = False,
    ):
        self.is_end = is_end
        self.msg = msg
        self.is_newline = is_newline


class ServerQueue:
    def __init__(self, out_q: Queue, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.out_q = out_q
        self.loop = loop

    # for c extension
    def output_msgstr_nowait(self, is_end: int, msg: str):
        # self.out_q.put_nowait(Message(is_end=(True if is_end != 0 else False), msg=msg))
        asyncio.run_coroutine_threadsafe(
            self.out_q.put(Message(is_end=(True if is_end != 0 else False), msg=msg)),
            self.loop,
        )

    def output_msg_nowait(self, msg: Message):
        asyncio.run_coroutine_threadsafe(self.out_q.put(msg), self.loop)

    async def output_msg(self, msg: Message):
        asyncio.run_coroutine_threadsafe(self.out_q.put(msg), self.loop)


class ServerPlugin:

    def __init__(self, cmd: str, out_q: ServerQueue):
        self.cmd = cmd
        self.out_q = out_q
        pass

    async def do_action(self, param):
        pass


class InteractiveServerPlugin(ServerPlugin):

    def __init__(self, cmd: str, in_q: queue.Queue, out_q: ServerQueue):
        super().__init__(cmd, out_q)
        self.in_q = in_q

    def on_connect(self) -> str:
        pass

    async def do_action_no_args(self):
        pass
