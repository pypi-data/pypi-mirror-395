from flight_profiler.help_descriptions import GILSTAT_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.gilstat.gilstat_parser import valid
from flight_profiler.utils.args_util import split_regex
from flight_profiler.utils.cli_util import common_plugin_execute_routine


class GilStatCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return GILSTAT_COMMAND_DESCRIPTION.help_hint()

    def do_gil_on_action(self, cmd: str, params: list):
        gil_cmd = params[0]
        if len(params) > 1:
            gil_cmd = gil_cmd + " " + str(int(params[1]))
        else:
            gil_cmd = gil_cmd + " 10"
        if len(params) > 2:
            gil_cmd = gil_cmd + " " + str(int(params[2]))
        else:
            gil_cmd = gil_cmd + " 10"
        if len(params) > 3:
            gil_cmd = gil_cmd + " " + str(int(params[3]))
        else:
            gil_cmd = gil_cmd + " 5"
        if len(params) > 4:
            gil_cmd = gil_cmd + " " + str(int(params[4]))
        else:
            gil_cmd = gil_cmd + " 500"

        common_plugin_execute_routine(
            cmd="gilstat",
            param=gil_cmd,
            port=self.port,
            raw_text=True
        )

    def do_gil_off_action(self):
        common_plugin_execute_routine(
            cmd="gilstat",
            param="off",
            port=self.port,
            raw_text=True
        )

    def do_action(self, cmd: str):
        params = split_regex(cmd)
        if not valid(params):
            print(self.get_help())
            return
        if params[0] == "on":
            self.do_gil_on_action(cmd, params)
        elif params[0] == "off":
            self.do_gil_off_action()

    # gilstat off when CTRL+C interrupt client
    def on_interrupted(self):
        self.do_gil_off_action()


def get_instance(port: str, server_pid: int):
    return GilStatCliPlugin(port, server_pid)
