import argparse

from flight_profiler.help_descriptions import TORCH_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.torch.torch_parser import parse_torch_cmd
from flight_profiler.utils.cli_util import (
    common_plugin_execute_routine,
    show_error_info,
    show_normal_info,
)


class TorchCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)
        self.last_cmd = ""

    def get_help(self):
        return TORCH_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        try:
            parse_torch_cmd(cmd)
        except argparse.ArgumentError as e:
            show_error_info(f"Trace command parsed failed, {e}")
            return
        except argparse.ArgumentTypeError as e:
            show_error_info(f"Trace command parsed failed, {e}")
            return
        except:
            show_normal_info(self.get_help())
            return

        self.last_cmd = cmd
        common_plugin_execute_routine(
            cmd="torch",
            param="on " + self.last_cmd,
            port=self.port,
            raw_text=True
        )

    def on_interrupted(self):
        common_plugin_execute_routine(
            cmd="torch",
            param="off " + self.last_cmd,
            port=self.port,
            raw_text=True
        )


def get_instance(port: str, server_pid: int):
    return TorchCliPlugin(port, server_pid)
