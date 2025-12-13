import argparse

from flight_profiler.help_descriptions import VMTOOL_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.vmtool.vmtool_parser import VmtoolArgumentParser
from flight_profiler.utils.cli_util import (
    common_plugin_execute_routine,
    show_error_info,
    show_normal_info,
)


class VmtoolCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return VMTOOL_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        try:
            VmtoolArgumentParser().parse_params(cmd)
        except argparse.ArgumentTypeError as e:
            show_error_info(f" vmtool command parsed failed, {e}")
            return
        except argparse.ArgumentError as e:
            show_error_info(f" vmtool command parsed failed, {e}")
            return
        except:
            show_normal_info(self.get_help())
            return

        common_plugin_execute_routine(
            cmd="vmtool",
            param=cmd,
            port=self.port,
            expression_result=True
        )

    def on_interrupted(self):
        pass


def get_instance(port: str, server_pid: int):
    return VmtoolCliPlugin(port, server_pid)
