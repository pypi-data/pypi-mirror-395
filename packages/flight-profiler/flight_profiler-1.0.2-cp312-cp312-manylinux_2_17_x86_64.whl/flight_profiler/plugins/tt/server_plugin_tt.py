import traceback

from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue
from flight_profiler.plugins.tt.time_tunnel_agent import global_tt_agent
from flight_profiler.plugins.tt.time_tunnel_parser import (
    TimeTunnelArgumentParser,
    TimeTunnelCmd,
)
from flight_profiler.utils.args_util import split_regex


class TimeTunnelServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    async def do_action(self, param):
        if param is None:
            await self.out_q.output_msg(Message(True, "tt param is None"))
            return
        splits = split_regex(param)
        if splits[0] == "on":
            new_param = param[len(splits[0]) :]
            try:
                time_tunnel_cmd: TimeTunnelCmd = (
                    TimeTunnelArgumentParser().parse_time_tunnel_cmd(new_param)
                )
                time_tunnel_cmd.out_q = self.out_q
                global_tt_agent.on_action(time_tunnel_cmd)
            except:
                await self.out_q.output_msg(Message(True, traceback.format_exc()))
        elif splits[0] == "off":
            new_param = param[len(splits[0]) :]
            try:
                time_tunnel_cmd: TimeTunnelCmd = (
                    TimeTunnelArgumentParser().parse_time_tunnel_cmd(new_param)
                )
                time_tunnel_cmd.out_q = self.out_q
                global_tt_agent.off_action(time_tunnel_cmd)
                await self.out_q.output_msg(Message(True, None))
            except:
                await self.out_q.output_msg(Message(True, traceback.format_exc()))
        else:
            await self.out_q.output_msg(Message(True, "tt param is illegal"))


def get_instance(cmd: str, out_q: ServerQueue):
    return TimeTunnelServerPlugin(cmd, out_q)
