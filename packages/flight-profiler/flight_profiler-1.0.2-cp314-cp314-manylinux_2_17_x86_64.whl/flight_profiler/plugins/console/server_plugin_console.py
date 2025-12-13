import sys
import traceback
from asyncio import Queue

from flight_profiler.plugins.console.remote_interactive_console import (
    RemoteInteractiveConsole,
)
from flight_profiler.plugins.server_plugin import (
    InteractiveServerPlugin,
    Message,
    ServerQueue,
)


class ConsoleServerPlugin(InteractiveServerPlugin):
    def __init__(self, cmd: str, in_q: Queue, out_q: ServerQueue):
        super().__init__(cmd, in_q, out_q)
        self.loop = out_q.loop

    def on_connect(self) -> str:
        return f"Python {sys.version}\nType 'quit' to exit\n>>> "

    async def do_action_no_args(self):
        origin_stdout, origin_stderr = sys.stdout, sys.stderr
        try:
            RemoteInteractiveConsole(in_q=self.in_q, out_q=self.out_q, loop=self.loop).interact()
            self.out_q.output_msg_nowait(Message(True, None))
            return
        except SystemExit:
            pass
        except:
            err = traceback.format_exc()
            self.out_q.output_msg_nowait(Message(True, err))
            return
        finally:
            sys.stdout, sys.stderr = origin_stdout, origin_stderr
        self.out_q.output_msg_nowait(Message(True, None))


def get_instance(cmd: str, in_q: Queue, out_q: ServerQueue):
    return ConsoleServerPlugin(cmd, in_q, out_q)
