import argparse
import os
from argparse import RawTextHelpFormatter
from typing import Optional

from flight_profiler.common.global_store import get_inject_server_pid
from flight_profiler.help_descriptions import PERF_COMMAND_DESCRIPTION
from flight_profiler.utils.args_util import rewrite_args


class PerfParams:

    def __init__(
        self, pid: int, filepath: Optional[str], duration: int, sample_rate: int
    ):
        self.pid = pid
        self.filepath = filepath
        self.duration = duration
        self.sample_rate = sample_rate

        if self.filepath is None:
            cwd_path: str = os.getcwd()
            if cwd_path.endswith("/"):
                self.filepath = cwd_path + "flamegraph.svg"
            else:
                self.filepath = cwd_path + "/flamegraph.svg"
        self.filepath = os.path.abspath(os.path.expanduser(self.filepath))


class PerfParser(argparse.ArgumentParser):

    def __init__(self):
        super(PerfParser, self).__init__(
            description=PERF_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False
        self.add_argument(
            "--pid",
            required=False,
            help="target process pid.",
            default=get_inject_server_pid(),
        )
        self.add_argument(
            "-r",
            "--rate",
            required=False,
            type=int,
            help="sample rate per second.",
            default=100,
        )
        self.add_argument(
            "-d",
            "--duration",
            required=False,
            type=int,
            help="sample duration seconds, default is unlimited",
            default=-1,
        )
        self.add_argument(
            "-f",
            "--filepath",
            required=False,
            help="dump stack trace flamegraph to filepath.",
            default=None,
        )

    def error(self, message):
        raise Exception(message)

    def parse_perf_params(self, arg_string: str) -> PerfParams:

        new_args = rewrite_args(arg_string, unspec_names=["pid"], omit_column=None)
        args = self.parse_args(args=new_args)
        return PerfParams(
            pid=getattr(args, "pid"),
            filepath=getattr(args, "filepath"),
            duration=getattr(args, "duration"),
            sample_rate=getattr(args, "rate"),
        )


global_perf_parser = PerfParser()
