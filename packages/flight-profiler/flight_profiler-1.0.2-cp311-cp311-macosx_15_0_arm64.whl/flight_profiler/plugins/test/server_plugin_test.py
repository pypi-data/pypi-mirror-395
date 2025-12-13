from asyncio import sleep

from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue


class TestServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    async def do_action(self, param):
        print("server plugin test do action")
        i = 0
        while i < 5:
            i = i + 1
            # stream message 1-5, message 5 marked as end
            await self.out_q.output_msg(
                Message(True if i == 5 else False, "message-" + str(i))
            )
            await sleep(1)


def get_instance(cmd: str, out_q: ServerQueue):
    return TestServerPlugin(cmd, out_q)
