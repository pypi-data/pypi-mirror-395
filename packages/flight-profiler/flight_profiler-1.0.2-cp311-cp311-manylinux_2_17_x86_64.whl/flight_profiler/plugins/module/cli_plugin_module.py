from argparse import ArgumentError, ArgumentTypeError

from flight_profiler.help_descriptions import MODULE_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.module.module_parser import ModuleArgumentParser
from flight_profiler.utils.cli_util import (
    common_plugin_execute_routine,
    show_error_info,
    show_normal_info,
)


class ModuleCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return MODULE_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        try:
            file_path = ModuleArgumentParser().parse_full_filepath(cmd)
        except ArgumentError as e:
            show_error_info(f"Parse module argument failed: {e}")
            return
        except ArgumentTypeError as e:
            show_error_info(f"Parse module argument failed: {e}")
            return
        except:
            show_normal_info(self.get_help())
            return

        common_plugin_execute_routine(
            cmd="module",
            param=file_path,
            port=self.port,
            raw_text=True
        )

    def on_interrupted(self):
        pass


def get_instance(port: str, server_pid: int):
    return ModuleCliPlugin(port, server_pid)
