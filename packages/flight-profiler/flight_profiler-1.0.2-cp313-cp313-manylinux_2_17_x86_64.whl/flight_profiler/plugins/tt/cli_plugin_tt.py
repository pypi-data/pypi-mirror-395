import argparse
import pickle
import sys
from typing import Union

from flight_profiler.communication.flight_client import FlightClient
from flight_profiler.help_descriptions import TIME_TUNNEL_COMMAND_DESCRIPTION
from flight_profiler.plugins.cli_plugin import BaseCliPlugin
from flight_profiler.plugins.tt.time_tunnel_parser import (
    TimeTunnelArgumentParser,
    TimeTunnelCmd,
)
from flight_profiler.plugins.tt.time_tunnel_recorder import (
    BaseInvocationRecord,
    FullInvocationRecord,
)
from flight_profiler.plugins.tt.time_tunnel_render import TimeTunnelRender
from flight_profiler.utils.cli_util import (
    common_plugin_execute_routine,
    show_error_info,
    show_normal_info,
)
from flight_profiler.utils.render_util import COLOR_END, COLOR_RED


class TimeTunnelCliPlugin(BaseCliPlugin):
    def __init__(self, port, server_pid):
        super().__init__(port, server_pid)

    def get_help(self):
        return TIME_TUNNEL_COMMAND_DESCRIPTION.help_hint()

    def do_action(self, cmd):
        try:
            tt_cmd: TimeTunnelCmd = (
                TimeTunnelArgumentParser().parse_time_tunnel_cmd(cmd)
            )
            tt_cmd.valid()
        except argparse.ArgumentTypeError as e:
            show_error_info(f" Trace command parsed failed, {e}")
            return
        except:
            show_normal_info(self.get_help())
            return

        self.last_cmd = cmd
        body = {"target": "tt", "param": "on " + cmd}
        try:
            client = FlightClient(host="localhost", port=self.port)
        except:
            show_error_info("Target process exited!")
            return
        try:
            render = TimeTunnelRender()
            if tt_cmd.time_tunnel is not None:
                first_chunk = True
                spy_chunk = True
                for content in client.request_stream(body):
                    is_first = False
                    if spy_chunk:
                        spy_chunk = False
                    elif first_chunk:
                        is_first = True
                        first_chunk = False

                    cli_base_record: Union[BaseInvocationRecord, str] = (
                        pickle.loads(content)
                    )
                    if type(cli_base_record) == str:
                        print(cli_base_record)
                    else:
                        render.render_tt_record(cli_base_record, is_first=is_first)
                    sys.stdout.flush()

            elif tt_cmd.index is not None:
                received_response: bool = False
                for content in client.request_stream(body):
                    received_response = True
                    full_record: Union[FullInvocationRecord, str] = (
                        pickle.loads(content)
                    )
                    if type(full_record) is str:
                        print(f"{COLOR_RED}{full_record}{COLOR_END}")
                    else:
                        render.render_indexed_record(full_record)
                    sys.stdout.flush()
                if not received_response:
                    print(
                        f"{COLOR_RED} There is no available index {tt_cmd.index} time fragments."
                    )

            elif tt_cmd.show_list:
                for content in client.request_stream(body):
                    render.render_records_list(content)
                    sys.stdout.flush()
            else:
                for line in client.request_stream(body):
                    if line:
                        line = line.decode("utf-8")
                        print(line)
                    sys.stdout.flush()
        finally:
            client.close()

    def on_interrupted(self):
        common_plugin_execute_routine(
            cmd="tt",
            param="off " + self.last_cmd,
            port=self.port,
        )


def get_instance(port: str, server_pid: int):
    return TimeTunnelCliPlugin(port, server_pid)
