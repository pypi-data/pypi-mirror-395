import pickle
import traceback

from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue
from flight_profiler.plugins.watch import watch_agent
from flight_profiler.plugins.watch.watch_agent import global_watch_agent
from flight_profiler.plugins.watch.watch_parser import WatchArgumentParser
from flight_profiler.utils.args_util import split_regex


class WatchServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    async def do_action(self, param):
        splits = split_regex(param)
        if splits[0] == "on":
            new_param = param[len(splits[0]) :]
            try:
                watch_setting: watch_agent.WatchSetting = (
                    WatchArgumentParser().parse_watch_setting(new_param)
                )
                watch_setting.out_q = self.out_q
                global_watch_agent.add_watch(watch_setting)
                # will not return end message, server request will block
            except:
                await self.out_q.output_msg(Message(True, traceback.format_exc()))
        elif splits[0] == "off":
            new_param = param[len(splits[0]) :]
            try:
                watch_setting: watch_agent.WatchSetting = (
                    WatchArgumentParser().parse_watch_setting(new_param)
                )
                watch_setting.out_q = self.out_q
                global_watch_agent.clear_watch(watch_setting)
                await self.out_q.output_msg(Message(True, None))
            except:
                await self.out_q.output_msg(Message(True, traceback.format_exc()))
        else:
            await self.out_q.output_msg(Message(True, pickle.dumps("watch param is illegal")))


def get_instance(cmd: str, out_q: ServerQueue):
    return WatchServerPlugin(cmd, out_q)
