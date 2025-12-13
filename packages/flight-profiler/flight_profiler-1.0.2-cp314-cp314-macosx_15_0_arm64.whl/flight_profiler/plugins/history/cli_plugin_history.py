
import readline

from flight_profiler.common.global_store import get_history_file_path
from flight_profiler.help_descriptions import HISTORY_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.history.history_parser import HistoryParams, HistoryParser


def clear_history_cmd():
    try:
        readline.clear_history()
        with open(get_history_file_path(), "w") as f:
            f.truncate(0)
    except:
        pass


def show_top_history_cmds(limits: int) -> None:
    try:
        readline.write_history_file(get_history_file_path())
        with open(get_history_file_path(), "r") as f:
            lines = f.readlines()
            le = len(lines)
            for cnt in range(min(limits, le), 0, -1):
                idx = le - cnt
                line = lines[idx].strip()
                print(f"    {str(idx + 1).ljust(5)} {line}")
    except:
        return


class HistoryCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return HISTORY_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        try:
            params: HistoryParams = HistoryParser().parse_history_params(cmd)
        except:
            print(self.get_help())
            return

        if params.clear:
            clear_history_cmd()
        else:
            show_top_history_cmds(params.limits)

    def on_interrupted(self):
        pass


def get_instance(port: str, server_pid: int):
    return HistoryCliPlugin(port, server_pid)
