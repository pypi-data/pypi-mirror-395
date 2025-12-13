from flight_profiler.help_descriptions import HELP_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.help.help_agent import global_help_agent
from flight_profiler.utils.args_util import split_regex
from flight_profiler.utils.cli_util import show_normal_info


class HelpCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return HELP_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        if cmd is None:
            show_normal_info(global_help_agent.display_all_commands())
            return
        params = split_regex(cmd)
        if len(params) == 0:
            show_normal_info(global_help_agent.display_all_commands())
        elif len(params) != 1:
            show_normal_info(global_help_agent.hint())
        else:
            show_normal_info(global_help_agent.get_command_description(params[0]))

    def on_interrupted(self):
        pass


def get_instance(port: str, server_pid: int):
    return HelpCliPlugin(port, server_pid)
