import time
import traceback

from flight_profiler.help_descriptions import (
    COLOR_END,
    COLOR_WHITE_255,
    MEM_COMMAND_DESCRIPTION,
)
from flight_profiler.plugins.mem.mem_parser import (
    MemCmd,
    MemDiffArgumentParser,
    MemSummaryArgumentParser,
    mem_diff_help_message,
    mem_summary_help_message,
)
from flight_profiler.plugins.server_plugin import Message, ServerPlugin, ServerQueue
from flight_profiler.utils.args_util import split_regex


class MemServerPlugin(ServerPlugin):
    def __init__(self, cmd: str, out_q: ServerQueue):
        super().__init__(cmd, out_q)

    def summary_mem(self, mem_summary_args):
        from pympler import muppy, summary

        all_objects = muppy.get_objects()
        mem_sum = summary.summarize(all_objects)
        contents = ""
        for line in summary.format_(
            mem_sum,
            limit=getattr(mem_summary_args, "limit"),
            sort="size",
            order=getattr(mem_summary_args, "order"),
        ):
            contents = contents + line + "\n"
        return contents

    def diff_mem(self, mem_diff_args):
        from pympler import muppy, summary

        all_objects = muppy.get_objects()
        mem_sum1 = summary.summarize(all_objects)
        interval = getattr(mem_diff_args, "interval")
        self.out_q.output_msg_nowait(
            Message(False, "wait for " + str(interval) + " seconds")
        )
        time.sleep(interval)
        all_objects = muppy.get_objects()
        mem_sum2 = summary.summarize(all_objects)
        diff = summary.get_diff(mem_sum1, mem_sum2)
        contents = ""
        for line in summary.format_(
            diff,
            limit=getattr(mem_diff_args, "limit"),
            sort="size",
            order=getattr(mem_diff_args, "order"),
        ):
            contents = contents + line + "\n"
        return contents

    async def do_action(self, param):
        try:
            params = split_regex(param)
            mem_cmd = MemCmd(params)
            if not mem_cmd.is_valid:
                await self.out_q.output_msg(Message(True, mem_cmd.valid_message))
                return
            # mem summary
            if mem_cmd.is_summary_cmd:
                try:
                    mem_summary_args = MemSummaryArgumentParser().parse_args(params[1:])
                except:
                    await self.out_q.output_msg(Message(True, mem_summary_help_message))
                    return
                await self.out_q.output_msg(
                    Message(
                        True,
                        f"{COLOR_WHITE_255}{self.summary_mem(mem_summary_args)}{COLOR_END}",
                    )
                )
            # mem diff
            elif mem_cmd.is_diff_cmd:
                try:
                    mem_diff_args = MemDiffArgumentParser().parse_args(params[1:])
                except:
                    await self.out_q.output_msg(Message(True, f"{COLOR_WHITE_255}{mem_diff_help_message}{COLOR_END}"))
                    return
                await self.out_q.output_msg(
                    Message(
                        True, f"{COLOR_WHITE_255}{self.diff_mem(mem_diff_args)}{COLOR_END}"
                    )
                )
            else:
                await self.out_q.output_msg(
                    Message(True, MEM_COMMAND_DESCRIPTION.help_hint())
                )
                return
        except:
            await self.out_q.output_msg(Message(True, traceback.format_exc()))


def get_instance(cmd: str, out_q: ServerQueue):
    return MemServerPlugin(cmd, out_q)
