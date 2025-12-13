from flight_profiler.help_descriptions import MEM_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.mem.mem_parser import MemCmd
from flight_profiler.utils.args_util import split_regex
from flight_profiler.utils.cli_util import (
    common_plugin_execute_routine,
    show_normal_info,
)


class MemCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return MEM_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        params = split_regex(cmd)
        mem_cmd = MemCmd(params)
        if not mem_cmd.is_valid:
            show_normal_info(mem_cmd.valid_message)
            return

        common_plugin_execute_routine(
            cmd="mem",
            param=cmd,
            port=self.port,
            raw_text=True
        )


def get_instance(port: str, server_pid: int):
    return MemCliPlugin(port, server_pid)
