import traceback

from flight_profiler.help_descriptions import COLOR_END, COLOR_WHITE_255
from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue
from flight_profiler.plugins.torch.torch_agent import global_torch_agent
from flight_profiler.plugins.torch.torch_parser import parse_torch_cmd
from flight_profiler.utils.args_util import split_regex


class TorchServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    async def do_action(self, param):

        try:
            if param is None:
                await self.out_q.output_msg(
                    Message(is_end=True, msg="torch params is None")
                )
            splits = split_regex(param)
            if splits[0] == "on":
                param = param[len(splits[0]) :]
                cmd = parse_torch_cmd(param)
                cmd.out_q = self.out_q
                global_torch_agent.on_action(cmd)
            elif splits[0] == "off":
                param = param[len(splits[0]) :]
                cmd = parse_torch_cmd(param)
                cmd.out_q = self.out_q
                global_torch_agent.clear_spy(cmd)
                await self.out_q.output_msg(
                    Message(
                        True,
                        msg=f"{COLOR_WHITE_255}Canceled by user interrupt, target method is not called during spy.{COLOR_END}",
                    )
                )
            else:
                await self.out_q.output_msg(
                    Message(True, "torch params is illegal")
                )
        except:
            await self.out_q.output_msg(Message(True, traceback.format_exc()))


def get_instance(cmd: str, out_q: ServerQueue):
    return TorchServerPlugin(cmd, out_q)
