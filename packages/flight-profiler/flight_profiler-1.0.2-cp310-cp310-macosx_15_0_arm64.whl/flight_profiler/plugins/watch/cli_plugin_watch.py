import argparse
import pickle
from typing import Union

from flight_profiler.communication.flight_client import FlightClient
from flight_profiler.help_descriptions import WATCH_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.watch.watch_agent import WatchSetting
from flight_profiler.plugins.watch.watch_displayer import WatchResult
from flight_profiler.plugins.watch.watch_parser import WatchArgumentParser
from flight_profiler.plugins.watch.watch_render import WatchRender
from flight_profiler.utils.cli_util import (
    common_plugin_execute_routine,
    show_error_info,
    show_normal_info,
)


class WatchCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return WATCH_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        try:
            watch_setting: WatchSetting = WatchArgumentParser().parse_watch_setting(
                cmd
            )
        except argparse.ArgumentError as e:
            show_error_info(f" Watch command parsed failed, {e}")
            return
        except Exception as e:
            show_normal_info(self.get_help())
            return

        self.last_cmd = cmd
        body = {"target": "watch", "param": "on " + cmd}
        try:
            client = FlightClient(host="localhost", port=self.port)
        except:
            show_error_info("Target process exited!")
            return
        try:
            render: WatchRender = WatchRender()
            for content in client.request_stream(body):
                result: Union[WatchResult, str] = pickle.loads(content)
                if type(result) is str:
                    print(result)
                else:
                    print(
                        render.show_watch_result(result, watch_setting.raw_output)
                    )
        finally:
            client.close()

    def on_interrupted(self):
        common_plugin_execute_routine(
            cmd="watch",
            param="off " + self.last_cmd,
            port=self.port,
        )

def get_instance(port: str, server_pid: int):
    return WatchCliPlugin(port, server_pid)
