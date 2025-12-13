import asyncio
import sys
from asyncio import Queue
from code import InteractiveConsole
from io import StringIO

from flight_profiler.plugins.server_plugin import Message, ServerQueue


class RemoteInteractiveConsole(InteractiveConsole):
    def __init__(self, in_q: Queue, out_q: ServerQueue, loop: asyncio.AbstractEventLoop):
        InteractiveConsole.__init__(self, globals())
        self.in_q = in_q
        self.out_q = out_q
        self.loop = loop
        self.set_buffer()

    def set_buffer(self):
        self.out_buffer = StringIO()
        sys.stdout = sys.stderr = self.out_buffer

    def unset_buffer(self) -> str:
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        value = self.out_buffer.getvalue()
        self.out_buffer.close()
        return value

    def raw_input(self, prompt=""):
        # render last output
        output = self.unset_buffer()
        if output is not None and output.endswith("\n"):
            # client side print already flush to next line
            output = output[:-1]
        self.out_q.output_msg_nowait(Message(False, "\n".join((prompt, output))))

        # generate next output
        cmd = asyncio.run_coroutine_threadsafe(self.in_q.get(), self.loop).result()
        self.set_buffer()
        return cmd
