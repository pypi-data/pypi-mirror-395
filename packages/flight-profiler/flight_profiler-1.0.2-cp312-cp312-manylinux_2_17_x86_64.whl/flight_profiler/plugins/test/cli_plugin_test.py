from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.utils.cli_util import common_plugin_execute_routine


class TestCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def do_action(self, cmd):
        common_plugin_execute_routine(
            cmd="test",
            param=cmd,
            port=self.port,
            raw_text=True
        )

    def on_interrupted(self):
        pass


def get_instance(port: str, server_pid: int):
    return TestCliPlugin(port, server_pid)
