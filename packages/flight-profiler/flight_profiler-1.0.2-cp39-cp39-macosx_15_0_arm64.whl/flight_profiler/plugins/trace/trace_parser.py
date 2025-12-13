import argparse
from argparse import RawTextHelpFormatter

from flight_profiler.help_descriptions import TRACE_COMMAND_DESCRIPTION
from flight_profiler.plugins.trace.trace_agent import TracePoint
from flight_profiler.utils.args_util import rewrite_args


def check_interval(value):
    try:
        f_value = float(value)
        return f_value
    except:
        raise argparse.ArgumentTypeError(f"interval: {value} is not a float.")

def check_depth(value):
    try:
        i_value = int(value)
        if i_value < 1:
            raise argparse.ArgumentTypeError(f"{value} should be above 1, or -1")
        # profile property contains two levels
        return i_value
    except:
        raise argparse.ArgumentTypeError(f"{value} is not a integer above 1 or -1")


class TraceArgumentParser(argparse.ArgumentParser):

    def __init__(self):
        super(TraceArgumentParser, self).__init__(
            description=TRACE_COMMAND_DESCRIPTION.help_hint(),
            add_help=True,
            formatter_class=RawTextHelpFormatter,
        )
        if hasattr(self, "exit_on_error"):
            self.exit_on_error = False

        self.add_argument("--mod", required=True, help="module package")
        self.add_argument("--cls", required=False, help="class name")
        self.add_argument("--func", required=True, help="function name")

        self.add_argument("-nm", "--nested-method", required=False, help="nested method")
        self.add_argument("-d",
                          "--depth",
                          required=False,
                          help="only display method invocation at most #depth.",
                          type=check_depth,
                          default=-1)
        self.add_argument(
            "-i",
            "--interval",
            type=check_interval,
            required=False,
            help="only show function which cost is larger than #interval milliseconds",
            default=0.1,
        )
        self.add_argument(
            "-et",
            "--entrance_time",
            type=check_interval,
            required=False,
            help="only show function which entrance cost is larger than #interval milliseconds",
            default=0,
        )
        self.add_argument(
            "-n",
            "--limits",
            type=int,
            required=False,
            help="threshold of trace method times, default is 10.",
            default=10,
        )
        self.add_argument(
            "-f",
            "--filter_expr",
            required=False,
            default=None,
            help="filter expression",
        )

    def error(self, message):
        raise Exception(message)

    def parse_trace_point(self, arg_string: str) -> TracePoint:
        new_args = rewrite_args(
            arg_string, unspec_names=["mod", "cls", "func"], omit_column="cls"
        )
        args = self.parse_args(args=new_args)
        point: TracePoint = TracePoint(
            module_name=getattr(args, "mod"),
            class_name=getattr(args, "cls"),
            method_name=getattr(args, "func"),
            depth=getattr(args, "depth"),
            nested_method=getattr(args, "nested_method"),
            interval=getattr(args, "interval"),
            entrance_time=getattr(args, "entrance_time"),
            limits=getattr(args, "limits"),
            filter_expr=getattr(args, "filter_expr"),
        )
        return point
