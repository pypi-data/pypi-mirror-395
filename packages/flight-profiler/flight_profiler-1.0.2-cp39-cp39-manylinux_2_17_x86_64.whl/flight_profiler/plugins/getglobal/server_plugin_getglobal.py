import pickle
import traceback

from flight_profiler.plugins.getglobal.getglobal_agent import GlobalGetGlobalAgent
from flight_profiler.plugins.getglobal.getglobal_parser import (
    GetGlobalParams,
    GetGlobalParser,
)
from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue


class GetGlobalServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    async def do_action(self, param):

        try:
            get_global_params: GetGlobalParams = (
                GetGlobalParser().parse_getglobal_params(param)
            )
            self.out_q.output_msg_nowait(
                Message(
                    True,
                    GlobalGetGlobalAgent.search_global_var(get_global_params),
                )
            )
        except:
            self.out_q.output_msg_nowait(
                Message(True, pickle.dumps(traceback.format_exc()))
            )


def get_instance(cmd: str, out_q: ServerQueue):
    return GetGlobalServerPlugin(cmd, out_q)
