import os
import traceback

from flight_profiler.ext.gilstat_C import deinit_gil_interceptor, init_gil_interceptor
from flight_profiler.help_descriptions import GILSTAT_COMMAND_DESCRIPTION
from flight_profiler.plugins.gilstat.gilstat_parser import valid
from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue
from flight_profiler.utils.args_util import split_regex
from flight_profiler.utils.shell_util import resolve_symbol_address


class GilStatServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    def enable_gil_stat(self, params):
        take_gil_addr = resolve_symbol_address("take_gil", os.getpid())
        drop_gil_addr = resolve_symbol_address("drop_gil", os.getpid())
        if len(params) > 1:
            take_threshold = int(params[1])
        else:
            take_threshold = 5
        if len(params) > 2:
            hold_threshold = int(params[2])
        else:
            hold_threshold = 5
        if len(params) > 3:
            stat_interval = int(params[3])
        else:
            stat_interval = 5
        if len(params) > 4:
            max_stat_threads = int(params[4])
        else:
            max_stat_threads = 500
        return init_gil_interceptor(
            self.out_q,
            take_gil_addr,
            drop_gil_addr,
            take_threshold,
            hold_threshold,
            stat_interval,
            max_stat_threads,
        )

    def disable_gil_stat(self):
        return deinit_gil_interceptor()

    async def do_action(self, param):
        params = split_regex(param)
        if not valid(params):
            await self.out_q.output_msg(
                Message(True, GILSTAT_COMMAND_DESCRIPTION.help_hint())
            )
            return
        try:
            if params[0] == "on":
                if self.enable_gil_stat(params) != 0:
                    await self.out_q.output_msg(Message(True, "gilstat enable failed"))
                else:
                    # will not return end message, server request will block
                    pass
            elif params[0] == "off":
                if self.disable_gil_stat() != 0:
                    await self.out_q.output_msg(Message(True, "gilstat disable failed"))
                else:
                    await self.out_q.output_msg(Message(True, None))

        except:
            await self.out_q.output_msg(Message(True, traceback.format_exc()))


def get_instance(cmd: str, out_q: ServerQueue):
    return GilStatServerPlugin(cmd, out_q)
