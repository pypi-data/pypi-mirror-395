from flight_profiler.help_descriptions import GETGLOBAL_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.getglobal.getglobal_parser import GetGlobalParser
from flight_profiler.utils.cli_util import (
    common_plugin_execute_routine,
    show_normal_info,
)


class GetGlobalCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return GETGLOBAL_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        try:
            GetGlobalParser().parse_getglobal_params(cmd)
        except:
            show_normal_info(self.get_help())
            return

        common_plugin_execute_routine(
            cmd="getglobal",
            param=cmd,
            port=self.port,
            expression_result=True
        )

    def on_interrupted(self):
        pass


def get_instance(port: str, server_pid: int):
    return GetGlobalCliPlugin(port, server_pid)
