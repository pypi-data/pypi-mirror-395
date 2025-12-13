import os
import tempfile
import threading
import traceback

from flight_profiler.ext.stack_C import dump_all_threads_stack
from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue
from flight_profiler.utils.args_util import split_regex
from flight_profiler.utils.shell_util import resolve_symbol_address


class StackServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    def add_thread_name(self, contents):
        threads = threading.enumerate()
        thread_map = dict()
        for thread in threads:
            thread_map[thread.ident] = thread.name
        new_contents = ""
        for content in contents:
            if content.startswith("Thread 0x"):
                thread_id = int(split_regex(content)[1][2:], 16)
                if thread_map.__contains__(thread_id):
                    new_contents = (
                        new_contents
                        + "("
                        + thread_map[thread_id]
                        + ")"
                        + content[len("Thread") :]
                    )
                else:
                    new_contents = new_contents + content
            elif content.startswith("Current thread 0x"):
                thread_id = int(split_regex(content[len("Current thread 0x")])[0], 16)
                if thread_map.__contains__(thread_id):
                    new_contents = (
                        new_contents
                        + "("
                        + thread_map[thread_id]
                        + ")"
                        + content[len("Current thread") :]
                    )
                else:
                    new_contents = new_contents + content
            else:
                new_contents = new_contents + content
        return new_contents

    async def do_action(self, param):
        tmp_fd, tmp_file_path = tempfile.mkstemp()
        try:
            addr = resolve_symbol_address("_Py_DumpTracebackThreads", os.getpid())
            if addr is None:
                await self.out_q.output_msg(
                    Message(True, "symbol _Py_DumpTracebackThreads not found")
                )
                return
            # dump stack to tempfile
            dump_all_threads_stack(tmp_fd, int(addr))
            with open(tmp_file_path, "r") as f:
                contents = f.readlines()
                await self.out_q.output_msg(
                    Message(True, self.add_thread_name(contents))
                )
        except:
            await self.out_q.output_msg(Message(True, traceback.format_exc()))


def get_instance(cmd: str, out_q: ServerQueue):
    return StackServerPlugin(cmd, out_q)
