import os

from flight_profiler.help_descriptions import CLS_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.utils.cli_util import show_normal_info


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class ClsCliPlugin(BaseCliPlugin):

    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return CLS_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        if cmd is None or len(cmd.strip()) == 0:
            clear_screen()
            return
        else:
            show_normal_info(self.get_help())
            return

    def on_interrupted(self):
        pass


def get_instance(port: str, server_pid: int):
    return ClsCliPlugin(port, server_pid)
