import traceback

from flight_profiler.plugins.module.module_agent import ModuleAgent
from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue


class ModuleServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    async def do_action(self, param):

        try:
            # argument verify is already done by client side
            await self.out_q.output_msg(
                Message(True, ModuleAgent.translate_filepath_to_module(param))
            )
        except:
            await self.out_q.output_msg(Message(True, traceback.format_exc()))


def get_instance(cmd: str, out_q: ServerQueue):
    return ModuleServerPlugin(cmd, out_q)
