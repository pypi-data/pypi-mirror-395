import asyncio
import importlib
import json
import os
import traceback
from asyncio import Queue
from asyncio.exceptions import CancelledError
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional

from flight_profiler.common.system_logger import logger
from flight_profiler.communication.flight_server import FlightServer
from flight_profiler.plugins.server_plugin import (
    InteractiveServerPlugin,
    Message,
    ServerPlugin,
    ServerQueue,
)

_global_task_executor = ThreadPoolExecutor(max_workers=200, thread_name_prefix="flight-profiler-worker-")

def do_action_background(current_plugin: ServerPlugin, param: str):
    async def async_run():
        await current_plugin.do_action(param)

    asyncio.run(async_run())


def do_action_background_no_params(current_plugin: InteractiveServerPlugin):
    async def async_run():
        await current_plugin.do_action_no_args()

    asyncio.run(async_run())


def status(ignored: str) -> Dict[str, str]:
    return {"pid": str(os.getpid()), "app_type": "py_flight_profiler"}


class FlightProfilerServer(FlightServer):

    def __init__(self, host: str, port: int) -> None:
        super().__init__({"console": True})
        self.special_method_dispatcher = {"status": status}
        self.host = host
        self.port = port

    async def run(self):
        await super().start_server(self.host, self.port)

    async def execute_plugin(
        self, cmd: str, param: str, writer: asyncio.StreamWriter
    ) -> None:
        module_name = "flight_profiler.plugins." + cmd + ".server_plugin_" + cmd
        module = importlib.import_module(module_name)
        out_q = Queue(maxsize=200)
        loop = asyncio.get_event_loop()
        current_plugin: ServerPlugin = module.get_instance(
            cmd, ServerQueue(out_q, loop)
        )
        # do action in background
        _global_task_executor.submit(do_action_background, current_plugin, param)

        async def iter_data():
            while True:
                try:
                    # unit: seconds
                    msg: Optional[Message] = await out_q.get()
                    if msg is None:
                        continue
                    if msg.msg is not None:
                        yield msg.msg
                    if msg.is_end:
                        return
                except CancelledError:
                    pass
                except:
                    logger.error(traceback.format_exc())
                    continue

        async for content in iter_data():
            if type(content) is bytes:
                await super().send(content, writer)
            else:
                await super().send(content.encode("utf-8"), writer)

    async def execute_plugin_interactively(
        self,
        cmd: str,
        param: str,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        module_name = "flight_profiler.plugins." + cmd + ".server_plugin_" + cmd
        module = importlib.import_module(module_name)
        out_q = Queue(maxsize=200)
        in_q = Queue(maxsize=200)
        loop = asyncio.get_event_loop()
        current_plugin: InteractiveServerPlugin = module.get_instance(
            cmd, in_q, ServerQueue(out_q, loop)
        )
        # do action in background
        _global_task_executor.submit(do_action_background_no_params, current_plugin)

        try:
            while True:
                msg: Optional[Message] = await out_q.get()
                if msg is None:
                    break
                # interactive cmd output must be str now
                if msg.msg is not None:
                    await super().send(msg.msg.encode("utf-8"), writer)
                if msg.is_end:
                    break
                statement: str = (await super().handle_read(reader)).decode("utf-8")
                await in_q.put(statement)
        except:
            logger.exception(f"interactive {cmd} exit exceptionally: ")

    async def special_calling(
        self, target: str, param: str, writer: asyncio.StreamWriter
    ) -> None:
        result = self.special_method_dispatcher[target](param)
        await super().send(json.dumps(result).encode("utf-8"), writer)
